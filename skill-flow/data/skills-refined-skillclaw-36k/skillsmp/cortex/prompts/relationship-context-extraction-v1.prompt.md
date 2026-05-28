# Relationship Context Extraction Prompt v1

## Purpose

Extract context about the user's relationships from conversations. This helps agents understand who people are and how they relate to the user, enabling more contextual responses.

## Input

- **Channel**: The communication channel (iMessage, Gmail, Cursor, etc.)
- **User**: The owner of the cortex database
- **Primary Contact**: The person the user is communicating with (if applicable)
- **Messages**: A conversation chunk

## Task

Extract relationship context about people mentioned:

1. **Who they are** — Name, role, how they relate to the user
2. **Relationship type** — Family, friend, colleague, etc.
3. **Context clues** — Things that help understand the relationship
4. **Communication patterns** — How the user talks to/about this person
5. **Importance signals** — How important this person is to the user

### Relationship Categories

| Category | Examples |
|----------|----------|
| **family** | Parents, siblings, spouse/partner, children |
| **romantic** | Girlfriend/boyfriend, spouse, partner |
| **friends** | Close friends, friend groups |
| **professional** | Colleagues, boss, reports, clients |
| **service** | Doctor, lawyer, accountant, etc. |
| **acquaintance** | Neighbors, casual contacts |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "imessage",
    "user_name": "Tyler Brandt",
    "primary_contact": "Casey Adams",
    "message_count": 100,
    "date_range": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-15T23:59:59Z"
    }
  },
  "relationships": [
    {
      "person_name": "Casey Adams",
      "relationship_type": "romantic",
      "relationship_label": "girlfriend",
      "memory_entry": "Casey Adams — girlfriend, they live together, dating since February 2023",
      "context": "They live together, dating since February 2023",
      "evidence": [
        "Can you pick up groceries on your way home?",
        "Our 3rd anniversary is coming up"
      ],
      "importance": "high",
      "confidence": "high"
    },
    {
      "person_name": "Dad",
      "canonical_name": "Jim Brandt",
      "relationship_type": "family",
      "relationship_label": "father",
      "memory_entry": "Jim Brandt (Dad) — father, owns Napa General Store, lives in Napa",
      "context": "Owns Napa General Store, lives in Napa",
      "evidence": [
        "Dad's dealing with the store stuff again",
        "Heading to Napa to see the parents"
      ],
      "importance": "high",
      "confidence": "high"
    },
    {
      "person_name": "Sarah",
      "relationship_type": "professional",
      "relationship_label": "colleague",
      "memory_entry": "Sarah — colleague, works with me on API redesign",
      "context": "Works at same company, collaborates on projects",
      "evidence": [
        "Sarah and I are working on the API redesign"
      ],
      "importance": "medium",
      "confidence": "medium"
    }
  ],
  "relationship_updates": [
    {
      "person_name": "Casey Adams",
      "update_type": "milestone",
      "detail": "3rd anniversary coming up (February)",
      "evidence": "Our 3rd anniversary is coming up in February"
    }
  ]
}
```

---

## Important Rules

1. **Focus on durable relationship facts** — Not transient interactions
2. **Capture relationship nuance**:
   - How the user refers to them (nickname vs formal name)
   - Tone of communication
   - Frequency/importance signals
3. **Include memory_entry** — A compact sentence suitable for MEMORY.md
4. **Link to canonical names** — If a nickname is used, try to identify full name
5. **Evidence matters** — Quote text that establishes the relationship
6. **Importance levels**:
   - **high**: Family, romantic partner, very close friends
   - **medium**: Regular contacts, colleagues
   - **low**: Occasional mentions, acquaintances
7. **Confidence levels**:
   - **high**: Relationship explicitly stated or very clear from context
   - **medium**: Implied through interaction patterns
   - **low**: Single mention, uncertain relationship
8. **Track updates** — Note life events, milestones, changes in relationship

---

## Privacy Considerations

- Focus on relationship context, not personal details about third parties
- Don't extract sensitive information about others
- The goal is to help agents understand social context, not build dossiers

---

## Conversation
{{{segment_text}}}
