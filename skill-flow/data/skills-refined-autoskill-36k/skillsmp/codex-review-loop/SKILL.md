---
name: codex-review-loop
description: On a GitHub PR, post '@codex review' via gh, wait for Codex’s review, then iterate fix+push cycles until Codex approves / reports no P0/P1 findings.
user-invocable: true
context: fork
---

# Codex Review Loop (gh + @codex)

## What this Skill does

When invoked, this Skill drives a tight PR iteration loop:

1) Identify the target PR (explicit `#123`/URL, or the PR for your current branch)
2) Post a PR comment containing `@codex review` (so the comment is authored by *your* GitHub account via `gh`)
3) Poll GitHub until Codex posts its review
4) Convert the findings into an actionable checklist
5) Apply fixes, run tests, commit, push
6) Repeat until Codex returns **APPROVED** or explicitly reports **no findings**

Codex is triggered by a PR comment containing `@codex review` (not by “requesting reviewer”). See OpenAI’s GitHub integration docs.

## Preconditions

- You are inside a git repo that has a PR (or you pass a PR number/URL).
- `gh auth status` works (you are logged in as the account that should author the comment).
- Codex GitHub code review is enabled for the repo (in Codex settings).
- Recommended: add an `AGENTS.md` with “Review guidelines” so Codex focuses on what you care about.

## Quick usage

### Run on current branch’s PR
Run:
```bash
python3 .claude/skills/codex-review-loop/scripts/codex_review_once.py
```

### Run on a specific PR
```bash
python3 .claude/skills/codex-review-loop/scripts/codex_review_once.py 123
# or:
python3 .claude/skills/codex-review-loop/scripts/codex_review_once.py https://github.com/OWNER/REPO/pull/123
```

## How to use this Skill in Claude Code

When I’m active, follow this loop:

1) **Fetch Codex feedback**:
   - Run `codex_review_once.py` (optionally with PR ref)
   - Parse its JSON output

2) **If clean**, stop:
   - Clean = `review.state == "APPROVED"` OR (`inline_comments` empty AND review body indicates no findings)

3) **If findings exist**, fix them:
   - Make minimal, surgical changes addressing each comment
   - Prefer adding/adjusting tests when behavior changes

4) **Run tests** (auto-detect):
   - If `package.json` exists: `npm test` (or `pnpm test` / `yarn test` if lockfile suggests)
   - If `go.mod`: `go test ./...`
   - If `pyproject.toml`/`requirements.txt`: `pytest -q`
   - If `CMakeLists.txt`: `cmake --build ...` then `ctest`
   - If none detected: run the repo’s documented test command in README / CI config

5) **Commit + push**:
   - Commit message: `Fix: address Codex review findings (iter N)`
   - Push to the PR branch

6) Go back to step (1).

### Guardrails

- Don’t do large refactors unless Codex finds a real bug.
- Keep iteration count capped (default 5). If still not clean, summarize remaining deltas.

## Optional: teach Codex what “issues” mean (AGENTS.md)

Codex reads `AGENTS.md` and follows “Review guidelines”. Put this at repo root:

```md
## Review guidelines
- Treat security/auth issues as P0.
- Treat data races / memory safety issues as P0.
- Treat flaky tests as P1.
- Treat doc typos as P2 (do not block).
```



## Blockers-only mode (recommended default)

This loop is most useful when it **stops on blockers only**.

**Definition of “clean” in blockers-only mode:**
- Clean if there are **no P0/P1 inline comments** from Codex (even if Codex summarizes P2 suggestions in the review body).
- Not clean if there are any inline comments labeled **P0** or **P1**, or if Codex submits a review with state **CHANGES_REQUESTED**.

### Getting reliable severity labels

Set `CODEX_EXTRA_PROMPT` so Codex labels findings and keeps P2 non-blocking:

```bash
export CODEX_EXTRA_PROMPT="Please label every finding as P0/P1/P2. Only leave inline review comments for P0/P1 blockers. Summarize P2 (nits) in the review body under a 'Non-blocking suggestions' section."
```

### Run blockers-only (default)

```bash
python3 .claude/skills/codex-review-loop/scripts/codex_review_once.py --blockers-only
# (or omit the flag; blockers-only is default)
```

### Run strict (rare)

```bash
python3 .claude/skills/codex-review-loop/scripts/codex_review_once.py --strict
```
