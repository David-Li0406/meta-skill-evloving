---
name: meaning-update
description: Sync .meaning/index.yaml with filesystem changes
argument-hint: "[--new|--modified|--deleted|--all]"
user-invocable: true
allowed-tools: [read_file, write_file, list_directory, terminal]
---

# Update Meaning Semantic Index

Synchronize the `.meaning/index.yaml` with filesystem changes by detecting new, modified, and deleted files.

## What This Does

Keeps your semantic index in sync with the actual filesystem by:
1. Detecting new files not yet in the index
2. Detecting files that have been modified since last verification
3. Detecting files in the index that no longer exist
4. Running inference on new/modified files
5. Updating the index with changes

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

# Load existing index
index = load_index(project_root)
schema = load_schema(project_root)
config = load_config(project_root)

print(f"✓ Loaded index with {len(index.files)} files")
```

### 2. Detect Changes

```python
from meaning.meaning_core import (
    find_unindexed_files,
    find_modified_files,
    find_deleted_files,
)

# Find changes
new_files = find_unindexed_files(project_root, index, config)
modified_files = find_modified_files(project_root, index)
deleted_files = find_deleted_files(project_root, index)

print(f"📊 Changes detected:")
print(f"   • New files: {len(new_files)}")
print(f"   • Modified files: {len(modified_files)}")
print(f"   • Deleted files: {len(deleted_files)}")

if not new_files and not modified_files and not deleted_files:
    print("✓ Index is up to date!")
    exit(0)
```

### 3. Process Deleted Files

```python
if deleted_files:
    print(f"\n🗑️  Removing {len(deleted_files)} deleted files:")
    for path in deleted_files:
        print(f"   • {path}")
        index.remove_file(path)
```

### 4. Process New Files

```python
from meaning_inference import infer_file_metadata, infer_timestamps
from meaning.meaning_core import FileEntry

if new_files:
    print(f"\n✨ Adding {len(new_files)} new files:")
    
    now = infer_timestamps()
    
    for i, file_path in enumerate(new_files):
        print(f"   Inferring {i+1}/{len(new_files)}: {file_path}")
        
        # Run inference
        result = infer_file_metadata(file_path, project_root, index, schema)
        
        # Determine if needs review
        needs_review = (
            not result.intent
            or (result.intent and result.intent.confidence < 0.8)
            or len(result.tags) == 0
            or any(e for e in result.errors)
        )
        
        # High-confidence tags and relationships
        high_conf_tags = [t.tag for t in result.tags if t.confidence >= 0.8]
        high_conf_rels = [r.relationship for r in result.relationships if r.confidence >= 0.8]
        
        # Create entry
        intent = result.intent.intent if result.intent else f"[REVIEW NEEDED] {file_path}"
        
        entry = FileEntry(
            path=file_path,
            intent=intent,
            tags=high_conf_tags if high_conf_tags else ["x-needs-tags"],
            status="active",
            needs_review=needs_review,
            last_verified=now,
            relationships=high_conf_rels,
        )
        
        index.add_file(entry)
```

### 5. Process Modified Files

```python
if modified_files:
    print(f"\n🔄 Flagging {len(modified_files)} modified files for review:")
    
    now = infer_timestamps()
    
    for file_path in modified_files:
        print(f"   • {file_path}")
        
        # Get existing entry
        entry = index.get_file(file_path)
        if entry:
            # Flag for review and update timestamp
            entry.needs_review = True
            entry.last_verified = now
            
            # Optionally re-run inference and show suggestions
            # (User can review and apply manually)
```

### 6. Save and Report

```python
from meaning.meaning_core import save_index, validate_index

# Update index timestamp
index.last_updated = infer_timestamps()

# Save
save_index(index, project_root)

print(f"\n✓ Saved updated index.yaml")

# Validate
validation = validate_index(index, schema, config, project_root)

print("\n" + "="*60)
print("📋 UPDATE COMPLETE")
print("="*60)
print(f"✓ Files in index: {len(index.files)}")
print(f"   + Added: {len(new_files)}")
print(f"   ~ Modified: {len(modified_files)}")
print(f"   - Deleted: {len(deleted_files)}")
print(f"⚠️  Files needing review: {len(index.files_needing_review())}")
print(f"✓ Validation: {validation.is_valid}")

if validation.errors:
    print(f"\n❌ Errors: {len(validation.errors)}")
    for e in validation.errors[:5]:
        print(f"   • {e}")
        
if validation.warnings:
    print(f"\n⚠️  Warnings: {len(validation.warnings)}")
    for w in validation.warnings[:5]:
        print(f"   • {w}")

print("\n" + "="*60)
print("Next steps:")
if index.files_needing_review():
    print("1. Run /meaning-review to review flagged entries")
print("2. Commit updated .meaning/ to git")
print("="*60)
```

## Arguments

Parse user arguments to control what gets updated:

- `--new` - Only process new files
- `--modified` - Only flag modified files
- `--deleted` - Only remove deleted files
- `--all` - Process all changes (default)
- `--re-infer` - Re-run inference on modified files (not just flag)
- `--dry-run` - Show what would change without writing

## Example Output

```
✓ Loaded index with 50 files

📊 Changes detected:
   • New files: 5
   • Modified files: 3
   • Deleted files: 1

🗑️  Removing 1 deleted file:
   • src/old_module.py

✨ Adding 5 new files:
   Inferring 1/5: src/new_feature.py
   Inferring 2/5: tests/test_new_feature.py
   Inferring 3/5: docs/new_feature.md
   Inferring 4/5: src/helpers/utils.py
   Inferring 5/5: tests/test_utils.py

🔄 Flagging 3 modified files for review:
   • src/api/client.py
   • README.md
   • CHANGELOG.md

✓ Saved updated index.yaml

============================================================
📋 UPDATE COMPLETE
============================================================
✓ Files in index: 57
   + Added: 5
   ~ Modified: 3
   - Deleted: 1
⚠️  Files needing review: 8
✓ Validation: True

⚠️  Warnings: 0

============================================================
Next steps:
1. Run /meaning-review to review flagged entries
2. Commit updated .meaning/ to git
============================================================
```

## Use Cases

| Scenario | Command |
|----------|---------|
| Added new files | `/meaning-update --new` |
| Edited existing files | `/meaning-update --modified` |
| Deleted files | `/meaning-update --deleted` |
| After git pull | `/meaning-update --all` |
| Daily sync | `/meaning-update` |

## Error Handling

| Error | Solution |
|-------|----------|
| `.meaning/` missing | Run `/meaning-init` first |
| Permission denied | Check file/directory permissions |
| Invalid index.yaml | Fix YAML syntax errors |
| Validation errors | Review and fix relationships |

## Notes

- **Non-destructive** - Modified files are flagged, not overwritten
- **Incremental** - Only processes changed files, not entire project
- **Fast** - Typically completes in seconds even for large projects
- **Safe** - Always validates before saving
- **Git-aware** - Works naturally with git workflow

## Philosophy

```
Do not write code before stating assumptions.
Do not claim correctness you haven't verified.
Do not handle only the happy path.
Under what conditions does this work?
```

This skill:
- ✓ Checks preconditions (.meaning/ must exist)
- ✓ Validates after changes (ensures index is valid)
- ✓ Handles edge cases (deleted files, permission errors)
- ✓ Reports all changes transparently