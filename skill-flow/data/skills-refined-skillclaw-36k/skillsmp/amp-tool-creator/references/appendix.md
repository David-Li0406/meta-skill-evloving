## Toolbox Protocol Reference

Toolboxes let you create custom tools using any programming language. Tools are executable files that communicate with Amp via stdin/stdout using a simple protocol. See [owners-manual.md](owners-manual.md) for an introduction.

### Overview

A toolbox is a directory containing executable files that become tools available to Amp. Each executable file in the directory represents a single tool.

Tools from toolboxes are registered with a `tb__` prefix (e.g., `run_tests` becomes `tb__run_tests`), and must implement the toolbox protocol (described below).

As long as the executables adhere to the protocol, they can be written in any language.

### Tool Discovery

Amp discovers tools by scanning directories specified in the `AMP_TOOLBOX` environment variable at startup, which works like the `PATH` variable: multiple directories separated by colons.

By default, if `AMP_TOOLBOX` is not set, Amp uses `~/.config/amp/tools` as the default toolbox directory.

When `AMP_TOOLBOX` is set to an empty string, or is not present in the environment, no toolbox directories are scanned.

Otherwise Amp scans the directories listed in `AMP_TOOLBOX` left-to-right, giving precedence to earlier directories for tools with conflicting names:

```bash
# Example: a run_tests tool in $PWD/.agents/tools will be used even if
# a tol with the same name exists in $HOME/.config/amp/tools
export AMP_TOOLBOX="$PWD/.agents/tools:$HOME/.config/amp/tools"
```

### Protocol Specification

Tools communicate with Amp through two actions: **describe** and **execute**. The action is determined by the `TOOLBOX_ACTION` environment variable.

The `describe` action is used to tell Amp about when and how to use the tool.

Once Amp decides to execute the tool, the executable is invoked again, but with `TOOLBOX_ACTION` set to `execute`.

**Communication:**

- Tools receive tool parameters via **stdin**, either as JSON or line-based key-value pairs.
- Tools write a message to the model to **stdout**.
- Exit code **0** indicates success, non-zero indicates error
- Stderr is used for error messages and diagnostics

**Environment variables passed to tools:**

| Variable          | Value                       | Available During |
| ----------------- | --------------------------- | ---------------- |
| `TOOLBOX_ACTION`  | `"describe"` or `"execute"` | Both actions     |
| `AGENT`           | `"amp"`                     | Both actions     |
| `CLAUDECODE`      | `"1"`                       | Both actions     |
| `AMP_THREAD_ID`   | Current thread ID           | Execute only     |
| `AGENT_THREAD_ID` | Current thread ID           | Execute only     |
| `PATH`            | Inherited from environment  | Both actions     |

### Communication Formats

Tools can use either **JSON format** or **text format** for communicating the tool schema and input parameters. Amp auto-detects the format during the **describe** action:

1. First attempts to parse output as JSON
2. If JSON parsing fails, falls back to text format
3. The detected format is used for both describe and execute actions

Amp remembers the format that the tool advertised and will provide tool input parameters in the same format.

When `TOOLBOX_ACTION` is **execute** Amp takes any output from the tool and passes it directly to the model.

#### JSON Format

The JSON format is easy to work with in most programming languages and the recommended way to write toolbox tools when most of the tool logic is expressed in an existing programming language library.

For tools that mostly call out to shell commands, the text format is recommended.

**Describe Action:**

Output a JSON object with `name`, `description`, and either `args` (compact) or `inputSchema` (full):

_Compact args format for simple tools:_

```json
{
  "name": "run_tests",
  "description": "Run the tests in the project using this tool instead of Bash",
  "args": {
    "workspace": ["string", "optional name of the workspace directory"],
    "test": ["string", "optional test name pattern to match"]
  }
}
```

For more structured parameters with deeply nested objects, use the full MCP `inputSchema`:

_Full inputSchema format (JSON Schema draft 2020-12):_

```json
{
  "name": "run_tests",
  "description": "Run the tests in the project using this tool instead of Bash",
  "inputSchema": {
    "type": "object",
    "properties": {
      "workspace": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "list of names of the workspace directories"
      },
      "test": {
        "type": "string",
        "description": "optional test name pattern to match"
      }
    },
    "required": ["workspace"]
  }
}
```

**Execute Action:**

- **Input:** JSON object with tool arguments via stdin
- **Output:** Free-form text written to stdout
- **Exit code:** 0 for success, non-zero for error

#### Text Format

The text format is convenient for simple tool definitions that mostly need a handful of string parameters.

It is easy to emit and easy to parse in any programming language.

**Describe Action**:

Output a line-based tool description:

```
name: run_tests
description: Run the tests in the project using this tool instead of Bash.
workspace: string optional name of the workspace directory
test: string optional test name pattern
```

Multiple description lines are concatenated with newlines.

Parameter lines without a type prefix default to string type.

Empty lines are ignored.

**Optional Parameters:**

Parameters can be marked as optional in three ways:

1. **Type suffix with `?`**: `param: string? description`
2. **`(optional)` in description**: `param: string (optional) description`
3. **Description starts with `optional`**: `param: string optional description` or `param: optional description`

All three methods are case-insensitive. Parameters not marked as optional are required by default.

**Execute Action:**

- **Input:** Key-value pairs separated by newlines (e.g., `param1=value1\nparam2=value2\n`)
- **Output:** Any output written to stdout

### CLI Commands

The `amp tools` command allows you to work with tools directly from the command line.

To get a list of all tools known to Amp, run `amp tools list`:

```
Bash                              built-in  Executes the given shell command in the user's default shell
# ...
mcp__context7__get-library-docs   local-mcp Fetches up-to-date documentation for a library
mcp__context7__resolve-library-id local-mcp Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries
tb__run_tests                     toolbox   Run tests using this tool instead of Bash
```

Tools provided by MCP servers have an `mcp__` prefix, tools coming from toolboxes get `tb__` as a prefix.

To create a new toolbox tool, use the `amp tools make` command:

```
$ amp tools make --bash run_tests
Tool created at: /Users/dhamidi/.config/amp/tools/run_tests

Inspect with: amp tools show tb__run_tests

Execute with: amp tools use tb__run_tests
```

By default a JavaScript tool using bun is created, the `--bash` and `--zsh` parameters scaffold the tool using the respective shell. This is useful when your tool is mostly just calling out other processes.

Using `amp tools show` you can see the schema of the generated tool:

```
amp tools show tb__run_tests
# tb__run_tests (toolbox: /Users/dhamidi/.config/amp/tools/run_tests)

Use this tool to get the current time.
Supported actions are:
date to retrieve the current time

# Schema

- action (string): the action to take
```

To invoke the tool as is, we’ll use `amp tools use`:

```
$ amp tools use tb__run_tests --action date
{
  "output": "Got action: date\nTue Oct 14 15:03:46 EEST 2025\n",
  "exitCode": 0
}
```

Amp collects the output of the toolbox executable and reports the collected output together with the exit status to the model.

After editing the scaffold to actually run Go tests for this example, it now looks like this:

```bash
#!/usr/bin/env bash

main() {
  case "${TOOLBOX_ACTION:-${1:-describe}}" in
  describe) print_tool_definition ;;
  execute) read_args_and_run ;;
  *)
    printf "Unknown action: %s\n" "$action" >&2
    exit 1
    ;;
  esac
}

print_tool_definition() {
  cat <<-'EOF'
        name: run_tests
        description: Run Go tests using this tool instead of Bash
        description: The pattern parameter limits the tests to a given pattern.

        pattern: string optional Only run tests matching this pattern
    EOF
}

read_args_and_run() {
  local pattern
  local input=$(</dev/stdin)
  while IFS=": " read name value; do
    if [ -n "$name" ]; then
      local $name="$value"
    fi
  done <<<"$input"

  go test ./... ${pattern:+-run "$pattern"}
}

main "$@"
```

We can verify that it works using `amp toosl use` again:

```
$ amp tools use --only output tb__run_tests
ok      github.com/dhamidi/proompt/cmd/proompt  (cached)
ok      github.com/dhamidi/proompt/pkg/config   (cached)
ok      github.com/dhamidi/proompt/pkg/copier   (cached)
ok      github.com/dhamidi/proompt/pkg/editor   (cached)
ok      github.com/dhamidi/proompt/pkg/filesystem       (cached)
ok      github.com/dhamidi/proompt/pkg/picker   (cached)
ok      github.com/dhamidi/proompt/pkg/prompt   (cached)
```
