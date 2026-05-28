---
name: vibe-coding
description: High-velocity, intent-driven development using agentic workflows and MCP servers.
---

# Vibe Coding Skill

Operate as a high-velocity coder: express intent, orchestrate tools, build fast.

## When to Use
- Rapid prototyping
- Intent-based requests ("make it feel modern")
- Complex multi-step implementations
- When user wants minimal back-and-forth

## 1. Core Principles

- **Intent over Implementation**: Focus on outcome, not every CSS property
- **Agentic Orchestration**: Break complex tasks into sub-tasks
- **Zero Friction**: Resolve trivial blockers proactively

## 2. Tool Priority

| Tool | When to Use |
|------|-------------|
| `context7` | Always—verify library docs before coding |
| `search_web` | Find "best-in-class" examples and trends |
| `supabase-mcp-server` | Database operations, auth, storage |
| `run_command` | Build, lint, test after significant changes |

## 3. Engagement Patterns

```tsx
// Instant Feedback Example
<button
  onClick={handleSave}
  className="btn-primary"
  disabled={isSaving}
>
  {isSaving ? <Spinner /> : <CheckIcon />}
  {isSaving ? 'Saving...' : 'Saved!'}
</button>

// Micro-onboarding Tooltip
<Tooltip content="Click here to get started">
  <InfoIcon />
</Tooltip>
```

### Quick Wins
- Glowing buttons on success
- Progress indicators for async ops
- Subtle tooltips for new features
- Empty states that guide users

## 4. Automation

After significant changes, run project quality checks if available:
```bash
# Check if script exists before running
npm run lint 2>/dev/null || echo "No lint script"
npm run build 2>/dev/null || echo "No build script"
```

## 5. Code Style

- Prefer fewer lines of code
- Use latest stable ES features
- Self-documenting variable names
- Extract repeated logic into helpers

---

> **Cross-reference**: See `best-practices` skill for UI/UX standards and research protocols.
