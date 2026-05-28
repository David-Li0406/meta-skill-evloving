---
name: cli-onboarding
description: "Production-ready first-time user experience patterns for CLI tools including setup wizards, first-run detection, doctor/diagnostic commands, actionable error messages, edge case handling, and update notifications. When building CLI packages that need: (1) Interactive setup commands, (2) Configuration validation, (3) Onboarding flows for new users, (4) Publishing preparation, or any CLI UX improvements"
---

# CLI Onboarding & First-Time User Experience

Implement production-ready first-time user experience for CLI packages. Use when the user asks to add setup wizards, improve onboarding, handle edge cases, or prepare a CLI for publication.

## When to Use

- User asks for "first-time user experience", "onboarding", or "setup wizard"
- User wants to "prepare for publishing" a CLI package
- User mentions "edge cases" for CLI tools
- User asks to add a "doctor" or diagnostic command
- User wants to improve error messages for new users

## Core Patterns to Implement

### 1. Interactive Setup Wizard (`<tool> setup`)

Create a guided setup command that:

```
<tool> setup

Welcome to <tool>! Let's get you set up.

📋 Step 1: <First requirement>
   [Guidance text]
   [Open browser/show URL if needed]

📁 Step 2: <Configuration step>
   [Prompt for input with validation]

🔐 Step 3: <Authentication/final step>
   [Complete setup]

🎉 You're all set! Try: <tool> <main-command>
```

**Key behaviors:**
- Open browser automatically for external services (use `open` package in Node, `webbrowser` in Python)
- Validate input immediately and loop on errors
- Support `~` path expansion
- Handle drag-drop file paths (strip quotes)
- Provide sensible defaults
- Show clear success message with next steps

### 2. First-Run Detection

When user runs the tool with no arguments:

```javascript
// Node.js pattern
if (process.argv.length === 2) {
  if (!isConfigured()) {
    console.log('Welcome to <tool>!');
    console.log('Run `<tool> setup` to get started.');
    return;
  }
}
```

```python
# Python pattern
if len(sys.argv) == 1:
    if not is_configured():
        print("Welcome to <tool>!")
        print("Run `<tool> setup` to get started.")
        return
```

### 3. Doctor/Diagnostic Command (`<tool> doctor`)

For tools with complex dependencies:

```
<tool> doctor

Checking system requirements...

✓ Node.js >= 18
✓ ffmpeg installed (version 7.1)
✗ API token missing

To fix: Run `<tool> setup` or set <ENV_VAR>
```

**Check for:**
- Runtime version requirements
- System dependencies (ffmpeg, git, etc.)
- API keys/tokens
- Configuration files
- Network connectivity (if applicable)

### 4. Credentials/Config Validation

Validate configuration files before use:

```javascript
// Node.js
function validateConfig(filePath) {
  if (!fs.existsSync(filePath)) {
    return { valid: false, error: 'File not found' };
  }
  try {
    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (!content.requiredField) {
      return { valid: false, error: 'Missing required field' };
    }
    return { valid: true };
  } catch (err) {
    return { valid: false, error: `Invalid JSON: ${err.message}` };
  }
}
```

```python
# Python
def validate_config(file_path: Path) -> tuple[bool, str | None]:
    if not file_path.exists():
        return False, "File not found"
    try:
        config = json.loads(file_path.read_text())
        if "required_field" not in config:
            return False, "Missing required field"
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
```

### 5. Actionable Error Messages

Transform errors into guidance:

```
❌ BAD:  "Error: ENOENT credentials.json"
✅ GOOD: "credentials.json not found at ~/.config/tool/

Run 'tool setup' to configure, or manually:
1. Go to https://console.example.com/
2. Create credentials
3. Save to ~/.config/tool/credentials.json"
```

### 6. Edge Cases to Handle

| Edge Case | Solution |
|-----------|----------|
| Ctrl+C during setup | SIGINT handler with clean exit message |
| Empty input | Provide sensible default |
| Path with spaces | Use proper quoting/escaping |
| Drag-drop paths | Strip quotes: `input.replace(/['"]/g, '')` |
| `~` in paths | Expand to home directory |
| Unknown command | Show help suggestion |
| Platform-specific features | Check platform, show alternatives |
| Missing dependencies | List what's missing with install commands |
| Network failures | Graceful error with retry suggestion |
| Already configured | Ask before overwriting |
| Outdated version | Use update-notifier to alert users |

### 7. Update Notifier

Alert users when a newer version is available:

```javascript
// Node.js - using update-notifier package
const updateNotifier = require('update-notifier');
const pkg = require('./package.json');

// Check for updates (non-blocking, cached)
updateNotifier({ pkg }).notify();
```

```python
# Python - using packaging and httpx (or requests)
import httpx
from importlib.metadata import version
from packaging.version import parse

def check_for_updates(package_name: str) -> None:
    """Check PyPI for newer version and notify user."""
    try:
        current = version(package_name)
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
        latest = response.json()["info"]["version"]
        
        if parse(latest) > parse(current):
            print(f"\n┌{'─' * 44}┐")
            print(f"│  Update available {current} → {latest}".ljust(45) + "│")
            print(f"│  Run: pip install --upgrade {package_name}".ljust(45) + "│")
            print(f"└{'─' * 44}┘\n")
    except Exception:
        pass  # Silently fail - don't block CLI usage

# Call early in main()
check_for_updates("tool-name")
```

This displays (only when update available):
```
┌────────────────────────────────────────────┐
│                                            │
│   Update available 1.0.5 → 1.0.7           │
│   Run npm install -g tool-name to update   │
│                                            │
└────────────────────────────────────────────┘
```

**Key behaviors:**
- Non-blocking: check happens quickly with timeout
- Cached: Node.js version caches (1 day default); Python can use file-based cache
- Unobtrusive: only shows message when update exists
- Fails silently: never breaks CLI if network unavailable

**Installation:**
```bash
# Node.js
npm install update-notifier

# Python
pip install packaging httpx
```

### 8. Platform Detection

```javascript
// Node.js - for platform-specific features
if (process.platform !== 'darwin') {
  console.log('This feature is macOS-only.');
  console.log('Alternative for your platform:');
  console.log('  crontab -e');
  console.log('  */5 * * * * /path/to/tool check');
  return;
}
```

```python
# Python
import platform
if platform.system() != 'Darwin':
    print("This feature is macOS-only.")
    print("Alternative: Use cron or systemd")
    return
```

### 9. Configuration Location Standards

| Platform | Location |
|----------|----------|
| macOS/Linux | `~/.config/<tool>/` |
| Windows | `%APPDATA%\<tool>\` |
| XDG-compliant | `$XDG_CONFIG_HOME/<tool>/` |

Always allow override via environment variable:
```
TOOL_CONFIG_DIR=/custom/path tool setup
```

## Package Metadata Checklist

Before publishing, ensure:

### Node.js (package.json)
```json
{
  "name": "tool-name",
  "version": "1.0.0",
  "description": "Clear one-line description",
  "bin": { "tool": "src/cli.js" },
  "engines": { "node": ">=18" },
  "repository": { "type": "git", "url": "..." },
  "bugs": { "url": ".../issues" },
  "homepage": "...#readme",
  "license": "MIT"
}
```

### Python (pyproject.toml)
```toml
[project]
name = "tool-name"
version = "1.0.0"
description = "Clear one-line description"
requires-python = ">=3.10"
license = { text = "MIT" }

[project.scripts]
tool = "tool.cli:main"
tool-doctor = "tool.cli:doctor"

[project.urls]
Homepage = "..."
Issues = ".../issues"
```

### Required Files
- `LICENSE` - Full license text
- `README.md` - With Quick Start section
- `.gitignore` - Exclude secrets, build artifacts

## Testing Setup Functionality

Test validation logic separately from interactive prompts:

```javascript
// tests/setup.test.js
describe('validateConfig', () => {
  it('returns error for missing file', () => {
    const result = validateConfig('/nonexistent');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('File not found');
  });

  it('returns error for invalid JSON', () => {
    // Create temp file with bad content
    // ...
  });
});
```

Use temp directories for file operations:
```javascript
const TEST_DIR = path.join(os.tmpdir(), 'tool-test-' + Date.now());
beforeEach(() => fs.mkdirSync(TEST_DIR, { recursive: true }));
afterEach(() => fs.rmSync(TEST_DIR, { recursive: true, force: true }));
```

## Implementation Order

1. **Add config validation helpers** - Pure functions, easy to test
2. **Update error messages** - Point to setup command
3. **Create `setup` command** - Interactive wizard
4. **Add first-run detection** - Welcome message when unconfigured
5. **Add `doctor` command** - If complex dependencies exist
6. **Handle edge cases** - SIGINT, paths, platform
7. **Add update-notifier** - Alert users of new versions
8. **Update README** - Setup as primary quick start
9. **Add tests** - Cover validation and edge cases
10. **Verify package metadata** - All fields present
11. **Create LICENSE file** - If missing

## Example Implementations

- **Node.js**: See `inboxd` repo - `inbox setup` command
- **Python**: See `VoxScriber` repo - `voxscriber-doctor` command
