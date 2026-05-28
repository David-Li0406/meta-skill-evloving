---
name: amp-tool-creator
description: Create custom toolbox tools for Amp using the toolbox protocol. Use when asked to create a tool, when asked to create a skill that requires a tool, or build toolbox executables.
---

# Amp Tool Creator

Create custom toolbox tools that extend Amp's capabilities using simple executable scripts.

## When to Use

- User asks to create a custom tool for Amp
- User wants to wrap a CLI command for controlled agent use
- User needs project-specific tooling (test runners, database queries, build scripts)
- A skill needs bundled executable tools in its `tools/` directory
- User says "create a tool", "make a tool", "add a command"

## Overview

Toolbox tools are executable files that communicate with Amp via stdin/stdout using a simple protocol. They can be written in any language—bash, zsh, JavaScript (bun), Python, Go, etc.

**Key characteristics:**

- Tools receive `TOOLBOX_ACTION=describe` to report their schema
- Tools receive `TOOLBOX_ACTION=execute` with parameters on stdin
- Tools write output to stdout, errors to stderr
- Exit code 0 = success, non-zero = error
- Registered with `tb__` prefix (e.g., `run_tests` → `tb__run_tests`)

## Tool Locations

**Global tools:** `~/.config/amp/tools/`
**Project tools:** `.agents/tools/` (in workspace root)
**Skill-bundled tools:** `skill-name/tools/`

The `AMP_TOOLBOX` environment variable controls search paths (colon-separated, like `PATH`).

## Protocol Specification

### Environment Variables for describe and execute modes

| Variable         | Value                       | Available During |
| ---------------- | --------------------------- | ---------------- |
| `TOOLBOX_ACTION` | `"describe"` or `"execute"` | Both             |
| `AGENT`          | `"amp"`                     | Both             |
| `AMP_THREAD_ID`  | Current thread ID           | Execute only     |

### Communication Formats

Tools can use **JSON format** or **text format**. Amp auto-detects based on the describe output.

#### Text Format (Recommended for Shell Scripts)

Simple and easy to parse. Best for tools that mostly call shell commands.

**Describe output:**

```
name: tool_name
description: What the tool does and when to use it.
param1: string description of param1
param2: string? optional parameter (note the ?)
param3: string (optional) another way to mark optional
```

**Execute input:** Key-value pairs on stdin

```
param1: value1
param2: value2
```

**Optional parameter markers:**

- Type suffix: `param: string?`
- In description: `param: string (optional) desc`
- Description starts with "optional": `param: string optional desc`

#### JSON Format (Recommended for Complex Tools)

Better for structured parameters, arrays, and nested objects.

**Describe output (compact args):**

```json
{
  "name": "tool_name",
  "description": "What the tool does",
  "args": {
    "workspace": ["string", "the workspace directory"],
    "patterns": ["string", "optional test patterns"]
  }
}
```

**Describe output (full inputSchema):**

```json
{
  "name": "tool_name",
  "description": "What the tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "files": {
        "type": "array",
        "items": { "type": "string" },
        "description": "List of files to process"
      }
    },
    "required": ["files"]
  }
}
```

**Execute input:** JSON object on stdin

## Tool Creation Workflow

### Step 1: Determine Requirements

- **Purpose:** What does the tool do?
- **Parameters:** What inputs does it need?
- **Language:** Bash for simple CLI wrappers, bun/node for complex logic
- **Location:** Global, project-local, or skill-bundled?

### Step 2: Scaffold the Tool

Use CLI or create manually:

```bash
# Create bash tool
amp tools make --bash tool_name

# Create zsh tool
amp tools make --zsh tool_name

# Create JavaScript/bun tool (default)
amp tools make tool_name
```

You may need to move the tool to the correct location after creation.

### Step 3: Implement the Tool

See templates below for language-specific patterns.

### Step 4: Make Executable

```bash
chmod +x path/to/tool_name
```

### Step 5: Verify

```bash
# Check schema
amp tools show tb__tool_name

# Test execution
amp tools use tb__tool_name --param value
```

## Writing Good Tool Descriptions

The description is critical—it tells the agent when to use your tool.

**Good descriptions:**

- "Run project tests. Use this tool instead of Bash for running tests in this workspace."
- "Query the development PostgreSQL database. Safer than raw psql commands."
- "Build and deploy to staging environment. Handles all necessary steps."

**Bad descriptions:**

- "Runs tests" (too vague)
- "A utility" (meaningless)
- "Do stuff with the database" (unprofessional)

**Include:**

- What the tool does
- When/why to use it over alternatives
- Any constraints or safety notes

## Error Handling

- Write errors to stderr
- Exit with non-zero code on failure
- Provide actionable error messages

```bash
if [[ -z "$required_param" ]]; then
  echo "Error: required_param is required" >&2
  echo "Usage: provide the path to the config file" >&2
  exit 1
fi
```

## Testing Tools

### Global/Project Tools

For tools in `~/.config/amp/tools/` or `.agents/tools/`:

```bash
# View tool schema
amp tools show tb__my_tool

# Run with parameters
amp tools use tb__my_tool --param1 value1 --param2 value2

# View only output (no metadata)
amp tools use --only output tb__my_tool --param1 value1

# List all tools
amp tools list
```

### Skill-Bundled Tools

Tools inside a skill's `tools/` directory aren't loaded until the skill is active. Test them manually:

```bash
# Test describe action
TOOLBOX_ACTION=describe ./skill-name/tools/my_tool

# Test execute action (text format)
echo "param1: value1" | TOOLBOX_ACTION=execute ./skill-name/tools/my_tool

# Test execute action (JSON format)
echo '{"param1": "value1"}' | TOOLBOX_ACTION=execute ./skill-name/tools/my_tool
```

## Troubleshooting

### Tool not appearing

- Verify file is executable: `chmod +x tool_name`
- Check location is in `AMP_TOOLBOX` path
- Restart Amp to rescan tools

### Parse errors

- Validate JSON syntax if using JSON format
- Check text format has `name:` and `description:` lines
- Ensure no trailing whitespace issues

### Execution errors

- Test manually: `TOOLBOX_ACTION=execute echo "param: value" | ./tool_name`
- Check stderr for error messages
- Verify all dependencies available

## References

@references/owners-manual.md
@references/appendix.md
