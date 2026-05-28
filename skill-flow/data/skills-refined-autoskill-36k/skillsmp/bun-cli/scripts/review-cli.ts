#!/usr/bin/env bun

/**
 * CLI Review Tool
 *
 * This is a stub script for the dev-toolkit markdown-only plugin.
 * In a full TypeScript implementation, this would:
 * - Review CLI implementations against BUN_CLI_STANDARD.md
 * - Check for common patterns and best practices
 * - Provide scoring and improvement suggestions
 * - Validate argument parsing, output formats, error handling
 *
 * Usage (when implemented):
 *   bunx review-cli ./src/cli.ts
 *   bunx review-cli ./src/cli.ts --format json
 *
 * Checks performed:
 *   ✓ Shebang present
 *   ✓ JSDoc documentation
 *   ✓ Argument parsing (handles --flag value, --flag=value, --flag)
 *   ✓ Output formats (markdown + JSON)
 *   ✓ Error handling (try/catch, exit codes)
 *   ✓ Usage text (clear, concise, examples)
 *   ✓ Subcommand dispatch (if applicable)
 *   ✓ Color output (formatted correctly)
 *   ✓ Tests present (unit + integration)
 *
 * Output: Score (0-10) with detailed feedback
 */

console.log(
	"review-cli: Review CLI against BUN_CLI_STANDARD.md (stub - not implemented)",
);
console.log("");
console.log("When implemented, this will:");
console.log("- Review CLI implementations against the marketplace standard");
console.log("- Check for common patterns and best practices");
console.log("- Provide scoring and improvement suggestions");
console.log("");
console.log("Standard checks:");
console.log("- Shebang: #!/usr/bin/env bun");
console.log(
	"- Argument parsing (3 formats: --flag value, --flag=value, --flag)",
);
console.log("- Output formats (markdown default, JSON via --format json)");
console.log("- Error handling (try/catch, exit codes 0/1)");
console.log("- Usage text (clear structure with examples)");
console.log("- Subcommands (if applicable)");
console.log("- Tests (unit + integration)");
console.log("");
console.log("References:");
console.log("- BUN_CLI_STANDARD.md for full standard details");
console.log("- CLI_REVIEW.md for reference implementation example");
