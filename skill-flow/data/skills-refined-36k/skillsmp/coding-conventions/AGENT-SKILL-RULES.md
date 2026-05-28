# Agent Skill Development Rules

Rules for building proper agent skills that integrate external tools, MCP servers, or system capabilities.

## 1. Research First

Before writing any skill documentation:

1. **Understand the technology** - How does it actually work?
2. **Verify compatibility** - Does it work with the target agent (Windsurf/Cascade)?
3. **Identify dependencies** - What must be installed? What versions?
4. **Find known issues** - Check GitHub issues, forums, community reports
5. **Test manually first** - Run commands yourself before documenting them

**Document your research** in an INFO document or the skill's SKILL.md.

## 2. Skill File Structure

### Required Files

- **`SKILL.md`** - Main skill documentation (see Section 2.1 for required content)

### Conditional Files

- **`SETUP.md`** - Required if software must be installed or configured
- **`UNINSTALL.md`** - Required if SETUP.md exists

### Optional Files

- Supporting documentation, templates, examples

### 2.1 SKILL.md Required Content

SKILL.md MUST contain sufficient technical detail for the agent to understand and use the skill correctly:

**Required sections:**

1. **Frontmatter** - `name` and `description` fields
2. **When to Use / When NOT to Use** - Clear guidance on applicability
3. **Architecture** - How components connect (diagram preferred)
4. **Technical Details** - How the underlying technology works
5. **Capabilities** - What the skill enables
6. **Limitations** - What it cannot do, known issues
7. **Sources** - Links to official documentation, repositories, research

**Technical depth requirements:**

- **Tool actions/API** - List all available actions with parameters
- **Dependencies** - What libraries/tools are used under the hood
- **Platform specifics** - OS-specific behavior (Windows, macOS, Linux)
- **Model requirements** - Which AI models work best (if applicable)
- **Execution flow** - How the tool operates step-by-step

**Example: Insufficient vs Sufficient**

```markdown
# BAD: Too vague
## Capabilities
- Can control the computer
- Takes screenshots

# GOOD: Specific and actionable
## Tool Actions
- **`screenshot`** - Capture full screen, returns base64 PNG
- **`mouse_move`** - Move cursor to (x, y) coordinates
- **`left_click`** - Single left click at current position
- **`key`** - Press key combination (e.g., `ctrl+c`)
- **`type`** - Type text string character by character

## Architecture
┌─────────────────────────────────────────┐
│ Agent → MCP Protocol → Server → Library │
│                              └→ OS APIs │
└─────────────────────────────────────────┘
```

**Why this matters:** Without sufficient technical detail, the agent cannot:
- Know which tool actions are available
- Understand parameter formats
- Anticipate limitations
- Troubleshoot failures

## 3. SETUP.md Requirements

SETUP.md files MUST follow this structure:

### 3.1 Pre-Installation Verification

**Before modifying the system:**

1. Verify all prerequisites exist (Node.js, Python, etc.)
2. Test that core functionality works in isolation
3. Check current system state (existing configs, conflicts)
4. Provide expected output for each verification step

```markdown
## Pre-Installation Verification

Complete ALL verification steps before modifying your system.
If any step fails, fix it before proceeding to installation.

## 1. Verify [Prerequisite]
[commands]
Expected: [what user should see]

## 2. Test [Core Functionality]
[commands that test WITHOUT modifying system]
Expected: [what success looks like]

## Pre-Installation Checklist
- [ ] Prerequisite 1 verified
- [ ] Prerequisite 2 verified
- [ ] Core functionality tested
- [ ] System state checked

**If all checks pass, proceed to installation.**
```

### 3.2 Installation Section

Only AFTER pre-installation verification passes:

1. Backup existing configuration
2. Make minimal changes
3. Provide rollback instructions inline
4. Show expected results after each step

### 3.2.1 MCP Config Modification Pattern (Windsurf)

For skills that modify `~/.codeium/windsurf/mcp_config.json`, use this PowerShell pattern:

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

# Define target server config
$targetServer = @{
    command = "npx"
    args = @("package-name")
}

# Read existing config (handle empty/missing)
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
} else {
    $config = @{ mcpServers = @{} }
}

# Convert PSCustomObject to Hashtable if needed
if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Compare current vs target (idempotent)
if ($config.mcpServers.ContainsKey("server-name")) {
    $currentJson = $config.mcpServers["server-name"] | ConvertTo-Json -Compress
    $targetJson = $targetServer | ConvertTo-Json -Compress
    if ($currentJson -eq $targetJson) {
        Write-Host "Already configured" -ForegroundColor Green
        return
    }
}

# Backup before modifying
$backupPath = "$configPath._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configPath $backupPath -ErrorAction SilentlyContinue

# Add/update server
$config.mcpServers["server-name"] = $targetServer

# Write config
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
```

**Key requirements:**
- **Idempotent** - Running twice produces same result
- **Backup first** - Always backup before modifying
- **Handle PSCustomObject** - JSON parsing returns PSCustomObject, convert to Hashtable
- **Compare before write** - Don't modify if already correct

### 3.3 Post-Installation Verification

1. Verify installation succeeded
2. Test actual functionality
3. Document expected behavior with specific prompts
4. Provide troubleshooting for common failures

## 4. UNINSTALL.md Requirements

UNINSTALL.md files MUST follow this structure:

### 4.1 Pre-Uninstall Verification

**Before removing anything:**

1. Verify what is currently installed
2. Check for dependencies that might break
3. Identify all files/configs that will be affected
4. Confirm user wants to proceed

```markdown
## Pre-Uninstall Verification

## 1. Check Current Installation
[commands to show what's installed]
Expected: [what indicates it's installed]

## 2. Check Dependencies
[commands to identify what depends on this]
If dependencies found: [what to do]

## Pre-Uninstall Checklist
- [ ] Current installation verified
- [ ] Dependencies checked
- [ ] Backup created (if needed)

**If all checks pass, proceed to uninstall.**
```

### 4.2 Uninstall Section

1. Remove in reverse order of installation
2. Show what each step removes
3. Verify removal after each step

### 4.3 Post-Uninstall Verification

1. Confirm all components removed
2. Verify system returned to clean state
3. Note any manual cleanup needed

## 5. Test Before Writing

**Critical Rule**: Test all code snippets WITHOUT modifying the system before including them in SETUP/UNINSTALL.

### Testing Approach

1. **Read-only tests first** - Verify state without changing it
2. **Isolated tests** - Test functionality in temporary location
3. **Destructive tests last** - Only after read-only tests pass

### Example Pattern

```powershell
# GOOD: Test package works before adding to config
npx -y some-mcp-server --help  # Downloads and tests, doesn't modify Windsurf

# GOOD: Check config state before modifying
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
if (Test-Path $configPath) { Get-Content $configPath }

# BAD: Modify first, test later
Set-Content $configPath $newConfig  # Don't do this before verification
```

## 6. Documentation Quality

### Include in Every Skill

- **Compatibility notes** - What's verified vs expected to work
- **Expected output** - What user should see at each step
- **Troubleshooting** - Common errors and fixes
- **References** - Links to official docs, repos, issues

### Avoid

- Untested commands
- Vague success criteria ("it should work")
- Missing error handling
- Assumptions about user's system state

## 7. Case Study: computer-use-mcp Skill

Example of applying these rules when building the `computer-use-mcp` skill:

### 7.1 Research Phase

1. **Web search** - Found domdomegg/computer-use-mcp repository
2. **Read documentation** - GitHub README, nut.js docs, Anthropic Computer Use docs
3. **Identify compatibility gap** - Repo lists Claude Desktop, Cursor, Cline but NOT Windsurf
4. **Document finding** - Added compatibility note: "expected to work but not officially verified"

### 7.2 Initial SETUP.md (What We Did Wrong)

First version jumped straight to installation:
```markdown
## 1. Configure MCP Server
Add to config...  # BAD: No verification first
```

### 7.3 Critique and Fix

Devil's Advocate review identified:
- No pre-installation verification
- Untested assumption that it works with Windsurf
- No nut.js dependency testing
- Vague test instructions

Fixed by adding:
- **Section 1-6**: Pre-installation verification (Node.js, npx, package test, nut.js test, screenshot test, config check)
- **Pre-Installation Checklist**: All checks must pass before proceeding
- **Separator**: Clear `---` line between verification and installation
- **Section 7+**: Installation only after verification passes
- **Expected output**: Specific prompts and what success looks like

### 7.4 SKILL.md Enhancement

Initial version was minimal. Enhanced with:
- Technical architecture diagram
- All tool actions with parameters
- nut.js API examples
- Model requirements
- Execution cycle explanation
- 7 verified source links

### 7.5 Lessons Learned

1. **Research before writing** - Found compatibility gap early
2. **Test commands first** - `npx -y computer-use-mcp --help` before documenting
3. **Verify then modify** - Pre-installation checks prevent broken installs
4. **Expected output is crucial** - User knows if something went wrong
5. **Sources matter** - Link to primary documentation

## 8. Skill Review Checklist

Before publishing a skill:

- [ ] Research documented (INFO or in SKILL.md)
- [ ] SKILL.md has clear "when to use" and "when NOT to use"
- [ ] SETUP.md has pre-installation verification
- [ ] SETUP.md tests before modifying
- [ ] UNINSTALL.md exists if SETUP.md exists
- [ ] UNINSTALL.md has pre-uninstall verification
- [ ] All code snippets tested manually
- [ ] Expected output documented for each step
- [ ] Troubleshooting section covers common errors
- [ ] References link to primary sources
