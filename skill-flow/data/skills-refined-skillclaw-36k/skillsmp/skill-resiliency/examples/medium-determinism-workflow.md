# Medium Determinism Example: Data Processing Workflow Skill

This example demonstrates moderate resiliency for a data processing workflow with medium determinism requirements.

## Determinism Assessment

**Scores:**
- Output Precision: 6 (structured format, some content variation acceptable)
- Process Rigidity: 5 (several valid processing approaches)
- Failure Consequence: 5 (data quality issues, but recoverable)
- Recovery Difficulty: 5 (can reprocess from source)

**Total: 21/40 - Medium-High Determinism → Moderate Resiliency**

## Skill Structure

```
data-processing-skill/
├── SKILL.md
├── scripts/
│   ├── validate-input.py
│   ├── validate-checkpoint.sh
│   └── generate-report.py
├── references/
│   ├── schemas.md
│   └── troubleshooting.md
└── examples/
    └── processing-workflow.md
```

## SKILL.md (Excerpt)

```markdown
---
name: data-processing-workflow
description: This skill should be used when the user asks to "process data files", "transform dataset", "batch process records", or discusses ETL workflows. Implements moderate resiliency with checkpoint validation and error recovery.
version: 1.5.0
---

# Data Processing Workflow

## Overview

This skill orchestrates data processing workflows with moderate resiliency: input validation, checkpoint-based progress tracking, error handling, and recovery procedures.

**Use for:** Batch data transformations, ETL pipelines, data quality processing

## Pre-Processing Validation

Before processing begins, validate input data:

```bash
python scripts/validate-input.py input-data/ --schema schemas/input-schema.json
```

**Validation Checks:**
- [ ] Input files present
- [ ] Files readable and not corrupted
- [ ] Data structure matches schema
- [ ] Required fields present
- [ ] Data types correct
- [ ] Value ranges acceptable

**If validation fails:**
- Review validation report: `validation-report.txt`
- Common fixes:
  - Missing fields: Check source data generation
  - Type errors: Verify upstream data formatting
  - Range violations: Check for data anomalies
- Re-validate after fixes

**Proceed only after validation passes.**

## Processing Workflow

### Phase 1: Data Extraction

Extract and normalize data from source files:

```python
#!/usr/bin/env python3
import json
import pandas as pd
from pathlib import Path

def extract_data(input_dir, output_file):
    """Extract data from input files."""
    all_data = []
    errors = []

    for input_file in Path(input_dir).glob('*.json'):
        try:
            with open(input_file) as f:
                data = json.load(f)
                all_data.extend(data['records'])
        except Exception as e:
            errors.append({
                'file': str(input_file),
                'error': str(e)
            })

    # Save extracted data
    df = pd.DataFrame(all_data)
    df.to_parquet(output_file)

    # Log errors
    if errors:
        with open('extraction-errors.json', 'w') as f:
            json.dump(errors, f, indent=2)
        print(f"⚠️  {len(errors)} files had extraction errors")

    return len(all_data), len(errors)

# Execute extraction
record_count, error_count = extract_data('input-data/', 'extracted.parquet')
print(f"Extracted {record_count} records with {error_count} errors")
```

**Checkpoint: Phase 1 Validation**

Before proceeding to Phase 2:

```bash
scripts/validate-checkpoint.sh phase1
```

**Validation checks:**
- [ ] Extracted data file exists (`extracted.parquet`)
- [ ] Record count >= expected minimum
- [ ] No critical extraction errors
- [ ] Data schema matches expected structure

**If validation fails:**
- Review extraction errors: `extraction-errors.json`
- Check troubleshooting guide: `references/troubleshooting.md` Section 1
- Fix source data issues
- Re-run Phase 1
- Re-validate

**Status Update:**
```markdown
## processing-status.md

---
phase: extraction-complete
records-extracted: 15234
errors: 3
validated: true
timestamp: 2026-01-07T15:45:00Z
---

Phase 1 (Extraction) complete.
Proceeding to Phase 2 (Transformation).
```

**Proceed to Phase 2 only after validation passes.**

### Phase 2: Data Transformation

Transform data according to business rules:

```python
#!/usr/bin/env python3
import pandas as pd

def transform_data(input_file, output_file):
    """Transform extracted data."""
    df = pd.read_parquet(input_file)

    # Transformation logic
    df['processed_date'] = pd.to_datetime('now')
    df['amount_usd'] = df['amount'] * df['exchange_rate']
    df['category'] = df['category'].str.lower().str.strip()

    # Data quality checks
    quality_issues = []

    # Check for negative amounts
    negative = df[df['amount_usd'] < 0]
    if len(negative) > 0:
        quality_issues.append({
            'issue': 'negative_amounts',
            'count': len(negative),
            'severity': 'high'
        })

    # Check for missing categories
    missing_cat = df[df['category'].isna()]
    if len(missing_cat) > 0:
        quality_issues.append({
            'issue': 'missing_categories',
            'count': len(missing_cat),
            'severity': 'medium'
        })

    # Save transformed data
    df.to_parquet(output_file)

    # Report quality issues
    if quality_issues:
        with open('quality-issues.json', 'w') as f:
            json.dump(quality_issues, f, indent=2)

        # Check if issues are blocking
        high_severity = [i for i in quality_issues if i['severity'] == 'high']
        if high_severity:
            print(f"❌ {len(high_severity)} high-severity quality issues found")
            print("   Review quality-issues.json before proceeding")
            return False
        else:
            print(f"⚠️  {len(quality_issues)} quality issues found (non-blocking)")

    return True

# Execute transformation
success = transform_data('extracted.parquet', 'transformed.parquet')
if not success:
    print("Transformation failed validation")
    exit(1)
```

**Checkpoint: Phase 2 Validation**

Before proceeding to Phase 3:

```bash
scripts/validate-checkpoint.sh phase2
```

**Validation checks:**
- [ ] Transformed data file exists (`transformed.parquet`)
- [ ] No high-severity quality issues
- [ ] All required fields present
- [ ] Value ranges acceptable
- [ ] No duplicate records

**If validation fails:**
- Review quality issues: `quality-issues.json`
- Determine if issues require source data fixes or transformation logic updates
- Medium-severity issues may be acceptable (document decision)
- High-severity issues must be resolved

**Recovery Options:**
1. Fix transformation logic and re-run Phase 2
2. Fix source data and restart from Phase 1
3. Document acceptable quality issues and proceed

**Update status:**
```markdown
## processing-status.md

---
phase: transformation-complete
records-transformed: 15231
quality-issues: 2 (medium severity)
validated: true
timestamp: 2026-01-07T16:15:00Z
---

Phase 2 (Transformation) complete.
Quality issues documented in quality-issues.json (acceptable).
Proceeding to Phase 3 (Export).
```

**Proceed to Phase 3 only after validation passes (or issues documented as acceptable).**

### Phase 3: Data Export

Export processed data to target format:

```python
#!/usr/bin/env python3
import pandas as pd
import json

def export_data(input_file, output_format='json'):
    """Export transformed data to target format."""
    df = pd.read_parquet(input_file)

    if output_format == 'json':
        # Export as JSON Lines
        output_file = 'output.jsonl'
        df.to_json(output_file, orient='records', lines=True)

    elif output_format == 'csv':
        # Export as CSV
        output_file = 'output.csv'
        df.to_csv(output_file, index=False)

    else:
        raise ValueError(f"Unsupported format: {output_format}")

    # Verify export
    if output_format == 'json':
        # Check each line is valid JSON
        with open(output_file) as f:
            for i, line in enumerate(f, 1):
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON on line {i}: {e}")
                    return False

    print(f"✅ Exported {len(df)} records to {output_file}")
    return True

# Execute export
success = export_data('transformed.parquet', output_format='json')
if not success:
    print("Export failed validation")
    exit(1)
```

**Final Validation**

After export completes:

```bash
python scripts/validate-output.py output.jsonl --schema schemas/output-schema.json
```

**Validation checks:**
- [ ] Output file exists
- [ ] File format valid
- [ ] Record count matches transformed data
- [ ] Schema compliance
- [ ] No data loss during export

**If validation fails:**
- Re-run export with different format options
- Check disk space
- Verify file permissions

**Update final status:**
```markdown
## processing-status.md

---
phase: complete
records-extracted: 15234
records-transformed: 15231
records-exported: 15231
quality-issues: 2 (medium severity - documented)
validated: true
timestamp: 2026-01-07T16:45:00Z
---

## Processing Summary

Successfully processed 15,231 records (3 extraction errors, 2 quality issues documented).

Output: output.jsonl
Format: JSON Lines
Validation: Passed

## Quality Issues (Acceptable)

1. Missing categories (12 records) - defaulted to 'uncategorized'
2. Future dates (5 records) - flagged for review

See quality-issues.json for details.
```

## Error Handling

### Handling Extraction Errors

If too many extraction errors occur:

```python
# In extraction phase
error_rate = error_count / (record_count + error_count)
if error_rate > 0.10:  # More than 10% errors
    print(f"❌ Error rate too high: {error_rate:.1%}")
    print("   Review source data quality")
    print("   Options:")
    print("   1. Fix source data and restart")
    print("   2. Adjust extraction logic")
    print("   3. Document acceptable error rate (requires approval)")
    exit(1)
```

### Handling Quality Issues

Quality issues are categorized:

**High Severity (Blocking):**
- Negative monetary amounts
- Invalid required fields
- Referential integrity violations
- Duplicate primary keys

**Medium Severity (Warning):**
- Missing optional fields
- Unusual value ranges
- Minor formatting inconsistencies

**Low Severity (Info):**
- Optimization opportunities
- Style inconsistencies

**Decision Process:**
1. High severity → Must fix before proceeding
2. Medium severity → Document and approve or fix
3. Low severity → Log for future improvement

### Recovery from Failed Checkpoint

If checkpoint validation fails:

```bash
# Reset to last successful checkpoint
scripts/reset-to-checkpoint.sh phase1

# This will:
# 1. Remove invalid output from failed phase
# 2. Reset status to last checkpoint
# 3. Prepare for re-execution

# Then fix issues and re-run failed phase
```

## Resuming Interrupted Processing

If processing is interrupted, resume from last checkpoint:

```bash
# Check current status
cat processing-status.md

# Resume from appropriate phase
case $PHASE in
    "extraction-complete")
        echo "Resuming from Phase 2 (Transformation)"
        python scripts/transform.py
        ;;
    "transformation-complete")
        echo "Resuming from Phase 3 (Export)"
        python scripts/export.py
        ;;
    *)
        echo "Starting from Phase 1 (Extraction)"
        python scripts/extract.py
        ;;
esac
```

## Success Criteria

Processing is complete when:

- [ ] All three phases completed
- [ ] All checkpoint validations passed
- [ ] Final output validation passed
- [ ] Quality issues documented (if any)
- [ ] Processing summary generated
- [ ] Output file delivered to target location

## Monitoring

**Progress tracking:**
```bash
# View current progress
cat processing-status.md

# View processing statistics
python scripts/generate-report.py
```

**Output:**
```
Data Processing Report
=====================

Phase 1: Extraction
  Status: Complete
  Records: 15,234
  Errors: 3 (0.02%)
  Duration: 5m 23s

Phase 2: Transformation
  Status: Complete
  Records: 15,231
  Quality Issues: 2 (medium)
  Duration: 10m 12s

Phase 3: Export
  Status: Complete
  Records: 15,231
  Format: JSON Lines
  Duration: 2m 08s

Total Duration: 17m 43s
Success Rate: 99.98%
```

## Additional Resources

- **`references/schemas.md`** - Input/output data schemas
- **`references/troubleshooting.md`** - Common issues and solutions
- **`scripts/validate-checkpoint.sh`** - Checkpoint validation script
```

## Key Resiliency Features

### 1. Checkpoint-Based Validation

Processing is divided into phases with explicit validation between them. If a phase fails, only that phase needs to be re-executed, not the entire workflow.

### 2. Quality Issue Categorization

Not all issues are blocking. Medium/low severity issues can be documented and accepted, allowing processing to continue while maintaining awareness of quality concerns.

### 3. Progress Tracking

The `processing-status.md` file maintains current state, enabling:
- Resume from interruption
- Progress monitoring
- Audit trail
- Recovery point identification

### 4. Error Rate Monitoring

Instead of failing on first error, the system monitors error rates and fails only if errors exceed acceptable thresholds.

### 5. Flexible Recovery

Multiple recovery options:
- Re-run single phase
- Reset to checkpoint
- Fix and continue
- Document and proceed (for acceptable issues)

## Why This Level of Resiliency?

**Determinism Score: 21/40 (Medium-High)**

- **Output Precision (6):** Structured format required, some content variation acceptable
- **Process Rigidity (5):** Several valid processing approaches, flexible within constraints
- **Failure Consequence (5):** Data quality issues impact downstream, but recoverable
- **Recovery Difficulty (5):** Can reprocess from source, moderate effort

**Therefore:** Moderate resiliency is appropriate:
- More than just "try again" (has checkpoints, validation)
- Less than production deployment (no automatic rollback, simpler monitoring)
- Recovery is supported but not fully automated
- Quality issues can be assessed and accepted (not always blocking)

## Resiliency Balance

**Not Too Much:**
- No automatic rollback (unnecessary for batch processing)
- No real-time monitoring (batch processing can be reviewed after)
- No comprehensive test suites (input variation is expected)

**Not Too Little:**
- Input validation prevents garbage-in-garbage-out
- Checkpoints enable efficient recovery
- Quality monitoring catches issues early
- Status tracking enables resume capability

**Just Right:** Resiliency matches the actual risk and recovery needs of batch data processing.

---

**Key Takeaway:** Medium determinism → moderate resiliency. Balance between safety and agility.
