---
name: fda-database
description: Use this skill when you need to query the openFDA API for comprehensive FDA regulatory data related to drugs, devices, adverse events, recalls, and more for safety research and regulatory analysis.
---

# FDA Database Access

## Overview

Access comprehensive FDA regulatory data through openFDA, the FDA's initiative to provide open APIs for public datasets. Query information about drugs, medical devices, foods, animal/veterinary products, and substances using Python with standardized interfaces.

**Key capabilities:**
- Query adverse events for drugs, devices, foods, and veterinary products
- Access product labeling, approvals, and regulatory submissions
- Monitor recalls and enforcement actions
- Look up National Drug Codes (NDC) and substance identifiers (UNII)
- Analyze device classifications and clearances (510k, PMA)
- Track drug shortages and supply issues
- Research chemical structures and substance relationships

## When to Use This Skill

This skill should be used when working with:
- **Drug research**: Safety profiles, adverse events, labeling, approvals, shortages
- **Medical device surveillance**: Adverse events, recalls, 510(k) clearances, PMA approvals
- **Food safety**: Recalls, allergen tracking, adverse events, dietary supplements
- **Veterinary medicine**: Animal drug adverse events by species and breed
- **Chemical/substance data**: UNII lookup, CAS number mapping, molecular structures
- **Regulatory analysis**: Approval pathways, enforcement actions, compliance tracking
- **Pharmacovigilance**: Post-market surveillance, safety signal detection
- **Scientific research**: Drug interactions, comparative safety, epidemiological studies

## Quick Start

### 1. Basic Setup

```python
from scripts.fda_query import FDAQuery

# Initialize (API key optional but recommended)
fda = FDAQuery(api_key="YOUR_API_KEY")

# Query drug adverse events
events = fda.query_drug_events("aspirin", limit=100)

# Get drug labeling
label = fda.query_drug_label("Lipitor", brand=True)

# Search device recalls
recalls = fda.query("device", "enforcement",
                   search="classification:Class+I",
                   limit=50)
```

### 2. API Key Setup

While the API works without a key, registering provides higher rate limits:
- **Without key**: 240 requests/min, 1,000/day
- **With key**: 240 requests/min, 120,000/day

Register at: https://open.fda.gov/apis/authentication/

Set as environment variable:
```bash
export FDA_API_KEY="your_api_key"
```