#!/usr/bin/env python3
"""Explain saved Endpoint/Deadline Sentry evidence without making requests."""
import argparse
import json
from pathlib import Path
import sys

MAX_BYTES = 1048576


class InvalidReport(ValueError):
    pass


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidReport('duplicate JSON key')
        result[key] = value
    return result


def load_report(path):
    # Explicit workspace paths only. No environment, home expansion or stdin.
    root = Path.cwd().resolve()
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(root):
        raise InvalidReport('input must be inside the current workspace directory')
    with resolved.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise InvalidReport('input exceeds 1 MiB')
    def invalid_constant(value):
        raise InvalidReport('non-finite JSON constant')
    def finite_number(value):
        import math
        number = float(value)
        if not math.isfinite(number):
            raise InvalidReport('non-finite JSON number')
        return number
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=invalid_constant, parse_float=finite_number)


ERRORS = {
    'dns': ('dns_resolution', 'Name resolution failed for this observation.',
            'Run TLS Route on the same public hostname to distinguish DNS from later stages.'),
    'tls': ('tls_handshake', 'The probe recorded a TLS error.',
            'Run TLS Route with hostname verification; review certificate validity and trust. Do not disable verification.'),
    'timeout': ('probe_timeout', 'The probe recorded a timeout; its exact blocked stage is not recorded.',
                'Use Deadline Sentry for a whole-process bound and TLS Route to isolate connection stages.'),
    'connect': ('connection', 'Connection setup failed; the report does not isolate TCP from every other setup error.',
                'Run TLS Route on the same hostname to separate DNS, TCP and TLS evidence.'),
    'headers': ('http_headers', 'No complete usable HTTP response headers were obtained.',
                'Compare TLS Route with a bounded Deadline Sentry observation; TLS success alone is insufficient.'),
    'body': ('response_body', 'Response capture was refused or failed after headers.',
             'Review the original error and byte limit, encoding and completeness; do not treat a partial digest as a full response.'),
    'json': ('json_decode', 'The captured response could not satisfy strict JSON decoding.',
             'Verify the documented response media type and API path; no response body is retained here.'),
    'json_pointer': ('json_path', 'The requested JSON pointer could not be resolved.',
                     'Compare the requested pointer with the API schema, including array indices and escaped keys.'),
    'deadline': ('watchdog_deadline', 'The watchdog killed its worker before a complete report; the blocked stage is unknown.',
                 'Use TLS Route for stage evidence; choose a larger bounded deadline only if the endpoint budget allows it.'),
    'arguments': ('probe_arguments', 'The worker refused the probe arguments.',
                  'Correct the original CLI arguments before probing again.'),
    'worker_start': ('worker_start', 'The watchdog could not start its worker.',
                     'Check the delivered Endpoint Sentry path and Python invocation inside this workspace.'),
    'worker_protocol': ('worker_protocol', 'The watchdog rejected the worker output or exit status.',
                        'Check that Deadline Sentry and Endpoint Sentry are compatible delivered versions.'),
}


def triage(report):
    if not isinstance(report, dict) or type(report.get('ok')) is not bool:
        raise InvalidReport('report needs boolean ok')
    schema = report.get('schema')
    if schema not in ('endpoint-sentry/v1', 'deadline-sentry/v1'):
        raise InvalidReport('unsupported report schema')
    original_ok = report['ok']
    prefix = ''
    if schema == 'deadline-sentry/v1' and 'probe' in report:
        probe = report['probe']
        if (not isinstance(probe, dict) or probe.get('schema') != 'endpoint-sentry/v1'
                or type(probe.get('ok')) is not bool or probe['ok'] != original_ok
                or 'error' in report):
            raise InvalidReport('wrapper contradicts or lacks a valid probe')
        report, prefix = probe, '/probe'
    elif schema == 'deadline-sentry/v1' and (original_ok or 'error' not in report):
        raise InvalidReport('watchdog without probe needs a failure error')

    findings = []
    def add(code, evidence, observation, next_step):
        findings.append(dict(code=code, evidence=prefix + evidence,
                             observation=observation, next_step=next_step))

    error = report.get('error')
    if 'error' in report:
        if (not isinstance(error, dict) or not isinstance(error.get('kind'), str)
                or not error['kind'] or not isinstance(error.get('message'), str)):
            raise InvalidReport('error needs string kind and message')
        if original_ok:
            raise InvalidReport('successful report contains an error')
        spec = ERRORS.get(error['kind'], ('unclassified_error',
            'The producer recorded an unrecognized error kind.',
            'Review the original producer report; no failing layer can be inferred.'))
        add(spec[0], '/error/kind', spec[1], spec[2])

    if report.get('schema') == 'endpoint-sentry/v1':
        checks, hops = report.get('checks'), report.get('hops')
        if not isinstance(checks, list) or not isinstance(hops, list):
            raise InvalidReport('probe needs checks and hops arrays')
        if len(checks) > 256 or len(hops) > 32:
            raise InvalidReport('report exceeds check/hop budget')
        for hop in hops:
            if (not isinstance(hop, dict) or type(hop.get('status')) is not int
                    or not 100 <= hop['status'] <= 599):
                raise InvalidReport('hop needs valid integer HTTP status')
        for index, check in enumerate(checks):
            if (not isinstance(check, dict) or not isinstance(check.get('name'), str)
                    or type(check.get('ok')) is not bool):
                raise InvalidReport('check needs name and boolean ok')
            if check['name'] == 'status':
                expected, actual = check.get('expected'), check.get('actual')
                if any(type(x) is not int or not 100 <= x <= 599 for x in (expected, actual)):
                    raise InvalidReport('status check needs valid expected and actual')
                if check['ok'] != (expected == actual) or not hops or hops[-1]['status'] != actual:
                    raise InvalidReport('status check contradicts evidence')
            if check['ok']:
                continue
            name = check['name']
            evidence = '/checks/' + str(index)
            if name == 'status':
                status = check['actual']
                if status == 404:
                    action = 'Verify the exact documented route; a missing route does not establish an origin outage.'
                elif status in (401, 403):
                    action = 'Check public access requirements. This anonymous probe cannot diagnose authenticated access.'
                elif status == 429:
                    action = 'Stop repeated probing and review published rate limits; this report contains no Retry-After evidence.'
                elif 500 <= status <= 599:
                    action = 'Compare a later bounded observation and service status; a single response does not prove the root cause.'
                elif 300 <= status <= 399:
                    action = 'Review redirect policy and the expected terminal status.'
                else:
                    action = 'Check the documented success status and the original expectation before changing either.'
                add('http_status', evidence,
                    'HTTP {} was observed; HTTP {} was expected.'.format(status, check['expected']), action)
            elif name == 'json_value':
                add('json_value', evidence, 'A resolved JSON value differed from the requested typed value.',
                    'Review the expected JSON value and API semantics; boolean and numeric expectations differ.')
            else:
                add('failed_check', evidence, 'A producer check failed.',
                    'Review the original named check; this tool does not infer an unsupported check meaning.')
        failed = any(not check['ok'] for check in checks)
        if original_ok and (failed or not checks or not any(c['name'] == 'status' for c in checks)):
            raise InvalidReport('success lacks passing status evidence')
        if not original_ok and not failed and error is None:
            raise InvalidReport('failure has neither failed checks nor an error')
    return {'schema': 'probe-triage/v1', 'source_schema': schema,
            'observed_ok': original_ok,
            'assessment': 'checks_passed' if original_ok else 'needs_attention',
            'findings': findings,
            'limits': ['Saved evidence only; no new request or retry was made.',
                       'A passing observation is not an availability, freshness or root-cause guarantee.',
                       'Evidence pointers refer to the original input document.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('report', help='saved JSON report within current workspace')
    parser.add_argument('--check', action='store_true', help='exit 1 for a valid failed observation')
    args = parser.parse_args(argv)
    try:
        result = triage(load_report(args.report))
    except (OSError, ValueError, RecursionError) as error:
        # Do not echo input paths or untrusted report text into diagnostics.
        print(json.dumps({'schema': 'probe-triage/v1', 'error':
                          'Invalid or unreadable report', 'kind': type(error).__name__}))
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 1 if args.check and not result['observed_ok'] else 0


if __name__ == '__main__':
    sys.exit(main())
