**Skill**: [LaTeX Environment Setup](../SKILL.md)

## Installation

### Option 1: Full MacTeX (Recommended)

```bash
# Download from mactex.org
# Or install via Homebrew:
brew install --cask mactex

# Size: ~4.5 GB (includes everything)
# Includes: TeX Live 2025, TeXShop, BibDesk, LaTeXiT, Skim
```

### Option 2: Lightweight (No GUI Tools)

```bash
# Smaller install without GUI tools
brew install mactex-no-gui

# Size: ~2 GB
# Includes: TeX Live 2025, latexmk, but no TeXShop/BibDesk
```

### Install Skim Separately (if using no-gui)

```bash
brew install --cask skim

# Why Skim?
# - ONLY macOS PDF viewer with full SyncTeX support
# - Forward search: LaTeX source → PDF location
# - Inverse search: PDF → LaTeX source
# - Auto-reload on PDF changes
```
