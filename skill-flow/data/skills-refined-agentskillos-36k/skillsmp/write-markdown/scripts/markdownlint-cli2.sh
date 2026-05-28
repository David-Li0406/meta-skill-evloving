#!/usr/bin/env sh
# markdownlint-cli2 v0.20.0 (markdownlint v0.40.0)
#
# Syntax: markdownlint-cli2 glob0 [glob1] [...] [globN] [--config file] [--fix]
#         [--format] [--help] [--no-globs]
#
# Glob expressions (from the globby library):
# - * matches any number of characters, but not /
# - ? matches a single character, but not /
# - ** matches any number of characters, including /
# - {} allows for a comma-separated list of "or" expressions
# - ! or # at the beginning of a pattern negate the match
# - : at the beginning identifies a literal file path
# - - as a glob represents standard input (stdin)
#
# Dot-only glob:
# - The command "markdownlint-cli2 ." lints Markdown files in the current
#   directory only (mapped to "*.{md,markdown}")
# - To lint every file in the current directory tree, use "markdownlint-cli2 **"
#
# Optional parameters:
# - --config    base configuration file
# - --fix       updates files to resolve fixable issues
# - --format    reads stdin, applies fixes, writes stdout
# - --help      prints help and exits
# - --no-globs  ignores the "globs" property in the top-level options object
#
# Configuration via:
# - .markdownlint-cli2.jsonc | .markdownlint-cli2.yaml
# - .markdownlint-cli2.cjs   | .markdownlint-cli2.mjs
# - .markdownlint.jsonc      | .markdownlint.json
# - .markdownlint.yaml       | .markdownlint.yml
# - .markdownlint.cjs        | .markdownlint.mjs
# - package.json
#
# Cross-platform compatibility:
# - Quote globs; shells expand globs differently.
# - Some Windows shells do not handle single quotes well; use double quotes.
# - Negated patterns require quoting; "#" is safer than "!" in some shells.
# - Use forward slashes; backslashes are converted automatically.
# - Passing "--" treats all remaining parameters literally.
#
# Most compatible syntax:
#   markdownlint-cli2 "**/*.md" "#node_modules"
#
# If markdownlint-cli2 is not installed but Node.js is available:
#   npx markdownlint-cli2 "$@"
markdownlint-cli2 "$@"
