# External Files

Include files from URLs, archives, or git repos using `.chezmoiexternal.toml`.

## File Types

### Single File

```toml
[".local/bin/starship"]
    type = "file"
    url = "https://github.com/starship/starship/releases/latest/download/starship-x86_64-apple-darwin.tar.gz"
    executable = true
    refreshPeriod = "168h"  # Re-download weekly
```

### Archive Extraction

```toml
[".config/nvim"]
    type = "archive"
    url = "https://github.com/user/nvim-config/archive/main.tar.gz"
    stripComponents = 1  # Remove top-level directory
    refreshPeriod = "168h"
```

### Git Repository

```toml
[".oh-my-zsh"]
    type = "git-repo"
    url = "https://github.com/ohmyzsh/ohmyzsh.git"
    refreshPeriod = "168h"

[".oh-my-zsh/custom/plugins/zsh-syntax-highlighting"]
    type = "git-repo"
    url = "https://github.com/zsh-users/zsh-syntax-highlighting.git"
    refreshPeriod = "168h"
```

### Archive File (Single File from Archive)

```toml
[".local/bin/fzf"]
    type = "archive-file"
    url = "https://github.com/junegunn/fzf/releases/download/0.44.1/fzf-0.44.1-darwin_arm64.zip"
    path = "fzf"
    executable = true
```

## Common Options

| Option | Description |
|--------|-------------|
| `type` | `file`, `archive`, `archive-file`, `git-repo` |
| `url` | Source URL |
| `refreshPeriod` | How often to re-download (e.g., `168h` = weekly) |
| `executable` | Set executable permission (for files) |
| `stripComponents` | Remove N path levels from archive |
| `path` | Path within archive (for `archive-file`) |
| `clone.args` | Git clone arguments |
| `pull.args` | Git pull arguments |

## Checksum Verification

```toml
[".local/bin/tool"]
    type = "file"
    url = "https://example.com/tool"
    executable = true
    [".local/bin/tool".checksum]
        sha256 = "abc123..."
```

## OS-Specific External Files

Use templates in `.chezmoiexternal.toml.tmpl`:

```toml
{{- if eq .chezmoi.os "darwin" }}
[".local/bin/tool"]
    type = "file"
    url = "https://example.com/tool-darwin-{{ .chezmoi.arch }}"
    executable = true
{{- else if eq .chezmoi.os "linux" }}
[".local/bin/tool"]
    type = "file"
    url = "https://example.com/tool-linux-{{ .chezmoi.arch }}"
    executable = true
{{- end }}
```

## Nested Git Repos

For repos with submodules or plugins:

```toml
[".oh-my-zsh"]
    type = "git-repo"
    url = "https://github.com/ohmyzsh/ohmyzsh.git"
    refreshPeriod = "168h"
    clone.args = ["--depth", "1"]

[".oh-my-zsh/custom/plugins/zsh-autosuggestions"]
    type = "git-repo"
    url = "https://github.com/zsh-users/zsh-autosuggestions.git"
    refreshPeriod = "168h"
    clone.args = ["--depth", "1"]

[".oh-my-zsh/custom/plugins/zsh-syntax-highlighting"]
    type = "git-repo"
    url = "https://github.com/zsh-users/zsh-syntax-highlighting.git"
    refreshPeriod = "168h"
    clone.args = ["--depth", "1"]
```

## GitHub Release Assets

Download specific release assets:

```toml
[".local/bin/gh"]
    type = "archive-file"
    url = "https://github.com/cli/cli/releases/download/v2.40.0/gh_2.40.0_macOS_arm64.zip"
    path = "gh_2.40.0_macOS_arm64/bin/gh"
    executable = true
```

## Refresh Behavior

- `refreshPeriod` determines how often chezmoi checks for updates
- Files are only re-downloaded if the source has changed
- Git repos do a `git pull` on refresh
- Use `chezmoi update` to force refresh

## Directory for External Configs

For complex external configurations, use `.chezmoiexternals/`:

```
.chezmoiexternals/
├── oh-my-zsh.toml
├── vim-plugins.toml
└── fonts.toml
```

Each file is processed as part of `.chezmoiexternal.toml`.
