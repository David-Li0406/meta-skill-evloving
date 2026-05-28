---
name: force-matching
description: >-
  UK police force identification via JavaScript pattern matching.
  ALWAYS use this before AI classification (see Guardrail G-005).
user-invocable: false
---

# Force Matching Skill

## Guardrail Reference

**G-005: Fuzzy JS Matching Before AI**

> Run hardcoded JavaScript pattern matching BEFORE falling back to AI for force identification.

**Why**: AI = 200ms + $0.002 per call. JS = <1ms + free. Pattern covers ~85% of cases.

## Quick Usage

```javascript
// In n8n Code node or JavaScript
const { lookupForce, processJobsWithForceMatching } = require('./patterns/force-matching.js');

// Single lookup
const force = lookupForce('Met Police HR Team');
// Returns: 'Metropolitan Police Service'

// Batch processing
const enrichedJobs = processJobsWithForceMatching(items);
// Adds: matchedForce, forceMatchedBy fields
```

## Coverage

**47 patterns** covering:
- 43 territorial police forces
- 5 national agencies (BTP, NCA, PSNI, Police Scotland, CTP)
- Common abbreviations (Met, PSNI, BTP)
- Naming variations (Constabulary vs Police)

## When to Use

### ALWAYS Before AI Classification

```
[Job Data] → [Force Matching JS] → Match? → Use it (skip AI)
                                → No match? → [Claude AI]
```

### In n8n Workflows

Add a Code node BEFORE the AI classification node:

```javascript
// n8n Code node
const FORCE_PATTERNS = {
  'metropolitan police': 'Metropolitan Police Service',
  'met police': 'Metropolitan Police Service',
  // ... (full list in patterns/force-matching.js)
};

function lookupForce(text) {
  if (!text) return null;
  const textLower = text.toLowerCase();
  for (const [pattern, forceName] of Object.entries(FORCE_PATTERNS)) {
    if (textLower.includes(pattern)) {
      return forceName;
    }
  }
  return null;
}

// Process items
return items.map(item => {
  const companyName = item.json.company_name || '';
  const matchedForce = lookupForce(companyName);

  return {
    json: {
      ...item.json,
      matchedForce,
      forceMatchedBy: matchedForce ? 'pattern' : null,
      needsAIClassification: !matchedForce
    }
  };
});
```

Then route:
- `needsAIClassification === false` → Skip AI, proceed with matched force
- `needsAIClassification === true` → Send to Claude API

## Pattern Examples

| Input | Output |
|-------|--------|
| `Met Police HR Team` | Metropolitan Police Service |
| `Hampshire Constabulary` | Hampshire Constabulary |
| `PSNI` | Police Service of Northern Ireland |
| `British Transport Police` | British Transport Police |
| `Random Company Ltd` | `null` (needs AI) |

## Maintenance

**Source file**: `patterns/force-matching.js`

**To add a pattern**:
1. Edit `patterns/force-matching.js`
2. Add to `FORCE_PATTERNS` object
3. Test with sample inputs
4. Commit with `[patterns] Add force pattern: X`

**Related data**: `reference-data/uk-police-forces.json` (48 forces)

## Integration Checklist

When building a job classification workflow:

- [ ] Added Code node for force matching BEFORE AI node
- [ ] Routing splits on `needsAIClassification`
- [ ] AI-classified results stored with `forceMatchedBy: 'ai'`
- [ ] Pattern-matched results stored with `forceMatchedBy: 'pattern'`
- [ ] Both paths merge to same output

## Cost Savings

| Method | Time | Cost |
|--------|------|------|
| JS Pattern | <1ms | Free |
| Claude API | ~200ms | ~$0.002 |

At 1000 jobs/day with 85% pattern hit rate:
- 850 jobs × $0.00 = $0.00 (pattern)
- 150 jobs × $0.002 = $0.30 (AI)
- **Savings**: $1.70/day vs all-AI

## Troubleshooting

**Pattern not matching expected force**:
1. Check lowercase in `FORCE_PATTERNS`
2. Verify spelling matches exactly
3. Add pattern variation if needed

**Too many false positives**:
1. Pattern may be too broad
2. Consider more specific pattern
3. Let AI handle ambiguous cases
