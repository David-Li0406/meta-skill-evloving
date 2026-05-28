# Source Format Reference

## Hyprnote (`data/transcripts/hyprnote/*/`)

### Files per session:
- `_meta.json` - Session metadata
- `_transcript.json` - Word-by-word transcript
- `_memo.md` - Human notes (optional, ~30% have this)

### _meta.json schema:
```json
{
  "created_at": "ISO timestamp",
  "id": "uuid",
  "participants": [],
  "title": "string or empty",
  "user_id": "uuid"
}
```

### _transcript.json schema:
```json
{
  "transcripts": [{
    "words": [
      {
        "channel": 0,        // Speaker identifier
        "text": " word",     // Single word with leading space
        "start_ms": 1234,    // Timing
        "end_ms": 1456
      }
    ]
  }]
}
```

### Transcript reconstruction:
```
words.map(w => w.text).join('').trim()
```

Group by channel for speaker separation.

### _memo.md format:
```yaml
---
id: uuid
session_id: uuid
type: memo
---

[Human-written notes in Finnish/English]
```

---

## Notion (`data/transcripts/notion/*.md`)

Plain markdown files. Filename is timestamp: `2025-12-12T01_00_00Z.md`

Content is meeting transcript, often with speaker names and timestamps embedded in text.

---

## WhatsApp (`data/messaging/whatsapp/*/`)

### Folder naming:
`WhatsApp Chat - [GroupName]-[ExportTimestamp]/`

### Files:
- `_chat.txt` - Full chat export
- Various attachments (images, PDFs, documents)

### Chat format:
```
[MM/DD/YY, HH:MM:SS] Sender: Message content
[MM/DD/YY, HH:MM:SS] Sender: ‎<attached: filename.jpg>
```

### Attachment naming:
`00000XXX-[original-name].[ext]`

---

## Hailer (`data/messaging/hailer/*.md`)

Raw copy-paste from Hailer platform. Format:

```
Username
HH:MM
Message content

Username
HH:MM
Another message
```

Filename timestamp is upload date, not message date.
