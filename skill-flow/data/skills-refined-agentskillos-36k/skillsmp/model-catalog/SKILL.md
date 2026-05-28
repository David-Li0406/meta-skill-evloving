---
name: model-catalog
description: Use when working with 3D model files (STL), print tracking, slicer profiles, or managing the model-catalog homelab service at model-catalog.internal.lakehouse.wtf
---

# Model Catalog

## Overview

A homelab FastAPI service for cataloging 3D models, tracking print history, managing slicer profiles, and storing print photos. Deployed as LXC 210 with Vue.js frontend and REST API.

## When to Use

Use this skill when:
- Uploading or searching for 3D model files (.stl)
- Tracking print jobs, success rates, or failures
- Managing PrusaSlicer profiles
- Querying print statistics
- Working with the model-catalog service deployment
- Integrating with PrusaLink/Prusa Connect

## Quick Reference

### Service Information

| Component | Details |
|-----------|---------|
| **URL** | https://model-catalog.internal.lakehouse.wtf |
| **Container** | LXC 210 on proxmox3 (192.168.1.211:8000) |
| **Frontend** | Vue 3 + TypeScript (served at `/`) |
| **API Docs** | `/docs` (Swagger UI) |
| **Database** | SQLite at `/var/lib/model-catalog/catalog.db` |
| **Storage** | NFS `/mnt/models` from TrueNAS |

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/models` | GET, POST | List/upload models |
| `/api/models/{id}` | GET, DELETE | Get/delete model |
| `/api/models/{id}/file` | GET | Download STL file |
| `/api/prints` | GET, POST | List/create print jobs |
| `/api/prints/{id}` | GET, PATCH | Get/update print |
| `/api/prints/{id}/complete` | POST | Mark print successful |
| `/api/prints/{id}/cancel` | POST | Cancel print |
| `/api/profiles` | GET, POST | List/create slicer profiles |
| `/api/profiles/{id}/ini` | GET | Download profile INI |
| `/api/tags` | GET, POST | List/create tags |
| `/api/stats` | GET | Overall statistics |
| `/api/printer/status` | GET | Printer status (via PrusaLink) |

### CLI Commands

The `mc` CLI is available in the container:

```bash
# List models
mc list
mc list --tag "functional-prints"

# Search models
mc search "benchy"

# Add model
mc add /path/to/model.stl --name "Test Print" --tags "test,calibration"

# Show details
mc show <model-id>

# Export model
mc export <model-id> /path/to/output.stl

# Delete model
mc delete <model-id>

# Tag operations
mc tag add <model-id> "new-tag"
mc tag remove <model-id> "old-tag"
```

## Common Workflows

### Uploading a Model

**Via API:**
```bash
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/models \
  -F "file=@model.stl" \
  -F "name=My Model" \
  -F "description=Test print" \
  -F "tags=functional,test"
```

**Via CLI (on container):**
```bash
ssh root@192.168.1.211
mc add /mnt/models/myfile.stl --name "My Model" --tags "functional,test"
```

### Tracking a Print Job

```bash
# Start print
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/prints \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "uuid-here",
    "profile_id": "profile-uuid",
    "notes": "First test print"
  }'

# Complete print (success)
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/prints/{print-id}/complete \
  -H "Content-Type: application/json" \
  -d '{"result": "success", "notes": "Perfect print"}'

# Mark failed
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/prints/{print-id}/complete \
  -H "Content-Type: application/json" \
  -d '{"result": "failure", "notes": "Layer shifting at 50%"}'
```

### Managing Slicer Profiles

```bash
# Import PrusaSlicer profile
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/profiles/import \
  -F "file=@profile.ini" \
  -F "name=PLA Standard"

# List profiles
curl https://model-catalog.internal.lakehouse.wtf/api/profiles

# Download profile INI
curl https://model-catalog.internal.lakehouse.wtf/api/profiles/{id}/ini -o profile.ini
```

## File Locations (Production)

```
LXC 210 (192.168.1.211):
  /var/lib/model-catalog/catalog.db    # SQLite database
  /opt/model-catalog/                  # Application code
  /etc/model-catalog/env               # Configuration
  /mnt/models/                         # NFS mount (TrueNAS)
    ├── models/{id}/original.stl.zst  # Compressed STL files
    ├── gcode/{id}.gcode.zst           # Generated G-code (temp)
    ├── photos/{id}/finished.jpg       # Print photos
    └── profiles/{id}.ini              # Slicer profiles

TrueNAS:
  /mnt/truenas_nvme/active_projects/model-catalog/  # NFS backing store
```

## Service Management

**Check service status:**
```bash
ssh root@192.168.1.126 "pct exec 210 -- systemctl status model-catalog"
```

**Restart service:**
```bash
ssh root@192.168.1.126 "pct exec 210 -- systemctl restart model-catalog"
```

**View logs:**
```bash
ssh root@192.168.1.126 "pct exec 210 -- journalctl -u model-catalog -f"
```

**Update deployment:**
```bash
# Package updated code
cd /home/dev/workspace/model-catalog
tar czf /tmp/update.tar.gz --exclude='.git' app/ frontend/dist/

# Deploy to container
scp /tmp/update.tar.gz root@192.168.1.126:/tmp/
ssh root@192.168.1.126 "
  pct push 210 /tmp/update.tar.gz /tmp/update.tar.gz
  pct exec 210 -- bash -c 'cd /opt/model-catalog && tar xzf /tmp/update.tar.gz'
  pct exec 210 -- chown -R model-catalog:model-catalog /opt/model-catalog
  pct exec 210 -- systemctl restart model-catalog
"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  https://model-catalog.internal.lakehouse.wtf               │
└──────────────────┬──────────────────────────────────────────┘
                   │ DNS → 192.168.1.101 (Traefik VIP)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    Traefik HA (VIP)                          │
│  Primary: 192.168.1.110 | Secondary: 192.168.1.103          │
└──────────────────┬──────────────────────────────────────────┘
                   │ Proxy → 192.168.1.211:8000
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            LXC 210 (model-catalog) - 192.168.1.211          │
│                                                              │
│  ┌────────────────┐  ┌──────────────────┐                  │
│  │ FastAPI (8000) │  │ Vue.js Frontend  │                  │
│  │   - API        │  │   - /            │                  │
│  │   - /api/*     │  │   - /assets/*    │                  │
│  └────────┬───────┘  └──────────────────┘                  │
│           │                                                  │
│           ▼                                                  │
│  ┌────────────────────────────────────┐                    │
│  │ SQLite (/var/lib/model-catalog/)  │                    │
│  └────────────────────────────────────┘                    │
└─────────────────┬───────────────────────────────────────────┘
                  │ NFS mount → /mnt/models
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                         TrueNAS                              │
│  /mnt/truenas_nvme/active_projects/model-catalog/           │
│    - STL files (zstd compressed)                            │
│    - G-code (temporary, deleted after success)              │
│    - Print photos (JPG from PrusaConnect)                   │
│    - Slicer profiles (INI)                                  │
└─────────────────────────────────────────────────────────────┘
```

## Environment Variables

Set in `/etc/model-catalog/env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MC_DATABASE_PATH` | `/var/lib/model-catalog/catalog.db` | SQLite database path |
| `MC_STORAGE_PATH` | `/mnt/models` | NFS mount point for files |
| `MC_COMPRESSION_LEVEL` | `3` | Zstd compression (1-22) |
| `MC_DEBUG` | `false` | Enable debug logging |
| `MC_PRUSASLICER_PATH` | `/usr/bin/prusa-slicer` | PrusaSlicer CLI path |

## Integration Examples

### From Claude Code

**Check if model exists:**
```bash
curl -s https://model-catalog.internal.lakehouse.wtf/api/models?search=benchy | jq '.items[0]'
```

**Upload from local file:**
```bash
curl -X POST https://model-catalog.internal.lakehouse.wtf/api/models \
  -F "file=@/path/to/model.stl" \
  -F "name=$(basename model.stl .stl)" \
  -F "tags=claude-generated"
```

**Get print statistics:**
```bash
curl -s https://model-catalog.internal.lakehouse.wtf/api/stats | jq
```

### From Automation Scripts

**Track automated print:**
```python
import httpx

async with httpx.AsyncClient() as client:
    # Create print job
    response = await client.post(
        "https://model-catalog.internal.lakehouse.wtf/api/prints",
        json={
            "model_id": model_uuid,
            "profile_id": profile_uuid,
            "notes": "Automated nightly print"
        }
    )
    print_id = response.json()["id"]

    # Mark complete when done
    await client.post(
        f"https://model-catalog.internal.lakehouse.wtf/api/prints/{print_id}/complete",
        json={"result": "success"}
    )
```

## Common Issues

### Frontend Returns 404

**Problem:** Root path returns `{"detail":"Not Found"}`

**Solution:** Frontend not configured to serve from `/`. Check:
```bash
# Verify frontend files deployed
ssh root@192.168.1.126 "pct exec 210 -- ls -la /opt/model-catalog/frontend/dist/"

# Check if main.py has static file mounting
ssh root@192.168.1.126 "pct exec 210 -- grep -A 5 'StaticFiles' /opt/model-catalog/app/main.py"
```

### Service Won't Start

**Problem:** `systemctl status model-catalog` shows failed

**Solution:** Check logs:
```bash
ssh root@192.168.1.126 "pct exec 210 -- journalctl -u model-catalog -n 50"
```

Common causes:
- NFS mount not available (`/mnt/models` missing)
- Database path not writable
- Python dependencies missing

### Traefik Returns 503

**Problem:** Traefik route configured but backend unreachable

**Solution:**
```bash
# Check backend is responding
curl http://192.168.1.211:8000/api/health

# Verify Traefik route points to correct IP
ssh root@192.168.1.110 "grep -A 5 'model-catalog:' /etc/traefik/dynamic/model-catalog.yml"
```

## Development

**Local development (in workspace):**
```bash
cd /home/dev/workspace/model-catalog

# Run backend
uvicorn app.main:app --reload --port 8000

# Run frontend dev server (separate terminal)
cd frontend
npm run dev

# Run tests
pytest
pytest --cov=app
```

**Testing API locally:**
```bash
# Health check
curl http://localhost:8000/api/health

# Interactive docs
open http://localhost:8000/docs
```

## Related Documentation

- Project: `/home/dev/workspace/model-catalog/`
- Design Doc: `/home/dev/workspace/model-catalog/docs/DESIGN.md`
- Deployment: `/home/dev/workspace/model-catalog/docs/DEPLOYMENT.md`
- Acceptance Criteria: `/home/dev/workspace/model-catalog/docs/ACCEPTANCE.md`
- Issue Tracking: `bd list` (beads in `/home/dev/workspace/model-catalog/.beads/`)
