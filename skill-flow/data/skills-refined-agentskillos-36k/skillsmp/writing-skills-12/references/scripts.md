## Critical Rule

When writing scripts for skills, you MUST use the templates provided in this document. Do not write scripts from scratch. Copy the template exactly and fill in the specific logic.

## Script Types

Choose the script type that makes the task simpler:

- **Bash:** Use when chaining together external commands (git, grep, jq, etc.). Bash excels at piping commands and simple command orchestration.
- **TypeScript:** Use when you need actual logic or external libraries. TypeScript excels at complex validation, data transformation, and leveraging npm packages.

The best choice is the one that's simplest for the job.

## Universal Conventions

- **File extensions:** Bash scripts use `.sh` extension, TypeScript scripts use `.ts` extension
- **kebab-case names:** Use hyphens between words (e.g., `extract-pr-number.sh`)
- **Shebang required:** First line must specify interpreter
- **Executable permissions:** Scripts must be executable
- **Flag-based arguments:** Use the `--flagName` format. Only use position arguments if they're very
  simple or there's only one.
- **Full variable names:** Use `directory` not `dir`, `message` not `msg`, `timestamp` not `ts`
- **Exit codes:** 0 for success, 1 for errors
- **Help flag mandatory:** Every script must support `--help` with dedicated help function

## Bash Scripts

### Template

Use the template at `assets/bash-script-template.sh`. Copy it exactly and fill in your specific logic.

### Requirements

- `set -euo pipefail`: Required at the top of every script
- `print_help()` function: Mandatory dedicated function for help output
- `--help` flag: Must exist and be the first case in argument parsing
- Error prefix: All error messages must start with "Error: " and go to stderr (`>&2`)
- Help on error: Always print help to stderr when validation fails or unknown options provided
- Quote variables: Always quote variable expansions (`"$variable"`)
- Validate required flags: Check after parsing loop completes
- Unknown options: Must print error with "Error: Unknown option:" prefix

## TypeScript Scripts

### Template

Use the template at `assets/typescript-script-template.ts`. Copy it exactly and fill in your specific logic.

### Requirements

- `#!/usr/bin/env bun`: Required shebang
- `printHelp()` function: Mandatory dedicated function for help output
- `--help` flag: Must be handled after parsing arguments
- `parseArgs` from `util`: Standard library argument parsing
- Zod schemas: Validate all arguments with descriptive schemas
- `strict: true`: Reject unknown arguments
- `safeParse`: Never throw, always handle validation errors gracefully
- Help on error: Call printHelp() after showing validation errors
- `process.exit(0)`: Exit successfully when help is requested
- `process.exit(1)`: Exit with error code on validation failure

## Output Conventions

- **stdout:** Primary output only (data the caller needs)
- **stderr:** Errors, warnings, progress messages
- **Silent success:** If nothing to output, exit silently with code 0
- **Structured output:** When outputting file paths or identifiers, output just the value (no "Created: " prefix)
- **No logging:** Don't add log-style messages that explain what the script is doing
