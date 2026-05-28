# PowerShell Profile Structure

Full documentation of the unified CLI environment profile.

## File Location

```
C:\Users\julien\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

Source of truth linked to CLI Tools management repo:
```
C:\Users\julien\OneDrive\Coding\_Projets de code\2025.11 Command Line Tools management
```

## Global Variables

```powershell
$global:CLI_ENV_ROOT    # Path to CLI tools repo
$global:profileDir      # Path to profile/functions/
$global:LoadedFunctions # Hashtable tracking lazy-loaded functions
```

## Section Details

### Section 1: UTF-8 Encoding (Lines 24-28)

```powershell
[console]::InputEncoding = [console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [console]::OutputEncoding
```

### Section 2: Environment Variables (Lines 30-39)

```powershell
$env:EDITOR = "hx"  # Helix editor
$env:PATH_OPTIMIZED = "1"  # Prevent duplicate PATH entries
```

### Section 3: Starship Prompt (Lines 41-47)

Initializes Starship with custom config from `$CLI_ENV_ROOT/starship/starship.toml`

### Section 4: Zoxide Navigation (Lines 49-57)

Smart directory jumping with `z` command.

### Section 5: FZF Fuzzy Finder (Lines 59-91)

- Catppuccin Mocha theme
- Uses `fd` for file search
- Uses `bat` for preview
- Keybindings: Ctrl+T (files), Ctrl+R (history), Alt+C (directories)

### Section 6: Lazy Loading System (Lines 93-107)

```powershell
function Load-Functions {
    param([string]$Name)
    # Loads $profileDir/functions/$Name.ps1 on first use
}
```

### Section 7: Direct Functions (Lines 109-201)

Functions loaded immediately (frequently used):

| Function | Description |
|----------|-------------|
| `fcd` | Fuzzy cd with eza preview |
| `fe` / `ff` | Fuzzy edit with bat preview |
| `y` | Yazi file manager with golden ratio + auto-cd |
| `yazi-normal` | Yazi without golden ratio |

### Section 8: Lazy Loaded Aliases (Lines 203-234)

Wrappers that load functions on first use:

| Category | Functions |
|----------|-----------|
| Navigation | `sf`, `mtd`, `rgg` |
| System | `hibernate`, `restart-bios`, `sysinfo` |
| Utils | `gpf`, `atp`, `add-cur-to-path`, `get-apps` |
| Certificate | `new-cert`, `sign-script`, `list-certs` |
| Audio/Dell | `audio`, `switch-audio`, `list-audio`, `dell-thermal`, `thermal`, `dell-status` |

### Section 9: Help System (Lines 236-242)

Loads `Show-CliHelp.ps1` for `??` command.

### Section 10: EZA + Core Aliases (Lines 244-274)

```powershell
# EZA replacements for ls
ll    # Long format with icons and git
la    # Long format + hidden files
ls    # Simple with icons
lt    # Tree view (2 levels)
lta   # Tree view + hidden

# Utilities
which  # Alias for Get-Command
rup    # Reload profile

# Carbonyl (WSL browser)
carbonyl
```

### Section 10b: Claude Function

```powershell
function claude {
    # Auto MCP config detection (.mcp.json)
    # Permission bypass mode
    # Auto-resume by default (--continue)
    # Flags: -n (new), -r (resume picker)
}
```

### Section 11: VSCode Integration (Lines ~280+)

Shell integration for VSCode terminal.

## Adding New Functions

### Direct Function (Always Loaded)

Add in Section 7:
```powershell
function MyFunction {
    param([string]$Arg1)
    # Implementation
}
```

### Lazy-Loaded Function

1. Create `$CLI_ENV_ROOT/profile/functions/mymodule.ps1`:
```powershell
function Actual-MyFunction {
    param([string]$Arg1)
    # Implementation
}
```

2. Add wrapper in Section 8:
```powershell
function myalias { Load-Functions "mymodule"; Actual-MyFunction @args }
```

## Testing Changes

```powershell
# Reload profile without restarting terminal
rup

# Or manually
. $PROFILE
```
