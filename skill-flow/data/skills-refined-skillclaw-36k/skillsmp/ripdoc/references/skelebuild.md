# Skelebuild Reference

Incrementally build Markdown "source maps" by mixing API skeletons, selective implementation spans, and commentary. State persists at `~/.local/state/ripdoc/skelebuild.json`.

## Workflow

```bash
# Start fresh
ripdoc skelebuild reset --output context.md

# Add items (includes implementation spans by default)
ripdoc skelebuild add bat::config::Config
ripdoc skelebuild add ./crate crate::Type::method

# Add multiple items at once
ripdoc skelebuild add ./tome/bin/tome-term \
  tome::editor::Editor::render \
  tome::editor::Editor::ensure_cursor_visible

# Add raw source directly from disk (for tests / code not in rustdoc)
ripdoc skelebuild add-raw ./path/to/file.rs:336:364
ripdoc skelebuild add-file ./path/to/file.rs  # entire file

# Add context from git diffs
ripdoc skelebuild add-changed --git HEAD^..HEAD --only-rust
ripdoc skelebuild add-changed --staged --only-rust

# Insert notes (prefer target-relative insertion; \n becomes newline)
ripdoc skelebuild inject '## Notes\nWhy this matters...' --after-target bat::config::Config

# Inject from stdin (auto-detected, no --from-stdin needed!)
ripdoc skelebuild inject --after-target bat::config::Config <<'EOF'
## Notes
My commentary with 'quotes' and $variables
EOF

# Or with a pipe
echo "## Notes" | ripdoc skelebuild inject --after-target bat::config::Config

# Other commands
ripdoc skelebuild preview      # print output without writing file
ripdoc skelebuild status       # show entries and indices
ripdoc skelebuild update bat::config::Config --implementation
ripdoc skelebuild remove bat::assets::get_acknowledgements
```

## Defaults

- `--implementation` ON (method bodies included)
- `--private` ON (private items resolved)
- Plain/flat output mode

Opt-out: `--no-implementation`, `--no-private`

## Tips

- **Injection placement**: Prefer `--after-target <spec>` / `--before-target <spec>` over `--at <index>` (indices shift)
- **Auto-stdin**: `inject` automatically reads from stdin when piping or using heredocs
- **Canonical keys**: `add-file` and `add-raw` print canonical repo-relative keys for easy matching
- **Impl-block targeting**: Target an entire impl with `Type::Trait` (e.g. `Editor::EditorOps`)
- **Validation**: `add` validates by default; use `--no-validate` to skip
- **Inject escaping**: `\n`, `\t`, `\\` are unescaped by default; use `--literal` to keep backslashes
- **Errors to stderr**: Warnings/errors go to stderr, keeping output doc clean

## Target Resolution

Target specs can be paths (`./path/to/crate`) or names (`serde`). Both forms work:

```bash
ripdoc skelebuild add ./path/to/crate crate::module::Type
ripdoc skelebuild add serde::de::Deserialize
```

**Resolution rules:**

- Inside Cargo workspace: resolves workspace members and dependencies by name
- Outside workspace: tries crates.io / local cache
- For bin crates, the `crate::` prefix is often the *bin name*, not the package name
- You can usually omit the crate prefix (e.g. `terminal_panel::TerminalState`)

**Finding paths:** Use `ripdoc list` to discover exact paths:

```bash
ripdoc list ./path/to/crate --search TerminalState --search-spec path --private
```

**Inherent vs trait methods:** If ambiguous, use a more specific path:

- Inherent: `crate::Type::method`
- Trait: `crate::Trait::method`
- Fully-qualified: `<crate::Type as crate::Trait>::method`

## Speed Guide: 1000+ Lines in \<60s

Execute multiple **parallel bash calls**, each containing **sequential `&&` chains**.

```bash
# Parallel call 1: code path A
ripdoc skelebuild add ./crate Path1::Item1 && ripdoc skelebuild add ./crate Path1::Item2

# Parallel call 2: code path B
ripdoc skelebuild add ./crate Path2::Item1 && ripdoc skelebuild add ./crate Path2::Item2
```

**Strategy:**

1. Initialize: `ripdoc skelebuild reset --output <file>.md`
2. Parallel blast: Launch 5-10 parallel bash tools covering:
   - Core structs & lifecycle methods
   - Primary API implementation
   - Error handling paths
   - Tests & raw source (`add-raw`)
3. Read output: The file auto-updates after each command

**Rules:**

- Sequential (`&&`): Within a single code path where order matters
- Parallel: For unrelated paths or different subsystems
- Use `--no-implementation` when you need ONLY signatures

## Troubleshooting: Empty Output

If skelebuild warns that entries exist but output is nearly empty:

```
Warning: 5 target entries exist but rebuilt output is nearly empty (0 chars).
```

**Causes & solutions:**

1. Feature-gated code: use `--features my_feature` when adding
2. Code not in rustdoc: use `add-raw` or `add-file` instead
3. Wrong paths: discover exact path with `ripdoc list --search <name> --private`
