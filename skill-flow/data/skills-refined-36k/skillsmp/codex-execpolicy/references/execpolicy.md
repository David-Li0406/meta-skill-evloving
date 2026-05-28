# Execpolicy Reference (Codex)

Use this as a compact reference when writing `.rules` files for Codex execpolicy.

## Rule files

- Rule files use Starlark syntax and end with `.rules`.
- Codex loads all `.rules` files under `~/.codex/rules/` at startup.
- The Codex TUI appends new allowlist entries to `~/.codex/rules/default.rules`.

## prefix_rule

`prefix_rule(...)` matches a command if the rule pattern is a prefix of the command's argv.

Parameters:

- `pattern` (required): a list of argv tokens.
  - Each element is either a literal token or a list of alternatives (union).
  - Example union: `["gh", "pr", ["view", "list"]]`
- `decision` (optional): `"allow"` (default), `"prompt"`, or `"forbidden"`.
- `match` / `not_match` (optional): tests that must pass at load time; use lists of argv examples.

Decision precedence:

- If multiple rules match, the most restrictive decision wins.
  - `forbidden` > `prompt` > `allow`

## Validation

Run a check before finishing edits:

```bash
codex execpolicy check --pretty --rules <path> -- <command>
```

- Provide multiple `--rules` arguments to combine files.
- Use real-world examples that should match and should not match.

## Minimal patterns

Block a command:

```starlark
prefix_rule(
  pattern = ["git"],
  decision = "forbidden",
)
```

Allow a specific subcommand prefix:

```starlark
prefix_rule(
  pattern = ["ssh", "-V"],
  decision = "allow",
)
```
