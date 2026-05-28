# Platform Detection

## Detection Snippets

### GitHub Codespaces

```bash
if [[ -n "$CODESPACES" ]]; then
    # Running in GitHub Codespaces
    # Usually Debian-based Linux
fi
```

The `$CODESPACES` environment variable is set automatically.

Additional Codespaces variables:
- `$CODESPACE_NAME` - Unique codespace identifier
- `$GITHUB_REPOSITORY` - The repo the codespace was created for

### macOS

```bash
if [[ "$(uname)" == "Darwin" ]]; then
    # Running on macOS
fi
```

### Arch Linux

```bash
if command -v pacman &>/dev/null; then
    # Running on Arch Linux (or Arch-based distro)
fi
```

### Omarchy

Omarchy is Arch Linux with a custom Hyprland setup. Detect it by checking for its marker directory:

```bash
if [[ -d "$HOME/.local/share/omarchy" ]]; then
    # Running on Omarchy
    # Uses default Omarchy configs, skip dotfiles apply()
fi
```

Note: Omarchy uses its own configs, so `dotfiles pull` skips `apply()` on Omarchy.

## Package Manager Commands

| Platform | Install | Update | Search |
|----------|---------|--------|--------|
| Codespaces | `sudo apt-get install -y <pkg>` | `sudo apt-get update` | `apt-cache search <pkg>` |
| macOS | `brew install <pkg>` | `brew update && brew upgrade` | `brew search <pkg>` |
| Arch | `sudo pacman -S --noconfirm <pkg>` | `sudo pacman -Syu` | `pacman -Ss <pkg>` |
| Arch (AUR) | `yay -S --noconfirm <pkg>` | `yay -Syu` | `yay -Ss <pkg>` |

## Combined Detection Pattern

```bash
detect_platform() {
    if [[ -n "$CODESPACES" ]]; then
        echo "codespaces"
    elif [[ "$(uname)" == "Darwin" ]]; then
        echo "macos"
    elif command -v pacman &>/dev/null; then
        echo "arch"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)

case "$PLATFORM" in
    codespaces)
        PKG_INSTALL="sudo apt-get install -y"
        ;;
    macos)
        PKG_INSTALL="brew install"
        ;;
    arch)
        PKG_INSTALL="sudo pacman -S --noconfirm"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

# Usage: $PKG_INSTALL <package-name>
```

## Common Gotchas

1. **apt vs apt-get**: Use `apt-get` in scripts (more stable interface)
2. **Homebrew on Linux**: Some people use Homebrew on Linux; check `uname` not just `brew`
3. **sudo in Codespaces**: Usually available without password
4. **yay vs pacman**: Use `yay` for AUR packages, `pacman` for official repos
