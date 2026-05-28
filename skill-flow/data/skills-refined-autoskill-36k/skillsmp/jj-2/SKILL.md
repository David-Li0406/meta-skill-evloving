---
name: jj
description: Jujutsu (jj) workflow guidance used in place of Git for commit/push, stacked work, status/log, diff/show, rebase, split/squash, abandon/restore, conflict resolve, bookmarks. Use when users mention jj/Jujutsu or ask how to do Git workflows in jj.
---

# JJ Workflow (Canonical)

## Policy

- For new PRs, use `jj push-new` (alias for `jj git push --change @-`) to create the bookmark and push it.
- Do not run `jj git push` directly; use `jj push` for updates and `jj push-new` for new PRs.
- Do not pre-create bookmarks for independent PRs. For stacked PRs, create a bookmark per layer so each PR has a stable head.
- Avoid generating multiple new bookmarks for the same PR. If a bookmark already exists, move it and run `jj push`.
- Only use `jj abandon` after confirming with the user; it is rare and usually indicates recovery from a bad state.
- Enforce Conventional Commits for commit messages and PR titles. Format: `type(scope optional)!: subject`.
  - Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`.
  - Scope is optional; `!` marks breaking changes.
  - If the user supplies a non-conforming title/message, propose a compliant one and confirm before committing/creating a PR.
  - If the merge strategy is squash, the PR title becomes the commit message; keep it Conventional.

## Notes

- `@` is the working-copy commit; `@-` is its parent.
- `jj push` (alias for `jj git push @-`) pushes the bookmark(s) pointing at `@-`. If `@-` has no bookmarks, use `jj push-new` instead.
- `jj push-new` (alias for `jj git push --change @-`) creates a new bookmark and pushes it.
- `trunk()` resolves to the repository's trunk bookmark and avoids guessing `main` vs `master`; wrap it in single quotes for shell safety.
- When a revset includes parentheses (like `trunk()`), single-quote it.

## Workflows

Initialize / clone:

- `jj git init [DESTINATION]`
- `jj git clone <SOURCE> [DESTINATION]`

Create a new change from trunk:

- `jj new 'trunk()'`

Decide whether the work is independent or stacked:

- Independent work must start from `trunk()` to avoid accidental stacking.
- Stacked work intentionally builds on a prior change; each stack layer gets its own bookmark and PR.
- Use an independent PR when the change does not depend on other unmerged work.
- Use a stack when the overall effort is too large for one PR but can be split into self-contained, mergeable chunks.
- Stack only when later changes rely on earlier unmerged work and reviewers benefit from smaller, focused slices.

Check where I am:

- `jj status`

Check commit history:

- `jj log`

View diff for current change:

- `jj diff` (defaults to `-r @`)

Show full change details:

- `jj show <rev>`
- Use `jj log -p -r <rev>` for patch-view history.

New commit (new PR):

- `jj commit -m "type: message"` (scope optional: `type(scope): message`)
- `jj push-new`
- If this PR was already pushed, move the existing bookmark and use `jj push` instead.

Independent PR (standalone) flow:

- `jj new 'trunk()'`
- Make changes → `jj commit -m "type: message"`
- `jj push-new`
- Create the PR with base `master` (or repo trunk) so GitHub shows only this change.

Stacked PR flow (multiple dependent changes):

- Create each change as a separate revision in a chain.
- Create a bookmark for each layer (example names: `bede/1`, `bede/2`):
  - `jj bookmark create <bookmark> -r <rev>`
- Push each bookmark:
  - Move bookmark if needed: `jj bookmark move <bookmark> --to <rev>`
  - `jj push`
- Create PRs in order, setting the base of each PR to the previous layer’s bookmark/branch.

Unwind an accidental stack (PR shows unrelated commits):

- `jj git fetch`
- Identify the intended change (bookmark or revision): `jj bookmark list` or `jj log -r <rev>`
- Rebase just that change onto trunk:
  - `jj rebase -r <rev> -A 'trunk()' --ignore-immutable`
- Move the bookmark to the rebased change (use `@-` if it is the parent of the working copy):
  - `jj bookmark move <bookmark> --to @-`
- Push the updated bookmark:
  - `jj push`
- Ensure the PR base is trunk (update via `gh pr edit --base <trunk-branch>` if needed).

Add a commit to an existing PR/stack (reuse existing bookmark):

- `jj commit -m "type: message"` (scope optional: `type(scope): message`)
- `jj status` (identify the existing `push-...` bookmark for the current change)
- If multiple `push-...` bookmarks are shown, ask which PR/bookmark to update.
- `jj bookmark move <bookmark-name> --to @-`
- `jj push`
- If no bookmark exists yet, do not create one manually; use `jj push-new`.

Amend current change content:

- `jj squash` (move working-copy changes into parent)

Split a change:

- `jj split`

Squash/merge changes in a stack:

- `jj squash [--from <rev>] [--into <rev>]`

Abandon a change:

- `jj abandon [REVSET]`

Restore a file to parent state:

- `jj restore <path>`
- Restore a file from trunk:
  - `jj restore --from 'trunk()' -- <path>`

Resolve conflicts:

- `jj resolve [FILESETS]...`

Recover from a bad state (operation log):

- Use when repo state is messed up (bad merges/conflicts/accidental rebase).
- Prefer `jj op log` + `jj op restore` over manual rebases when unsure.
- `jj op log` (see recent operations; each op snapshots repo state)
- Optional preview: `jj --at-op=<op-id> log`
- `jj undo` (undo the most recent operation)
- `jj redo` (redo the most recently undone operation)
- `jj op restore <op-id>` (restore repo state to a specific operation)
- `jj op revert <op-id>` (revert a specific earlier operation)

Sync with trunk:

- `jj git fetch`
- `jj rebase -d 'trunk()'`

Rebase a stack onto trunk (move a change and all its descendants):

- `jj rebase -r <rev>:: -A 'trunk()' --ignore-immutable`
