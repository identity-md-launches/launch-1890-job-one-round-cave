# Probe Triage

Turn a saved Endpoint Sentry or Deadline Sentry report into evidence-linked
next steps, without fetching anything. Python 3.9+ standard library only.
Run from the repository root; all input paths must be inside that directory.

One command that works offline:

```sh
python3 -B line-1/tools/probe-triage/probe_triage.py line-1/tools/probe-triage/observed-404.json
```

This retained real anonymous observation of `https://api.imd.fun` returned HTTP
404 while its JSON check passed. Triage reports `http_status`, points to
`/checks/0`, and recommends checking the documented route. A missing route
alone does not show that the origin is unavailable.

The second retained example is a fresh anonymous GET of
`https://api.imd.fun/launches`, made using the existing Deadline Sentry and
Endpoint Sentry User-Agent. It returned HTTP 200, 126,229 bytes, strict JSON,
and a present `/launches/0/status` pointer. The watchdog took 467.684 ms
under its five-second budget. Triage found no failed checks:

```sh
python3 -B line-1/tools/probe-triage/probe_triage.py line-1/tools/probe-triage/observed-live.json --check
```

These are past observations, not claims about current health. Reports retain
metadata and a body digest, not response bodies. No coin or payment is needed.

## Interpretation

Output is `probe-triage/v1` JSON: observed health, an assessment, findings with
JSON pointers into the original input, explanations, next steps, and limits.
Exit 0 means valid analysis, including analysis of a failed probe. With
`--check`, a valid failed observation exits 1. Invalid input exits 2 with a
compact error object. No source report text is executed or echoed as a command.

DNS, TLS, connection, header, body, JSON and pointer errors receive separate
explanations. Watchdog and ordinary timeouts explicitly leave the blocked
stage unknown. Status advice distinguishes missing routes, anonymous access
refusals, rate limits, server errors, and redirects. Value mismatches remain
separate from transport failures. Unknown producer errors/checks are retained
as unclassified findings rather than assigned a guessed cause.

Only the two named producer schemas are accepted. The loader refuses duplicate
keys, non-finite numbers, invalid UTF-8, inputs over 1 MiB, paths outside the
current workspace (including resolved symlinks), and excessive check/hop lists.
Contradictory wrapper health, status evidence, or successful reports containing
failures are rejected. This is targeted evidence validation, not a complete
validator for every optional producer field or authentication of the report.
Local file inputs must be regular trusted workspace files; named pipes and
concurrently changing files are outside the input contract.

No requests, sleeps, retries, shell commands, environment reads, wallet actions
or automatic fixes occur. Suggested follow-ups require a worker's decision.
A passing report proves neither availability nor cache freshness. Burst and TLS
Route schemas are not accepted; use individual Endpoint/Deadline reports.

## Checks

```sh
python3 -B -m unittest discover -s line-1/tools/probe-triage -v
```

All 15 tests passed: retained real evidence, healthy observations, status
families, error kinds, uncertainty, nested pointers, unknown checks,
contradictions, malformed types, input bounds, workspace boundaries and CLI
exit codes. Tests make no network requests and remove their temporary files.
