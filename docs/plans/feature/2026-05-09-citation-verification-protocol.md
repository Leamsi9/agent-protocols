# Citation Verification Protocol Extraction

Status: active
Branch: `feature/citation-check-protocol-2026-05-09`
Baseline: `origin/main`
Worktree: `/home/ismael/Github/.worktrees/agent-protocols-citation-check-protocol-2026-05-09`

## Goal

Extract the citation-verification workflow proven in the Computing Within Planetary
Boundaries manuscript into a reusable `agent-protocols` package surface.

The resulting package should let an operator say "verify citations on this research"
and get a deterministic gated workflow that checks, in order:

1. every machine-readable citation resolves to a bibliography entry;
2. every bibliography entry has online metadata evidence;
3. every cited source supports the content claim it is used for;
4. every source-attributed quotation is verified verbatim;
5. the final state is reviewable through ledgers and gates.

## Scope

Package-owned files:

- `citation-verification-protocol.md`
- `scripts/citation_inventory.py`
- `scripts/citation_build_source_audit.py`
- `scripts/citation_check_content_support.py`
- `scripts/citation_check_audit_ledger.py`
- `scripts/install.py`
- `README.md`
- tests under `tests/`

Workstream files:

- this plan
- `docs/plans/feature/2026-05-09-citation-verification-protocol.plan.toml`

The Computing manuscript repo is source material only. No files in that repo are part
of this implementation.

## Phases

### setup

Goal: prove this is a branch-owned substantive worktree and establish the durable plan.

Exit gate: branch/worktree binding and plan artifacts pass the manifest.

### protocol_doc

Goal: add a reusable citation-verification protocol that is research-format agnostic
while staying explicit about the supported deterministic gates.

Exit gate: the protocol documents all four verification levels, ledger artifacts,
manual evidence expectations, and failure rules.

### tooling

Goal: extract reusable scripts from the manuscript-specific audit into package-owned
tools with configurable inputs and deterministic check modes.

Exit gate: scripts compile and focused tests prove inventory checks, content-support
coverage checks, and audit-ledger status gates.

### packaging

Goal: make the new protocol and scripts available to consumer repos through the normal
installer and package docs.

Exit gate: installer vendoring tests prove the protocol and scripts appear in a fresh
consumer install, and README lists the protocol.

### validation

Goal: run the full package validation set and leave a reviewable branch state.

Exit gate: all phase checks pass and git status is reported for review.

### closeout

Goal: commit the package change and leave the branch in a clean reviewable state.

Exit gate: `HEAD` is ahead of `origin/main` and the worktree is clean.
