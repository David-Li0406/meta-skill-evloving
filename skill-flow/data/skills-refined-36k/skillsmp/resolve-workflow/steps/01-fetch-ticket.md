---
name: fetch-ticket
description: Retrieve ticket from source, extract Figma URLs, collect user context
order: 1

skip_if:
  - flag: "--continue"
  - flag: "--refine-plan"

next:
  default: analyze-complexity

tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
  - mcp__youtrack__get_issue
  - mcp__youtrack__get_issue_comments
  - mcp__youtrack__get_issue_attachments
---

# Step: Fetch Ticket

<context>
This step retrieves the ticket from the configured source (YouTrack, GitHub, or file),
extracts Figma URLs for visual verification, and optionally collects additional user context.
</context>

## Instructions

<instructions>

### 1. Fetch Ticket Content

Apply skill: `~/.claude/skills/fetch-ticket/SKILL.md`

- Detect source from ticket ID pattern
- Retrieve ticket via MCP (YouTrack) or gh CLI (GitHub)
- Save to `.claude/feature/{ticket-id}/ticket.md`

### 2. Extract Figma URLs

Parse ticket content (description + comments) for Figma URLs:

**Pattern**: `https://www.figma.com/(file|design|proto|board)/[A-Za-z0-9]+/.*node-id=[\d-]+`

If URLs found, store in `status.json`:
```json
{
  "figma_urls": ["url1", "url2"]
}
```

### 3. Handle Missing Figma URLs (INTERACTIVE only)

If no URLs found:

```yaml
AskUserQuestion:
  question: "Aucun lien Figma specifique trouve dans le ticket. Y a-t-il des ecrans Figma a verifier ?"
  header: "Figma"
  options:
    - label: "Oui, je fournis les liens"
      description: "Saisir les URLs Figma pour verification visuelle"
    - label: "Non, pas de verification"
      description: "Continuer sans verification visuelle"
```

If user provides URLs, store them in `status.json`.

### 4. Add User Context (INTERACTIVE only)

Offer opportunity to provide additional context:

```yaml
AskUserQuestion:
  question: "Voulez-vous ajouter du contexte supplementaire pour ce ticket ?"
  header: "Context"
  options:
    - label: "Oui, j'ai des precisions"
      description: "Ajouter des commentaires, contraintes ou clarifications"
    - label: "Non, continuer"
      description: "Le ticket est suffisamment clair"
```

If user adds context:
1. Store in `status.json` as `user_context`
2. Append to `ticket.md`:
   ```markdown
   ---

   ## Additional Context (User Provided)

   {user_context}
   ```

</instructions>

## Output

<output>
- File: `.claude/feature/{ticket-id}/ticket.md`
- Status: `phases.fetch = "completed"`
- Optional: `figma_urls[]`, `user_context`
</output>

## Auto Behavior

<auto_behavior>
- Skip Figma URL prompt (continue without visual verification if none found)
- Skip user context prompt
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Prompt for Figma URLs if not found
- Prompt for additional user context
</interactive_behavior>

## Context Types

<example>
Types of context the user might provide:
- Technical constraints not mentioned in the ticket
- Preferred implementation approach
- Related code areas to check
- Edge cases to consider
- Business rules clarifications
- Dependencies or blockers
- Links to documentation or examples
</example>
