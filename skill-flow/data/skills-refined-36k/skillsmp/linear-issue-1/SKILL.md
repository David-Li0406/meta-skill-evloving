---
name: linear-issue
description: Create a Linear issue. Use when user asks to create an issue, register a task, track work, or needs a ticket before starting development. Do NOT load for: implementation work, code review, deployment.
allowed-tools: ["mcp__plugin_linear_linear__*", "AskUserQuestion"]
user-invocable: true
---

# Linear Issue Registration Skill

Create a new Linear issue.

## Configuration

**Team Selection:** Query available teams dynamically using `mcp__plugin_linear_linear__list_teams`, then select the appropriate team. If only one team exists, use it automatically.

 # Mandatory Labels (CRITICAL)

**Every issue MUST have these labels:**

### 1. Type Label (MANDATORY - Choose ONE)

| Type | Purpose | Creates PR? |
|------|---------|-------------|
| **Feature** | New functionality | Yes |
| **Bug** | Fix broken behavior | Yes |
| **Chore** | Config, CI, maintenance | Usually Yes |
| **Thinking** | Design, research, memo | No |

**This is the primary classification for MCP operations.**

Simple rule:
- **Feature / Bug / Chore** → Produces PR, needs worktree
- **Thinking** → No PR, no worktree needed

### 2. Repository Label (MANDATORY - Choose ONE)

Every issue MUST have exactly one Repository label (exclusive).
Query existing labels: `mcp__plugin_linear_linear__list_issue_labels` with `team` parameter.
(チーム固有のRepositoryラベルを取得するため、teamパラメータは必須)

## Prerequisites

- Linear MCP tools are available (`mcp__plugin_linear_linux__*`)

## Workflow

### Step 1: Determine Type Label

Ask or determine from context:

**Feature**: New functionality being added
**Bug**: Something is broken and needs fixing
**Chore**: Config, CI, dotfiles, non-functional tasks
**Thinking**: Research, design comparison, hypothesis, undecided

If unclear, ask: "Does this produce a PR?"
- YES → Feature / Bug / Chore
- NO / Undecided → Thinking

### Step 2: Determine Team

Query teams: `mcp__plugin_linear_linear__list_teams`
- If single team → use automatically
- If multiple teams → ask user or infer from context

### Step 3: Gather Information + Repository Label

**IMPORTANT:** Query Repository labels with team parameter:
`mcp__plugin_linear_linear__list_issue_labels` with `team: <selected_team>`

**CRITICAL:** ラベル付与時は名前ではなくIDを使用すること。
`list_issue_labels`の結果から該当ラベルのIDを取得し、`create_issue`の`labels`パラメータにはIDを指定する。

**For Feature / Bug / Chore:**
- Repository label (select from team's Repository label group)
- What to change (files, behavior)
- Done criteria (clear and measurable)

**For Thinking:**
- Repository label (select from team's Repository label group)
- Topic/question
- Current state
- Options/candidates
- Decision criteria (if any)

### Step 4: Create Issue

Use `mcp__plugin_linear_linear__create_issue` with:
- `team`: Selected team name or ID
- `title`: English (for branch name generation)
- `description`: User's language (see templates below)
- `labels`: [Type label ID, Repository label ID] ← 名前ではなくIDを使用

## Description Templates

### Feature / Bug / Chore Template

```markdown
Repo: {repository-name}
Files:
- src/xxx.ts
- src/yyy.ts

Done Criteria:
- [ ] Specific condition is satisfied
- [ ] Existing behavior unchanged
- [ ] Tests pass
```

Keep it concise. NO thinking logs.

### Thinking Template

```markdown
## Current State
{What exists now}

## Options
- Option A: ...
- Option B: ...

## Decision Criteria
- Criterion 1
- Criterion 2

## Notes
{Free-form thinking, long text OK}
```

Thinking Issues:
- Do NOT need to be Done
- Can stay in Todo/Backlog indefinitely
- Can contain long text

## Step 5: Return Information

After creation, provide:
- Issue identifier (e.g., DEV-123-feat-awesome-feature)
- Issue URL
- Applied labels (Type + Repository)
- Auto-generated branch name (for Feature/Bug/Chore)

## Thinking → Feature/Bug/Chore Flow

When a Thinking Issue leads to implementation:

1. Keep the Thinking Issue open (or close, your choice)
2. Create a **new** Feature/Bug/Chore Issue
3. Link from the Thinking Issue
4. Complete the new Issue

Never mix thinking logs into Feature/Bug/Chore Issues.

## Error Handling

| Scenario | Action |
|----------|--------|
| Type unclear | Ask "Does this produce a PR?" |
| Repository Label not found | Query labels, create if needed |
| Missing title | Prompt user using AskUserQuestion |

## Important Notes

- Linear is for "action management", GitHub is for "change history"
- Do NOT use GitHub Issues - Linear is the single source of truth
- Status is auto-managed via GitHub or other service integrations
- Branch names are auto-generated - never create locally
- Issue title MUST be in English for clean branch names
