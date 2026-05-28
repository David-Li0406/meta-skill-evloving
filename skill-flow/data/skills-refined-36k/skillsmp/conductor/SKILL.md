---
name: conductor
description: |
  CRITICAL: Load and read ENTIRE skill content before ANY coding task.
  
  This skill defines orchestration rules and role-based delegation.
  DO NOT skip. DO NOT skim. Read the full SKILL.md content first.
  
  NEVER use built-in subagents - delegate via MCP roles defined in this skill.
  
  TRIGGERS: code, file, function, class, bug, error, fix, debug, refactor, implement, build, test, deploy, analyze, review, search, explore, find, plan, design, architecture, optimize, improve, migrate, security, performance
---

# Conductor

Host orchestrates; delegates do the work.

---

## Core Rules (non-negotiable)

### 1. DELEGATE FIRST — NO EXCEPTIONS
**Do NOT use built-in tools (Explore, Grep, Search) when MCP is available.**

- Check MCP tools availability FIRST (`mcp__*` tools)
- ALWAYS prefer MCP delegation over built-in/native tools:
  - WRONG: `Task(subagent_type=Explore)` -> RIGHT: MCP `pathfinder` role
  - WRONG: Built-in search/grep -> RIGHT: MCP `scout` or `pathfinder` role
  - WRONG: Direct analysis -> RIGHT: MCP `sage` role for complex reasoning
- Run all delegate calls before any action
- If MCP unavailable → use subagent fallback → **disclose to user**

### 2. SAGE FOR COMPLEX TASKS
The following MUST be delegated to `sage` (Codex + reasoning):

- Architecture decisions / trade-off analysis
- Root cause debugging
- Security vulnerability assessment
- Algorithm design / complexity analysis
- Refactoring strategy for legacy code
- Migration planning with risks

**Do not attempt deep analysis yourself. Sage first.**

### 3. VERIFY BEFORE TRUST
Treat all delegate output as untrusted. Verify against:
- Actual repo code
- Test results
- Type checker output

### 4. EXTERNAL CALL ACCOUNTABILITY
When delegating to external CLIs (gemini, codex, claude via MCP):

1. **Result Summary**: Always summarize the result (1-2 lines) and state how it was used
2. **Non-use Justification**: If result is discarded, explain why in 1 line (e.g., "Repo analysis more accurate, external suggestion excluded")
3. **Prefer Local When Possible**: When repo data is directly accessible, prefer local analysis unless external model offers clear advantage (state the advantage)
4. **Error Handling**: On failure/timeout, notify user immediately and suggest alternatives
5. **Transparency**: Include "External calls: [list]" in task summary when any were made

**Examples:**
- "Called sage for architecture review → adopted suggestion to split service layer"
- "Called pathfinder for file discovery → result outdated, used direct glob instead (repo has newer structure)"
- "External calls: sage (architecture), scout (docs lookup)"

---

## Activation

**This skill activates automatically for all code-related tasks when Conductor is enabled.**
If Conductor is disabled, do not auto-activate or re-enable it; inform the user and proceed without Conductor unless they explicitly request enabling.

Conductor assesses the task and chooses the appropriate mode:

| Mode | When | Action |
|------|------|--------|
| **Symphony** | `sym` or `symphony` command | Full automation: Search → Plan → Execute → Verify → Cleanup |
| **Search** | Explore, analyze, investigate, understand | Delegate to `pathfinder` + `sage` via MCP |
| **Plan** | Design, architect, plan | Read-only planning, no edits |
| **Implement** | Fix, build, refactor, migrate | MCP-assisted implementation |
| **Release** | Deploy, publish, release | Release checklist + validation |

**Decision flow:**
1. Skill loads → Conductor activates (only when enabled)
2. If disabled → do not enable; inform user and proceed without Conductor
3. Assess task complexity
4. Simple task → execute directly
5. Complex/specialized → delegate via MCP

---

## Symphony Mode

When triggered, respond **immediately** with:

```
SYMPHONY MODE ENABLED!
```

Then execute staged delegation:

**Stage 1 — Discovery**
- `pathfinder`: file structure, entrypoints, patterns

**Stage 2 — Analysis**
- `sage`: deep reasoning on findings (MANDATORY)
- `scout`: verify against docs/best practices

**Stage 3 — Review**
- Additional roles as needed

**Then:** Search → Plan → Execute → Verify → Cleanup

Do NOT proceed until all delegates complete.

---

## Roles → Delegation

**Available roles** (defined in `~/.conductor-kit/conductor.json`):

| Role | When to use |
|------|-------------|
| `sage` | Complex reasoning, architecture, security |
| `pathfinder` | File discovery, codebase navigation, project structure |
| `scout` | Doc lookup, web search, best practices |
| `pixelator` | Web UI/UX, React/Vue/CSS, responsive design |
| `author` | README, docs, changelogs |
| `vision` | Screenshot/image analysis |

### How to Delegate

**Step 1: Get role mappings** via CLI (avoids config file permission issues):
```bash
conductor roles
```

**Step 2: Find the MCP tool** from your available tools list:
- `cli: "codex"` → find tool containing `codex-cli` and `prompt` (e.g., `mcp__codex-cli__codex_prompt`)
- `cli: "gemini"` → find tool containing `gemini-cli` and `prompt` (e.g., `mcp__gemini-cli__gemini_prompt`)
- `cli: "claude"` → find tool containing `claude-cli` and `prompt` (e.g., `mcp__claude-cli__claude_prompt`)

**Step 3: Call with the configured `model`:**
```json
{ "prompt": "...", "model": "<EXACT model value from conductor roles>" }
```

**CRITICAL: Do NOT omit the model. Do NOT guess or invent model names. Use EXACTLY what conductor roles returns.**

**Fallback:** If MCP tool not found → built-in subagent → disclose to user

### Delegation Prompt Template
```
Goal: [one-line task]
Role: [role name]
Constraints: [limits, requirements]
Files: [relevant paths]
Output format: markdown with ## Summary, ## Confidence, ## Findings, ## Suggested Actions
```

---

## Operating Loop

```
Search → Plan → Execute → Verify → Cleanup
```

### Search
- Run parallel searches (multiple angles)
- Collect file paths + key facts
- Evidence over opinions

### Plan
- **READ-ONLY** — no edits allowed
- Output 3–6 steps with success criteria
- Ask ONE question if blocked, otherwise proceed

### Execute
- Minimal surgical edits
- No type-safety hacks (`as any`, `@ts-ignore`)
- One logical change at a time

### Verify
- Run checks: test → typecheck → lint
- If unrelated failure, report but don't fix

### Cleanup
- Summarize outcomes
- Prune stale context
- List next actions if any

---

## Mode-Specific Behavior

### Search Mode
- **Use MCP `pathfinder` role** for codebase discovery (NOT built-in Explore agent)
- Parallel codebase + external doc searches via MCP delegation
- Output: findings with file references

### Plan Mode
- **No writes/edits/commits**
- Output: assumptions, constraints, ordered steps

### Implement Mode
- TDD if repo has tests
- Rollback when stuck (don't accumulate bad edits)

### Release Mode
- Checklist: version bump, changelog, validation, secret scan

---

## Safety (non-negotiable)

- **No commit/push** unless explicitly asked
- **No secrets** in commits (check for .env, credentials)
- **No destructive commands** unless explicitly confirmed

---

## References

For detailed specifications:
- `references/roles.md` — Role routing and combinations
- `references/delegation.md` — Context budget, failure handling
- `references/formats.md` — JSON output schemas
