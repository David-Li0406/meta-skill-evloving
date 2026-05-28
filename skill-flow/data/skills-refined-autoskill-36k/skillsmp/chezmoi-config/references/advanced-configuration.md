# Chezmoi Advanced Configuration

## Configuration Files

### File Locations

Chezmoi looks for configuration files in this order:

1. `~/.config/chezmoi/chezmoi.toml` (user config)
2. `~/.config/chezmoi/chezmoi.yaml` (YAML format)
3. `~/.config/chezmoi/chezmoi.json` (JSON format)
4. `.chezmoi.toml.tmpl` in source state (template, can be committed)

### Basic Configuration

**chezmoi.toml:**
```toml
[data]
    name = "John Doe"
    email = "john@example.com"

[editor]
    command = "vim"

[merge]
    command = "vimdiff"
```

### Template Configuration

**.chezmoi.toml.tmpl:**
```toml
{{- $email := promptBool "use work email?" -}}
[data]
    name = "{{ promptString "your name" }}"
    email = {{ if $email -}}
        "john@work.com"
    {{- else -}}
        "john@personal.com"
    {{- end }}
    editor = "{{ promptString "favorite editor" "vim" }}"

{{ if eq .chezmoi.os "darwin" -}}
[data.darwin]
    homebrew_prefix = "/opt/homebrew"
{{ end -}}
```

## Configuration Sections

### Color Configuration

```toml
[color]
    # Enable color output (auto, always, never)
    when = "auto"
```

### Data Section

Custom variables for templates:

```toml
[data]
    # Simple values
    name = "John Doe"
    editor = "vim"

    # Nested data
    [data.github]
        username = "johndoe"
        token_var = "GITHUB_TOKEN"

    # Lists
    [data.packages]
        darwin = ["git", "vim", "ripgrep"]
        linux = ["git", "vim", "ripgrep", "fd-find"]
```

### Editor Configuration

```toml
[editor]
    command = "vim"
    # Or with arguments
    args = ["--noplugin", "+set\\ ft=chezmoi"]
```

### Merge Configuration

How to merge conflicting files:

```toml
[merge]
    command = "vimdiff"

# Or use a 3-way merge tool
[merge]
    command = "nvim"
    args = ["-d", "{{ .Destination }}", "{{ .Source }}", "{{ .Target }}"]
```

**Common merge tools:**
- `vimdiff` - Vim's built-in diff
- `nvim -d` - Neovim diff
- `code --wait` - VS Code merge
- `opendiff` - macOS FileMerge
- `kdiff3` - Cross-platform merge tool

### Encryption Configuration

Encrypt sensitive files with age, gpg, or vault:

**Age encryption:**
```toml
[encryption]
    age = "age1xyz...age1key"
```

**Age with multiple recipients:**
```toml
[encryption]
    age = ["age1xyz...", "age1abc..."]
```

**GPG encryption:**
```toml
[encryption]
    gpg = "john@example.com"
```

**Or use GPG ID:**
```toml
[encryption]
    gpg = "ABCD1234"
```

### Password Manager Configuration

**1Password:**
```toml
[onepassword]
    account = "my-account.1password.com"
```

**Bitwarden:**
```toml
[bitwarden]
    # No config needed if CLI is set up
```

**Pass (password store):**
```toml
[pass]
    command = "pass"  # or "passage" for alternative
```

**Vault:**
```toml
[vault]
    address = "https://vault.example.com:8200"
    # Use VAULT_TOKEN environment variable
```

### Hook Configuration

Run scripts at specific points:

```toml[hooks]
    # Run before chezmoi apply
    [hooks.pre-apply]
        command = "system-check.sh"

    # Run after chezmoi apply
    [hooks.post-apply]
        command = "cleanup.sh"
```

### Interactive Prompting

Require user confirmation for destructive actions:

```toml
[mode]
    # Ask before overwriting files
    apply = "prompt"
```

### Umask Configuration

Set file permissions for created files:

```toml
[umask]
    # Restrict permissions (user-only)
    files = 0077  # -rw-------
    directories = 0027  # drwxr-x---
```

### CD to Source State

Change working directory when running `chezmoi cd`:

```toml
[cd]
    command = "code"
    args = ["."]
```

### Diff Configuration

How to show differences:

```toml
[diff]
    command = "diff"
    args = ["-u", "{{ .Destination }}", "{{ .Target }}"]
    pager = "less"
```

## Advanced Features

### Prompting for Values

Interactively prompt user during `chezmoi init` or `chezmoi apply`:

**Prompt for string:**
```toml
[data]
    name = "{{ promptString \"your name\" }}"
    email = "{{ promptString \"your email\" }}"
```

**Prompt with default:**
```toml
[data]
    editor = "{{ promptString \"favorite editor\" \"vim\" }}"
```

**Prompt for choice:**
```toml
{{- $editor := promptChoice "favorite editor" ["vim" "neovim" "emacs"] -}}
[data]
    editor = {{ $editor }}
```

**Prompt for confirmation:**
```toml
{{- if promptBool "enable work config?" -}}
[data]
    work_enabled = true
    work_email = "{{ promptString \"work email\" }}"
{{ end }}
```

**Prompt from template:**
```toml
{{- $name := promptStringOnce . "name" "your name" -}}
[data]
    name = {{ $name }}
```

### Conditional Configuration

Include different configs based on conditions:

**.chezmoi.toml.tmpl:**
```toml
{{- if eq .chezmoi.os "darwin" }}
[data]
    homebrew_prefix = "/opt/homebrew"
    package_manager = "brew"
{{ else if eq .chezmoi.os "linux" }}
[data]
    package_manager = "apt"
{{ end }}

{{- if eq .chezmoi.hostname "work-laptop" }}
[data]
    work_mode = true
{{ end }}
```

### Variable Expansion

Use environment variables and other data:

```toml
[data]
    # From environment variable
    github_token = "{{ .chezmoi.env.GITHUB_TOKEN }}"

    # Path expansion
    config_dir = "{{ .chezmoi.homeDir }}/.config"

    # Custom data in .chezmoidata
    theme = "{{ .theme.name }}"
```

### Multiple Configuration Files

 chezmoi merges configs from multiple files:

1. `.chezmoidata.$FORMAT` files (in source state)
2. `data` section in config files
3. Later sources override earlier ones

**.chezmoidata/packages.yaml:**
```yaml
packages:
  darwin:
    - git
    - vim
```

**.chezmoidata/work.yaml:**
```yaml
work:
  email: "john@work.com"
```

**chezmoi.toml:**
```toml
[data]
    name = "John Doe"
```

Result: All data available in templates (later sources override).

## Complete Configuration Examples

### Developer Workstation

**.chezmoi.toml.tmpl:**
```toml
{{- $email := promptChoice "email type" ["personal" "work"] -}}
{{- $editor := promptChoice "editor" ["vim" "neovim" "vscode"] -}}
{{- $shell := promptChoice "shell" ["zsh" "bash" "fish"] -}}

[data]
    name = "{{ promptString "your name" }}"
    email = {{ if eq $email "work" -}}
        "{{ promptString "work email" }}"
    {{- else -}}
        "{{ promptString "personal email" }}"
    {{- end }}
    editor = {{ $editor }}
    shell = {{ $shell }}

    {{ if eq .chezmoi.os "darwin" -}}
    homebrew_prefix = "/opt/homebrew"
    {{ end -}}

[encryption]
    age = "{{ promptString "your age public key" }}"

[merge]
    command = "nvim"
    args = ["-d", "{{ .Destination }}", "{{ .Source }}", "{{ .Target }}"]

{{ if promptBool "enable work config?" -}}
[data.work]
    enabled = true
    vpn_server = "{{ promptString "VPN server" }}"
{{ end }}
```

### Minimal Configuration

**chezmoi.toml:**
```toml
[data]
    name = "John Doe"
    email = "john@example.com"

[merge]
    command = "vimdiff"
```

### Team/Shared Configuration

**.chezmoi.toml.tmpl:**
```toml
{{- $username := promptString "username" -}}
[data]
    username = {{ $username }}

{{- if eq $username "alice" -}}
[data]
    email = "alice@example.com"
    role = "admin"
{{ else if eq $username "bob" -}}
[data]
    email = "bob@example.com"
    role = "developer"
{{ end }}

{{ if eq .chezmoi.os "darwin" -}}
[merge]
    command = "opendiff"
{{ else -}}
[merge]
    command = "vimdiff"
{{ end }}
```

## Best Practices

1. **Use `.chezmoi.toml.tmpl`** for version-controlled config
2. **Keep secrets encrypted** - Use password managers or encryption
3. **Prompt for user-specific data** - Don't hardcode personal info
4. **Organize `.chezmoidata`** - Separate concerns into multiple files
5. **Test configs** - Use `chezmoi doctor` to verify setup
6. **Document choices** - Comment complex configuration logic
7. **Use defaults** - Provide sensible defaults in prompts
8. **Keep it simple** - Don't over-engineer configuration

## Debugging Configuration

**Check configuration:**
```bash
chezmoi doctor
```

**View all data:**
```bash
chezmoi data
```

**Test template:**
```bash
chezmoi execute-template < ~/.local/share/chezmoi/dot_zshrc.tmpl
```

**Validate config:**
```bash
chezmoi init --verbose
```
