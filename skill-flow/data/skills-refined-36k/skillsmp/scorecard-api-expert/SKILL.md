---
name: scorecard-api-expert
description: Constructs precise URL queries for the US Department of Education College Scorecard API. Use this skill when fetching, cleaning, or explaining institutional data.
---

# College Scorecard API Expert

You are an expert in the College Scorecard API architecture.

## API Configuration

- **Base URL**: `https://api.data.gov/ed/collegescorecard/v1/schools`
- **API Key**: Use environment variable `SCORECARD_API_KEY`

## Query Rules

1. **Always** use `latest` prefix for current data (e.g., `latest.student.size`)
2. **Always** append `keys_nested=true` for structured JSON responses
3. **Always** handle pagination via `page` parameter when total > 100

## Field Mappings

| Business Concept       | API Field                                              | Notes                                                    |
| ---------------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| Earnings (ROI)         | `latest.earnings.4_yrs_after_completion.median`        | **Gold standard**. Avoid deprecated `10_yrs_after_entry` |
| Debt                   | `latest.aid.median_debt.completers.overall`            | Graduates only                                           |
| Net Price (Low Income) | `latest.cost.net_price.public.by_income_level.0-30000` | True affordability metric                                |
| Retention              | `latest.student.retention_rate.four_year.full_time`    | Primary target variable                                  |
| Pell Rate              | `latest.student.share_lowincome.0_30000`               | Socioeconomic proxy                                      |
| Admission Rate         | `latest.admissions.admission_rate.overall`             | Market demand signal                                     |
| Completion Rate        | `latest.completion.completion_rate_4yr_150nt`          | 150% time standard                                       |
| Location               | `location.lat`, `location.lon`                         | For geospatial analysis                                  |
| Carnegie               | `school.carnegie_basic`                                | For peer imputation                                      |

## Data Cleaning

1. Replace `PrivacySuppressed` → `NaN`
2. Replace `NULL` → `NaN`
3. Impute missing values using **median of same Carnegie classification** (not global mean)

## Example Query

```python
import requests

params = {
    'api_key': API_KEY,
    'fields': 'school.name,latest.student.retention_rate.four_year.full_time',
    'keys_nested': 'true',
    'per_page': 100
}
response = requests.get(BASE_URL, params=params)
```
