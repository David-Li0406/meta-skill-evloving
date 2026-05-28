# Label Strategy Reference

This document describes the label suggestion strategy used by the issue-create skill.

## Core Principles

1. **Taxonomy Awareness**: Only suggest labels that exist in the repository
2. **Conservative Suggestions**: Suggest 2-4 labels (not too many)
3. **Type Alignment**: Prefer labels matching detected content type
4. **Cache Efficiency**: Cache labels per-repo for 24 hours

## Label Suggestion Flow

```
1. Fetch Labels
   └── gh label list --repo OWNER/REPO --json name,description,color

2. Cache Check
   ├── Hit (< 24h) → Use cached labels
   └── Miss → Fetch fresh, cache result

3. AI Suggestion (if gh-models available)
   ├── Build prompt with available labels
   ├── Send to openai/gpt-4.1
   └── Parse JSON response

4. Fallback (keyword matching)
   ├── Match content against keyword patterns
   └── Return matching labels from taxonomy

5. Validation
   └── Filter out any labels not in taxonomy
```

## AI Prompt Template

```
Suggest 2-4 labels from the EXISTING taxonomy only for this GitHub issue.
Never suggest labels that don't exist in the list below.
Return ONLY a JSON array of label names, nothing else.

AVAILABLE LABELS:
- bug: Something isn't working
- enhancement: New feature or request
- documentation: Improvements to docs
...

ISSUE TITLE: {title}
ISSUE BODY:
{body}

Return format: ["label1", "label2"]
```

## Keyword Patterns (Fallback)

| Label Category   | Keywords                                               |
| ---------------- | ------------------------------------------------------ |
| bug              | bug, error, crash, broken, fail, exception, defect     |
| enhancement      | feature, add, implement, improve, enhancement, request |
| documentation    | docs, documentation, readme, typo, example, guide      |
| question         | question, help, how, support, confused                 |
| good first issue | simple, easy, beginner, first, starter                 |
| priority         | urgent, critical, blocker, important, asap             |
| help wanted      | help, wanted, contribution, volunteer                  |

## Cache Structure

Location: `~/.cache/gh-issue-skill/labels/{owner}_{repo}.json`

```json
{
  "labels": [
    {
      "name": "bug",
      "description": "Something isn't working",
      "color": "d73a4a"
    }
  ],
  "cachedAt": 1705123456789,
  "repo": "owner/repo"
}
```

## Cache Management

```bash
# View cache
ls ~/.cache/gh-issue-skill/labels/

# Invalidate specific repo cache
rm ~/.cache/gh-issue-skill/labels/owner_repo.json

# Clear all cache
rm -rf ~/.cache/gh-issue-skill/labels/
```

## Edge Cases

### Empty Taxonomy

- Repository has no labels
- Behavior: Skip label suggestion, log warning
- User action: Consider adding labels to repository

### Large Taxonomy (100+ labels)

- AI handles large taxonomies better than keywords
- Keyword fallback may be less accurate
- Consider enabling gh-models for best results

### Private Repositories

- Requires appropriate GitHub authentication
- Uses `gh` CLI which handles auth automatically
