# Reliable acceptance gates for Leam

Status: implementation verified, independent review accepted; not merged upstream. Baseline: f54819b.
Branch: feature/leam-build-protocols-2026-09-20.
Ownership: generic contract/tooling; no live deployment changes.

Reject empty acceptance phases, omitted/duplicate phases, missing dependencies, cycles and non-topological phase orders before running any command. Incorporate Earthshift opt-in unittest execution counts without losing current-checkout checks. Pin release provenance in Leam.

Validation: regression tests drive the checker CLI, including invalid graphs with a command that must never execute. Run existing suite, independent review, then commit. No refresh of other consumers is in scope.

Validation: 28 tests pass, no skips/expected failures. Independent review found hidden failing pipelines and masked dependency tests; fixed and re-reviewed. Review accepted. Live-deployment states not applicable: this is CLI tooling, verified through caller-level subprocess tests.
