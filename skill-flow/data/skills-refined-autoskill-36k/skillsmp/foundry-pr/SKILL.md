---
name: foundry-pr
description: AI-powered PR creation after spec completion. Analyzes spec metadata, git diffs, commit history, and journal entries to generate comprehensive PR descriptions with user approval before creation.
---

# Spec-Driven Development: PR Creation Skill

## Overview

The `foundry-pr` skill creates professional, comprehensive pull requests by analyzing your completed specs and git history. Instead of manually writing PR descriptions, this skill uses AI to analyze all available context and generate detailed, well-structured PR descriptions.

## When to Use This Skill

Use `Skill(foundry:foundry-pr)` to:
- **After Spec Completion**: Create PRs when handed off from sdd-update
- **Comprehensive PRs**: Generate detailed PR descriptions
- **Save Time**: Automate writing thorough PR descriptions

**When NOT to use:**
- For quick, trivial changes (use `gh` CLI directly)
- When you need a very specific custom PR format
- For PRs without an associated spec

## MCP Tooling

This skill works exclusively through the Foundry MCP server (`foundry-mcp`). Tools use the router+action pattern: `mcp__plugin_foundry_foundry-mcp__<router>` with `action="<action>"`.

**Key tools:**
- `mcp__plugin_foundry_foundry-mcp__pr action="create"` - Create PR with spec context
- `mcp__plugin_foundry_foundry-mcp__pr action="context"` - Gather PR context from spec
- `mcp__plugin_foundry_foundry-mcp__journal action="list"` - Get journal entries for context
- `mcp__plugin_foundry_foundry-mcp__spec action="history"` - View spec evolution timeline
- `mcp__plugin_foundry_foundry-mcp__spec action="diff"` - Compare spec versions

### PR Context Enrichment

Use `spec:history` and `spec:diff` to enrich PR descriptions with change context:

```bash
# View spec evolution during implementation
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="{spec-id}" limit=10

# Compare current spec vs original to show requirement evolution
mcp__plugin_foundry_foundry-mcp__spec action="diff" spec_id="{spec-id}" compare_to="specs/.backups/{spec-id}-original.json"
```

**Why this enriches PRs:**
- **history**: Shows requirement changes made during implementation, explaining scope adjustments
- **diff**: Highlights requirements that were added/modified, documenting intentional deviations from original plan

**Include in PR description:**
- Requirements added during implementation
- Scope changes with rationale
- Timeline of significant spec updates

## Core Philosophy

### From Template to Intelligence

Traditional PR creation uses static templates. The foundry-pr skill:

1. **Analyzes Multiple Sources** - Spec metadata, git diffs, commit history, journal entries
2. **Generates Context-Aware Descriptions** - Explains "why" not just "what"
3. **Requires User Approval** - Always shows draft before creation

## Essential Workflow

> `[x?]`=decision · `(GATE)`=user approval · `→`=sequence · `↻`=loop · `§`=section ref

```
- **Entry** → Gather context → `pr action="context"` → Collect: Spec, Tasks, Commits, Journals, Diff
  - Spec change summary → `spec action="diff"` → `spec action="history"` → Capture requirement evolution
  - AI analysis → Synthesize context
  - Draft PR → (GATE: user review)
    - [approved] → Push branch → Create PR → Update meta → **Exit**
    - [changes] → ↻ back to Draft PR
```

## Context Sources

| Source | What It Provides |
|--------|------------------|
| **Spec Metadata** | Title, description, objectives |
| **Completed Tasks** | Files modified, changes made |
| **Commit History** | Messages, SHAs, task associations |
| **Journal Entries** | Technical decisions, rationale |
| **Git Diff** | Actual code changes |
| **Spec History** | Requirement changes during implementation |
| **Spec Diff** | Comparison showing added/modified requirements |

> For detailed context gathering, see `references/context.md`

### Example: PR with Spec Evolution Context

When specs change during implementation, the PR description captures this:

```markdown
## Summary
Implements OAuth 2.0 authentication with PKCE flow.

## Scope Evolution
During implementation, the following requirements were refined:
- **Added**: Refresh token rotation (task-1-4, discovered during security review)
- **Modified**: Token expiry from 24h → 1h (task-1-2, per security feedback)
- **Removed**: Legacy session fallback (deemed unnecessary)

## What Changed
...
```

This gives reviewers visibility into why the implementation may differ from the original spec.

## PR Structure

Generated PRs include: Summary, What Changed, Technical Approach, Implementation Details, Testing, and Commits sections.

> For full template with examples, see `references/template.md`

## Quick Start

```bash
# After completing a spec, create PR
Skill(foundry:foundry-pr) "Create PR for spec oauth-feature-2025-11-03-001"

# Agent shows draft, user approves, PR created
```

## Long-Running Operations

This skill may take up to 5 minutes. Always use foreground execution with appropriate timeout.

**CRITICAL:** Read [references/long-running.md](./references/long-running.md) before execution. Contains mandatory timeout rules.

## Detailed Reference

For comprehensive documentation including:
- Long-running operations → `references/long-running.md`
- Complete workflow → `references/workflow.md`
- Context sources → `references/context.md`
- PR structure → `references/structure.md`
- Draft template → `references/template.md`
- Examples → `references/examples.md`
- Best practices → `references/best-practices.md`
- Troubleshooting → `references/troubleshooting.md`
