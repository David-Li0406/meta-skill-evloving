# File Operations

Upload, download, and manage files on the Restspace server.

**Important:** File service paths must be discovered dynamically - they are NOT always at `/files`.

## Step 1: Find File Services

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# List all file services with their paths and names
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("file.rsm"))) | .[] | {path: .key, name: .value.name}'
```

Example output:
```json
{"path": "/files", "name": "Main File Storage"}
{"path": "/uploads", "name": "User Uploads"}
{"path": "/assets", "name": "Static Assets"}
```

## Step 2: Select File Service

**If multiple file services exist**, present them to the user and ask which to use.

**If user specifies a path** in their prompt, use that path directly.

```bash
# Get the first file service (or use user-specified path)
FILE_PATH=$(curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq -r 'to_entries | map(select(.value.source | contains("file.rsm"))) | .[0].key // empty')
```

## Operations

All operations use the discovered `$FILE_PATH`.

### Upload File

```bash
# Upload from local file
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/documents/report.pdf" \
  -H "Content-Type: application/pdf" \
  --data-binary @report.pdf

# Upload text content directly
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/notes/readme.txt" \
  -H "Content-Type: text/plain" \
  -d "This is the file content"

# Upload JSON file
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/config/settings.json" \
  -H "Content-Type: application/json" \
  -d '{"theme": "dark", "language": "en"}'
```

**Response (200 OK or 201 Created)**

### Download File

```bash
# Download to local file
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/documents/report.pdf" -o report.pdf

# View text file content
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/notes/readme.txt"

# Download and pipe to another command
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/config/settings.json" | jq '.'
```

### List Directory

```bash
# List files in directory (note trailing slash)
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/documents/"
```

**Response (200 OK):**
```json
[
  {
    "name": "report.pdf",
    "size": 102400,
    "modified": "2024-01-15T10:30:00Z"
  },
  {
    "name": "notes/",
    "isDirectory": true
  }
]
```

### Delete File

```bash
curl -s -b cookies.txt -X DELETE "$RESTSPACE_URL$FILE_PATH/documents/report.pdf"
```

**Response (200 OK)**

## Complete Example

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# 1. Discover file services
echo "Available file services:"
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("file.rsm"))) | .[] | {path: .key, name: .value.name}'

# 2. Use specific service (replace with discovered path)
FILE_PATH="/files"

# 3. List root directory
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/" | jq '.'

# 4. Upload a file
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/test.txt" \
  -H "Content-Type: text/plain" \
  -d "Hello, World!"

# 5. Download it back
curl -s -b cookies.txt "$RESTSPACE_URL$FILE_PATH/test.txt"
```

## Common MIME Types

| Extension | Content-Type |
|-----------|--------------|
| `.txt` | `text/plain` |
| `.html` | `text/html` |
| `.css` | `text/css` |
| `.js` | `application/javascript` |
| `.json` | `application/json` |
| `.pdf` | `application/pdf` |
| `.png` | `image/png` |
| `.jpg` | `image/jpeg` |
| `.zip` | `application/zip` |

## Working with Binary Files

Always use `--data-binary` for binary files to preserve content:

```bash
# Correct - preserves binary data
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/images/photo.jpg" \
  -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg

# Incorrect - may corrupt binary files
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$FILE_PATH/images/photo.jpg" \
  -H "Content-Type: image/jpeg" \
  -d @photo.jpg
```

## Notes

- File paths are relative to the service's configured root
- Allowed extensions may be restricted by server configuration
- Large files support range requests for partial downloads
- ZIP uploads can be auto-extracted (depends on configuration)
- Some servers may have multiple file services for different purposes (uploads, assets, etc.)
