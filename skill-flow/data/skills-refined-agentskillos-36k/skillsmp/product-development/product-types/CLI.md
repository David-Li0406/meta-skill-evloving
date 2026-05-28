# CLI Tools

Specific guidance for building command-line interfaces and developer tools.

## Product Requirements Focus

### Typical Personas
- **Developer**: Uses CLI for daily workflows
- **DevOps/SRE**: Uses CLI for automation and scripting
- **Power User**: Needs advanced features and customization
- **Newcomer**: First-time user needing clear guidance

### Key Questions to Ask
1. Is this tool interactive or primarily for scripting?
2. What shells/environments must be supported?
3. Should output be parseable (JSON) or human-friendly?
4. What's the expected frequency of use?
5. Are there existing tools users expect consistency with?

### CLI-Specific User Stories

```markdown
**As a** developer
**I expect to** quickly learn commands through help text
**So that** I don't need to reference external documentation

**As a** DevOps engineer
**I expect to** pipe output to other tools
**So that** I can integrate into existing workflows

**As a** first-time user
**I expect to** see examples for every command
**So that** I understand the expected usage

**As a** scripter
**I expect to** get machine-readable output (JSON)
**So that** I can parse results reliably
```

## Design Principles

### CLI Design Best Practices

1. **Consistency**: Follow established conventions (POSIX, GNU)
2. **Discoverability**: Good help text, examples, tab completion
3. **Scriptability**: Exit codes, machine-readable output
4. **Forgiveness**: Confirm destructive actions, undo where possible
5. **Speed**: Fast startup, minimal dependencies
6. **Quiet by Default**: Only output what's needed

### Command Structure Pattern

```
program [global-flags] command [subcommand] [flags] [arguments]

Examples:
git commit -m "message"
kubectl get pods -n namespace
docker run -it ubuntu bash
```

### Exit Code Standards

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Operation completed |
| 1 | General error | Unspecified failure |
| 2 | Usage error | Invalid arguments |
| 3 | Data error | Invalid input format |
| 64-78 | BSD sysexits.h | Various specific errors |
| 126 | Not executable | Permission denied |
| 127 | Not found | Command not found |
| 128+N | Signal N | Killed by signal |

## Interface Contracts

### Command Contract Template

```markdown
## command-name subcommand

### Synopsis
```
program subcommand [flags] <required-arg> [optional-arg]
```

### Description
One paragraph description of what the command does.

### Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| required-arg | Yes | Description of required argument |
| optional-arg | No | Description with [default] |

### Flags
| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| --flag-name | -f | string | "" | Description |
| --verbose | -v | bool | false | Verbose output |
| --output | -o | string | text | Output format |

### Examples
```bash
# Basic usage
program subcommand my-arg

# With flags
program subcommand -v --output json my-arg

# Common workflow
program subcommand my-arg | jq '.field'
```

### Exit Codes
| Code | Condition |
|------|-----------|
| 0 | Success |
| 1 | Error description |
```

### Output Format Standards

**Human-readable (default)**:
```
Resource "my-resource" created successfully.

ID:      abc-123
Name:    my-resource
Status:  active
Created: 2024-01-15T10:30:00Z
```

**JSON (--output json)**:
```json
{
  "id": "abc-123",
  "name": "my-resource",
  "status": "active",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**Table (--output table)**:
```
ID        NAME          STATUS   CREATED
abc-123   my-resource   active   2024-01-15
def-456   other-res     pending  2024-01-14
```

**Quiet (--quiet)**:
```
abc-123
```

## Architecture Patterns

### CLI Application Structure

```
cli/
├── cmd/
│   └── root.go              # Root command, global flags
│   └── create.go            # create subcommand
│   └── list.go              # list subcommand
│   └── delete.go            # delete subcommand
├── internal/
│   ├── config/
│   │   └── config.go        # Configuration loading
│   ├── client/
│   │   └── api.go           # API client (if applicable)
│   ├── output/
│   │   ├── formatter.go     # Output formatting
│   │   └── table.go         # Table rendering
│   └── prompt/
│       └── confirm.go       # Interactive prompts
├── pkg/                     # Reusable packages
├── completions/             # Shell completions
│   ├── bash.go
│   ├── zsh.go
│   └── fish.go
├── main.go                  # Entry point
├── go.mod
└── Makefile
```

### Configuration Hierarchy

```
Priority (highest to lowest):
1. Command-line flags
2. Environment variables
3. Local config file (./.app.yaml)
4. User config file (~/.config/app/config.yaml)
5. System config file (/etc/app/config.yaml)
6. Default values
```

### Command Implementation Pattern

```go
// Using cobra (Go)
var createCmd = &cobra.Command{
    Use:   "create <name>",
    Short: "Create a new resource",
    Long:  `Create a new resource with the specified name...`,
    Example: `
  # Create a basic resource
  app create my-resource

  # Create with options
  app create my-resource --description "My description"`,
    Args: cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        description, _ := cmd.Flags().GetString("description")

        // Get output format from persistent flag
        outputFormat, _ := cmd.Flags().GetString("output")

        result, err := client.Create(name, description)
        if err != nil {
            return fmt.Errorf("failed to create: %w", err)
        }

        return output.Print(result, outputFormat)
    },
}

func init() {
    rootCmd.AddCommand(createCmd)
    createCmd.Flags().StringP("description", "d", "", "Resource description")
}
```

## Testing Strategy

### CLI Test Categories

**Unit Tests**: Test individual functions
```go
func TestParseArgs(t *testing.T) {
    args := []string{"--name", "test", "--count", "5"}
    config, err := parseArgs(args)

    assert.NoError(t, err)
    assert.Equal(t, "test", config.Name)
    assert.Equal(t, 5, config.Count)
}
```

**Integration Tests**: Test command execution
```go
func TestCreateCommand(t *testing.T) {
    // Setup mock server
    server := httptest.NewServer(mockHandler)
    defer server.Close()

    // Execute command
    cmd := exec.Command("./app", "create", "test-resource")
    cmd.Env = append(os.Environ(), "APP_API_URL="+server.URL)

    output, err := cmd.CombinedOutput()

    assert.NoError(t, err)
    assert.Contains(t, string(output), "created successfully")
}
```

**Golden Tests**: Test output format
```go
func TestListOutput(t *testing.T) {
    output := captureOutput(func() {
        listCmd.Run(nil, []string{})
    })

    golden := filepath.Join("testdata", "list.golden")
    if *update {
        os.WriteFile(golden, []byte(output), 0644)
    }

    expected, _ := os.ReadFile(golden)
    assert.Equal(t, string(expected), output)
}
```

### Testing Interactive Features

```go
func TestConfirmPrompt(t *testing.T) {
    // Simulate user input
    input := strings.NewReader("y\n")

    confirmed := prompt.Confirm("Delete resource?", input, os.Stdout)

    assert.True(t, confirmed)
}
```

## User Experience Features

### Help Text Best Practices

```
Usage:
  app command [flags] <required> [optional]

Description:
  Brief description of what the command does.

Arguments:
  required    Description of required argument
  optional    Description of optional argument (default: value)

Flags:
  -h, --help          Show this help message
  -v, --verbose       Enable verbose output
  -o, --output TYPE   Output format: text, json, yaml (default: text)

Examples:
  # Basic usage
  app command my-arg

  # Common workflow
  app command my-arg | jq '.field'

See also:
  app help other-command
```

### Progress Indicators

```go
// Spinner for indeterminate progress
spinner := NewSpinner("Processing...")
spinner.Start()
defer spinner.Stop()
doWork()

// Progress bar for known progress
bar := NewProgressBar(total)
for i := 0; i < total; i++ {
    doItem(i)
    bar.Increment()
}
bar.Finish()
```

### Color and Formatting

```go
// Use colors judiciously, respect NO_COLOR
func colorize(text, color string) string {
    if os.Getenv("NO_COLOR") != "" || !isTerminal() {
        return text
    }
    return color + text + Reset
}

// Standard color conventions
Green  = Success, additions
Red    = Errors, deletions
Yellow = Warnings
Blue   = Information
Bold   = Headers, emphasis
```

### Tab Completion

```bash
# Bash completion
_app_completions() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "create list delete help" -- "$cur"))
}
complete -F _app_completions app
```

## Common Pitfalls to Avoid

1. **Inconsistent Flags**: Same meaning should use same flag across commands
2. **Missing --help**: Every command needs help text
3. **Slow Startup**: Defer expensive initialization
4. **No Exit Codes**: Scripts need meaningful exit codes
5. **stdout vs stderr**: Use stderr for progress/errors, stdout for data
6. **No Quiet Mode**: Scripts need clean output
7. **Missing Examples**: Examples are often the best documentation
8. **Ignoring NO_COLOR**: Respect user preferences
9. **Long Running with No Progress**: Show something is happening
10. **Destructive Without Confirm**: Always confirm deletes/overwrites

## Distribution Considerations

### Cross-Platform Builds

```makefile
# Makefile
PLATFORMS := linux/amd64 linux/arm64 darwin/amd64 darwin/arm64 windows/amd64

build-all:
	@for platform in $(PLATFORMS); do \
		GOOS=$${platform%/*} GOARCH=$${platform#*/} \
		go build -o dist/app-$${platform%/*}-$${platform#*/} .; \
	done
```

### Installation Methods

```bash
# Homebrew (macOS/Linux)
brew install myapp

# Go install
go install github.com/user/myapp@latest

# Direct download
curl -sSL https://get.myapp.com | sh

# Package managers
apt install myapp      # Debian/Ubuntu
dnf install myapp      # Fedora
```

### Auto-Update Mechanism

```go
func checkForUpdates() {
    latest, err := getLatestVersion()
    if err != nil || latest == currentVersion {
        return
    }

    fmt.Fprintf(os.Stderr,
        "A new version (%s) is available. Run 'app update' to upgrade.\n",
        latest)
}
```
