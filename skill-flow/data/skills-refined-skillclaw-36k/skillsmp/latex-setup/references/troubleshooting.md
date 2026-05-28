**Skill**: [LaTeX Environment Setup](../SKILL.md)

## Troubleshooting

### Issue: TeX binaries not in PATH

```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/Library/TeX/texbin:$PATH"

# Reload shell
source ~/.zshrc
```

### Issue: sudo required for tlmgr

```bash
# This is normal for system-wide MacTeX installation
# Use sudo for package management:
sudo tlmgr install <package>
```

### Issue: Package not found

```bash
# Update tlmgr database
sudo tlmgr update --self --all

# Search for package
tlmgr search --global <package-name>

# Install
sudo tlmgr install <package-name>
```

### Issue: Permission errors

```bash
/usr/bin/env bash << 'TROUBLESHOOTING_SCRIPT_EOF'
# Fix permissions on TeX Live directory
sudo chown -R $(whoami):staff /usr/local/texlive/2025/texmf-var
TROUBLESHOOTING_SCRIPT_EOF
```
