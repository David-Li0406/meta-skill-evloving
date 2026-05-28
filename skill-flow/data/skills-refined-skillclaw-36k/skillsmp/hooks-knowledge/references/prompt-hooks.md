# Prompt Hooks (LLM-Based)

> **Pattern**: Qualitative evaluation using LLM judgment
> **Use For**: Stop and SubagentStop events only
> **Philosophy**: Review and validate response quality, not deterministic operations

## Overview

Prompt hooks use Haiku (fast LLM) for **qualitative evaluation**. They can only be used with `Stop` and `SubagentStop` events for reviewing response quality and completeness.

**⚠️ CRITICAL**: Prompt hooks ONLY work for Stop and SubagentStop. For all other events, use command hooks.

## When to Use Prompt Hooks

**Use Prompt Hooks For**:
- Quality review of responses
- Completeness validation
- Style and clarity checks
- Content review (not security)
- Subjective evaluation

**Use Command Hooks For**:
- Security validation
- Path safety checks
- Deterministic operations
- Fast validation
- All non-Stop/SubagentStop events

## Common Patterns

### 1. Response Quality Review

**Event**: `Stop`
**Purpose**: Review response for quality before session ends

```yaml
---
name: code-reviewer
description: "Reviews code for quality and best practices"
hooks:
  Stop:
    - hooks:
        - type: "prompt"
          prompt: "Review this response for code quality. Check for: 1) Best practices followed, 2) Security considerations, 3) Performance implications, 4) Clarity and maintainability. Provide specific feedback on any issues found."
---
```

### 2. Content Completeness Check

**Event**: `Stop`
**Purpose**: Ensure response addresses all requirements

```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Evaluate if this response fully addresses the user's request. Check: 1) All questions answered, 2) Examples provided where needed, 3) Edge cases considered, 4) Next steps suggested. Rate completeness from 1-10."
    }]
  }]
}
```

### 3. Subagent Output Review

**Event**: `SubagentStop`
**Purpose**: Review subagent output for quality

```json
{
  "SubagentStop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review the subagent's output for accuracy and completeness. Check: 1) Correct analysis, 2) No missing information, 3) Clear conclusions, 4) Actionable recommendations. Flag any issues."
    }]
  }]
}
```

### 4. Project Standards Validation

**Event**: `Stop`
**Purpose**: Ensure code meets project standards

```yaml
---
name: standards-validator
description: "Validates code against project standards"
hooks:
  Stop:
    - hooks:
        - type: "prompt"
          prompt: "Review code against project standards defined in CLAUDE.md. Check: 1) Naming conventions, 2) Documentation present, 3) Error handling, 4) Type safety. Note any deviations."
---
```

### 5. Security Review

**Event**: `Stop`
**Purpose**: Review for security implications

```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review this code for security vulnerabilities. Check: 1) Input validation, 2) SQL injection risks, 3) XSS vulnerabilities, 4) Authentication issues, 5) Data exposure. Report any concerns."
    }]
  }]
}
```

## Prompt Design Guidelines

### Effective Prompts

**DO ✅**:
- Be specific about what to evaluate
- Provide clear criteria (list numbered points)
- Ask for specific feedback, not just yes/no
- Reference project standards when applicable
- Keep prompts concise but comprehensive

**Example**:
```markdown
Review this deployment response. Evaluate:
1. **Rollback plan**: Is a rollback strategy clearly defined?
2. **Testing**: Are deployment tests specified?
3. **Monitoring**: Is monitoring and alerting covered?
4. **Security**: Are security considerations addressed?
5. **Documentation**: Are deployment steps documented?

Provide specific feedback on any gaps or issues.
```

### Ineffective Prompts

**DON'T ❌**:
- Vague: "Check if this is good"
- Overly broad: "Review everything"
- No criteria: "Is this correct?"
- Too long: Complex multi-part evaluations
- Binary: Yes/no questions without context

**Example of BAD prompt**:
```markdown
Is this response good?  # Too vague, no criteria
```

## Integration with Command Hooks

**Best Practice**: Use both types together:

```yaml
---
name: secure-deploy
description: "Deploy with security validation"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"  # Deterministic validation
  Stop:
    - hooks:
        - type: "prompt"
          prompt: "Review deployment for security best practices."  # Qualitative review
---
```

## Workflow Pattern

### 1. Command Hook (PreToolUse)
- **Fast, deterministic**
- Validates inputs
- Runs tests
- Checks security patterns

### 2. Prompt Hook (Stop)
- **Qualitative evaluation**
- Reviews overall quality
- Validates completeness
- Checks against standards

## Performance Considerations

**Prompt hooks use Haiku** (fast, cost-effective LLM):
- Quick evaluation (<2 seconds)
- Lower cost than Opus/ Sonnet
- Good for quality checks
- Not for complex reasoning

**Cost Optimization**:
- Use command hooks for validation
- Use prompt hooks only for qualitative review
- Keep prompts concise
- Avoid unnecessary Stop hooks (can slow response)

## Limitations

### What Prompt Hooks CANNOT Do:
- ❌ Validate file paths (use command hooks)
- ❌ Block operations (can't use `exit 2`)
- ❌ Run tests (use command hooks)
- ❌ Check security vulnerabilities directly
- ❌ Work with PreToolUse, SessionStart, etc.

### What Prompt Hooks CAN Do:
- ✅ Review response quality
- ✅ Check completeness
- ✅ Validate against standards
- ✅ Suggest improvements
- ✅ Review code style
- ✅ Check documentation

## Anti-Patterns

### DON'T Use Prompt Hooks For:
1. **Security validation** (use command hooks)
2. **Fast checks** (use command hooks)
3. **Path validation** (use command hooks)
4. **File operations** (use command hooks)
5. **Any non-Stop/SubagentStop event** (use command hooks)

**Why**: Prompt hooks can't block operations and are slower than command hooks.

## Best Practices Summary

### DO ✅
- Use ONLY for Stop/SubagentStop events
- Provide specific evaluation criteria
- Reference project standards when available
- Keep prompts concise
- Use for qualitative, not deterministic checks
- Combine with command hooks for complete validation

### DON'T ❌
- Don't use for PreToolUse or other events
- Don't use for security validation
- Don't create vague prompts
- Don't use for blocking operations
- Don't rely on prompt hooks alone
- Don't use for performance-critical checks

## Example Workflow

```yaml
---
name: quality-gate-deploy
description: "Deploy with complete validation"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "validate-deploy.sh"  # Fast, deterministic
  Stop:
    - hooks:
        - type: "prompt"
          prompt: |
            Review deployment plan for:
            1. Rollback strategy present
            2. Testing coverage adequate
            3. Security checklist complete
            4. Monitoring configured
            Provide feedback on completeness.
---
```

## Reference

- **Hooks Guide**: https://code.claude.com/docs/en/hooks
- **Command Hooks**: [command-hooks.md](command-hooks.md)
- **Security Patterns**: [security-patterns.md](security-patterns.md)
