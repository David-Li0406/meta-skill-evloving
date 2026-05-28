---
name: google-docs
description: Read, create, and edit Google Docs and comments. Supports granular editing via API requests.
---

# Google Docs Skill

This skill allows you to interact with Google Docs to read content, create new documents, make granular edits, and manage comments.

## Prerequisites

1.  **Authentication**: The script requires a valid Google Cloud Access Token.
    - You can obtain one using the `gcloud` CLI: `gcloud auth print-access-token`.
    - Pass this token to the script via the `GCLOUD_ACCESS_TOKEN` environment variable.

## Capabilities

### 1. Read a Document

Retrieves the JSON representation of a Google Doc. By default, it returns the content of the first tab. You can optionally specify a `tabId` to retrieve a specific tab's content.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
# Read the default (first) tab
node skills/google-docs/scripts/docs.js read <DOC_ID>
# Read a specific tab
node skills/google-docs/scripts/docs.js read <DOC_ID> --tabId=<TAB_ID>
```

### 2. List Tabs

Lists all tabs in a document, including their titles and `tabId`s. Useful for finding the correct `tabId` to use in an edit request.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js tabs <DOC_ID>
```

### 3. Create a Document

Creates a new blank Google Doc with the specified title.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js create "<TITLE>"
```

### 4. Edit a Document (Granular Edits)

Performs batch updates on a document. You can insert text, delete text, apply styles, etc.
You must provide a valid JSON string representing the `requests` array for the `documents.batchUpdate` method.

**Multi-tab Support:** To target a specific tab, include the `tabId` field in the request object. If `tabId` is omitted, the request applies to the first tab (or all tabs for certain request types like `replaceAllText`).

**File Injection (New!):** You can upload local files (images, etc.) as part of the edit request.
- Use the flag `--file-<ID>=<PATH>` to specify a file.
- In your JSON request, use `FILE_<ID>` as the placeholder for the file's URL.
- The script will automatically upload the file, make it public, replace the placeholder with the public URL, execute the request, and then delete the temporary file from Drive.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js edit <DOC_ID> '<JSON_REQUESTS>' [--file-<ID>=<PATH> ...]
```

**Example JSON Request (Insert Text into a Specific Tab):**
```json
[
  {
    "insertText": {
      "text": "Hello Tab",
      "location": {
        "index": 1,
        "tabId": "TAB_ID_HERE"
      }
    }
  }
]
```

**Example: Replacing an Image**
```bash
node skills/google-docs/scripts/docs.js edit <DOC_ID> \
  '[{"replaceImage": {"imageObjectId": "kix.abc123xyz", "uri": "FILE_MY_IMG"}}]' \
  --file-MY_IMG=./new_image.png
```

**Example JSON Request (Insert Text):**
```json
[
  {
    "insertText": {
      "text": "Hello World",
      "location": {
        "index": 1
      }
    }
  }
]
```

**Note:** The JSON argument can be a single request object or an array of request objects.

**Important:** When using `insertText`, the `index` must be **strictly less than** the segment's end index. For example, if a paragraph ends at index 16, the maximum valid insertion index is 15. Attempting to insert at the end index (16) will result in an error.

### 4. Append to Document

To safely append text to the end of the document without calculating indices, use `endOfSegmentLocation`.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js edit <DOC_ID> '<JSON_REQUESTS>'
```

**Example JSON Request (Append):**
```json
[
  {
    "insertText": {
      "text": "\nAppended text.",
      "endOfSegmentLocation": {
        "segmentId": ""
      }
    }
  }
]
```
*   `segmentId`: Use `""` (empty string) for the main body.

### 5. Read Comments

Retrieves the list of comments for a specific document (or any Drive file).

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js comments <DOC_ID>
```

### 6. Create a Comment

Creates a new comment on a document.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js create_comment <DOC_ID> "<CONTENT>" [ANCHOR_JSON]
```

*   `ANCHOR_JSON`: Optional. A JSON string specifying the region of the document to comment on.

### 7. Reply to a Comment

Replies to an existing comment.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js reply_comment <DOC_ID> <COMMENT_ID> "<CONTENT>"
```

### 8. Resolve a Comment

Resolves a comment.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js resolve_comment <DOC_ID> <COMMENT_ID>
```

### 9. Insert Image from Local File

Uploads a local image file to Google Drive, makes it temporarily accessible, and inserts it into the Google Doc at the specified index. Can target a specific tab.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js insert_image <DOC_ID> <LOCAL_FILE_PATH> <INDEX> [WIDTH] [HEIGHT] [--tabId=TAB_ID]
```

*   `INDEX`: The 0-based index in the document where the image should be inserted.
*   `WIDTH` / `HEIGHT`: (Optional) Size in points (PT).
*   `--tabId`: (Optional) The ID of the tab to insert the image into. If omitted, the image is inserted into the main body of the first tab.

### 10. Create a Tab

Creates a new tab in the document.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-docs/scripts/docs.js create_tab <DOC_ID> "[TITLE]" [--parentTabId=ID] [--index=N] [--emoji=EMOJI]
```

*   `TITLE`: (Optional) The title of the new tab. Defaults to "New Tab".
*   `--parentTabId=ID`: (Optional) The ID of the parent tab to nest the new tab under.
*   `--index=N`: (Optional) The 0-based index for the tab position.
*   `--emoji=EMOJI`: (Optional) An emoji to use as the tab icon.

## Example Workflow

User: "Read the doc with ID 12345"
Model:
1.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-docs/scripts/docs.js read 12345`

User: "Add 'Summary' to the beginning of doc 12345"
Model:
1.  Construct JSON: `[{"insertText": {"text": "Summary\n", "location": {"index": 1}}}]`
2.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-docs/scripts/docs.js edit 12345 '[{"insertText": {"text": "Summary\n", "location": {"index": 1}}}]'`
