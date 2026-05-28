# Database Schema

## Overview

Reports are stored in SQLite with versioning support. Finalized reports extract findings to queryable tables.

---

## Tables

### reports

Core report metadata with versioning.

```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    contract_id INTEGER NOT NULL,
    report_type TEXT NOT NULL CHECK (report_type IN ('risk_review', 'redline', 'comparison')),
    version INTEGER NOT NULL DEFAULT 1,
    parent_report_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalized_at TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'finalized')),
    report_data TEXT NOT NULL,  -- JSON blob with full report content
    docx_path TEXT,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (parent_report_id) REFERENCES reports(id)
);

CREATE INDEX idx_reports_contract ON reports(contract_id);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_status ON reports(status);
```

### report_findings

Queryable findings extracted on finalization.

```sql
CREATE TABLE report_findings (
    id INTEGER PRIMARY KEY,
    report_id INTEGER NOT NULL,
    clause_type TEXT NOT NULL,
    section_number TEXT,
    risk_level TEXT CHECK (risk_level IN ('CRITICAL', 'HIGH', 'MODERATE', 'LOW')),
    concern TEXT,
    recommendation TEXT,
    rationale TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

CREATE INDEX idx_findings_report ON report_findings(report_id);
CREATE INDEX idx_findings_clause ON report_findings(clause_type);
CREATE INDEX idx_findings_risk ON report_findings(risk_level);
```

### report_deltas

Version comparison deltas (Report 3 only).

```sql
CREATE TABLE report_deltas (
    id INTEGER PRIMARY KEY,
    report_id INTEGER NOT NULL,
    clause_type TEXT NOT NULL,
    section_number TEXT,
    v1_risk_level TEXT CHECK (v1_risk_level IN ('CRITICAL', 'HIGH', 'MODERATE', 'LOW')),
    v2_risk_level TEXT CHECK (v2_risk_level IN ('CRITICAL', 'HIGH', 'MODERATE', 'LOW')),
    delta TEXT CHECK (delta IN ('increased', 'decreased', 'unchanged')),
    v1_text TEXT,
    v2_text TEXT,
    business_impact TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

CREATE INDEX idx_deltas_report ON report_deltas(report_id);
CREATE INDEX idx_deltas_clause ON report_deltas(clause_type);
CREATE INDEX idx_deltas_delta ON report_deltas(delta);
```

---

## Versioning Logic

### Creating New Version

When editing a finalized report:

```sql
-- Get current version
SELECT MAX(version) as current_version 
FROM reports 
WHERE contract_id = ? AND report_type = ?;

-- Insert new version
INSERT INTO reports (
    contract_id, 
    report_type, 
    version, 
    parent_report_id, 
    status, 
    report_data
)
VALUES (
    ?,                      -- contract_id
    ?,                      -- report_type
    current_version + 1,    -- new version
    ?,                      -- parent_report_id (previous version's id)
    'draft',
    ?                       -- report_data JSON
);
```

### Version Chain Example

```
Contract: MSA v3
Report: Contract Risk Review

├── v1 (id=101, finalized 2025-01-15, parent=NULL)
├── v2 (id=145, finalized 2025-02-20, parent=101)
└── v3 (id=178, draft, parent=145)
```

---

## Common Queries

### Latest Version of Report

```sql
SELECT * FROM reports 
WHERE contract_id = ? 
  AND report_type = ?
ORDER BY version DESC 
LIMIT 1;
```

### Full Version History

```sql
SELECT 
    id, 
    version, 
    status, 
    created_at, 
    finalized_at 
FROM reports 
WHERE contract_id = ? 
  AND report_type = ?
ORDER BY version ASC;
```

### All CRITICAL Findings Across Contracts

```sql
SELECT 
    r.id as report_id,
    c.name as contract_name,
    rf.clause_type,
    rf.section_number,
    rf.concern,
    rf.recommendation
FROM report_findings rf
JOIN reports r ON rf.report_id = r.id
JOIN contracts c ON r.contract_id = c.id
WHERE rf.risk_level = 'CRITICAL'
  AND r.status = 'finalized'
ORDER BY c.name, rf.clause_type;
```

### Risk Trends for Counterparty

```sql
SELECT 
    rf.clause_type,
    rf.risk_level,
    COUNT(*) as count
FROM report_findings rf
JOIN reports r ON rf.report_id = r.id
JOIN contracts c ON r.contract_id = c.id
WHERE c.counterparty = '[COMPANY_B]'
  AND r.status = 'finalized'
GROUP BY rf.clause_type, rf.risk_level
ORDER BY rf.clause_type;
```

### Comparison: What Changed Between Versions

```sql
SELECT 
    clause_type,
    section_number,
    v1_risk_level,
    v2_risk_level,
    delta,
    business_impact
FROM report_deltas
WHERE report_id = ?
ORDER BY 
    CASE delta 
        WHEN 'increased' THEN 1 
        WHEN 'unchanged' THEN 2 
        WHEN 'decreased' THEN 3 
    END,
    clause_type;
```

---

## JSON Structure: report_data

### Risk Review

```json
{
    "title_page": {
        "contract_name": "Master Services Agreement",
        "our_entity": "[COMPANY_A]",
        "counterparty": "[COMPANY_B]",
        "position": "Systems Integrator",
        "date": "2025-11-29"
    },
    "executive_summary": {
        "overall_risk": "HIGH",
        "top_concerns": [
            {"clause_type": "Indemnification", "concern": "Unlimited scope"},
            {"clause_type": "Limitation of Liability", "concern": "Cap too low"}
        ],
        "distribution": {
            "CRITICAL": 2,
            "HIGH": 3,
            "MODERATE": 4,
            "LOW": 2
        }
    },
    "heat_map": [...],
    "clause_analysis": [...],
    "negotiation_playbook": {...}
}
```

### Redline

```json
{
    "title_page": {...},
    "executive_summary": {
        "revision_impact": {
            "before": {"CRITICAL": 3, "HIGH": 4, "MODERATE": 2, "LOW": 1},
            "after": {"CRITICAL": 1, "HIGH": 2, "MODERATE": 5, "LOW": 2}
        },
        "changes_proposed": {
            "total": 12,
            "dealbreaker": 4,
            "industry_standard": 5,
            "nice_to_have": 3
        },
        "key_revisions": [...]
    },
    "risk_matrix": [...],
    "redline_table": [...],
    "implementation_notes": {...},
    "negotiation_guide": {...}
}
```

### Comparison

```json
{
    "title_page": {
        "v1_label": "October Draft",
        "v2_label": "November Final",
        ...
    },
    "executive_summary": {
        "version_delta": {
            "v1": {"CRITICAL": 3, "HIGH": 4, "MODERATE": 2, "LOW": 1},
            "v2": {"CRITICAL": 1, "HIGH": 2, "MODERATE": 5, "LOW": 2}
        },
        "changes_detected": {
            "total": 11,
            "additions": 2,
            "modifications": 8,
            "deletions": 1
        },
        "key_themes": {...}
    },
    "risk_matrix": [...],
    "comparison_table": [...]
}
```

---

## Finalization Process

When user finalizes a report:

1. Update `reports.status` to 'finalized'
2. Set `reports.finalized_at` to current timestamp
3. Extract findings to `report_findings` table
4. For comparisons, extract deltas to `report_deltas` table
5. Generate .docx and save path to `reports.docx_path`

```python
def finalize_report(report_id):
    # 1. Update status
    db.execute("""
        UPDATE reports 
        SET status = 'finalized', finalized_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    """, [report_id])
    
    # 2. Get report data
    report = db.execute("SELECT * FROM reports WHERE id = ?", [report_id]).fetchone()
    data = json.loads(report['report_data'])
    
    # 3. Extract findings
    for finding in data.get('clause_analysis', []):
        db.execute("""
            INSERT INTO report_findings 
            (report_id, clause_type, section_number, risk_level, concern, recommendation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [report_id, finding['clause_type'], ...])
    
    # 4. Extract deltas (comparison only)
    if report['report_type'] == 'comparison':
        for delta in data.get('comparison_table', []):
            db.execute("""
                INSERT INTO report_deltas 
                (report_id, clause_type, section_number, v1_risk_level, v2_risk_level, delta, ...)
                VALUES (?, ?, ?, ?, ?, ?, ...)
            """, [...])
    
    # 5. Generate docx
    docx_path = generate_docx(report_id, data)
    db.execute("UPDATE reports SET docx_path = ? WHERE id = ?", [docx_path, report_id])
    
    db.commit()
```
