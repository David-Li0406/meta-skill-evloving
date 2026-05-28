---
name: uspto-database
description: Use this skill when you need to access USPTO APIs for patent and trademark searches, examination history, assignments, citations, and office actions for IP analysis and prior art searches.
---

# USPTO Database

## Overview

The USPTO provides specialized APIs for accessing patent and trademark data. You can search patents by keywords, inventors, or assignees, retrieve examination history via PEDS, track assignments, analyze citations and office actions, and access TSDR for trademarks.

## When to Use This Skill

This skill should be used when:

- **Patent Search**: Finding patents by keywords, inventors, assignees, classifications, or dates.
- **Patent Details**: Retrieving full patent data including claims, abstracts, and citations.
- **Trademark Search**: Looking up trademarks by serial or registration number.
- **Trademark Status**: Checking trademark status, ownership, and prosecution history.
- **Examination History**: Accessing patent prosecution data from PEDS (Patent Examination Data System).
- **Office Actions**: Retrieving office action text, citations, and rejections.
- **Assignments**: Tracking patent/trademark ownership transfers.
- **Citations**: Analyzing patent citations (forward and backward).
- **Litigation**: Accessing patent litigation records.
- **Portfolio Analysis**: Analyzing patent/trademark portfolios for companies or inventors.

## USPTO API Ecosystem

The USPTO provides multiple specialized APIs for different data needs:

### Core APIs

1. **PatentSearch API** - Modern ElasticSearch-based patent search (replaced legacy PatentsView in May 2025).
   - Search patents by keywords, inventors, assignees, classifications, and dates.
   - Access to patent data through June 30, 2025.
   - 45 requests/minute rate limit.
   - **Base URL**: `https://search.patentsview.org/api/v1/`

2. **PEDS (Patent Examination Data System)** - Patent examination history.
   - Application status and transaction history from 1981-present.
   - Office action dates and examination events.
   - Use `uspto-opendata-python` Python library.
   - **Replaced**: PAIR Bulk Data (PBD) - decommissioned.

3. **TSDR (Trademark Status & Document Retrieval)** - Trademark data.
   - Trademark status, ownership, prosecution history.
   - Search by serial or registration number.
   - **Base URL**: `https://tsdrapi.uspto.gov/ts/cd/`

### Additional APIs

4. **Patent Assignment Search** - Ownership records and transfers.
5. **Trademark Assignment Search** - Trademark ownership changes.