# Book CLI

Command-line tool for managing LaTeX book projects.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) (Python package manager):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

### Option 1: Install CLI globally (recommended)

```bash
uv tool install .claude/skills/book/cli/windows/
```

This installs the `book` command globally - no virtual environment activation needed.

### Option 2: No installation required

Run the standalone script directly with `uv run` - no installation needed.

---

## Usage

All commands must be run from the **project root directory**.

### Compile Commands

| Task | CLI (after install) | Standalone (no install) |
|------|---------------------|------------------------|
| Compile full book | `book compile` | `uv run .claude/skills/book/cli/windows/compile_latex.py` |
| Compile chapter 1 | `book compile ch01` | `uv run .claude/skills/book/cli/windows/compile_latex.py ch01` |
| Compile chapter ii | `book compile chii` | `uv run .claude/skills/book/cli/windows/compile_latex.py chii` |
| Show help | `book --help` | `uv run .claude/skills/book/cli/windows/compile_latex.py --help` |

**Examples:**
```bash
book compile              # Compile main.tex (full book)
book compile ch01         # Compile ch01-ettersporselprognoser.tex
book compile chii         # Compile chii-arbeidsflyt-og-ki.tex
book compile sec01        # Compile first matching sec01-*.tex
```

### Image Commands

Generate and edit images using AI (requires GEMINI_API_KEY in .env):

| Task | CLI (after install) | Standalone (no install) |
|------|---------------------|------------------------|
| Generate image | `book image new --path "path.png" "prompt"` | `uv run .../image_gen.py new --path "path.png" "prompt"` |
| Edit image | `book image edit --path "path.png" "prompt"` | `uv run .../image_gen.py edit --path "path.png" "prompt"` |

**Examples:**
```bash
book image new --path "figures/flowchart.png" "A process diagram showing order fulfillment"
book image new -p "charts/sales.png" -r 4K "Bar chart comparing Q1-Q4 sales"
book image edit --path "figures/logo.png" "Change background to blue"
```

**Resolution options:** 1K (default), 2K, 4K

**Note:** `edit` overwrites the original image file.

**Standalone:**
```bash
uv run .claude/skills/book/cli/windows/image_gen.py new --path "figures/diagram.png" "A flowchart"
uv run .claude/skills/book/cli/windows/image_gen.py edit --path "figures/chart.png" "Add legend"
```

### Init Commands

| Task | CLI (after install) | Standalone (no install) |
|------|---------------------|------------------------|
| Init LaTeX project | `book init latex` | `uv run .claude/skills/book/cli/windows/init_book.py latex` |

### Output

All PDFs are saved to `latex/build/`.

---

## File Matching

Both CLI and standalone support the same file matching:

1. **Exact match**: `<name>.tex`
2. **Prefix match**: `<name>-*.tex`

This allows using short prefixes:
- `ch01` → `ch01-ettersporselprognoser.tex`
- `chii` → `chii-arbeidsflyt-og-ki.tex`

## Excluded Files

`localsettings.tex` cannot be compiled (not a standalone file).

---

## CLI Management

### Update CLI after code changes

```bash
uv cache clean && uv tool uninstall book-cli && uv tool install .claude/skills/book/cli/windows/
```

### Uninstall CLI

```bash
uv tool uninstall book-cli
```

---

## File Structure

```
.claude/skills/book/cli/windows/
├── pyproject.toml      # Package configuration
├── book_cli.py         # Click CLI (imports from compile_latex)
└── compile_latex.py    # Core logic (also runnable standalone)
```

Both methods use the same core logic in `compile_latex.py`, ensuring they stay in sync.
