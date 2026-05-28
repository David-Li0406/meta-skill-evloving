---
name: packmind-standard-creator
description: Use this skill when you want to create a new coding standard or add rules to an existing standard that captures team conventions, best practices, or coding guidelines for distribution to your team.
---

# Standard Creator

This skill provides a complete walkthrough for creating coding standards via the Packmind CLI.

## About Coding Standards

Coding standards are collections of rules that capture team conventions, best practices, and coding guidelines. They help maintain consistency across codebases and enable tools like CoPilot or Claude to follow your team's specific practices.

### What Standards Provide

1. **Consistent code style** - Rules that enforce naming conventions, formatting, and structure.
2. **Best practices** - Guidelines for error handling, testing, security, and performance.
3. **Domain knowledge** - Company-specific patterns, architectural decisions, and business logic.
4. **Code examples** - Positive/negative examples that demonstrate correct vs incorrect usage.

### Standard Structure

Every standard consists of:

```json
{
  "name": "Standard Name",
  "description": "What the standard covers and why",
  "scope": "Where/when the standard applies",
  "rules": [
    {
      "content": "Rule description starting with action verb",
      "examples": {
        "positive": "Valid code example",
        "negative": "Invalid code example",
        "language": "TYPESCRIPT"
      }
    }
  ]
}
```

## Prerequisites

Before creating a standard, verify that the required tools are available:

### Python 3

Check if Python 3 is installed:

```bash
python3 --version
```

If not available, install it:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3`
- **Windows**: Download from https://python.org or use `winget install Python.Python.3`

### Packmind CLI

Check if packmind-cli is installed:

```bash
packmind-cli --version
```

If not available, install it:

```bash
npm install -g @packmind/cli
```

Then login to Packmind:

```bash
packmind-cli login
```

## Standard Creation Process

To create a standard, follow this process in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Standard's Purpose

Skip this step only when the standard's scope and rules are already clearly defined. It remains valuable even when working with existing standards.