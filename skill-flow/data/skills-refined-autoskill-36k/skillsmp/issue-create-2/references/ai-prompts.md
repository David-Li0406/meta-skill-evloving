# AI Prompts Reference

This document describes the AI prompts used by the issue-create skill for content detection and label suggestion.

## Model Configuration

| Setting  | Value                               |
| -------- | ----------------------------------- |
| Model    | openai/gpt-4.1                      |
| Provider | GitHub Models (gh-models extension) |
| Timeout  | 30 seconds                          |
| Fallback | Keyword-based matching              |

## Content Type Detection Prompt

**Purpose**: Classify issue content into one of four categories.

```
Classify this GitHub issue content into exactly one category.
Categories: bug, feature, question, documentation
Return ONLY the category name, nothing else.

Content:
{content}
```

**Expected Response**: Single word - `bug`, `feature`, `question`, or `documentation`

**Validation**: Response must contain one of the valid category names.

## Label Suggestion Prompt

**Purpose**: Suggest 2-4 labels from the repository's existing taxonomy.

```
Suggest 2-4 labels from the EXISTING taxonomy only for this GitHub issue.
Never suggest labels that don't exist in the list below.
Return ONLY a JSON array of label names, nothing else.

AVAILABLE LABELS:
- label1: description
- label2: description
...

ISSUE TITLE: {title}
ISSUE BODY:
{body}

Return format: ["label1", "label2"]
```

**Expected Response**: JSON array of label names

```json
["bug", "authentication", "priority-high"]
```

**Validation**:

1. Parse as JSON array
2. Filter to only labels that exist in taxonomy
3. Return validated list

## Title Extraction (Future)

**Purpose**: Extract a clear, searchable title from issue content.

```
Extract a clear, searchable GitHub issue title (max 72 chars).
Format: "{Type}: {Specific description}"
Content: {content}
```

**Expected Response**: Single line title string

## Error Handling

### AI Unavailable

1. Check if gh-models extension is installed
2. If not, offer installation command
3. Fall back to keyword-based detection

### Parse Errors

1. Log the raw response for debugging
2. Fall back to keyword matching
3. Return empty array for labels

### Timeout

1. 30-second timeout on all AI calls
2. On timeout, fall back to keywords
3. Log timeout event

## Prompt Engineering Guidelines

1. **Be Explicit**: Clearly state expected output format
2. **Constrain Output**: Ask for ONLY the specific format needed
3. **Provide Context**: Include relevant labels/categories
4. **Limit Input**: Truncate long content to avoid token limits
5. **Validate Output**: Always validate AI responses before use

## Token Considerations

| Content         | Limit          |
| --------------- | -------------- |
| Issue body      | 2000 chars max |
| Label list      | 200 labels max |
| Prompt overhead | ~200 tokens    |

## Debugging AI Responses

Enable verbose logging:

```bash
bun issue-create.ts --body "..." --verbose
```

Check logs:

```bash
tail -20 ~/.claude/logs/gh-issue-create.jsonl | jq 'select(.ai_model)'
```
