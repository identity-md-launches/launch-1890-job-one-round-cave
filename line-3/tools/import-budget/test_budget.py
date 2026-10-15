"""Behavior checks; temporary source trees live only in test/scratch."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location('budget_tool', Path(__file__).with_name('budget.py'))
B = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(B)


class BudgetTests(unittest.TestCase):
    def setUp(self):
        scratch = Path('test/scratch')
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.mapper = B.load_mapper()

    def put(self, name, source=b''):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(source if isinstance(source, bytes) else source.encode())
        return path

    def scan(self, **limits):
        return B.scan(self.root, dict(B.DEFAULTS, **limits), self.mapper)

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = B.main([str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_real_example_matches_original_mapper(self):
        root = Path(__file__).resolve().parents[1] / 'import-map/examples'
        result = B.scan(root)
        self.assertEqual(result['map'], self.mapper.inspect(root))
        self.assertEqual(result['map']['summary']['module_count'], 4)
        self.assertEqual(result['map']['cycles'], [['pkg.engine', 'pkg.helper']])
        self.assertEqual(result, B.scan(root))

    def test_exact_file_and_byte_limits_accept_then_refuse(self):
        self.put('a.py', b'import b\n')
        self.put('b.py', b'# hi\n')
        result = self.scan(files=2, file_bytes=9, total_bytes=14, entries=2)
        self.assertEqual(result['inventory']['bytes'], 14)
        self.assertEqual(result['map']['edges'], [{'from': 'a', 'to': 'b'}])
        for key, limit in [('files', 1), ('file_bytes', 8), ('total_bytes', 13), ('entries', 1)]:
            with self.subTest(key=key), self.assertRaises(B.BudgetExceeded) as raised:
                self.scan(**{key: limit})
            self.assertEqual(raised.exception.evidence['budget'], key)
            self.assertEqual(raised.exception.evidence['limit'], limit)

    def test_no_parsing_until_entire_collection_passes(self):
        self.put('a.py', 'import helper\n')
        self.put('z.py', '#' * 100)
        with mock.patch.object(self.mapper, 'inspect', side_effect=AssertionError('parsed early')):
            with self.assertRaises(B.BudgetExceeded):
                self.scan(file_bytes=32)

    def test_depth_and_non_python_entries_are_bounded(self):
        self.put('one/two/main.py', '')
        with self.assertRaises(B.BudgetExceeded) as raised:
            self.scan(depth=1)
        self.assertEqual(raised.exception.evidence['budget'], 'depth')
        self.assertEqual(self.scan(depth=2)['inventory']['files'], 1)
        self.put('note.txt', 'ignored content')
        with self.assertRaises(B.BudgetExceeded):
            self.scan(entries=3)

    def test_skip_directories_without_descending_and_skip_symlinks(self):
        self.put('main.py', '')
        self.put('.hidden/large.py', '#' * 200)
        self.put('node_modules/nested/large.py', '#' * 200)
        (self.root / 'linked.py').symlink_to(self.root / '.hidden/large.py')
        (self.root / 'linked_dir').symlink_to(self.root / '.hidden', target_is_directory=True)
        result = self.scan(files=1, file_bytes=1, entries=5)
        self.assertEqual(result['inventory']['skipped_symlinks'], 2)
        self.assertEqual(result['inventory']['skipped_directories'], 2)
        self.assertEqual(result['inventory']['files'], 1)

    def test_snapshot_is_exact_and_requires_no_second_read(self):
        path = self.put('a.py', b'import b\n')
        self.put('b.py', b'')
        sources, inventory = B.collect(self.root, B.DEFAULTS, self.mapper.SKIP_DIRS)
        path.write_bytes(b'import missing\n')
        with mock.patch.object(Path, 'read_bytes', side_effect=AssertionError('reread')):
            report = self.mapper.inspect(self.root, source_bytes=sources)
        self.assertEqual(report['edges'], [{'from': 'a', 'to': 'b'}])
        self.assertEqual(inventory['manifest'][0], {
            'path': 'a.py', 'bytes': 9, 'sha256': hashlib.sha256(b'import b\n').hexdigest()})

    def test_encoding_collision_and_parse_warnings_survive(self):
        self.put('main.py', b'\xef\xbb\xbfimport pkg\n')
        self.put('pkg.py', b'raise RuntimeError("never execute")\n')
        self.put('pkg/__init__.py', b'from . import helper\n')
        self.put('pkg/helper.py', b'# coding: latin-1\nNAME="caf\xe9"\n')
        self.put('bad.py', b'if :\n')
        result = self.scan()
        self.assertEqual(result['map'], self.mapper.inspect(self.root))
        self.assertEqual({x['type'] for x in result['map']['issues']},
                         {'module_collision', 'parse_error'})
        self.assertEqual(result['inventory']['files'], 5)
        self.assertEqual(result['map']['summary']['module_count'], 4)

    def test_cli_strict_warning_and_refusal_envelopes(self):
        self.put('a.py', 'import a\n__import__("unknown")\n')
        self.assertEqual(self.cli('--json')[0], 0)
        self.assertEqual(self.cli('--strict', '--json')[0], 1)
        code, out, err = self.cli('--json', '--max-file-bytes', '1')
        self.assertEqual((code, err), (2, ''))
        refused = json.loads(out)
        self.assertEqual(refused['status'], 'refused')
        self.assertEqual(refused['error']['budget'], 'file_bytes')
        self.assertNotIn('map', refused)
        code, out, err = self.cli('--max-file-bytes', '1')
        self.assertEqual((code, out), (2, ''))
        self.assertIn('file_bytes budget', err)

    def test_source_is_never_executed(self):
        marker = self.root / 'executed'
        self.put('main.py', f'open({str(marker)!r}, "w").write("ran")\n'
                 'import helper\nif __name__ == "__main__": pass\n')
        self.put('helper.py', 'raise RuntimeError("never run")\n')
        self.assertEqual(self.scan()['map']['summary']['entrypoints'], ['main'])
        self.assertFalse(marker.exists())

    def test_empty_tree_and_root_initializer_budget(self):
        self.assertEqual(self.scan()['inventory']['files'], 0)
        self.put('__init__.py', b'# root initializer\n')
        result = self.scan()
        self.assertEqual(result['inventory']['files'], 1)
        self.assertEqual(result['map']['summary']['module_count'], 0)

    def test_invalid_limits_and_outside_root_rejected_before_enumeration(self):
        for key in B.DEFAULTS:
            for invalid in (0, -1, True, 1.5):
                with self.subTest(key=key, invalid=invalid), self.assertRaises(ValueError):
                    self.scan(**{key: invalid})
        with mock.patch.object(B.os, 'scandir', side_effect=AssertionError('enumerated')):
            with self.assertRaisesRegex(ValueError, 'inside the current workspace'):
                B.collect(Path('/not-a-workspace-root'), B.DEFAULTS, self.mapper.SKIP_DIRS)
        code, out, _ = self.cli('--max-files', '0', '--json')
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out)['error']['type'], 'scan_error')

    def test_oversized_file_is_refused_before_read(self):
        self.put('large.py', '#' * 100)
        real_fdopen = B.os.fdopen
        class ReadTrap:
            def __init__(self, *args):
                self.stream = real_fdopen(*args)
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.stream.close()
            def fileno(self):
                return self.stream.fileno()
            def read(self, *args):
                raise AssertionError('oversized source was read')
        with mock.patch.object(B.os, 'fdopen', side_effect=ReadTrap) as opened:
            with self.assertRaises(B.BudgetExceeded):
                self.scan(file_bytes=20)
            self.assertEqual(opened.call_count, 1)

    def test_io_failure_refuses_without_partial_map(self):
        self.put('a.py', 'import b\n')
        with mock.patch.object(B.os, 'open', side_effect=PermissionError('source unavailable')):
            code, out, err = self.cli('--json')
        self.assertEqual((code, err), (2, ''))
        result = json.loads(out)
        self.assertEqual(result['status'], 'refused')
        self.assertEqual(result['error']['type'], 'scan_error')
        self.assertNotIn('map', result)

    def test_growing_file_still_has_a_bounded_read(self):
        self.put('a.py', '#' * 100)
        real_fstat = os.fstat
        def stale_size(fd):
            data = list(real_fstat(fd))
            data[6] = 1
            return os.stat_result(data)
        with mock.patch.object(B.os, 'fstat', side_effect=stale_size):
            with self.assertRaises(B.BudgetExceeded) as raised:
                self.scan(file_bytes=10)
        self.assertEqual(raised.exception.evidence['observed'], 11)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'requires POSIX FIFO')
    def test_nonregular_sources_are_not_opened(self):
        os.mkfifo(self.root / 'pipe.py')
        with mock.patch.object(B.os, 'open', side_effect=AssertionError('opened FIFO')):
            result = self.scan()
        self.assertEqual(result['inventory']['skipped_nonregular'], 1)
        self.assertEqual(result['inventory']['files'], 0)


if __name__ == '__main__':
    unittest.main()
