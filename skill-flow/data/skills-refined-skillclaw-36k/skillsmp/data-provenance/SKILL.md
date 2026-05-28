---
name: data-provenance
description: |
  Track data lineage and provenance from source to consumption. Use when auditing data flows,
  debugging data quality issues, ensuring compliance (GDPR, SOX), or understanding data dependencies.
  Covers lineage tracking, impact analysis, data catalogs, and metadata management.
---

# Data Provenance & Lineage

Track where data comes from, how it transforms, and where it goes—essential for trust, compliance, and debugging.

## When to Use

Use this skill when:
- Auditing data for compliance (GDPR, HIPAA, SOX, CCPA)
- Debugging data quality issues ("Where did this bad data come from?")
- Understanding impact of schema changes ("What breaks if I change this field?")
- Building data catalogs or governance systems
- Tracking sensitive data (PII, PHI) through systems
- Responding to data deletion requests (GDPR "right to be forgotten")

---

## What is Data Provenance?

**Provenance**: The complete history and lineage of a data element

```
Question: "Where does the revenue number in this dashboard come from?"

Answer (with provenance):
Dashboard.revenue (computed 2026-01-21 08:00)
  ← warehouse.daily_sales.total (aggregated 2026-01-21 02:00)
    ← etl_pipeline.transform_sales (ran 2026-01-21 01:30)
      ← production_db.orders.amount (order #12345, created 2026-01-20 15:23)
        ← stripe_api.charge (charge_id: ch_abc123, processed 2026-01-20 15:23)
          ← user input (customer: cust_xyz, card ending 4242)
```

**Key questions provenance answers**:
1. **Where** did this data come from? (source)
2. **When** was it created/updated? (timestamp)
3. **How** was it transformed? (logic, code version)
4. **Who** created/modified it? (user, system, process)
5. **Why** does it have this value? (business logic)
6. **What** depends on it? (downstream consumers)

---

## Levels of Provenance Tracking

### Level 1: Table-Level Lineage

**What**: Track which tables feed into other tables

```
┌────────────┐
│ orders     │──┐
└────────────┘  │
                ├──► ┌──────────────┐
┌────────────┐  │    │ daily_sales  │
│ customers  │──┘    └──────────────┘
└────────────┘
```

**Implementation: Metadata table**
```sql
CREATE TABLE table_lineage (
  downstream_table VARCHAR(255),
  upstream_table VARCHAR(255),
  relationship_type VARCHAR(50),  -- 'direct_copy', 'join', 'aggregate'
  created_at TIMESTAMPTZ DEFAULT NOW(),

  PRIMARY KEY (downstream_table, upstream_table)
);

INSERT INTO table_lineage VALUES
  ('daily_sales', 'orders', 'aggregate'),
  ('daily_sales', 'customers', 'join');
```

**Query**: "What tables does daily_sales depend on?"
```sql
SELECT upstream_table
FROM table_lineage
WHERE downstream_table = 'daily_sales';
-- Result: orders, customers
```

**Query**: "What tables depend on orders?"
```sql
SELECT downstream_table
FROM table_lineage
WHERE upstream_table = 'orders';
-- Result: daily_sales, weekly_report, customer_lifetime_value
```

### Level 2: Column-Level Lineage

**What**: Track which columns feed into which columns

```
orders.amount ──┐
orders.tax    ──┼──► daily_sales.total_revenue
orders.shipping─┘
```

**Implementation**:
```sql
CREATE TABLE column_lineage (
  downstream_table VARCHAR(255),
  downstream_column VARCHAR(255),
  upstream_table VARCHAR(255),
  upstream_column VARCHAR(255),
  transformation TEXT,  -- SQL or description
  created_at TIMESTAMPTZ DEFAULT NOW(),

  PRIMARY KEY (downstream_table, downstream_column, upstream_table, upstream_column)
);

INSERT INTO column_lineage VALUES
  ('daily_sales', 'total_revenue', 'orders', 'amount', 'SUM(amount + tax + shipping)'),
  ('daily_sales', 'order_count', 'orders', 'id', 'COUNT(id)'),
  ('daily_sales', 'customer_name', 'customers', 'name', 'LEFT JOIN on customer_id');
```

**Query**: "Where does daily_sales.total_revenue come from?"
```sql
SELECT
  upstream_table,
  upstream_column,
  transformation
FROM column_lineage
WHERE downstream_table = 'daily_sales'
  AND downstream_column = 'total_revenue';
```

### Level 3: Row-Level Lineage

**What**: Track individual record transformations

```
orders.id=12345 (amount=$100) ──► daily_sales.id=67 (date=2026-01-20, total=$100)
orders.id=12346 (amount=$50)  ──┘
```

**Implementation: Lineage table**
```sql
CREATE TABLE row_lineage (
  id BIGSERIAL PRIMARY KEY,
  downstream_table VARCHAR(255),
  downstream_pk BIGINT,
  upstream_table VARCHAR(255),
  upstream_pk BIGINT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- After ETL run
INSERT INTO row_lineage (downstream_table, downstream_pk, upstream_table, upstream_pk)
SELECT
  'daily_sales',
  ds.id,
  'orders',
  o.id
FROM daily_sales ds
JOIN orders o ON DATE(o.created_at) = ds.sale_date;
```

**Query**: "What orders contributed to daily_sales row 67?"
```sql
SELECT o.*
FROM row_lineage rl
JOIN orders o ON rl.upstream_pk = o.id
WHERE rl.downstream_table = 'daily_sales'
  AND rl.downstream_pk = 67;
```

### Level 4: Value-Level Lineage (Finest)

**What**: Track transformations at the field value level

```
order.amount = $100
order.tax = $10
order.shipping = $5
  ↓ (SUM transformation)
daily_sales.total_revenue = $115
```

**Implementation: Event log**
```sql
CREATE TABLE value_lineage (
  id BIGSERIAL PRIMARY KEY,
  entity_type VARCHAR(50),
  entity_id BIGINT,
  field_name VARCHAR(100),
  old_value TEXT,
  new_value TEXT,
  transformation TEXT,
  source_values JSONB,  -- Array of source values
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by VARCHAR(255)  -- User or process
);

-- Example: Revenue calculation
INSERT INTO value_lineage VALUES (
  DEFAULT,
  'daily_sales',
  67,
  'total_revenue',
  NULL,
  '115.00',
  'SUM(orders.amount + orders.tax + orders.shipping) WHERE date = 2026-01-20',
  '[{"table": "orders", "id": 12345, "amount": 100, "tax": 10, "shipping": 5}]',
  NOW(),
  'etl_pipeline_v1.2.3'
);
```

---

## Provenance Capture Methods

### Method 1: Code Instrumentation

**Manual tracking in ETL code**:
```python
def etl_orders_to_daily_sales():
    # Extract
    orders = db.query("SELECT * FROM orders WHERE date = ?", yesterday)

    # Transform
    daily_sales = {}
    for order in orders:
        date = order['created_at'].date()
        if date not in daily_sales:
            daily_sales[date] = {'total': 0, 'count': 0, 'order_ids': []}

        daily_sales[date]['total'] += order['amount']
        daily_sales[date]['count'] += 1
        daily_sales[date]['order_ids'].append(order['id'])

    # Load with lineage tracking
    for date, metrics in daily_sales.items():
        ds_id = db.insert(
            "INSERT INTO daily_sales (date, total, count) VALUES (?, ?, ?)",
            date, metrics['total'], metrics['count']
        )

        # Track lineage
        for order_id in metrics['order_ids']:
            db.insert(
                "INSERT INTO row_lineage (downstream_table, downstream_pk, upstream_table, upstream_pk) VALUES (?, ?, ?, ?)",
                'daily_sales', ds_id, 'orders', order_id
            )
```

### Method 2: SQL Parsing

**Automatically extract lineage from SQL queries**:
```python
import sqlparse
from sqllineage.runner import LineageRunner

sql = """
INSERT INTO daily_sales (date, total_revenue, order_count)
SELECT
  DATE(created_at) as date,
  SUM(amount + tax + shipping) as total_revenue,
  COUNT(*) as order_count
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.id
WHERE created_at >= '2026-01-20'
GROUP BY DATE(created_at)
"""

# Parse lineage
runner = LineageRunner(sql)

print("Source tables:", runner.source_tables)
# {'orders', 'customers'}

print("Target tables:", runner.target_tables)
# {'daily_sales'}

# Store in lineage table
for source in runner.source_tables:
    db.insert(
        "INSERT INTO table_lineage (downstream_table, upstream_table) VALUES (?, ?)",
        'daily_sales', source
    )
```

### Method 3: Database Triggers

**Capture changes automatically**:
```sql
-- Audit trail for all changes
CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  table_name VARCHAR(255),
  record_id BIGINT,
  operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
  old_values JSONB,
  new_values JSONB,
  changed_by VARCHAR(255),
  changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger on orders table
CREATE OR REPLACE FUNCTION audit_orders()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, operation, old_values, new_values, changed_by)
  VALUES (
    'orders',
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    row_to_json(OLD),
    row_to_json(NEW),
    current_user
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_audit
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION audit_orders();
```

### Method 4: CDC (Change Data Capture)

**Stream database changes**:
```python
# Using Debezium or similar CDC tool
from kafka import KafkaConsumer

consumer = KafkaConsumer('postgres.public.orders')

for message in consumer:
    change_event = json.loads(message.value)

    # Store in lineage system
    db.insert(
        "INSERT INTO change_log (table_name, operation, before, after, timestamp) VALUES (?, ?, ?, ?, ?)",
        change_event['source']['table'],
        change_event['op'],  # 'c' (create), 'u' (update), 'd' (delete)
        change_event.get('before'),
        change_event.get('after'),
        change_event['ts_ms']
    )
```

---

## Impact Analysis

### Downstream Impact

**Question**: "If I change orders.amount, what breaks?"

```sql
-- Find all downstream dependencies
WITH RECURSIVE dependencies AS (
  -- Base: Direct dependencies
  SELECT
    downstream_table,
    downstream_column,
    1 as depth
  FROM column_lineage
  WHERE upstream_table = 'orders'
    AND upstream_column = 'amount'

  UNION ALL

  -- Recursive: Dependencies of dependencies
  SELECT
    cl.downstream_table,
    cl.downstream_column,
    d.depth + 1
  FROM column_lineage cl
  JOIN dependencies d
    ON cl.upstream_table = d.downstream_table
   AND cl.upstream_column = d.downstream_column
  WHERE d.depth < 10  -- Prevent infinite loops
)
SELECT DISTINCT
  downstream_table,
  downstream_column,
  depth
FROM dependencies
ORDER BY depth, downstream_table, downstream_column;
```

**Result**:
```
| downstream_table       | downstream_column  | depth |
|------------------------|--------------------|-------|
| daily_sales            | total_revenue      | 1     |
| monthly_revenue        | total              | 2     |
| executive_dashboard    | ytd_revenue        | 3     |
| investor_report        | arr                | 4     |
```

**Interpretation**: Changing `orders.amount` affects 4 layers of downstream tables!

### Upstream Impact

**Question**: "What source data feeds into this dashboard metric?"

```sql
-- Trace backwards to original sources
WITH RECURSIVE sources AS (
  -- Base: Direct sources
  SELECT
    upstream_table,
    upstream_column,
    1 as depth
  FROM column_lineage
  WHERE downstream_table = 'executive_dashboard'
    AND downstream_column = 'ytd_revenue'

  UNION ALL

  -- Recursive: Sources of sources
  SELECT
    cl.upstream_table,
    cl.upstream_column,
    s.depth + 1
  FROM column_lineage cl
  JOIN sources s
    ON cl.downstream_table = s.upstream_table
   AND cl.downstream_column = s.upstream_column
  WHERE s.depth < 10
)
SELECT DISTINCT
  upstream_table,
  upstream_column,
  depth
FROM sources
WHERE upstream_table NOT IN (
  SELECT DISTINCT downstream_table FROM column_lineage
)  -- Only leaf nodes (true sources)
ORDER BY upstream_table, upstream_column;
```

**Result**: Original sources for dashboard metric
```
| upstream_table | upstream_column | depth |
|----------------|-----------------|-------|
| orders         | amount          | 4     |
| orders         | tax             | 4     |
| orders         | shipping        | 4     |
| stripe_events  | charge_amount   | 5     |
```

---

## Data Catalog

### Schema Registry

**Track all datasets and their metadata**:
```sql
CREATE TABLE data_catalog (
  id BIGSERIAL PRIMARY KEY,
  dataset_name VARCHAR(255) UNIQUE NOT NULL,
  dataset_type VARCHAR(50),  -- 'table', 'view', 'api', 'file'
  description TEXT,
  owner VARCHAR(255),
  steward VARCHAR(255),  -- Data steward (responsible for quality)
  sensitivity VARCHAR(50),  -- 'public', 'internal', 'confidential', 'restricted'
  contains_pii BOOLEAN DEFAULT FALSE,
  retention_days INT,  -- How long to keep data
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE data_catalog_columns (
  dataset_id BIGINT REFERENCES data_catalog(id),
  column_name VARCHAR(255),
  data_type VARCHAR(50),
  description TEXT,
  is_nullable BOOLEAN,
  is_pii BOOLEAN DEFAULT FALSE,
  pii_type VARCHAR(50),  -- 'email', 'ssn', 'phone', 'name', etc.
  sample_values TEXT[],

  PRIMARY KEY (dataset_id, column_name)
);

-- Example: Register orders table
INSERT INTO data_catalog VALUES (
  DEFAULT,
  'orders',
  'table',
  'Customer orders from e-commerce platform',
  'engineering@company.com',
  'data-team@company.com',
  'internal',
  TRUE,  -- Contains PII
  2555,  -- 7 years retention
  NOW(),
  NOW()
);

INSERT INTO data_catalog_columns VALUES
  (1, 'id', 'BIGINT', 'Unique order ID', FALSE, FALSE, NULL, NULL),
  (1, 'customer_email', 'VARCHAR(255)', 'Customer email address', FALSE, TRUE, 'email', NULL),
  (1, 'amount', 'DECIMAL(10,2)', 'Order total in USD', FALSE, FALSE, NULL, '{10.99, 25.50, 100.00}');
```

### Searchable Catalog

**Find datasets by keyword**:
```sql
-- Full-text search
CREATE INDEX idx_catalog_search ON data_catalog
USING GIN(to_tsvector('english', dataset_name || ' ' || description));

-- Search for "revenue"
SELECT
  dataset_name,
  dataset_type,
  description,
  owner
FROM data_catalog
WHERE to_tsvector('english', dataset_name || ' ' || description)
   @@ to_tsquery('english', 'revenue')
ORDER BY dataset_name;
```

---

## Compliance & Data Privacy

### GDPR: Right to be Forgotten

**Track all PII to enable deletion**:
```sql
-- Find all PII for a user
SELECT
  dc.dataset_name,
  dcc.column_name,
  dcc.pii_type
FROM data_catalog dc
JOIN data_catalog_columns dcc ON dc.id = dcc.dataset_id
WHERE dcc.is_pii = TRUE;

-- Result: Tables/columns containing PII
| dataset_name    | column_name    | pii_type |
|-----------------|----------------|----------|
| orders          | customer_email | email    |
| users           | email          | email    |
| users           | name           | name     |
| support_tickets | email          | email    |
| analytics_events| user_id        | user_id  |

-- Generate deletion script
SELECT
  'DELETE FROM ' || dataset_name || ' WHERE ' || column_name || ' = ''' || user_email || ''';'
FROM (
  SELECT DISTINCT
    dc.dataset_name,
    dcc.column_name
  FROM data_catalog dc
  JOIN data_catalog_columns dcc ON dc.id = dcc.dataset_id
  WHERE dcc.pii_type = 'email'
) subq;

-- Output:
-- DELETE FROM orders WHERE customer_email = 'user@example.com';
-- DELETE FROM users WHERE email = 'user@example.com';
-- DELETE FROM support_tickets WHERE email = 'user@example.com';
```

### PII Tracking in Data Flow

**Tag PII as it flows through pipeline**:
```python
def track_pii_flow(source_table, dest_table, pii_fields):
    """Track movement of PII between tables"""
    for field in pii_fields:
        db.insert(
            """
            INSERT INTO pii_lineage (source_table, source_column, dest_table, dest_column, tracked_at)
            VALUES (?, ?, ?, ?, NOW())
            """,
            source_table, field, dest_table, field
        )

# Usage
track_pii_flow('users', 'orders', ['email'])
track_pii_flow('orders', 'daily_sales_with_emails', ['email'])

# Query: "Where has this user's email propagated?"
db.query("""
  WITH RECURSIVE pii_flow AS (
    SELECT dest_table, dest_column, 1 as depth
    FROM pii_lineage
    WHERE source_table = 'users' AND source_column = 'email'

    UNION ALL

    SELECT pl.dest_table, pl.dest_column, pf.depth + 1
    FROM pii_lineage pl
    JOIN pii_flow pf ON pl.source_table = pf.dest_table AND pl.source_column = pf.dest_column
    WHERE pf.depth < 10
  )
  SELECT DISTINCT dest_table, dest_column FROM pii_flow;
""")
```

---

## Visualization & Tools

### Lineage Graph

**Generate visual lineage**:
```python
import graphviz

def visualize_lineage(table_name):
    # Fetch lineage
    lineage = db.query("""
        SELECT upstream_table, downstream_table
        FROM table_lineage
        WHERE upstream_table = ? OR downstream_table = ?
    """, table_name, table_name)

    # Create graph
    dot = graphviz.Digraph()

    for row in lineage:
        dot.edge(row['upstream_table'], row['downstream_table'])

    dot.render('lineage_graph', format='png', view=True)

visualize_lineage('orders')
```

**Output**:
```
stripe_api ──► orders ──┬──► daily_sales ──► monthly_revenue
                        │
customers ──────────────┘
```

### Commercial Tools

| Tool | Use Case | Features |
|------|----------|----------|
| **Apache Atlas** | Open-source data governance | Metadata management, lineage, search |
| **Collibra** | Enterprise data governance | Catalog, lineage, policies, workflows |
| **Alation** | Data catalog | Metadata search, collaboration, lineage |
| **Amundsen** (Lyft) | Open-source data discovery | Search, lineage, usage analytics |
| **DataHub** (LinkedIn) | Open-source metadata platform | Lineage, discovery, governance |
| **dbt** | Analytics engineering | SQL lineage, documentation, tests |

---

## Implementation Checklist

### Minimal (Start Here)

```
[ ] Table-level lineage tracking
[ ] Audit logs for critical tables
[ ] Data catalog for major datasets
[ ] Documentation of ETL processes
```

### Standard

```
[ ] Column-level lineage
[ ] Automated lineage extraction from SQL
[ ] PII tagging and tracking
[ ] Impact analysis queries
[ ] Change notifications for downstream consumers
```

### Advanced

```
[ ] Row-level lineage
[ ] Real-time lineage from CDC
[ ] Searchable data catalog
[ ] Automated GDPR compliance tools
[ ] Data quality metrics tied to lineage
[ ] Machine learning for anomaly detection
```

---

## Output Format

When helping with data provenance:

```
## Provenance Strategy

### Lineage Level
- [ ] Table-level
- [ ] Column-level
- [ ] Row-level
- [ ] Value-level

### Capture Method
- [ ] Code instrumentation
- [ ] SQL parsing
- [ ] Database triggers
- [ ] CDC (Change Data Capture)

### Data Catalog Schema

[SQL DDL for catalog tables]

### Impact Analysis Queries

[SQL queries for upstream/downstream impact]

### PII Tracking

Tables with PII:
- [Table 1]: [Columns]
- [Table 2]: [Columns]

Deletion strategy:
[Step-by-step process]

### Visualization

[Lineage graph representation]

### Compliance Requirements
- [ ] GDPR
- [ ] CCPA
- [ ] HIPAA
- [ ] SOX
- [ ] Other: [specify]

### Tooling
- Lineage tracking: [Tool/Custom]
- Data catalog: [Tool/Custom]
- Visualization: [Tool/Custom]
```

---

## Integration

Works with:
- **scalable-data-schema** - Track schema evolution over time
- **data-infrastructure-at-scale** - Lineage for pipelines and ETL
- **multi-source-data-conflation** - Track source of merged data
- **systems-decompose** - Plan lineage as part of feature design
