---
name: meeting-from-transcription
description: Create meeting notes from transcription files. Extracts metadata (date, type, summary) and creates bi-directional links. Use when converting voice memo transcriptions (.md) or VTT files (.vtt) into structured meeting notes, or when asked to "create a meeting from a transcription".
context: fork
allowed-tools: Read, Bash, mcp__plugin_para-obsidian_para-obsidian__para_read, mcp__plugin_para-obsidian_para-obsidian__para_commit, mcp__plugin_para-obsidian_para-obsidian__para_frontmatter_set, mcp__plugin_para-obsidian_para-obsidian__para_index_prime, mcp__plugin_para-obsidian_para-obsidian__para_index_query, AskUserQuestion
---

# Meeting from Transcription

Create meeting notes from transcription sources with intelligent metadata extraction.

## Input Detection

| Input | Action |
|-------|--------|
| No argument | Query inbox for transcriptions, show list |
| `.vtt` file | Convert first, **requires --date** |
| `.md` file | Validate `type: transcription` |
| Bare name | Expand to `00 Inbox/<name>.md` |

## Workflow

### Step 1: Resolve Input

**No input provided:**

First, prime the index to ensure it's up-to-date:
```
para_index_prime({ dir: "00 Inbox", response_format: "json" })
```

Then query for transcriptions:
```
para_index_query({ frontmatter: "type=transcription", dir: "00 Inbox", response_format: "json" })
```

- If transcriptions found → Display numbered list with `recorded` dates, then stop
- If none found → Use `AskUserQuestion` to prompt for file path

**Input provided:**
- `.vtt` extension → See [vtt-conversion.md](references/vtt-conversion.md) — **REQUIRES `--date` flag**
- `.md` or bare name → Continue to Step 2

**Path expansion:** If no `/` in path, prepend `00 Inbox/`. If no `.md` extension, append it.

### Step 2: Read & Validate Transcription

```
para_read({ file: "<PATH>", response_format: "json" })
```

**Validate frontmatter:**
- Has frontmatter block
- Has `type: transcription`
- Has `recorded` field OR user provided `--date`

On validation error → See [error-handling.md](references/error-handling.md)

**Extract:**
- `recorded` → Meeting datetime (or use `--date` override)
- `summary` → Use if present, otherwise generate from content
- Body content → Everything AFTER the `---` frontmatter block

### Step 3: Determine Meeting Type

If `--type` override provided, use it. Otherwise infer from transcript content.

See [meeting-types.md](references/meeting-types.md) for enum values and inference signals.

### Step 3b: Determine Area or Project

**REQUIRED:** Meeting notes must have either `area` or `project` in frontmatter.

1. Check transcription frontmatter for existing `area` or `project` field
2. If present → Use that value (already a wikilink)
3. If not present → Use `AskUserQuestion` to ask user:
   - "Which area or project does this meeting belong to?"
   - Provide options based on context from the transcript content
   - Include "Other" option for custom input

The value must be a wikilink format: `[[Area Name]]` or `[[Project Name]]`

### Step 4: Commit Uncommitted Changes

```
para_commit({ response_format: "json" })
```

### Step 5: Create Meeting Note

```bash
cd ${CLAUDE_PLUGIN_ROOT} && bun src/cli.ts create \
  --template meeting \
  --source-text "<TRANSCRIPT_BODY>" \
  --arg "meeting_date=<DATE>" \
  --arg "meeting_type=<TYPE>" \
  --arg "transcription=[[<NOTE_NAME>]]" \
  --arg "summary=<SUMMARY>" \
  --arg "area=[[<AREA_NAME>]]"
```

Or if project instead of area:
```bash
  --arg "project=[[<PROJECT_NAME>]]"
```

**Arguments:**
- `meeting_date` — ISO format: `YYYY-MM-DDTHH:mm:ss`
- `meeting_type` — One of: `1-on-1`, `standup`, `planning`, `retro`, `review`, `interview`, `stakeholder`, `general`
- `transcription` — Note name WITHOUT path or `.md` extension, wrapped in `[[...]]`
- `summary` — Concise 1-line description (max 100 chars)
- `area` OR `project` — **REQUIRED** (one of these must be provided) — Wikilink to parent area or project

### Step 6: Link Transcription to Meeting

Extract meeting filename from CLI output, then:

```
para_frontmatter_set({
  file: "<TRANSCRIPTION_PATH>",
  set: { "meeting": "[[<MEETING_NOTE_NAME>]]" },
  response_format: "json"
})
```

### Step 7: Final Commit

```
para_commit({ response_format: "json" })
```

### Step 8: Report Results

Return:
- Meeting note path created
- Meeting type (inferred or overridden)
- Summary used
- Confirmation of bi-directional links

---

## References

Load as needed based on input type or errors:

- **VTT files**: [references/vtt-conversion.md](references/vtt-conversion.md) — Conversion command, date requirement
- **Meeting types**: [references/meeting-types.md](references/meeting-types.md) — Enum values, inference rules
- **Errors**: [references/error-handling.md](references/error-handling.md) — Validation errors, recovery steps
