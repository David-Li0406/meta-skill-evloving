# question archetypes

patterns for different question types and when to deploy them.

## core archetypes

### 1. clarification

resolve ambiguity in user's request.

**when**: user's language has multiple interpretations

```yaml
question: "when you say 'tier-aware', which dimension matters most?"
header: "tier focus"
options:
  - label: "user relationship"
    description: "how well saya knows this person (new vs familiar)"
  - label: "channel type"
    description: "public channel vs DM vs thread context"
  - label: "workspace culture"
    description: "formal work vs casual team vs personal"
```

**chaining**: answer informs scope of next question

---

### 2. preference

understand user's aesthetic/process preferences.

**when**: multiple valid approaches, user taste matters

```yaml
question: "what interaction style feels right for onboarding?"
header: "style"
options:
  - label: "warm + curious"
    description: "ask questions, show interest, build rapport"
  - label: "quiet + observant"
    description: "watch first, contribute when value-add is clear"
  - label: "playful + proactive"
    description: "jump in with personality, light touch"
```

**chaining**: preference shapes all subsequent options

---

### 3. confirmation

validate assumptions before proceeding.

**when**: context search revealed something - verify before acting

```yaml
question: "found existing ack logic in decisions.ts. is this the right place to modify?"
header: "location"
options:
  - label: "yes, modify there (Recommended)"
    description: "keep ack generation centralized in attention agent"
  - label: "no, extract to new module"
    description: "separate ack logic into its own composable"
  - label: "need to understand more first"
    description: "show me the current flow before deciding"
```

**chaining**: confirmation unlocks implementation questions

---

### 4. exploration

map the problem space when boundaries unclear.

**when**: early in conversation, problem scope fuzzy

```yaml
question: "what aspects of the current behavior bother you most?"
header: "pain point"
multiSelect: true
options:
  - label: "repetitive acks"
    description: "'on it~' every time feels robotic"
  - label: "channel announcements"
    description: "'yo #channel' feels unnatural"
  - label: "timing/pacing"
    description: "messages arrive at wrong moments"
  - label: "tone mismatch"
    description: "voice doesn't match context"
```

**chaining**: selected pain points become focused follow-ups

---

### 5. trade-off

surface tensions between competing values.

**when**: implementation choices have real costs

```yaml
question: "how should we balance personality vs efficiency in acks?"
header: "trade-off"
options:
  - label: "lean into personality"
    description: "more varied, creative acks even if occasionally miss"
  - label: "optimize for relevance"
    description: "only ack when truly useful, skip when redundant"
  - label: "context-dependent"
    description: "personality in casual, efficiency in serious"
```

**chaining**: trade-off choice constrains future options

---

### 6. scope

bound the work before diving in.

**when**: task could be small or huge depending on interpretation

```yaml
question: "how far should we take this fix?"
header: "scope"
options:
  - label: "quick patch"
    description: "fix the 'yo' and 'on it~' specifically, ship fast"
  - label: "systematic fix"
    description: "audit all ack/greeting patterns, consistent solution"
  - label: "full redesign"
    description: "rethink onboarding flow architecture"
```

**chaining**: scope determines depth of subsequent questions

---

### 7. meta

step back from the problem to examine the process.

**when**: after 3-4 questions, or when sensing drift

```yaml
question: "we've covered acks, onboarding, and context-awareness. what feels missing?"
header: "reflection"
options:
  - label: "nothing, ready to proceed"
    description: "clear picture, let's implement"
  - label: "testing strategy"
    description: "how will we verify this works?"
  - label: "edge cases"
    description: "what weird situations might break this?"
  - label: "prior art"
    description: "are there patterns elsewhere we should reference?"
```

**chaining**: meta answers often reveal new question threads

---

### 8. integration

understand how this connects to other systems.

**when**: implementation touches multiple areas

```yaml
question: "should this connect to other agents/systems?"
header: "integration"
multiSelect: true
options:
  - label: "reaction agent"
    description: "coordinate acks with emoji reactions"
  - label: "memory/context system"
    description: "remember user preferences across sessions"
  - label: "analytics"
    description: "track what ack styles land well"
  - label: "keep isolated"
    description: "start simple, integrate later"
```

**chaining**: integrations spawn technical questions

---

### 9. sequence

establish order of operations.

**when**: multiple things need to happen, order matters

```yaml
question: "what should happen first when saya joins a channel?"
header: "sequence"
options:
  - label: "immediate context-aware ack"
    description: "quick wave, then analyze"
  - label: "silent analysis first"
    description: "observe, then speak with context"
  - label: "user-dependent"
    description: "immediate for new users, silent for familiar"
```

**chaining**: sequence locks in implementation order

---

### 10. edge case

probe boundary conditions.

**when**: core path clear, need to handle weird situations

```yaml
question: "what if saya is added to a channel where she's the only member?"
header: "edge case"
options:
  - label: "skip intro entirely"
    description: "no one to greet, stay silent"
  - label: "brief self-note"
    description: "leave a marker for later ('ready when you are')"
  - label: "full onboarding anyway"
    description: "treat it as practice run"
```

**chaining**: edge cases often reveal unstated assumptions

## archetype combinations

### discovery sequence
`exploration → clarification → preference → confirmation`

good for: new features, unclear requirements

### implementation sequence
`scope → trade-off → sequence → edge case`

good for: well-defined work, technical decisions

### debugging sequence
`confirmation → exploration → meta → integration`

good for: bug fixes, unexpected behavior

### architecture sequence
`trade-off → integration → scope → meta`

good for: system design, refactoring

## voice notes

questions should feel conversational:

| avoid | prefer |
|-------|--------|
| "would you like me to..." | "should we..." |
| "what is your preference for..." | "which feels right?" |
| "please select an option" | "what's the move here?" |
| "shall i proceed with..." | "ready to go with this?" |

headers stay punchy (12 chars max):
- "auth method" not "authentication approach"
- "scope" not "project scope"
- "trade-off" not "trade-off consideration"

descriptions reveal implications:
- not just "what" but "so what"
- include cost/benefit hints
- surface non-obvious consequences
