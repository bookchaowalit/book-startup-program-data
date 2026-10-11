# Upgrade plan — book-startup-program-data

Score: **7.5/10** (6 -> 7.5 in pass 1; unchanged in passes 2-4). Offline contract, adapters and CLI are tested and linted in GitHub Actions CI (green on `claude/untitled-session-bhlj06`, 2026-10-01); live capture, source permission and consumers remain unverified by design. Before pass 1: four generic sources untested, PRODUCT.md said one source; no CI.

## Backlog

- P1: Capture current cohort/application windows (Antler, EF) as `fixed` deadlines only
  when the page states an exact date and timezone.
- P1: Model AWS Activate credit tiers as `value.kind = credit` with explicit USD amounts.
- P1: Live-source monitoring (drift alerts) stays in the shared runtime; keep adapters pure.
- P2: Fill the PRODUCT.md acceptance-gate table only with evidence that exists (CI run link,
  replay report); do not mark gates passed without it.
- P2: Consider extracting the byte-identical `cli.py` shared by the sibling `book-*-data`
  products into one versioned package once a consumer exists (today each repo vendors it).

## Docs sync (2026-10-01)

- Closed P0 "confirm CI green": the `CI` run on `claude/untitled-session-bhlj06` passed on both Python versions (earlier ~5 s runs without job logs were runner start failures, not test failures).

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
  `SOLO_DATA_LAKE_ROOT`, CLI `validate` exit codes without echoing input, bad demo clock.
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

## Done in this pass (pass 3)

- Score unchanged; shared-CLI hardening only.
- Shared `cli.py` (same edit in all 13 sibling copies): `validate` now rejects NaN, ±Infinity and overflowing literals such as `1e400` (Python's json turns them into non-finite floats that JSON Schema `number` accepted); `timestamp` normalises fractional seconds so Python 3.10 accepts the same RFC3339 values as 3.11+ (it rejected e.g. `.1Z`) and only ASCII digits match; a trailing-dot `example.org.` host can no longer be claimed `live`.
- `tests/test_shared_cli.py` (byte-identical in all 13 repos) pins this repo's `cli.py` sha256 (three variants: base, +`contract --version`, +benefit availability) so a one-repo edit fails CI, and covers the fixes above across UTC/+07:00/-04:00 offsets. To change `cli.py`: edit every copy of the variant, then update `CLI_SHA256` in all 13 copies of the test.
- Not done (needs a reviewed live capture, so left blocked): stronger drift markers and any page-phrase extraction; no page phrases were invented.

## Done in this pass (pass 4: edge cases)

- Shared `cli.py` (all 13 copies, pins updated in `tests/test_shared_cli.py`):
  - `validate` accepted `" "` or a lone U+200B/BOM/soft hyphen as `id`,
    `title`, `provider` or `eligibility_text` (schema `minLength: 1` counts
    invisible characters); these are now rejected as blank.
  - Record ids that differ only by invisible characters or surrounding
    whitespace (`"x"` vs `"​x "`) are now reported as duplicates.
  - `demo --query` compared raw `casefold()` strings, so Thai SARA AM (`ำ`)
    did not match NIKHAHIT + SARA AA (either mark order), Thai digits did not
    match ASCII (`๒๕๖๙` vs `2569`), and full-width Latin (`ＵＫ`) or a stray
    zero-width space never matched; both sides are now NFKC-folded.
  - Verified: new `TextNormalisationTest` (all cases fail on the old code);
    full suite on Python 3.10 and 3.11; ruff 0.15.8 + 0.16.9.
