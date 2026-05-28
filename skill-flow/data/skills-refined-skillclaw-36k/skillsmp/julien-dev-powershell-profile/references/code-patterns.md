# Code Patterns for Profile Modifications

## Add New Alias (Direct - Section 7 or 10)

```powershell
function myalias { some-command @args }
```

## Add Lazy-Loaded Function

### Step 1: Create function file

Path: `$CLI_ENV_ROOT/profile/functions/<name>.ps1`

```powershell
function Actual-MyFunction {
    param([string]$Arg1)
    # Implementation
}
```

### Step 2: Add wrapper in Section 8

```powershell
function myalias { Load-Functions "name"; Actual-MyFunction @args }
```

## Modify Claude Command (Section 10)

Current `claude` function features:
- Auto MCP config detection (`.mcp.json`)
- Permission bypass mode
- Auto-resume (`--continue` by default)
- Flags: `-n` (new session), `-r` (resume picker)

Example modification - add new flag:

```powershell
# In the claude function, add new condition:
elseif ($args -contains "-x" -or $args -contains "--example") {
    # Custom behavior
    & claude.cmd @baseArgs --some-new-flag @args
}
```

## EZA Aliases (Section 10)

```powershell
ll    # Long format with icons and git
la    # Long format + hidden files
ls    # Simple with icons
lt    # Tree view (2 levels)
lta   # Tree view + hidden
```

## Section Quick Reference

| Section | Purpose | Line Range |
|---------|---------|------------|
| 7 | Direct Functions (fcd, fe, y, yazi) | 109-201 |
| 8 | Lazy Loaded Aliases | 203-234 |
| 10 | EZA + Core Aliases + claude | 244-307 |
