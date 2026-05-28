---
name: xl-cli
description: Use this skill when performing LLM-friendly Excel operations via the `xl` CLI, such as reading cells, evaluating formulas, and exporting data.
---

# Skill body

## Installation

Check if installed: 
```bash
which xl || echo "not installed"
```

**If not installed**, download the latest native binary (no JDK required):

**macOS/Linux (recommended):**
```bash
# Auto-detect platform and install latest release
REPO="TJC-LP/xl"
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
VERSION=${LATEST#v}
case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)  BINARY="xl-$VERSION-linux-amd64" ;;
  Linux-aarch64) BINARY="xl-$VERSION-linux-arm64" ;;
  Darwin-x86_64) BINARY="xl-$VERSION-darwin-amd64" ;;
  Darwin-arm64)  BINARY="xl-$VERSION-darwin-arm64" ;;
  *) echo "Unsupported: $(uname -s)-$(uname -m)" && exit 1 ;;
esac
mkdir -p ~/.local/bin
curl -sL "https://github.com/$REPO/releases/download/$LATEST/$BINARY" -o ~/.local/bin/xl
chmod +x ~/.local/bin/xl
echo "Installed xl $VERSION to ~/.local/bin/xl"
```

**Alternative using GitHub CLI:**
```bash
# If gh is installed (simpler, handles auth for private repos)
gh release download --repo TJC-LP/xl --pattern "xl-*-$(uname -s | tr A-Z a-z)-$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')" -D /tmp
mv /tmp/xl-* ~/.local/bin/xl && chmod +x ~/.local/bin/xl
```

**Windows (PowerShell):**
```powershell
$repo = "TJC-LP/xl"
$latest = (Invoke-RestMethod "https://api.github.com/repos/$repo/releases/latest").tag_name
$version = $latest -replace '^v', ''
$url = "https://github.com/$repo/releases/download/$latest/xl-$version-windows-amd64.exe"
Invoke-WebRequest -Uri $url -OutFile "$env:LOCALAPPDATA\xl.exe"
Write-Host "Installed xl $version"
```

Ensure `~/.local/bin` is in your PATH: 
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

Run `xl <command> --help` for comprehensive usage, options, and examples. 

### Quick Reference

#### Info Commands (no file required)
```bash
xl functions                           # List all 81 supported functions
xl rasterizers                         # Check SVG-to-raster backends
```

#### Read Operations
```bash
xl -f <file> sheets                    # List sheets with stats
xl -f <file> names                     # List named ranges
```

### Common Operations
- **Read cells**: `xl -f <file> get <cell>` to read a specific cell.
- **View ranges**: `xl -f <file> view <range>` to view a specific range.
- **Search**: `xl -f <file> search <term>` to search for a term in the spreadsheet.
- **Evaluate formulas**: `xl -f <file> eval <formula>` to evaluate a formula.
- **Export**: `xl -f <file> export <format>` to export data in CSV, JSON, PNG, or PDF.
- **Style cells**: `xl -f <file> style <cell> <style>` to apply styles to specific cells.
- **Modify rows/columns**: `xl -f <file> modify <row/column> <action>` to modify rows or columns.