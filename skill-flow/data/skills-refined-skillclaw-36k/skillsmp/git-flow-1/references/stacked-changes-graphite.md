# Stacked Changes and Graphite Workflow (2026)

Stacked changes (or "Stacked PRs") is a workflow where a large feature is broken into a series of small, dependent pull requests. This makes reviews 10x faster and more thorough.

## 1. The Concept of Stacking

Instead of:
`Feature A (1,000 lines)` -> One giant PR.

Use:
`Part 1: Database Schema (100 lines)` -> PR #1
`Part 2: API Client (150 lines)` -> PR #2 (depends on #1)
`Part 3: UI Component (200 lines)` -> PR #3 (depends on #2)

## 2. Manual Stacking with Git CLI

1.  `git checkout -b part-1` -> commit -> push.
2.  `git checkout -b part-2` (while on `part-1`) -> commit -> push.
3.  When `part-1` changes, you must `git rebase` `part-2` onto the new `part-1`.

## 3. Automated Stacking with Graphite.dev

Graphite automates the rebase/restack process.

-   **`gt create`**: Create a new branch in the stack.
-   **`gt submit`**: Push all branches in the stack as separate PRs.
-   **`gt restack`**: Automatically rebase all dependent branches when a parent changes.

## 4. Benefits for 2026 Teams

-   **Parallel Review**: Different experts can review different parts of the stack simultaneously.
-   **Atomic Reverts**: If the UI is buggy, you can revert PR #3 without losing the DB schema in PR #1.
-   **Reduced Cognitive Load**: Reviewers only need to look at 100-200 lines at a time.

## 5. Best Practices

-   **Title your stacks**: `[1/3] Database Setup`, `[2/3] API implementation`.
-   **Merge in Order**: Always merge the base of the stack first.
-   **Restack Frequently**: Keep your stack healthy by restacking against `main` every morning.

---
*Updated: January 22, 2026 - 18:55*
