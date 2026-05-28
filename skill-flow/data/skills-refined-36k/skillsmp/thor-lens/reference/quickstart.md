# Quickstart

Get THOR Lens running in 5 minutes.

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Go | 1.21+ | `go version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Make | any | `make --version` |

## Step 1: Clone and Build

```bash
git clone https://github.com/NextronSystems/thor-lens.git
cd thor-lens
make build
```

This builds both the React frontend and Go backend, producing `./thorlens`.

## Step 2: Import an Audit Trail

```bash
./thorlens import --log /path/to/audit.jsonl --case mycase
```

This creates `./cases/mycase/` with:
- Partitioned Parquet files for fast querying
- Metadata about the import

## Step 3: Start the Server

```bash
./thorlens serve --case ./cases/mycase --port 8080
```

## Step 4: Open Browser

Navigate to **http://127.0.0.1:8080**

You should see the THOR Lens interface with your timeline data.

## Sanity Checks

### Before Import

```bash
# Verify audit trail file exists and is valid
ls -lh /path/to/audit.jsonl
file /path/to/audit.jsonl

# If gzipped
gzip -t /path/to/audit.jsonl.gz && echo "OK"

# Preview first few records
head -3 /path/to/audit.jsonl | jq .
# or for gzipped
zcat /path/to/audit.jsonl.gz | head -3 | jq .
```

### After Import

```bash
# Verify case was created
ls -la ./cases/mycase/

# Expected structure:
# ./cases/mycase/
# ├── meta.json
# ├── events/
# │   └── date=YYYY-MM-DD/
# │       └── part-0000.parquet
# └── annotations.sqlite
```

### After Serve

```bash
# Test API endpoint
curl http://127.0.0.1:8080/api/meta | jq .
```

## Common First-Run Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `make: command not found` | Build tools missing | Install: `xcode-select --install` (macOS), `apt install build-essential` (Ubuntu) |
| `go: command not found` | Go not in PATH | Add to PATH: `export PATH=$PATH:/usr/local/go/bin` |
| `npm: command not found` | Node.js not installed | Install via package manager |
| Port 8080 in use | Another service | Use `--port 9000` |
| Empty UI | Wrong input file | Verify it's THOR v11 audit trail JSONL, not text log |

## Next Steps

- [Build & Prerequisites](build-and-prereqs.md) - Detailed setup instructions
- [Import & Cases](import-and-cases.md) - Import options and case management
- [MCP Integration](mcp-integration.md) - Connect Claude Code to THOR Lens
