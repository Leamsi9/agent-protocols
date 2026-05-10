# Citation Verification Protocol

Use this protocol when an operator asks to verify citations, references,
quotations, or source support for a research document.

This protocol is intentionally format-tolerant but evidence-strict. It can be
used for LaTeX, Markdown, Quarto, Pandoc-generated manuscripts, white papers,
reports, grant proposals, and similar research artefacts. It does not assume
that the document is already correct. It proceeds through gated levels and does
not advance from one level to the next until the current level is green.

If the verification work is non-trivial, run it under the
[Substantive Work Protocol](substantive-work-protocol.md). Create a dedicated
branch and branch-owned worktree in the repo that owns the research artefact,
then add a durable plan and adjacent `.plan.toml` manifest for the citation
audit.

## Core Rule

Treat source verification as a ledgered evidence process, not a narrative
impression.

Do not advance, report completion, or say that all citations are valid unless
the relevant deterministic gate passes. If a source cannot be accessed, the row
is `blocked`. If a source is online but metadata or claim support is not yet
checked, the row is `todo`, `online`, or `needs_review`, and the gate remains
red.

## Inputs

Identify these paths before starting:

- one or more source documents, such as `.tex`, `.md`, `.qmd`, `.rst`, or `.docx`
  exports;
- one or more bibliography files, usually `.bib`;
- any rendered reference list if the source document has already been
  CSL-rendered and no longer contains machine-readable citation commands;
- the expected style of citation keys, if non-standard;
- any access limitations, such as paywalls, institutional portals, or local PDF
  copies.

When possible, prefer primary sources, publisher pages, official report pages,
DOIs, arXiv/OpenReview/SSRN records, official company/institution pages, and
catalogue or ISBN pages for books. Use media, relay pages, analyst pages, or
third-party summaries only at the evidence tier appropriate to the manuscript's
claim.

## Artifacts

Use these repo-local artefacts for each audit:

- durable plan: `docs/plans/<slice>.md`;
- phase manifest: `docs/plans/<slice>.plan.toml`;
- temporary audit ledger: `docs/temp/citation-source-audit.md`;
- optional metadata overrides: `docs/temp/citation-metadata-overrides.toml`;
- source-content ledger: `docs/temp/citation-content-support.toml`;
- optional quote ledger if not stored in the source-audit table:
  `docs/temp/citation-quote-support.toml`.

The temporary ledgers are working evidence. At closeout, either preserve them as
review evidence if the audit remains useful, or fold the durable findings into
the plan and delete the temporary files per the
[Temp Doc Protocol](temp-doc-protocol.md).

## Status Vocabulary

Use these statuses consistently:

- `verified`: checked and supported by evidence;
- `not_applicable`: the level does not apply to this row, for example a source
  has no source-attributed quotation;
- `online`: a URL resolves but exact metadata has not been reviewed;
- `needs_review`: a lookup resolves but conflicts or fuzzy matching require
  manual review;
- `blocked`: source access failed, metadata contradicted the local entry, or the
  claim is not supported;
- `todo`: not checked yet.

Only `verified` and `not_applicable` are final passing statuses. For metadata
and content support, `not_applicable` should be rare and explained.

## Level 1: Local Citation Inventory

Goal: prove that every machine-readable citation in the research source maps to
a bibliography entry, and that the bibliography is internally coherent.

Checks:

- parse all bibliography entries;
- detect duplicate keys;
- extract machine-readable citations from the source documents;
- detect `\nocite{*}` when a LaTeX manuscript relies on prose author-year
  citations rather than explicit `\cite{}` calls;
- list bibliography entries without DOI, URL, ISBN, or other direct locator;
- fail if any explicit citation key is absent from the bibliography;
- fail if required local fields are missing.

Recommended command:

```bash
python3 agent-protocols/scripts/citation_inventory.py \
  --source manuscript.tex \
  --bib references.bib \
  --require-nocite-all
```

Use `--require-nocite-all` only when the document intentionally includes all
bibliography entries through `\nocite{*}` or equivalent prose-citation workflow.
If a rendered document has no machine-readable citation keys, record that
limitation in the plan and verify the visible reference list manually before
moving to Level 2.

Exit gate: the inventory command exits green and produces a count of
bibliography entries, extracted citation keys, missing keys, duplicate keys, and
locatorless rows.

## Level 2: Online Existence and Metadata

Goal: verify that every bibliography entry exists online and is correctly named,
attributed, dated, and cited.

Checks:

- DOI entries resolve through Crossref, DataCite, arXiv DOI, or publisher pages;
- arXiv URLs resolve through the arXiv API or page metadata;
- URL entries resolve to the cited primary, publisher, official, or accepted
  evidence page;
- locatorless book/report entries receive a manual locator in the audit ledger
  or metadata override file;
- title, year, authorship/owner, venue, and source type agree with the online
  record;
- weak, stale, or working-title entries are corrected in the bibliography before
  the gate passes.

Recommended generator:

```bash
python3 agent-protocols/scripts/citation_build_source_audit.py \
  --bib references.bib \
  --metadata-overrides docs/temp/citation-metadata-overrides.toml \
  --output docs/temp/citation-source-audit.md
```

Recommended deterministic gate:

```bash
python3 agent-protocols/scripts/citation_check_audit_ledger.py \
  --bib references.bib \
  --ledger docs/temp/citation-source-audit.md \
  --level metadata
```

Exit gate: every bibliography key has a row in the source-audit ledger and the
metadata column contains only `verified`.

## Level 3: Source-Content Support

Goal: verify that the manuscript claim supported by each citation corresponds to
the actual content of that source.

Checks:

- inspect the manuscript context around the citation;
- inspect the source passage, abstract, figure, table, report section, dataset,
  or official disclosure used as support;
- distinguish headline quantitative anchors from contextual sources;
- mark unsupported, overstated, non-commensurable, or wrong-scope claims as
  `blocked`;
- correct the manuscript or bibliography before marking a row `verified`;
- record a short content-support note for each bibliography key.

Recommended ledger shape:

```toml
[example2026source]
status = "verified"
note = "Used for the 2030 data-centre electricity projection; the report section states the projection and scenario boundary."
evidence = "https://example.org/report"
```

The protocol can automate ledger coverage, not source-claim judgement. Use the
content-support checker in update mode to create a complete TOML scaffold from
the bibliography, preserve existing rows, and optionally seed rows from a prior
audit:

```bash
python3 agent-protocols/scripts/citation_check_content_support.py \
  --bib references.bib \
  --support docs/temp/citation-content-support.toml \
  --merge-from ../old-audit/docs/temp/citation-content-support.toml \
  --update
```

Rows seeded this way remain `todo` until an agent or reviewer records a support
note and marks the row `verified` or justified `not_applicable`.

Recommended gate:

```bash
python3 agent-protocols/scripts/citation_check_content_support.py \
  --bib references.bib \
  --support docs/temp/citation-content-support.toml

python3 agent-protocols/scripts/citation_check_audit_ledger.py \
  --bib references.bib \
  --ledger docs/temp/citation-source-audit.md \
  --level content
```

Exit gate: every bibliography key has a content-support row, every row has a
note, and the audit ledger content column contains only `verified` or a justified
`not_applicable`.

## Level 4: Verbatim Quotation Verification

Goal: verify every source-attributed quotation verbatim.

Checks:

- extract quoted strings from the manuscript;
- classify scare quotes, terminology, variables, and ordinary emphasis as
  `not_applicable` unless they are source-attributed;
- for every source-attributed quotation, compare against the cited source text;
- preserve exact wording, spelling, capitalization, punctuation, ellipses, and
  bracketed insertions;
- if a statement is a paraphrase, remove quotation marks instead of forcing a
  non-verbatim quote through the gate.

The source-audit ledger may carry quote statuses directly:

- `verified`: source-attributed quote exists verbatim;
- `not_applicable`: no source-attributed quote is associated with this source;
- `blocked`: quote could not be found verbatim or source access failed;
- `todo`: quote verification is incomplete.

Recommended gate:

```bash
python3 agent-protocols/scripts/citation_check_audit_ledger.py \
  --bib references.bib \
  --ledger docs/temp/citation-source-audit.md \
  --level quote
```

Exit gate: all quote rows are `verified` or `not_applicable`.

## Gated Manifest Pattern

A citation-verification workstream should normally use these ordered phases:

```toml
phase_order = [
  "setup",
  "citation_inventory",
  "online_metadata",
  "source_content",
  "quotation_verification",
  "closeout",
]
```

Each phase should depend on the previous phase. Use command gates for the
scripts above, plus `regex_absent` or `citation_check_audit_ledger.py` checks to
prove there are no unresolved statuses.

## Failure Rules

Use the smallest correction that makes the citation true:

- fix the bibliography when metadata is wrong;
- fix the manuscript when the source supports a narrower or different claim;
- demote a source from headline evidence to context when its evidence tier is
  too weak;
- remove quotation marks when the source supports a paraphrase but not the
  exact words;
- mark the row `blocked` when the source cannot be found or checked.

Do not hide unresolved rows in prose. The ledger is the source of truth for
audit status.

## Closeout

Before reporting completion:

1. re-run the manifest through the highest completed phase;
2. run a bibliography or document build if the repo has one;
3. report any remaining style warnings separately from citation validity;
4. summarize corrected citations and blocked rows;
5. state whether temporary ledgers are being preserved for review or folded into
   durable docs;
6. report branch, worktree, commit/push status, and whether the worktree is
   clean.
