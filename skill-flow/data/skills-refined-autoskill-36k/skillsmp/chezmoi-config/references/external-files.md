# Chezmoi External Files (.chezmoiexternal)

## Overview

`.chezmoiexternal.$FORMAT.tmpl` files allow chezmoi to automatically download and integrate external resources (files, archives, git repositories) into your dotfiles.

## File Format

- **Location**: Anywhere in source state (`~/.local/share/chezmoi` or `.chezmoiroot`)
- **Formats**: `.chezmoiexternal.toml`, `.chezmoiexternal.yaml`, `.chezmoiexternal.json`
- **Template**: Always interpreted as a template (with or without `.tmpl` extension)

## Entry Types

### 1. File Download

Download a single file from a URL:

```toml
[".vim/autoload/plug.vim"]
    type = "file"
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    refreshPeriod = "168h"
```

**Parameters:**
- `type` (required): `"file"`
- `url` (required): URL to download from
- `refreshPeriod` (optional): How often to re-download (e.g., `"168h"`, `"744h"`)
- `executable` (optional): Set file as executable (`true`/`false`)

### 2. Archive Download

Download and extract archives:

```toml
[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"
```

**Parameters:**
- `type` (required): `"archive"`
- `url` (required): Archive URL
- `exact` (optional): Extract archive to exact path (`true`/`false`)
- `stripComponents` (optional): Number of path components to strip (default: `0`)
- `refreshPeriod` (optional): Update interval
- `include` (optional): Array of glob patterns to include
- `exclude` (optional): Array of glob patterns to exclude

**Supported archive formats:**
- `.tar.gz`, `.tar.bz2`, `.tar.xz`, `.tar.zst`
- `.zip`
- `.gz` (single file, decompressed only)

### 3. Archive File Download

Extract specific file from archive:

```toml
[".local/bin/age"]
    type = "archive-file"
    url = "https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-{{ .chezmoi.os }}-{{ .chezmoi.arch }}.tar.gz"
    path = "age/age"
    executable = true
```

**Parameters:**
- `type` (required): `"archive-file"`
- `url` (required): Archive URL
- `path` (required): Path within archive to extract
- `executable` (optional): Set as executable
- `stripComponents` (optional): Path components to strip

### 4. Git Clone

Clone a git repository:

```toml
[".local/share/chezmoi/lib/zsh-zimfw"]
    type = "git"
    url = "https://github.com/zimfw/zimfw.git"
    pull = {
        ref = "main"
        args = ["--rebase", "--autostash"]
    }
    refreshPeriod = "168h"
    exact = true
```

**Parameters:**
- `type` (required): `"git"`
- `url` (required): Git repository URL
- `pull.ref` (optional): Branch/tag/commit to checkout (default: remote's default)
- `pull.args` (optional): Arguments for `git pull`
- `refreshPeriod` (optional): How often to pull updates
- `exact` (optional): Clone to exact path without `.git` directory
- `clone.args` (optional): Arguments for `git clone`
- `shallow` (optional): Use shallow clone (`--depth=1`)
- `sparseCheckout` (optional): Enable sparse checkout
- `sparseCheckoutPaths` (optional): Paths for sparse checkout

## Complete Examples

### Oh My Zsh with Plugins

```toml
# .chezmoiexternal.toml.tmpl

[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"

[".oh-my-zsh/custom/plugins/zsh-syntax-highlighting"]
    type = "archive"
    url = "https://github.com/zsh-users/zsh-syntax-highlighting/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"

[".oh-my-zsh/custom/plugins/zsh-autosuggestions"]
    type = "archive"
    url = "https://github.com/zsh-users/zsh-autosuggestions/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"

[".oh-my-zsh/custom/themes/powerlevel10k"]
    type = "archive"
    url = "https://github.com/romkatv/powerlevel10k/archive/v1.15.0.tar.gz"
    exact = true
    stripComponents = 1
```

### Platform-Specific Binaries

```toml
[".local/bin/age"]
    type = "archive-file"
    url = "https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-{{ .chezmoi.os }}-{{ .chezmoi.arch }}.tar.gz"
    path = "age/age"
    executable = true
```

### Conditional External Resources

```toml
{{- if eq .chezmoi.os "darwin" }}

[".local/bin/brew"]
    type = "file"
    url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    executable = true

{{- end }}
```

### Selective Archive Inclusion

```toml
["www/adminer/plugins"]
    type = "archive"
    url = "https://api.github.com/repos/vrana/adminer/tarball"
    refreshPeriod = "744h"
    stripComponents = 2
    include = ["*/plugins/**"]
```

### Git Repository with Sparse Checkout

```toml
[".vim/bundle/youcompleteme"]
    type = "git"
    url = "https://github.com/ycm-core/YouCompleteMe.git"
    shallow = true
    sparseCheckout = true
    sparseCheckoutPaths = [
        "autoload/",
        "plugin/",
        "doc/"
    ]
```

## Refresh Period Format

- `"168h"` - 168 hours (7 days)
- `"24h"` - 24 hours
- `"744h"` - 744 hours (31 days)
- `"0"` - Always refresh (not recommended)

## Best Practices

1. **Use `stripComponents`** to avoid nested vendor directories
2. **Set appropriate `refreshPeriod`** to balance freshness and bandwidth
3. **Use templates** (`{{ .chezmoi.os }}`) for platform-specific downloads
4. **Pin versions** in URLs (e.g., `v1.15.0.tar.gz`) for reproducibility
5. **Use `exact = true`** to remove `.git` directories from externals
6. **Organize entries** by purpose (shell, editors, tools)
7. **Test URLs** before adding to ensure they're accessible

## Ignoring External Files

If `.chezmoiexternal.$FORMAT` is in an ignored directory (listed in `.chezmoiignore`), all entries are also ignored.
