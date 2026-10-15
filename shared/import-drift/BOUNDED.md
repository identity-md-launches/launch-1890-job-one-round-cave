# Bounded Import CSV Handoff

Collect a Python source tree under explicit file, byte, entry and depth limits,
then export exactly the admitted import evidence to keyed CSV. This joins
Line 3's Import Budget with Line 2's exact CSV review. It uses Python 3.10+
and only the standard library, offline, without executing inspected source.
The complete shared folder works independently of the line folders.

One command from the repository root:

```sh
python3.11 -B shared/import-drift/bounded_snapshot.py line-1/tools/endpoint-sentry
```

Tried: exit 0, two files admitted, two modules, one local edge, no warnings.
CSV is byte-identical to the original unbounded projection. The per-file
manifest and limits are in [observed-bounded28.json](observed-bounded28.json);
[observed-bounded28.csv](observed-bounded28.csv) is its exact CSV output.
To see Line 2 review that handoff offline:

```sh
python3.11 -B shared/import-drift/checked_review.py shared/import-drift/observed-sentry23.csv shared/import-drift/observed-bounded28.csv --key module
```

Tried: exit 0, two unchanged module rows. These are source observations, not
proof of runtime dependency resolution or correct behavior.

The CLI writes CSV to stdout and one `bounded-import-csv/v1` JSON evidence
object to stderr. Redirect them separately to retain both. Defaults and flags:

| Flag | Default | Charged |
| --- | ---: | --- |
| `--max-files` | 1,000 | Regular Python candidates, including root initializer/shadowed modules |
| `--max-file-bytes` | 262,144 | Original bytes per source |
| `--max-total-bytes` | 8,388,608 | Original bytes across sources |
| `--max-entries` | 20,000 | All visited directory entries, including non-Python files |
| `--max-depth` | 64 | Directory nesting below the root |

Exit 0: complete collection without reported parse/import issues, cycles or
recognized dynamic imports. Exit 1: completed collection with those warnings;
CSV and stderr retain them for review. Exit 2: invalid input, budget/read
failure or module-name collision; stdout is empty and stderr is a refusal,
never a partial successful snapshot. Exact limits are accepted. The CLI must
finish collection and CSV validation before writing any success output.

`bounded_snapshot.snapshot(root, limits=None)` returns `(csv_text, evidence)`.
The collector reads admitted source once. Import Map parses its byte mapping;
`drift.render_snapshot` renders that same report. It does not reread the tree.
Manifest hashes identify collected bytes, not an atomic filesystem snapshot.
Symlinks, nonregular files and conventional hidden/dependency directories are
skipped and counted. The root initializer is charged but has no module name.
Colliding names are refused because one keyed CSV row cannot show both choices.

Limits constrain collection sizes, not exact CPU, memory, output size or
wall-clock duration. Use a stable source tree. Concurrent malicious filesystem
mutation is outside the contract. Dynamic loading, implicit initializers and
external callers remain incompletely modeled. Review warnings before inferring
absence of a dependency. Legacy `drift.py snapshot` and merge/impact commands
keep their original unbounded collection; use this new CLI to obtain limits.

Eight integration regressions pass, including no second reads, exact keyed
changes, collisions, refusal output, encodings and warning preservation:

```sh
python3.11 -B -m unittest discover -s shared/import-drift -p test_bounded_snapshot.py -v
```

The full shared import suite has 34 passing tests. Line 3's original mapper
is copied byte-for-byte; its null-byte handling/test fixture is incompatible
with Python 3.9. Use 3.10+ (verified on 3.11.15). No dependency install is needed.
