---
name: meaning-validate
description: Validate .meaning/index.yaml for errors and warnings
argument-hint: "[--verbose]"
user-invocable: true
allowed-tools: [read_file, terminal]
---

# Validate Meaning Semantic Index

Run health checks on the `.meaning/` index to detect errors, warnings, and inconsistencies.

## What This Does

Validates the semantic index by checking:
1. YAML syntax is valid
2. All required fields are present
3. Relationship targets exist in the index
4. Tags are in the schema vocabulary
5. Relationship types are defined in schema
6. Files referenced in index still exist
7. Stale entries (not verified recently)
8. Unindexed files in the project

## Workflow

### 1. Pre-flight Checks

```python
from pathlib import Path
from meaning.meaning_core import meaning_dir_exists, load_index, load_schema, load_config

project_root = Path.cwd()

# Check if .meaning/ exists
if not meaning_dir_exists(project_root):
    print("❌ .meaning/ not found!")
    print("Run /meaning-init to create semantic index first")
    exit(1)

print("✓ Found .meaning/ directory")
```

### 2. Load and Parse

```python
try:
    index = load_index(project_root)
    schema = load_schema(project_root)
    config = load_config(project_root)
    print(f"✓ Loaded index with {len(index.files)} files")
    print(f"✓ Loaded {schema.project_type} schema")
    print(f"✓ Loaded config")
except Exception as e:
    print(f"❌ Failed to load .meaning/ files:")
    print(f"   {e}")
    exit(1)
```

### 3. Run Validation

```python
from meaning.meaning_core import validate_index

validation = validate_index(index, schema, config, project_root)

print("\n" + "="*60)
print("📋 VALIDATION RESULTS")
print("="*60)
```

### 4. Report Results

```python
# Overall status
if validation.is_valid:
    print("✅ Index is VALID")
else:
    print("❌ Index has ERRORS")

print(f"\n📊 Summary:")
print(f"   Files indexed: {len(index.files)}")
print(f"   Concepts: {len(index.concepts)}")
print(f"   Errors: {len(validation.errors)}")
print(f"   Warnings: {len(validation.warnings)}")

# Show all errors
if validation.errors:
    print(f"\n❌ ERRORS ({len(validation.errors)}):")
    print("   These MUST be fixed:")
    for error in validation.errors:
        print(f"   • {error}")

# Categorize warnings
if validation.warnings:
    print(f"\n⚠️  WARNINGS ({len(validation.warnings)}):")
    
    # Separate warning types
    unindexed = [w for w in validation.warnings if "not indexed" in w]
    stale = [w for w in validation.warnings if "Stale entry" in w]
    unknown_tags = [w for w in validation.warnings if "Unknown tag" in w]
    other = [w for w in validation.warnings if w not in unindexed + stale + unknown_tags]
    
    if stale:
        print(f"\n   Stale entries (>{config.stale_threshold_days} days):")
        for w in stale[:5]:
            print(f"   • {w}")
        if len(stale) > 5:
            print(f"   ... and {len(stale) - 5} more")
    
    if unknown_tags:
        print(f"\n   Unknown tags (not in schema):")
        for w in unknown_tags[:5]:
            print(f"   • {w}")
        if len(unknown_tags) > 5:
            print(f"   ... and {len(unknown_tags) - 5} more")
    
    if other:
        print(f"\n   Other warnings:")
        for w in other[:5]:
            print(f"   • {w}")
        if len(other) > 5:
            print(f"   ... and {len(other) - 5} more")
    
    if unindexed:
        print(f"\n   Unindexed files: {len(unindexed)}")
        print(f"   (Run /meaning-update to index them)")

# Files needing review
needs_review = index.files_needing_review()
if needs_review:
    print(f"\n🔍 Files needing review ({len(needs_review)}):")
    for entry in needs_review[:10]:
        print(f"   • {entry.path}")
    if len(needs_review) > 10:
        print(f"   ... and {len(needs_review) - 10} more")
    print(f"\n   (Run /meaning-review to review them)")

print("\n" + "="*60)
```

### 5. Exit with Status Code

```python
# Exit with error code if validation failed
if not validation.is_valid:
    exit(1)
else:
    print("✅ All checks passed!")
    exit(0)
```

## Arguments

- `--verbose` - Show all warnings (don't truncate)
- `--errors-only` - Only show errors, skip warnings
- `--fix` - Attempt to auto-fix common issues

## Example Output (Success)

```
✓ Found .meaning/ directory
✓ Loaded index with 57 files
✓ Loaded python schema
✓ Loaded config

============================================================
📋 VALIDATION RESULTS
============================================================
✅ Index is VALID

📊 Summary:
   Files indexed: 57
   Concepts: 3
   Errors: 0
   Warnings: 8

⚠️  WARNINGS (8):

   Stale entries (>7 days):
   • Stale entry (>7 days): src/old_module.py
   • Stale entry (>7 days): tests/test_old.py

   Unindexed files: 6
   (Run /meaning-update to index them)

🔍 Files needing review (3):
   • src/new_feature.py
   • tests/test_new_feature.py
   • docs/new_doc.md

   (Run /meaning-review to review them)

============================================================
✅ All checks passed!
```

## Example Output (Errors)

```
✓ Found .meaning/ directory
✓ Loaded index with 57 files
✓ Loaded python schema
✓ Loaded config

============================================================
📋 VALIDATION RESULTS
============================================================
❌ Index has ERRORS

📊 Summary:
   Files indexed: 57
   Concepts: 3
   Errors: 3
   Warnings: 2

❌ ERRORS (3):
   These MUST be fixed:
   • Dangling relationship to 'src/missing.py' from: src/client.py
   • Dangling relationship to 'lib/util.py' from: tests/test_client.py
   • File in index not found: src/deleted_module.py

⚠️  WARNINGS (2):

   Unknown tags (not in schema):
   • Unknown tag 'deprecated' on file: src/old_api.py

============================================================
```

## Use Cases

| Scenario | When to Use |
|----------|-------------|
| Before committing | Ensure index is valid |
| After git pull | Check for consistency |
| CI/CD pipeline | Automated validation |
| Before release | Final health check |
| Debugging issues | Identify problems |

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Dangling relationship | Referenced file not in index | Add the file or remove relationship |
| File not found | File deleted but still in index | Run `/meaning-update --deleted` |
| Unknown tag | Tag not in schema vocabulary | Add to schema or use `x-` prefix |
| Stale entry | File not verified recently | Review file and update `last_verified` |
| Unindexed files | New files added | Run `/meaning-update --new` |

## Integration with CI/CD

Add to your CI pipeline:

```bash
# In .github/workflows/validate.yml
- name: Validate Meaning Index
  run: |
    python -c "
    from meaning.meaning_core import load_index, load_schema, load_config, validate_index
    from pathlib import Path
    
    index = load_index(Path('.'))
    schema = load_schema(Path('.'))
    config = load_config(Path('.'))
    result = validate_index(index, schema, config, Path('.'))
    
    if not result.is_valid:
        print('❌ Validation failed')
        for e in result.errors:
            print(f'  {e}')
        exit(1)
    print('✅ Validation passed')
    "
```

## Error Handling

| Error | Solution |
|-------|----------|
| `.meaning/` missing | Run `/meaning-init` |
| YAML syntax error | Fix manually, check line numbers |
| Permission denied | Check read permissions |
| Corrupted index | Restore from git or regenerate |

## Notes

- **Non-destructive** - Only reads, never writes
- **Fast** - Completes in milliseconds
- **Comprehensive** - Checks all aspects of index health
- **CI-friendly** - Returns proper exit codes
- **Detailed** - Clear error messages with context

## Philosophy

```
Do not write code before stating assumptions.
Do not claim correctness you haven't verified.
Do not handle only the happy path.
Under what conditions does this work?
```

This skill:
- ✓ Checks all preconditions (.meaning/ exists, files parseable)
- ✓ Reports all issues found (errors and warnings)
- ✓ Categorizes problems (helps prioritize fixes)
- ✓ Provides clear remediation steps