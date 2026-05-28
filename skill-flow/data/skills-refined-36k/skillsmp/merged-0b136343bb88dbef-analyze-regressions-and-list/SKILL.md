---
name: analyze-regressions-and-list
description: Use this skill to fetch regression data and analyze component health for OpenShift releases based on triage metrics.
---

# Analyze Regressions and List

This skill combines functionality to fetch regression data for OpenShift components and analyze their health based on regression management metrics. It evaluates how well components are managing their test regressions by analyzing triage coverage, timeliness, and resolution speed.

## When to Use This Skill

Use this skill when you need to:

- Analyze component health for a specific OpenShift release
- Track regressions across releases
- Grade component health based on regression triage metrics
- Identify components needing assistance with regression handling
- Generate reports on component stability and quality scorecards

## Prerequisites

1. **Python 3 Installation**

   - Check if installed: `which python3`
   - Python 3.6 or later is required
   - Comes pre-installed on most systems

2. **Network Access**

   - The scripts require network access to reach the component health API and release dates API
   - Ensure you can make HTTPS requests

3. **API Endpoint Configuration**
   - The script includes a placeholder API endpoint that needs to be updated
   - Update the `base_url` in `list_regressions.py` with the actual component health API endpoint

## Implementation Steps

### Step 1: Verify Prerequisites

Ensure Python 3 is available:

```bash
python3 --version
```

If Python 3 is not installed, guide the user through installation for their platform.

### Step 2: Parse Arguments

Extract the release version and optional component filter from the command arguments:

- **Release format**: "X.Y" (e.g., "4.17", "4.21")
- **Components** (optional): List of component names to filter by

### Step 3: Fetch Release Dates

Run the `get_release_dates.py` script to determine the development window for the release:

```bash
python3 plugins/component-health/skills/get-release-dates/get_release_dates.py \
  --release <release_version>
```

### Step 4: Execute List Regressions Script

Run the `list_regressions.py` script with the appropriate arguments:

```bash
python3 plugins/component-health/skills/list-regressions/list_regressions.py \
  --release <release_version> \
  --start <development_start_date> \
  --end <ga_date> \
  --components <component_names> \
  --short
```

### Step 5: Parse Output Structure

The script outputs JSON to stdout with the following structure:

```json
{
  "summary": {
    "total": <number>,
    "triaged": <number>,
    "triage_percentage": <number>,
    "time_to_triage_hrs_avg": <number>,
    "time_to_triage_hrs_max": <number>,
    "time_to_close_hrs_avg": <number>,
    "time_to_close_hrs_max": <number>,
    "open": {
      "total": <number>,
      "triaged": <number>,
      "triage_percentage": <number>,
      "open_hrs_avg": <number>,
      "open_hrs_max": <number>
    },
    "closed": {
      "total": <number>,
      "triaged": <number>,
      "triage_percentage": <number>,
      "time_to_triage_hrs_avg": <number>,
      "time_to_triage_hrs_max": <number>,
      "time_to_close_hrs_avg": <number>,
      "time_to_close_hrs_max": <number>
    }
  },
  "components": {
    "ComponentName": {
      "summary": {
        "total": <number>,
        "triaged": <number>,
        "triage_percentage": <number>,
        "time_to_triage_hrs_avg": <number>,
        "time_to_triage_hrs_max": <number>,
        "time_to_close_hrs_avg": <number>,
        "time_to_close_hrs_max": <number>,
        "open": {
          "total": <number>,
          "triaged": <number>,
          "triage_percentage": <number>,
          "open_hrs_avg": <number>,
          "open_hrs_max": <number>
        },
        "closed": {
          "total": <number>,
          "triaged": <number>,
          "triage_percentage": <number>,
          "time_to_triage_hrs_avg": <number>,
          "time_to_triage_hrs_max": <number>,
          "time_to_close_hrs_avg": <number>,
          "time_to_close_hrs_max": <number>
        }
      }
    }
  }
}
```

### Step 6: Calculate Health Grades

Calculate grades based on three key metrics:

1. **Triage Coverage** (`summary.triage_percentage`)
2. **Triage Timeliness** (`summary.time_to_triage_hrs_avg`)
3. **Resolution Speed** (`summary.time_to_close_hrs_avg`)

### Step 7: Generate Reports

Generate text and optional HTML reports based on the regression data and health grades.

### Step 8: Error Handling

Handle common errors such as network issues, invalid release formats, and missing regressions.

## Output Format

The script outputs JSON with summaries and regressions grouped by component, and generates reports with overall health grades and component scorecards.

## Related Skills

- Component health analysis
- Release comparison
- Regression tracking
- Quality metrics reporting

## Notes

- The script uses Python's built-in `urllib` module (no external dependencies)
- Output is always JSON format for easy parsing
- Diagnostic messages are written to stderr, data to stdout
- The script has a 30-second timeout for HTTP requests