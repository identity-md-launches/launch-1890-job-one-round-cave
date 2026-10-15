#!/usr/bin/env python3
"""Bound source collection before mapping Python imports, without running source."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys


DEFAULTS = {'files': 1000, 'file_bytes': 262144, 'total_bytes': 8388608,
            'entries': 20000, 'depth': 64}
SCOPE = ('Complete means collection finished within the stated budgets, not that '
         'runtime imports are known. Hidden and conventional dependency directories, '
         'symlinks and nonregular files are skipped. Explicit AST imports only; '
         'parse issues and dynamic calls remain visible. Use a stable source tree. '
         'These are input-size limits, not CPU, memory or elapsed-time guarantees.')


class BudgetExceeded(ValueError):
    def __init__(self, budget, limit, observed, path):
        self.evidence = {'type': 'budget_exceeded', 'budget': budget,
                         'limit': limit, 'observed': observed, 'path': path}
        super().__init__(f'{budget} budget {limit} exceeded at {path} (observed {observed})')


def load_mapper():
    path = Path(__file__).resolve().parents[1] / 'import-map' / 'import_map.py'
    spec = importlib.util.spec_from_file_location('line3_budget_mapper', path)
    mapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mapper)
    return mapper


def collect(root, limits, skip_dirs):
    """Collect bytes once; reject exceeded budgets before AST parsing begins."""
    if set(limits) != set(DEFAULTS):
        raise ValueError('limits must specify files, file_bytes, total_bytes, entries and depth')
    if any(type(value) is not int or value <= 0 for value in limits.values()):
        raise ValueError('all limits must be positive integers')
    workspace = Path.cwd().resolve()
    root = Path(root).resolve()
    if not root.is_relative_to(workspace) or not root.is_dir():
        raise ValueError('root must be an existing directory inside the current workspace')

    def check(key, observed, path):
        if observed > limits[key]:
            raise BudgetExceeded(key, limits[key], observed, path)

    inventory = {'files': 0, 'bytes': 0, 'entries': 0,
                 'skipped_symlinks': 0, 'skipped_directories': 0,
                 'skipped_nonregular': 0}
    pending, paths = [(root, 0)], []
    while pending:
        directory, depth = pending.pop()
        if directory.is_symlink() or not directory.resolve().is_relative_to(root):
            raise ValueError('directory changed during collection')
        children = []
        with os.scandir(directory) as entries:
            for entry in entries:
                inventory['entries'] += 1
                relative = (directory / entry.name).relative_to(root).as_posix()
                check('entries', inventory['entries'], relative)
                if entry.is_symlink():
                    inventory['skipped_symlinks'] += 1
                elif entry.is_dir(follow_symlinks=False):
                    if entry.name.startswith('.') or entry.name in skip_dirs:
                        inventory['skipped_directories'] += 1
                        continue
                    check('depth', depth + 1, relative)
                    children.append((Path(entry.path), depth + 1))
                elif entry.is_file(follow_symlinks=False):
                    if entry.name.endswith('.py'):
                        inventory['files'] += 1
                        check('files', inventory['files'], relative)
                        paths.append(relative)
                else:
                    inventory['skipped_nonregular'] += 1
        pending.extend(sorted(children, reverse=True))

    sources, manifest = {}, []
    for relative in sorted(paths):
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('source changed during collection: ' + relative)
        # Refuse a substituted symlink/FIFO where supported. Directory mutation
        # races are outside this tool's contract: this is not an OS sandbox.
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
        descriptor = os.open(path, flags)
        with os.fdopen(descriptor, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise ValueError('source is no longer a regular file: ' + relative)
            check('file_bytes', info.st_size, relative)
            check('total_bytes', inventory['bytes'] + info.st_size, relative)
            allowance = min(limits['file_bytes'], limits['total_bytes'] - inventory['bytes'])
            source = stream.read(allowance + 1)
        check('file_bytes', len(source), relative)
        check('total_bytes', inventory['bytes'] + len(source), relative)
        inventory['bytes'] += len(source)
        sources[relative] = source
        manifest.append({'path': relative, 'bytes': len(source),
                         'sha256': hashlib.sha256(source).hexdigest()})
    inventory['manifest'] = manifest
    return sources, inventory


def scan(root, limits=None, mapper=None):
    limits = dict(DEFAULTS if limits is None else limits)
    mapper = load_mapper() if mapper is None else mapper
    sources, inventory = collect(root, limits, mapper.SKIP_DIRS)
    report = mapper.inspect(Path(root), source_bytes=sources)
    return {'status': 'complete', 'limits': limits, 'inventory': inventory,
            'map': report, 'scope': SCOPE}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, help='explicit import root inside the current workspace')
    for name, value in DEFAULTS.items():
        parser.add_argument('--max-' + name.replace('_', '-'), type=int, default=value,
                            dest=name, help=f'maximum {name.replace("_", " ")} (default {value})')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--strict', action='store_true',
                        help='exit 1 for map issues, cycles or dynamic import calls')
    args = parser.parse_args(argv)
    mapper = load_mapper()
    try:
        result = scan(args.root, {name: getattr(args, name) for name in DEFAULTS}, mapper)
    except (OSError, ValueError, RuntimeError, RecursionError) as exc:
        error = (exc.evidence if isinstance(exc, BudgetExceeded) else
                 {'type': 'scan_error', 'detail': str(exc)})
        if args.json:
            print(json.dumps({'status': 'refused', 'error': error}, indent=2))
        else:
            print('import-budget: ' + str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        inventory = result['inventory']
        print(f"Collection complete: {inventory['files']} files, {inventory['bytes']} source bytes, "
              f"{inventory['entries']} directory entries")
        print(mapper.format_text(result['map']))
        print(SCOPE)
    report = result['map']
    warnings = (report['issues'] or report['cycles'] or
                any(module['dynamic_import_lines'] for module in report['modules']))
    return int(args.strict and bool(warnings))


if __name__ == '__main__':
    sys.exit(main())
