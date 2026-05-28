---
name: update-timeline
description: Update the chronological events index with deep understanding of transcripts, messages, and communications. Use when user says "update timeline", "index events", or "process transcripts".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Update Timeline Skill

Update `analysis/events-chronological.md` with deep understanding of all project communications.

## Source Registry

This skill uses a source registry to detect and parse different data formats.

### Loading Sources

1. Read `sources/_registry.json` from this skill directory
2. For each registered source, check if `detectPattern` matches any files
3. Track which sources are present

### Unknown Source Detection

After checking registered sources, scan `unknownDataPaths` for directories not in the registry:

```markdown
Warning: Unknown data sources detected:
- data/messaging/telegram/ (not in registry)
- data/raw/linear/ (not in registry)

To add support, document the format in source-formats.md and add to sources/_registry.json
```

Continue processing known sources, but warn about unknown ones.

## Execution Steps (FOLLOW EXACTLY)

### Step 1: Load State (EXACT)
```
Read `.claude/state/timeline-state.json`
If file doesn't exist → treat all files as new
Parse JSON → store in memory as `state`
```

### Step 2: Discover Sources (EXACT)
```
Run: Glob("data/transcripts/hyprnote/*/_meta.json") → hyprnote_sessions
Run: Glob("data/transcripts/notion/*.md") → notion_files (exclude readme.md)
Run: Glob("data/messaging/whatsapp/*/_chat.txt") → whatsapp_chats
Run: Glob("data/messaging/hailer/*.md") → hailer_files (exclude readme.md)
```

### Step 3: Build Unified Source List (EXACT)
```
For each hyprnote session:
  - Read _meta.json → extract created_at
  - Add to sources: {type: "hyprnote", date: created_at, path: folder_path}

For each notion file:
  - Extract date from filename (YYYY-MM-DDTHH_MM_SSZ.md)
  - Add to sources: {type: "notion", date: extracted_date, path: file_path}

For whatsapp:
  - Add to sources: {type: "whatsapp", date: "continuous", path: folder_path}

For hailer:
  - Add to sources: {type: "hailer", date: "continuous", path: folder_path}

Sort sources by date DESCENDING (newest first)
```

### Step 4: Identify Changes (EXACT)
```
For each source in sorted list:
  If type == "hyprnote" or type == "notion":
    If path NOT in state.processed_files[type] → mark as NEW
    Else if file mtime > state.processed_files[type][path].processed_at → mark as CHANGED

  If type == "whatsapp":
    Read first 100 chars of _chat.txt
    If chars != state.whatsapp.file_hash → mark as CHANGED (re-process ALL)

  If type == "hailer":
    For each file in hailer_files:
      Read first 100 chars
      If chars != state.hailer.files[path].file_hash → mark as CHANGED (re-process ALL)
```

### Step 5: Process Each Source (PRESCRIPTIVE + INTERPRETIVE)

**For Hyprnote (EXACT steps, then INTERPRET):**
```
1. Read _meta.json → extract title, created_at
2. Read _transcript.json → extract transcripts[0].words array
3. Reconstruct text: words.map(w => w.text).join('').trim()
4. Group words by channel field (speaker separation)
5. Check if _memo.md exists → if yes, read it
6. [INTERPRET] Write 2-4 sentence summary using transcript + memo
7. [INTERPRET] Extract decisions, action items, key insights
8. [INTERPRET] Identify participants and roles
9. [INTERPRET] Rate relevance (High/Medium/Low)
```

**For Notion (EXACT steps, then INTERPRET):**
```
1. Read entire .md file
2. [INTERPRET] Identify speakers from text patterns
3. [INTERPRET] Write 2-4 sentence summary
4. [INTERPRET] Extract decisions, action items, key insights
5. [INTERPRET] Identify participants and roles
6. [INTERPRET] Rate relevance
```

**For WhatsApp (EXACT steps, then INTERPRET):**
```
1. Read entire _chat.txt
2. Parse messages: regex [MM/DD/YY, HH:MM:SS] Sender: Message
3. List all attachments in folder
4. For each image attachment → Read image, describe visual content
5. For each document (.pdf, .md, .docx) → Read and summarize
6. [INTERPRET] Group messages into topic clusters (time gaps >24h, topic shifts)
7. [INTERPRET] For each cluster: write summary, list key events
8. [INTERPRET] Rate relevance per cluster
```

**For Hailer (EXACT steps, then INTERPRET):**
```
1. Read ALL .md files in folder
2. Parse message format (Username, timestamp, content)
3. Combine into chronological order
4. [INTERPRET] Group into topic clusters
5. [INTERPRET] Write summary, extract key points
6. [INTERPRET] Identify participants
7. [INTERPRET] Rate relevance
```

### Step 6: Generate Output (EXACT)
```
1. Sort all processed entries by date ASCENDING (oldest first for output)
2. Group by month
3. Write to analysis/events-chronological.md using output-template.md format
4. Include YAML frontmatter with counts
```

### Step 7: Validate Output (EXACT CHECKLIST)
```
Before finishing, verify each entry has:
- [ ] Substantive summary (not just "Meeting occurred" or title repeat)
- [ ] At least one of: decision, action item, or key insight
- [ ] Participants listed
- [ ] Relevance rating

For Hyprnote with _memo.md:
- [ ] Memo content incorporated in entry

For WhatsApp:
- [ ] All images have visual descriptions
- [ ] All documents have content summaries
- [ ] Clusters have date ranges

If any check fails → fix before proceeding
```

### Step 8: Update State (EXACT)
```
Update state.last_updated = current ISO timestamp
For each processed source:
  Add/update entry in state.processed_files with:
    - processed_at: current timestamp
    - deep_processed: true
    - summary: first 100 chars of generated summary
Write state to .claude/state/timeline-state.json
```

## Supporting Files

- [Processing Rules](processing-rules.md) - Deep understanding guidelines
- [Source Formats](source-formats.md) - Parsing reference
- [Output Template](output-template.md) - Entry format specification
