# Output Templates

## Proposal Display Format

Present proposals ONE AT A TIME with this format:

```markdown
## Proposal 1 of 3

**📝 [Proposed Title]**
From: ✂️ [Original filename]

### Summary
[2-3 sentences]

### Categorization Hints
> *For organization only - use `/para-obsidian:distill-resource` for deep learning*

- [Hint 1 - helps with PARA placement]
- [Hint 2 - helps identify connections]
- [Hint 3 - helps with future search]

### Classification
| Field | Value |
|-------|-------|
| Template | [resource] |
| Type | [article] |
| Format | [video] |

### Connections
- Area: [[Suggested Area]]
- Project: [[Suggested Project]]

---

**Actions:**
- **A** - Accept as-is
- **E** - Edit (tell me what to change)
- **S** - Skip (keep in inbox for later)
- **D** - Delete (remove from inbox)
- **3** - Deeper (get 3 alternative proposals)
- **Q** - Quit (save progress for later)
```

## Deep Analysis Options Format

When user chooses "3" (Deeper), present 3 options:

```markdown
## 3 Ways to Categorize This

**Option A: Meeting Notes (standup)**
> Summary: Team sync discussing sprint progress...
> Area: [[🌱 Work]] → Project: [[🎯 Sprint 42]]
> Rationale: Multiple speakers, action items, time-boxed format

**Option B: Personal Reflection**
> Summary: Thinking through career direction...
> Area: [[🌱 Personal Development]]
> Rationale: First-person, introspective tone, no action items

**Option C: Brainstorm Session**
> Summary: Ideas for new feature implementation...
> Area: [[🌱 AI Practice]] → Project: [[🎯 Claude Plugins]]
> Rationale: Exploratory thinking, multiple possibilities listed

---

Which interpretation? (A/B/C or tell me something different)
```

## Inbox Summary Format

After scanning inbox, present this summary:

```markdown
Found [N] items in inbox:

📋 By Type:
• [N] clippings (web articles, threads)
• [N] voice memos (transcriptions)
• [N] attachments (PDFs, docs)

📋 By Enrichment Strategy:
• [N] parallel-enrichable (YouTube, public articles)
• [N] sequential-only (Twitter, Confluence)
• [N] no enrichment needed (voice, attachments)

📋 Task Graph Created:
• Batch 1: 3 items → review
• Batch 2: 3 items → review
• Cleanup

Starting enrichment phase...
```

## Completion Report Format

After triage completes:

```markdown
✅ Triage complete!

Processed [N] items:
• [N] accepted → created resource notes
• [N] skipped → still in inbox
• [N] deleted

All triage tasks cleaned up.
```

## Action Handling Reference

| Action | Behavior |
|--------|----------|
| **A (Accept)** | Create note with proposal, handle original (delete clipping / move transcription) |
| **E (Edit)** | Ask what to change, update proposal, re-present |
| **S (Skip)** | Mark as skipped, move to next |
| **D (Delete)** | Delete original file (with confirmation) |
| **3 (Deeper)** | Spawn subagent for deep analysis, return 3 OPTIONS |
| **Q (Quit)** | Tasks already persisted in TodoWrite, just exit |

## Item Type Handling

| Type | Icon | After Processing |
|------|------|------------------|
| Clipping | ✂️ | DELETE original |
| Transcription | 🎤 | MOVE to Archives |
| Attachment | 📎 | KEEP (linked) |

### For Clippings
```typescript
para_create({ template, title, dest: "03 Resources", args: {..., distilled: "false"}, content: {...} })
para_delete({ file: "00 Inbox/[original]", confirm: true })
```

### For Transcriptions
```typescript
para_create({ template, title, dest: "03 Resources", args: {..., distilled: "false"}, content: {...} })
para_rename({ from: "00 Inbox/[original]", to: "04 Archives/Transcriptions/[original]" })
```

### For Attachments
```typescript
// Use para scan CLI for PDF processing
para_create({ template: "resource", title, dest: "03 Resources", args: {..., distilled: "false"} })
// Attachment stays in place, linked via source field
```

**Note:** `distilled: false` marks the resource as not yet fully processed through progressive summarization. Use `/para-obsidian:distill-resource` to complete the distillation process and set `distilled: true`.
