# Import & Cases

## Import Command

```bash
./thorlens import --log <path> --case <name> [--workers N]
```

| Option | Description |
|--------|-------------|
| `--log, -l` | Path to JSONL file (required) |
| `--case, -c` | Case name (required) |
| `--workers, -w` | Parallel workers (default: 4) |

## Supported Input Formats

- `.jsonl` - JSON Lines (one JSON object per line)
- `.jsonl.gz` - Gzip-compressed JSONL

The input must be a THOR v11 audit trail file, not a regular THOR log.

## Import Examples

### Basic Import

```bash
./thorlens import --log ~/Downloads/thor_audit_2024-01-15.jsonl --case investigation1
```

### Gzipped Audit Trail

```bash
./thorlens import --log /cases/host01_audit.jsonl.gz --case host01
```

### With More Workers (Faster)

```bash
./thorlens import --log audit.jsonl --case mycase --workers 8
```

## Case Folder Structure

After import, a case folder is created:

```
./cases/<name>/
├── meta.json              # Import metadata (immutable)
├── events/                # Parquet files (immutable)
│   ├── date=2024-11-14/
│   │   └── part-0000.parquet
│   └── ...
└── annotations.sqlite     # Tags, comments, bookmarks (mutable)
```

### meta.json

Contains import metadata:
- Source file path
- Import timestamp
- Event count
- Time range

### events/

Partitioned Parquet files for fast querying. Data is partitioned by date for efficient time-range queries. **These files are immutable** - never modified after import.

### annotations.sqlite

SQLite database storing user annotations:
- Tags
- Comments
- Bookmarks
- Exclusion filters
- Named selections

**This file is mutable** - updated as you annotate events in the UI.

## Multi-Timepoint Expansion

THOR Lens expands audit records into multiple timeline events. One audit record may contain multiple timestamps (created, modified, accessed, etc.), each becoming a separate timeline row.

Example: A 309 MB audit trail with 200,751 records can expand to 575,950+ timeline events.

## Verifying Import

### Check Case Exists

```bash
ls -la ./cases/mycase/
```

### Check Metadata

```bash
cat ./cases/mycase/meta.json | jq .
```

### Check Parquet Files

```bash
find ./cases/mycase/events -name "*.parquet" | head
```

### Count Events

```bash
# Via API after starting server
curl http://127.0.0.1:8080/api/meta | jq '.event_count'
```

## Import Performance

Tested on 309 MB audit trail (200,751 records):
- Import time: ~4 seconds (4 workers)
- Timeline rows: 575,950 (2.87x expansion)
- Parse errors: 0

### Improving Performance

```bash
# More workers for faster import
./thorlens import --log large_audit.jsonl --case bigcase --workers 8
```

## Re-Importing

To re-import a case, delete the existing case folder first:

```bash
rm -rf ./cases/mycase
./thorlens import --log updated_audit.jsonl --case mycase
```

**Note**: This removes all annotations. If you need to preserve annotations, back up `annotations.sqlite` first.

## Input Validation

Before importing, verify your audit trail:

```bash
# Check file exists
ls -lh /path/to/audit.jsonl

# For gzipped files, verify integrity
gzip -t /path/to/audit.jsonl.gz && echo "OK"

# Preview content (should be JSON objects)
head -3 /path/to/audit.jsonl | jq .
# or
zcat /path/to/audit.jsonl.gz | head -3 | jq .
```

## Object Types

THOR Lens handles 34+ object types from THOR v11:

| Category | Types |
|----------|-------|
| Files | file |
| Processes | process, process handle, process connection, process start |
| Registry | registry key, registry value |
| System | Windows service, scheduled task, autorun entry |
| Network | firewall rule, network share, named pipe |
| Artifacts | AmCache entry, shim cache entry, shellbag entry, jump list entry |
| Logs | eventlog entry, log line |
| Web | web page visit, web download |
| SRUM | SRUM Resource Usage Entry |
| Other | environment variable, Windows user, user profile, WMI startup command, antivirus exclusion |
