# Agent Protocols

Version `0.1.0`

A small working agreement for AI coding agents, vendored into repositories as
`agent-protocols/`.

- [work-protocol.md](work-protocol.md): how to plan, build, test, release and
  review, and where extra care is required. This is the one protocol.
- [citation-verification-protocol.md](citation-verification-protocol.md) and
  the `citation-substance-review` skill: checking that a research document's
  citations exist and support its claims.

A repository's own `AGENTS.md` supplies local facts (how to release, where data
lives, which risks are specific to it) and points agents at
`agent-protocols/work-protocol.md`. Keep `AGENTS.md` short and written as
positive statements of how work is done.

## Install or update

From the repository that uses the package:

```bash
python3 /path/to/agent-protocols/scripts/install.py
```

This copies the package files into `agent-protocols/`, removes package files
that a newer version no longer ships, and writes `agent-protocols.lock.json`
(version, source commit and file checksums). Repository-owned files such as
`agent-protocols/local/` are left alone. Commit the result.

## Migrating from 0.0.x

Version 0.1.0 replaces the substantive, minor, plan, proposal, temporary-note,
delegation, merge and pull-request protocols, the gated-phase skill, the
git-cleanup skill and their checkers with `work-protocol.md`. After updating:

1. Rewrite `AGENTS.md` to point at `agent-protocols/work-protocol.md`, and
   remove references to the retired files.
2. Remove `agent-protocols.toml`, `docs/live-workstream-status.md` and any
   `*.plan.toml` manifests that the old installer scaffolded.
3. Delete historical plans and handoffs from files agents read; Git keeps them.
4. Start new agent sessions: a running session keeps the instructions it
   started with.

## License

MIT or Apache-2.0, at your option.
