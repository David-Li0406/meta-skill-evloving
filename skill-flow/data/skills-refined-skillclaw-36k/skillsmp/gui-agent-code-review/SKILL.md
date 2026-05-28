---
name: gui-agent-code-review
version: 1.0.0
description: |
  This skill should be used when the user asks to "review code", "code review", "check my changes", "review this PR", "review my implementation", "PR review", "look at my code", or when reviewing GUI automation code, vision agent code, or PyAutoGUI-based automation. Provides domain-specific review criteria covering prompts, debugging, context management, action design, and coordinate systems.
---

# GUI Agent Code Review

A specialized code review skill for GUI automation projects that applies domain-specific criteria across five key areas: LLM prompts, execution debugging, context optimization, action design, and screenshot/coordinate handling.

## When to Use

Apply this skill when reviewing:
- Changes to core agent logic (main orchestrator, context manager)
- LLM prompt modifications (system prompts, planning prompts)
- New action types or input controller changes
- Screenshot handling or coordinate system changes
- Context management or token optimization code
- Any pull request to a GUI automation project

## Review Process

### 1. Identify Changed Domains

First, categorize the changes by domain:

| Domain | Files/Patterns | Key Concerns |
|--------|---------------|--------------|
| Prompts | `SYSTEM_PROMPT`, `*_PROMPT`, prompt strings | Clarity, token efficiency, structured output |
| Debugging | Executor, error handling, logging | Failure traceability, recovery paths |
| Context | `context_manager.py`, history handling | KV-cache stability, token budget, compression |
| Actions | `ActionType`, `InputController`, `_*` methods | Schema consistency, PyAutoGUI safety |
| Screenshots | `ScreenController`, grid overlay, coordinates | Normalized coords, resolution handling |

### 2. Apply Domain-Specific Criteria

For each domain touched by the changes, apply the relevant review criteria from the checklist in `references/review-checklist.md`.

### 3. Assess Cross-Domain Impact

Check for cross-domain concerns:
- **Prompt → Action**: Do prompt instructions match available action types?
- **Action → Screenshot**: Do new actions handle coordinate normalization?
- **Context → Prompt**: Does context compression preserve critical prompt info?
- **Screenshot → Debugging**: Are coordinates logged for failure analysis?

### 4. Provide Structured Feedback

Format review feedback as:

```markdown
## Code Review: [file/feature]

### Domain: [domain name]
**Severity**: [Critical/Important/Minor]
**Issue**: [Description]
**Suggestion**: [How to fix]
**Reference**: [Line number or code snippet]
```

## Quick Reference: Critical Checks

### Prompts (from prompt-engineer domain)
- [ ] Clear, unambiguous instructions
- [ ] Structured output format specified (JSON schema)
- [ ] Token-efficient (no redundant examples)
- [ ] Consistent terminology with codebase

### Debugging (from plan-debugger domain)
- [ ] Errors include context (what was attempted, what failed)
- [ ] Screenshots saved before/after actions
- [ ] Action results logged with coordinates
- [ ] Recovery paths for common failures

### Context (from context-optimizer domain)
- [ ] Stable prefix never modified after init
- [ ] History compression preserves task-critical info
- [ ] Token budget respected (check ContextConfig)
- [ ] Checkpoint/restore compatibility maintained

### Actions (from action-designer domain)
- [ ] ActionType enum updated for new actions
- [ ] NextAction model has required fields
- [ ] InputController.execute() handles new type
- [ ] Appropriate action_delay after execution
- [ ] Error handling returns (False, "message")

### Screenshots (from screenshot-analyzer domain)
- [ ] Coordinates normalized (0.0-1.0 range)
- [ ] Grid overlay respects add_grid parameter
- [ ] Resolution-independent calculations
- [ ] Pixel conversion uses screen dimensions

## Common Issues by Domain

### Prompt Issues
| Issue | Detection | Fix |
|-------|-----------|-----|
| Ambiguous instructions | Multiple valid interpretations | Add explicit constraints |
| Missing output format | No JSON schema reference | Add Pydantic model reference |
| Token bloat | Repeated examples | Use single clear example |

### Debugging Issues
| Issue | Detection | Fix |
|-------|-----------|-----|
| Silent failures | Bare `except:` | Log error, return (False, str(e)) |
| Missing context | Error lacks action info | Include action type and params |
| No screenshots | Failed action without visual | Call _save_screenshot before action |

### Context Issues
| Issue | Detection | Fix |
|-------|-----------|-----|
| Prefix mutation | System prompt modified mid-session | Make prefix immutable after init |
| Aggressive compression | Task info lost | Increase min_recent_pairs |
| Token overflow | Context exceeds max_tokens | Trigger compression earlier |

### Action Issues
| Issue | Detection | Fix |
|-------|-----------|-----|
| Missing enum value | New action not in ActionType | Add to enum class |
| Unhandled in execute | No elif branch | Add dispatch case |
| No delay | Immediate return after action | Add time.sleep(config.action_delay) |

### Screenshot Issues
| Issue | Detection | Fix |
|-------|-----------|-----|
| Pixel coordinates | Values > 1.0 | Normalize: x / screen_width |
| Grid misalignment | Labels don't match positions | Check font offset calculation |
| Resolution assumptions | Hardcoded 1920x1080 | Use pyautogui.size() |

## Integration with Agents

This skill encodes knowledge from five specialized agents. For deeper analysis, invoke the relevant agent:

| Domain | Agent | When to Escalate |
|--------|-------|-----------------|
| Prompts | `prompt-engineer` | Major prompt rewrites, new LLM integrations |
| Debugging | `plan-debugger` | Complex failure patterns, execution traces |
| Context | `context-optimizer` | Token budget redesign, compression algorithms |
| Actions | `action-designer` | New action types, PyAutoGUI patterns |
| Screenshots | `screenshot-analyzer` | Coordinate system changes, grid overlay updates |

Note: These agents are defined in the project's `agents/` directory as part of the gui-agent-dev plugin.

## Additional Resources

### Reference Files

For detailed review criteria and checklists, consult:

- **`references/review-checklist.md`** - Complete checklist with all criteria by domain
- **`references/common-patterns.md`** - Code patterns to look for and their implications

### Project Documentation

These project-level files provide additional context:

- **`docs/ARCHITECTURE.md`** - System architecture overview (if available)
- **Agent files** in `agents/` - Domain-specific expertise for deeper analysis
