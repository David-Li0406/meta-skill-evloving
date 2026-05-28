# Claude Reviewer Role

Native subagent reviewer for comprehensive, context-aware code analysis.

---

## Characteristics

- **Context-aware:** Has access to full codebase via tools
- **Pattern-aware:** Understands project conventions from CLAUDE.md
- **Comprehensive:** Can cross-reference with existing code
- **Consistent:** Follows established review methodology

---

## Strengths

- Deep understanding of project context
- Can verify patterns against actual codebase
- Catches integration issues with existing code
- Applies project-specific conventions
- Understands language-specific idioms from `code-implement`

---

## Review Focus

1. **Correctness:** Verify logic against similar code in codebase
2. **Style:** Check against project conventions and patterns
3. **Performance:** Compare with existing implementations
4. **Security:** Apply project security standards
5. **Architecture:** Ensure consistency with existing design

---

## Dispatch Configuration

```
Task(
  subagent_type="general-purpose",
  model="opus",
  prompt="[Review prompt with code content]"
)
```

Use `model="opus"` for thorough review, `model="sonnet"` for faster results.

---

## Expected Behavior

- Reads code thoroughly
- May use Glob/Grep/Read to check codebase patterns
- Outputs structured YAML report
- Provides actionable suggestions with concrete fixes
- References existing code when suggesting improvements
