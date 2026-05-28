# Apple Photos Technical Reference

## Database Access

- **Database**: `~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite`
- **Main table**: `ZASSET`
- **Access**: Read-only via SQLite
- **Timestamps**: Apple Core Data format (seconds since 2001-01-01)

## File Locations

Photos stored in:
- Modern: `~/Pictures/Photos Library.photoslibrary/originals/{directory}/{filename}`
- Legacy: `~/Pictures/Photos Library.photoslibrary/Masters/{directory}/{filename}`

## photos-search Index

- Index location: `~/.cache/photos-ocr-index/`
- Uses Apple's Live Text (OCR) data from Photos.sqlite
- Auto-updates when Photos library changes
- Tracks last indexed photo for incremental updates

## Limitations

- **Read-only**: Cannot modify Photos library
- **Local only**: Cloud-only photos not accessible
- **No deleted**: Trashed photos excluded
- **HEIC format**: May need conversion for processing

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 2 | Library not found or database error |

### Common Errors

**Photos library not found**:
Library in non-standard location or not set up.

**Database access error**:
Database locked or corrupted. Try closing Photos.app.

**No photos found**:
No photos match query criteria. Handle gracefully.
