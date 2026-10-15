#!/usr/bin/env python3
"""Review Python import changes offline, without executing inspected source."""
import argparse
import csv
import io
import json
from pathlib import Path
import sys

import import_map
import reconcile
import review

FIELDS = ['module', 'path', 'entrypoint', 'local_imports', 'external_imports',
          'unresolved_imports', 'dynamic_import_lines', 'parse_errors']


def workspace_path(value):
    path = Path(value).resolve()
    if not path.is_relative_to(Path.cwd().resolve()):
        raise ValueError('input must resolve inside the current working directory')
    return path


def snapshot(root):
    root = workspace_path(root)
    if not root.is_dir():
        raise ValueError('snapshot root must be a directory')
    names = {}
    for path in import_map.source_files(root):
        name = import_map.module_name(path.relative_to(root))
        if name in names:
            raise ValueError(f'module name collision: {names[name]} and {path.relative_to(root)}')
        names[name] = path.relative_to(root)
    report = import_map.inspect(root)
    return render_snapshot(report), report


def render_snapshot(report):
    """Render an already collected map without reading source a second time."""
    if any(issue['type'] == 'module_collision' for issue in report['issues']):
        raise ValueError('module name collision cannot be represented by unique CSV keys')
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    for module in report['modules']:
        local, external, unresolved = set(), set(), set()
        for item in module['imports']:
            if item['kind'] in ('local', 'local_namespace'):
                local.add(item['resolved'])
            elif item['kind'] == 'external':
                external.add(item['target'])
            else:
                unresolved.add(item['target'])
        row = {'module': module['module'], 'path': module['path'],
               'entrypoint': 'true' if module['entrypoint'] else 'false'}
        for field, values in [('local_imports', sorted(local)),
                              ('external_imports', sorted(external)),
                              ('unresolved_imports', sorted(unresolved)),
                              ('dynamic_import_lines', module['dynamic_import_lines']),
                              ('parse_errors', [x for x in report['issues']
                                                if x['path'] == module['path']
                                                and x['type'] == 'parse_error'])]:
            row[field] = json.dumps(values, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'))
        writer.writerow(row)
    return stream.getvalue()


def compare(before, after):
    # Validate this schema before handing off to the generic reconciler.
    for value in (before, after):
        header, _, _ = reconcile.load_table(workspace_path(value), ('module',))
        if set(header) != set(FIELDS):
            raise ValueError('comparison requires import-drift/v1 snapshot columns')
    return reconcile.reconcile(before, after, ('module',))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    snap = commands.add_parser('snapshot', help='emit keyed CSV to stdout')
    snap.add_argument('root')
    diff = commands.add_parser('compare', help='reconcile two saved snapshots')
    diff.add_argument('before')
    diff.add_argument('after')
    diff.add_argument('--format', choices=('json', 'text', 'html'), default='json',
                      help='comparison format (default: json; html is a self-contained review)')
    args = parser.parse_args(argv)
    try:
        if args.command == 'snapshot':
            text, report = snapshot(args.root)
            sys.stdout.write(text)
            summary = dict(report['summary'])
            summary['schema'] = 'import-drift/v1'
            print(json.dumps(summary, sort_keys=True), file=sys.stderr)
            return 1 if report['issues'] or report['cycles'] else 0
        report = compare(args.before, args.after)
        if args.format == 'html':
            for chunk in review.iter_html(report):
                print(chunk)
        else:
            print(reconcile.render_text(report) if args.format == 'text' else
                  json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if report['equal'] else 1
    except (OSError, ValueError, RecursionError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
