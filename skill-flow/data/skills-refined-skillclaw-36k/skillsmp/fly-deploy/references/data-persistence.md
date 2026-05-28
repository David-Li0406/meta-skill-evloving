# Data Persistence on fly.io

## Managed Postgres (Recommended for Production)

Fly.io now offers **Managed Postgres** which handles production database operations with automated backups, monitoring, and support.

**Important:** Fly.io explicitly states they cannot provide support for unmanaged Postgres clusters. For production workloads, use Managed Postgres.

### Creating a Managed Postgres Database

```bash
# Create managed Postgres cluster
fly postgres create
```

Interactive prompts:
- Choose a name for your database
- Select region (choose same as your app)
- Select configuration (Development or Production)

### Attaching Database to App

```bash
# Attach to your app
fly postgres attach <postgres-app-name>
```

This automatically:
1. Creates a new database in the cluster named after your app
2. Sets `DATABASE_URL` secret on your app
3. Connects your app to the database over private network

### Connecting from Your App

The `DATABASE_URL` is automatically available:

**Node.js:**
```js
const DATABASE_URL = process.env.DATABASE_URL
```

**Python:**
```python
import os
DATABASE_URL = os.getenv("DATABASE_URL")
```

**Rust:**
```rust
let database_url = std::env::var("DATABASE_URL")
    .expect("DATABASE_URL must be set");
```

### Connection String Format

```
postgres://postgres:password@appname.internal:5432/dbname?sslmode=disable
```

**Note for SQLAlchemy (Python):**
SQLAlchemy requires `postgresql://` prefix:

```python
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

### Managing Databases

```bash
# List all databases in cluster
fly postgres db list -a <postgres-app-name>

# Create additional database
fly postgres db create -a <postgres-app-name> <db-name>

# Connect to postgres console
fly postgres connect -a <postgres-app-name>
```

### Running Migrations

**Option 1: Release command in fly.toml**

```toml
[deploy]
  release_command = "npm run migrate"
  # or: "python manage.py migrate"
  # or: "alembic upgrade head"
  # or: "./target/release/migrate"
```

**Option 2: Manual migration**

```bash
# Deploy without running release command
fly deploy --no-release-command

# Run migration manually
fly ssh console -C "npm run migrate"

# Then resume normal deployments
fly deploy
```

### Backups and Snapshots

Managed Postgres includes daily snapshots by default.

**List snapshots:**
```bash
fly volumes snapshots list -a <postgres-app-name>
```

**Restore from snapshot:**
```bash
fly volumes restore <snapshot-id> -a <postgres-app-name>
```

### High Availability

**For production, use multi-node cluster:**

```bash
# During creation, choose "Production" configuration
fly postgres create

# Or scale existing single-node to HA
fly machine clone <machine-id> --region ord -a <postgres-app-name>
```

High Availability provides:
- Automatic failover
- Read replicas
- Better uptime guarantees

### Monitoring

```bash
# Check database status
fly status -a <postgres-app-name>

# View logs
fly logs -a <postgres-app-name>

# Check health
fly checks list -a <postgres-app-name>
```

---

## Fly Volumes

Volumes provide persistent local storage for SQLite databases, uploaded files, or any data that needs to persist across deployments.

**Key characteristics:**
- Tied to a single machine and region
- NVMe-backed local storage
- Faster than networked storage
- Survives deployments and restarts

### Creating Volumes

```bash
# Create a volume
fly volumes create <volume-name> --size 1 --region ord

# Create in same region as app
fly volumes create data --size 1 --region ord -a my-app
```

**Size options:**
- Minimum: 1GB
- Maximum: 500GB
- Can be extended later

### Configuring Volume in fly.toml

```toml
[[mounts]]
  source = "data"
  destination = "/data"
```

This mounts the volume named "data" to `/data` in your container.

### Using Volumes for SQLite

**fly.toml:**
```toml
[[mounts]]
  source = "sqlite_db"
  destination = "/app/data"

[env]
  DATABASE_PATH = "/app/data/db.sqlite3"
```

**In your app:**

```js
// Node.js with better-sqlite3
const Database = require('better-sqlite3');
const db = new Database(process.env.DATABASE_PATH || '/app/data/db.sqlite3');
```

```python
# Python with sqlite3
import sqlite3
import os

db_path = os.getenv('DATABASE_PATH', '/app/data/db.sqlite3')
conn = sqlite3.connect(db_path)
```

### Volume Best Practices

1. **One volume per machine** - Each machine needs its own volume
2. **Same region** - Volume must be in same region as machine
3. **Backups** - Use volume snapshots for backups
4. **Size planning** - Start small, extend as needed

### Managing Volumes

```bash
# List volumes
fly volumes list

# Extend volume size
fly volumes extend <volume-id> --size 10

# Create snapshot
fly volumes snapshots create <volume-id>

# Delete volume
fly volumes delete <volume-id>
```

### Multi-Region with Volumes

For multi-region deployments with volumes, you need a volume in each region:

```bash
# Create volume in each region
fly volumes create data --size 1 --region ord
fly volumes create data --size 1 --region iad

# Scale to 2 machines across regions
fly scale count 2 --region ord,iad
```

**Important:** Volumes are not automatically synced. For shared data across regions, use:
- Managed Postgres (automatically replicated)
- Tigris object storage (globally cached)
- LiteFS (SQLite replication - advanced)

---

## Tigris Object Storage

Tigris is S3-compatible object storage with global caching, built on fly.io infrastructure.

**Use cases:**
- User uploads (images, videos, documents)
- Static assets (media files, PDFs)
- Backups and archives
- Large file storage

### Setting Up Tigris

```bash
# Create a bucket (from within your app directory)
fly storage create

# Create with custom name
fly storage create --name my-bucket

# Create public bucket
fly storage create --public
```

This automatically sets these secrets on your app:
- `BUCKET_NAME`
- `AWS_ENDPOINT_URL_S3`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Using Tigris (S3-Compatible)

**Node.js with AWS SDK v3:**

```js
const { S3Client, PutObjectCommand, GetObjectCommand } = require('@aws-sdk/client-s3');

const s3Client = new S3Client({
  region: 'auto',
  endpoint: process.env.AWS_ENDPOINT_URL_S3,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

// Upload file
async function uploadFile(key, body) {
  await s3Client.send(new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: key,
    Body: body,
  }));
}

// Download file
async function downloadFile(key) {
  const response = await s3Client.send(new GetObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: key,
  }));
  return response.Body;
}
```

**Python with boto3:**

```python
import boto3
import os

s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('AWS_ENDPOINT_URL_S3'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='auto'
)

# Upload file
def upload_file(key, body):
    s3_client.put_object(
        Bucket=os.getenv('BUCKET_NAME'),
        Key=key,
        Body=body
    )

# Download file
def download_file(key):
    response = s3_client.get_object(
        Bucket=os.getenv('BUCKET_NAME'),
        Key=key
    )
    return response['Body'].read()
```

**Rust with aws-sdk-s3:**

```rust
use aws_sdk_s3::{Client, Config, Credentials, Region};

#[tokio::main]
async fn main() {
    let creds = Credentials::new(
        std::env::var("AWS_ACCESS_KEY_ID").unwrap(),
        std::env::var("AWS_SECRET_ACCESS_KEY").unwrap(),
        None, None, "tigris"
    );

    let config = Config::builder()
        .credentials_provider(creds)
        .region(Region::new("auto"))
        .endpoint_url(std::env::var("AWS_ENDPOINT_URL_S3").unwrap())
        .build();

    let client = Client::from_conf(config);

    // Upload
    client.put_object()
        .bucket(std::env::var("BUCKET_NAME").unwrap())
        .key("test.txt")
        .body("Hello World".into())
        .send()
        .await
        .unwrap();
}
```

### Public vs Private Buckets

**Private (default):**
- Files require signed URLs or credentials
- Best for user data, private files

**Public:**
- Files accessible via direct URL
- Best for public assets, images, CSS, JS

```bash
# Create public bucket
fly storage create --public
```

Public file URL format:
```
https://<bucket-name>.fly.storage.tigris.dev/<key>
```

### Signed URLs for Private Buckets

**Node.js:**
```js
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const { GetObjectCommand } = require('@aws-sdk/client-s3');

async function getPresignedUrl(key, expiresIn = 3600) {
  const command = new GetObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: key,
  });
  return await getSignedUrl(s3Client, command, { expiresIn });
}
```

**Python:**
```python
def generate_presigned_url(key, expiration=3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': os.getenv('BUCKET_NAME'), 'Key': key},
        ExpiresIn=expiration
    )
```

### Shadow Buckets (Migration)

Migrate from existing S3-compatible storage without downtime:

```bash
fly storage create --shadow-bucket s3://existing-bucket
```

Tigris will:
- Read from shadow bucket if object not in Tigris
- Copy objects to Tigris on first access
- Gradually migrate data

---

## External Databases

Connect to databases hosted outside fly.io (Supabase, PlanetScale, Neon, etc.).

### Connection Setup

```bash
# Set database URL as secret
fly secrets set DATABASE_URL=postgresql://user:pass@external-host.com:5432/dbname
```

### Security Considerations

**Connection over public internet:**
- Always use SSL/TLS
- Use connection pooling
- Consider VPN for sensitive data

**Connection string with SSL:**
```
postgresql://user:pass@host:5432/db?sslmode=require
```

### Common External Providers

**Supabase:**
```bash
fly secrets set DATABASE_URL="postgresql://postgres:password@db.project.supabase.co:5432/postgres"
```

**PlanetScale:**
```bash
fly secrets set DATABASE_URL="mysql://user:pass@host.planetscale.com/dbname?sslmode=require"
```

**Neon:**
```bash
fly secrets set DATABASE_URL="postgres://user:pass@ep-cool-meadow-123456.us-east-2.aws.neon.tech/neondb"
```

**MongoDB Atlas:**
```bash
fly secrets set MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/dbname"
```

### Connection Pooling

For better performance with external databases:

**Node.js (pg-pool):**
```js
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

**Python (SQLAlchemy):**
```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

---

## Choosing the Right Storage

| Use Case | Solution | Why |
|----------|----------|-----|
| Structured data, SQL | Managed Postgres | Reliable, managed, replicated |
| Simple app, low traffic | SQLite + Volume | Simple, no network overhead |
| User uploads, media | Tigris | Globally cached, S3-compatible |
| Cache, sessions | Upstash Redis | Fast, managed, serverless |
| Large files, backups | Tigris | Cost-effective, global |
| External team DB | External DB | Use existing infrastructure |

## Best Practices

1. **Use Managed Postgres for production** - Don't run unmanaged databases
2. **Backups** - Always configure automated backups
3. **Secrets** - Never commit connection strings to git
4. **SSL** - Always use encrypted connections
5. **Connection pooling** - Reduce connection overhead
6. **Monitoring** - Watch for slow queries and errors
7. **Regional data** - Keep data close to compute for latency
