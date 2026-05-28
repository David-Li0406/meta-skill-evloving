# difft (Difftastic) Advanced Usage

## Display Modes

```bash
difft --display=side-by-side file1 file2  # Default
difft --display=inline file1 file2         # Unified style
```

## Filtering

```bash
difft --skip-unchanged                     # Skip unchanged files
difft --context=3                          # Control context lines
difft --language=python file1 file2        # Override language detection
difft --list-languages                     # Show supported parsers
```

## Visual Customization

```bash
difft --color=always                       # Force color (for piping)
difft --color=never                        # Disable color
difft --width=120                          # Set terminal width
difft --tab-width=4                        # Set tab width
```

## Git Integration

**One-time use:**
```bash
GIT_EXTERNAL_DIFF=difft git diff
GIT_EXTERNAL_DIFF=difft git show HEAD
GIT_EXTERNAL_DIFF=difft git log -p
```

**Permanent config (`~/.gitconfig`):**
```ini
[diff]
    external = difft
```

**As difftool:**
```bash
git config --global diff.tool difftastic
git config --global difftool.difftastic.cmd 'difft "$LOCAL" "$REMOTE"'
git difftool HEAD~1
```

## Directory Comparison

```bash
difft dir1/ dir2/                          # Compare directories
difft --skip-unchanged dir1/ dir2/         # Skip identical files
```

## Semantic Advantages

Unlike traditional diff:
- Recognizes reformatted code as unchanged
- Identifies moved functions
- Highlights variable renames precisely
- Ignores whitespace-only changes

## Exit Codes

- `0` - Files are identical
- `1` - Files differ

Enables scripted workflows:
```bash
if difft --quiet old.py new.py; then
    echo "No semantic changes"
fi
```

## Configuration File

`~/.config/difft/config.toml`:
```toml
display = "inline"
context = 5
tab-width = 4
color = "auto"
```

## Supported Languages

40+ languages including: TypeScript, JavaScript, Python, Go, Rust, Java, C/C++, Ruby, Haskell, OCaml, Elixir, and more.
