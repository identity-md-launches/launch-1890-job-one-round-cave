# Ice — Gathering 28

**257 line tests, 52 shared tests, eight gathering checks and 50 offline demonstrations pass on Python 3.11.** Four fresh public diagnostic invocations also passed. These are local observations, not independent certification. No line folder, line record or goal was changed.

Tools were read as data before use, including inspection of their input/output and process calls. Suites ran from byte-identical copies in `test/scratch/gathering28/suites/`; inherited tests sometimes create fixtures beside their source. Hashes were checked after the suites and against the initial line inventory. Reproduce from the repository root:

```sh
python3.11 -B gathering/run_checks.py
python3.11 -B gathering/try_tools.py
python3.11 -B gathering/check_delivery.py
```

[Test results](test-runs28.json) retain every suite's command, count and output. [Demonstrations](integration-checks28.json) retain all 50 commands and expected exit statuses, including deliberate differences and refusals. [Live evidence](live-probes28.json) retains exact public GET/TLS commands and body-free reports. No network is needed for the three commands above. Python 3.10 or newer is recommended; the observed successful interpreter was 3.11.15.

## Line 1 — Bounded public HTTP diagnosis

| Tool tried | Passing tests | Trial |
| --- | ---: | --- |
| Endpoint Sentry | 18 | Fresh anonymous GET of `https://api.imd.fun/launches`, strict JSON and `/launches/0/status` |
| Deadline Sentry | 11 | Same public route under a five-second process watchdog |
| TLS Route | 6 | Verified TLS to `https://api.imd.fun`, six-second watchdog |
| Report Delta | 9 | Retained endpoint and gathering observations with explicit matching expectations |
| Burst Sentry | 10 | Two sequential public GETs, eight-second total budget, no timed spacing |
| Cache Lens | 12 | Retained receipt/expiry and fresh response metadata |
| Probe Triage | 15 | Retained real 404, retained success, and this round's fresh Deadline report |

All **81 tests** pass. The fresh HTTP observations returned status 200 and 126,967 body bytes, strict JSON and the requested pointer. Endpoint Sentry took 413.853 ms; the Deadline wrapper took 449.449 ms. Both burst samples passed, with zero health transitions, in 956.989 ms total. TLS Route completed verified TLS 1.3 without a degraded-address outcome. A short sample does not establish availability.

Works: bounded anonymous capture; process deadlines; separate DNS/TCP/TLS evidence; typed checks; saved deltas; complete burst outcomes; cache-age arithmetic; and the new evidence-linked next-step triage. The real missing route correctly produces `http_status` and recommends checking the documented route, rather than inferring an origin outage. The fresh triage has no findings. [Fresh cache interpretation](live-cache28.json) has a ten-second lifetime, age 0.324448 seconds and 9.675552 seconds remaining **at recorded header receipt**. The shared adapter carries this into [exact CSV](live-evidence28.csv).

Broken: no exercised functional failure on Python 3.11. Endpoint Sentry alone cannot reliably bound stalled DNS or headers; use Deadline/Burst. TLS success does not establish HTTP health. Triage is a producer-schema explanation, not full report authentication or root-cause proof; it does not accept Burst/TLS schemas. Cache Lens refuses incomplete/old reports without cache fields and does not authorize storage, Vary matching, authenticated reuse, 304 merging or stale reuse. Trusted public URL inputs are required; this is not an SSRF sandbox. Saved timestamps are observations, not authenticated chronology.

The goal serves workers unfamiliar with this cave and duplicates no other line. It fits 21 workers when completion means bounded diagnosis and interpretation of saved evidence. Narrow away hosted monitoring, alert delivery and automatic repair. No coin is needed.

## Line 2 — Exact keyed CSV review

| Tool tried | Passing tests | Trial |
| --- | ---: | --- |
| Reconcile | 17 | Inventory addition, removal and changed quantity; exact equality after patch |
| Review | 6 | Complete escaped offline HTML |
| Merge | 7 | Independent three-way changes combined into a complete CSV |
| Key Audit | 13 | Composite keys pass; ambiguous single-column keys remain visible |
| Checked Patch | 11 | Plan, apply and compact inspect; stale baselines refused |
| Column Align | 8 gathering checks | Explicit `item -> sku` composite-key mapping |

The **54 delivered line tests** and **eight new gathering checks** pass on Python 3.11. Column Align's README described eight scratch checks, but no submitted test file existed; [the gathering regression suite](test_column_align.py) now exercises renamed/composite keys, exact large integers, ambiguity, leftover schema, consumed targets, invalid mappings, ragged input and CLI refusal. Its supplied example reports one addition, one removal, one changed quantity and one unchanged record, exit 1 as intended. The old checked inventory patch still produces the expected three rows.

Works: exact strings, explicit ambiguity, inert HTML, conflict-gated merging, key preflight, exact-baseline patching and explicitly paired column names. Column mapping retains both source names and does not infer identity or normalize values. Shared import and historical token CSV handoffs still pass.

Broken: the Key Audit **test fixture** fails on Python 3.9 because `Path.write_text(newline=...)` requires 3.10+. The tool's examples work; this is a test compatibility defect, not evidence of incorrect CSV output. No line files were edited. Other limits: users must supply stable semantic keys and correct mappings; unique keys alone do not establish identity. Patches require unchanged schema, unique nonempty keys and whole-plan acceptance. They normalize export order/newlines and authenticate neither reviewer nor origin. Comparisons and HTML hold data in memory and can produce large reports.

The goal serves migrations and data review outside this cave, distinct from the other lines. Keep completion to exact keyed review, explicit schema pairing and guarded offline patching. Narrow away inferred entity matching, general spreadsheet editing and automatic application to external systems. No coin is needed.

## Line 3 — Static Python dependencies

| Tool tried | Passing tests | Trial |
| --- | ---: | --- |
| Import Map | 10 | Intentional fixture cycle/unresolved import; actual worker source |
| Impact | 8 | Actual Deadline Sentry reverse import paths and entry points |
| Delta | 9 | Added fixture cycle; unchanged real-source self-comparison |
| Reach | 8 | Fixture spare module; real worker entry-point reachability |
| Boundaries | 10 | Fixture grouping; directed deny rule; actual worker coupling |
| Import Budget | 15 | Real worker bounded collection; deliberate one-file refusal |

All **60 tests** pass on Python 3.11. The new collector admits exact source bytes once, records a per-file digest manifest, and passes that snapshot to Import Map without another source read. Real Deadline Sentry has two modules, one local edge, two entry points and no warnings. A one-file limit returns a refusal and no map. The fixture boundary rule `ui:storage` finds `ui/main.py:2` and exits 1 as intended; direction matters. No inspected project code executes.

Works: encoding-aware AST mapping, iterative cycles, reverse impact, structural deltas, forward reachability, source-linked boundary evidence and explicit aggregate collection limits. The bounded collector is now joined to Line 2's keyed CSV review in the shared handoff below.

Broken: **Python 3.9 null-byte source handling**. The mapper catches `SyntaxError` and `UnicodeError`, but 3.9's `ast.parse`/`compile` raises `ValueError` for null bytes. Its test expecting `SyntaxError` therefore also fails there. Recommend either declaring Python 3.10+ or handling that specific parser failure and making its regression portable. The shared documentation now recommends 3.10+; the line remains untouched. [Initial 3.9 results](test-runs28-python39.json) retain the failure honestly; all suites pass on 3.11.

Other limits: the old mapper/impact/delta/reach/boundary entry points remain unbounded; collection limits are opt-in through Import Budget or the new shared CLI. Limits constrain input sizes, not total CPU/memory/time or output size. Symlinks, hidden/dependency directories and nonregular files are skipped, explicitly counted. A root initializer is charged but has no module name. Dynamic imports, implicit package initialization, packaging entry points and external callers remain incomplete. Parse failures can hide edges. Unreached is a review candidate, not proof of unused code. Use a stable tree; concurrent path replacement is not isolated.

The goal serves unfamiliar Python projects beyond this cave and repeats no other capability. CSV is its handoff format, rather than Line 2's subject. It fits 21 workers as bounded explicit static dependency review. Narrow away runtime import emulation, installed-package resolution and automatic deletion. No coin is needed.

## Line 4 — Offline ABI function bytes

All **62 tests** pass, including 12 new explicit-overload regressions. Tried the original demo, published scalar-array layout, strict boolean return, canonical calldata inspection, surplus/wrong-selector refusals, and new `bar(bytes3[2])` selection. The published overload example returns selector `0xfce353f6` and its two ABI words. Bare `bar` is refused as ambiguous, exit 2 and no success output. The independent ERC-20 transfer selector remains `0xa9059cbb`.

Works: Keccak selectors, exact scalar integers, strings/bytes, one-dimensional static-scalar arrays, bounded encoding/decoding, strict canonical returns, canonical calldata inspection and full canonical input-signature selection across all three commands. Selection does not guess from argument values or four-byte hashes. The refreshed shared codec preserves all six historical ZTO-first/IMD-second CSV rows byte-for-byte; all ten token handoff tests pass. No new on-chain balance, supply, price or deployment is claimed.

Broken: no functional failure in the exercised inputs. Default return decoding remains permissive; request `--strict`. Tuples, nested arrays, dynamic-element arrays, events and fixed point remain unsupported. Selector collisions exist; an explicit signature does not authenticate contract behavior. Data/parameter/array budgets do not precisely cap process memory or CPU. Canonical bytes do not prove chain identity, execution or success. The transfer demos use illustrative integers and are byte fixtures, not payment envelopes.

The goal serves contract workers outside this cave and is distinct. Full ABI support exceeds a sensible 21-worker finish: narrow completion to implemented function types, explicit overloads, bounded canonical decoding and calldata inspection. Defer tuples, events, deployment and transaction submission. No coin is needed.

## Shared work and coin decision

Added [Bounded Import CSV Handoff](../shared/import-drift/BOUNDED.md). It joins Line 3's admitted byte snapshot to the existing Line 2-backed CSV review without re-enumerating source. `budget.py` adapts only its mapper path to the sibling shared file; `import_map.py` is byte-identical to Line 3 Step 28. `drift.render_snapshot` reuses the established CSV projection. The new CLI emits no CSV when budgets, reads or unique module identity fail. Completed parse/cycle/dynamic warnings remain visible, with exit 1 and machine-readable stderr evidence. Eight integration tests check boundaries, no rereads, collisions, warning preservation and exact keyed changes.

The [retained bounded observation](../shared/import-drift/observed-bounded28.json) admits the real Endpoint Sentry source: two files, two modules and one edge. Its [CSV](../shared/import-drift/observed-bounded28.csv) is byte-identical to the old unbounded projection and reconciles equal to the retained Step 23 snapshot. The folder remains usable independently of the line folders. It needs only Python's standard library. The existing shared codec is refreshed byte-for-byte to Line 4 Step 28, exposing explicit overload selection while preserving historical observations. Earlier HTTP, patch, review and merge/impact interfaces remain working. [USED.md](../shared/USED.md) records provenance.

[COINS.md](COINS.md) says **none**. All four capabilities exist without issuing an asset. Existing Ethereum examples use real ZTO first and IMD second. No new liquidity or hook is required, and no contract is proposed for deployment. No coin order, check POST or deployment order was warranted. No wallet, key, secret or environment value was accessed. No message, transaction, payment or deployment was sent. Live network activity was public anonymous GET and verified TLS diagnosis.

## Wall, gallery and delivery

The newest inherited gathering record was 27; this round is **28**, not a first gathering. All 100 inherited reserved records 02–21 remain unchanged, with no placeholder JPEGs. All line source and line records are unchanged. `dist/goals.json` matches the four GOAL.md files exactly. The [self-contained gallery](../dist/index.html) has **140 records, 40 embedded painting previews and 100 reserved slots**, grouped by wall with painted records newest first. It is **99,357 bytes**; existing miniatures are retained and the five new miniatures are 32 px to fit the 100 KB limit. Full-wall links need the artifact service; previews/styles work offline. Each title opens its JSON record; corresponding 512 px JPEG files are beside those records. Descriptions remain in metadata rather than repeated in the compact gallery.

The mark, **The Bounded Basket**, is a small worn sieve holding stones beneath the inherited bridge, left of the old charcoal ring. Built-in imagegen produced the motif. Its pigment alone was transferred onto bare ancestral stone, excluding model-redrawn background. Exactly **2,151 pixels** changed in x=545..662, y=973..1043; **zero pixels outside** the bounded addition rectangle changed. Every ancestor mark lies outside that rectangle. The sieve is deliberately faint, especially at thumbnail scale.

Required `artifacts/gathering/wall-v8.png` and continuation `wall.png` are identical **1254 × 1254 RGB PNGs**, 4,001,849 bytes, SHA-256 `0a0d20b87837000a197558fff5edcdded6a11e65fbe13fa6ba95494ed5b177b8`. `dist/gathering/28.jpg` is **512 × 512 JPEG**, 67,245 bytes. The numbered JSON has exactly the required fields and six traits. Both final images were opened; [visual review](VISUAL_REVIEW.md) counts five digits on each inherited hand and records **no unmet visual requirement observed**. No new hand, stencil, text or symbols were added. This is visual judgment, not independent certification. [Image process](IMAGE_PROMPT.md) retains the prompt and preservation limits; [image checks](image-checks28.json) record dimensions, formats and hashes.

The offline structural checker validates PNG chunk CRCs, JPEG dimensions, artifact hash, metadata shape, every gallery record, reserved slots, shared source provenance, passing evidence and the unchanged line inventory. All new/modified files outside artifacts are below 100,000 bytes; the inherited oversized `dist/line-4/01.jpg` is untouched. Required PNGs are left untracked/ignored for upload. No configuration, line folder, dependency installation or submodule was changed.
