---
name: semgrep-rule-creator
description: Use this skill when you need to create custom Semgrep rules for detecting bug patterns and security vulnerabilities in your codebase.
---

# Semgrep Rule Creator

Create production-quality Semgrep rules with proper testing and validation.

## When to Use

**Ideal scenarios:**
- Creating custom detection rules for specific bug patterns
- Building security vulnerability detectors for your codebase
- Writing taint-mode rules for data flow vulnerabilities
- Developing rules to enforce coding standards

## When NOT to Use

Do NOT use this skill for:
- Running existing Semgrep rulesets (use the `semgrep` skill instead)
- General static analysis without custom rules (use `static-analysis` plugin)
- One-off scans where existing rules suffice
- Non-Semgrep pattern matching needs

## Rationalizations to Reject

When creating Semgrep rules, reject these common shortcuts:

- **"The pattern looks complete"** → Still run `semgrep --test --config rule.yaml test-file` to verify. Untested rules have hidden false positives/negatives.
- **"It matches the vulnerable case"** → Matching vulnerabilities is half the job. Verify safe cases don't match (false positives break trust).
- **"Taint mode is overkill for this"** → If data flows from user input to a dangerous sink, taint mode gives better precision than pattern matching.
- **"One test case is enough"** → Include edge cases: different coding styles, sanitized inputs, safe alternatives, and boundary conditions.
- **"I'll optimize the patterns first"** → Write correct patterns first, optimize after all tests pass. Premature optimization causes regressions.
- **"The AST dump is too complex"** → The AST reveals exactly how Semgrep sees code. Skipping it leads to patterns that miss syntactic variations.

## Anti-Patterns

**Too broad** - matches everything, useless for detection:
```yaml
# BAD: Matches any function call
pattern: $FUNC(...)

# GOOD: Specific dangerous function
pattern: eval(...)
```

**Missing safe cases in tests** - leads to undetected false positives:
```python
# BAD: Only tests vulnerable case
# ruleid: my-rule
dangerous(user_input)

# GOOD: Include safe cases to verify no false positives
# ruleid: my-rule
dangerous(user_input)

# ok: my-rule
dangerous(sanitize(user_input))

# ok: my-rule
dang
```