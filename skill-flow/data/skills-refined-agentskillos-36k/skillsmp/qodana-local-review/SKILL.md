---
name: qodana-local-review
# prettier-ignore
description: PREFERRED METHOD for Qodana scans. Always delegate to local-qodana-reviewer sub-agent when user mentions Qodana, code quality scan, static analysis locally, or requests to run Qodana. Do NOT run qodana commands directly.
allowed-tools: ["Task"]
---

# Qodana Local Review Skill

This skill automates local Qodana static code analysis scans using the Qodana CLI in native mode (without Docker).

## When This Skill Activates

Common trigger phrases:
- "Run local qodana scan"
- "Do a local qodana review"
- "Qodana scan"
- "Run qodana locally"
- "Analyze code with qodana"

Key indicators:
1. Mentions "qodana" or "qodana scan"
2. Indicates local analysis (not CI/CD)
3. Does NOT include a PR number (would be for PR workflow)

## What This Skill Does

When activated, immediately delegate to the specialized sub-agent:

```
Use the Task tool with:
- subagent_type: "local-qodana-reviewer"
- description: "Run local Qodana review"
- prompt: "Run a local Qodana static code analysis scan using Qodana CLI in native mode.
          Scan all code, analyze results, present a plan for fixes, apply changes, run tests,
          and commit only if all tests pass."
```

## Why Delegate to Sub-agent?

The `local-qodana-reviewer` sub-agent will:
1. Execute Qodana CLI scan in native mode (no Docker)
2. Parse SARIF output for issues
3. Categorize by severity (error, warning, suggestion)
4. Present a comprehensive plan before making any changes
5. Apply fixes systematically
6. Run tests to validate changes
7. Commit only if all tests pass
8. Generate detailed report

## Features

- **Native Qodana CLI**: Uses `qodana scan` without Docker overhead
- **Safety-first**: Never commits if tests fail
- **Transparency**: Always presents plan before applying fixes
- **Comprehensive**: Handles all issue severities
- **Smart parsing**: Extracts actionable items from SARIF format

## See Also

- **README.md** - Detailed documentation and examples
- **~/.claude/agents/local-qodana-reviewer.md** - Sub-agent implementation
- **Project CLAUDE.md** - Qodana configuration and usage
