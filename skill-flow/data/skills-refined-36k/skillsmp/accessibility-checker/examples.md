# Accessibility Checker - Examples

## Structured Analysis Report

Here is the report template to generate after verifying a component:

```markdown
# Accessibility Report - [Component Name]

## ✅ Positive Points

[List detected good practices]

## ⚠️ Issues Detected

### Critical (P0) - Blocking

- [ ] Line X : [Problem description]
      Solution : [How to fix]

### Important (P1) - To fix

- [ ] Line Y : [Problem description]
      Solution : [How to fix]

## 📊 Overall Score

- Semantic elements : X/5
- ARIA attributes : X/5
- Focus/Keyboard : X/5
- a11y tests : X/5

**Total score : X/20**

## ✅ Verdict

[COMPLIANT / TO FIX / NON-COMPLIANT]
```

## Usage Example

Read a React component, verify each criterion defined in `.claude/rules/accessibility.md`, then generate a structured report using this template by replacing values with your findings.
