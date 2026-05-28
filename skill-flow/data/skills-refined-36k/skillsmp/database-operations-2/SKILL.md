---
name: Database Operations
description: This skill should be used when the user asks to "database migration", "create migration", "backup database", "restore database", "database replication", "database performance", "query optimization", "connection pooling", "database scaling", "sharding", or needs help with database management, migrations, and optimization.
version: 1.0.0
---

# Database Operations

Comprehensive guidance for database migrations, backups, replication, and performance optimization.

## Database Migrations

### SQL Migrations (PostgreSQL)

```sql
-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users.down.sql
DROP TABLE IF EXISTS users;
```

### Migration Tools

**golang-migrate:**
```bash
# Install
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Create migration
migrate create -ext sql -dir migrations -seq create_users

# Run migrations
migrate -database "postgres://user:pass@localhost/db?sslmode=disable" -path migrations up

# Rollback
migrate -database "..." -path migrations down 1
```

**Prisma:**
```bash
# Create migration
npx prisma migrate dev --name add_users

# Deploy migrations
npx prisma migrate deploy

# Reset database
npx prisma migrate reset
```

**Alembic (Python):**
```python
# alembic/versions/001_create_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('users')
```

```bash
alembic revision --autogenerate -m "create users"
alembic upgrade head
alembic downgrade -1
```

### Migration Best Practices

| Practice | Description |
|----------|-------------|
| Small, incremental | One logical change per migration |
| Reversible | Always include down migration |
| Idempotent | Safe to run multiple times |
| No data loss | Avoid destructive changes |
| Test first | Run on staging before production |

## Backup and Recovery

### PostgreSQL Backup

```bash
# Full backup (pg_dump)
pg_dump -h localhost -U postgres -Fc mydb > backup.dump

# Compressed backup
pg_dump -h localhost -U postgres mydb | gzip > backup.sql.gz

# Parallel backup (large databases)
pg_dump -h localhost -U postgres -j 4 -Fd -f backup_dir mydb

# Point-in-time recovery setup
# postgresql.conf
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'
```

```bash
# Restore
pg_restore -h localhost -U postgres -d mydb backup.dump

# Restore with options
pg_restore --clean --if-exists -d mydb backup.dump
```

### MySQL Backup

```bash
# mysqldump
mysqldump -h localhost -u root -p mydb > backup.sql

# With compression
mysqldump -h localhost -u root -p mydb | gzip > backup.sql.gz

# All databases
mysqldump --all-databases > all_databases.sql

# Binary log backup (PITR)
mysqlbinlog mysql-bin.000001 > binlog.sql
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh
set -e

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="mydb"
S3_BUCKET="s3://my-backups"

# Create backup
pg_dump -Fc $DB_NAME > "$BACKUP_DIR/$DB_NAME-$DATE.dump"

# Upload to S3
aws s3 cp "$BACKUP_DIR/$DB_NAME-$DATE.dump" "$S3_BUCKET/$DB_NAME-$DATE.dump"

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete

echo "Backup completed: $DB_NAME-$DATE.dump"
```

## Database Replication

### PostgreSQL Streaming Replication

**Primary Configuration:**
```conf
# postgresql.conf
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1GB

# pg_hba.conf
host replication replicator 10.0.0.0/8 md5
```

**Replica Setup:**
```bash
# Create base backup
pg_basebackup -h primary -U replicator -D /var/lib/postgresql/data -P -R

# standby.signal file created automatically with -R flag
```

### MySQL Replication

```sql
-- Primary
CHANGE MASTER TO
  MASTER_HOST='primary.example.com',
  MASTER_USER='replicator',
  MASTER_PASSWORD='password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=0;

START SLAVE;
SHOW SLAVE STATUS\G
```

### Read Replica Patterns

```python
# Application-level routing
def get_connection(read_only=False):
    if read_only:
        return read_replica_pool.getconn()
    return primary_pool.getconn()

# Usage
with get_connection(read_only=True) as conn:
    # Read queries go to replica
    users = query_users(conn)

with get_connection(read_only=False) as conn:
    # Write queries go to primary
    create_user(conn, user_data)
```

## Performance Optimization

### Query Optimization

```sql
-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Check for sequential scans
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- Create appropriate indexes
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial indexes
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Expression indexes
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

### Index Guidelines

| Index Type | Use Case |
|------------|----------|
| B-tree | Most queries (default) |
| Hash | Equality comparisons only |
| GiST | Geometric data, full-text search |
| GIN | Arrays, JSONB, full-text |
| BRIN | Large sequential data |

### Connection Pooling

**PgBouncer Configuration:**
```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
```

**Application-level pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

### Query Performance Monitoring

```sql
-- PostgreSQL: Enable pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Find missing indexes
SELECT schemaname, tablename, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_scan DESC;
```

## Database Scaling

### Vertical Scaling

- Increase CPU, RAM, storage
- Use faster storage (NVMe SSD)
- Optimize configuration for resources

### Horizontal Scaling (Sharding)

```python
# Application-level sharding
def get_shard(user_id):
    shard_count = 4
    shard_id = user_id % shard_count
    return shard_connections[shard_id]

# Query routing
def get_user(user_id):
    shard = get_shard(user_id)
    return shard.execute("SELECT * FROM users WHERE id = ?", user_id)
```

### Partitioning

```sql
-- PostgreSQL range partitioning
CREATE TABLE orders (
    id SERIAL,
    user_id INTEGER,
    created_at TIMESTAMP,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

## Additional Resources

### Reference Files

- **`references/postgresql-tuning.md`** - PostgreSQL configuration tuning
- **`references/mysql-performance.md`** - MySQL optimization guide

### Example Files

- **`examples/migration-workflow.sh`** - Safe migration deployment
- **`examples/backup-rotation.sh`** - Automated backup with rotation
