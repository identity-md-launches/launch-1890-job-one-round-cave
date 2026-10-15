import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import probe_triage as t


def good():
    return {'schema': 'endpoint-sentry/v1', 'ok': True,
            'hops': [{'status': 200}], 'checks': [
                {'name': 'status', 'ok': True, 'expected': 200, 'actual': 200}]}


def status(value):
    report = good()
    report['ok'] = False
    report['hops'][0]['status'] = value
    report['checks'][0].update(ok=False, actual=value)
    return report


class TriageTests(unittest.TestCase):
    def test_real_missing_route(self):
        report = t.load_report(Path(__file__).parent / 'observed-404.json')
        result = t.triage(report)
        self.assertEqual(result['findings'][0]['code'], 'http_status')
        self.assertIn('route', result['findings'][0]['next_step'])
        self.assertFalse(result['observed_ok'])

    def test_success_not_availability(self):
        result = t.triage(good())
        self.assertEqual(result['assessment'], 'checks_passed')
        self.assertEqual(result['findings'], [])
        self.assertIn('availability', result['limits'][1])

    def test_status_actions(self):
        for value, hint in [(401, 'anonymous'), (403, 'anonymous'),
                            (429, 'rate limits'), (503, 'single response'),
                            (301, 'redirect'), (201, 'documented')]:
            with self.subTest(value=value):
                result = t.triage(status(value))
                self.assertIn(hint, result['findings'][0]['next_step'])

    def test_connect_does_not_assert_tcp(self):
        report = good()
        report.update(ok=False, checks=[], hops=[], error={'kind': 'connect', 'message': 'x'})
        self.assertIn('does not isolate', t.triage(report)['findings'][0]['observation'])

    def test_error_kinds(self):
        for kind, spec in t.ERRORS.items():
            report = good()
            report.update(ok=False, checks=[], hops=[], error={'kind': kind, 'message': 'x'})
            self.assertEqual(t.triage(report)['findings'][0]['code'], spec[0])

    def test_unknown_error_conservative(self):
        report = good()
        report.update(ok=False, error={'kind': 'future-kind', 'message': 'x'})
        self.assertEqual(t.triage(report)['findings'][0]['code'], 'unclassified_error')

    def test_watchdog_timeout_has_no_invented_stage(self):
        report = {'schema': 'deadline-sentry/v1', 'ok': False,
                  'error': {'kind': 'deadline', 'message': 'killed'}}
        finding = t.triage(report)['findings'][0]
        self.assertEqual(finding['evidence'], '/error/kind')
        self.assertIn('unknown', finding['observation'])

    def test_wrapper_evidence_pointer(self):
        report = {'schema': 'deadline-sentry/v1', 'ok': False, 'probe': status(404)}
        self.assertEqual(t.triage(report)['findings'][0]['evidence'], '/probe/checks/0')

    def test_value_failure_and_unknown_check(self):
        report = good()
        report['ok'] = False
        report['checks'] += [{'name': 'json_value', 'ok': False},
                             {'name': 'future-check', 'ok': False}]
        self.assertEqual([x['code'] for x in t.triage(report)['findings']],
                         ['json_value', 'failed_check'])

    def test_contradictions_refused(self):
        cases = []
        r = good(); r['checks'][0]['ok'] = False; cases.append(r)
        r = good(); r['hops'][0]['status'] = 404; cases.append(r)
        r = good(); r['ok'] = False; cases.append(r)
        r = good(); r['checks'] = []; cases.append(r)
        r = good(); r['error'] = {'kind': 'dns', 'message': 'x'}; cases.append(r)
        cases.append({'schema': 'deadline-sentry/v1', 'ok': False, 'probe': good()})
        for report in cases:
            with self.subTest(report=report), self.assertRaises(t.InvalidReport):
                t.triage(report)

    def test_malformed_types_and_budgets(self):
        for field, value in [('ok', 1), ('hops', [{}]), ('hops', [{'status': True}]),
                             ('checks', [{'name': 'json', 'ok': 1}]),
                             ('checks', [{}] * 257), ('schema', 'burst-sentry/v1'),
                             ('error', None)]:
            report = good(); report[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(t.InvalidReport):
                t.triage(report)

    def test_strict_loader(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
            path = Path(folder) / 'report.json'
            for raw in [b'{"ok":true,"ok":false}', b'{"x":NaN}',
                        b'{"x":1e9999}', b'[]' * 600000, b'\xff']:
                path.write_bytes(raw)
                with self.subTest(raw=raw[:30]), self.assertRaises(ValueError):
                    t.load_report(path)

    def test_workspace_boundary_without_read(self):
        with self.assertRaises(t.InvalidReport):
            t.load_report(Path.cwd().parent / 'not-read.json')

    def test_cli_exit_codes(self):
        script = str(Path(__file__).with_name('probe_triage.py'))
        fixture = str(Path(__file__).with_name('observed-404.json'))
        for flags, expected in [([], 0), (['--check'], 1)]:
            result = subprocess.run([sys.executable, '-B', script, fixture] + flags,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, expected, result.stderr)
            self.assertEqual(json.loads(result.stdout)['assessment'], 'needs_attention')
        result = subprocess.run([sys.executable, '-B', script, script], capture_output=True,
                                text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['error'], 'Invalid or unreadable report')

    def test_no_input_mutation(self):
        report = status(404); before = copy.deepcopy(report)
        t.triage(report)
        self.assertEqual(report, before)


if __name__ == '__main__':
    unittest.main()
