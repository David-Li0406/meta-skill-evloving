---
name: Verified Data Only
description: MANDATORY skill that enforces strict data integrity - NO simulated, fake, or extrapolated data allowed. Only verified scraped data from confirmed sources.
---

# 🚨 VERIFIED DATA ONLY - MANDATORY ACKNOWLEDGMENT REQUIRED 🚨

## Critical Law: Data Integrity Mandate

**Before EVERY scraping operation, you MUST read and acknowledge this skill.**

### Absolute Rules

1. **NO SIMULATED DATA** - Never generate fake tournament data
2. **NO EXTRAPOLATED DATA** - Never estimate dates, buy-ins, or guarantees based on "typical patterns"
3. **NO INVENTED SERIES** - Never create series names that weren't explicitly found in search results
4. **ONLY VERIFIED DATA** - Every single data point must come directly from a confirmed source

### Required Source Verification

For each piece of data inserted into the database, you MUST have:

- ✅ **Explicit confirmation** from a search result (web search, URL content, or browser scrape)
- ✅ **Source citation** - the website/source where the data was found
- ✅ **Date verification** - confirm the event is for 2026, not 2025 or prior years

### Forbidden Actions

❌ "Based on typical patterns, this venue usually runs events in March..."
❌ "Similar to last year, I estimate the buy-in would be..."
❌ "This venue typically hosts a spring series, so I'll add one..."
❌ Adding any series/event without explicit search result confirmation

### Required Acknowledgment

**Before providing ANY SQL for tournament data, the agent MUST state:**

> "I acknowledge the Verified Data Only mandate. The following data comes exclusively from confirmed search results. Each entry includes source attribution. No simulated, extrapolated, or invented data is included."

### Violation Consequences

If ANY data is later found to be extrapolated or invented:
1. Immediately provide DELETE SQL to remove the fake entries
2. Document the violation
3. Re-scrape with proper verification

### Audit Trail

For each batch of SQL provided, include:
- List of search queries performed
- Source websites cited
- Explicit confirmation that each data point was found in results

---

## Example of CORRECT Behavior

```
Agent performs: search_web("bestbet Jacksonville poker 2026 blizzard")

Search result says: "bestbet Blizzard Festival February 5-16, 2026, $1,700 Mystery Bounty Main Event, $400,000 GTD"

Agent then provides SQL with ONLY the data explicitly stated:
- Series: bestbet Blizzard Festival
- Dates: Feb 5-16, 2026
- Buy-in: $1,700 (for mystery bounty)
- GTD: $400,000
- Source: bestbetjax.com

✅ This is correct - all data came from verified search result
```

## Example of INCORRECT Behavior

```
Agent performs: search_web("Lucky Chances Casino poker 2026")

Search result: No specific 2026 series found

Agent then INVENTS: "Lucky Chances Winter Series, Jan 15-26, $150-$500, $75K GTD"

❌ VIOLATION - This data was fabricated, not found in search results
```

---

**This skill MUST be acknowledged before every scraping session.**
