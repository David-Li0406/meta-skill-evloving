---
name: obsidian-frontmatter
description: Search and manage Obsidian note frontmatter metadata. Use to find notes
  by properties (tags, status, dates, custom fields) or to create/update/delete frontmatter
  with user confirmation.
license: MIT
metadata:
  author: gabrielwithappy
  version: '1.0'
tags: 30_Resources
---
# Obsidian Frontmatter Explorer Skill

This skill enables agents to search and manage Obsidian note frontmatter (YAML metadata) to help discover relevant files and maintain metadata consistency across your vault.

## Purpose

Before starting work on Obsidian notes, agents need to find the right files. This skill acts as a "discovery tool" that:
- Searches notes by frontmatter properties
- Lists all values for a property across the vault
- Creates, updates, or deletes frontmatter properties with user confirmation

## Core Operations

### 1. Search Notes by Frontmatter

Find notes matching specific frontmatter criteria.

**Usage:**
```bash
python .agent/skills/obsidian-frontmatter/scripts/frontmatter_search.py <vault_path> [options]
```

**Options:**
- `--property <name>` - Property name to search
- `--exists` - Find notes where property exists
- `--not-exists` - Find notes where property does not exist
- `--equals <value>` - Find notes where property equals value
- `--contains <value>` - Find notes where property contains value (for lists/text)
- `--gt <value>` - Greater than (for numbers/dates)
- `--lt <value>` - Less than (for numbers/dates)
- `--format json|table` - Output format (default: table)
- `--output <file>` - Save output to file instead of printing to console

**Examples:**

Find all notes with `status` property:
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" --property "status" --exists
```

Find notes without tags:
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" --property "tags" --not-exists
```

Find notes tagged with "30_Resources":
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" --property "tags" --contains "30_Resources"
```

Find notes with status equals "진행중":
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" --property "상태" --equals "진행중"
```

Multiple filters (AND logic):
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" \
  --property "tags" --contains "22_업무경력/개발/AI" \
  --property "상태" --equals "정보"
```

---

### 2. List Property Values

Show all unique values for a property across the vault with usage counts.

**Usage:**
```bash
python .agent/skills/obsidian-frontmatter/scripts/frontmatter_list.py <vault_path> --property <name> [options]
```

**Options:**
- `--property <name>` - Property name to list (required)
- `--min-count <n>` - Only show values used at least n times
- `--format json|table` - Output format (default: table)
- `--output <file>` - Save output to file instead of printing to console

**Examples:**

List all tag values:
```bash
python scripts/frontmatter_list.py "d:\00_MyData\obsidianKMS" --property "tags"
```

List status values used at least 5 times:
```bash
python scripts/frontmatter_list.py "d:\00_MyData\obsidianKMS" --property "상태" --min-count 5
```

---

### 3. Modify Frontmatter (Create/Update/Delete)

Modify frontmatter properties with preview and user confirmation.

**Usage:**
```bash
python .agent/skills/obsidian-frontmatter/scripts/frontmatter_modify.py <file_or_pattern> [operation] [options]
```

**Operations:**
- `--create <key:value>` - Add new property
- `--update <key:value>` - Update existing property
- `--delete <key>` - Remove property
- `--apply` - Actually apply changes (without this, shows preview only)

**File Selection:**
- Single file: `path/to/note.md`
- Multiple files: `--files file1.md file2.md file3.md`
- Pattern: `--pattern "*.md"` (within vault)

**Examples:**

Preview adding a property (shows diff, doesn't apply):
```bash
python scripts/frontmatter_modify.py "note.md" --create "reviewed:true"
```

Apply the change after user confirms:
```bash
python scripts/frontmatter_modify.py "note.md" --create "reviewed:true" --apply
```

Update existing property:
```bash
python scripts/frontmatter_modify.py "note.md" --update "상태:완료" --apply
```

Delete a property:
```bash
python scripts/frontmatter_modify.py "note.md" --delete "draft" --apply
```

Batch update multiple files:
```bash
python scripts/frontmatter_modify.py --files note1.md note2.md note3.md \
  --update "reviewed:true" --apply
```

---

## Property Types

The skill automatically handles different property types:

| Type | Example | Notes |
|------|---------|-------|
| Text | `title: My Note` | Simple string values |
| Number | `rating: 4.5` | Integer or float |
| Boolean | `completed: true` | true/false |
| Date | `date: 2024-01-15` | ISO date format |
| DateTime | `due: 2024-01-15T14:30:00` | ISO datetime |
| List | `tags: [tag1, tag2]` | Arrays |
| Links | `related: "[[Other Note]]"` | Wikilinks in quotes |

---

## Confirmation Workflow

**IMPORTANT:** All modification operations require user confirmation by default.

1. **Preview Mode (Default)**: Shows what will change without applying
   ```bash
   python scripts/frontmatter_modify.py "note.md" --create "status:draft"
   # Shows diff preview, asks for confirmation
   ```

2. **Apply Mode**: Actually makes the changes
   ```bash
   python scripts/frontmatter_modify.py "note.md" --create "status:draft" --apply
   # Applies changes after showing preview
   ```

3. **Force Mode** (only if user explicitly requests):
   ```bash
   python scripts/frontmatter_modify.py "note.md" --create "status:draft" --apply --force
   # Applies without confirmation (use with caution!)
   ```

**Agent Instructions:**
- Always run modification commands WITHOUT `--apply` first to show preview
- Present the preview to the user via notify_user
- Only add `--apply` flag after user confirms
- Never use `--force` unless user explicitly requests it

---

## Common Use Cases

### Finding Notes to Work On

**Find all project notes that are in progress:**
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" \
  --property "tags" --contains "10_Projects" \
  --property "상태" --equals "진행중"
```

**Find all notes about AI development:**
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" \
  --property "tags" --contains "22_업무경력/개발/AI"
```

### Maintaining Metadata Consistency

**List all unique status values to check for inconsistencies:**
```bash
python scripts/frontmatter_list.py "d:\00_MyData\obsidianKMS" --property "상태"
```

**Update misspelled tag across multiple notes:**
```bash
# First, find affected notes
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" \
  --property "tags" --contains "old-tag" --format json > affected.json

# Preview changes
python scripts/frontmatter_modify.py --files $(cat affected.json | jq -r '.[].file') \
  --update "tags:new-tag"

# Apply after user confirms
python scripts/frontmatter_modify.py --files $(cat affected.json | jq -r '.[].file') \
  --update "tags:new-tag" --apply
```

---

## Error Handling

The scripts handle common errors gracefully:
- **Malformed YAML**: Skips files with invalid frontmatter, reports in output
- **Missing properties**: Returns empty results for searches, creates new for modifications
- **Type mismatches**: Validates property types before applying changes
- **File not found**: Reports clear error messages
- **Permission errors**: Reports files that cannot be modified

---

## Integration with Other Skills

This skill complements other Obsidian skills:

- **obsidian-markdown**: Use frontmatter-explorer to find notes, then obsidian-markdown to edit content
- **obsidian-bases**: Search for notes to include in Base views
- **json-canvas**: Find notes to add to canvas diagrams

**Example Workflow:**
1. Use `frontmatter_search.py` to find notes about a topic
2. Use `obsidian-markdown` skill to edit the found notes
3. Use `frontmatter_modify.py` to update status after editing

---

## References

- [Obsidian Properties Documentation](https://help.obsidian.md/properties)
- [YAML Frontmatter Specification](https://yaml.org/spec/1.2/spec.html)
- [Agent Skills Specification](https://agentskills.io/specification)
