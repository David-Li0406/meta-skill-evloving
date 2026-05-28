---
name: check-health
description: Run comprehensive data health checks on the database, reporting on data quality issues, dead letters, duplicates, and anomalies. Use when you need to assess overall data quality, identify issues requiring attention, or perform daily data quality monitoring.
---

# Check Health

**Purpose:** Quickly assess overall data quality and identify issues requiring attention.

## Instructions for Claude

When this skill is invoked:

1. **Create and run a Node.js script** that connects to MongoDB and performs these checks:

   **Basic Stats:**
   - Total people count
   - Total visits count
   - Total scans count
   - Total dead letters count
   - Recent observations (last 24h, last 7d)

   **Identity Issues:**
   - People without canonical_id
   - People with missing Sales Nav ID
   - People with unstable IDs (URL-based _id)
   - Duplicate aliases (same alias.value on multiple people)

   **Data Quality:**
   - People without observations
   - People with missing critical fields (fullName, currentTitle, etc.)
   - Orphaned observations (not linked to any person)
   - Observations with missing stable identifiers

   **Dead Letters:**
   - Count by status (pending, replayed, failed_again)
   - Most common error types
   - Oldest pending dead letter
   - Recent failure rate

   **Role & Company Issues:**
   - People with overlapping role timelines
   - Companies missing canonical IDs
   - Locations missing structured data

2. **Output format:**
   ```
   DATABASE HEALTH CHECK
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📊 BASIC STATS
   ✓ People: [count]
   ✓ Visits: [count]
   ✓ Scans: [count]
   ⚠ Dead Letters: [count]

   📈 RECENT ACTIVITY
   • Last 24h: [count] observations
   • Last 7d: [count] observations

   🔍 IDENTITY ISSUES [priority: high]
   ⚠ Missing canonical_id: [count]
   ⚠ URL-based IDs: [count]
   ⚠ Duplicate aliases: [count]

   📋 DATA QUALITY [priority: medium]
   • Missing names: [count]
   • Missing positions: [count]
   • Orphaned observations: [count]

   💀 DEAD LETTERS
   • Pending: [count]
   • Failed again: [count]
   • Common errors:
     - [error type]: [count]
     - [error type]: [count]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [SUMMARY]
   Overall health: [GOOD/WARNING/CRITICAL]
   Priority actions: [list top 3 issues to fix]
   ```

3. **Priority levels:**
   - CRITICAL: > 10% people have identity issues
   - WARNING: > 5% people have quality issues or > 100 pending dead letters
   - GOOD: < 5% issues overall

4. **Detailed mode** (--detailed flag):
   - Show sample records for each issue type
   - List specific people with problems
   - Provide SQL/MongoDB queries to investigate further

## Error Handling

- If database connection fails, show clear error
- If any check fails, continue with others and note the failure
