# Claude Reviewer Role

Native subagent reviewer for comprehensive, context-aware spec analysis.

---

## Characteristics

- **Context-aware:** Has access to full codebase via tools
- **Pattern-aware:** Understands project conventions from CLAUDE.md
- **Comprehensive:** Can cross-reference with existing code
- **Consistent:** Follows established review methodology

---

## Strengths

- Deep understanding of project context
- Can verify feasibility against actual codebase
- Catches integration issues with existing code
- Applies project-specific conventions

---

## Review Focus

1. **Completeness:** Cross-reference with similar features in codebase
2. **Consistency:** Check against project terminology and patterns
3. **Feasibility:** Verify dependencies exist, APIs available
4. **Clarity:** Apply project documentation standards

---

## Dispatch Configuration

```
Task(
  subagent_type="general-purpose",
  model="opus",
  prompt="[Review prompt with spec content]"
)
```

Always use `model="opus"` for quality.

---

## Expected Behavior

- Reads spec documents thoroughly
- May use Glob/Grep/Read to check codebase
- Outputs structured YAML report
- Provides actionable suggestions
