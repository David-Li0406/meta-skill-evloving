---
name: recall-memory
description: Search and retrieve from memory. Use when user asks about past conversations, "what did we discuss", "find my notes about", "remember when", or needs historical context.
allowed-tools: mcp__aiii__recall_memories, mcp__aiii__list_spaces
---

# Recall from Memory

Search and retrieve previously saved memories from aiii's local store.

## When to Use

- User asks about previous conversations
- User needs context from past sessions
- User wants to find specific notes or decisions
- Before making a decision that might contradict past context

## Instructions

1. **Parse the user's query** for:
   - Keywords and topics
   - Time references ("yesterday", "last week", "when we discussed X")
   - Space hints ("my work notes", "health stuff")

2. **Formulate the search**:
   - Extract primary search terms
   - Identify space filter if mentioned
   - Determine result limit (default 5-10)

3. **Call recall_memories tool**:

   ```json
   {
     "query": "search terms",
     "space_id": "space_xxx", // optional
     "limit": 10
   }
   ```

4. **Present results clearly**:
   - Show title and date for each result
   - Include brief summary preview
   - Indicate the source (claude-code, claude-desktop, etc.)
   - Group by space if multiple spaces returned

5. **Offer to expand**:
   - Ask if user wants full content of any specific memory
   - Offer to narrow search if too many results
   - Suggest related searches if no results found

## Result Format

```
## Found 3 memories

### Work Space
1. **Auth refactoring: JWT to session-based** (Jan 7, 2026)
   > Refactored authentication from JWT to session-based approach...
   Source: claude-code | Tags: auth, jwt

2. **Rate limiting implementation** (Jan 6, 2026)
   > Added sliding window rate limiter to API endpoints...
   Source: claude-code | Tags: api, security

### Health Space
3. **Vitamin D discussion** (Jan 5, 2026)
   > Discussed optimal vitamin D levels and supplementation...
   Source: claude-desktop | Tags: vitamins, supplements
```

## No Results Handling

If no memories match:

1. Acknowledge the search found nothing
2. Suggest broadening search terms
3. List available spaces that might contain relevant info
4. Offer to help reformulate the query

## Example Interaction

**User:** "What did we discuss about authentication last week?"

**Claude:**

1. Parses: topic="authentication", time="last week"
2. Searches: `query: "authentication", limit: 10`
3. Finds 2 results in Work space
4. Presents formatted results
5. Offers: "Want me to show the full content of any of these?"
