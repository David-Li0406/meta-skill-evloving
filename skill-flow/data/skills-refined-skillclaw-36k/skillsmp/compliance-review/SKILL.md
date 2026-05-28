---
name: compliance-review
description: This skill should be used when the user asks to "check CLAUDE.md compliance", "review against coding standards", "check AI agent instructions", "verify guidelines", "check coding conventions", "check naming conventions", or wants to ensure code follows project-specific rules and standards.
version: 3.1.1
---

# Compliance Code Review Skill

Verify code adherence to AI Agent Instructions (CLAUDE.md, copilot-instructions, and similar files) and project-specific rules through targeted compliance-focused code review.

## When to Use

Use this skill to:
- Check code against CLAUDE.md rules
- Verify coding standards adherence
- Review AI agent instructions compliance
- Validate project guidelines
- Check convention adherence
- Verify architecture pattern compliance
- Check naming convention consistency

## Process Overview

1. **Determine scope** - Identify code requiring compliance review
2. **Gather context** - Detect project type and locate all AI instruction files
3. **Launch compliance agent** - Execute thorough mode, then gaps mode
4. **Validate findings** - Confirm issues against exact rule text
5. **Report results** - Generate output with exact rule citations

For detailed procedures on steps 1, 2 (project type detection), 4, and 5, see `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`.

---

## Compliance-Specific Configuration

### Agent Parameters

- **Agent:** `${CLAUDE_PLUGIN_ROOT}/agents/compliance-agent.md`
- **Model:** Sonnet (for efficient compliance checking)
- **Modes:** thorough (first pass), gaps (second pass)

### Instruction File Locations (Part of Step 2)

See `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md` Step 2 for the canonical search order.

---

## Rule Classification

For rule classification (MUST/SHOULD/MAY keywords and severity mapping), see `references/compliance-patterns.md`.

---

## Compliance Categories Checked

**Architecture Violations (Major):**
- Layer violations (UI importing from data layer)
- Business logic in wrong location (controller, view)
- Direct database access bypassing repositories
- Circular dependencies

**Naming Convention Violations (Minor to Major):**
- File naming patterns (kebab-case, PascalCase)
- Class/function/variable naming
- Constant naming (UPPER_SNAKE_CASE)
- Interface prefixing (I prefix in C#)

**Documentation Requirements (Minor):**
- Missing JSDoc/XMLDoc on public APIs
- Undocumented complex functions
- README updates for new features

**Security Requirements (Major):**
- Missing authentication on endpoints
- Input validation gaps
- Logging requirements for sensitive operations

---

## Auto-Validated Patterns

These high-confidence patterns skip validation:

| Pattern | Description |
|---------|-------------|
| `missing_authorize_attribute` | Controller action without `[Authorize]` when CLAUDE.md requires auth |
| `wrong_case_filename` | File using wrong case pattern (e.g., PascalCase in Node.js project) |
| `explicit_must_violation` | Code contradicts explicit "MUST" or "MUST NOT" rule with exact match |
| `missing_required_jsdoc` | Public API without JSDoc when CLAUDE.md requires documentation |

---

## Compliance-Specific False Positives

Do NOT flag:
- Explicit override comments (`// claude-ignore: rule-name`)
- Scope mismatch (rule doesn't apply to this file type)
- Ambiguous rule (benefit of doubt to code)
- Intentional deviation with documented reason
- Framework exemption (framework provides required behavior)

### Ignore Comment Patterns

Respect these silencing patterns:
```javascript
// claude-ignore: no-console
// eslint-disable-next-line rule-name
// @ts-ignore: explanation
```

---

## Rule Citation Guidelines

Always include exact rule citation:

- **Rule text**: Exact quoted text from instruction file
- **Source**: File path and line number
- **Keyword**: The strength keyword (MUST, SHOULD, MAY)

Example: "The endpoint violates 'All API endpoints MUST have authentication' from CLAUDE.md:31"

---

## Compliance Score

Include in output:

```markdown
### Compliance Score

- Rules checked: 28
- Rules passed: 24
- Rules violated: 4
- Compliance rate: 86%
```

---

## Example Output

See `examples/example-output.md` for a sample showing:
- Missing authentication violation with diff fix
- Business logic in controller with prompt fix
- Missing JSDoc violation with diff fix

---

## Additional Resources

### Reference Files

For detailed compliance patterns:
- **`references/compliance-patterns.md`** - Rule classification, common rule categories, checking process

### Related Components

- **Agent Definition:** `${CLAUDE_PLUGIN_ROOT}/agents/compliance-agent.md`
- **Subagent Type:** `code-review:compliance-agent` (for Task tool invocation)
- **Language checks:** `${CLAUDE_PLUGIN_ROOT}/languages/nodejs.md`, `${CLAUDE_PLUGIN_ROOT}/languages/dotnet.md`
- **Common workflow:** `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`
