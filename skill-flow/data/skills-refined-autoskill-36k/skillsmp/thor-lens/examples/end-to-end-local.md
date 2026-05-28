# End-to-End Local Workflow

Complete workflow for THOR Lens on a local machine.

## Overview

1. Build THOR Lens
2. Run THOR v11 scan with audit trail
3. Import audit trail into THOR Lens
4. Explore timeline in web UI
5. (Optional) Connect Claude Code via MCP

## Step 1: Build THOR Lens

```bash
# Clone repository
git clone https://github.com/NextronSystems/thor-lens.git
cd thor-lens

# Build (requires Go 1.21+, Node 18+, npm, make)
make build

# Verify build
ls -la ./thorlens
```

## Step 2: Run THOR v11 Scan

Scan the target system with audit trail enabled.

### Live System (Current Host)

```bash
# Linux
sudo ./thor-linux-64 --lab \
  -p / \
  --audit-trail /cases/$(hostname)_audit.jsonl \
  -e /cases/reports

# Windows
thor64.exe --lab ^
  -p C:\ ^
  --audit-trail C:\cases\%COMPUTERNAME%_audit.jsonl ^
  -e C:\cases\reports
```

### Specific Directory

```bash
./thor-linux-64 --lab \
  -p /home/user \
  --audit-trail /cases/user_home_audit.jsonl \
  -e /cases/reports
```

## Step 3: Verify Audit Trail

```bash
# Check file exists
ls -lh /cases/*_audit.jsonl

# Verify content (should be JSON)
head -3 /cases/*_audit.jsonl | jq .

# Count records
wc -l /cases/*_audit.jsonl
```

## Step 4: Import into THOR Lens

```bash
cd /path/to/thor-lens

./thorlens import \
  --log /cases/hostname_audit.jsonl \
  --case hostname

# Verify import
ls -la ./cases/hostname/
cat ./cases/hostname/meta.json | jq '.event_count'
```

## Step 5: Start Web Server

```bash
./thorlens serve --case ./cases/hostname --port 8080
```

## Step 6: Open Web UI

Open browser to **http://127.0.0.1:8080**

### Initial Exploration

1. Review the histogram - see activity distribution over time
2. Check summary stats in header
3. Look for high-score events (bright colors in score mode)
4. Browse event table for suspicious entries

### Key Actions

| Action | How |
|--------|-----|
| Filter by time | Drag on histogram |
| Filter by type | Click type in sidebar |
| Search | Press `/` and type |
| View details | Click event row |
| Bookmark | Press `b` on selected event |
| Tag | Press `t` and enter tag |

## Step 7: Connect Claude Code (Optional)

### Option A: Stdio Mode

Create `.mcp.json` in your project:

```json
{
  "mcpServers": {
    "thor-lens": {
      "command": "/path/to/thor-lens/thorlens",
      "args": ["serve", "--case", "/path/to/thor-lens/cases/hostname", "--mcp-stdio"]
    }
  }
}
```

Restart Claude Code.

### Option B: HTTP Mode

Keep the server running from Step 5.

Create `.mcp.json`:

```json
{
  "mcpServers": {
    "thor-lens": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

Restart Claude Code.

### Example Claude Queries

```
"Show me the highest scoring events"
"Find events related to PowerShell activity"
"What happened around 2024-01-15 03:00 UTC?"
"Tag all suspicious events as 'needs-review'"
```

## Quick Reference

| Step | Command |
|------|---------|
| Build | `make build` |
| Scan | `./thor-linux-64 --lab -p / --audit-trail audit.jsonl` |
| Import | `./thorlens import --log audit.jsonl --case mycase` |
| Serve | `./thorlens serve --case ./cases/mycase --port 8080` |
| Browse | http://127.0.0.1:8080 |

## Cleanup

When done with a case:

```bash
# Remove case (loses all annotations!)
rm -rf ./cases/hostname
```
