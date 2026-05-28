---
name: multi-source-data-conflation
description: |
  Merge and reconcile data from multiple sources into a unified view. Use when integrating APIs,
  consolidating databases, building data warehouses, or creating master data. Covers entity
  resolution, conflict resolution, data quality, and real-time vs batch conflation.
---

# Multi-Source Data Conflation

Merge data from disparate sources into a single, unified, and accurate view.

## When to Use

Use this skill when:
- Integrating data from multiple APIs or databases
- Building a "single source of truth" from fragmented systems
- Merging customer data from different platforms (CRM, support, analytics)
- Consolidating after company acquisition or system migration
- Creating a data warehouse from operational databases
- Resolving duplicate or conflicting records

---

## Core Challenges

### 1. Entity Resolution

**Problem**: Is "John Smith, john@gmail.com" the same person as "J. Smith, jsmith@gmail.com"?

**Strategies**:

**Exact Match** (simplest):
```python
def deduplicate_exact(records):
    seen = set()
    unique = []

    for record in records:
        key = (record['email'].lower(), record['phone'])
        if key not in seen:
            seen.add(key)
            unique.append(record)

    return unique
```
- ✓ Fast, simple
- ✗ Misses near-duplicates

**Fuzzy Matching** (similar records):
```python
from fuzzywuzzy import fuzz

def are_similar(record1, record2, threshold=85):
    # Compare names
    name_score = fuzz.ratio(record1['name'], record2['name'])

    # Compare emails (domain must match)
    email1_domain = record1['email'].split('@')[1]
    email2_domain = record2['email'].split('@')[1]

    if email1_domain != email2_domain:
        return False

    # Combined score
    return name_score >= threshold

# Example
are_similar(
    {'name': 'John Smith', 'email': 'john@gmail.com'},
    {'name': 'Jon Smith', 'email': 'jsmith@gmail.com'}
)  # True (typo in first name)
```

**Probabilistic Matching** (ML-based):
```python
from recordlinkage import Compare

# Features for matching
compare = Compare()
compare.exact('email', 'email')  # Email must match exactly
compare.string('name', 'name', method='jarowinkler')  # Name similarity
compare.numeric('age', 'age', method='gauss')  # Age proximity

# Train a classifier
# Score each pair: 0 (different entities) to 1 (same entity)
scores = compare.compute(pairs, dataset1, dataset2)
matches = scores[scores['total_score'] > 0.8]
```

**Deterministic Rules** (business logic):
```python
def match_customers(customer1, customer2):
    # Rule 1: Email match = 100% match
    if customer1['email'] == customer2['email']:
        return True

    # Rule 2: Phone + same last name = match
    if (customer1['phone'] == customer2['phone'] and
        customer1['last_name'] == customer2['last_name']):
        return True

    # Rule 3: Same full name + address = match
    if (customer1['full_name'] == customer2['full_name'] and
        customer1['zip_code'] == customer2['zip_code']):
        return True

    return False
```

### 2. Conflict Resolution

**Problem**: Source A says user's email is "old@example.com", Source B says "new@example.com"

**Strategies**:

**Most Recent Wins**:
```python
def merge_records(records):
    # Sort by timestamp, take latest
    records.sort(key=lambda r: r['updated_at'], reverse=True)
    return records[0]
```

**Most Trusted Source**:
```python
# Source priority: CRM > Support > Analytics
SOURCE_PRIORITY = {'crm': 1, 'support': 2, 'analytics': 3}

def merge_records(records):
    records.sort(key=lambda r: SOURCE_PRIORITY[r['source']])
    return records[0]
```

**Field-level Merge**:
```python
def merge_records(records):
    merged = {}

    for field in ['name', 'email', 'phone', 'address']:
        # Take non-null value from highest priority source
        for record in sorted(records, key=lambda r: SOURCE_PRIORITY[r['source']]):
            if record.get(field):
                merged[field] = record[field]
                break

    return merged

# Example
merge_records([
    {'source': 'analytics', 'email': None, 'phone': '555-1234'},
    {'source': 'crm', 'email': 'user@example.com', 'phone': None}
])
# Result: {'email': 'user@example.com', 'phone': '555-1234'}
```

**Majority Vote**:
```python
from collections import Counter

def resolve_by_vote(values):
    # Most common value wins
    if not values:
        return None

    counter = Counter(values)
    most_common = counter.most_common(1)[0]

    return most_common[0]

# Example
emails = ['user@example.com', 'user@example.com', 'old@example.com']
resolve_by_vote(emails)  # 'user@example.com' (2 vs 1)
```

**Custom Business Logic**:
```python
def resolve_email_conflict(records):
    # Business rule: Corporate email > personal email
    corporate_domains = ['company.com', 'corp.com']

    for record in records:
        email = record.get('email', '')
        domain = email.split('@')[1] if '@' in email else ''

        if domain in corporate_domains:
            return record['email']

    # Fallback: most recent
    records.sort(key=lambda r: r['updated_at'], reverse=True)
    return records[0]['email']
```

### 3. Data Quality

**Problem**: Garbage in, garbage out

**Validation Rules**:
```python
from pydantic import BaseModel, EmailStr, validator

class Customer(BaseModel):
    email: EmailStr  # Must be valid email
    phone: str
    age: int

    @validator('phone')
    def validate_phone(cls, v):
        # Must be 10 digits
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) != 10:
            raise ValueError('Phone must be 10 digits')
        return digits

    @validator('age')
    def validate_age(cls, v):
        if not 0 <= v <= 120:
            raise ValueError('Invalid age')
        return v

# Usage
try:
    customer = Customer(
        email='user@example.com',
        phone='(555) 123-4567',
        age=30
    )
except ValidationError as e:
    logger.error("Invalid data", errors=e.errors())
```

**Data Cleansing**:
```python
def cleanse_customer(raw_data):
    cleaned = {}

    # Standardize name (title case)
    cleaned['name'] = raw_data.get('name', '').strip().title()

    # Normalize email (lowercase)
    cleaned['email'] = raw_data.get('email', '').strip().lower()

    # Normalize phone (digits only)
    phone = raw_data.get('phone', '')
    cleaned['phone'] = ''.join(filter(str.isdigit, phone))

    # Standardize address (remove extra spaces)
    address = raw_data.get('address', '')
    cleaned['address'] = ' '.join(address.split())

    # Parse dates consistently
    if raw_data.get('birthdate'):
        cleaned['birthdate'] = parse_date(raw_data['birthdate'])

    return cleaned
```

---

## Conflation Patterns

### Pattern 1: Batch ETL (Nightly)

**Use when**: Daily updates are acceptable, large data volumes

```python
# Run nightly at 2am
def nightly_conflation():
    # 1. Extract from all sources
    crm_customers = extract_from_crm()
    support_customers = extract_from_support()
    analytics_events = extract_from_analytics()

    # 2. Transform: Normalize to common schema
    normalized = []
    for customer in crm_customers:
        normalized.append({
            'source': 'crm',
            'external_id': customer['id'],
            'email': customer['email'].lower(),
            'name': customer['name'].title(),
            'updated_at': customer['modified_date']
        })

    # ... normalize other sources

    # 3. Conflate: Group by email, merge
    by_email = {}
    for record in normalized:
        email = record['email']
        if email not in by_email:
            by_email[email] = []
        by_email[email].append(record)

    # 4. Resolve conflicts
    master_records = []
    for email, records in by_email.items():
        merged = merge_records(records)
        master_records.append(merged)

    # 5. Load into master database
    master_db.truncate('customers')
    master_db.bulk_insert('customers', master_records)
```

**Pros**: Simple, resource-efficient
**Cons**: Data up to 24 hours stale

### Pattern 2: Incremental Updates

**Use when**: Need fresher data, manageable update volume

```python
# Track last sync time per source
last_sync = {
    'crm': datetime(2026, 1, 20, 14, 0, 0),
    'support': datetime(2026, 1, 20, 14, 0, 0)
}

def incremental_sync():
    # Only fetch records updated since last sync
    crm_updates = crm_api.get_customers(
        modified_after=last_sync['crm']
    )

    for customer in crm_updates:
        # Find existing master record
        master = master_db.query(
            "SELECT * FROM customers WHERE email = ?",
            customer['email']
        )

        if master:
            # Merge and update
            merged = merge_records([master, normalize(customer)])
            master_db.update('customers', merged)
        else:
            # New customer
            master_db.insert('customers', normalize(customer))

    # Update last sync time
    last_sync['crm'] = datetime.now()
```

**Pros**: Fresher data (minutes old)
**Cons**: More complex, potential for partial failures

### Pattern 3: Real-time Streaming

**Use when**: Need immediate updates, event-driven architecture

```python
# Listen to events from all sources
@kafka.subscribe('customer_updates')
def handle_customer_update(event):
    source = event['source']
    customer_data = event['data']

    # Normalize
    normalized = normalize(customer_data, source)

    # Fetch existing master record
    master = master_db.query(
        "SELECT * FROM customers WHERE email = ?",
        normalized['email']
    )

    if master:
        # Merge
        merged = merge_records([master, normalized])

        # Only update if newer
        if merged['updated_at'] > master['updated_at']:
            master_db.update('customers', merged)
    else:
        # Create new
        master_db.insert('customers', normalized)

# Producers
@crm.on_customer_change
def publish_crm_update(customer):
    kafka.publish('customer_updates', {
        'source': 'crm',
        'data': customer
    })
```

**Pros**: Real-time, event-driven
**Cons**: Complex, requires message queue infrastructure

### Pattern 4: Federation (Virtual Conflation)

**Use when**: Sources can't be copied, query-time conflation acceptable

```python
# Don't copy data, query all sources at runtime
def get_customer_360(email):
    # Query all sources in parallel
    results = await asyncio.gather(
        crm_api.get_customer(email=email),
        support_api.get_tickets(email=email),
        analytics_api.get_events(email=email)
    )

    crm_data, support_data, analytics_data = results

    # Merge at query time
    return {
        'profile': crm_data,
        'support_tickets': support_data['tickets'],
        'recent_events': analytics_data['events'][-10:],
        'lifetime_value': analytics_data['ltv']
    }
```

**Pros**: Always fresh, no storage duplication
**Cons**: Slow queries, dependent on source availability

---

## Schema Mapping

### Challenges

**Different field names**:
```python
# Source A
{'firstName': 'John', 'lastName': 'Smith'}

# Source B
{'first_name': 'John', 'family_name': 'Smith'}

# Master schema
{'first_name': 'John', 'last_name': 'Smith'}
```

**Different data types**:
```python
# Source A: String
{'created_at': '2026-01-15T10:30:00Z'}

# Source B: Unix timestamp
{'created_at': 1737801000}

# Master schema: datetime
{'created_at': datetime(2026, 1, 15, 10, 30, 0)}
```

**Different structures**:
```python
# Source A: Nested
{
    'name': {'first': 'John', 'last': 'Smith'},
    'contact': {'email': 'john@example.com'}
}

# Source B: Flat
{
    'first_name': 'John',
    'last_name': 'Smith',
    'email': 'john@example.com'
}
```

### Mapping Framework

```python
class SourceMapper:
    """Map source schema to master schema"""

    def __init__(self, source_name):
        self.source = source_name
        self.field_map = self.get_field_map()

    def get_field_map(self):
        """Define mapping for this source"""
        if self.source == 'crm':
            return {
                'id': 'customer_id',
                'email': 'email_address',
                'name': lambda r: f"{r['firstName']} {r['lastName']}",
                'created_at': lambda r: parse_date(r['dateCreated'])
            }
        elif self.source == 'support':
            return {
                'id': 'user_id',
                'email': 'email',
                'name': 'full_name',
                'created_at': lambda r: datetime.fromtimestamp(r['created'])
            }

    def map(self, source_record):
        """Transform source record to master schema"""
        master = {}

        for master_field, source_field in self.field_map.items():
            if callable(source_field):
                # Custom transformation
                master[master_field] = source_field(source_record)
            else:
                # Direct mapping
                master[master_field] = source_record.get(source_field)

        master['source'] = self.source
        master['source_id'] = source_record.get(self.field_map.get('id'))

        return master

# Usage
crm_mapper = SourceMapper('crm')
support_mapper = SourceMapper('support')

crm_record = {'customer_id': 123, 'firstName': 'John', 'lastName': 'Smith', ...}
support_record = {'user_id': 456, 'full_name': 'John Smith', ...}

master1 = crm_mapper.map(crm_record)
master2 = support_mapper.map(support_record)

# Now both are in master schema
```

---

## Master Data Management

### Golden Record

**Pattern**: Maintain a "golden record" for each entity

```sql
-- Master customer table
CREATE TABLE customers (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,  -- Master identifier
  name VARCHAR(255),
  phone VARCHAR(20),
  address TEXT,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ,

  -- Metadata
  source_of_truth VARCHAR(50),  -- Which source is most trusted
  confidence_score FLOAT,       -- 0-1, how confident in data quality
  last_verified_at TIMESTAMPTZ
);

-- Source mapping table
CREATE TABLE customer_source_mappings (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT REFERENCES customers(id),
  source_name VARCHAR(50) NOT NULL,  -- 'crm', 'support', etc.
  source_id VARCHAR(255) NOT NULL,   -- ID in source system
  created_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(source_name, source_id)
);

-- Field-level lineage
CREATE TABLE customer_field_lineage (
  customer_id BIGINT REFERENCES customers(id),
  field_name VARCHAR(50),
  value TEXT,
  source_name VARCHAR(50),
  updated_at TIMESTAMPTZ,

  PRIMARY KEY (customer_id, field_name)
);
```

**Query golden record with lineage**:
```sql
SELECT
  c.id,
  c.email,
  c.name,
  jsonb_object_agg(
    fl.field_name,
    jsonb_build_object(
      'value', fl.value,
      'source', fl.source_name,
      'updated_at', fl.updated_at
    )
  ) as field_lineage
FROM customers c
LEFT JOIN customer_field_lineage fl ON c.id = fl.customer_id
WHERE c.email = 'user@example.com'
GROUP BY c.id, c.email, c.name;
```

### Survivorship Rules

**Define which source "survives" for each field**:

```python
SURVIVORSHIP_RULES = {
    'email': 'most_recent',           # Latest email always wins
    'name': 'most_trusted',           # CRM > Support > Analytics
    'phone': 'most_complete',         # Longest phone number
    'address': 'manual_override',     # User-edited takes precedence
    'created_at': 'earliest',         # Earliest registration date
}

def apply_survivorship(field, values):
    rule = SURVIVORSHIP_RULES[field]

    if rule == 'most_recent':
        return max(values, key=lambda v: v['updated_at'])['value']

    elif rule == 'most_trusted':
        priority = {'crm': 1, 'support': 2, 'analytics': 3}
        return min(values, key=lambda v: priority[v['source']])['value']

    elif rule == 'most_complete':
        return max(values, key=lambda v: len(v['value'] or ''))['value']

    elif rule == 'manual_override':
        manual = [v for v in values if v['source'] == 'manual']
        if manual:
            return manual[0]['value']
        return values[0]['value']

    elif rule == 'earliest':
        return min(values, key=lambda v: v['value'])['value']
```

---

## Handling Changes Over Time

### Slowly Changing Dimensions (SCD)

**Type 1**: Overwrite (no history)
```sql
UPDATE customers
SET email = 'new@example.com'
WHERE id = 123;
-- Old email is lost
```

**Type 2**: Add new row (full history)
```sql
CREATE TABLE customers_scd2 (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL,       -- Logical ID
  email VARCHAR(255),
  name VARCHAR(255),
  valid_from TIMESTAMPTZ NOT NULL,
  valid_to TIMESTAMPTZ,              -- NULL = current
  is_current BOOLEAN DEFAULT TRUE
);

-- Insert new version
INSERT INTO customers_scd2 (customer_id, email, valid_from)
VALUES (123, 'new@example.com', NOW());

-- Mark old version as historical
UPDATE customers_scd2
SET valid_to = NOW(), is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE;

-- Query current state
SELECT * FROM customers_scd2
WHERE customer_id = 123 AND is_current = TRUE;

-- Query state at specific time
SELECT * FROM customers_scd2
WHERE customer_id = 123
  AND valid_from <= '2026-01-15'
  AND (valid_to IS NULL OR valid_to > '2026-01-15');
```

**Type 3**: Add column (limited history)
```sql
ALTER TABLE customers ADD COLUMN previous_email VARCHAR(255);

-- On update
UPDATE customers
SET previous_email = email,
    email = 'new@example.com'
WHERE id = 123;
-- Only keeps one previous value
```

---

## Data Quality Monitoring

### Metrics to Track

```python
def calculate_quality_metrics(merged_data):
    metrics = {
        'total_records': len(merged_data),
        'completeness': {},
        'conflicts': 0,
        'duplicates': 0,
        'sources': {}
    }

    # Completeness: % of non-null values per field
    for field in ['email', 'name', 'phone', 'address']:
        non_null = sum(1 for r in merged_data if r.get(field))
        metrics['completeness'][field] = non_null / len(merged_data)

    # Conflicts: Records with different values from different sources
    for record in merged_data:
        if len(record.get('source_values', {})) > 1:
            metrics['conflicts'] += 1

    # Duplicates: Records with same email
    emails = [r['email'] for r in merged_data if r.get('email')]
    metrics['duplicates'] = len(emails) - len(set(emails))

    # Source distribution
    for record in merged_data:
        source = record.get('source', 'unknown')
        metrics['sources'][source] = metrics['sources'].get(source, 0) + 1

    return metrics

# Example output
{
    'total_records': 10000,
    'completeness': {
        'email': 0.98,    # 98% have email
        'name': 0.95,
        'phone': 0.72,    # Only 72% have phone - flag for review
        'address': 0.45   # Low! Action needed
    },
    'conflicts': 234,     # 234 records have conflicting data
    'duplicates': 12,
    'sources': {
        'crm': 6000,
        'support': 3500,
        'analytics': 500
    }
}
```

### Automated Data Quality Rules

```python
from great_expectations import DataContext

# Define expectations
def validate_merged_data(df):
    expectations = [
        # Email must exist and be valid
        df.expect_column_values_to_not_be_null('email'),
        df.expect_column_values_to_match_regex('email', r'^[\w\.-]+@[\w\.-]+\.\w+$'),

        # Email must be unique
        df.expect_column_values_to_be_unique('email'),

        # Name must exist
        df.expect_column_values_to_not_be_null('name'),

        # Age must be in valid range (if present)
        df.expect_column_values_to_be_between('age', 0, 120, mostly=0.99),

        # Source must be known
        df.expect_column_values_to_be_in_set('source', ['crm', 'support', 'analytics'])
    ]

    results = df.validate()

    if not results['success']:
        logger.error("Data quality check failed", failures=results['failures'])
        # Alert or halt pipeline

    return results
```

---

## Output Format

When helping with data conflation:

```
## Conflation Strategy

### Sources Identified
1. [Source A]: [Schema, update frequency, trustworthiness]
2. [Source B]: [Schema, update frequency, trustworthiness]

### Entity Resolution Strategy
- Matching key: [field(s) used to match]
- Fuzzy matching: [Yes/No, threshold if yes]
- Expected match rate: [X%]

### Conflict Resolution Rules
- Field 1: [Strategy (most recent, most trusted, etc.)]
- Field 2: [Strategy]

### Schema Mapping

[Source A] → [Master Schema]
- source_field_1 → master_field_1
- source_field_2 → master_field_2 (transformation: [description])

[Source B] → [Master Schema]
...

### Implementation Approach
- [ ] Pattern: [Batch/Incremental/Real-time/Federation]
- [ ] Frequency: [Nightly/Hourly/Real-time]
- [ ] Technology: [ETL tool/Code/Platform]

### Data Quality Metrics
- Completeness targets: [field: X%]
- Duplicate tolerance: [< X%]
- Conflict resolution: [automated/manual review]

### Risks & Mitigation
- Risk 1: [Mitigation]
- Risk 2: [Mitigation]
```

---

## Integration

Works with:
- **scalable-data-schema** - Design master schema
- **data-infrastructure-at-scale** - Build pipeline infrastructure
- **data-provenance** - Track data lineage through conflation
- **systems-decompose** - Plan conflation as part of feature
