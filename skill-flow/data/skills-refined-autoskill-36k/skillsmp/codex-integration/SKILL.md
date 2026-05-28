---
name: codex-integration
description: This skill provides guidance on using OpenAI's Codex CLI for detail-oriented code analysis. Use when the user explicitly invokes "/codex", asks to "use codex", "run codex", "have codex review", or when Claude determines that Codex's sharp-eyed analysis would complement its work on code review, bug hunting, or planning tasks.
allowed-tools: Bash
---

# Codex Integration

OpenAI's Codex CLI is a complementary tool for detail-oriented code analysis. Codex excels at thorough, meticulous review work - think of it as a "sharp-eyed second opinion" for code.

## When to Use Codex

**Ideal use cases:**
- Deep code review for security vulnerabilities or correctness issues
- Thorough bug hunting in complex code paths
- Detailed implementation planning with attention to edge cases
- Getting a second perspective on critical code
- Exploratory analysis requiring meticulous attention

**Not ideal for:**
- Simple, straightforward tasks Claude handles well alone
- Interactive debugging sessions (Codex exec is non-interactive)
- Tasks where speed matters more than depth
- Trivial code changes or obvious fixes

## Invocation Methods

### Method 1: Explicit /codex Command

Users invoke directly with optional flags:

```
/codex review the authentication middleware for security issues
/codex --model gpt-5.2 analyze this algorithm
/codex --sandbox workspace-write generate tests for this module
```

**Available flags:**
| Flag | Values | Default |
|------|--------|---------|
| `--model` | any model name | gpt-5.2-codex |
| `--sandbox` | read-only, workspace-write, danger-full-access | read-only |

### Method 2: Spawning codex-agent

When Claude determines Codex would add value, spawn the `codex-agent` subagent:

```
"Let me have Codex take a detailed look at this code for potential bugs..."
[Spawn codex-agent with task description]
[Synthesize Codex's findings with own analysis]
```

The agent always uses safe defaults (gpt-5.2-codex, read-only sandbox).

## CLI Reference

Core command pattern for non-interactive execution (use inline prompt, not piped stdin):

```bash
codex exec \
  --model gpt-5.2-codex \
  --sandbox read-only \
  "<prompt>" \
  2>&1
```

**Key flags:**
- `--model, -m` - Model to use (gpt-5.2-codex recommended for code tasks)
- `--sandbox, -s` - Execution permissions (read-only safest)
- `2>&1` - Capture all output

**Note:** Interactive slash commands like `/review` only work in Codex's interactive mode, not via `codex exec`.

## Error Handling

### Codex Not Installed

If `codex` command not found, show:

```
Codex CLI is not installed.

To install:
  brew install codex

Then authenticate:
  codex login

For more info: https://developers.openai.com/codex/cli
```

### Common Issues

- **API key issues**: User needs to run `codex login` to authenticate
- **Timeout**: Complex tasks may take time. Be patient or try a simpler task description.
- **Sandbox errors**: If Codex needs to write files, user must specify `--sandbox workspace-write`

## Best Practices

1. **Start with defaults** - gpt-5.2-codex works well for most tasks
2. **Keep read-only sandbox** - Unless task explicitly requires file modifications
3. **Be specific in prompts** - Tell Codex exactly what to look for
4. **Synthesize results** - When using codex-agent, combine Codex's findings with Claude's analysis

## Prompting Best Practices

GPT-5.2-codex responds best to explicit, scoped prompts with concrete constraints.

### Core Principles

1. **Scope discipline** - Be explicit about boundaries
   - DO: "Review ONLY the auth flow. Do NOT suggest unrelated improvements."
   - DON'T: "Review this code" (too open-ended)

2. **Bias toward action** - Request concrete output
   - DO: "List specific bugs found with file:line references"
   - DON'T: "Tell me what you think about this code"

3. **No preambles** - Skip status updates
   - Add to prompts: "Skip preambles. Lead with findings."

4. **Structured output** - Request specific formats
   - "Format: `file.ts:line` - issue description"

### Task-Specific Prompt Templates

#### Security Review
```
Review <file/module> for security vulnerabilities.
Focus ONLY on: auth, injection, data exposure, access control.
Do NOT suggest style changes or refactoring.
Format each finding as: `file:line` - severity - issue
Skip preambles.
```

#### Bug Hunting
```
Find bugs in <file/module>.
Look for: edge cases, off-by-one, null handling, race conditions.
ONLY report actual bugs, not style issues.
Format: `file:line` - bug description - suggested fix
Skip preambles. Lead with findings.
```

#### Implementation Planning
```
Create implementation plan for: <feature>.
Constraints: <existing patterns to follow>.
Output structure:
1. Overview
2. Files to modify (with line ranges)
3. Implementation steps
4. Edge cases to handle
Do NOT include code samples unless critical. Skip preambles.
```

#### Code Review
```
Review <file> for correctness and reliability.
Focus ONLY on: logic errors, missing error handling, incorrect assumptions.
Ignore: style, naming, formatting.
Format: `file:line` - issue - recommendation
Skip preambles.
```
