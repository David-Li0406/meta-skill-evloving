---
title: Customizable Linter
impact: MEDIUM
impactDescription: Flexible rule configuration
tags: lint, revive, customizable
---

## Customizable Linter

Use revive for flexible code checking.

**Installation:**

```bash
go install github.com/mgechev/revive@latest
```

**Running:**

```bash
revive ./...
```

**Configuration File (revive.toml):**

```toml
ignoreGeneratedHeader = true
severity = "warning"
confidence = 0.8

[rule.blank-imports]
[rule.context-as-argument]
[rule.context-keys-type]
[rule.dot-imports]
[rule.error-return]
[rule.error-strings]
[rule.error-naming]
[rule.exported]
  arguments = ["checkPrivateReceivers", "disableStutteringCheck"]
[rule.if-return]
[rule.increment-decrement]
[rule.var-naming]
[rule.var-declaration]
[rule.package-comments]
[rule.range]
[rule.receiver-naming]
[rule.time-naming]
[rule.unexported-return]
[rule.indent-error-flow]
[rule.errorf]
[rule.empty-block]
[rule.superfluous-else]
[rule.unused-parameter]
[rule.unreachable-code]
[rule.redefines-builtin-id]

# Function complexity limit
[rule.cognitive-complexity]
  arguments = [15]

# Function line limit
[rule.function-length]
  arguments = [50, 0]

# Parameter count limit
[rule.argument-limit]
  arguments = [5]

# Return value count limit
[rule.function-result-limit]
  arguments = [3]
```

**Common Rules:**

| Rule | Description |
|------|-------------|
| `blank-imports` | Forbid blank imports (except for side effects) |
| `context-as-argument` | context.Context must be the first parameter |
| `error-return` | error must be the last return value |
| `error-naming` | error variable names must start with err or Err |
| `exported` | Exported items must have comments |
| `var-naming` | Variable naming convention checking |
| `cognitive-complexity` | Cognitive complexity limit |
| `function-length` | Function length limit |

**Integration with golangci-lint:**

```yaml
# .golangci.yml
linters:
  enable:
    - revive

linters-settings:
  revive:
    rules:
      - name: blank-imports
      - name: context-as-argument
      - name: error-return
      - name: cognitive-complexity
        arguments: [15]
```
