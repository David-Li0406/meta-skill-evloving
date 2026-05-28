---
name: save-to-memory
description: Save current conversation to persistent memory. Use when user says "save this", "remember this", "store this for later", or wants to preserve context for future sessions.
allowed-tools: mcp__aiii__save_memory, mcp__aiii__list_spaces, mcp__aiii__create_space
---

# Save to Memory

Save the current conversation or specific content to aiii's local encrypted memory store for future recall.

## When to Use

- User explicitly asks to save/remember something
- Important decision or conclusion was reached
- User wants to preserve context for future sessions
- After completing a significant task

## Instructions

1. **Analyze the conversation** for key content worth saving:
   - Main topics discussed
   - Decisions made
   - Code changes or implementations
   - Important conclusions

2. **Determine the appropriate space**:
   - Query available spaces using the MCP resource `aiii://spaces`
   - Match content to existing spaces:
     - Work: coding, tickets, PRs, technical work
     - Health: medical, fitness, nutrition discussions
     - Learning: tutorials, concepts learned
     - Finance: budgets, investments, purchases
   - If no suitable space exists, offer to create one

3. **Generate a concise title** (under 50 characters):
   - Use action-oriented language
   - Include key identifiers (PR numbers, feature names)
   - Examples: "Fixed auth bug in PR #234", "Vitamin D discussion"

4. **Extract relevant tags**:
   - Technologies used (react, rust, python)
   - Project names
   - Key concepts
   - People mentioned

5. **Create a summary**:
   - 2-3 sentences capturing the essence
   - Include outcomes and next steps if applicable

6. **Call the save_memory tool**:

   ```json
   {
     "content": "Full conversation summary...",
     "title": "Concise title",
     "summary": "Brief 2-3 sentence summary",
     "space_id": "space_xxx",
     "source": "claude-code",
     "tags": ["tag1", "tag2"]
   }
   ```

7. **Confirm to user** with:
   - Space name where saved
   - Title used
   - Tags applied

## Example Interaction

**User:** "Save this conversation about the auth refactoring"

**Claude:**

1. Analyzes conversation → Found auth refactoring discussion
2. Identifies space → Work
3. Generates title → "Auth refactoring: JWT to session-based"
4. Extracts tags → ["auth", "jwt", "refactoring", "security"]
5. Creates summary → "Refactored authentication from JWT to session-based approach. Implemented HttpOnly cookies and CSRF protection. Next: add rate limiting."
6. Saves to aiii
7. Confirms: "Saved to Work space: 'Auth refactoring: JWT to session-based' with tags: auth, jwt, refactoring, security"
