# Pattern 1: The Doctor (Health)

> *"The best error message is the one that never shows up."* — Thomas Fuchs

**Problem**: Users install your tool, run it, and get cryptic errors because dependencies are missing, environment variables aren't set, or permissions are wrong.

**Solution**: Verify all preconditions upfront, before any work begins. Provide a `doctor` command that diagnoses and suggests fixes.

---

## Concept

The Doctor pattern ensures your tool can answer: **"Is my environment ready to run this?"**

A good doctor:
1. Checks all external dependencies
2. Reports what's missing with actionable fixes
3. Caches expensive checks
4. Runs automatically on first use

---

## Decision Tree

```
Does your tool have external dependencies?
├─ No → Skip this pattern
└─ Yes → Implement doctor
    │
    ├─ How critical is setup?
    │   ├─ Critical (won't work without) → Block on failure
    │   └─ Optional (degrades gracefully) → Warn, don't block
    │
    └─ How expensive are checks?
        ├─ Fast (< 100ms) → Check every run
        └─ Slow (API calls, disk) → Cache results
```

---

## Implementation

### Python CLI

```python
import shutil
import sys
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class CheckResult:
    ok: bool
    message: str
    fix_command: Optional[str] = None

def check_binary(name: str, min_version: Optional[str] = None) -> CheckResult:
    """Check if a binary exists and meets version requirements."""
    path = shutil.which(name)
    if not path:
        return CheckResult(
            ok=False,
            message=f"{name} not found in PATH",
            fix_command=f"brew install {name}  # or apt-get install {name}"
        )
    # Version check logic here if min_version provided
    return CheckResult(ok=True, message=f"{name} found at {path}")

def check_env_var(name: str) -> CheckResult:
    """Check if an environment variable is set."""
    value = os.environ.get(name)
    if not value:
        return CheckResult(
            ok=False,
            message=f"Environment variable {name} not set",
            fix_command=f"export {name}=<your-value>"
        )
    return CheckResult(ok=True, message=f"{name} is set")

def check_writable(path: str) -> CheckResult:
    """Check if a path is writable."""
    if not os.path.exists(path):
        return CheckResult(
            ok=False,
            message=f"Directory {path} does not exist",
            fix_command=f"mkdir -p {path}"
        )
    if not os.access(path, os.W_OK):
        return CheckResult(
            ok=False,
            message=f"Directory {path} is not writable",
            fix_command=f"chmod u+w {path}"
        )
    return CheckResult(ok=True, message=f"{path} is writable")

def doctor():
    """Run all health checks and report results."""
    checks = [
        ("ffmpeg", check_binary("ffmpeg", min_version="4.0")),
        ("API_KEY", check_env_var("API_KEY")),
        ("output_dir", check_writable("./output")),
    ]

    all_passed = True
    for name, result in checks:
        status = "✓" if result.ok else "✗"
        print(f"{status} {name}: {result.message}")
        if not result.ok:
            all_passed = False
            if result.fix_command:
                print(f"  Fix: {result.fix_command}")

    if all_passed:
        print("\nAll checks passed! Ready to run.")
    else:
        print("\nSome checks failed. Fix the issues above and run again.")
        sys.exit(1)
```

### Node.js CLI

```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function checkBinary(name, versionFlag = '--version') {
  try {
    const version = execSync(`${name} ${versionFlag}`, { encoding: 'utf8' }).trim();
    return { ok: true, message: `${name} found: ${version.split('\n')[0]}` };
  } catch {
    return {
      ok: false,
      message: `${name} not found`,
      fix: `npm install -g ${name}  # or brew install ${name}`
    };
  }
}

function checkEnvVar(name) {
  const value = process.env[name];
  if (!value) {
    return {
      ok: false,
      message: `Environment variable ${name} not set`,
      fix: `export ${name}=<your-value>`
    };
  }
  return { ok: true, message: `${name} is set` };
}

function checkWritable(dirPath) {
  try {
    if (!fs.existsSync(dirPath)) {
      return {
        ok: false,
        message: `Directory ${dirPath} does not exist`,
        fix: `mkdir -p ${dirPath}`
      };
    }
    fs.accessSync(dirPath, fs.constants.W_OK);
    return { ok: true, message: `${dirPath} is writable` };
  } catch {
    return {
      ok: false,
      message: `${dirPath} is not writable`,
      fix: `chmod u+w ${dirPath}`
    };
  }
}

async function doctor() {
  const checks = [
    ['ffmpeg', checkBinary('ffmpeg')],
    ['API_KEY', checkEnvVar('API_KEY')],
    ['output', checkWritable('./output')],
  ];

  let allPassed = true;
  for (const [name, result] of checks) {
    const status = result.ok ? '✓' : '✗';
    console.log(`${status} ${name}: ${result.message}`);
    if (!result.ok) {
      allPassed = false;
      if (result.fix) {
        console.log(`  Fix: ${result.fix}`);
      }
    }
  }

  if (allPassed) {
    console.log('\nAll checks passed! Ready to run.');
  } else {
    console.log('\nSome checks failed. Fix the issues above and run again.');
    process.exit(1);
  }
}
```

### TypeScript (Browser Extension)

```typescript
interface CheckResult {
  ok: boolean;
  message: string;
  fix?: string;
}

async function checkPermission(permission: string): Promise<CheckResult> {
  const granted = await chrome.permissions.contains({ permissions: [permission] });
  if (!granted) {
    return {
      ok: false,
      message: `Missing permission: ${permission}`,
      fix: `Add "${permission}" to manifest.json permissions array`
    };
  }
  return { ok: true, message: `Permission ${permission} granted` };
}

async function checkStorage(): Promise<CheckResult> {
  try {
    await chrome.storage.local.get(null);
    return { ok: true, message: 'Storage accessible' };
  } catch (e) {
    return {
      ok: false,
      message: 'Cannot access chrome.storage',
      fix: 'Ensure "storage" permission in manifest.json'
    };
  }
}

async function doctor(): Promise<void> {
  const checks: [string, Promise<CheckResult>][] = [
    ['tabs', checkPermission('tabs')],
    ['storage', checkStorage()],
  ];

  let allPassed = true;
  for (const [name, checkPromise] of checks) {
    const result = await checkPromise;
    console.log(`${result.ok ? '✓' : '✗'} ${name}: ${result.message}`);
    if (!result.ok) {
      allPassed = false;
      if (result.fix) console.log(`  Fix: ${result.fix}`);
    }
  }

  console.log(allPassed ? '\nAll checks passed!' : '\nFix issues and reload.');
}
```

---

## What to Check

Priority order:

1. **Binaries** — Required executables exist and are the right version
2. **Credentials** — API keys, tokens, env vars are present and valid
3. **Permissions** — Write access to output paths
4. **Connectivity** — Required endpoints are reachable (optional, cache results)

---

## Checklist

- [ ] `<tool> doctor` command exists
- [ ] Checks all external binaries with version requirements
- [ ] Checks required environment variables
- [ ] Checks file/directory permissions
- [ ] Error messages include exact fix commands
- [ ] First run triggers doctor automatically (or prompts user)
- [ ] Expensive checks are cached (with `--force` to re-check)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Check at point-of-use | Fails deep in execution | Check upfront in doctor |
| Generic error messages | "Error: command failed" | Include name, version, fix |
| Hard fail on optional deps | Blocks users unnecessarily | Warn, degrade gracefully |
| Check every run | Slow startup | Cache, use `--force` |

---

## Success Signals

- New user runs `doctor` → sees all green or actionable red
- Zero support requests of "I installed it but it doesn't work"
- Docs can say "run `tool doctor` first" instead of listing prerequisites
