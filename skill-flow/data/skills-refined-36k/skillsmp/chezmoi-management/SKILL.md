---
name: chezmoi-management
description: Expert guidance for managing and evolving a chezmoi-based dotfiles repo. Use for tasks like adding/removing managed files, debugging apply/diff/merge behavior, working with templates and data, `.chezmoiignore` rules, encryption/secret handling, and advanced workflows (hooks, scripts, conditional config). Prefer using Context7 to fetch the latest chezmoi docs when uncertain about flags, commands, or current behavior.
---

# Chezmoi Management

Operate as a chezmoi power-user for dotfiles management: understand the source/target model, common CLI workflows, templating, ignore rules, and drift/conflict resolution.

## Default workflow

1. **Inspect state**: use `chezmoi status` and `chezmoi diff`.
2. **Edit source directly**: modify files in this repo (the source state) using normal file edits.
3. **Apply safely**: prefer `chezmoi apply --dry-run -v`, then `chezmoi apply`.
4. **Verify**: use `chezmoi verify` after larger refactors or machine moves.

`chezmoi edit <target-path>` is optional and mainly useful when you need to jump from a target path to the correct source file without thinking about mapping.

## Complexity decision tree

- **Simple change to one file**: edit the source file → `chezmoi apply <target>`.
- **New file should be managed**: add/create source file (or `chezmoi add <target>`) → `chezmoi apply`.
- **Unexpected diffs/drift**: `chezmoi diff -v` → `chezmoi verify` → troubleshoot.
- **Conditional/templated behavior**: inspect templates + `chezmoi data`.
- **Command ambiguity / version-specific behavior**: fetch latest docs via Context7.

## Chezmoi expertise checklist

When helping with a request, explicitly consider:
- **Source vs target**: user might be editing the wrong side.
- **Source file naming**: `dot_` prefixes, `private_` files, templated variants, etc.
- **Ignore rules**: `.chezmoiignore` patterns and conditionals.
- **Templates**: `{{ ... }}` logic, `chezmoi data`, external template execution.
- **Secrets**: whether encryption/secret workflows are in play.
- **Safe operations**: prefer dry-runs and diffs before applying.

## Context7 usage (required when unsure)

When you are uncertain about the correct chezmoi command/flag, or suspect behavior has changed across versions:

1. Call `context7_resolve-library-id` with `libraryName="chezmoi"`.
2. Call `context7_query-docs` with a targeted question (exact command/flag/workflow).
3. Prefer the newest documented behavior, and mention any assumptions.

## Repo-local awareness

This repo is a chezmoi source directory. When asked to implement a change here:
- Prefer changing the **source** under version control (not `~`), unless the user explicitly wants target-side behavior.
- Use searches to find existing patterns for templates/ignore rules before inventing new ones.

## References

- Practical command patterns: `references/commands-and-workflows.md`
- Common pitfalls: `references/troubleshooting.md`
