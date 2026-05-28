---
name: code-quality-analysis
description: Use this skill when you need to validate code quality through linting, testing, and comprehensive analysis for security, performance, and architecture.
---

# Code Quality Analysis Skill

## Purpose

This skill validates code quality before commits and performs a comprehensive analysis to identify issues and improvement opportunities across various dimensions such as quality, security, performance, and architecture.

---

## 🔴 Skill Chaining (NON-NEGOTIABLE)

> This skill is called in the `implement(write-code) → write-test` chain.

```text
skill:write-code completed
    │
    └→ "Shall I write tests?"
           │
           ├─ "Please write tests" → skill:write-test
           │       │
           │       └→ "Shall I validate quality?"
           │              └→ skill:code-quality-analysis (this skill)
           │                      │
           │                      └→ "Shall I commit?"
           │                             └→ skill:git-workflow
           │
           └─ "Validate for me" → skill:code-quality-analysis (skip tests)
```

---

## 🔴 Execution Order (NON-NEGOTIABLE)

### Quality Gate Validation Steps

| Step | Command | Description |
|------|---------|-------------|
| 1 | `npm run lint` | ESLint check |
| 2 | `npx tsc --noEmit` | TypeScript type check |
| 3 | `npm run build` | Build validation |
| 4 | `npm test` | Execute tests |

> **⚠️ Each step is executed sequentially and will stop immediately on failure.**

### Comprehensive Code Analysis Steps

1. **Exploration Phase**: Identify files and project structure.
   ```bash
   find src/main -name "*.kt" | head -50
   ```

2. **Scanning Phase**: Apply analysis based on focus areas.
   - Quality: Code smell pattern checks
   - Security: Vulnerability pattern checks
   - Performance: Anti-pattern checks
   - Architecture: Dependency and structure checks

3. **Evaluation Phase**: Prioritize findings.
   - Critical: Immediate fix required
   - High: Quick fix recommended
   - Medium: Planned fix
   - Low: Improvement opportunity

4. **Reporting Phase**: Generate a comprehensive analysis report.

---

## Output Format

### Quality Gate Success

```markdown
[SEMO] Skill: code-quality-analysis completed

✅ **Quality Gate Passed**

| Step | Status | Duration |
|------|--------|----------|
| Lint | ✅ Pass | 2.3s |
| TypeCheck | ✅ Pass | 4.1s |
| Build | ✅ Pass | 12.5s |
| Test | ✅ Pass (42/42) | 8.2s |

---

💡 **Next Step**: Shall I commit?
   - "Please commit" → skill:git-workflow called
   - "No" → wait
```

### Quality Gate Failure

```markdown
[SEMO] Skill: code-quality-analysis failed

❌ **Lint Failed**

Errors:
src/utils/auth.ts
  42:10  error  'foo' is not defined  no-undef
  55:3   error  Unexpected any type    @typescript-eslint/no-explicit-any

💡 Would you like help fixing the errors?
   - "Please fix" → skill:write-code called
   - "Ignore and continue" → proceed to next step (not recommended)
```

### Comprehensive Analysis Summary

```markdown
[SEMO] Skill: analyze-code completed

## 📊 Analysis Summary

| Focus | Critical | High | Medium | Low | Score |
|-------|----------|------|--------|-----|-------|
| Quality | 0 | 2 | 5 | 8 | 78/100 |
| Security | 1 | 1 | 3 | 2 | 65/100 |
| Performance | 2 | 3 | 1 | 4 | 62/100 |
| Architecture | 0 | 1 | 2 | 3 | 85/100 |

**Overall Score**: 72.5/100
```

---

## Options

### Execute Specific Steps

```markdown
"Run only lint" → execute `npm run lint` only
"Run only build" → execute `npm run build` only
"Run only tests" → execute `npm test` only
```

### Continue on Failure

```markdown
"Continue despite failures" → execute all steps and provide final report
```

---

## Related Skills

| Skill | Role | Connection Point |
|-------|------|------------------|
| `write-code` | Code implementation | Before quality analysis |
| `write-test` | Test writing | Before quality analysis |
| `git-workflow` | Commit/Push | After quality analysis |

---

## References

- [SEMO Quality Gate Principles](../../semo-core/principles/QUALITY_GATE.md)
- [Analysis Patterns](references/analysis-patterns.md) - Focus-specific analysis patterns
- [Severity Definitions](references/severity-definitions.md) - Definitions of severity levels
- [Score Calculation](references/score-calculation.md) - Logic for score calculation