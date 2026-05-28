# Self-Knowledge Extraction Prompt v1

## Purpose

Extract what the user knows, understands, and cares about from conversations. This creates a profile of the user's expertise, interests, and context that agents can reference.

## Input

- **Channel**: The communication channel (iMessage, Gmail, Cursor, etc.)
- **User**: The owner of the cortex database
- **Messages**: A conversation chunk

## Task

Extract knowledge signals about the user:

1. **Technical skills** — Programming languages, tools, frameworks they know
2. **Domain expertise** — Areas they demonstrate deep understanding
3. **Current projects** — What they're working on
4. **Interests** — Topics they engage with enthusiastically
5. **Context they provide** — Background they share that indicates knowledge
6. **Questions they ask** — What they're learning or don't know (inverse signal)

### Knowledge Categories

| Category | Examples |
|----------|----------|
| **technical_skills** | Languages, frameworks, tools, platforms |
| **domain_expertise** | Business areas, industries, specialized knowledge |
| **current_work** | Active projects, responsibilities, focus areas |
| **interests** | Topics they care about, engage with, read about |
| **relationships** | People they know, professional network |
| **learning** | Things they're actively learning or curious about |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "cursor",
    "user_name": "Tyler Brandt",
    "message_count": 60,
    "date_range": {
      "start": "2024-01-15T10:00:00Z",
      "end": "2024-01-15T16:00:00Z"
    }
  },
  "knowledge": [
    {
      "category": "technical_skills",
      "knowledge": "Proficient in Go",
      "memory_entry": "technical_skills: Proficient in Go",
      "evidence": "I'll refactor this to use Go interfaces properly",
      "confidence": "high",
      "signal_type": "demonstrated"
    },
    {
      "category": "technical_skills",
      "knowledge": "Understands SQLite internals",
      "memory_entry": "technical_skills: Understands SQLite internals",
      "evidence": "We need to use WAL mode here for the concurrent writes, and probably increase the busy_timeout",
      "confidence": "high",
      "signal_type": "demonstrated"
    },
    {
      "category": "domain_expertise",
      "knowledge": "Deep understanding of LLM orchestration patterns",
      "memory_entry": "domain_expertise: Deep understanding of LLM orchestration patterns",
      "evidence": "The issue is context window management - we need compaction before we hit the limit, not after",
      "confidence": "high",
      "signal_type": "demonstrated"
    },
    {
      "category": "current_work",
      "knowledge": "Building Nexus - AI workspace/OS for personal productivity",
      "memory_entry": "current_work: Building Nexus - AI workspace/OS for personal productivity",
      "evidence": "This is for nexus, my AI workspace project",
      "confidence": "high",
      "signal_type": "explicit"
    },
    {
      "category": "interests",
      "knowledge": "Cares deeply about developer experience",
      "memory_entry": "interests: Cares deeply about developer experience",
      "evidence": "The DX here is terrible, nobody will use this if it's this complicated",
      "confidence": "medium",
      "signal_type": "demonstrated"
    },
    {
      "category": "learning",
      "knowledge": "Learning about embedding models",
      "memory_entry": "learning: Learning about embedding models",
      "evidence": "How do the different embedding models compare? I'm not sure which to use",
      "confidence": "medium",
      "signal_type": "question"
    }
  ]
}
```

---

## Important Rules

1. **Focus on durable knowledge** — Skills and expertise, not transient facts
2. **Include memory_entry** — A compact sentence suitable for MEMORY.md (prefix with category)
3. **Distinguish proficiency levels**:
   - "Proficient in X" — demonstrates fluent use
   - "Understands X" — shows conceptual understanding
   - "Familiar with X" — basic awareness
   - "Learning X" — actively acquiring
4. **Quote evidence** — Include the text that shows the knowledge
5. **Confidence levels**:
   - **high**: Demonstrated expertise or explicit statement
   - **medium**: Implied through discussion
   - **low**: Single mention or unclear signal
6. **Signal types**:
   - `demonstrated`: User shows knowledge through action/explanation
   - `explicit`: User directly states they know something
   - `question`: User asks about something (indicates learning/gaps)
   - `context`: User provides background that implies knowledge
7. **Don't confuse interest with expertise** — Asking about X ≠ knowing X
8. **Note recency** — Current projects matter more than past ones

---

## Negative Signals

Also extract things the user explicitly doesn't know or is confused about:

```json
"knowledge_gaps": [
  {
    "category": "technical_skills",
    "gap": "Not familiar with Kubernetes",
    "evidence": "I've never used k8s, can you explain what a pod is?",
    "confidence": "high"
  }
]
```

These are valuable for agents to know what NOT to assume.

---

## Conversation
{{{segment_text}}}
