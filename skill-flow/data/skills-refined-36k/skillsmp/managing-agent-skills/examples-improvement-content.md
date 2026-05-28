# Skill Improvement Examples: Content Quality

Before/After transformations for improving content conciseness, validation, and workflow clarity.

## Transformation 1: Bloated to Concise

### ❌ Before (Unnecessarily Verbose)
```markdown
# Processing Financial Data

## Introduction to Financial Statements
Financial statements are documents that show the financial activities
of a business. There are three main types:

1. Income Statement: Shows revenue and expenses
   - Revenue is money earned
   - Expenses are costs incurred
   - Net income is revenue minus expenses

2. Balance Sheet: Shows assets, liabilities, and equity
   - Assets are what the company owns
   - Liabilities are what the company owes
   - Equity is the residual ownership

[300 more lines of basic accounting concepts...]

## How to Calculate Ratios in Python
Python is a programming language. Here's how to use it:

```python
# Import the json module to work with JSON
import json

# Open a file
with open('file.txt', 'r') as f:
    data = f.read()
```

[200 more lines of basic Python...]
```

**Problems:**
- Teaches basic concepts Claude already knows
- Wastes context on general knowledge
- No company-specific or unique information

---

### ✅ After (Concise and Focused)
```markdown
# Analyzing Financial Statements

## Company-Specific Data Requirements

### Input Format
Financial data must be in our proprietary JSON schema:

```json
{
  "fiscal_period": "Q4-2024",
  "revenue_sources": {
    "product_alpha": 1500000,
    "product_beta": 2300000,
    "legacy_systems": 450000
  },
  "adjusted_ebitda": "use this for calculations, not reported EBITDA"
}
```

### Custom Metrics
Calculate these company-specific metrics:
- **Adjusted Customer LTV**: Revenue per customer / churn_rate * 0.85 (85% retention assumption)
- **Platform Efficiency Ratio**: (GMV - direct_costs) / headcount
- **Legacy Revenue %**: Must stay below 15% per board policy

### Workflow
1. Validate input matches company schema
2. Run calculate_ratios.py with company-specific formulas
3. Compare to internal benchmarks (see benchmarks.csv)
4. Flag if legacy_revenue_pct > 15%
```

**Improvements:**
- ✅ Only company-specific information
- ✅ Proprietary schemas and metrics
- ✅ Internal policies Claude wouldn't know
- ✅ Under 100 lines vs 500+

---

## Transformation 2: Adding Validation Steps

### ❌ Before
```markdown
## Workflow
1. Load data
2. Run calculations
3. Generate output
```

**Problems:**
- No validation
- No error handling
- No success criteria

---

### ✅ After
```markdown
## Workflow

### Step 1: Load and Validate Data
**Actions:**
- [ ] Load data from provided source
- [ ] Check required fields present: company_name, fiscal_year, revenue, expenses
- [ ] Verify numeric fields contain valid numbers (not None/NaN)
- [ ] Ensure dates in ISO format (YYYY-MM-DD)

**Validation:**
- All required fields present and properly typed
- No missing or malformed data

### Step 2: Calculate Ratios
**Actions:**
- [ ] Run calculate_ratios.py with validated data
- [ ] Check script exit code is 0 (success)
- [ ] Verify output contains all 15 expected ratios

**Validation:**
- Script completes without errors
- All ratios calculated (no None/NaN values)
- Results within reasonable ranges

**If validation fails:**
1. Review error messages from script
2. Check input data quality
3. Fix issues and retry

### Step 3: Generate and Verify Output
**Actions:**
- [ ] Format results using report-template.md
- [ ] Include industry benchmarks from benchmarks.csv
- [ ] Export to Excel with formatting

**Validation:**
- [ ] Excel file created: {company}_{year}_financial_analysis.xlsx
- [ ] All sections present: summary, ratios, benchmarks, charts
- [ ] File opens without errors
```

**Improvements:**
- ✅ Validation checkpoints at each step
- ✅ Clear success criteria
- ✅ Error handling guidance
- ✅ Specific verification items

---

## Transformation 3: Fixing Time-Sensitive Content

### ❌ Before
```markdown
## API Version Selection

If today's date is before 2024-06-01:
  Use v1 API: https://api.example.com/v1/
  Auth: API Key only

If today's date is after 2024-06-01:
  Use v2 API: https://api.example.com/v2/
  Auth: OAuth2 required
```

**Problems:**
- Date-based conditional will become outdated
- Confusing when read after transition date
- Requires maintenance to update

---

### ✅ After
```markdown
## API Version Selection

### Current Approach
Use v2 API for all requests:
- **Base URL**: https://api.example.com/v2/
- **Authentication**: OAuth2 (see authentication.md)
- **Features**: All current functionality

### Old Patterns
Previous implementations used v1 API:
- v1 used API Key authentication
- v1 had limited rate limits
- Migration to v2 completed company-wide
- v1 endpoint is deprecated and may be shut down

**Note**: If you encounter old code referencing /v1/, update it to /v2/
```

**Improvements:**
- ✅ No date conditionals
- ✅ Clear current vs old distinction
- ✅ Doesn't require date-based maintenance
- ✅ Provides migration guidance

---

## Transformation 4: Fixing Workflow Vagueness

### ❌ Before
```markdown
## Workflow
1. Get the user's requirements
2. Process the data appropriately
3. Make sure everything is correct
4. Deliver the results
```

**Problems:**
- Extremely vague
- No actionable steps
- No guidance on "how"

---

### ✅ After
```markdown
## Workflow

### Step 1: Gather Requirements
**Actions:**
- [ ] Identify required financial metrics (ROE, ROA, profit margin, etc.)
- [ ] Determine time period for analysis
- [ ] Confirm data source (user-provided vs database)
- [ ] Note any specific comparison needs (industry, historical, peer companies)

**Validation:**
- Requirements documented and confirmed with user

### Step 2: Validate Input Data
**Actions:**
- [ ] Load financial statement data
- [ ] Verify required fields present: revenue, expenses, assets, liabilities, equity
- [ ] Check numeric fields for validity (no None/NaN/Inf)
- [ ] Ensure dates in ISO format (YYYY-MM-DD)
- [ ] Validate data completeness (no missing periods)

**Validation:**
- All required data present and properly formatted
- Data passes quality checks

### Step 3: Calculate Financial Ratios
**Actions:**
- [ ] Run calculate_ratios.py with validated data
- [ ] Check script exit code (0 = success)
- [ ] Verify all requested ratios calculated
- [ ] Check for calculation errors or anomalies

**Validation:**
- All ratios calculated successfully
- Results within expected ranges (e.g., profit margin between -100% and 100%)
- No division-by-zero or other calculation errors

### Step 4: Generate Analysis Report
**Actions:**
- [ ] Format results using company report template
- [ ] Add industry benchmark comparisons (from benchmarks.csv)
- [ ] Generate visualization charts
- [ ] Include executive summary with key findings
- [ ] Export to Excel with proper formatting

**Validation:**
- [ ] Report includes all requested metrics
- [ ] Benchmarks loaded and displayed correctly
- [ ] Charts render properly
- [ ] File naming: {company}_{fiscal_year}_financial_analysis.xlsx
- [ ] File opens without errors
```

**Improvements:**
- ✅ Specific, actionable steps
- ✅ Clear validation criteria
- ✅ Tools and files specified
- ✅ Success criteria defined

---

## Transformation 5: Adding Company-Specific Knowledge

### ❌ Before
```markdown
# API Integration

## Making API Calls

Use the requests library to make HTTP calls:

```python
import requests
response = requests.get(url, headers=headers)
data = response.json()
```

Handle errors appropriately.
```

**Problems:**
- Generic knowledge Claude already has
- No company-specific information
- Wastes context space

---

### ✅ After
```markdown
# Internal API Integration

## Company API Authentication

All internal API calls require:
1. **Service Account Token** from `get_service_token()` (internal auth lib)
2. **Request ID** in header: `X-Acme-Request-ID` (format: ACME-YYYY-UUID)
3. **Environment indicator**: `X-Acme-Env` (prod/staging/dev)

```python
from acme_auth import get_service_token
import uuid

headers = {
    'Authorization': f'Bearer {get_service_token()}',
    'X-Acme-Request-ID': f'ACME-{datetime.now().year}-{uuid.uuid4()}',
    'X-Acme-Env': 'prod'
}
```

## Rate Limiting
- **Tier 1 services**: 1000 req/min (billing, payments)
- **Tier 2 services**: 5000 req/min (analytics, reporting)
- Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Critical**: If rate limited, exponential backoff: 2^n seconds (max 60s)

## Error Codes
- **E1001**: Invalid service token (rotate token using `refresh_token()`)
- **E2005**: Request ID format invalid (ensure ACME-YYYY-UUID format)
- **E3010**: Environment mismatch (check X-Acme-Env matches deployment)
```

**Improvements:**
- ✅ Company-specific authentication system
- ✅ Internal tools and libraries
- ✅ Proprietary error codes
- ✅ Internal policies and thresholds
- ✅ Information Claude doesn't have

---

## Key Patterns: Content Quality Improvements

### Fix Verbosity → Remove Redundancy
**Remove:**
- General knowledge Claude already knows
- Basic programming language syntax
- Standard library documentation
- Common development practices

**Keep:**
- Company-specific schemas and formats
- Internal tools and libraries
- Proprietary metrics and calculations
- Internal policies and thresholds
- Custom error codes and handling

### Fix Validation → Add Checkpoints
**Add at each workflow step:**
- Specific validation criteria
- Expected success conditions
- Clear error handling paths
- Verification checklists

### Fix Vagueness → Add Specificity
**Replace vague terms:**
- "Process the data" → "Run calculate_ratios.py with validated input"
- "Check results" → "Verify all 15 ratios calculated, no None/NaN values"
- "Handle errors" → "If E1001 error, rotate token using refresh_token()"
- "Format output" → "Export to Excel using report-template.md formatting"
