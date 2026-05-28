# Documentation Transformation Patterns

Concrete before/after examples showing how to transform documentation from 7/10 → 9/10.

## Pattern 1: Add Quick Start Section

### Before (7/10)

```markdown
# My Project

This project provides tools for analyzing crypto data.

## Installation

pip install myproject

## Usage

See examples directory for usage patterns.
```

**Problems**:
- No immediate working example
- User must explore examples directory
- Unclear what the project actually does
- Time-to-first-success: >5 minutes

### After (9/10)

```markdown
# My Project

Query remote Parquet files without downloading using DuckDB.

## Quick Start

Prerequisites: Python 3.8+, install with: `pip install duckdb myproject`

python
import duckdb

# Query remote data (no download required)
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

result = conn.execute("""
    SELECT date, symbol, price
    FROM read_parquet('https://example.com/data.parquet')
    WHERE symbol = 'BTCUSDT'
    LIMIT 5
""").fetchall()

print(result)  # Expected: [(2024-01-01, BTCUSDT, 42000), ...]


See [Full Documentation](#full-documentation) for advanced usage.

---

## Installation
[rest of docs...]
```

**Improvements**:
- Copy-paste working example at top
- Clear value proposition (1 sentence)
- Prerequisites inline
- Expected output shown
- Time-to-first-success: <60 seconds

**Effort**: 30 minutes
**Impact**: +2 points

## Pattern 2: Make Prerequisites Explicit

### Before (6/10)

```markdown
## Installation

pip install myproject
```

**Problems**:
- Python version unstated
- Dependencies unclear
- Platform requirements unknown

### After (9/10)

```markdown
## Prerequisites

### Required

- **Python**: 3.8 or later ([download](https://www.python.org/downloads/))
- **DuckDB**: 1.0.0+ (installed automatically via pip)

### Optional

- **PyArrow**: Faster Parquet reads (`pip install pyarrow`)

### Verification

bash
python --version  # Should be 3.8+
python -c "import duckdb; print(duckdb.__version__)"  # Should be 1.0.0+


## Installation

bash
# Install from PyPI
pip install myproject

# Or install from source
git clone https://github.com/org/myproject
cd myproject
pip install -e .

```

**Improvements**:
- Explicit version requirements
- Platform-independent install commands
- Verification steps
- Optional dependencies separated

**Effort**: 15 minutes
**Impact**: +1.5 points

## Pattern 3: Transform Abstract Examples to Concrete

### Before (7/10)

```markdown
## Examples

python
from myproject import query_data

# Query data
result = query_data(url, filters)
print(result)

```

**Problems**:
- Placeholder variables (url, filters)
- Unclear what filters should be
- Can't copy-paste and run
- No expected output

### After (9/10)

```markdown
## Examples

### Example 1: Query Single Symbol

python
import duckdb

conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

# Query BTCUSDT data for 2024
result = conn.execute("""
    SELECT date, open, high, low, close, volume
    FROM read_parquet('https://cdn.jsdelivr.net/gh/org/data@v1.0.0/availability.parquet')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
    ORDER BY date DESC
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]}: Open={row[1]}, Close={row[4]}, Vol={row[5]}")


**Expected Output**:
2024-11-15: Open=89123.45, Close=91234.56, Vol=12345678
2024-11-14: Open=88234.12, Close=89123.45, Vol=11234567
...


### Example 2: Aggregate Daily Volume

python
# Calculate total volume by symbol
result = conn.execute("""
    SELECT symbol, SUM(volume) as total_volume
    FROM read_parquet('https://cdn.jsdelivr.net/gh/org/data@v1.0.0/availability.parquet')
    WHERE date >= '2024-01-01'
    GROUP BY symbol
    ORDER BY total_volume DESC
    LIMIT 5
""").fetchall()

print("Top 5 symbols by volume:")
for symbol, volume in result:
    print(f"{symbol}: {volume:,.0f}")


**Expected Output**:
Top 5 symbols by volume:
BTCUSDT: 123,456,789,012
ETHUSDT: 98,765,432,109
...

```

**Improvements**:
- Real URLs (not placeholders)
- Copy-paste ready
- Expected output shown
- Multiple examples (simple → complex)
- Domain-specific (crypto data)

**Effort**: 45 minutes
**Impact**: +2 points

## Pattern 4: Add Troubleshooting Section

### Before (4/10)

```markdown
## Usage

[examples...]

For issues, see GitHub Issues.
```

**Problems**:
- No self-service troubleshooting
- Users must search issues or create new ones
- Common errors undocumented

### After (8/10)

```markdown
## Troubleshooting

### Issue: "DuckDB cannot find httpfs extension"

**Symptom**:
Error: Extension "httpfs" not found


**Diagnosis**:
bash
# Check if httpfs is available
duckdb -c "SELECT * FROM duckdb_extensions() WHERE extension_name='httpfs'"


**Solution**:
python
# Install httpfs extension manually
conn.execute("INSTALL httpfs FROM 'https://extensions.duckdb.org'")
conn.execute("LOAD httpfs")


---

### Issue: Query downloads full file (not using range requests)

**Symptom**:
Query takes 30+ seconds for small result


**Diagnosis**:
bash
# Check if server supports range requests
curl -I https://your-url/data.parquet | grep "Accept-Ranges"
# Should see: Accept-Ranges: bytes


**Solution**:
If server doesn't support range requests, use CDN proxy:

python
# Instead of direct GitHub Releases URL:
bad_url = "https://github.com/org/repo/releases/download/v1.0.0/data.parquet"

# Use jsDelivr CDN proxy:
good_url = "https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet"

result = conn.execute(f"SELECT * FROM read_parquet('{good_url}') LIMIT 5").fetchall()


---

### Issue: Memory error on large queries

**Symptom**:
OutOfMemoryError: Failed to allocate ...


**Solution**:
sql
-- Increase DuckDB memory limit
SET memory_limit = '4GB';  -- Adjust based on available RAM

-- Or filter data to reduce memory usage
SELECT *
FROM read_parquet('url')
WHERE date >= '2024-01-01'  -- Reduce scanned rows
  AND symbol IN ('BTCUSDT', 'ETHUSDT')  -- Limit to specific symbols


---

### Still Having Issues?

1. Check [GitHub Issues](https://github.com/org/repo/issues) for similar problems
2. Run diagnostic: `duckdb -c "SELECT version()"`
3. Include error message and minimal reproducible example when filing new issue
```

**Improvements**:
- 3-5 common errors documented
- Symptom → Diagnosis → Solution pattern
- Diagnostic commands provided
- Copy-paste solutions
- Escalation path (GitHub Issues)

**Effort**: 1 hour
**Impact**: +2 points

## Pattern 5: Improve Navigation with Table of Contents

### Before (6/10)

```markdown
# My Project

[Long wall of text with sections buried deep...]

## Installation
[...]

## Advanced Usage
[...]

## API Reference
[...]
```

**Problems**:
- Can't scan available sections
- Must scroll to find information
- No clear hierarchy

### After (9/10)

```markdown
# My Project

Query remote Parquet files without downloading using DuckDB.

## Table of Contents

- [Quick Start](#quick-start) - Get running in <60 seconds
- [Installation](#installation) - Prerequisites and setup
- [Examples](#examples) - Common usage patterns
  - [Basic Queries](#basic-queries)
  - [Aggregations](#aggregations)
  - [Caching](#caching)
- [Troubleshooting](#troubleshooting) - Common errors and solutions
- [Advanced](#advanced) - Performance tuning and optimization
- [API Reference](#api-reference) - Full function documentation

---

## Quick Start

[copy-paste example...]

## Installation

### Prerequisites
[...]

[rest of docs with clear sections...]
```

**Improvements**:
- Scannable TOC at top
- Descriptive annotations (what each section contains)
- Nested sections shown
- Jump links work
- Progressive disclosure (Quick Start first)

**Effort**: 20 minutes
**Impact**: +1 point

## Pattern 6: Replace Placeholder Content

### Before (7/10)

```markdown
## Configuration

python
# TODO: Document configuration options
config = {
    "url": "YOUR_URL_HERE",
    "api_key": "YOUR_API_KEY",
}

```

**Problems**:
- Placeholder values confuse users
- TODO items make docs feel incomplete
- Unclear what valid values are

### After (9/10)

```markdown
## Configuration

### Environment Variables (Recommended)

bash
# Set your data URL
export DATA_URL="https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet"

# Optional: Set API key for private repositories
export GITHUB_TOKEN="ghp_abc123..."  # Generate at: https://github.com/settings/tokens


### Python Configuration

python
import os
import duckdb

# Load from environment
data_url = os.getenv("DATA_URL")

conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

# Optional: Authenticate for private repositories
if token := os.getenv("GITHUB_TOKEN"):
    conn.execute(f"SET s3_access_key_id = 'token'; SET s3_secret_access_key = '{token}'")

result = conn.execute(f"SELECT * FROM read_parquet('{data_url}') LIMIT 5").fetchall()


### Hardcoded Configuration (Not Recommended)

python
# For testing only - don't commit credentials!
config = {
    "url": "https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet",
    "token": None,  # Leave None for public repositories
}

```

**Improvements**:
- Real example values
- Environment variables pattern (best practice)
- Security note (don't hardcode credentials)
- Multiple approaches (env vars, hardcoded)
- Links to credential generation

**Effort**: 30 minutes
**Impact**: +1.5 points

## Pattern 7: Add Expected Output

### Before (7/10)

```markdown
python
result = conn.execute("SELECT COUNT(*) FROM table").fetchone()
print(result)

```

**Problems**:
- Unclear what output should be
- User can't verify correctness
- Silent failures undetected

### After (9/10)

```markdown
python
# Count total rows
result = conn.execute("""
    SELECT COUNT(*) as row_count
    FROM read_parquet('https://example.com/data.parquet')
""").fetchone()

print(f"Total rows: {result[0]:,}")


**Expected Output**:
Total rows: 1,234,567


**Troubleshooting**:
- If count is 0: Check URL is accessible (`curl -I URL`)
- If count differs: Parquet file may have been updated

```

**Improvements**:
- Expected output shown
- Formatted for readability (comma separators)
- Verification guidance
- Troubleshooting for mismatches

**Effort**: 10 minutes per example
**Impact**: +0.5 points

## Transformation Workflow

### Step 1: Assess Current State
Use quality-assessment-checklist.md to score each dimension.

### Step 2: Prioritize Improvements
Focus on dimensions scoring <7/10:
1. **Critical** (score <5): Quick Start, Prerequisites
2. **High** (score 5-6): Examples, Troubleshooting
3. **Medium** (score 7-8): Navigation, Polish

### Step 3: Apply Patterns
Select transformation patterns based on gaps:
- Missing Quick Start? → Pattern 1
- Unclear prerequisites? → Pattern 2
- Abstract examples? → Pattern 3
- No troubleshooting? → Pattern 4
- Poor navigation? → Pattern 5
- Placeholder content? → Pattern 6
- No expected output? → Pattern 7

### Step 4: Validate
After applying transformations:
1. Ask external developer to run Quick Start (<60 seconds?)
2. Re-score using quality-assessment-checklist.md
3. Target: 9/10 overall score

## Effort Estimates

| Pattern | Effort | Impact | ROI |
|---------|--------|--------|-----|
| Pattern 1: Quick Start | 30 min | +2 pts | **High** |
| Pattern 2: Prerequisites | 15 min | +1.5 pts | High |
| Pattern 3: Concrete Examples | 45 min | +2 pts | **High** |
| Pattern 4: Troubleshooting | 60 min | +2 pts | Medium |
| Pattern 5: Navigation/TOC | 20 min | +1 pt | Medium |
| Pattern 6: Remove Placeholders | 30 min | +1.5 pts | High |
| Pattern 7: Expected Output | 10 min | +0.5 pts | High |

**Typical transformation** (7/10 → 9/10):
- Apply Patterns 1, 2, 3, 4 = 2.5 hours
- Impact: +7.5 points (easily exceeds +2 needed)
- Select highest ROI patterns first

## Real-World Example: ADR-0014 Transformation

**Before**: README.md scored 7.5/10 (good but improvable)

**Applied Patterns**:
1. ✅ Pattern 1: Added Quick Start with DuckDB query (30 min)
2. ✅ Pattern 2: Documented prerequisites with versions (15 min)
3. ✅ Pattern 3: Replaced placeholder URLs with jsDelivr (45 min)
4. ✅ Pattern 4: Added 5 common troubleshooting errors (60 min)
5. ✅ Pattern 5: Added table of contents (20 min)

**Total Effort**: 2.5 hours
**Result**: 7.5/10 → 9.5/10 (+2 points)

**Key Success Factors**:
- Focused on highest ROI patterns first (1, 2, 3)
- Validated with external developer (confirmed <60s time-to-first-success)
- Used real URLs (jsDelivr CDN) instead of placeholders
- Documented actual errors from GitHub Issues
