---
name: devonthink
description: |
  Automate DEVONthink on macOS via JXA (JavaScript for Automation) and Python. Use this skill when:
  - Creating, searching, organizing, or managing records in DEVONthink databases
  - Working with documents, notes, bookmarks, groups, PDFs, or web archives
  - Adding/removing tags, moving/duplicating/replicating records
  - Converting documents between formats (markdown, PDF, HTML, rich text)
  - Importing files/URLs or exporting records
  - Using DEVONthink's AI features (classification, similarity, summarization)
  - Querying record metadata, content, or properties
  - Looking up citation keys from bibliography JSON exports
  - Finding DEVONthink records by citation key
  Triggers: "DEVONthink", "DT3", "DEVONthink database", "organize documents", "document management", "citation key", "bibliography", "Zotero"
---

# DEVONthink Automation

Automate DEVONthink via JXA scripts executed with `osascript -l JavaScript`.

## Quick Start

```javascript
osascript -l JavaScript << 'EOF'
(() => {
  const app = Application("DEVONthink");
  app.includeStandardAdditions = true;

  // Your code here
  return JSON.stringify({ success: true });
})();
EOF
```

## Common Workflows

### 1. Get Citation Key of a DEVONthink Record

Given a DEVONthink record, find its Zotero citation key:

```bash
# Using the record's file path
python3 scripts/bib_lookup.py --path "~/Library/Mobile Documents/com~apple~CloudDocs/Zotero/Pastoralism/journalArticle/Gkartzios - 2023 - Editorial. Counterurbanisation, Again.pdf"
```

**Output:**

```json
{
  "success": true,
  "citationKey": "gkartzios2023",
  "title": "Editorial. Counterurbanisation, again..."
}
```

### 2. Find DEVONthink Record by Citation Key

Given a citation key (e.g., `@gkartzios2023`), find the matching DEVONthink record:

```bash
python3 scripts/bib_lookup.py --citation-key "gkartzios2023" --find-devonthink
```

**Output:**

```json
{
  "success": true,
  "citationKey": "gkartzios2023",
  "title": "Editorial. Counterurbanisation, again...",
  "devonthinkRecords": [
    {
      "uuid": "E1DF0C33-D4C8-4ECA-9890-81B012EFDD49",
      "name": "Gkartzios - 2023 - Editorial. Counterurbanisation, Again",
      "path": "~/Library/Mobile Documents/com~apple~CloudDocs/Zotero/Pastoralism/journalArticle/Gkartzios - 2023 - Editorial....pdf",
      "recordType": "PDF document"
    }
  ]
}
```

### 3. Get Full Content of a DEVONthink Record

Read the full text of any record (PDF, markdown, HTML, etc.). DEVONthink automatically extracts/OCRs text from PDFs.

```bash
osascript -l JavaScript << 'EOF'
(() => {
  const app = Application("DEVONthink");
  try {
    const record = app.getRecordWithUuid("E1DF0C33-D4C8-4ECA-9890-81B012EFDD49");
    if (!record) {
      return JSON.stringify({ success: false, error: "Record not found" });
    }
    const result = {};
    result["name"] = record.name();
    result["recordType"] = record.recordType();
    result["plainText"] = record.plainText();
    return JSON.stringify(result);
  } catch (e) {
    return JSON.stringify({ success: false, error: e.toString() });
  }
})();
EOF
```

**Tip:** Combine workflows 2 and 3 to read a document by citation key:

1. `bib_lookup.py --citation-key "gkartzios2023" --find-devonthink` → get UUID
2. Use UUID in JXA script → get full text content

## Core Operations

### Search Records

```javascript
const results = app.search("invoice 2024", { in: app.currentDatabase() });
// Filter: kind:pdf, kind:markdown, kind:!group, name:~keyword
// Dates: created:Yesterday, created:#3days, created>=2026-01-01
```

### Create Record

```javascript
const record = app.createRecordWith({
  name: "New Note",
  type: "markdown",  // or: group, bookmark, formatted note, txt, rtf
  content: "# Hello\n\nContent here"
}, { in: app.currentGroup() });
```

### Get Record by UUID/ID

```javascript
const record = app.getRecordWithUuid("UUID-HERE");
// Or by ID (requires database context):
const db = app.databases().find(d => d.name() === "MyDB");
const record = db.getRecordWithId(12345);
```

### Move/Duplicate/Replicate

```javascript
app.move({ record: theRecord, to: destinationGroup });
app.duplicate({ record: theRecord, to: destinationGroup });
app.replicate({ record: theRecord, to: destinationGroup }); // Same DB only
```

### Tags

```javascript
const tags = record.tags();           // Get tags
record.tags = ["tag1", "tag2"];       // Set tags (replaces all)

// Add a tag
const current = record.tags();
record.tags = [...current, "newTag"];

// Remove a tag
record.tags = record.tags().filter(t => t !== "oldTag");
```

### Delete

```javascript
app.delete({ record: theRecord });
```

### Rename Record

```javascript
record.name = "New Name";
```

### Get Record Content

```javascript
const text = record.plainText();      // Plain text content
const rich = record.richText();       // Rich text content
const html = record.source();         // HTML source (for HTML/webarchive)
```

### Update Record Content

```javascript
record.plainText = "New content";     // For text-based records
record.source = "<html>...</html>";   // For HTML records
```

### Get Selected Records

```javascript
const selected = app.selectedRecords();
selected.forEach(r => {
  // Process each selected record
});
```

### List Group Content

```javascript
const group = app.getRecordWithUuid("GROUP-UUID");
const children = group.children();
children.forEach(child => {
  // Process each child record
});
```

## Record Properties

| Property | Type | R/W | Description |
| ---------- | ------ | ----- | ------------- |
| `id` | Number | R | Database-specific ID |
| `uuid` | String | R | Globally unique identifier |
| `name` | String | RW | Record name |
| `path` | String | R | Filesystem path |
| `location` | String | R | DEVONthink location path |
| `recordType` | String | R | group, markdown, PDF document, etc. |
| `plainText` | String | RW | Plain text content |
| `richText` | RichText | RW | Rich text content |
| `source` | String | RW | HTML/XML source |
| `tags` | Array | RW | Record tags |
| `creationDate` | Date | RW | Creation date |
| `modificationDate` | Date | RW | Last modified |
| `size` | Number | R | Size in bytes |
| `comment` | String | RW | Record comment |
| `label` | Number | RW | Label index (0-7) |
| `rating` | Number | RW | Rating (0-5) |
| `flag` | Boolean | RW | Flagged state |
| `unread` | Boolean | RW | Unread state |

## Record Types

`group`, `smart group`, `markdown`, `txt`, `rtf`, `rtfd`, `formatted note`, `HTML`, `webarchive`, `PDF document`, `picture`, `multimedia`, `bookmark`, `feed`, `sheet`, `XML`, `unknown`

## Convert Formats

```javascript
app.convert({ record: theRecord, to: "markdown" });
// Formats: simple, rich, note, markdown, HTML, webarchive,
//          PDF document, single page PDF document
```

## Web Import

```javascript
app.createMarkdownFrom("https://example.com", { in: app.currentGroup() });
app.createPDFDocumentFrom("https://example.com", { in: app.currentGroup() });
app.createFormattedNoteFrom("https://example.com", { in: app.currentGroup() });
app.createWebDocumentFrom("https://example.com", { in: app.currentGroup() });
```

## AI Features

```javascript
// Classification suggestions
const proposals = app.classify({ record: theRecord });

// Find similar records
const similar = app.compare({ record: theRecord });

// Chat/summarize (requires AI config in DEVONthink)
const response = app.getChatResponseForMessage("Summarize this", {
  record: theRecord, temperature: 0
});
```

## Database Navigation

```javascript
const dbs = app.databases();                    // All open databases
const db = app.currentDatabase();               // Current database
const root = db.root();                         // Root group
const incoming = db.incomingGroup();            // Inbox
const trash = db.trashGroup();                  // Trash
```

## Lookup Records

```javascript
app.lookupRecordsWithFile("report.pdf", { in: db });
app.lookupRecordsWithTags(["important", "work"], { in: db });
app.lookupRecordsWithComment("review needed", { in: db });
app.lookupRecordsWithURL("https://example.com", { in: db });
app.lookupRecordsWithPath("/path/to/file.pdf", { in: db });
app.lookupRecordsWithContentHash("hash-value", { in: db });
```

## Custom Metadata

```javascript
app.addCustomMetaData("John Doe", { for: "author", to: record });
const author = app.getCustomMetaData({ for: "author", from: record });
```

## Bibliography Lookup (Zotero Integration)

Look up citation keys from Zotero CSL JSON exports using the bundled Python script.

### Get Citation Key by File Path

```bash
python3 scripts/bib_lookup.py --path "/path/to/document.pdf"
```

### Get Metadata by Citation Key

```bash
python3 scripts/bib_lookup.py --citation-key "smith2024"
```

### Find DEVONthink Records by Citation Key

```bash
python3 scripts/bib_lookup.py --citation-key "smith2024" --find-devonthink
```

**Options:**

- `--path`: File path to look up
- `--citation-key`: Citation key to look up
- `--bib-json`: Override path to Zotero JSON export (or set `BIBLIOGRAPHY_JSON` env var)
- `--find-devonthink`: Also search DEVONthink for matching records
- `--full`: Include complete bibliography item in output

## JXA Best Practices

1. **Build objects with bracket notation** (avoid inline object literals in returns):

```javascript
const result = {};
result["success"] = true;
result["data"] = someData;
return JSON.stringify(result);
```

2. **Never use console.log** - causes stdio errors

3. **Wrap in try-catch** and return JSON:

```javascript
try {
  // operations
  return JSON.stringify({ success: true, data: result });
} catch (e) {
  return JSON.stringify({ success: false, error: e.toString() });
}
```

4. **DEVONthink paths vs filesystem paths**: Use `location()` for DEVONthink internal paths, `path()` for filesystem paths.

## Search Query Syntax

```
kind:pdf                    # By type
kind:!group                 # Exclude groups
name:~invoice              # Name contains
created:Yesterday          # Date shortcuts
created:#3days             # Last 3 days
created>=2026-01-01        # Date range
kind:pdf created:#1week    # Combined
```

## References

- **Full JXA API**: See [references/jxa-api.md](references/jxa-api.md) for complete command and property reference
