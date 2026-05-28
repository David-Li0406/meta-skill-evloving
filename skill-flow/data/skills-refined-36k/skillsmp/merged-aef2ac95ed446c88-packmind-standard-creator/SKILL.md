---
name: packmind-standard-creator
description: Use this skill when you want to create or update coding standards via the Packmind CLI, capturing team conventions and best practices for distribution.
---

# Standard Creator

This skill provides a complete walkthrough for creating coding standards via the Packmind CLI.

## About Coding Standards

Coding standards are collections of rules that capture team conventions, best practices, and coding guidelines. They help maintain consistency across codebases and enable AI coding agents to follow your team's specific practices.

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

To create an effective standard, clearly understand:

1. **What problem does this standard solve?**
2. **Who will benefit from this standard?**
3. **Where does this standard apply?**

Conclude this step when there is a clear sense of the standard's purpose and scope.

### Step 2: Gathering and Writing Rules

Transform the understanding from Step 1 into concrete rules.

#### Rule Writing Guidelines

Each rule should:

1. **Start with an action verb** - Use imperative form (e.g., "Use", "Avoid", "Prefer", "Include").
2. **Be specific and actionable** - Avoid vague guidance.
3. **Focus on one concept** - One rule per convention.

**Good rules:**
- "Use const instead of let for variables that are never reassigned."
- "Prefix interface names with I (e.g., IUserService)."

**Bad rules:**
- "Write good code" (too vague).

#### Adding Examples (Recommended)

For each rule, consider adding:

- **positive**: Code that correctly follows the rule.
- **negative**: Code that violates the rule.
- **language**: The programming language for syntax highlighting.

### Step 3: Creating the Playbook File

When creating a new standard from scratch, use the `init_playbook.py` script to generate a template playbook file:

```bash
python3 scripts/init_playbook.py <standard-name> --path <output-directory>
```

### Step 4: Creating the Standard via CLI

Run the packmind-cli command to create the standard:

```bash
packmind-cli standard create <path-to-playbook.json>
```

### Step 5: Verifying the Standard

After creation, verify the standard was created correctly by checking in the Packmind UI and ensuring all rules appear with correct content.

### Step 6: Iterate and Improve

Standards benefit from iteration. Consider adding more rules, examples, and refining rule wording based on how AI agents interpret them.

## Quick Reference

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Standard name |
| description | Yes | What and why |
| scope | Yes | Where it applies |
| rules | Yes | At least one rule |
| rules[].content | Yes | Rule text (verb-first) |
| rules[].examples | No | Code examples |
| examples.positive | If examples | Valid code |
| examples.negative | If examples | Invalid code |
| examples.language | If examples | Language ID |