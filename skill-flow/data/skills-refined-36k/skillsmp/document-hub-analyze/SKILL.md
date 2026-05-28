---
name: document-hub-analyze
description: Deep analysis of codebase vs documentation alignment. Detects drift, identifies undocumented code, extracts missing glossary terms, and provides actionable recommendations without making changes.
---

# Document Hub: Analyze

Analyze documentation quality and detect drift from actual codebase.

**Helper Scripts Available**:
- `scripts/detect_drift.py` - Comprehensive drift detection
- `scripts/extract_glossary.py` - Find undocumented domain terms
- `scripts/validate_hub.py` - Structure validation

**Use this skill to** diagnose documentation issues without making changes. This is a read-only analysis that reports problems and recommendations.

## What This Skill Does

Performs deep analysis to answer:
- What code exists but isn't documented?
- What documentation exists for removed code?
- What domain terms are missing from glossary?
- How healthy is the documentation overall?

## Decision Tree: When to Use This Skill

```
User wants to check documentation → Run analysis:
    1. Validate structure (errors block analysis)
    2. Detect module drift (src/ vs keyPairResponsibility.md)
    3. Detect technology drift (package.json vs techStack.md)
    4. Extract missing glossary terms
    5. Calculate overall health score
    6. Generate recommendations

→ Present findings without making changes
→ Suggest /document-hub update if drift detected
```

## Analysis Workflow

### Phase 1: Validation Check

Start with structure validation:

```bash
python scripts/validate_hub.py /path/to/project
```

If validation fails:
- Report structural errors
- Recommend fixing before analyzing content
- Exit early if hub doesn't exist

### Phase 2: Module Drift Analysis

Detect undocumented modules:

```bash
python scripts/detect_drift.py /path/to/project
```

This returns:
```json
{
  "drift_score": 0.23,
  "module_drift": {
    "undocumented": ["analytics", "webhooks"],
    "documented_but_missing": ["legacy"]
  }
}
```

**Interpret results:**
- `undocumented` → Code exists but not in docs
- `documented_but_missing` → Docs reference non-existent code

### Phase 3: Technology Drift Analysis

From the same `detect_drift.py` output:

```json
{
  "technology_drift": {
    "undocumented": ["Redis", "BullMQ"],
    "documented_but_missing": ["MongoDB"]
  }
}
```

**Interpret results:**
- Check `package.json`/`requirements.txt` for discrepancies
- Identify when tech was added (git log)
- Determine if tech is actually in use

### Phase 4: Glossary Gap Analysis

Find missing domain terms:

```bash
python scripts/extract_glossary.py /path/to/project
```

Returns ranked terms from codebase. Compare with current `glossary.md`:

1. Read existing glossary
2. Extract current terms
3. Identify terms in code but not in glossary
4. Rank by importance (score from script)
5. Recommend top 10-20 additions

### Phase 5: Health Scoring

Calculate overall documentation health:

**Scoring Formula:**
```
Health Score = 100 - (drift_score * 100)

Interpretation:
- 90-100: Excellent (drift < 0.10)
- 75-89:  Good (drift 0.10-0.25)
- 60-74:  Needs Attention (drift 0.25-0.40)
- < 60:   Poor (drift > 0.40)
```

### Phase 6: Generate Recommendations

Produce actionable recommendations prioritized by impact:

**HIGH PRIORITY:**
- Undocumented modules with many files
- Missing critical technologies (databases, frameworks)
- Broken cross-references

**MEDIUM PRIORITY:**
- Documented-but-missing code
- Complex diagrams needing split
- Missing glossary terms for core concepts

**LOW PRIORITY:**
- Minor tech stack updates
- Formatting inconsistencies
- Additional glossary terms

## Analysis Report Format

Present findings in a structured report:

```
Documentation Hub Analysis Report
==================================

Overall Health: 77/100 (Good)
Drift Score: 0.23

STRUCTURE VALIDATION
--------------------
✓ All required files present
✓ Mermaid syntax valid
⚠ 1 warning: systemArchitecture.md diagram complex (22 nodes)

MODULE DRIFT ANALYSIS
---------------------
Drift Score: 0.30 (Medium)

Undocumented Modules (2):
  • src/analytics - 8 files, appears to be user analytics tracking
  • src/webhooks - 4 files, webhook event handling

Documented but Missing (1):
  • src/legacy - Referenced in docs but directory doesn't exist
    Last seen: commit abc123 (3 months ago)

TECHNOLOGY DRIFT ANALYSIS
--------------------------
Drift Score: 0.15 (Low)

Missing from techStack.md (2):
  • Redis - Found in package.json, added 2 weeks ago
  • BullMQ - Found in package.json, used for job queues

Documented but Not Found (1):
  • MongoDB - Still in techStack.md but removed from dependencies

GLOSSARY GAPS
-------------
Found 18 potential domain-specific terms not in glossary:

High Relevance:
  1. BatchProcessor (score: 45) - "Processes items in configurable batch sizes"
  2. FulfillmentQueue (score: 42) - "Queue for order fulfillment jobs"
  3. CIPIntegration (score: 38) - "Customer Information Portal integration"

Medium Relevance:
  [Additional terms...]

RECOMMENDATIONS
---------------

HIGH PRIORITY (Do these first):
  1. Document analytics module in keyPairResponsibility.md
  2. Document webhooks module in keyPairResponsibility.md
  3. Add Redis to techStack.md
  4. Remove legacy module reference from docs

MEDIUM PRIORITY (Do when possible):
  5. Add BullMQ to techStack.md
  6. Add top 10 glossary terms
  7. Consider splitting systemArchitecture.md diagram

LOW PRIORITY (Nice to have):
  8. Add remaining glossary terms
  9. Update MongoDB reference or re-add dependency

NEXT STEPS
----------
Run /document-hub update to apply these recommendations automatically.
```

## Example: Complete Analysis

```python
import json
import subprocess
from pathlib import Path

project_path = Path("/path/to/project")

# 1. Validate
validate = subprocess.run(
    ["python", "scripts/validate_hub.py", str(project_path)],
    capture_output=True, text=True
)
validation = json.loads(validate.stdout)

# 2. Detect drift
drift = subprocess.run(
    ["python", "scripts/detect_drift.py", str(project_path)],
    capture_output=True, text=True
)
drift_data = json.loads(drift.stdout)

# 3. Extract glossary gaps
glossary = subprocess.run(
    ["python", "scripts/extract_glossary.py", str(project_path)],
    capture_output=True, text=True
)
glossary_data = json.loads(glossary.stdout)

# Read existing glossary
glossary_file = project_path / "cline-docs" / "glossary.md"
existing_terms = set()
if glossary_file.exists():
    with open(glossary_file) as f:
        # Extract terms from glossary
        # [Parsing logic...]
        pass

# Find gaps
missing_terms = [
    t for t in glossary_data["terms"]
    if t["term"] not in existing_terms
]

# 4. Calculate health score
health_score = 100 - (drift_data["drift_score"] * 100)

# 5. Generate report
print("Documentation Hub Analysis Report")
print("=" * 50)
print(f"Overall Health: {health_score:.0f}/100")
print(f"Drift Score: {drift_data['drift_score']:.2f}")
print()
print("UNDOCUMENTED MODULES:")
for module in drift_data["module_drift"]["undocumented"]:
    print(f"  • {module}")
print()
print("GLOSSARY GAPS:")
for term in missing_terms[:10]:
    print(f"  • {term['term']} (score: {term['score']})")
```

## Use Cases

### Pre-Update Health Check

Before running `/document-hub update`:
```
→ Run /document-hub analyze
→ Understand scope of needed changes
→ Prioritize what to update
```

### Periodic Documentation Audit

Monthly or quarterly:
```
→ Run /document-hub analyze
→ Track health score trend
→ Address high-priority items
```

### Onboarding Documentation Validation

When taking over a project:
```
→ Run /document-hub analyze
→ Understand documentation completeness
→ Identify knowledge gaps
```

## Best Practices

- **Run before updating** - Understand scope before making changes
- **Track drift score** - Monitor documentation health over time
- **Prioritize recommendations** - Don't try to fix everything at once
- **Use as diagnostic** - This is read-only analysis, not updates

## Common Pitfalls

❌ **Don't** make changes during analysis - this is read-only
❌ **Don't** ignore high-priority items - they indicate real gaps
❌ **Don't** run too frequently - analysis is for planning, not continuous monitoring

✅ **Do** use findings to guide updates
✅ **Do** prioritize high-impact recommendations
✅ **Do** track health score trends
✅ **Do** run before major updates

## Interpretation Guide

### Drift Scores

- **< 0.10** - Excellent: Minor gaps only
- **0.10-0.25** - Good: Some undocumented items, easy to fix
- **0.25-0.40** - Needs Attention: Significant gaps exist
- **> 0.40** - Poor: Major documentation debt

### When to Act

**Immediate action needed:**
- Drift score > 0.35
- Multiple undocumented core modules
- Broken cross-references

**Plan for next sprint:**
- Drift score 0.20-0.35
- Some missing technologies
- Glossary gaps

**Low priority:**
- Drift score < 0.20
- Minor formatting issues
- Optional glossary terms

## What Comes Next

After analysis:
1. **If high drift** → Run `/document-hub update` immediately
2. **If medium drift** → Schedule update for next sprint
3. **If low drift** → Continue monitoring, update as needed

## Helper Script Reference

**detect_drift.py** - Module and technology drift
```bash
python scripts/detect_drift.py /path/to/project
# Returns: drift scores + specific gaps
```

**extract_glossary.py** - Find missing terms
```bash
python scripts/extract_glossary.py /path/to/project
# Returns: ranked terms with contexts
```

**validate_hub.py** - Structure validation
```bash
python scripts/validate_hub.py /path/to/project
# Returns: structural issues
```

See `scripts/README.md` for complete documentation.
