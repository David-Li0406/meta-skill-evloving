**Skill**: [LaTeX Environment Setup](../SKILL.md)

## Skim Configuration

### Enable SyncTeX

**In LaTeX compilation:**

```bash
# Add -synctex=1 flag
pdflatex -synctex=1 document.tex

# Or use latexmk (automatically enables SyncTeX)
latexmk -pdf document.tex
```

### Skim Preferences

1. **Skim → Preferences → Sync**
1. **Preset:** Custom
1. **Command:** Path to editor executable
1. **Arguments:** Depends on editor (e.g., for VS Code: `--goto %file:%line`)

**For Helix:**

```
Command: /usr/local/bin/hx
Arguments: %file:%line
```
