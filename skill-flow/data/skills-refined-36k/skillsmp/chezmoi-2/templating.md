# Templating

Chezmoi uses Go's `text/template` for dynamic configuration.

## Syntax Basics

```text
{{ .chezmoi.os }}                      # Variable access
{{ .email | quote }}                   # Pipe to function

{{ if eq .chezmoi.os "darwin" }}       # Conditional
# macOS config
{{ else if eq .chezmoi.os "linux" }}
# Linux config
{{ end }}

{{- .variable -}}                      # Trim whitespace (- on either side)

{{ range .items }}                     # Loop
{{ . }}
{{ end }}
```

## Template Variables

### System Information

| Variable | Description |
|----------|-------------|
| `.chezmoi.os` | Operating system: `darwin`, `linux`, `windows` |
| `.chezmoi.arch` | Architecture: `amd64`, `arm64`, `arm` |
| `.chezmoi.hostname` | Hostname (up to first `.`) |
| `.chezmoi.fqdnHostname` | Fully-qualified hostname |
| `.chezmoi.kernel.osrelease` | Kernel release (Linux) |

### User Information

| Variable | Description |
|----------|-------------|
| `.chezmoi.username` | Current username |
| `.chezmoi.homeDir` | Home directory path |
| `.chezmoi.uid` | User ID |
| `.chezmoi.gid` | Primary group ID |

### Paths

| Variable | Description |
|----------|-------------|
| `.chezmoi.sourceDir` | Source directory path |
| `.chezmoi.sourceFile` | Current template's source path |
| `.chezmoi.targetFile` | Target file path |
| `.chezmoi.executable` | Path to chezmoi binary |

### Linux-Specific (from /etc/os-release)

| Variable | Description |
|----------|-------------|
| `.chezmoi.osRelease.id` | Distribution ID: `ubuntu`, `fedora`, `arch` |
| `.chezmoi.osRelease.idLike` | Similar distributions |
| `.chezmoi.osRelease.versionID` | Version number |
| `.chezmoi.osRelease.versionCodename` | Version codename |

## Common Template Functions

```text
{{ .value | quote }}                   # Quote string for TOML/YAML
{{ .path | joinPath .chezmoi.homeDir }}  # Join paths
{{ "string" | lower }}                 # Lowercase
{{ "string" | upper }}                 # Uppercase
{{ "string" | trim }}                  # Trim whitespace
{{ lookPath "brew" }}                  # Find executable in PATH
{{ stat "/path/to/file" }}             # Get file info (or false)
{{ output "command" "arg" }}           # Run command, get output
{{ include "filename" }}               # Include file contents
{{ includeTemplate "name.tmpl" . }}    # Include and execute template
```

## Data Format Functions

```text
{{ .data | toJson }}                   # Serialize to JSON
{{ .data | toYaml }}                   # Serialize to YAML
{{ .data | toToml }}                   # Serialize to TOML
{{ .jsonStr | fromJson }}              # Parse JSON
{{ .yamlStr | fromYaml }}              # Parse YAML
```

## OS Detection Patterns

```text
{{- if eq .chezmoi.os "darwin" -}}
# macOS-specific configuration
export HOMEBREW_PREFIX="/opt/homebrew"
{{- else if eq .chezmoi.os "linux" -}}
# Linux-specific configuration
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{- end -}}
```

## Architecture Detection

```text
{{- if eq .chezmoi.arch "arm64" -}}
# Apple Silicon / ARM64
{{- else if eq .chezmoi.arch "amd64" -}}
# Intel / AMD64
{{- end -}}
```

## Hostname-Based Configuration

```text
{{- if eq .chezmoi.hostname "work-laptop" -}}
# Work-specific settings
{{- end -}}
```

## Linux Distribution Detection

```text
{{- if eq .chezmoi.osRelease.id "ubuntu" -}}
# Ubuntu-specific
{{- else if eq .chezmoi.osRelease.id "fedora" -}}
# Fedora-specific
{{- else if eq .chezmoi.osRelease.id "arch" -}}
# Arch-specific
{{- end -}}
```

## Custom Data Variables

Define in `~/.config/chezmoi/chezmoi.toml`:

```toml
[data]
    isWork = true
    email = "work@company.com"
    editor = "nvim"
```

Use in templates:

```text
{{- if .isWork -}}
# Work configuration
{{- end -}}
git config --global user.email {{ .email | quote }}
```

## Conditional File Inclusion

Use different source files per OS with `include`:

```text
# dot_bashrc.tmpl
{{- if eq .chezmoi.os "darwin" -}}
{{- include "dot_bashrc_darwin" -}}
{{- else if eq .chezmoi.os "linux" -}}
{{- include "dot_bashrc_linux" -}}
{{- end -}}
```

## Config File Template (.chezmoi.toml.tmpl)

Create for interactive setup during `chezmoi init`:

```toml
{{- $email := promptStringOnce . "email" "Email address" -}}
{{- $name := promptStringOnce . "name" "Full name" -}}
{{- $isWork := promptBoolOnce . "isWork" "Is this a work machine" -}}

[data]
    email = {{ $email | quote }}
    name = {{ $name | quote }}
    isWork = {{ $isWork }}

{{- if eq .chezmoi.os "darwin" }}

[edit]
    command = "code"
    args = ["--wait"]
{{- end }}
```

### Init Functions

| Function | Purpose |
|----------|---------|
| `promptString "prompt" ["default"]` | Prompt for string |
| `promptStringOnce .data "key" "prompt" ["default"]` | Prompt if not already set |
| `promptBool "prompt" [default]` | Prompt for yes/no |
| `promptBoolOnce .data "key" "prompt" [default]` | Prompt if not already set |
| `promptInt "prompt" [default]` | Prompt for integer |
| `promptChoice ["opt1" "opt2"] ["default"]` | Prompt to select one |
| `stdinIsATTY` | Check if running interactively |
| `writeToStdout "message"` | Print message during init |

## Testing Templates

```bash
chezmoi execute-template '{{ .chezmoi.hostname }}'
chezmoi execute-template < ~/.local/share/chezmoi/home/dot_bashrc.tmpl
chezmoi cat ~/.bashrc                  # See rendered output
chezmoi diff                           # Compare rendered vs current
chezmoi data                           # View all available variables
```
