---
name: generate-report-header
description: Create standardized report headers with metadata for all agent-generated reports. Use when generating bug reports, security audits, dependency reports, or any worker output requiring consistent formatting.
---

# Generate Report Header

Create consistent headers for agent-generated reports.

## Instructions

### Step 1: Collect Input

- `reportType`: String (e.g., "Bug Hunting", "Security Audit")
- `version`: String (e.g., "0.8.0", "2025-10-17")
- `status`: success|partial|failed|in_progress
- `timestamp`: String (optional, ISO-8601)
- `additionalMetadata`: Object (optional)

### Step 2: Status Emoji Mapping

- `success`: checkmark
- `partial`: warning
- `failed`: x
- `in_progress`: refresh

### Step 3: Generate Header

```markdown
# {ReportType} Report: {Version}

**Generated**: {Timestamp}
**Status**: {StatusEmoji} {Status}
**Version**: {Version}
{Additional metadata fields}

---

## Executive Summary
```

## Error Handling

- Missing Report Type: Return error
- Invalid Status: Return error with valid values
- Invalid Timestamp: Use current time
