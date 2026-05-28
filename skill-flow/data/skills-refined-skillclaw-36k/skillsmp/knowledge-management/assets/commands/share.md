---
description: Share knowledge across projects by copying to shared-knowledge directory
---

# Share - Cross-Project Knowledge Sync

Copy project-specific knowledge to the shared directory for reuse across projects.

## Usage

```
/share [knowledge-file-path]
/share docs/knowledge-base/retry-pattern.md
```

**Output:** `$PROJECT_ROOT/docs/shared-knowledge/[filename].md`

## Instructions

1. **Validate** the source file exists and is in docs/
2. **Copy** to `docs/shared-knowledge/`
3. **Clean** project-specific references (paths, project names)
4. **Add** cross-project metadata:
   - Remove project-specific paths
   - Add `scope: cross-project` to frontmatter
   - Add source project reference
5. **Confirm** with user

## Template Additions

Add to the shared file's frontmatter:
```yaml
scope: cross-project
source_project: [current project name]
shared_date: YYYY-MM-DD
```

## Sync to Other Projects

To use shared knowledge in another project:

```bash
# Option 1: Symlink
ln -s /path/to/shared-knowledge docs/shared-knowledge

# Option 2: Copy specific files
cp /path/to/shared-knowledge/pattern.md docs/knowledge-base/
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/distill` | Create knowledge (can then /share) |
| `/search` | Find knowledge to share |
| `/share` | Share cross-project (you are here) |
