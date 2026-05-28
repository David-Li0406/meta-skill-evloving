# DSPy Version Management

Track and manage dependency versions to ensure compatibility. This guide covers dependency versioning, version mismatch detection, and compatibility best practices.

## Table of Contents

- [Versioning Overview](#versioning-overview)
- [Dependency Versioning](#dependency-versioning)
- [Version Mismatch Detection](#version-mismatch-detection)
- [Version Best Practices](#version-best-practices)
- [Compatibility](#compatibility)

## Versioning Overview

### What is Version Management?

DSPy automatically captures and stores dependency versions when saving modules, ensuring compatibility when loading modules later.

### Why Manage Versions?

- **Compatibility**: Prevents issues from version changes
- **Reproducibility**: Ensures consistent results across runs
- **Debugging**: Identifies version-related problems
- **Migration**: Facilitates upgrades with minimal disruption

## Dependency Versioning

### Automatic Version Capture

DSPy's `save()` method automatically captures dependency versions:

```python
import dspy

# Create and configure program
program = MyDSPyProgram()
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

# Save program
program.save("my_program.json")

# Dependency versions are automatically captured
```

### What is Captured?

DSPy captures versions of:
- **DSPy itself**: The DSPy version used
- **Critical dependencies**: Key dependencies that affect behavior
- **Provider libraries**: LLM provider libraries (OpenAI, Anthropic, etc.)

### Loading with Version Check

When loading a saved module, DSPy can check for version mismatches:

```python
import dspy

# Load program (with automatic version check)
loaded_program = dspy.load("my_program.json")

# DSPy will warn if versions don't match
```

## Version Mismatch Detection

### Automatic Warnings

DSPy automatically warns about version mismatches:

```python
import dspy

# Load program with version mismatch
loaded_program = dspy.load("my_program.json")

# Output:
# WARNING: DSPy version mismatch
# Saved version: 2.5.0
# Current version: 2.6.0
# This may cause unexpected behavior.
```

### Explicit Version Check

Manually check versions before loading:

```python
import dspy
import json

# Load saved program metadata
with open("my_program.json", "r") as f:
    metadata = json.load(f)

# Check DSPy version
saved_dspy_version = metadata.get("_metadata", {}).get("dspy_version")
current_dspy_version = dspy.__version__

if saved_dspy_version != current_dspy_version:
    print(f"WARNING: DSPy version mismatch!")
    print(f"Saved: {saved_dspy_version}")
    print(f"Current: {current_dspy_version}")
```

### Dependency Version Check

```python
import dspy
import json

# Load saved program metadata
with open("my_program.json", "r") as f:
    metadata = json.load(f)

# Check dependency versions
saved_deps = metadata.get("_metadata", {}).get("dependencies", {})

for package, saved_version in saved_deps.items():
    try:
        current_version = __import__(package).__version__
        if saved_version != current_version:
            print(f"WARNING: {package} version mismatch!")
            print(f"Saved: {saved_version}")
            print(f"Current: {current_version}")
    except ImportError:
        print(f"WARNING: {package} not installed!")
```

### Version Mismatch Handling

Handle version mismatches gracefully:

```python
import dspy
import json

def load_with_version_check(filepath):
    """Load program with version check."""
    # Load saved program
    with open(filepath, "r") as f:
        metadata = json.load(f)

    # Check versions
    saved_version = metadata.get("_metadata", {}).get("dspy_version")
    current_version = dspy.__version__

    if saved_version != current_version:
        print(f"WARNING: DSPy version mismatch!")
        print(f"Saved: {saved_version}")
        print(f"Current: {current_version}")

        # Ask user what to do
        choice = input("Continue anyway? (y/n): ")
        if choice.lower() != 'y':
            return None

    # Load program
    return dspy.load(filepath)

# Use with version check
program = load_with_version_check("my_program.json")
```

## Version Best Practices

### 1. Always Save Programs

```python
# Good: Save programs to capture versions
program = MyDSPyProgram()
program.save("my_program.json")

# Bad: Don't save programs (no version info)
program = MyDSPyProgram()
```

### 2. Check Versions Before Loading

```python
# Good: Check versions before loading
def load_program(filepath):
    saved_version = get_saved_version(filepath)
    current_version = dspy.__version__

    if saved_version != current_version:
        print("WARNING: Version mismatch!")
        return None

    return dspy.load(filepath)

# Bad: Load without checking
program = dspy.load("my_program.json")
```

### 3. Document Version Requirements

```python
"""
My DSPy Program

Version Requirements:
- DSPy: 2.5.0 or higher
- OpenAI: 1.0.0 or higher
- Python: 3.10 or higher

Created with DSPy 2.5.0
Last updated: 2024-01-15
"""
```

### 4. Use Version-Pinned Environments

```python
# requirements.txt
dspy==2.5.0
openai==1.0.0
anthropic==0.18.0
```

### 5. Version Compatibility Matrix

| DSPy Version | OpenAI SDK | Anthropic SDK | Notes |
|--------------|-------------|----------------|--------|
| 2.5.0 | 1.0.0+ | 0.18.0+ | Stable |
| 2.6.0 | 1.0.0+ | 0.18.0+ | New features |

## Compatibility

### Minor Version Changes

Minor version changes (e.g., 2.5.0 → 2.6.0) are generally compatible:

```python
# Saved with DSPy 2.5.0
# Load with DSPy 2.6.0

# Should work without issues
program = dspy.load("my_program.json")
```

### Major Version Changes

Major version changes (e.g., 2.5.0 → 3.0.0) may have breaking changes:

```python
# Saved with DSPy 2.5.0
# Load with DSPy 3.0.0

# May fail due to breaking changes
program = dspy.load("my_program.json")
```

### Dependency Updates

Update dependencies regularly for security and bug fixes:

```python
# Update all packages
!pip install --upgrade dspy openai anthropic

# Save program after update
program = MyDSPyProgram()
program.save("my_program_v2.json")
```

### Migration Path

When upgrading DSPy versions, follow this path:

1. **Test with old version**: Ensure program works correctly
2. **Save with old version**: Capture baseline behavior
3. **Upgrade DSPy**: `pip install --upgrade dspy`
4. **Test with new version**: Check for issues
5. **Save with new version**: Capture new behavior
6. **Compare results**: Ensure outputs are consistent

## Common Issues and Solutions

### Issue: Version Mismatch on Load

**Problem**: Program fails to load due to version mismatch

**Solution**:
1. Check DSPy version: `import dspy; print(dspy.__version__)`
2. Reinstall correct version: `pip install dspy==2.5.0`
3. Or upgrade and retrain program with new version
4. Use version pinning in requirements.txt

### Issue: Dependency Not Found

**Problem**: Program fails because of missing dependency

**Solution**:
1. Install missing dependency: `pip install <package>`
2. Check requirements.txt: Ensure all dependencies are listed
3. Use version pinning: `pip install <package>==<version>`
4. Update dependencies regularly

### Issue: Inconsistent Behavior

**Problem**: Program behaves differently across runs

**Solution**:
1. Check DSPy version is consistent
2. Verify dependency versions are correct
3. Check for environment variable changes
4. Use version-pinned environments
5. Set random seeds for reproducibility

### Issue: Cannot Load Old Program

**Problem**: Cannot load program saved with old DSPy version

**Solution**:
1. Reinstall old DSPy version: `pip install dspy==<old_version>`
2. Load and test program
3. Re-export or migrate to new version
4. Document breaking changes
