#!/usr/bin/env python3
"""Collect a bounded Python snapshot and hand exact import evidence to CSV review."""
import argparse
import json
import sys

import budget
import drift
import import_map


def snapshot(root, limits=None):
    result = budget.scan(root, limits, mapper=import_map)
    # Convert precisely the admitted AST report. Do not enumerate/read again.
    text = drift.render_snapshot(result['map'])
    report = result['map']
    evidence = {'schema': 'bounded-import-csv/v1', 'status': 'complete',
                'limits': result['limits'], 'inventory': result['inventory'],
                'summary': report['summary'], 'issues': report['issues'],
                'cycles': report['cycles'], 'dynamic_imports': [
                    {'module': m['module'], 'lines': m['dynamic_import_lines']}
                    for m in report['modules'] if m['dynamic_import_lines']],
                'scope': result['scope']}
    return text, evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('root', help='source root inside the current workspace')
    for name, default in budget.DEFAULTS.items():
        parser.add_argument('--max-' + name.replace('_', '-'), type=int,
                            default=default, dest=name)
    args = parser.parse_args(argv)
    try:
        text, evidence = snapshot(args.root, {k: getattr(args, k) for k in budget.DEFAULTS})
    except (OSError, ValueError, RuntimeError, RecursionError) as error:
        detail = (error.evidence if isinstance(error, budget.BudgetExceeded)
                  else {'type': 'snapshot_error', 'detail': str(error)})
        print(json.dumps({'schema': 'bounded-import-csv/v1', 'status': 'refused',
                          'error': detail}, ensure_ascii=True), file=sys.stderr)
        return 2
    # Success evidence and CSV only exist after the whole collection and
    # collision check pass. Exit 1 retains a completed map's semantic warnings.
    print(json.dumps(evidence, ensure_ascii=True, sort_keys=True), file=sys.stderr)
    sys.stdout.write(text)
    return int(bool(evidence['issues'] or evidence['cycles'] or evidence['dynamic_imports']))


if __name__ == '__main__':
    raise SystemExit(main())
