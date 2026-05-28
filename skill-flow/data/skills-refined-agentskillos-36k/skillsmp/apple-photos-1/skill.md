---
name: apple-photos
description: Query Apple Photos library for recent photos, search by text/OCR, get metadata and file paths. Use when user asks about photos, wants to find specific images, or needs photo file access.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Apple Photos

Access Photos library via direct SQLite queries (no Photos.app needed).

## Quick Start

| You want to... | Run... |
|----------------|--------|
| Most recent photo | `photos-query --last` |
| Last N photos | `photos-query -l 10` |
| Photos from last week | `photos-query -d 7` |
| Search text in photos | `photos-search "receipt"` |

All commands support `-j` for JSON output.

## Commands

### photos-query
Query recent photos by count or date range.
```bash
photos-query                    # Last 10 (default)
photos-query --last             # Most recent only
photos-query -l 20              # Last 20 photos
photos-query -d 7               # Last 7 days
```

### photos-search
Search photos by visible text (Live Text/OCR).
```bash
photos-search "VIN 1G6DD"       # Search for text
photos-search "receipt" -l 5    # With limit
photos-search --status          # Index status
photos-search --update          # Update index
```

First run builds index (~2-3 min for ~20k photos). Subsequent runs are fast.

## Working with Photos

Get file path for reading:
```bash
photos-query --last -j | jq -r '.photos[0].filePath'
```

Convert HEIC to JPEG if needed:
```bash
sips -s format jpeg input.heic --out /tmp/photo.jpg
```

## Security & Privacy

- **Read-only** - Cannot modify Photos library
- Photos may contain **sensitive content** and **GPS coordinates**
- **NEVER** upload or share photos without explicit permission

## Technical Details

See [reference/technical.md](reference/technical.md) for database paths, file locations, and limitations.

## Related Skills

- `apple-productivity` - Calendar, Contacts, Mail, Messages
- `apple-shortcuts` - Run macOS Shortcuts
