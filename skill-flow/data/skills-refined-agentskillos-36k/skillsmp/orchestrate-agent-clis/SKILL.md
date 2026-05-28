---
name: orchestrate-agent-clis
description: >
  Execute and orchestrate multiple AI agent CLIs (Gemini, Codex, Cursor, Claude
  Code) for getting alternative opinions, comparing approaches, or leveraging
  different AI models' strengths. Use when the user explicitly mentions agent
  names like "ask gemini", "ask cursor", "ask codex", "use composer", "try
  grok", or when needing diverse perspectives on complex problems, alternative
  implementation approaches, or multi-agent collaboration.
---

# Orchestrate Agent CLIs

Execute different AI agent CLIs to get alternative perspectives, compare
approaches, or leverage specific model strengths.

## Available CLIs

### Gemini

```bash
gemini -p "<prompt>"
```

Has internet access. Good for research and current information.

### Codex

```bash
codex exec "<prompt>"
```

No internet access. Fast, focused on code generation.

### Claude Code

```bash
claude -p "<prompt>"
```

Full-featured Claude agent with tool access.

### Cursor Agent

```bash
cursor-agent --model=MODEL -p "<prompt>"
```

Available models:

- `composer-1` (preferred for multi-file edits, also fast)
- `gemini-3-pro` (better for code investigation, planning and web research)
- `gemini-3-flash` (faster, good for simple tasks)
- `grok` (creative solutions, unconventional approaches)
- `gpt-5.2-codex` (code-focused)

Note: If these models fail, you can get the list of available models by running:

```bash
cursor-agent models
```

## File References

Reference files using `@` prefix with relative paths:

```bash
codex exec "Review @src/components/Button.tsx"
gemini -p "Create tests for @src/utils/helpers.ts"
cursor-agent --model=composer-1 -p "Refactor @src/api/client.ts"
```

## Task Guidelines

### Read-Only Tasks

For questions, plans, reviews, or analysis, instruct agents not to make file
changes:

```bash
cursor-agent --model=gemini-3-pro -p "Analyze the architecture in @src/core/ - explain only, do not modify files"
```

### Comparison Workflows

Get multiple perspectives on the same problem:

```bash
# Get Gemini's opinion first
gemini -p "How would you implement feature X?"

# Then compare with Codex
codex exec "How would you implement feature X?"
```
