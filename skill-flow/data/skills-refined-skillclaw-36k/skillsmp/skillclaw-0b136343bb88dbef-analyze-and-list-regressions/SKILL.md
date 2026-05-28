---
name: analyze-and-list-regressions
description: Use this skill to fetch and analyze component health regressions for OpenShift releases, helping to grade and track regression management metrics.
---

# Skill body

## When to Use This Skill

Use this skill when you need to:

- Analyze component health for a specific OpenShift release
- Track regressions and grade component health based on regression management metrics
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
   - Update the `base_url` in the relevant scripts with the actual component health API endpoint.

## Implementation Steps

### Step 1: Verify Prerequisites

First, ensure Python 3 is available:

```bash
python3 --version
```

If Python 3 is not installed, guide the user through installation for their platform.

### Step 2: Locate the Scripts

The scripts are located at:

```
plugins/component-health/skills/list-regressions/list_regressions.py
plugins/component-health/skills/get-release-dates/get_release_dates.py
```

### Step 3: Fetch Release Dates

Run the `get_release_dates.py` script to determine the development window for the release:

```bash
python3 plugins/component-health/skills/get-release-dates/get_release_dates.py \
  --release <release_version>
```

### Step 4: Run the List Regressions Script

Execute the `list_regressions.py` script with appropriate arguments:

```bash
# Basic usage - all regressions for a release
python3 plugins/component-health/skills/list-regressions/list_regressions.py \
  --release <release_version>

# Filter by specific components
python3 plugins/component-health/skills/list-regressions/list_regressions.py \
  --release <release_version> \
  --components <component_name>
```

### Step 5: Analyze Regressions

After fetching regression data, analyze and grade component health based on regression management metrics:

```bash
python3 plugins/component-health/skills/analyze-regressions/analyze_regressions.py \
  --release <release_version> \
  --components <component_name>
```

### Step 6: Process the Output

The scripts output JSON data with regression details and health metrics. Use this data to generate reports or scorecards as needed.