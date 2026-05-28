---
name: prompt
description: Manage the system prompt for the Vocal Bridge voice agent. Can show, edit, or set the prompt and greeting.
allowed-tools: Bash, Read, Write
---

Manage the voice agent's system prompt.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

## Commands

### Show current prompt

```bash
vb prompt show
```

### Set prompt from file

```bash
vb prompt set --file <path>
```

For greeting:

```bash
vb prompt set --file <path> --greeting
```

### Set prompt from stdin (pipe content)

```bash
echo "Your prompt here" | vb prompt set
```

For greeting:

```bash
echo "Hello! How can I help?" | vb prompt set --greeting
```

## Based on $ARGUMENTS

Determine user intent from $ARGUMENTS:
- "show" or empty → show current prompt with `vb prompt show`
- "set" with file path → set from file
- Contains prompt text → pipe to `vb prompt set`
- "greeting" modifier → operate on greeting instead of prompt

## Interactive Edit Flow

If user wants to edit:
1. Run `vb prompt show` to get current prompt
2. Let user provide new prompt text
3. Pipe new text to `vb prompt set`
