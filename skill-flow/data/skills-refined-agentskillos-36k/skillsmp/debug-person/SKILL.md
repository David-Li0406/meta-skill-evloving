---
name: debug-person
description: Find and inspect a person in the database using any identifier (username, Sales Nav ID, numeric ID, profile URL, or name). Use when debugging person records, looking up specific people, inspecting aliases and observations, or investigating identity issues.
---

# Debug Person

**Purpose:** Streamlines the common debugging task of finding and inspecting person records.

## Instructions for Claude

When this skill is invoked:

1. **Parse the identifier** from the args (username, Sales Nav ID, URL, numeric ID, or name)

2. **Create and run a Node.js script** that:
   - Connects to the MongoDB database
   - Searches for the person using multiple strategies:
     - Exact match on `_id`
     - Exact match on `aliases.value`
     - Exact match on `canonical_id`
     - Fuzzy match on `snapshot.fullName` (case-insensitive)
   - If found, displays:
     - Basic info (ID, canonical_id, name, current position)
     - All aliases (grouped by type)
     - Observation counts (visits, scans)
     - Last observed date
     - Current snapshot summary
     - Recent observations (last 3)
   - If not found, suggests similar matches
   - Disconnects from database

3. **Output format:**
   ```
   ✓ FOUND: [Full Name]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ID:           [_id]
   Canonical ID: [canonical_id]

   Current Position:
     • [currentTitle] at [currentCompany]

   Aliases:
     • salesNavId: [value]
     • numericId: [value]
     • profileUrl: [value]
     • linkedInUsername: [value]

   Observations:
     • Visits: [count]
     • Scans: [count]
     • Last seen: [date]

   Location: [location info]

   Recent Observations:
     1. [type] - [date]
     2. [type] - [date]
     3. [type] - [date]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

4. **Example usage:**
   - `/debug-person riya-thosar`
   - `/debug-person ACoAAAOp_GgBB5xIe1UsUcokRenyVryVDfOYAfI`
   - `/debug-person 123456789`
   - `/debug-person linkedin.com/in/mahesh-chandra-wipro`

## Error Handling

- If no match found, display: "✗ NOT FOUND" and suggest similar names
- If multiple matches, display all with basic info and ask user to clarify
- If database connection fails, show clear error message
