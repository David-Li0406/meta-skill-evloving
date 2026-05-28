---
name: vault-archive
description: >
  Use when user wants to store completed or inactive items.
  Triggered when intention involves finishing, closing, or preserving old work.
  Moves items to 04_Archive with proper metadata.
---

# Vault Archive

## Behavior

1. Identify what to archive:
   - Completed project → entire folder
   - Outdated resource → single note
   - Old area content → folder or notes
2. Update frontmatter with archive metadata
3. Move to `04_Archive/` preserving structure
4. Update any MOCs that referenced archived items

## Archive Metadata

Add to frontmatter before moving:
```yaml
archived: {YYYY-MM-DD}
status: completed  # for projects
```

## Folder Structure Preservation

```
Original: 01_Projects/marketing-campaign/
Archived: 04_Archive/01_Projects/marketing-campaign/
```

Preserve the source folder prefix to maintain context.

## Pre-Archive Checklist

Before archiving, verify:
- [ ] All tasks completed (or intentionally abandoned)
- [ ] No active references from other notes
- [ ] User confirms archival

## Confirmation Flow

1. Show what will be archived:
   - File/folder name
   - Note count (if folder)
   - Last modified date
2. Warn about any active links to this content
3. Ask for explicit confirmation
4. Execute archive

## Post-Archive Actions

- Confirm completion with new location
- Remind: "Archived items remain searchable"
- Offer to update any MOCs that linked to archived content
- Suggest: "You might want to run vault-status to see remaining active projects"

## Undo Guidance

If user wants to unarchive:
1. Move folder/file back to original location
2. Remove `archived:` field from frontmatter
3. Update `status:` if applicable
