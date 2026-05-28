---
name: google-drive
description: Download and sync files from Google Drive. Supports automatic format conversion for Docs, Sheets, and Slides.
---

# Google Drive Skill

This skill allows you to interact with Google Drive to download and update files using direct REST API calls.

## Prerequisites

1.  **Authentication**: The script requires a valid Google Cloud Access Token.
    - You can obtain one using the `gcloud` CLI: `gcloud auth print-access-token`.
    - Pass this token to the script via the `GCLOUD_ACCESS_TOKEN` environment variable.

## Capabilities

### 1. Download a File

Downloads a file from Google Drive.
- **Docs** are converted to Markdown (text/plain) or DOCX.
- **Sheets** are converted to CSV.
- **Slides** are converted to PDF.
- **Binary files** (images, PDFs) are downloaded as-is.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-drive/scripts/drive.js download <FILE_ID> [OPTIONAL_FORMAT]
```
*   `FILE_ID`: The ID of the file in Google Drive.
*   `OPTIONAL_FORMAT`: (Optional) Mime type to export to (e.g., `text/csv`, `application/pdf`).

**Output:**
The file will be saved as `Sanitized_Name.FILE_ID.ext`.

### 2. Refresh a File

Updates a local file with the latest version from Drive. It extracts the File ID from the filename.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-drive/scripts/drive.js refresh <LOCAL_FILENAME>
```
*   `LOCAL_FILENAME`: The path to the local file (must follow the `Name.ID.ext` pattern).

### 3. Upload a File

Uploads a local file to Google Drive.
- **Markdown (.md)** files are automatically converted to **Google Docs**.
- **CSV (.csv)** files are automatically converted to **Google Sheets**.
- Other files are uploaded as-is.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-drive/scripts/drive.js upload <LOCAL_FILE_PATH> [--rename]
```
*   `LOCAL_FILE_PATH`: The path to the file you want to upload.
*   `--rename`: (Optional) If provided, renames the local file to `Name.ID.ext` upon successful upload.

**Output:**
Prints the new File ID and the WebView Link.

### 4. Update a File

Replaces the content of an existing file in Google Drive with the content of a local file. The target file ID is extracted from the local filename (which must follow the `Name.ID.ext` pattern, similar to `refresh`).
- If the local file is **Markdown**, it will update the target **Google Doc** content.
- If the local file is **CSV**, it will update the target **Google Sheet** content.

**Usage:**
```bash
export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token)
node skills/google-drive/scripts/drive.js update <LOCAL_FILENAME>
```
*   `LOCAL_FILENAME`: The path to the local file (must follow the `Name.ID.ext` pattern).

## Example Workflow

User: "Download the file 1234abcd"
Model:
1.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-drive/scripts/drive.js download 1234abcd`

User: "Refresh Project_Plan.1234abcd.md"
Model:
1.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-drive/scripts/drive.js refresh Project_Plan.1234abcd.md`

User: "Upload meeting_notes.md"
Model:
1.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-drive/scripts/drive.js upload meeting_notes.md`

User: "Update the budget sheet budget_v1.1234abcd.csv"
Model:
1.  Run: `export GCLOUD_ACCESS_TOKEN=$(gcloud auth print-access-token) && node skills/google-drive/scripts/drive.js update budget_v1.1234abcd.csv`
