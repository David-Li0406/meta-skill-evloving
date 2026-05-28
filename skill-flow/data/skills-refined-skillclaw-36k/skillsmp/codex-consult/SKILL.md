---
name: codex-consult
description: This skill should be used when the user asks to "consult Codex", "ask Codex for advice", "get implementation suggestions from Codex", "codexに相談", "codexにきいて", "実装方針を相談", "アーキテクチャをcodexに聞く", or needs deeper analysis using OpenAI's Codex model for complex implementation decisions, architecture design, or code review that benefits from extended reasoning.
version: 1.0.0
---

# Codex Consult

## Overview

This skill enables consultation with OpenAI's Codex CLI for deeper implementation analysis. Codex uses more powerful reasoning models (gpt-5.2-codex) that can provide thorough architectural guidance and implementation plans.

**When to use:**
- Complex architectural decisions requiring deep analysis
- Implementation planning for multi-file changes
- Code review needing extended reasoning
- Design pattern recommendations
- Refactoring strategy development

## Execution Modes

### Plan Mode (Default)
Provides analysis and implementation planning without code changes.

Output includes:
1. Summary of the approach
2. Implementation strategy
3. Verification steps

### Patch Mode
Provides analysis with concrete code change suggestions in unified diff format.

Output includes:
1. Summary of proposed changes
2. Unified diff patches
3. Verification steps

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| Task description | Required. What to analyze or plan | - |
| `--model=<model>` | Model to use | gpt-5.2-codex |
| `--mode=plan\|patch` | Execution mode | plan |
| `--scope=<path>` | Target directory | current repo root |
| `--no-web` | Disable web search | web enabled by default |

## Usage Instructions

### Basic Consultation (Plan Mode)

To consult Codex for implementation planning:

1. Execute the wrapper script with task description:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/scripts/codex-exec.sh "Implement user authentication with JWT"
   ```

2. Read the output from `/tmp/codex-consult.last.md`

3. If output is empty or error occurs, check `/tmp/codex-consult.run.log`

### Patch Mode Consultation

To get concrete code change suggestions:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/codex-exec.sh --mode=patch "Refactor the database connection to use connection pooling"
```

### Custom Model

To use a different model:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/codex-exec.sh --model=o4-mini "Design the caching layer"
```

### Scoped Analysis

To analyze a specific directory:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/codex-exec.sh --scope=/path/to/src "Review error handling patterns"
```

### Disable Web Search

To run without web search:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/codex-exec.sh --no-web "Analyze this legacy code"
```

## Output Interpretation

### Summary Section
- What changes are proposed
- Assumptions and preconditions
- Impact analysis

### Changes Section (Patch Mode)
- Unified diff format
- File-by-file breakdown
- Explanation of each change

### Verification Section
- Test commands to run
- Manual verification steps
- Edge cases to check

## Best Practices

1. **Be specific**: Provide clear task descriptions with context
2. **Scope appropriately**: Use `--scope` to limit analysis to relevant code
3. **Start with plan mode**: Use plan mode first, then patch mode if needed
4. **Verify suggestions**: Always review Codex output before applying changes

## Error Handling

If Codex execution fails:
1. Check `/tmp/codex-consult.run.log` for error details
2. Verify Codex CLI is authenticated (`codex login`)
3. Check network connectivity
4. Try with a different model if quota exceeded

## Additional Resources

### Reference Files
- **`references/codex-cli-reference.md`** - Codex CLI commands and options
- **`references/output-format.md`** - Output format specification

### Examples
- **`examples/sample-consultation.md`** - Sample consultation outputs
