Overview

This document defines recommended Git and branch practices for WAIF's multi-agent, multi-team workflow. The goals are to minimize merge friction, keep `main` releasable, and make coordination explicit and auditable.

TL;DR (default happy path)

1) Start from an up-to-date `main`.
2) Create a short-lived topic branch for a single beads issue. Branch names MUST use the beads prefix and id and follow the form `<beads_prefix>-<id>/<short-desc>` (for example `bd-123/fix-ask-prompt` or `wafi-73k/add-feature`).
3) Keep work small; re-sync frequently; avoid rewriting shared history.
4) Open a PR into `main` with the bd id in the title and use the PR template.
5) Record handoffs, commands run, and files touched in bd. When an agent works on a branch, it MUST record involvement in bd comments.

Scope and assumptions

- Teams are persistent (they deliver many bd issues over time).
- Each bd issue is implemented on a short-lived topic branch created from `origin/main`.
- Branches are the canonical unit of work; `main` is the canonical integration branch and must remain releasable.
- `bd` is the authoritative source of work state and the place to record handoffs, decisions, and commands executed.

Important constraint

- If multiple agents must work in parallel on the same bd issue, they should use separate branches (agent sub-branches) and merge into the topic branch (or use stacked PRs). Branch-per-bd ensures a single, traceable branch name that corresponds to a `bd` issue.

Principles

- Topic branch is the unit of work: one bd issue → one topic branch. Branch names MUST include the bd id and should be used by both humans and agents.
- Keep branches short-lived and PRs small; merge frequently.
- Prefer determinism over cleverness: record what you did in bd.
- Never force-push shared branches without explicit Producer authorization.

Naming conventions

Topic branches (required):

- One topic branch per beads issue. There must be only one canonical branch per beads id. Examples:
  - `bd-123/fix-ask-prompt`
  - `wafi-79y/pr-title-validation`

Agent sub-branches (only when parallel work is needed):

-- If multiple agents need to work at the same time on the same beads issue, create short-lived agent sub-branches from the canonical beads branch. Examples:
  - `bd-123/patch`
  - `bd-123/docs`
  - `bd-123/ci`

Branch naming rules:

-- Branch names MUST include the beads prefix and id (e.g., `bd-123`) as the canonical tie to issue tracking.
-- There can be only one canonical branch per beads id. Before creating a branch, agents or contributors MUST check for any branch that starts with `<beads_prefix>-<id>` (for example `bd-123`) locally or on `origin` and reuse it if present. When reusing, record your involvement in the bd comments.
-- Avoid using branches without beads ids for tracked work.

Branch lifecycle (topic branches)

1) Sync with `origin/main`:
   - `git fetch origin`
   - `git checkout main`
   - `git pull --rebase`

2) Create or reuse the topic branch for the beads issue:
   - Check for an existing branch that starts with the beads prefix and id (for example `git branch --list "bd-123*"` or `git ls-remote --heads origin "bd-123*"`). If a matching branch exists, reuse it:
     - `git checkout bd-<id>/<short-desc>`
   - Otherwise create the canonical branch:
     - `git checkout -b bd-<id>/<short-desc>`
   - Record your involvement in bd comments when you start work in the branch.

3) Work locally with small commits. Run local quality gates when appropriate:
   - `npm test`
   - `npm run lint`
   - `npm run build`

4) Publish and open a PR to `main`:
   - PR title must include the bd id, e.g. `bd-123: fix ask prompt`
   - Use `.github/PULL_REQUEST_TEMPLATE.md`

5) Merge to `main` only when CI is green and reviews are complete.

6) Cleanup after merge:
   - delete the remote branch

Agent workflows and patterns

-- One agent working solo on a topic branch:
  - Work directly on `bd-<id>/<short-desc>`.

- Multiple agents working in parallel:
  - Create agent sub-branches and merge into the topic branch.
  - Keep sub-branches short-lived.

Example parallel flow:

-- Create canonical branch: `bd-123/fix-thing`
-- Create parallel branches:
  - Patch works on `bd-123/patch`
  - Scribbler works on `bd-123/docs`
-- Merge sub-branches into `bd-123/fix-thing` (merge owner coordinates).
-- Open PR to `main` from `bd-123/fix-thing`.

Rebasing vs merging (rules)

| Situation | Recommended update strategy |
|---|---|
| Local-only branch (not pushed / nobody else fetched it) | Rebase frequently onto `origin/main` |
| Published branch (others may have fetched) | Prefer merge from `origin/main` into branch; avoid rewriting public history |
| Long-running work | Prefer incremental PRs + feature flags; avoid mega-rebases |

Push and publish policy

- Default: humans own pushes and merges.
- Agents must follow their permission files (`.opencode/agent/*.md`). Agents and humans MUST use branches named with the bd id. When an agent works in a branch for a bd issue, it MUST record its involvement in bd comments and avoid editing files that other agents have claimed in bd unless coordination is documented.

Pull requests, reviews, and CI

- PRs are the integration and review point.
- PR titles should include the bd id (e.g., `bd-123: short description`) for traceability.
- Use `.github/PULL_REQUEST_TEMPLATE.md`.
- Branch protection should require:
  - PRs to merge to `main`
  - passing CI checks
  - at least one approving review
  - force-push disabled

See: `docs/.github/branch_protection.md`

Automation note (planned)

- We intend to add a PR validation workflow that enforces PR title formatting and (optionally) template sections.
- Tracking issue: `wf-79y.14`.

Agent boundaries and responsibilities (summary)

- Patch (Implementation): implements changes and tests; asks before pushing and before destructive git operations.
- Probe (QA): runs tests and assesses risk; provides structured feedback in bd.
- Ship (DevOps): keeps CI healthy and monitors release readiness.
- Forge: maintains `.opencode/agent/*.md` and least-privilege permissions.
- Build: coordinates bd state and assigns ownership; does not merge by default.
- Scribbler / Muse / Pixel: doc/design/asset work; avoid publishing risky changes without Producer coordination.

Handoffs and delegation

- Use the canonical handoff template at `docs/.github/handoff_note_template.md` (mirrored in `history/handoff_note_template.md`).
- For hard handoffs and any transfer of responsibility, copy the template into a bd comment and fill it out.

Handoff checklist (must include for hard handoffs)

1) bd id and branch name (topic branch)
2) From and To (agent/person)
3) Summary and acceptance criteria
4) Commands run and results
5) Files changed (paths)
6) Risks and follow-ups
7) Any planning stored in `history/`

Delegation and merge ownership

- Build or the Producer should designate the merge owner early.
- Record delegations in bd using: `delegated-to:@<actor> (scope)`.
- Do not assume merge authority unless it is explicitly delegated.

Related process artifacts

- Handoff template: `docs/.github/handoff_note_template.md`
- PR template: `.github/PULL_REQUEST_TEMPLATE.md`
- Branch protection guidance: `docs/.github/branch_protection.md`
- Permissions matrix: `docs/.github/permissions_matrix.md`

Notes

This guidance intentionally trades some flexibility for predictability. When in doubt about destructive actions, shared branch rewrites, or ownership, escalate via bd and the Producer.

```
- Record delegations in bd using: `delegated-to:@<actor> (scope)`.
