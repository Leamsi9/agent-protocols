# Text Authorship Integrity Protocol

This protocol is a deterministic workflow for reviewing scholarly or
professional prose when AI-text detection risk matters.

It is not a detector-evasion workflow. Do not optimize text to bypass or defeat a detector, hide prohibited AI use, inject artificial errors, or run iterative
"humanizer" loops. The goal is to make the text genuinely accountable to the
human author: source-grounded, document-specific, stylistically natural for the
author, and transparent about any permitted assistance.

## When To Use This

Use this protocol when any of these are true:

- a submission, review, policy, or venue may scan for AI-generated text;
- the author wants to reduce generic LLM-style prose in a draft;
- an assistant has substantially revised human text and the author needs to
  preserve provenance;
- a detector or reviewer has flagged a passage and the team needs a careful
  non-punitive review;
- a repo needs a repeatable authorship-integrity gate before publication.

For citation support, pair this with `citation-verification-protocol.md`.

## Research Snapshot

As of 2026-05-10, AI-text detection is not one technique. Practical systems
combine several families:

- supervised classifiers trained on broad human/AI corpora;
- zero-shot scoring from model likelihood, probability curvature, or paired
  scoring models;
- mixed-authorship and AI-editing estimators that classify the degree of AI
  intervention rather than only `human` versus `AI`;
- watermarking and provenance schemes where the generator participates;
- segment-level and policy-cap reporting that lets reviewers set false-positive
  tolerances.

The strongest current clue for protocol design is not "find a magic detector."
It is that modern detectors increasingly reward provenance-aware review:
document-length context, segment-level signals, matched human/AI training data,
active hard-example mining, and calibrated false-positive caps. A responsible
writing protocol should therefore produce reviewable provenance and better
writing, not detector-specific camouflage.

Useful current references:

- OpenAI, "New AI classifier for indicating AI-written text" (2023), for
  limitations, false positives, short-text weakness, and the retirement of its
  classifier.
- Mitchell et al., "DetectGPT" (ICML 2023), for probability-curvature
  detection.
- Bao et al., "Fast-DetectGPT" (ICLR 2024), for efficient zero-shot curvature
  detection.
- Hans et al., "Binoculars" (ICML 2024), for paired-model zero-shot scoring.
- Dugan et al., "RAID" (ACL 2024), for shared adversarial robustness
  benchmarking.
- Sadasivan et al., "Can AI-Generated Text be Reliably Detected?" (TMLR 2025),
  for robustness limits under recursive paraphrasing and the theoretical
  boundary of distributional detection.
- Liang et al., "GPT detectors are biased against non-native English writers"
  (Patterns 2023), for fairness risk.
- Thai et al., "EditLens" (ICLR 2026), for continuous AI-edit extent scoring
  and the importance of mixed-authorship review.
- Emi et al., "Pangram at GenAI Detection Task 3" (GenAIDetect 2025), for
  broad pretraining, augmentation, and hard-example active learning.

## Core Rules

1. Treat detector output as a diagnostic signal, never as proof of authorship
   or misconduct.
2. Preserve the authorial chain: notes, outlines, source excerpts, drafts,
   revision diffs, and explicit author decisions.
3. Prefer human revision from claims and evidence over model paraphrasing.
4. Resolve generic prose by adding real reasoning, source-specific constraints,
   methodological detail, or author judgement.
5. Do not add randomness, slang, typos, autobiographical detail, or stylistic
   quirks solely to manipulate detector scores.
6. Do not ask an LLM to "make this undetectable", "humanize this", or minimize
   a detector score.
7. If AI assistance was permitted and material, preserve a disclosure note that
   matches the venue policy.
8. If a passage cannot be tied to author intent or evidence, mark it for
   rewriting from source material rather than polishing it.

## Workflow

### 1. Establish Policy And Provenance

Record the governing policy before revising:

- venue, employer, publisher, or classroom AI-use rules;
- whether language editing, grammar correction, translation, summarization, or
  substantive generation are allowed;
- required disclosure wording;
- confidentiality limits for external detector APIs.

Create or update `docs/temp/text-authorship-audit.toml` with one row per
passage that needs review. Keep the ledger temporary unless the project wants a
durable publication audit trail.

Minimum row fields:

```toml
[segment-id]
status = "todo"
locator = "section, paragraph, line, or heading"
claim_role = "what this passage does in the document"
human_source = "notes, prior draft, source excerpt, calculation, or author decision"
revision_action = "pending"
detector_signal = "not_run"
notes = ""
```

Allowed `status` values:

- `todo`
- `needs_revision`
- `verified`
- `blocked`
- `not_applicable`

### 2. Extract And Score The Draft

Run the deterministic local audit before editing:

```bash
python3 agent-protocols/scripts/text_authorship_audit.py \
  --input manuscript.tex \
  --format latex \
  --ledger docs/temp/text-authorship-audit.toml
```

This script is not an AI detector. It flags review priorities using stable,
local stylometric and provenance-adjacent signals such as sentence-length
uniformity, formulaic connective phrases, abstraction density, citation
density, numeric specificity, and optional author-baseline distance.

If a baseline corpus is available, add it:

```bash
python3 agent-protocols/scripts/text_authorship_audit.py \
  --input manuscript.tex \
  --format latex \
  --baseline docs/style-baseline/*.md \
  --ledger docs/temp/text-authorship-audit.toml
```

Do not interpret the score as probability of AI authorship. Interpret it as a
queue for human review.

### 3. Diagnose Each Flagged Passage

For each medium or high review-priority passage:

1. identify the smallest claim being made;
2. find the human source for that claim;
3. check whether the passage includes enough local specificity for the reader
   to see the authorial reasoning;
4. check whether citations or data support the claim;
5. decide whether the problem is style, evidence, structure, policy, or missing
   provenance.

Common legitimate findings:

- `formulaic_style`: generic transitions or over-smoothed phrasing;
- `thin_provenance`: no clear human note, source, or calculation;
- `unsupported_generality`: broad claim without local evidence;
- `voice_mismatch`: the passage departs from the author's baseline style;
- `citation_gap`: the citation does not carry the claim;
- `policy_gap`: the AI-use or disclosure status is unclear.

### 4. Revise From Substance

Allowed revision actions:

- replace generic summary with the author's actual reasoning step;
- add concrete denominators, dates, model assumptions, units, or evidence;
- split an over-compressed paragraph into claim, evidence, and implication;
- remove unsupported intensifiers;
- restore author-specific phrasing from notes or prior drafts;
- narrow the claim to what the cited source can support;
- preserve awkward but meaningful authorial choices when they carry intent;
- disclose material AI assistance when policy requires it.

Disallowed revision actions:

- paraphrasing solely to change detector output;
- adding typos, filler, slang, or false personal anecdotes;
- asking a model to imitate a private person's style without consent;
- repeatedly submitting confidential drafts to external detectors without
  permission;
- treating a detector pass as evidence that authorship is acceptable.

### 5. Optional Detector Diagnostics

External detectors can be useful when confidentiality and policy permit. Record
them as diagnostic signal rows, not gates:

```toml
[segment-3.detector.pangram]
tool = "Pangram V3"
date = "2026-05-10"
scope = "paragraph"
prediction = "Moderately AI-Assisted"
score = "0.42"
review_outcome = "needs_revision"
note = "Used only to prioritize manual review."
```

If using open research models such as Open Pangram/EditLens, Binoculars, or
Fast-DetectGPT, pin the model, revision, threshold, dependency versions, and
input scope. If using a commercial API, record the endpoint/version shown by
the service and avoid sending confidential text unless permitted.

No detector score is a required pass condition. The required condition is that
the author reviewed the passage, tied it to evidence or intent, and resolved
any policy or provenance gap.

### 6. Acceptance Gate

A passage may be marked `verified` only when:

- its claim role is clear;
- its human source or author decision is identified;
- citations and evidence are adequate for the claim;
- any material AI assistance is disclosed according to policy;
- the final text was revised from substance, not detector-gaming;
- detector signals, if any, were reviewed as diagnostic signals.

The overall document may pass when all required ledger rows are `verified` or
`not_applicable`, and no `blocked` row affects submission readiness.

## Failure Modes

Stop and escalate when:

- the governing policy forbids the actual assistance used;
- the author cannot identify human source material for substantive claims;
- the text depends on unverifiable citations or invented sources;
- the only available fix is to conceal prohibited AI generation;
- an external detector is being used as an automatic punitive authority;
- the revision would alter evidence, methods, or claims merely to reduce a
  detector score.

## Assistant Behaviour

When assisting with revisions under this protocol:

- make the authorship boundary explicit in your work notes;
- ask for author notes or prior drafts when provenance is missing;
- suggest substance-first rewrites rather than generic style swaps;
- keep the author's technical vocabulary and argumentative commitments;
- report what changed and why in audit terms;
- refuse detector-evasion framing and redirect to provenance, disclosure, and
  source-grounded revision.
