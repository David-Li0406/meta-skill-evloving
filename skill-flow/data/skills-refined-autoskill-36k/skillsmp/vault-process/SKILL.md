---
name: vault-process
description: >
  Use when user wants to organize, classify, or process Inbox items.
  Triggered when intention is to transform fleeting notes into permanent knowledge.
  Moves notes from 00_Inbox to appropriate destinations.
---

# Vault Process

## Behavior

1. List unprocessed notes in `00_Inbox/`
2. For each note:
   - Read and review content
   - Suggest destination (Projects, Areas, or Resources)
   - Propose enriched frontmatter (tags, type change)
   - Move to destination after user approval
   - Update any internal links if necessary

## Destination Logic

| Content Type | Destination | New Type |
|--------------|-------------|----------|
| Has clear goal/deadline | `01_Projects/{project}/` | project |
| Ongoing responsibility | `02_Areas/{area}/` | area |
| Reference/knowledge | `03_Resources/{topic}/` | permanent |
| Not worth keeping | Delete or leave in Inbox | - |

## Processing Flow

1. Show list of Inbox items with brief summaries
2. For each item, suggest:
   - Destination folder
   - Updated frontmatter
   - Potential tags
3. Ask for confirmation before moving
4. Execute moves and report results

## Frontmatter Updates

When moving to Resources, update to permanent note structure:
```yaml
---
type: permanent
topic: {inferred topic}
created: {original date}
source: capture
tags: [{suggested tags}]
---
```

## After Processing

- Summarize what was moved where
- Note any items that need further clarification
- Report Inbox status (empty or remaining items)
