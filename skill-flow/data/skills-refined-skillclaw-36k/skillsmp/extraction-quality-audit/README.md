# Extraction Quality Audit Skill

Version 1.0 - Created 2026-01-21

**Project-level skill** for the medical-exams-parser repository.

## Quick Start

This skill provides comprehensive quality assessment for document extraction pipelines through stratified sampling, systematic verification, pattern analysis, and detailed reporting.

### Usage

Invoke this skill when:
- After implementing or modifying extraction pipeline
- Before production deployment
- Periodic quality audits (quarterly/annual)
- Investigating suspected quality issues
- Validating prompt or model changes
- Benchmarking extraction accuracy

### Files Created

```
extraction-quality-audit/
├── SKILL.md                          # Main skill documentation (~400 lines)
├── README.md                         # This file
├── scripts/
│   ├── generate_inventory.py        # Phase 1: Generate document catalog
│   ├── stratified_sampling.py       # Phase 2: Select representative sample
│   ├── verification_framework.py    # Phase 3: Guide systematic verification
│   └── report_generator.py          # Phase 5: Generate markdown report
├── references/
│   ├── sampling_methodology.md      # Stratified sampling theory & best practices
│   ├── verification_checklist.md    # Detailed verification steps & scoring
│   ├── medical_terminology_guide.md # Domain-specific verification (medical)
│   └── report_template.md          # Report structure & sections
└── assets/
    └── (none)
```

### Workflow

**Phase 1: Inventory Generation**
```bash
python scripts/generate_inventory.py \
  --output-dir /path/to/extraction/outputs \
  --profile-name your_profile \
  --output inventory.json
```

**Phase 2: Stratified Sampling**
```bash
python scripts/stratified_sampling.py \
  --inventory inventory.json \
  --target-size 30 \
  --output sample.json
```

**Phase 3: Systematic Verification**
```bash
python scripts/verification_framework.py \
  --sample sample.json \
  --results verification_results.json
```
Then use Claude vision to verify each document interactively.

**Phase 4: Pattern Analysis**
Interactive analysis with Claude to identify systematic issues.

**Phase 5: Report Generation**
```bash
python scripts/report_generator.py \
  --inventory inventory.json \
  --sample sample.json \
  --results verification_results.json \
  --output QUALITY_REPORT.md
```

## Key Features

- **Generic Design:** Works with any extraction pipeline (not just medical)
- **Configurable Sampling:** Customize priority tags and coverage rates
- **Domain Agnostic:** Create custom terminology guides for any domain
- **Comprehensive Reporting:** Detailed markdown reports with statistics
- **Incremental Progress:** Save verification results as you go
- **Statistical Rigor:** Stratified sampling with confidence calculations

## Customization

### For Non-Medical Domains

1. **Create domain-specific terminology guide:**
   - Copy `references/medical_terminology_guide.md`
   - Adapt for your domain (legal, financial, scientific, technical)

2. **Define custom priority tags:**
   - Edit `scripts/generate_inventory.py`
   - Add domain-specific tag definitions

3. **Adjust sampling configuration:**
   - Create `sampling_config.json`
   - Specify tag coverage rates

### Example: Legal Documents

```python
# Custom tags for legal documents
PRIORITY_TAGS = {
    'LOW_CONF': lambda doc: doc.get('min_confidence', 1) < 0.7,
    'COMPLEX': lambda doc: doc['page_count'] >= 50,
    'MULTI_PARTY': lambda doc: doc.get('party_count', 0) > 2,
    'OLD_DOC': lambda doc: doc.get('year', 9999) < 1950,
    'HIGH_VALUE': lambda doc: doc.get('contract_value', 0) > 1000000,
}
```

## Documentation

- **Main documentation:** `SKILL.md`
- **Sampling methodology:** `references/sampling_methodology.md`
- **Verification checklist:** `references/verification_checklist.md`
- **Report template:** `references/report_template.md`

## Example Use Case

**Medical Exams Parser Quality Investigation:**
- Corpus: 199 medical documents (1991-2025)
- Sample: 44 documents (22% coverage)
- Verified: 4 documents (representative examples)
- Result: Grade A (Excellent) - 9.8/10 average quality
- Time: ~4 hours total for complete investigation

See `QUALITY_INVESTIGATION_REPORT.md` in medical-exams-parser repo for full example.

## Requirements

- Python 3.7+
- Libraries: `pyyaml`, `json`, `pathlib`
- Claude with vision access (for verification phase)
- Source documents and extraction outputs

## Success Criteria

The skill is successful if:
- ✅ Can be invoked for any extraction pipeline
- ✅ Produces comprehensive quality report
- ✅ Identifies systematic issues (if any)
- ✅ Provides actionable recommendations
- ✅ Completes verification in reasonable time (2-4 hours for 25-30 docs)

## Support

For issues or questions:
- Read `SKILL.md` for detailed instructions
- Check `references/` for methodology details
- Review example files in medical-exams-parser repo

## Version History

- **v1.0** (2026-01-21): Initial release
  - Full 5-phase quality audit workflow
  - Stratified sampling implementation
  - Domain-agnostic design with medical example
  - Comprehensive report generation
