# Reference

## Command choice
- Prefer `sg` if available. Fallback `ast-grep`. Last resort: `nix run nixpkgs#ast-grep --`.
- Default command is `run` when `--pattern` is provided.

## Read-only mode
- Do not use: `--rewrite`, `-r`, `--update-all`, `--interactive`.
- Safe flags: `--files-with-matches`, `--json=stream`, `--color=never` for pipes.

## Pattern basics
- Single meta-var: `$A` matches one node.
- Multi meta-var: `$$$A` matches multiple sibling nodes.
- Anonymous: `$_` matches without capture.
- Use `--selector` to match a sub-node kind inside a larger pattern.

## Language control
- `--lang` required for `--stdin`.
- Force language when extensions are misleading or files are generated.

## Strictness
- `cst`: exact nodes (strict).
- `smart`: skip trivial nodes.
- `ast`: named nodes only.
- `relaxed`: ignore comments.
- `signature`: ignore comments + text.
- `template`: ignore node kinds, match text.

Use strictness when patterns under/over-match.

## Debugging patterns
- `--debug-query=pattern|ast|cst|sexp` to view parsed pattern.
- Start with `ast` or `cst` to see structure.

## Output formats
- Human: default colored diagnostics.
- Files only: `--files-with-matches`.
- JSON: `--json=pretty|stream|compact`.

## Filters and scope
- Paths: pass directories or files.
- Globs: `--globs 'src/**/*.ts' --globs '!**/*.test.ts'`.
- Ignore control: `--no-ignore` (hidden, dot, vcs, etc.).
- Threads: `--threads 0` for auto.

## Inspection
-- `--inspect summary|entity` to debug file filtering.

## Safety
- Read-only search only; skip rewrite flags.

## Stdin
- Use `--stdin -l <lang>`.
- Interactive mode incompatible with stdin.
