---
name: meaning-init
description: Bootstrap .meaning/ directory for a project with intelligent inference
argument-hint: "[--type python|node|rust|docs] [--limit N]"
user-invocable: true
allowed-tools: [read_file, write_file, list_directory, terminal, grep, find_path]
---

# Initialize Meaning Semantic Index

Bootstrap the `.meaning/` directory for a project with semantic file indexing and intelligent inference.

## What This Does

Creates a complete semantic index for a project by:
1. Detecting project type (Python, Node, Rust, docs)
2. Installing appropriate schema and config templates
3. Scanning all non-excluded files
4. Running inference on each file (tags, relationships, intents)
5. Generating initial `index.yaml` with high-confidence suggestions
6. Flagging low-confidence entries for user review

## Workflow

### 1. Pre-flight Checks

```python
from pathlib import Path
from meaning.meaning_core import meaning_dir_exists, detect_project_type, is_git_repo

project_root = Path.cwd()

# Check if .meaning/ already exists
if meaning_dir_exists(project_root):
    print("❌ .meaning/ already exists!")
    print("Use /meaning-update to sync with filesystem changes")
    exit(1)

# Detect project type
project_type = detect_project_type(project_root)
is_git = is_git_repo(project_root)

print(f"✓ Detected project type: {project_type}")
print(f"✓ Git repository: {is_git}")
```

### 2. Initialize Structure

```python
from meaning.meaning_core import initialize_meaning, save_index

# Create .meaning/ with templates
index, schema, config = initialize_meaning(project_root, project_type=project_type)

print(f"✓ Created .meaning/ directory")
print(f"✓ Installed {project_type} schema")
print(f"✓ Installed default config")
```

### 3. Scan and Infer

```python
from meaning.meaning_core import scan_project_files
from meaning_inference import infer_file_metadata, infer_timestamps

# Scan project files
all_files = scan_project_files(project_root, config)
print(f"✓ Found {len(all_files)} files to index")

# Run inference on each file (limit for initial run)
limit = 50  # Process first 50 files by default
results = []

for i, file_path in enumerate(all_files[:limit]):
    print(f"  Inferring {i+1}/{min(len(all_files), limit)}: {file_path}")
    result = infer_file_metadata(file_path, project_root, index, schema)
    results.append(result)

if len(all_files) > limit:
    print(f"⚠️  Limited to first {limit} files. Run /meaning-update to index remaining {len(all_files) - limit} files.")
```

### 4. Build Index with Suggestions

```python
from meaning.meaning_core import FileEntry

now = infer_timestamps()

for result in results:
    # Determine if entry needs review
    needs_review = False
    
    # High-confidence tags
    high_conf_tags = [t.tag for t in result.tags if t.confidence >= 0.8]
    
    # High-confidence relationships
    high_conf_rels = [r.relationship for r in result.relationships if r.confidence >= 0.8]
    
    # Intent (may need review if confidence < 0.8)
    intent = result.intent.intent if result.intent and result.intent.confidence >= 0.7 else ""
    if not intent or (result.intent and result.intent.confidence < 0.8):
        needs_review = True
    
    # Create entry
    entry = FileEntry(
        path=result.path,
        intent=intent or f"[REVIEW NEEDED] {result.path}",
        tags=high_conf_tags if high_conf_tags else ["x-needs-tags"],
        status="active",
        needs_review=needs_review,
        last_verified=now,
        relationships=high_conf_rels,
    )
    
    index.add_file(entry)

print(f"✓ Created {len(index.files)} file entries")
```

### 5. Save and Report

```python
from meaning.meaning_core import save_index, validate_index

# Update timestamps
index.last_updated = now

# Save index
save_index(index, project_root)

print(f"✓ Saved index.yaml")

# Validate
validation = validate_index(index, schema, config, project_root)

print("\n" + "="*60)
print("📋 INITIALIZATION COMPLETE")
print("="*60)
print(f"✓ Files indexed: {len(index.files)}")
print(f"✓ Concepts: {len(index.concepts)} (none yet - add manually or use /meaning-review)")
print(f"⚠️  Files needing review: {len(index.files_needing_review())}")
print(f"✓ Validation: {validation.is_valid}")

if validation.warnings:
    print(f"\n⚠️  Warnings: {len(validation.warnings)}")
    for w in validation.warnings[:5]:
        print(f"   • {w}")
    if len(validation.warnings) > 5:
        print(f"   ... and {len(validation.warnings) - 5} more")

print("\n" + "="*60)
print("Next steps:")
print("1. Review entries with needs_review: true")
print("2. Run /meaning-review to accept/modify suggestions")
print("3. Add concept groupings manually to index.yaml")
print("4. Commit .meaning/ to git")
print("="*60)
```

## Arguments

Parse user arguments if provided:

- `--type TYPE` - Force project type (python, node, rust, docs)
- `--limit N` - Process first N files (default: 50)
- `--all` - Process all files (no limit)
- `--dry-run` - Show what would be created without writing

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| `.meaning/` exists | Use `/meaning-update` instead |
| No write permissions | Check directory permissions |
| Unknown project type | Specify `--type` explicitly |
| No files found | Check config exclusion patterns |

## Example Output

```
✓ Detected project type: python
✓ Git repository: true
✓ Created .meaning/ directory
✓ Installed python schema
✓ Installed default config
✓ Found 127 files to index
  Inferring 1/50: src/main.py
  Inferring 2/50: src/api/client.py
  ...
  Inferring 50/50: tests/test_utils.py
⚠️  Limited to first 50 files. Run /meaning-update to index remaining 77 files.
✓ Created 50 file entries
✓ Saved index.yaml

============================================================
📋 INITIALIZATION COMPLETE
============================================================
✓ Files indexed: 50
✓ Concepts: 0 (none yet - add manually or use /meaning-review)
⚠️  Files needing review: 12
✓ Validation: True

⚠️  Warnings: 77
   • File not indexed: docs/api.md
   • File not indexed: scripts/deploy.sh
   ... and 75 more

============================================================
Next steps:
1. Review entries with needs_review: true
2. Run /meaning-review to accept/modify suggestions
3. Add concept groupings manually to index.yaml
4. Commit .meaning/ to git
============================================================
```

## Notes

- **Inference is not perfect** - Review suggestions before committing
- **Start small** - Default 50-file limit prevents overwhelming output
- **Iterative** - Run `/meaning-update` to index remaining files after review
- **Git-friendly** - All YAML files are human-readable and diffable
- **No external dependencies** - Works offline, no API calls

## Philosophy

```
Do not write code before stating assumptions.
Do not claim correctness you haven't verified.
Do not handle only the happy path.
Under what conditions does this work?
```

This skill:
- ✓ States assumptions (project type, file accessibility)
- ✓ Verifies correctness (validation after creation)
- ✓ Handles errors (checks for existing .meaning/, permission issues)
- ✓ Documents conditions (requires write access, valid project structure)