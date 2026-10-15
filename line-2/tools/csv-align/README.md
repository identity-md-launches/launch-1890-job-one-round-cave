# CSV Column Align

This Python 3.10+ standard-library tool reconciles two workspace-local CSV
exports by stable keys when some column headers changed. A worker explicitly
pairs each renamed header with `--map BEFORE AFTER`. Unmapped columns stay
visible as schema additions or removals. Values remain exact strings; the
tool never guesses that two different headers mean the same thing.

From the repository root, one command shows it working:

```sh
python3 -B line-2/tools/csv-align/align.py line-2/tools/csv-align/demo-before.csv line-2/tools/csv-align/demo-after.csv --key item --key location --map item sku
```

The JSON report identifies the key pair `item`/`sku`, one added row, one
removed row, one quantity change, and one unchanged row. Exit status 1 means
there is a difference; 0 means equal after the declared mapping; 2 means
invalid input. The report retains original column names and logical CSV
record numbers on both sides. Ambiguous duplicate keys include every
conflicting row and are never paired automatically. `complete: false` flags
that ambiguity.

Use `--key` again for every component of a composite key and `--map` again
for every explicit column pair. Names given to `--key` are from the before
CSV. Same-named columns pair automatically unless an explicit mapping has
already consumed the after column. Mapping sources and targets must each be
unique. A key without a distinct matching column is refused. A renamed
column with unchanged values is treated as equal *after* the explicit pair;
the pair remains in `schema.paired_columns` for review.

The tool reuses the existing [CSV Reconcile](../csv-reconcile/README.md)
bounded reader. Each CSV must be UTF-8, at most 16 MiB and 100,000 data
records, with unique nonempty headers and no ragged records; every value is
kept as a string. Paths must resolve inside the current working directory.
The whole report is written to stdout, with no network access or file writes.
The report can be large for a large dataset, and the tables are held in
memory. Key uniqueness proves only a syntactic match, not that two exports
refer to the same real entity. Review the mapping before relying on it.

## What happened when tried

Eight focused checks in `test/scratch/line2-step28/` passed: renamed and
composite keys, exact large integers, schema leftovers, duplicate ambiguity,
mapping collisions, missing targets, and malformed rows. The command above
returned exit 1 with the expected 1 added, 1 removed, 1 changed and 1
unchanged row. No coin or chain access is needed for this offline operation.
