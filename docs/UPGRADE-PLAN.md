# Upgrade plan — book-startup-program-data

Score: 6/10 -> 7.5/10 (pass 1) -> 7.5/10 (pass 2) — four generic sources untested, PRODUCT.md said one source; no CI.

## Backlog

- P0: Confirm the new GitHub Actions CI is green on the first push and keep it required.
- P1: Capture current cohort/application windows (Antler, EF) as `fixed` deadlines only
  when the page states an exact date and timezone.
- P1: Model AWS Activate credit tiers as `value.kind = credit` with explicit USD amounts.
- P1: Live-source monitoring (drift alerts) stays in the shared runtime; keep adapters pure.
- P2: Fill the PRODUCT.md acceptance-gate table only with evidence that exists (CI run link,
  replay report); do not mark gates passed without it.
- P2: Consider extracting the byte-identical `cli.py` shared by the sibling `book-*-data`
  products into one versioned package once a consumer exists (today each repo vendors it).

## Done in this pass (pass 1)

- Added tests for the four generic sources (normalize + script-hidden markers rejected);
  moved the misplaced `normalize` docstring.
- PRODUCT.md: source list and evidence boundary now match the five enabled sources.
- Added `.github/workflows/ci.yml`: Python 3.10/3.12 matrix, `pip install -e ".[dev]"`,
  `ruff check .`, `pytest`, and a `contract`/`validate`/`demo` CLI smoke. Verified by
  replaying those steps in a clean Python 3.10 venv.
- Added `[project.optional-dependencies] dev`, pytest config (`pythonpath = src`) and an
  explicit ruff rule set (E4/E9/F/I/B/UP); fixed the resulting import-order/encode lint.
- Added `tests/test_policy.py`: `sources.json` ↔ `source*.json` ↔ schema category
  consistency, duplicate policy copies identical, https/no-query URLs, 6h minimum
  interval, `--source-id` traversal rejection, capture fail-closed without
  `SOLO_EMPIRE_ROOT`, CLI `validate` exit codes without echoing input, bad demo clock.
- README: documented the developer/CI commands and offline test boundary.

## Done in this pass (pass 2)

- Data fix: the Google for Startups Accelerator record claimed `startup_stage: "any"` while
  the page says "ideally from Seed to Series A"; no single contract stage fits, so it is now
  `null` (not asserted). Regression assertion added.
- Drift guard: the HTML text extractor now also ignores `<noscript>` and `<svg>` (as the
  sibling creator/deal/learning/mobility/paid-study/partnership adapters do), so markers
  hidden there no longer pass; test covers all four hidden containers.
- Remaining P1s (cohort windows, AWS credit tiers) need reviewed live page content; not
  attempted offline. `source.json` stays content-identical to
  `source-google-startups-accelerator-us.json` (asserted by `tests/test_policy.py`).
