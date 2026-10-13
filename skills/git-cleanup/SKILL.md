---
name: git-cleanup
description: Clean stale Git branches, worktrees and checkout registrations, or assess what can be removed. Use for requested repository hygiene, not as a prerequisite for ordinary implementation or deployment.
metadata:
  short-description: Clean branch and worktree state safely
---

# Git cleanup

Work within the requested cleanup scope. Use judgment about what needs inspection;
one finished worktree does not require an inventory of every branch or a separate
verification report. Existing user authorization applies without asking again.

For a targeted cleanup, inspect the affected checkout's status and whether its
work was delivered. With cherry-picked delivery, ancestry alone is insufficient;
`git cherry <integration-ref> <branch>` can identify patches already integrated.
Preserve dirty or undelivered work unless its disposal was explicitly authorized.
Keep active checkouts and unrelated user files out of routine cleanup.

Use `git worktree remove <path>` for a clean, finished linked worktree; do not use
`--force` to conceal unexpected changes. Retain its branch when useful. Use
`git branch -d` for an unwanted integrated branch and `git worktree prune` for
stale registrations. Never delete or move a registered checkout behind Git's back.

For broad or ambiguous cleanup, the repository's `repo_state.py` may help identify
stale registrations, shadowed checkouts and misplaced worktrees. Run it when it
answers the actual question; its full inventory and report are optional. Use
`git worktree move` for an authorized relocation. Quarantine genuinely ambiguous
contents when useful, rather than creating recovery copies of every disposable
checkout.

Pause only for unresolved ambiguity that risks losing useful work or exceeds
existing authorization. Mention material removals and anything left unresolved;
no mandatory before/after audit, command transcript or certificate is needed.
