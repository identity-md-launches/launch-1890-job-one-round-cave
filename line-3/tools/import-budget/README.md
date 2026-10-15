# Import Budget

Map an unfamiliar Python source tree with explicit limits on files, bytes and
directory traversal. The tool collects a bounded snapshot, then passes those
exact bytes to the existing Import Map AST analyzer. It never runs inspected
source. An exceeded budget or read failure produces a refusal without a partial
map, so a missing edge cannot be mistaken for a completed collection.

Run from the repository root, offline, with Python 3.9 or newer:

```sh
python3 -B line-3/tools/import-budget/budget.py line-3/tools/import-map/examples
```

This command succeeds and shows four modules, three edges, one cycle and one
unresolved local import. The cycle and unresolved import are intentional example
findings. Add `--strict` to return exit 1 for map issues, cycles or recognized
dynamic import calls. No package installation or configuration is required.
Keep the sibling `import-map/import_map.py` when copying this tool elsewhere.

## Budgets and output

| Option | Default | What is counted |
| --- | ---: | --- |
| `--max-files` | 1,000 | All regular `.py` candidates, including shadowed sources and the root initializer |
| `--max-file-bytes` | 262,144 | Original bytes in each source file |
| `--max-total-bytes` | 8,388,608 | Original bytes across all candidates |
| `--max-entries` | 20,000 | Every entry encountered in visited directories, including non-Python entries |
| `--max-depth` | 64 | Directory nesting below the supplied root, which has depth zero |

Limits must be positive integers. Exact limits are accepted. Collection refuses
on the first exceeded limit; the reported observed count is a lower bound, not
the size of the full tree. Failure locations may depend on directory enumeration
order. Completed reports are sorted and deterministic for unchanged inputs.

`--json` returns `status`, `limits`, `inventory`, `map` and `scope`. The inventory
includes skipped-item counts and a sorted manifest of relative paths, byte
counts and SHA-256 hashes. Hashes identify the actual bytes analyzed, not an
authenticated source or an atomic snapshot of a changing tree. The nested `map`
retains the existing mapper's report schema, including all warnings.

Exit codes are 0 for a completed collection, 1 for a completed collection with
`--strict` findings, and 2 for invalid input, exceeded budgets or read/scan
failure. JSON failures contain only `status: "refused"` and an `error`, with
no map. Argument syntax errors use argparse's ordinary stderr output and exit 2.

Try an intentional refusal (exit 2):

```sh
python3 -B line-3/tools/import-budget/budget.py line-3/tools/import-map/examples --max-files 1 --json
```

## What was tried

All 15 behavioral checks passed, as did the 45 inherited line tests. Checks
cover exact boundaries and one-over failures for each budget, refusal before
any AST parsing, bounded reads when a file grows, snapshot reuse after source
changes, encoding declarations, collisions, parse warnings, symlinks, skipped
directories, FIFOs, read failures, outside-root refusal, strict exit behavior,
and source containing an execution trap that remains unexecuted.

```sh
python3 -B -m unittest discover -s line-3/tools/import-budget -v
```

A scan of the real shared import-review worker completed with 15 Python files,
81,701 source bytes, 23 visited directory entries, 15 modules and 20 local
edges, with no issues, cycles or recognized dynamic calls. Its exact report
and source hashes are in [observed-source.json](observed-source.json).
Reproduce that source-only scan:

```sh
python3 -B line-3/tools/import-budget/budget.py shared/import-drift --json --strict
```

## Limits of the result

The root must resolve inside the current working directory; choose an explicit
import root (`src/` when appropriate). Hidden directories, `.git`, `.hg`, `.svn`,
`__pycache__`, `.venv`, `venv` and `node_modules` are pruned before descent.
Symlinks and nonregular files are skipped, counted, and never intentionally
followed. Hidden `.py` files are included, matching the inherited mapper.

Use a stable tree. Final-component symlink and special-file replacement is
refused where the OS supports the relevant flags, but concurrent directory
replacement is not isolated. This is not a filesystem security sandbox.
Collection reads each source once, with at most one byte beyond the remaining
allowance to detect growth; over-budget bytes never reach the parser.

These are input-size limits, not precise RAM, CPU, output-size or elapsed-time
guarantees. The admitted byte snapshot and resulting graph remain in memory.
Python's AST parser retains its own resource limits. Implicit package startup,
runtime conditions, dynamic targets, installed-package resolution and external
callers remain outside the mapper's model. Collection completion does not mean
every source parsed successfully; inspect the preserved warnings. Existing
tools keep their old behavior unless they explicitly use this bounded scan.
