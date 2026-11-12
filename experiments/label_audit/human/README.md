# Human label check (100 pairs)

`make_sheet.py` samples 100 of the 313 open-only cross-author pairs behind the papers' main result (seed 0;
51 repositories) and writes:

- `label_sheet_A.xlsx`, `label_sheet_B.xlsx`: one per labeller. Instructions are on the first tab; the `label`
  column has a drop-down with six choices (yes - same change, yes - replacement, partly - one PR contains the
  other, no - related, no - unrelated, unclear).
- `pairs.csv`: the same 100 rows as plain CSV.
- `key_do_not_open.csv`: the Claude Haiku audit label for each row. Labellers should not open it.

Label independently, then run:

```bash
python agreement.py label_sheet_A.xlsx label_sheet_B.xlsx
```

It reports label precision (strict: duplicate or replacement; loose: also "partly"), Cohen's kappa between the two
labellers, and each labeller's kappa with the Haiku audit, and writes `agreement.json`.
