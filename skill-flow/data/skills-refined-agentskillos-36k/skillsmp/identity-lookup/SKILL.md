---
name: identity-lookup
description: Resolve LinkedIn identity from any identifier (URL, username, Sales Nav ID, numeric ID) to canonical form, showing all known aliases and suggesting the best stable identifier to use. Use when investigating identity resolution, understanding which identifier to use in code, or troubleshooting duplicate person records.
---

# Identity Lookup

**Purpose:** Helps understand identity resolution and find the canonical ID for a person.

## Instructions for Claude

When this skill is invoked:

1. **Parse the identifier** from args (can be URL, Sales Nav ID, numeric ID, username, etc.)

2. **Create and run a Node.js script** that:
   - Uses the same identity resolution logic as the main ETL pipeline
   - Shows step-by-step resolution process
   - Indicates which identifier was matched
   - Shows priority order of identifiers
   - Displays final canonical_id

3. **Resolution strategy** (following project rules):
   ```
   Priority order:
   1. Sales Navigator ID (ACwAAAA... or ACoAAAA...)
   2. LinkedIn numeric ID (8+ digits)
   3. LinkedIn username (from URL)
   4. Profile URL (least stable)
   ```

4. **Output format:**
   ```
   IDENTITY RESOLUTION
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Input: [original identifier]

   🔍 RESOLUTION PROCESS:
   Step 1: Parse identifier
     • Type detected: [salesNavId/numericId/username/url]
     • Normalized value: [normalized]

   Step 2: Database lookup
     • Match found: YES/NO
     • Matched on: aliases.value (type: [type])

   Step 3: Canonical ID
     • Person _id: [_id]
     • Canonical ID: [canonical_id]

   ✓ RESOLVED TO:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Name: [fullName]
   Best ID: [salesNavId or numericId]

   ALL KNOWN ALIASES:
   ✓ salesNavId:         [value] ⭐ (most stable)
   ✓ numericId:          [value] ⭐ (very stable)
   • linkedInUsername:   [value]
   • profileUrl:         [value] (unstable)
   • publicUrl:          [value] (unstable)

   RECOMMENDATION:
   Use this identifier in your code:
   const PERSON_ID = '[best stable ID]';

   Reason: [why this ID is best]
   ```

## Error Handling

- Invalid format: explain expected formats
- Not found: suggest corrections and similar names
- Database errors: show clear message
