---
name: backlog-planner
description: "Create or refine backlog items with clear scope and acceptance criteria using the gh CLI; use when planning work, writing tickets, or breaking down epics (trigger keywords: backlog, issue, ticket, epic, roadmap)."
---

# Backlog Planner

## What this skill does
- Turns ideas into actionable backlog items with clear scope and criteria.
- Uses the gh CLI to create/update issues with labels and milestones.
- Decomposes large efforts into smaller, sequenced tasks using sub-issues when supported.

## When to use it
- Trigger phrases: "backlog", "issue", "ticket", "epic", "roadmap".
- Use when planning work or creating issues for others to implement.

## Step-by-step workflow
1) Confirm repo context with `gh repo view --json nameWithOwner -q .nameWithOwner` and verify `gh auth status`.
2) Check for duplicates with `gh issue list --search "keywords" --state all --limit 20`.
3) List labels with `gh label list --limit 200` and map to type, component, priority, and AI labels when available.
4) List milestones with `gh api repos/{owner}/{repo}/milestones --jq '.[].title'` and select if relevant.
5) Draft the issue body with clear Overview, Current State, Acceptance Criteria, and Technical Context.
6) Create or update the issue with `gh issue create` / `gh issue edit` using `--label` and `--milestone`.
7) If the work is an epic, decide on sub-issues and manage them with `scripts/gh-sub-issues.sh` when supported.

## Sub-issues: when and how
Use sub-issues when:
- The work spans multiple components or teams and can be parallelized.
- The epic requires 3+ distinct deliverables or 3+ PRs.
- The effort is larger than ~1-2 days and needs progress tracking.

Avoid sub-issues when:
- The task is a single change set or under ~4 hours.
- The work is a simple bug fix or small docs update.
- Sub-issues are not enabled for the repo; use a checklist instead.

Workflow:
1) Create the parent epic issue with a clear scope and target milestone.
2) Identify existing related issues; only create new sub-issues when needed.
3) Use `scripts/gh-sub-issues.sh add <parent> <child...>` to attach sub-issues.
4) If sub-issues are not supported, add a task checklist in the epic and link related issues.

## Scripts
- `scripts/gh-sub-issues.sh list <parent> [--repo OWNER/REPO] [--limit N]`
- `scripts/gh-sub-issues.sh add <parent> <child...> [--repo OWNER/REPO]`
- `scripts/gh-sub-issues.sh remove <parent> <child...> [--repo OWNER/REPO]`
- If the script reports that sub-issues are not available, use a checklist and issue links instead.

## Expected outputs / formatting
- Issue template with Overview, Current State, Acceptance Criteria, Technical Context.
- Selected labels and milestone (if available).
- Sub-issue plan or checklist with clear titles and ordering.

## Example prompts
- "Draft a backlog issue for adding export support."
- "Break this epic into smaller, sequenced tasks."
- "Create a ticket with clear acceptance criteria for this feature."
- "Use gh to create an issue with labels and a milestone."
