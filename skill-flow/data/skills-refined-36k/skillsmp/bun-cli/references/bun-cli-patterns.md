# Bun CLI Patterns Reference

Unified CLI patterns and best practices for all plugins with command-line interfaces. This reference provides comprehensive guidance, patterns, examples, and case studies.

---

## Table of Contents

### Core Patterns
- [File Structure](#file-structure)
- [Entry Point (cli.ts)](#entry-point-clist)
- [Argument Utilities](#argument-utilities-utilsargsts)
- [Output Formatting](#output-formatting-utilsoutputts)
- [Error Handling](#error-handling)
- [Configuration & Environment](#configuration--environment)
- [Testing CLI](#testing-cli)
- [Bun-Specific Patterns](#bun-specific-patterns)

### Advanced Topics
- [Command Dispatch](#command-dispatch-pattern)
- [Examples from Codebase](#examples-from-codebase)
- [Checklist for New CLIs](#checklist-for-new-cli-tools)
- [Anti-Patterns](#anti-patterns-dont-do-these)
- [Migration Guide](#migration-guide-for-existing-clis)
- [Performance Notes](#performance-notes)

### Reference Implementation
- [Para Obsidian CLI Review](#para-obsidian-cli---reference-implementation-1010)
- [Resources](#resources)

---

## File Structure

```
plugin/
├── src/
│   ├── cli.ts                    # Main CLI entry point
│   ├── utils/
│   │   ├── args.ts              # Argument parsing
│   │   └── output.ts            # Output formatting
│   └── commands/                # Optional: separate command files
│       ├── config.ts
│       └── search.ts
└── bin/                         # Optional: wrapper scripts
    └── plugin-name              # Shebang wrapper
```

---

## Entry Point (`cli.ts`)

### Shebang & Imports

```typescript
#!/usr/bin/env bun

/**
 * Plugin Name CLI
 *
 * Command-line interface for [description].
 * Output formats: markdown (default) for humans, JSON for machines.
 */

import { parseOutputFormat, type OutputFormat } from "@sidequest/core/formatters";
```

**Rules:**
- ✅ Always include shebang: `#!/usr/bin/env bun`
- ✅ Include JSDoc comment explaining purpose
- ✅ Import `OutputFormat` and `parseOutputFormat` from core/formatters
- ✅ Use absolute imports for @sidequest modules (workspace protocol)

### Structured Argument Parsing

```typescript
interface ParsedArgs {
  command: string;
  subcommand?: string;
  positional: string[];
  flags: Record<string, string | boolean>;
}

function parseArgs(argv: string[]): ParsedArgs {
  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg) continue;

    if (arg.startsWith("--")) {
      const [keyRaw, value] = arg.split("=");
      const key = keyRaw?.slice(2);
      if (!key) continue;

      const next = argv[i + 1];
      if (value !== undefined) {
        // --key=value
        flags[key] = value;
      } else if (next && !next.startsWith("--")) {
        // --key value
        flags[key] = next;
        i++;
      } else {
        // --flag (boolean)
        flags[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }

  const [command, subcommand, ...rest] = positional;
  return { command: command ?? "", subcommand, positional: rest, flags };
}
```

**Rules:**
- ✅ Support three flag formats: `--key=value`, `--key value`, `--flag`
- ✅ Separate positional args from flags
- ✅ Return structured object with command/subcommand/positional/flags
- ✅ Handle edge cases (missing args, trailing flags)

### Usage Output

```typescript
function printUsage(): void {
  const lines = [
    color("cyan", "Plugin Name CLI"),
    "",
    "Usage:",
    "  bun run src/cli.ts command [subcommand] [args] [--flags]",
    "  bun run src/cli.ts config [--format md|json]",
    "  bun run src/cli.ts search <query> [--dir path] [--format md|json]",
    "",
    "Options:",
    "  --format md|json   Output format (default: md)",
    "  --dry-run          Preview changes without writing",
    "  --help             Show this help message",
    "",
    "Examples:",
    '  bun run src/cli.ts config --format json',
    '  bun run src/cli.ts search "pattern" --dir src',
  ];
  console.log(lines.map((line) => emphasize("cyan", line)).join("\n"));
}
```

**Rules:**
- ✅ Use cyan color for headers (from @sidequest/core/formatters)
- ✅ Structure: Usage → Options → Examples
- ✅ Keep under 30 lines (fit in terminal)
- ✅ Show command variations clearly
- ✅ Include real examples users can copy-paste

### Main Function

```typescript
async function main() {
  try {
    // Skip first two args: 'bun' and 'src/cli.ts'
    const args = process.argv.slice(2);
    const { command, subcommand, positional, flags } = parseArgs(args);

    const outputFormat = parseOutputFormat(flags.format) ?? "md";

    // Handle help
    if (!command || flags.help) {
      printUsage();
      process.exit(0);
    }

    // Dispatch to command handlers
    switch (command) {
      case "config":
        await handleConfig(outputFormat);
        break;
      case "search":
        if (!positional[0]) {
          console.error("Error: search requires a query");
          process.exit(1);
        }
        await handleSearch(positional[0], flags, outputFormat);
        break;
      default:
        console.error(`Unknown command: ${command}`);
        printUsage();
        process.exit(1);
    }
  } catch (error) {
    console.error("Error:", error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
```

**Rules:**
- ✅ Always wrap in try/catch
- ✅ Skip first two argv (bun + script path)
- ✅ Check for help flag first
- ✅ Validate required positional args
- ✅ Use switch for command dispatch
- ✅ Exit with code 1 on error, 0 on success
- ✅ Use console.error for errors

---

## Argument Utilities (`@sidequest/core/cli`)

All CLI argument parsing utilities are now centralized in the core package for reuse across all marketplace plugins:

```typescript
// Import from core (available to all CLI plugins)
import {
  parseArgs,
  parseKeyValuePairs,
  coerceValue,
} from "@sidequest/core/cli";

/**
 * Parse key=value pairs into object
 *
 * Example: parseKeyValuePairs(["title=My Project", "status=active"])
 * Returns: { title: "My Project", status: "active" }
 */
export function parseKeyValuePairs(
  inputs: ReadonlyArray<string>,
): Record<string, string>

/**
 * Parse command-line arguments into structured format
 *
 * Handles three flag formats:
 * - `--key value` (spaced)
 * - `--key=value` (equals)
 * - `--key` (boolean)
 *
 * Example: parseArgs(["config", "--format", "json"])
 * Returns: { command: "config", positional: [], flags: { format: "json" } }
 */
export function parseArgs(argv: string[]): {
  command: string;
  subcommand?: string;
  positional: string[];
  flags: Record<string, string | boolean>;
}

/**
 * Coerce string value to appropriate type for JSON output
 *
 * Converts:
 * - "true"/"false" → boolean
 * - "-?\\d+(\\.\\d+)?" → number
 * - "[...]"/"{...}" → parsed JSON
 * - "a,b,c" → array
 * - Otherwise → string
 *
 * Example: coerceValue("123") → 123
 */
export function coerceValue(raw: string): unknown
```

**Rules:**
- ✅ Import from @sidequest/core/cli (not local utils/)
- ✅ Available to all CLI plugins in marketplace
- ✅ Handles edge cases (empty, malformed)
- ✅ Type coercion for JSON output
- ✅ Fully documented with JSDoc and examples
- ✅ Covered by 29+ comprehensive tests

---

## Output Formatting (`utils/output.ts`)

**Use core/formatters:**

```typescript
import {
  color,
  emphasize,
  parseOutputFormat,
  type OutputFormat,
} from "@sidequest/core/formatters";

interface FormattedOutput {
  markdown: string;
  json: Record<string, unknown>;
}

function formatOutput(result: unknown, format: OutputFormat): string {
  if (format === "json") {
    return JSON.stringify(result, null, 2);
  }

  // Markdown output (human-readable)
  return formatMarkdown(result);
}
```

**Rules:**
- ✅ Always support `--format md|json`
- ✅ Default to markdown (human-readable)
- ✅ Use color() for colored output (cyan, green, yellow, red)
- ✅ JSON output for machine parsing
- ✅ Never mix formats in single output

### Color Palette

```typescript
// From @sidequest/core/formatters
color("cyan", "Header")      // Information, CLI banners
color("green", "Success")    // Successful operations
color("yellow", "Warning")   // Warnings, dry-run
color("red", "Error")        // Errors, failures
color("gray", "Muted")       // Less important info
```

---

## Error Handling

### Exit Codes

```typescript
// process.exit(code)
process.exit(0)  // Success
process.exit(1)  // General error
process.exit(2)  // Argument parsing error
process.exit(3)  // Validation error
```

**Rules:**
- ✅ Exit 0 on success
- ✅ Exit non-zero on any error
- ✅ Print error to stderr with console.error
- ✅ Include helpful context in error message

### Error Messages

```typescript
// BAD ❌
console.error("Error");

// GOOD ✅
console.error(`Error: File not found at ${path}`);
console.error("Usage: bun run src/cli.ts read <file>");
```

**Rules:**
- ✅ Be specific about what failed
- ✅ Include the value that caused error
- ✅ Suggest how to fix (if obvious)
- ✅ Use color("red", ...) for errors

---

## Configuration & Environment

### Environment Variables

```typescript
// CRITICAL: Document required env vars
function loadConfig() {
  const vault = process.env.PARA_VAULT;
  if (!vault) {
    console.error("Error: PARA_VAULT environment variable required");
    process.exit(1);
  }
  return { vault };
}
```

**Rules:**
- ✅ Document all required env vars in comments
- ✅ Validate at startup
- ✅ Provide helpful error if missing
- ✅ Use `process.env.VAR_NAME`

### Package.json Bin Entry

```json
{
  "name": "@sidequest/plugin-name",
  "bin": {
    "plugin-name": "./src/cli.ts"
  },
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "bun test --recursive",
    "check": "biome check --write ."
  }
}
```

**Rules:**
- ✅ Add bin entry pointing to cli.ts
- ✅ Include executable scripts in package.json

---

## Testing CLI

```typescript
// src/cli.test.ts
import { describe, it, expect } from "bun:test";
import { parseArgs } from "@sidequest/core/cli";

describe("CLI argument parsing", () => {
  it("should parse flags with values", () => {
    const result = parseArgs(["config", "--format", "json"]);
    expect(result.command).toBe("config");
    expect(result.flags.format).toBe("json");
  });

  it("should parse --key=value format", () => {
    const result = parseArgs(["search", "query", "--dir=src"]);
    expect(result.flags.dir).toBe("src");
  });

  it("should separate positional args from flags", () => {
    const result = parseArgs(["read", "file.md", "--format", "json"]);
    expect(result.positional[0]).toBe("file.md");
    expect(result.flags.format).toBe("json");
  });
});
```

**Rules:**
- ✅ Test argument parsing thoroughly
- ✅ Test flag formats: `--key value`, `--key=value`, `--flag`
- ✅ Test error cases (missing args, invalid flags)
- ✅ Mock file I/O and external calls
- ✅ Use Bun test native (no jest/vitest)

---

## Bun-Specific Patterns

### Process I/O

```typescript
// Reading stdin (interactive)
for await (const line of console) {
  console.log(`Got: ${line}`);
}

// Writing to stdout/stderr
process.stdout.write("message");
process.stderr.write("error");
console.error("error");  // Preferred

// Running subprocesses
import { $ } from "bun";
const result = await $`ls -la`.text();
```

**Rules:**
- ✅ Use `Bun.$` for shell commands (pipes, redirects)
- ✅ Use `Bun.spawn()` for simple commands
- ✅ Capture stdout/stderr as needed
- ✅ Handle exit codes from subprocesses

### File I/O

```typescript
// Use core/fs utilities (sync + async variants)
import {
  pathExistsSync,
  readJsonFileSync,
  writeJsonFileSync,
  readTextFile,
  writeTextFile,
} from "@sidequest/core/fs";

// Don't use Node.js fs directly in new code
// ❌ import { readFileSync } from "node:fs";
```

**Rules:**
- ✅ Use @sidequest/core/fs for file operations
- ✅ Use sync versions in CLI (faster feedback)
- ✅ Validate paths (vault-scoped if applicable)
- ✅ Error on missing files early

---

## Command Dispatch Pattern

### Simple Commands (Same File)

```typescript
// For 1-3 commands
async function handleConfig(format: OutputFormat) {
  try {
    const config = await loadConfig();
    console.log(formatOutput(config, format));
  } catch (error) {
    console.error("Failed to load config:", error);
    process.exit(1);
  }
}

async function handleSearch(
  query: string,
  flags: Record<string, string | boolean>,
  format: OutputFormat,
) {
  // ...
}
```

### Complex Commands (Separate Files)

```typescript
// For 5+ commands, separate into command files
import { searchCommand } from "./commands/search";
import { configCommand } from "./commands/config";

switch (command) {
  case "search":
    await searchCommand(positional, flags, outputFormat);
    break;
  case "config":
    await configCommand(flags, outputFormat);
    break;
}
```

**Rules:**
- ✅ 1-3 commands: keep in cli.ts
- ✅ 5+ commands: split into commands/
- ✅ Each command function takes (args, flags, format)
- ✅ Commands always async (for future I/O)
- ✅ Commands handle their own errors

---

## Examples from Codebase

### Para Obsidian (Comprehensive)

```
✅ Structured parseArgs
✅ Color-coded usage output
✅ Multiple output formats (md/json)
✅ Key=value pair parsing
✅ Subcommands (frontmatter migrate)
✅ Dry-run support
✅ Error messages with context
```

### Kit CLI

```
✅ Long usage with command descriptions
✅ Separate command functions
✅ Format-agnostic output
✅ Help text extensive
```

### MCP Manager

```
✅ Configuration loading from ENV
✅ Interactive mode integration
✅ File path validation
```

---

## Checklist for New CLI Tools

### Implementation

- [ ] Shebang `#!/usr/bin/env bun`
- [ ] `parseArgs()` function with flag support
- [ ] `printUsage()` function with examples
- [ ] Output formatter (md/json)
- [ ] Error handling with exit codes
- [ ] JSDoc on all public functions

### Testing

- [ ] Test argument parsing (all flag formats)
- [ ] Test command dispatch
- [ ] Test error cases
- [ ] Test output formats (md/json)
- [ ] Manual test in shell: `bun run src/cli.ts --help`

### Documentation

- [ ] Document required environment variables
- [ ] Usage examples in --help
- [ ] README with examples
- [ ] CLAUDE.md with CLI section

### Package.json

- [ ] Bin entry pointing to cli.ts
- [ ] Scripts: typecheck, test, check
- [ ] @sidequest/core in dependencies (if using formatters/fs)

### CI/CD

- [ ] Typecheck passes (`bun typecheck`)
- [ ] Tests pass (`bun test`)
- [ ] Biome lint passes (`bun check`)

---

## Anti-Patterns (Don't Do These)

❌ **No custom argument parsing**
```typescript
// BAD - fragile, doesn't handle edge cases
const args = process.argv.slice(2);
const format = args[args.indexOf("--format") + 1];
```

❌ **No color/emphasis on output**
```typescript
// BAD - hard to read in terminal
console.log("Usage: ...");  // Should be colored
```

❌ **Mixing stdout and stderr**
```typescript
// BAD - logs errors to stdout
console.log("error details");
```

❌ **No validation of environment variables**
```typescript
// BAD - crashes later with cryptic error
const vault = process.env.VAULT_PATH;  // Could be undefined
```

❌ **Hardcoding file paths**
```typescript
// BAD - not portable
const configPath = "/Users/nathan/.config/app.json";
```

❌ **No exit codes**
```typescript
// BAD - parent process can't tell if succeeded
process.exit();  // Default exit code?
```

---

## Migration Guide for Existing CLIs

If updating existing CLI to match this standard:

1. **Extract parseArgs** → Move to utils/args.ts
2. **Standardize usage** → Use printUsage() with color
3. **Add output formatting** → Support --format md|json
4. **Use core/formatters** → Import from @sidequest/core
5. **Use core/fs** → Replace node:fs with core/fs
6. **Add tests** → Test parsing and commands
7. **Document** → Update CLAUDE.md CLI section

---

## Performance Notes

**Optimization for CLI speed:**

- ✅ Use sync file I/O for CLI (faster than async)
- ✅ Defer heavy operations (only run when needed)
- ✅ Cache index files (para-obsidian, kit)
- ✅ Use Bun's native `$` shell for pipes (faster than spawn)
- ✅ Lazy-load modules (require only used commands)

**Bun vs Node.js:**
- Bun startup: ~10-20ms
- Node.js startup: ~50-100ms
- Bun Bun.$ pipes: 2-3x faster than Node.js exec

---

## Para Obsidian CLI - Reference Implementation (10/10)

### Executive Summary

**Score: 10/10** — Para Obsidian CLI is the definitive reference implementation for the Bun CLI standard.

**Strengths:**
- ✅ Excellent argument parsing (handles all flag formats)
- ✅ Comprehensive usage with colored output (fixed: skips empty lines)
- ✅ Dual output formats (markdown + JSON)
- ✅ Rich subcommand support (frontmatter migrate, plan, apply-plan)
- ✅ Proper error handling with context
- ✅ Core utility usage (core/formatters, core/fs)
- ✅ Extracted argument utilities to utils/args.ts for reuse
- ✅ 80+ comprehensive tests covering CLI edge cases

**Recent Upgrades (✅ Completed):**
- Moved `parseArgs`, `parseKeyValuePairs`, `coerceValue` to `@sidequest/core/cli` (marketplace-wide)
- Replaced `node:fs` with `@sidequest/core/fs` utilities throughout
- Fixed usage output coloring to skip empty lines
- Added 29 argument parsing edge case tests (now 80 total tests)
- Now available for all marketplace CLI plugins to import and reuse

### Detailed Analysis

#### 1. Entry Point & Shebang ✅

```typescript
#!/usr/bin/env bun

/**
 * PARA Obsidian CLI
 *
 * Command-line interface for managing a PARA-style Obsidian vault.
 * Mirrors Kit CLI style: subcommands with minimal flags, JSON/MD output.
 */

import {
	color,
	emphasize,
	OutputFormat,
	parseOutputFormat,
} from "@sidequest/core/formatters";
```

**Status: PERFECT**
- ✅ Proper shebang
- ✅ JSDoc explaining purpose
- ✅ Correct imports from core/formatters
- ✅ Clear design philosophy documented

#### 2. Usage Output ✅

**Status: EXCELLENT** (one small refinement)
- ✅ Color-coded headers (cyan)
- ✅ Clear Usage → Options → Examples structure
- ✅ Real, copy-paste examples
- ✅ Shows flag formats clearly

#### 3. Argument Parsing ✅✅✅

**Status: PERFECT** — This became the standard pattern!
- ✅ Handles `--key=value`
- ✅ Handles `--key value`
- ✅ Handles `--flag` (boolean)
- ✅ Properly indexes through argv
- ✅ Separates command/subcommand/positional/flags
- ✅ Returns structured object

This is the **reference implementation** that other plugins should copy.

#### 4. Utility Functions ✅✅

**Status: PERFECT** (moved to core)
- ✅ Separate utility functions for clarity
- ✅ Type coercion for JSON output
- ✅ Edge case handling (empty, malformed)

**Now In Core:** These utilities have been moved to `@sidequest/core/cli` so all marketplace CLI plugins can import and reuse them.

```typescript
import { parseArgs, parseKeyValuePairs, coerceValue } from "@sidequest/core/cli";
```

This ensures consistent argument parsing across all marketplace tools.

#### 5. Core Utility Usage ✅

**Status: GOOD**
- ✅ Uses core/formatters for colors and output
- ✅ Doesn't re-implement formatting

**Enhancement:** Could use core/fs utilities for consistency with other plugins.

#### 6. Output Formatting ✅

**Status: PERFECT**
- ✅ Every command supports `--format md|json`
- ✅ Default to markdown (human-readable)
- ✅ JSON for machine parsing

#### 7. Error Handling ✅✅

**Status: EXCELLENT**
- ✅ Try/catch wrapping all operations
- ✅ Contextual error messages
- ✅ Proper exit codes (0 = success, 1 = error)
- ✅ Environment variable validation

#### 8. Subcommand Support ✅✅✅

**Status: EXCELLENT** — Clean subcommand hierarchy
- ✅ Two-level commands (frontmatter + operation)
- ✅ Clear dispatch pattern
- ✅ Each operation validates its args

#### 9. CLI Features ✅✅

**Dry-Run Support**
- ✅ All mutations support --dry-run
- ✅ Shows what would change
- ✅ User can preview before committing

**Auto-Commit Integration**
- ✅ Optional git auto-commit
- ✅ Smart attachment discovery
- ✅ Integrates with vault git repo

**Directory Scoping**
- ✅ Scopes searches to directories
- ✅ Flexible path matching
- ✅ Default: all directories

#### 10. Test Coverage ✅

**Status: GOOD**
- ✅ 51 tests passing
- ✅ Comprehensive coverage of CLI operations
- ✅ Frontmatter operations heavily tested

**Suggestion:** Add CLI arg parsing tests for edge cases.

#### 11. Documentation ✅

**Status: EXCELLENT**
- ✅ Already comprehensive
- ✅ Mirrors CLI structure

#### 12. Package.json ✅

**Status: PERFECT**
- ✅ Bin entry for executable
- ✅ Workspace dependency
- ✅ All required scripts

### Comparison to Kit CLI

| Aspect | Para Obsidian | Kit CLI |
|--------|---------------|---------|
| Arg parsing | Simple, elegant | Similar, extracted |
| Subcommands | Yes (frontmatter) | Flat |
| Color output | Yes (cyan) | Yes |
| Formats | md/json | md/json |
| Tests | 51 tests | Extensive |
| Usage text | Structured, concise | Very detailed |
| Error handling | Good | Excellent |

**Verdict:** Para Obsidian is **more advanced** (subcommands, dry-run, auto-discover), Kit is **more comprehensive** (more commands, more tests).

### Recommendations (Status Updates)

**High Priority (✅ COMPLETED)**
1. ✅ **Move parseArgs to @sidequest/core/cli** — Now available for all marketplace plugins
2. ✅ **Use core/fs utilities** — Completed, using core/fs throughout
3. ✅ **Add more CLI parsing tests** — Completed, 29 edge case tests added (80 total)

**Medium Priority (Completed)**
4. ✅ **Document argv format** — Clear in usage output (shows all three formats)
5. ✅ **Fix whitespace in usage coloring** — Now skips empty lines

**For Future Enhancement**
6. **Add --help flag** — Show usage for specific subcommands
7. **Extract command handlers** — Could split 19+ MCP tools to commands/ if needed
8. **Add performance benchmarks** — If startup speed becomes priority
9. **Add more integration tests** — End-to-end CLI testing

### Conclusion

**Para Obsidian CLI is the 10/10 reference implementation** for this marketplace:

**Exemplary Patterns:**
- ✅ Elegant argument parsing with three flag formats (now in @sidequest/core/cli)
- ✅ Advanced features (subcommands, dry-run, auto-discover, git integration)
- ✅ Excellent UX (colored output, comprehensive help, real examples)
- ✅ Comprehensive test coverage (80 tests covering edge cases)
- ✅ Clean integration with core utilities (formatters, fs)

**Use Para Obsidian as the template for:**
- **Argument parsing:** Import utilities from `@sidequest/core/cli`
- Usage output structure with colored headers
- Output formatting (markdown default + JSON)
- Error handling with contextual messages
- Subcommand dispatch architecture
- Test coverage for CLI operations

**Marketplace-Wide Benefit:**
Utilities now available in core package for all CLI plugins:
```typescript
import { parseArgs, parseKeyValuePairs, coerceValue } from "@sidequest/core/cli";
```

**This is production-grade CLI tooling for Bun.** Perfect score achieved through systematic improvements, comprehensive testing, and centralized utilities for consistency across the marketplace.

---

## Resources

- **Bun Process API:** https://bun.sh/docs/guides/process
- **Bun Shell:** https://bun.sh/docs/runtime/shell
- **Bun File I/O:** https://bun.sh/docs/runtime/file-io
- **CLI Best Practices:** https://12factor.net (especially config section)
- **Exit Codes:** https://en.wikipedia.org/wiki/Exit_status

---

## Summary

**Key Principles:**
1. **Consistency** — All CLIs follow same pattern
2. **Clarity** — Help text is comprehensive and examples work
3. **Predictability** — Flags work the same everywhere
4. **Maintainability** — Code is organized and testable
5. **Performance** — Leverage Bun's speed (sync I/O, $, startup)
6. **Accessibility** — Colored output, JSON for machines, markdown for humans

Apply these standards to all new CLI tools and refactor existing ones incrementally.

---

**Last Updated:** 2025-12-05
**Status:** Comprehensive Reference
**For Quick Start:** See [SKILL.md](../SKILL.md)
