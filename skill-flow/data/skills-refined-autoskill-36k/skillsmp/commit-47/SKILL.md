---
name: commit
description: Create atomic git commits following project conventions with chunk-based staging
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

Create atomic commits for staged/unstaged changes using chunk-based staging.

## Commit Format

Title: `module: Verb in imperative style`
- Lowercase module name before colon
- Capital letter after colon
- Imperative verb: Add, Fix, Update, Remove, Refactor

Body: Bullet points only
- Lowercase start for each bullet
- NO prose paragraphs
- NO Co-Authored-By
- NO Claude signatures
- NO emojis

## Process

1. Run `git status` and `git diff` to understand all changes
2. Run `git log -5 --oneline` to see recent commit style
3. Identify logical groups of changes that belong together
4. For each logical group:
   - Stage specific chunks with `git add -p <file>` for modified files
   - For new files: `git add -N <file> && git add -p <file>`
   - Verify staged changes: `git diff --cached`
   - Run `nix flake check`
   - Create commit using HEREDOC:
     ```bash
     git commit -m "$(cat <<'EOF'
     module: Title here

     - bullet point describing what changed
     - another bullet if needed
     EOF
     )"
     ```
5. Run `git log --oneline -5` to verify

## Fixup Commits

For iterations after review feedback, use fixup commits:
```bash
git commit --fixup=HEAD
```

Or target a specific commit:
```bash
git commit --fixup=<commit-hash>
```

Fixups will be squashed later with `/branch-cleanup`.

## Chunk Staging Reference

Interactive patch mode (`git add -p`) commands:
- `y` - stage this hunk
- `n` - skip this hunk
- `s` - split into smaller hunks
- `q` - quit, do not stage remaining hunks

## Rules

- One logical change per commit
- Separate unrelated changes into different commits
- NEVER push to remote
- NEVER use --amend unless explicitly requested
- NEVER skip nix flake check
