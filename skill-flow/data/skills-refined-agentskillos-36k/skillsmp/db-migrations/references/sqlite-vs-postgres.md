# SQLite vs PostgreSQL Gotchas

## SQLite Limitations

SQLite has limited support for `ALTER TABLE`, especially around constraints and foreign keys. In Alembic this often shows up as:

```
NotImplementedError: No support for ALTER of constraints in SQLite dialect...
```

### Common Issues

- Cannot drop columns directly
- Cannot modify column types easily
- Cannot add/drop foreign key constraints
- Cannot rename columns in all cases

### How to Handle

**Option 1: Use PostgreSQL for development (Recommended)**

```bash
# Set PostgreSQL URL
export DATABASE_URL="postgresql://user:pass@localhost:5432/vibe4vets"

# Run migrations
alembic upgrade head
```

**Option 2: Use Alembic batch mode for SQLite**

```python
def upgrade() -> None:
    with op.batch_alter_table('resource') as batch_op:
        batch_op.add_column(sa.Column('new_field', sa.String()))
        batch_op.drop_column('old_field')

def downgrade() -> None:
    with op.batch_alter_table('resource') as batch_op:
        batch_op.add_column(sa.Column('old_field', sa.String()))
        batch_op.drop_column('new_field')
```

## Autogenerate Differences

Running `alembic revision --autogenerate` against SQLite vs PostgreSQL can produce different diffs:

- Index names may differ
- Constraint detection varies
- Type mappings differ (e.g., `VARCHAR` vs `TEXT`)

### Recommendations

1. **Always autogenerate against PostgreSQL** for production migrations
2. **Review generated migrations** carefully
3. If you see unexpected index drops/adds, check which database engine was used

## PostgreSQL-Specific Features

These features only work with PostgreSQL:

```python
# JSONB columns
from sqlalchemy.dialects.postgresql import JSONB
metadata: dict = Field(sa_column=Column(JSONB))

# Array columns
from sqlalchemy import ARRAY, String
tags: List[str] = Field(sa_column=Column(ARRAY(String)))

# Partial indexes
Index('idx_active_only', 'name', postgresql_where=text('is_active = true'))

# Full-text search
Index('idx_search', text("to_tsvector('english', name)"), postgresql_using='gin')
```

## Engine Selection

For Vibe4Vets:

```python
# backend/app/core/database.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://localhost:5432/vibe4vets"  # Default to PostgreSQL
)
```

## Summary

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| ALTER TABLE | Limited | Full support |
| Drop columns | Batch mode only | Direct |
| Foreign keys | Limited ALTER | Full support |
| JSONB | No | Yes |
| Arrays | No | Yes |
| Full-text search | No | Yes |
| Partial indexes | No | Yes |

**Recommendation**: Use PostgreSQL for development and production. SQLite is only suitable for quick local testing without migrations.
