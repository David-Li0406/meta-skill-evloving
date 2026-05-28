---
title: "[command-name] - [Brief Description]"
description: "[What this command does in 1-2 sentences]"
type: reference
category: cli-reference
tags:
  - cli
  - [tag2]
  - [tag3]
status: published
version: "1.0.0"
created: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
---


[Brief description of what this command does and when to use it.]

## Synopsis

```bash
[command-name] [OPTIONS] [ARGUMENTS]
```

## Description

The `[command-name]` command [detailed description of functionality].

**Common use cases**:

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Options

### Global Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--help` | `-h` | Show help message | - |
| `--version` | `-v` | Show version | - |
| `--verbose` | `-V` | Enable verbose output | false |

### Command-Specific Options

| Option | Short | Type | Description | Default | Required |
|--------|-------|------|-------------|---------|----------|
| `--option1` | `-o` | string | [Description] | [value] | No |
| `--option2` | `-p` | integer | [Description] | [value] | Yes |
| `--flag` | `-f` | boolean | [Description] | false | No |

## Arguments

| Argument | Type | Description | Required |
|----------|------|-------------|----------|
| `[arg1]` | string | [Description] | Yes |
| `[arg2]` | path | [Description] | No |

## Examples

### Example 1: [Common Use Case]

[Brief explanation of what this example does.]

```bash
[command-name] [options] [arguments]
```

**Output**:

```
[expected-output]
```

### Example 2: [Another Common Use Case]

[Brief explanation of what this example does.]

```bash
[command-name] [different-options] [arguments]
```

**Output**:

```
[expected-output]
```

### Example 3: [Advanced Use Case]

[Brief explanation of what this example does.]

```bash
[command-name] \
  --option1 value1 \
  --option2 value2 \
  argument1
```

**Output**:

```
[expected-output]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid argument |
| 3 | [Specific error] |
| 127 | Command not found |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `[VAR_NAME]` | [Description] | [value] |
| `[VAR_NAME2]` | [Description] | [value] |

**Example**:

```bash
export [VAR_NAME]=value
[command-name] [arguments]
```

## Configuration Files

The command reads configuration from:

1. `/etc/[app]/config.conf` - System-wide configuration
2. `~/.config/[app]/config.conf` - User configuration
3. `./.[app]rc` - Project-specific configuration

**Priority**: Project > User > System

**Example configuration**:

```ini
[section]
option1 = value1
option2 = value2
```

## Common Errors

### Error: "[Error Message 1]"

**Cause**: [Why this error occurs]

**Solution**:

```bash
[command-to-fix]
```

### Error: "[Error Message 2]"

**Cause**: [Why this error occurs]

**Solution**:

```bash
[command-to-fix]
```

## Related Commands

- [`[related-command1]`](/docs/cli/[command1]) - [Brief description]
- [`[related-command2]`](/docs/cli/[command2]) - [Brief description]
- [`[related-command3]`](/docs/cli/[command3]) - [Brief description]

## See Also

- [[Configuration Guide]](/docs/guides/configuration) - How to configure the CLI
- [[Getting Started]](/docs/getting-started) - Quick start guide
- [[API Reference]](/docs/api) - Programmatic API
