# DEVONthink JXA API Reference

Complete reference for DEVONthink JavaScript for Automation commands and properties.

## Table of Contents

1. [Database Management](#database-management)
2. [Record Management](#record-management)
3. [Search & Classification](#search--classification)
4. [Lookup Commands](#lookup-commands)
5. [Web Content](#web-content)
6. [Import & Export](#import--export)
7. [Metadata](#metadata)
8. [AI Features](#ai-features)
9. [Windows & UI](#windows--ui)
10. [Record Properties](#record-properties)
11. [Database Properties](#database-properties)
12. [Enumerations](#enumerations)

---

## Database Management

### createDatabase(path, [encryptionKey], [size])

Creates a new database.

- `path`: String - POSIX path (suffix: .dtBase2, .dtSparse, .dtArchive)
- `encryptionKey`: String (optional)
- `size`: Number (optional) - Max size in MB for encrypted DBs
- Returns: Database or null

### openDatabase(path)

Opens an existing database.

- `path`: String - POSIX path
- Returns: Database or null

### checkFileIntegrityOf({database})

Checks file integrity.

- Returns: Number - Count of files with invalid hash

### optimize({database})

Backup & optimize database.

- Returns: Boolean

### verify({database})

Verifies database.

- Returns: Number - Error count

### compress({database, [password], to})

Compresses to Zip.

- `to`: String - Destination path (.zip)
- Returns: Boolean

---

## Record Management

### createRecordWith(properties, [options])

Creates a new record.

```javascript
app.createRecordWith({
  name: "Note",
  type: "markdown",
  content: "# Title"
}, { in: destinationGroup });
```

- `properties`: Object (must include 'type')
- `options.in`: Parent group (optional)
- Returns: Record or null

### delete({record, [in]})

Deletes record(s).

- Returns: Boolean

### move({record, [from], to})

Moves record(s).

- Returns: Record(s) or null

### duplicate({record, to})

Duplicates record(s) to any database.

- Returns: Record(s) or null

### replicate({record, to})

Replicates record(s) within same database.

- Returns: Record(s) or null

### convert({record, [to], [in]})

Converts to different format.

- `to`: String - Target format (default: "simple")
- Returns: Record(s) or null

---

## Search & Classification

### search(query, [options])

Searches for records.

```javascript
app.search("invoice 2024", {
  in: app.currentDatabase(),
  comparison: "fuzzy",
  excludeSubgroups: false
});
```

- `comparison`: "no case" | "no umlauts" | "fuzzy" | "related"
- Returns: Array of Records

### showSearch(query)

Performs search in frontmost window.

- Returns: Boolean

### classify({record, [in], [comparison], [tags]})

Gets classification proposals.

- `tags`: Boolean - Propose tags instead of groups
- Returns: Array of Parents

### compare({[record], [content], [to], [comparison]})

Finds similar records.

- Returns: Array of Records

---

## Lookup Commands

### lookupRecordsWithFile(filename, [options])

Finds by filename.

- Returns: Array of Records

### lookupRecordsWithPath(path, [options])

Finds by path.

- Returns: Array of Records

### lookupRecordsWithURL(url, [options])

Finds by URL.

- Returns: Array of Records

### lookupRecordsWithTags(tags, [options])

Finds by tags.

- `options.any`: Boolean - Match any tag vs all
- Returns: Array of Records

### lookupRecordsWithComment(comment, [options])

Finds by comment.

- Returns: Array of Records

### lookupRecordsWithContentHash(hash, [options])

Finds by content hash.

- Returns: Array of Records

---

## Web Content

### createFormattedNoteFrom(url, [options])

Creates formatted note from URL.

```javascript
app.createFormattedNoteFrom("https://example.com", {
  in: app.currentGroup(),
  name: "Custom Name",
  readability: true
});
```

### createMarkdownFrom(url, [options])

Creates Markdown from URL.

### createPDFDocumentFrom(url, [options])

Creates PDF from URL.

- `options.pagination`: Boolean
- `options.width`: Number (points)

### createWebDocumentFrom(url, [options])

Creates web document from URL.

### downloadURL(url, [options])

Downloads raw data.

- `options.method`: HTTP method
- `options.post`: POST parameters
- Returns: Raw data

### downloadMarkupFrom(url, [options])

Downloads HTML/XML.

- Returns: String

### downloadJSONFrom(url, [options])

Downloads JSON.

- Returns: Object

---

## Import & Export

### importPath(path, [options])

Imports file or folder.

```javascript
app.importPath("/path/to/file.pdf", { to: app.currentGroup() });
```

- Returns: Record or null

### indexPath(path, [options])

Indexes (references) file or folder.

- Returns: Record or null

### export({record, to, [DEVONtech_Storage]})

Exports record.

- `to`: String - Destination directory
- Returns: String (export path)

### exportWebsite({record, to, [options]})

Exports as website.

- Returns: String (export path)

---

## Metadata

### addCustomMetaData(value, {for, to, [as]})

Adds custom metadata.

```javascript
app.addCustomMetaData("John", { for: "author", to: record });
```

- Returns: Boolean

### getCustomMetaData({[defaultValue], for, from})

Gets custom metadata.

```javascript
app.getCustomMetaData({ for: "author", from: record });
```

- Returns: Value or null

### addReminder(properties, {to})

Adds reminder.

```javascript
app.addReminder({
  schedule: "once",
  "due date": new Date(),
  alarm: "notification"
}, { to: record });
```

- Returns: Reminder or null

---

## AI Features

### getChatResponseForMessage(message, [options])

Gets AI chat response.

```javascript
app.getChatResponseForMessage("Summarize this", {
  record: theRecord,
  temperature: 0,
  engine: "Claude"
});
```

- `options.mode`: Content usage mode
- `options.model`: AI model
- `options.engine`: ChatGPT | Claude | Gemini | Ollama | etc.
- Returns: String or Object

### summarizeContentsOf({records, to, [as], [in]})

Summarizes content.

- `to`: Output format
- `as`: Summary style
- Returns: Record

### summarizeText(text, [options])

Summarizes text.

- Returns: String

### extractKeywordsFrom({record, [options]})

Extracts keywords.

- Returns: Array of Strings

---

## Windows & UI

### openTabFor({[record], [URL], [in]})

Opens new tab.

- Returns: Tab or null

### openWindowFor({record, [enforcement]})

Opens window for record.

- Returns: ThinkWindow or null

### displayGroupSelector([title], [options])

Shows group selector dialog.

- Returns: Parent or null

### displayNameEditor([title], [options])

Shows name editor.

- Returns: String or null

### showProgressIndicator(title, [options])

Shows progress.

- `options.steps`: Number
- Returns: Boolean

### stepProgressIndicator([info])

Updates progress.

- Returns: Boolean

### hideProgressIndicator()

Hides progress.

- Returns: Boolean

---

## Record Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `id` | Number | R | Database-specific ID |
| `uuid` | String | R | Globally unique ID |
| `name` | String | RW | Record name |
| `aliases` | String | RW | Wiki aliases |
| `comment` | String | RW | Comment |
| `tags` | Array | RW | Tags array |
| `label` | Number | RW | Label (0-7) |
| `rating` | Number | RW | Rating (0-5) |
| `flag` | Boolean | RW | Flagged state |
| `unread` | Boolean | RW | Unread state |
| `locking` | Boolean | RW | Lock state |
| `path` | String | R | Filesystem path |
| `location` | String | R | DEVONthink path |
| `recordType` | String | R | Record type |
| `kind` | String | R | Kind description |
| `mimeType` | String | R | MIME type |
| `plainText` | String | RW | Plain text content |
| `richText` | RichText | RW | Rich text content |
| `source` | String | RW | HTML/XML source |
| `data` | RawData | RW | File data |
| `size` | Number | R | Size in bytes |
| `creationDate` | Date | RW | Creation date |
| `modificationDate` | Date | RW | Modification date |
| `additionDate` | Date | R | Addition date |
| `database` | Database | R | Parent database |
| `duplicates` | Array | R | Duplicate records |
| `numberOfDuplicates` | Number | R | Duplicate count |
| `numberOfReplicants` | Number | R | Replicant count |
| `pageCount` | Number | R | Page count |
| `wordCount` | Number | R | Word count |
| `characterCount` | Number | R | Character count |
| `indexed` | Boolean | R | Is indexed |
| `url` | String | RW | Record URL |
| `referenceURL` | String | R | Reference URL |
| `thumbnail` | Any | RW | Thumbnail |
| `customMetaData` | Object | RW | Custom metadata |

---

## Database Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `id` | Number | R | Database ID |
| `uuid` | String | R | Database UUID |
| `name` | String | RW | Database name |
| `comment` | String | RW | Comment |
| `path` | String | R | Database path |
| `filename` | String | R | Filename |
| `root` | Parent | R | Root group |
| `incomingGroup` | Parent | R | Inbox group |
| `trashGroup` | Parent | R | Trash group |
| `tagsGroup` | Parent | R | Tags group |
| `encrypted` | Boolean | R | Is encrypted |
| `readOnly` | Boolean | R | Is read-only |
| `versioning` | Boolean | RW | Versioning enabled |
| `spotlightIndexing` | Boolean | RW | Spotlight indexing |

---

## Enumerations

### Record Types

`group`, `smart group`, `markdown`, `txt`, `rtf`, `rtfd`, `formatted note`, `HTML`, `webarchive`, `PDF document`, `picture`, `multimedia`, `bookmark`, `feed`, `sheet`, `XML`, `property list`, `AppleScript file`, `unknown`

### Convert Formats

`bookmark`, `simple`, `rich`, `note`, `markdown`, `HTML`, `webarchive`, `PDF document`, `single page PDF document`, `PDF without annotations`, `PDF with annotations burnt in`

### Search Comparison

`no case`, `no umlauts`, `fuzzy`, `related`

### Comparison Types

`data comparison`, `tags comparison`

### Reminder Alarms

`no alarm`, `dock`, `sound`, `speak`, `notification`, `alert`, `open internally`, `open externally`, `launch`, `mail with item link`, `mail with attachment`

### Reminder Schedules

`never`, `once`, `hourly`, `daily`, `weekly`, `monthly`, `yearly`

### AI Engines

`ChatGPT`, `Claude`, `Gemini`, `Ollama`, `Mistral AI`, `GPT4All`, `LM Studio`

### Labels

0 = None, 1-7 = Custom label colors (configurable in DEVONthink preferences)
