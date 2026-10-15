"""Check bounded collection through the existing CSV review interface."""
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import bounded_snapshot as bounded
import budget
import drift
import import_map
import reconcile


class BoundedSnapshotTests(unittest.TestCase):
    def setUp(self):
        scratch = Path('test/scratch')
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'main.py').write_text('import helper\nif __name__ == "__main__": pass\n')
        (self.root / 'helper.py').write_text('raise RuntimeError("never execute")\n')

    def cli(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = bounded.main([str(self.root), *args])
        return code, stdout.getvalue(), json.loads(stderr.getvalue())

    def test_same_csv_as_original_with_manifest(self):
        text, evidence = bounded.snapshot(self.root)
        self.assertEqual(text, drift.snapshot(self.root)[0])
        self.assertEqual(evidence['inventory']['files'], 2)
        self.assertEqual(evidence['summary']['local_edge_count'], 1)
        self.assertEqual([m['path'] for m in evidence['inventory']['manifest']],
                         ['helper.py', 'main.py'])
        self.assertEqual(self.cli()[0], 0)

    def test_no_second_enumeration_or_source_read(self):
        with mock.patch.object(import_map, 'source_files', side_effect=AssertionError('enumerated twice')):
            with mock.patch.object(Path, 'read_bytes', side_effect=AssertionError('source reread')):
                text, _ = bounded.snapshot(self.root)
        self.assertEqual(len(list(csv.DictReader(io.StringIO(text)))), 2)

    def test_refusal_has_no_csv_or_partial_manifest(self):
        code, text, evidence = self.cli('--max-files', '1')
        self.assertEqual((code, text, evidence['status']), (2, '', 'refused'))
        self.assertEqual(evidence['error']['budget'], 'files')
        self.assertNotIn('inventory', evidence)

    def test_collision_refused_before_csv_export(self):
        (self.root / 'helper').mkdir()
        (self.root / 'helper/__init__.py').write_text('')
        code, text, evidence = self.cli()
        self.assertEqual((code, text), (2, ''))
        self.assertIn('collision', evidence['error']['detail'])

    def test_changed_source_reconciles_by_module(self):
        before, _ = bounded.snapshot(self.root)
        (self.root / 'helper.py').write_text('import csv\n')
        after, _ = bounded.snapshot(self.root)
        a, b = self.root / 'before.csv', self.root / 'after.csv'
        a.write_text(before); b.write_text(after)
        result = reconcile.reconcile(a, b, ['module'])
        self.assertEqual(result['summary']['changed'], 1)
        self.assertEqual(result['changed'][0]['key'], {'module': 'helper'})

    def test_parse_dynamic_and_cycle_warnings_remain_visible(self):
        for source, finding in [('def broken(\n', 'issues'),
                                ('__import__("x")\n', 'dynamic_imports'),
                                ('import helper\n', 'cycles')]:
            (self.root / 'helper.py').write_text(source)
            code, text, evidence = self.cli()
            self.assertEqual(code, 1)
            self.assertTrue(evidence[finding])
            self.assertEqual(len(list(csv.DictReader(io.StringIO(text)))), 2)

    def test_input_boundaries_and_symlink_skip(self):
        (self.root / 'link.py').symlink_to(self.root / 'main.py')
        _, evidence = bounded.snapshot(self.root)
        self.assertEqual(evidence['inventory']['skipped_symlinks'], 1)
        with self.assertRaises(ValueError):
            bounded.snapshot(Path.cwd().parent)
        with self.assertRaises(ValueError):
            bounded.snapshot(self.root, dict(budget.DEFAULTS, files=0))

    def test_encoding_and_root_initializer_counted(self):
        (self.root / 'helper.py').write_bytes(b'# coding: latin-1\nname="caf\xe9"\n')
        (self.root / '__init__.py').write_bytes(b'# counted, root has no module name\n')
        text, evidence = bounded.snapshot(self.root)
        self.assertEqual(evidence['inventory']['files'], 3)
        self.assertEqual(evidence['summary']['module_count'], 2)
        self.assertEqual(text, drift.snapshot(self.root)[0])


if __name__ == '__main__':
    unittest.main()
