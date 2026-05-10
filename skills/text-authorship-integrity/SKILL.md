---
name: text-authorship-integrity
description: Use when asked to review, revise, or audit prose for AI-text detection risk, LLM-style markers, mixed-authorship concerns, or publication authorship integrity. This skill helps preserve human provenance and source-grounded authorial voice; it must not be used for detector evasion, concealment of prohibited AI use, or "humanizer" bypass workflows.
metadata:
  short-description: Audit prose for authorship integrity
---

# Text Authorship Integrity

Use this skill when the user wants help with AI-detection risk, generic
LLM-style prose, mixed-authorship review, or making a draft feel more genuinely
authorial.

## Core Rule

The canonical workflow is
`agent-protocols/text-authorship-integrity-protocol.md`. This skill is an
assistant adapter for that protocol.

Do not help optimize text to bypass or defeat detectors. Redirect evasion
requests toward provenance, disclosure, source support, and substance-first
revision.

## Review Loop

1. Identify the governing AI-use policy and disclosure expectation.
2. Run or request the deterministic local audit:
   `python3 agent-protocols/scripts/text_authorship_audit.py --input <file> --format <latex|markdown|plain> --ledger docs/temp/text-authorship-audit.toml`
3. Treat any detector or audit output as a diagnostic signal, not proof.
4. For each flagged passage, name the smallest claim and the human source for
   that claim.
5. Revise from evidence, author notes, calculations, and document-specific
   reasoning.
6. Record the result in `docs/temp/text-authorship-audit.toml`.

## Good Revision Moves

- add precise dates, units, assumptions, denominators, or source locators;
- replace generic transitions with the actual argumentative relation;
- narrow broad claims to what the evidence supports;
- restore the author's phrasing when it carries intent;
- split over-compressed paragraphs into claim, evidence, and implication;
- preserve required disclosure of material AI assistance.

## Bad Revision Moves

- paraphrase until a detector score changes;
- add typos, slang, filler, or fake personal details;
- imitate a private person's style without consent;
- submit confidential text to detector APIs without permission;
- call a detector pass proof that the prose is acceptable.

## Output Style

When reporting back, separate:

- detector or audit signals;
- provenance gaps;
- substantive revision recommendations;
- policy or disclosure blockers;
- completed edits.
