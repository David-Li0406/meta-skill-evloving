---
name: p6-project-controls
description: Specialized skill for Primavera P6 schedule management and automation in mining/engineering projects. Use this when working with P6 schedules, XER files, P6 APIs, schedule analysis, or building automation tools for project controls. Includes P6 data model knowledge, mining industry best practices, and code generation for schedule operations.
---

# P6 Project Controls Skill

This skill provides specialized knowledge and workflows for building automation tools that interface with Oracle Primavera P6 for mining and engineering project controls. It enables AI-assisted schedule management, analysis, and reporting.

## When to Use This Skill

Use this skill when:

- Working with Primavera P6 schedules, XER files, or P6 APIs
- Building automation tools for schedule management and analysis
- Analyzing schedule health, critical path, or performing quality checks
- Generating reports, dashboards, or KPIs from P6 data
- Implementing resource management or baseline comparison features
- Developing integrations with P6 EPPM Web Services API
- Applying mining industry scheduling best practices
- Troubleshooting P6 data model queries or field mappings

## P6 Integration Approaches

### 1. P6 EPPM Web Services API

The primary integration method for real-time P6 operations. Reference [references/p6-api-guide.md](references/p6-api-guide.md) for:

- Authentication and connection patterns
- Common API endpoints and operations
- Error handling and best practices
- Example request/response patterns

### 2. XER File Processing

For batch operations and offline analysis. Use [scripts/parse_xer.py](scripts/parse_xer.py) to:

- Parse XER file structure into structured data
- Extract activities, relationships, resources, and calendars
- Transform XER data for analysis or reporting
- Generate modified XER files for import

### 3. Database Direct Access

For advanced queries and reporting. Reference [references/p6-database-schema.md](references/p6-database-schema.md) for:

- Core table structures (PROJECT, TASK, TASKPRED, PROJWBS, etc.)
- Key relationships and joins
- Important field mappings
- Query patterns for common operations

## Core Workflows

### Schedule Analysis & Health Checks

To perform automated schedule quality validation:

1. Load schedule data (via API, XER, or database)
2. Apply validation rules from [references/schedule-quality-rules.md](references/schedule-quality-rules.md)
3. Check for:
   - Logic issues (missing predecessors/successors, out-of-sequence, constraints)
   - Critical path integrity
   - Resource over-allocation
   - Calendar assignments
   - Baseline deviations
4. Generate findings report with severity levels and recommendations
5. Use [scripts/schedule_validator.py](scripts/schedule_validator.py) for common validations

### Schedule Updates & Baseline Comparison

To automate schedule updates and variance analysis:

1. Retrieve current schedule and target baseline
2. Compare key metrics:
   - Start/finish date variances
   - Duration changes
   - Critical path changes
   - Float consumption
   - Milestone slippage
3. Use [scripts/baseline_compare.py](scripts/baseline_compare.py) for automated comparison
4. Generate variance reports highlighting areas of concern
5. Apply mining project thresholds from [references/mining-standards.md](references/mining-standards.md)

### Resource Management

To analyze and optimize resource allocation:

1. Extract resource assignments and availability
2. Identify over-allocations and capacity issues
3. Calculate resource loading curves
4. Use [scripts/resource_analyzer.py](scripts/resource_analyzer.py) for analysis
5. Generate resource histograms and leveling recommendations

### Reporting & Dashboards

To generate custom P6 reports:

1. Define required data points and KPIs
2. Query P6 data sources (prioritize API for real-time, database for complex)
3. Use report templates from [assets/report-templates/](assets/report-templates/)
4. Apply calculations and transformations
5. Export to desired format (Excel, PDF, JSON for dashboards)

## Mining Industry Best Practices

When working with mining project schedules, apply standards from [references/mining-standards.md](references/mining-standards.md):

- **Activity Duration Limits**: Mining projects typically limit activity durations (e.g., max 20 working days for construction activities)
- **Logic Density**: Maintain minimum 1.5 relationships per activity
- **Float Thresholds**: Activities with <10 days total float require attention
- **Critical Path**: Must represent true project completion path
- **Milestones**: Key project gates must have proper constraints
- **Resource Loading**: Follow BHP resource coding standards
- **Progress Updates**: Weekly for construction, monthly for early phases

## Code Generation Patterns

### P6 API Connection Template

```python
import requests
from requests.auth import HTTPBasicAuth

class P6Client:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()

    def get_projects(self):
        """Retrieve all projects"""
        response = self.session.get(
            f"{self.base_url}/api/project",
            auth=self.auth,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()
```

### XER File Parsing Pattern

Use [scripts/parse_xer.py](scripts/parse_xer.py) which provides:

```python
from scripts.parse_xer import XERParser

parser = XERParser('schedule.xer')
activities = parser.get_activities()
relationships = parser.get_relationships()
resources = parser.get_resources()
```

### Database Query Pattern

```python
import sqlite3  # or appropriate DB driver

def get_critical_activities(conn, project_id):
    """Query critical path activities"""
    query = """
    SELECT task_code, task_name, target_start_date, target_end_date
    FROM TASK
    WHERE proj_id = ? AND total_float_hr_cnt <= 0
    ORDER BY target_start_date
    """
    return conn.execute(query, (project_id,)).fetchall()
```

## Schedule Quality Rules

Implement automated checks following [references/schedule-quality-rules.md](references/schedule-quality-rules.md):

1. **Logic Checks**
   - No activities without predecessors (except project start)
   - No activities without successors (except project finish)
   - No date constraints on non-milestone activities
   - No out-of-sequence progress

2. **Duration Checks**
   - Activity durations within acceptable ranges
   - No excessively long activities (>20 days for detail work)
   - Zero-duration activities must be milestones

3. **Critical Path Checks**
   - Single continuous critical path exists
   - Critical path leads to project completion
   - No unexplained gaps in critical path

4. **Resource Checks**
   - All activities have resource assignments (if applicable)
   - No resource over-allocations beyond thresholds
   - Resource calendars properly assigned

5. **Progress Checks**
   - Actual dates align with percent complete
   - No future actuals
   - Remaining duration is reasonable

## Development Guidelines

### Data Extraction

- **Prefer API** for real-time operations and single-project operations
- **Use Database** for multi-project queries, complex analytics, reporting
- **Use XER** for batch operations, backups, external tool integration

### Error Handling

Always implement robust error handling:

- Validate P6 connection before operations
- Handle missing data gracefully
- Log errors with context (project ID, activity codes)
- Provide meaningful error messages to users

### Performance

- Cache frequently accessed data (project lists, calendars)
- Use pagination for large datasets
- Batch database queries when possible
- Process XER files in streaming mode for large schedules

### Testing

- Test with sample schedules from [assets/sample-schedules/](assets/sample-schedules/)
- Validate against known baselines
- Test edge cases (empty schedules, missing data)
- Verify calculations match P6 native calculations

## Common Use Cases

### Example 1: Schedule Health Check

```python
# User: "Analyze this XER file for schedule quality issues"

from scripts.parse_xer import XERParser
from scripts.schedule_validator import ScheduleValidator

# Parse XER file
parser = XERParser('project_schedule.xer')
activities = parser.get_activities()
relationships = parser.get_relationships()

# Run validation
validator = ScheduleValidator()
issues = validator.validate_schedule(activities, relationships)

# Generate report
validator.generate_report(issues, 'health_check_report.html')
```

### Example 2: Baseline Variance Report

```python
# User: "Compare current schedule against baseline and show variances"

from scripts.baseline_compare import BaselineComparator

comparator = BaselineComparator()
comparator.load_current_schedule('current.xer')
comparator.load_baseline('baseline.xer')

variances = comparator.analyze_variances()
critical_variances = comparator.filter_critical(variances)

comparator.export_report(critical_variances, 'variance_report.xlsx')
```

### Example 3: Critical Path Analysis

```python
# User: "Show me the critical path and activities with less than 5 days float"

from scripts.parse_xer import XERParser

parser = XERParser('schedule.xer')
activities = parser.get_activities()

# Filter critical and near-critical
critical = [a for a in activities if a.total_float <= 0]
near_critical = [a for a in activities if 0 < a.total_float <= 5]

# Generate visualization
parser.export_critical_path_diagram(critical, 'critical_path.png')
```

## Bundled Resources Reference

- **[scripts/parse_xer.py](scripts/parse_xer.py)**: XER file parser and data extractor
- **[scripts/schedule_validator.py](scripts/schedule_validator.py)**: Automated schedule quality validation
- **[scripts/baseline_compare.py](scripts/baseline_compare.py)**: Baseline comparison and variance analysis
- **[scripts/resource_analyzer.py](scripts/resource_analyzer.py)**: Resource loading and allocation analysis
- **[references/p6-database-schema.md](references/p6-database-schema.md)**: P6 database table structure and relationships
- **[references/p6-api-guide.md](references/p6-api-guide.md)**: P6 EPPM Web Services API documentation
- **[references/schedule-quality-rules.md](references/schedule-quality-rules.md)**: Industry-standard schedule validation rules
- **[references/mining-standards.md](references/mining-standards.md)**: Mining industry scheduling best practices and BHP standards
- **[assets/report-templates/](assets/report-templates/)**: Excel, HTML, and PDF report templates
- **[assets/sample-schedules/](assets/sample-schedules/)**: Sample XER files for testing

## Notes

- Always validate user permissions before modifying P6 data
- Follow BHP information security protocols when handling schedule data
- Document any custom validation rules or thresholds
- Keep API credentials secure and never commit to version control
- When generating code, include proper error handling and logging
- Test schedule modifications on copies before applying to production schedules
