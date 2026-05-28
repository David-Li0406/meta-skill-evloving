---
name: clinicaltrials-database
description: Use this skill when you need to query ClinicalTrials.gov for clinical trial data, enabling patient matching, research analysis, and data export.
---

# ClinicalTrials.gov Database

## Overview

ClinicalTrials.gov is a comprehensive registry of clinical studies conducted worldwide, maintained by the U.S. National Library of Medicine. Access API v2 to search for trials, retrieve detailed study information, filter by various criteria, and export data for analysis. The API is public (no authentication required) with rate limits of ~50 requests per minute, supporting JSON and CSV formats.

## When to Use This Skill

This skill should be used when working with clinical trial data in scenarios such as:

- **Patient matching** - Finding recruiting trials for specific conditions or patient populations.
- **Research analysis** - Analyzing clinical trial trends, outcomes, or study designs.
- **Drug/intervention research** - Identifying trials testing specific drugs or interventions.
- **Geographic searches** - Locating trials in specific locations or regions.
- **Sponsor/organization tracking** - Finding trials conducted by specific institutions.
- **Data export** - Extracting clinical trial data for further analysis or reporting.
- **Trial monitoring** - Tracking status updates or results for specific trials.
- **Eligibility screening** - Reviewing inclusion/exclusion criteria for trials.

## Quick Start

### Basic Search Query

Search for clinical trials using the helper script:

```bash
cd scientific-databases/clinicaltrials-database/scripts
python3 query_clinicaltrials.py
```

Or use Python directly with the `requests` library:

```python
import requests

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} trials")
```

### Retrieve Specific Trial

Get detailed information about a trial using its NCT ID:

```python
import requests

nct_id = "NCT04852770"
url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"

response = requests.get(url)
study = response.json()

# Access specific modules
title = study['protocolSection']['identificationModule']['briefTitle']
status = study['protocolSection']['statusModule']['overallStatus']
```