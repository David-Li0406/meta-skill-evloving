---
name: ripdoc
description: Query Rust docs and crate APIs from CLI. Use when exploring Rust crates, building API context and codemaps for handoffs, searching rustdoc, or needing crate skeletons. Trigger on "ripdoc", "rust docs", "crate API", "skelebuild", "create codemap", or when investigating Rust library usage.
compatibility: Requires the `ripdoc` cli tool (https://github.com/Alb-O/ripdoc)
---

# Ripdoc

Query Rust docs and crate APIs from the command line.

## Commands

| Command      | Purpose                          |
| ------------ | -------------------------------- |
| `print`      | Render items as Markdown         |
| `list`       | List items with source locations |
| `skelebuild` | Stateful context builder         |
| `raw`        | Output raw rustdoc JSON          |
| `readme`     | Fetch crate README               |
| `agents`     | Print AI agent guides            |

## Targets

- Crate names: `serde`, `tokio@1.0`
- Local paths: `./path/to/crate`
- Item paths: `serde::Deserialize`, `./crate::module::Type`

## Print Command

```bash
# Full crate skeleton
ripdoc print serde

# Specific item
ripdoc print serde::Deserialize

# Search by name (default)
ripdoc print tokio --search "spawn"

# Search domains: name, path, doc, signature
ripdoc print serde --search "parse" --search-spec name,signature

# Include method bodies
ripdoc print serde::Deserialize --implementation

# Include full source files
ripdoc print ./my-crate crate::Config --raw-source

# Private items
ripdoc print ./my-crate --private
```

## Skelebuild Command

Stateful context builder for creating Markdown "source maps". **Always read [references/skelebuild.md](references/skelebuild.md) when a skelebuild task is given by user for full usage!**

Quick start:

```bash
ripdoc skelebuild reset --output context.md
ripdoc skelebuild add bat::config::Config
ripdoc skelebuild add ./crate crate::Type::method
ripdoc skelebuild add-raw ./path/to/file.rs:336:364  # code not in rustdoc
ripdoc skelebuild add-changed --staged --only-rust   # from git diffs
ripdoc skelebuild preview
```

Defaults: `--implementation` ON, `--private` ON. Opt-out with `--no-implementation`, `--no-private`.

## Common Options

| Option                                  | Effect                    |
| --------------------------------------- | ------------------------- |
| `--search <regex>`                      | Filter by pattern         |
| `--search-spec name,doc,signature,path` | Search domains            |
| `--implementation`                      | Include method bodies     |
| `--raw-source`                          | Include full source files |
| `--private`                             | Include private items     |
| `--features <list>`                     | Enable crate features     |
| `--all-features`                        | Enable all features       |
| `--no-default-features`                 | Disable defaults          |

## Path Resolution

Rustdoc paths differ from `use` paths. Discover exact paths:

```bash
ripdoc list serde --search "Deserialize" --search-spec path --private
```

- Use `crate::` prefix for local crates
- Bin crates use binary name as root
- Re-exports appear at definition site

## Troubleshooting

**No matches found:**

1. Check path: `ripdoc list <target> --search "<name>" --search-spec path --private`
2. Item may be re-exported; search by name for definition path
3. Private items need `--private`

**Missing items:**

- Feature-gated: use `--features`
- Private: use `--private`
- Not in rustdoc: use `add-raw` or `add-file`

**Empty skelebuild output**: See [references/skelebuild.md](references/skelebuild.md#troubleshooting-empty-output)
