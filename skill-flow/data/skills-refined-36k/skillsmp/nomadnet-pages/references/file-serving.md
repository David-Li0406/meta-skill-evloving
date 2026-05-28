# NomadNet File Serving

Guide to hosting and serving files on NomadNet nodes.

## File Storage

### Default Location

```
~/.nomadnetwork/storage/files/
```

Configurable via `files_path` in `~/.nomadnetwork/config`.

### Directory Structure

Files in subdirectories map to URL paths:

```
~/.nomadnetwork/storage/files/
├── readme.txt            → :/file/readme.txt
├── docs/
│   ├── guide.pdf         → :/file/docs/guide.pdf
│   └── manual.pdf        → :/file/docs/manual.pdf
├── software/
│   ├── release.zip       → :/file/software/release.zip
│   └── source.tar.gz     → :/file/software/source.tar.gz
└── media/
    ├── logo.png          → :/file/media/logo.png
    └── banner.jpg        → :/file/media/banner.jpg
```

## URL Format

### Full URL (Remote Node)

```
<destination_hash>:/file/path/to/file.ext
```

Example:
```
e9eafceea9e3664a5c55611c5e8c420a:/file/docs/guide.pdf
```

### Local URL (Same Node)

```
:/file/path/to/file.ext
```

Example:
```
:/file/software/release.zip
```

## Creating Download Links

### Basic File Link

```micron
`[Download`:/file/document.pdf]
```

### Labeled File Link

```micron
`[User Guide (PDF)`:/file/docs/guide.pdf]
```

### Styled File Link

```micron
`F0af`_`[Download Release v1.0`:/file/software/release_v1.0.zip]`_`f
```

### File Listing Page

```micron
>Available Downloads

>>Documents
`[User Guide`:/file/docs/user_guide.pdf]
`[API Reference`:/file/docs/api_reference.pdf]
`[Changelog`:/file/docs/changelog.txt]

>>Software
`[Latest Release`:/file/software/latest.zip]
`[Source Code`:/file/software/source.tar.gz]
```

## File Transfer

### Transfer Behavior

- Files are transferred over Reticulum links
- Large files (>32MB) are automatically compressed during transfer
- Progress tracking available in client UI
- Resumable downloads via file receipts

### Client Download Location

Downloaded files are saved to:
```
~/.nomadnetwork/downloads/
```

Configurable via `downloads_path` in config.

## File Types

### Supported File Types

Any file type can be served. Common uses:

| Type | Extension | Use Case |
|------|-----------|----------|
| Documents | `.pdf`, `.txt`, `.md` | Documentation |
| Archives | `.zip`, `.tar.gz`, `.7z` | Software releases |
| Images | `.png`, `.jpg`, `.gif` | Media content |
| Data | `.json`, `.csv`, `.xml` | Data files |
| Code | `.py`, `.sh`, `.js` | Scripts and source |

### Binary Files

Binary files are served without modification:

```micron
`[Download Binary`:/file/software/program.bin]
```

### Text Files

Text files can be viewed in-browser or downloaded:

```micron
`[View README`:/file/readme.txt]
```

## Organization Best Practices

### Recommended Structure

```
files/
├── docs/               # Documentation
│   ├── guides/
│   └── references/
├── software/           # Software releases
│   ├── releases/
│   └── source/
├── media/              # Images and media
│   ├── logos/
│   └── screenshots/
└── data/               # Data files
    └── samples/
```

### Naming Conventions

- Use lowercase with hyphens: `user-guide.pdf`
- Include version numbers: `release-v1.2.3.zip`
- Be descriptive: `api-reference-2024.pdf`

## File Index Page

Create a browsable file index:

```micron
#!c=300
>File Repository

`cBrowse and download available files
`a

-

>>Documentation

`F0af`_`[User Guide (2.1 MB)`:/file/docs/user-guide.pdf]`_`f
Getting started with the system.

`F0af`_`[API Reference (1.5 MB)`:/file/docs/api-reference.pdf]`_`f
Complete API documentation.

`F0af`_`[FAQ (45 KB)`:/file/docs/faq.txt]`_`f
Frequently asked questions.

>>Software

`F0af`_`[Release v1.0.0 (5.2 MB)`:/file/software/release-v1.0.0.zip]`_`f
Latest stable release.

`F0af`_`[Source Code (1.8 MB)`:/file/software/source.tar.gz]`_`f
Source code archive.

-

`c`F888Last updated: 2024-01-15`f
```

## Dynamic File Listings

Generate file listings dynamically:

```python
#!/usr/bin/env python3
import os

files_path = os.path.expanduser("~/.nomadnetwork/storage/files")

print("#!c=60")
print(">Available Files")
print("")

for root, dirs, files in os.walk(files_path):
    rel_path = os.path.relpath(root, files_path)
    if rel_path != ".":
        print(f">>{rel_path}")

    for filename in sorted(files):
        full_path = os.path.join(root, filename)
        size = os.path.getsize(full_path)
        size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / (1024*1024):.1f} MB"

        if rel_path == ".":
            url = f":/file/{filename}"
        else:
            url = f":/file/{rel_path}/{filename}"

        print(f"`F0af`_`[{filename} ({size_str})`{url}]`_`f")
    print("")
```

## Configuration

### Node Config Options

```ini
[node]
# File storage path
files_path = ~/.nomadnetwork/storage/files

# Interval in minutes to rescan files (0 = startup only)
file_refresh_interval = 0
```

### Refresh Interval

Set `file_refresh_interval` to automatically detect new files:

- `0` - Only scan at startup
- `5` - Rescan every 5 minutes
- `60` - Rescan every hour

## Security Considerations

### File Permissions

Files inherit the permissions of the node. Use `.allowed` files (in pages) to restrict access if needed by requiring authentication before showing file links.

### Sensitive Files

- Don't store sensitive data in the files directory
- Consider authentication for private files
- Use `.allowed` on index pages that list sensitive files

### Path Traversal

NomadNetwork prevents path traversal attacks. Requests for `:/file/../config` are blocked.

## Bandwidth Optimization

### Compression

Large files are automatically compressed during transfer. For pre-compressed formats (`.zip`, `.gz`, `.jpg`), this is detected and skipped.

### Caching Recommendations

| Content Type | Cache Duration |
|--------------|----------------|
| Static releases | Long (86400s) |
| Frequently updated | Short (300s) |
| Dynamic listings | Very short (60s) |

### File Size Considerations

- Small files (<1MB): Quick transfer
- Medium files (1-10MB): Reasonable transfer times
- Large files (>10MB): May take significant time on slow links
- Very large files: Consider splitting or providing mirrors
