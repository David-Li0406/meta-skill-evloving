# tokei Advanced Usage

## Language Filtering

```bash
tokei --type=TypeScript,JavaScript,Python  # Specific languages
tokei --exclude-lang=JSON,Markdown         # Exclude languages
tokei --languages                          # List all recognized languages
```

## Path Filtering

```bash
tokei src/                                 # Target specific directory
tokei --exclude="vendor/*"                 # Exclude paths
tokei --exclude="*.test.*"                 # Exclude patterns
tokei --hidden                             # Include hidden files
tokei --no-ignore                          # Include gitignored files
tokei --max-depth=2                        # Limit traversal depth
```

## Output Formats

```bash
tokei                                      # Default table format
tokei --compact                            # Condensed table
tokei -o json                              # JSON (for jq/automation)
tokei -o yaml                              # YAML output
```

**JSON with jq:**
```bash
tokei -o json | jq '.TypeScript.code'      # Get TypeScript lines
tokei -o json | jq 'to_entries | sort_by(.value.code) | reverse'
```

## Sorting

```bash
tokei --sort=code                          # By code lines (default)
tokei --sort=files                         # By file count
tokei --sort=comments                      # By comment lines
tokei --sort=blanks                        # By blank lines
tokei --sort=lines                         # By total lines
```

## Per-File Statistics

```bash
tokei --files                              # Show stats per file
tokei --files --type=Go                    # Per-file for specific lang
```

## Automation Patterns

**Before/After comparison:**
```bash
tokei -o json > before.json
# ... make changes ...
tokei -o json > after.json
diff <(jq '.Go.code' before.json) <(jq '.Go.code' after.json)
```

**CI size validation:**
```bash
MAX_LINES=50000
TOTAL=$(tokei -o json | jq '[.[].code] | add')
if [ "$TOTAL" -gt "$MAX_LINES" ]; then
    echo "Codebase exceeds $MAX_LINES lines"
    exit 1
fi
```

**Historical tracking:**
```bash
echo "$(date -I),$(tokei -o json)" >> metrics.jsonl
```

## Configuration

Create `.tokeirc` or `tokei.toml` in project root:
```toml
[languages.Python]
extensions = ["py", "pyw"]

[languages.TypeScript]
extensions = ["ts", "tsx"]
```

## Performance

- Multi-threaded by default
- Fastest among line-counting tools
- Handles large monorepos efficiently
