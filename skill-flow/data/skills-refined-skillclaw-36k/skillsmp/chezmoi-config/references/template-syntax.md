# Chezmoi Template Syntax Reference

## Overview

Chezmoi uses Go's `text/template` syntax for creating dynamic configuration files. Template files have the `.tmpl` extension.

## Creating Template Files

### Add existing file as template
```bash
chezmoi add --template ~/.gitconfig
```

### Convert existing managed file to template
```bash
chezmoi chattr +template ~/.gitconfig
```

### Create template manually
```bash
chezmoi cd
$EDITOR dot_gitconfig.tmpl
```

## Template Variables

### Chezmoi Built-in Variables (`.chezmoi.*`)

| Variable | Description | Example |
|----------|-------------|---------|
| `.chezmoi.os` | Operating system | `linux`, `darwin`, `windows` |
| `.chezmoi.arch` | Architecture | `amd64`, `arm64` |
| `.chezmoi.hostname` | Machine hostname | `my-laptop` |
| `.chezmoi.username` | Current user | `john` |
| `.chezmoi.homeDir` | Home directory path | `/home/john` |
| `.chezmoi.sourceDir` | Source state directory | `/home/john/.local/share/chezmoi` |
| `.chezmoi.version` | Chezmoi version | `v2.0.0` |
| `.chezmoi.kernel.version` | Kernel version | `Linux info: 6.1.0` |

### Custom Data Variables

Custom variables are defined in:
1. `.chezmoidata.$FORMAT` files (JSON, JSONC, TOML, YAML)
2. `data` section in `.chezmoi.toml` or `chezmoi.toml`

Example in `chezmoi.toml`:
```toml
[data]
    name = "John Doe"
    email = "john@example.com"
    editor = "vim"
```

Usage in template:
```go
{{ .name }}
{{ .email }}
{{ .editor }}
```

## Template Syntax Examples

### Conditionals

**Operating system detection:**
```go
{{- if eq .chezmoi.os "darwin" }}
[credential]
    helper = osxkeychain
{{- else if eq .chezmoi.os "linux" }}
[credential]
    helper = cache
{{- end }}
```

**Architecture detection:**
```go
{{- if eq .chezmoi.arch "arm64" }}
# ARM64 specific configuration
{{- end }}
```

**Custom data conditions:**
```go
{{- if .work }}
# Work-specific configuration
{{- end }}
```

### Loops

**Iterate over package lists:**
```go
{{ range .packages.darwin.brews -}}
brew {{ . | quote }}
{{ end -}}
```

**Iterate with index:**
```go
{{ range $index, $value := .servers -}}
server {{ $index }} {{ $value }}
{{ end -}}
```

### String Manipulation

**Trim whitespace:**
```go
{{- "content" -}}  # Trim leading and trailing whitespace
```

**Quote strings:**
```go
{{ .package | quote }}  # Add quotes
```

**Print and format:**
```go
{{ printf "User: %s" .name }}
```

### Comparison Operators

- `eq` - equal (`{{ eq .chezmoi.os "linux" }}`)
- `ne` - not equal
- `lt` - less than
- `le` - less than or equal
- `gt` - greater than
- `ge` - greater than or equal
- `and` - logical AND
- `or` - logical OR
- `not` - logical NOT

## Complete Template Example

**dot_gitconfig.tmpl:**
```go
[user]
    name = {{ .name }}
    email = {{ .email }}
{{- if .chezmoi.githubToken }}
    githubToken = {{ .chezmoi.githubToken }}
{{- end }}

[core]
    editor = {{ .editor | default "vim" }}
    excludesFile = {{ .chezmoi.homeDir }}/.gitignore_global

{{- if eq .chezmoi.os "darwin" }}
[credential]
    helper = osxkeychain
{{- else if eq .chezmoi.os "linux" }}
[credential]
    helper = cache
{{- end }}

{{- if .work }}
[work]
    enabled = true
{{- end }}
```

## Template Functions

Chezmoi provides many template functions for:
- **Password managers**: `onepassword`, `bitwarden`, `lastpass`, `keepassxc`, `pass`, `vault`, `gopass`, etc.
- **Environment variables**: `env`, `lookPath`
- **File operations**: `stat`, `include`
- **String operations**: `trim`, `replace`, `split`, `join`
- **Path operations**: `joinPath`

See [password-managers.md](password-managers.md) for password manager integrations.

## Best Practices

1. **Use `{{-` and `-}}`** to control whitespace
2. **Quote user data** with `| quote` to prevent injection
3. **Use `.chezmoi.os`** for cross-platform configs
4. **Store secrets** in password managers, not templates
5. **Use `.chezmoi.homeDir`** instead of hardcoding paths
