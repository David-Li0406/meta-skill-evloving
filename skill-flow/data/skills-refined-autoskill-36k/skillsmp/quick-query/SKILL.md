---
name: quick-query
description: Run ad-hoc MongoDB queries in natural language. Translates natural language queries into MongoDB queries and executes them. Use for quick data exploration, answering "how many" questions, finding specific records, or aggregating statistics.
---

# Quick Query

**Purpose:** Quick data exploration without writing scripts.

## Instructions for Claude

When this skill is invoked:

1. **Parse the natural language query** from args

2. **Translate to MongoDB query:**
   - Understand the user intent
   - Generate appropriate Mongoose query
   - Use proper model (Person, Visit, Scan, DeadLetter, Company, Location)
   - Apply filters, projections, sorts, limits as needed

3. **Execute query and format results:**
   - Connect to database
   - Run query
   - Format output in readable table or JSON
   - Show count and sample results
   - Disconnect

4. **Example translations:**

   Input: "How many people work at Google?"
   → `Person.countDocuments({ 'snapshot.currentCompany': /google/i })`

   Input: "Show me people added in the last 7 days"
   → `Person.find({ createdAt: { $gte: new Date(Date.now() - 7*24*60*60*1000) } }).limit(20)`

   Input: "Find people without Sales Nav IDs"
   → `Person.find({ 'aliases.type': { $ne: 'salesNavId' } }).limit(20)`

   Input: "What are the most common job titles?"
   → `Person.aggregate([{ $group: { _id: '$snapshot.currentTitle', count: { $sum: 1 } } }, { $sort: { count: -1 } }, { $limit: 10 }])`

5. **Output format:**
   ```
   QUICK QUERY
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Query: [original natural language]

   MongoDB Query:
   ─────────────────────────────────
   Person.countDocuments({
     'snapshot.currentCompany': /google/i
   })
   ─────────────────────────────────

   ✓ Result: 127 people

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

6. **Safety limits:**
   - Default limit: 20 results (prevent overwhelming output)
   - For counts: no limit
   - Warn if query might be slow

## Examples

```bash
/quick-query how many people have no observations?
/quick-query show people at Microsoft
/quick-query most common companies
/quick-query recent dead letters
```

## Error Handling

- Ambiguous query: ask for clarification
- Invalid model/field: suggest corrections
- Database error: show clear message
- No results: confirm and suggest alternative queries
