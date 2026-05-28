**Skill**: [LaTeX Environment Setup](../SKILL.md)

## Package Management

### Check if Package Installed

```bash
# Use kpsewhich to find package
kpsewhich tabularray.sty
# If found: /usr/local/texlive/2025/texmf-dist/tex/latex/tabularray/tabularray.sty
# If not found: (empty output)
```

### Install Missing Package

```bash
# Update TeX Live package manager
sudo tlmgr update --self

# Install specific package
sudo tlmgr install tabularray

# Verify installation
kpsewhich tabularray.sty
```

### Search for Packages

```bash
# Search for package by name
tlmgr search --global tabularray

# List all installed packages
tlmgr list --only-installed
```
