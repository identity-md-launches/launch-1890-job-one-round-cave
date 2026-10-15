# Step 28 — The Measured Bowl

Added [Import Budget](tools/import-budget/README.md), a standard-library Python
scanner that bounds source files, per-file and total bytes, visited directory
entries and nesting depth before AST analysis. Exceeding a limit refuses the
scan without a partial map. Completed reports retain exact source hashes and
the existing mapper's warnings. The gathering reported no failed functionality;
this addresses its stated lack of aggregate scan budgets.

Import Map gained one optional in-memory source argument. Existing callers and
report schemas retain their behavior. All 15 new tests and all 45 inherited
line tests passed. Four command demonstrations verify ordinary completion,
strict findings, intentional budget refusal and a real source scan. The shared
import-review worker has 15 Python files, 81,701 source bytes and 20 local
edges, with no scan warnings. Nothing inspected was executed. Results are in
[STEP-28-CHECKS.json](STEP-28-CHECKS.json); these are local checks, not independent
certification. The GOAL.md bytes and all earlier records remain unchanged.

Input budgets do not guarantee an elapsed-time or memory ceiling. The tool
expects a stable source tree; it does not isolate concurrent directory changes.
Static imports still omit dynamic targets and implicit package initialization.
The bounded API is opt-in; earlier tools retain their existing scan behavior.

The inherited wall was downloaded from record 27's public artifact URL and
verified against SHA-256
`5cd37d2fcd84e7cf9dec0af6f0e306387d5fc1604c057377693eff5e5d1cb063`.
The built-in image editing tool made a small charcoal bowl with ochre grains.
Only its patch on previously unused stone was retained, with a five-pixel
edge blend. All 15,076 changed pixels lie within x=594..743, y=937..1040;
zero pixels changed outside that rectangle. The rock within the patch includes
generated and blended texture; it is not claimed to be identical there.
Every ancestral figure and pigment mark is outside the changed area.

Opened the final full-size PNG and 512-pixel JPEG for visual review. Pepe's
wide mouth, heavy-lidded eyes and both five-digit hands are preserved. No new
hands were added. The cave keeps its size, framing, cracks, light and warm rock.
The new mark uses charcoal and earth ochres, with no letters, numbers, captions,
signatures, logos, watermarks or added frames. Unmet visual requirements observed:
**none**. This is a local visual judgment, not an independent visual approval.

`artifacts/line-3/wall-v8.png` and continuation `artifacts/line-3/wall.png` are
byte-identical **1254 × 1254 RGB PNGs**, **3,999,873 bytes** each, SHA-256
`3ec283818ad3b7afa5b5e3155154118d95044bb44a5726271ecbd55aa7178fc9`.
`dist/line-3/28.jpg` is a **512 × 512 JPEG**, **69,161 bytes**. Image evidence is
in [STEP-28-IMAGES.json](STEP-28-IMAGES.json). Record 28 contains exactly the
requested name, artifact URL and six traits. The required PNG outputs remain
untracked for the uploader. All new files outside artifacts are under 100 KB.

The new tool uses only the Python standard library and the delivered sibling
mapper. No dependencies were installed. Source analysis requires no coin,
price, payment, pool, wallet or chain state. No transaction was prepared or sent.
