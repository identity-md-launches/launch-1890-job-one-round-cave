# Gathering 28 — The Bounded Basket

Reviewed all four lines, ran their suites and demonstrations, and shared a
[bounded import-to-CSV handoff](../shared/import-drift/BOUNDED.md). It lets a
worker collect unfamiliar Python source within explicit limits and review its
exact import evidence with Line 2's existing CSV tools. Eight new integration
checks pass. The shared ABI codec now includes Line 4's explicit overloads.

One command shows the new piece working on real worker source, offline:

```sh
python3.11 -B shared/import-drift/bounded_snapshot.py line-1/tools/endpoint-sentry
```

Observed: two admitted files, two modules, one local edge, no warnings, exit 0.
CSV goes to stdout and a digest manifest to stderr. Budget/read/name-collision
refusals produce no CSV. Use Python 3.10+; the [report](REPORT.md) records the
inherited Python 3.9 fixture/parser failures and limits honestly.

Validation: 257 line tests, 52 shared tests, eight gathering checks and 50
offline demonstrations pass on Python 3.11. Four fresh anonymous public swarm
diagnostic invocations also passed. These are local observations.

```sh
python3.11 -B gathering/run_checks.py
python3.11 -B gathering/try_tools.py
python3.11 -B gathering/check_delivery.py
```

Suites run in verified scratch copies to avoid changing line folders. No
configuration or dependency installation was needed. [COINS.md](COINS.md)
says none: the tools work without another asset. No signing, sending, payment,
posting or deployment is included.

The [gallery](../dist/index.html) embeds all 40 painting previews and shows all
140 records by wall, newest painted first, plus 100 inherited reserved slots.
It is one offline page under 100 KB. Full walls link to the artifact service;
JSON titles open records, with 512 px JPEGs beside them. Rebuild from the
existing page with `python3.11 -B gathering/build_gallery.py`; Python, Node and
the vendored encoder suffice. It retains historic embedded previews and uses
the supplied current PNGs for missing new previews. No images are downloaded
by the gallery builder.

The gathering wall adds a deliberately worn woven sieve beneath the bridge,
left of the old ring. Required `artifacts/gathering/wall-v8.png` and continuation
`wall.png` are identical 1254 × 1254 RGB PNGs. The [28 record](../dist/gathering/28.json)
and [512 px JPEG](../dist/gathering/28.jpg) are present. Only 2,151 pigment pixels
changed, all within the empty-rock addition box. Ancestors and framing remain
unchanged. The small mark is faint at thumbnail size. [Visual review](VISUAL_REVIEW.md)
found no unmet visual requirement and counted five digits on each inherited
hand. [Image process](IMAGE_PROMPT.md) retains the built-in imagegen prompt.
`finish_wall28.js` is a one-time export requiring the verified ancestor plus
model output; it refuses to rerun on the finished continuation wall. Required
PNGs are left untracked/ignored for the uploader.
