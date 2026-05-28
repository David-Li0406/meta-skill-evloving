---
name: project-status
description: Reports implementation status of project components with evidence. Use when asked about what's done, in progress, or planned for a project.
---

## Purpose

Provide accurate project status by distinguishing between what was discussed versus what is actually implemented.

## When to Use

Apply when user asks:
- "What's the status of X?"
- "Is Y complete?"
- "What has been implemented?"
- "Show me project progress"

## Status Levels

| Status | Definition | Evidence Required |
|--------|------------|-------------------|
| `Triage` | Mentioned but needs review | Transcript/message reference |
| `Backlog` | Accepted, prioritized for future | Decision documented, or Linear/GitHub Issue |
| `Todo` | Scheduled, ready to start | Assigned in Linear or explicitly scheduled |
| `In Progress` | Implementation started | Code in repo or open PR |
| `In Review` | PR open, awaiting review | Open PR with review requested |
| `Done` | Working implementation | Code + tests, or merged PR with CI passing |
| `Shipped` | Deployed to production | Deployment evidence from GitHub |
| `Canceled` | Explicitly closed | Issue/PR closed as won't fix, duplicate, etc. |
| `Unknown` | Insufficient evidence | N/A |

---

## Agent Skills as Product Features

Claude Code plugins and agent skills (SKILL.md files) are product features. They serve as executable prompts that define agent behavior.

### Detecting Skill Features

When scanning repositories, also check for:
```
skills/*/SKILL.md
commands/*.md
.claude/skills/*/SKILL.md
.claude/commands/*.md
```

### Skill Status Evidence

| Evidence | Status | Confidence |
|----------|--------|------------|
| SKILL.md exists + tests in `evaluations/` | Complete | High |
| SKILL.md exists (no tests) | In Progress | Medium |
| Skill mentioned in transcripts only | Discussed | Medium |

Include skills in the component status table with type indicator:
```
| grounded-query (skill) | Complete | SKILL.md + evaluations | entourage-plugin | High |
```

## Workflow

1. Identify components/features in query
2. Search data files for transcript mentions of each component
3. Check if `.entourage/repos.json` exists
4. If repos configured with `path` field:
   - Invoke `/local-repo-check <components>` for local git evidence
5. If repos configured with `github` field:
   - Invoke `/github-repo-check <components>` for GitHub evidence
6. If `linear` section configured:
   - Invoke `/linear-check <components>` for Linear issue evidence
7. Combine all evidence sources using the unified hierarchy
8. Output status table with sources

---

## Evidence Sources

This skill uses three sub-skills to verify implementation status:
- `/local-repo-check` - Scans local git repositories
- `/github-repo-check` - Queries GitHub API for PRs, issues, Actions, deployments
- `/linear-check` - Queries Linear for issue tracking status

### Configuration Check

Read `.entourage/repos.json` and check for:
- `path` field in repos - Enables local scanning via `/local-repo-check`
- `github` field in repos - Enables GitHub scanning via `/github-repo-check`
- `linear` section - Enables Linear scanning via `/linear-check`

### With Local Repository (`path` configured)

1. Invoke `/local-repo-check <component-names>`
2. Get evidence: file existence, test files, git history

### With GitHub Repository (`github` configured)

1. Invoke `/github-repo-check <component-names>`
2. Get evidence: PRs, issues, Actions status, deployments

### With Linear (`linear` section configured)

1. Invoke `/linear-check <component-names>`
2. Get evidence: issue status, assignees, workflow state

### Without Any Configuration

- Skip all sub-skills
- Limit status levels to "Triage" (transcript evidence only)
- Add note about configuring sources

---

## Unified Evidence Hierarchy

When combining evidence from transcripts, local repos, GitHub, and Linear, use this priority order:

| Priority | Evidence Type | Source | Max Status |
|----------|--------------|--------|------------|
| 1 | Deployment to production | GitHub | Shipped |
| 2 | PR merged + CI passing | GitHub | Done |
| 3 | Code + tests on main | Local | Done |
| 4 | PR merged (no CI info) | GitHub | Done |
| 5 | Linear issue "Done" | Linear | Done |
| 6 | Code + tests (any branch) | Local | Done |
| 7 | Open PR with approvals | GitHub | In Review |
| 8 | Open PR (review requested) | GitHub | In Review |
| 9 | Linear issue "In Review" | Linear | In Review |
| 10 | Code exists (no tests) | Local | In Progress |
| 11 | Open PR (no reviews) | GitHub | In Progress |
| 12 | Feature branch exists | Local | In Progress |
| 13 | Linear issue "In Progress" | Linear | In Progress |
| 14 | GitHub Issue (in progress label) | GitHub | In Progress |
| 15 | Linear issue "Todo" | Linear | Todo |
| 16 | GitHub Issue (open) | GitHub | Backlog |
| 17 | Linear issue "Backlog" | Linear | Backlog |
| 18 | Architecture decision documented | Transcripts | Backlog |
| 19 | Linear issue "Triage" | Linear | Triage |
| 20 | Meeting discussion | Transcripts | Triage |

**Rule:** Higher priority evidence overrides lower. If GitHub shows PR merged but local shows no tests, use the GitHub evidence (Done).

---

## Conflict Resolution: GitHub is Source of Truth

When local and GitHub evidence conflict (e.g., PR merged on GitHub but local repo not updated):

**GitHub wins** - GitHub represents the canonical shared state.

When this conflict is detected, add a sync note to the output:
```
Info: Local repo may be behind remote. Consider running `git pull`.
```

---

## Context Mismatch Detection

After scanning configured repos, check if results suggest misconfiguration:

### Warning Triggers

1. **High Unknown Rate**: >50% of queried components return "Unknown" status
2. **Transcript Mismatch**: Transcripts mention repo names not in repos.json
3. **Empty Scans**: Configured repos return no relevant code for any component

### Warning Output

When triggered, add to Notes section:
```
Warning: Configured repos may not contain the discussed features.
- Transcripts mention: entourage-web, entourage-api
- Configured repos: entourage-plugin
Consider updating `.entourage/repos.json` to include missing repositories.
```

### Detection Method

1. After transcript search, extract repo names mentioned (patterns: `entourage-*`, `*-web`, `*-api`)
2. Compare against repos.json entries
3. If mismatch detected, include warning in output

---

## Output Format

```
## Status: [Project Name]

| Component | Status | Evidence | Source | Confidence |
|-----------|--------|----------|--------|------------|
| [Name] | Discussed/Planned/etc | [Brief description] | [Source] | High/Med/Low |

### Notes
- [Any caveats about verification limitations]
```

## Critical Rule

**Never mark a component as "Done" or "In Progress" based solely on meeting transcripts.**

Meeting transcripts can only support `Triage` or `Backlog` status. Higher statuses require code evidence from repositories (local, GitHub) or issue tracking evidence (Linear).

If no sources are configured, add this note:
> Source verification not configured. Maximum verifiable status is "Triage". Add repos or Linear to `.entourage/repos.json` for implementation status.

---

## Example Output

### With All Sources (Local, GitHub, Linear)

**Query:** "What's the status of authentication?"

```
## Status: Entourage

| Component | Status | Evidence | Source | Confidence |
|-----------|--------|----------|--------|------------|
| Clerk auth | Shipped | PR #42 merged, deployed to prod | GitHub | Very High |
| User dashboard | Done | PR #45 merged, CI passing | GitHub + Local | High |
| Email notifications | In Review | PR #48 open, 2 approvals | GitHub | High |
| Analytics | Backlog | Issue #52 created | GitHub | High |
| Notifications | Triage | Mentioned Dec 21 meeting | Transcripts | High |

Info: Local repo may be behind remote. Consider running `git pull`.

### Evidence Details

**Clerk auth (Shipped)**
- PR: #42 "Add Clerk authentication" - merged Jan 8
- Actions: Build, Test, Lint passed
- Deployment: prod-v1.2.0 deployed Jan 8 14:32 UTC

**User dashboard (Done)**
- PR: #45 "User dashboard" - merged Jan 10
- Actions: Build, Test passed
- Local: Tests found at `src/dashboard/__tests__/`
```

### With Linear and Local Only

**Query:** "What's the status of authentication?"

```
## Status: My Project

| Component | Status | Evidence | Source | Confidence |
|-----------|--------|----------|--------|------------|
| Clerk auth | Done | Tests passing, merged to main | my-project | High |
| User dashboard | In Progress | TEAM-123 In Progress, code exists | Linear + Local | High |
| Email notifications | Todo | TEAM-456 scheduled | Linear | High |
| Payments | Backlog | TEAM-789 in backlog | Linear | High |

### Notes
- GitHub verification not configured. Add `github` field to repos for PR/CI/deployment status.
```

### Without Any Configuration

**Query:** "What's the status of the database?"

```
## Status: Entourage

| Component | Status | Evidence | Source | Confidence |
|-----------|--------|----------|--------|------------|
| Database schema | Backlog | Architecture decided Dec 22 | Transcripts | Medium |
| Clerk auth | Triage | Mentioned Dec 21 | Transcripts | Low |
| API endpoints | Unknown | No mentions found | - | Low |

### Notes
- Source verification not configured. Maximum verifiable status is "Triage".
- Add repos to `.entourage/repos.json` for implementation status.
- Add `linear` section for issue tracking status.
```

---

## After Output

This skill returns results to the calling context. **Do not stop execution.**
Continue with the next step in the workflow or TODO list.
