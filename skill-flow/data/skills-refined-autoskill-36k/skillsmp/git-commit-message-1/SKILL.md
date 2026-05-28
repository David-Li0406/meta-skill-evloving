---
name: git-commit-message
description: Generate Conventional Commits git commit messages from the staged diff. Use this when the user asks to craft a commit message or when preparing a commit.
---

# Conventional Commit Message Authoring

Use this skill when the user asks for a git commit message (for example: “craft commit message”, “write commit message”, “conventional commit”).

## Output contract

Return a commit message in **Conventional Commits** format.

- **Subject line format:** `<type>(<scope>): <subject>`
- **Scope:** optional but preferred when obvious
- **Subject:** imperative, present tense; no trailing period; keep it short

If useful, add a body separated by a blank line. The body should explain *why* and notable behavior changes, not a code dump.

When the staged change spans multiple areas (for example: UI change + dependency updates + tooling/docs), omit scope and add a short body summarizing the main buckets of change.

## Allowed types

- `feat`: a new feature
- `fix`: a bug fix
- `docs`: documentation-only changes
- `style`: formatting/whitespace (no logic)
- `refactor`: code change that neither fixes a bug nor adds a feature
- `perf`: performance improvement
- `test`: adding/fixing tests
- `build`: build system or external dependencies
- `ci`: CI configuration/scripts
- `chore`: other changes that don’t modify product code
- `revert`: revert a previous commit

## Procedure

1. Inspect the actual change (prefer staged changes when available; otherwise use the working tree diff).
2. Choose **type** based on intent.
3. Choose **scope** as the smallest meaningful area (examples: `auth`, `chat`, `ui`, `api`, `deps`, `build`, `tests`).
4. Write a single clear subject describing the change.
5. If multiple distinct concerns are included, propose splitting commits; otherwise add a short body (1–6 lines) that summarizes the key parts.
6. If the change introduces a breaking change, add `!` after type/scope and include a `BREAKING CHANGE:` footer.

## Examples

### Simple UI affordance

```
feat(auth): add cancel button to registration form
```

### Bug fix with brief rationale

```
fix(chat): prevent duplicate broadcast on reconnect

Avoids emitting a second join event when the socket reconnects.
```

### Breaking change

```
feat(api)!: rename /v1/messages to /v1/chat-messages

BREAKING CHANGE: Clients must call /v1/chat-messages instead of /v1/messages.
```
