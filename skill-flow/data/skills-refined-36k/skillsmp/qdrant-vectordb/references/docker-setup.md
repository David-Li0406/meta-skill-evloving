# Qdrant Docker Setup

## Local Development with Docker

### Quick Start
```bash
# Pull Qdrant image
docker pull qdrant/qdrant

# Run with persistent storage
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### With Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"  # HTTP API & Web UI
      - "6334:6334"  # gRPC API
    volumes:
      - ./qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### With API Key Authentication

Create `.env`:
```env
QDRANT_API_KEY=your-secret-key-here
```

Update `docker-compose.yml`:
```yaml
services:
  qdrant:
    environment:
      - QDRANT__SERVICE__API__KEY=${QDRANT_API_KEY}
```

## Qdrant Cloud Setup

### 1. Sign Up & Create Cluster
1. Go to https://cloud.qdrant.io
2. Create account (free tier available)
3. Create new cluster
4. Choose region (same as your app for low latency)

### 2. Get Credentials
```bash
# From Qdrant Cloud dashboard:
QDRANT_URL="https://xxx-xxx.qdrant.io"
QDRANT_API_KEY="your-api-key"
```

### 3. Test Connection
```typescript
import { QdrantClient } from '@qdrant/js-client';

const client = new QdrantClient({
  url: process.env.QDRANT_URL,
  apiKey: process.env.QDRANT_API_KEY,
});

// Test connection
const collections = await client.getCollections();
console.log('Connected! Collections:', collections);
```

## Ports

- **6333**: HTTP API + Web UI (dashboard)
- **6334**: gRPC API (faster but requires gRPC client)

## Web UI

Access at: `http://localhost:6333/dashboard`

Features:
- Browse collections
- View vectors and payloads
- Test search queries
- Monitor performance

## Storage

Qdrant stores data in:
- **Local**: `./qdrant_storage/` directory
- **Docker**: `/qdrant/storage` (mount to host)
- **Cloud**: Managed by Qdrant

## System Requirements

- **CPU**: 64-bit (x86_64 or ARM64)
- **RAM**: Min 4GB (8GB+ recommended)
- **Storage**: SSD or NVMe (no NFS or S3)
- **OS**: Linux, macOS, Windows

## Backup & Restore

### Backup
```bash
# Snapshot a collection
curl -X POST 'http://localhost:6333/collections/textbook_chunks/snapshots'

# Download snapshot
curl 'http://localhost:6333/collections/textbook_chunks/snapshots/snapshot-2024.snapshot' \
  --output snapshot.snapshot
```

### Restore
```bash
# Upload snapshot
curl -X PUT 'http://localhost:6333/collections/textbook_chunks/snapshots/upload' \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @snapshot.snapshot
```

## Production Considerations

1. **Enable authentication** (API key required)
2. **Use reverse proxy** (Nginx/Caddy) for HTTPS
3. **Monitor disk usage** (vectors take significant space)
4. **Regular backups** (snapshots before major changes)
5. **Resource limits** (set Docker memory/CPU limits)
