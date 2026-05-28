---
name: promote-command
description: Promote a captured command to the baseline permissions
allowed-tools: Read, Edit, Bash
argument-hint: <command-pattern>
---

# Promote Command to Baseline

Add a captured command pattern to the baseline settings.json permissions.

## Instructions

1. Parse the command pattern from the argument
2. Validate it's a safe pattern to add (check against deny list patterns)
3. Read the current `.claude/settings.json`
4. Add the pattern to the `permissions.allow` array if not already present
5. Write the updated settings back
6. Confirm the addition

## Pattern Format

Commands should be in the format: `Bash(command:*)`

Examples:
- `Bash(pnpm:*)` - Allow all pnpm commands
- `Bash(cargo test:*)` - Allow cargo test with any arguments
- `Bash(kubectl get pods:*)` - Allow getting pods

## Safety Checks

Before promoting, verify the pattern:
- Does not match any deny patterns
- Is not overly broad (avoid patterns like `Bash(*:*)`)
- Follows the principle of least privilege

## Example

User: `/promote-command pnpm`

Result: Adds `"Bash(pnpm:*)"` to settings.json allow list
