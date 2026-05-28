# Adaptive Questioning Patterns

## Question Types

### Broad Opener
Start exploration of a new area with an open-ended question.

**Purpose**: Understand user's high-level thinking before diving into details

**Pattern**: "What are your [goals/thoughts/expectations] for [area]?"

**Examples**:
- "What are your goals for user authentication?"
- "How do you envision the data storage working?"
- "What should the user experience be like for [feature]?"

**When to Use**: Beginning of new L1 area exploration

---

### Drill-Down
Go deeper into a concept the user mentioned.

**Purpose**: Get specifics on mentioned but unexplored concepts

**Pattern**: "You mentioned [concept] - [specific question about it]?"

**Examples**:
- "You mentioned OAuth - which providers should be supported?"
- "You said 'fast' - what response time are you targeting?"
- "You brought up notifications - should these be real-time or batched?"

**When to Use**: After user mentions something interesting but doesn't elaborate

---

### Probe
Explore areas the user hasn't mentioned but likely matter.

**Purpose**: Surface implicit requirements or unstated assumptions

**Pattern**: "We haven't discussed [area] - [question about it]?"

**Examples**:
- "We haven't discussed error handling - how should login failures work?"
- "We haven't covered offline scenarios - is internet always available?"
- "What about accessibility - are there specific requirements?"

**When to Use**: When important areas remain UNCHARTED

---

### Clarify
Remove ambiguity from vague statements.

**Purpose**: Turn fuzzy requirements into concrete specifications

**Pattern**: "When you say '[vague term]', [specific interpretation question]?"

**Examples**:
- "When you say 'secure', are you thinking encryption at rest, in transit, or both?"
- "By 'admin users', do you mean a separate user type or elevated permissions?"
- "What does 'responsive' mean in this context - fast or mobile-friendly?"

**When to Use**: When user uses subjective or ambiguous terms

---

### Boundary
Define scope and constraints.

**Purpose**: Understand what's in scope vs. out of scope

**Pattern**: "Should [feature/behavior] be included, or is that out of scope?"

**Examples**:
- "Should this work offline, or is internet connection assumed?"
- "Are we supporting multiple languages, or English only for now?"
- "Is this for internal users only, or public-facing?"

**When to Use**: When scope is unclear or seems to be creeping

---

### Trade-off
Surface decisions between competing priorities.

**Purpose**: Force explicit prioritization when options conflict

**Pattern**: "If we can only have one, which matters more: [A] or [B]?"

**Examples**:
- "If we can only have one, security or convenience?"
- "What's more important: fast delivery or comprehensive features?"
- "Would you prioritize data accuracy or processing speed?"

**When to Use**: When detecting potential conflicts or resource constraints

---

### Scenario
Explore behavior through concrete examples.

**Purpose**: Ground abstract requirements in specific situations

**Pattern**: "What should happen when [specific scenario]?"

**Examples**:
- "What should happen when a user enters an incorrect password three times?"
- "If a user loses internet mid-transaction, what's the expected behavior?"
- "How should the system handle two users editing the same item?"

**When to Use**: When need to understand edge cases or error handling

---

### Validation
Confirm understanding of what was discussed.

**Purpose**: Verify interpretation before moving on

**Pattern**: "So to confirm, [summary of understanding]?"

**Examples**:
- "So to confirm, users will login via email/password only, no social auth?"
- "Let me make sure I understand: all data must be encrypted at rest?"
- "So the priority order is: security, then performance, then UX?"

**When to Use**: Before marking an area as EXPLORED

---

## Questioning Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              ADAPTIVE QUESTIONING FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ENTER NEW AREA                                              │
│     └─ Ask BROAD OPENER                                         │
│                                                                 │
│  2. ANALYZE RESPONSE                                            │
│     ├─ Extract key concepts mentioned                           │
│     ├─ Identify areas not addressed                             │
│     └─ Note ambiguities or assumptions                          │
│                                                                 │
│  3. GENERATE FOLLOW-UPS                                         │
│     ├─ DRILL-DOWN questions for mentioned concepts              │
│     ├─ PROBE questions for unaddressed areas                    │
│     └─ CLARIFY questions for ambiguities                        │
│                                                                 │
│  4. SELECT NEXT QUESTION                                        │
│     Based on priority:                                          │
│     1. Critical ambiguities → CLARIFY                           │
│     2. Important gaps → PROBE                                   │
│     3. Mentioned concepts → DRILL-DOWN                          │
│     4. Scope questions → BOUNDARY                               │
│                                                                 │
│  5. OFFER USER CHOICE                                           │
│     ├─ Answer selected question                                 │
│     ├─ Choose different question                                │
│     ├─ Skip this area                                           │
│     └─ Mark area complete                                       │
│                                                                 │
│  6. UPDATE MAP                                                  │
│     ├─ Mark explored areas with findings                        │
│     ├─ Add newly discovered sub-topics                          │
│     └─ Record skipped areas with reasons                        │
│                                                                 │
│  REPEAT until area marked complete or skipped                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Response Analysis

### Extracting Concepts

From user response, identify:

| Pattern | Extraction |
|---------|------------|
| Nouns/noun phrases | Potential sub-areas |
| Adjectives | Quality requirements (may need CLARIFY) |
| "should", "must", "will" | Requirements to document |
| "maybe", "could", "might" | Uncertain areas (may need CLARIFY) |
| Technical terms | Domain concepts to DRILL-DOWN |
| Comparisons | Trade-offs to explore |

### Identifying Gaps

Compare response against expected areas for the topic:

```markdown
Topic: User Authentication
Expected areas:
- [ ] Login method (email, social, SSO)
- [ ] Password requirements
- [ ] Session management
- [ ] Account recovery
- [ ] Multi-factor auth
- [ ] Rate limiting
- [ ] Audit logging

User covered: Login method, Password requirements
Gaps: Session management, Account recovery, MFA, Rate limiting, Audit logging

Generate PROBE questions for gaps.
```

### Detecting Ambiguity

Look for vague terms that need CLARIFY:

| Vague Term | Clarification Needed |
|------------|---------------------|
| "fast" | Specific latency target |
| "secure" | Which security aspects |
| "simple" | Compared to what |
| "good UX" | Specific behaviors |
| "scalable" | Expected load/growth |
| "flexible" | What kind of changes |

## Question Sequencing

### Natural Flow Order

1. Start broad (OPENER)
2. Follow user's thread (DRILL-DOWN)
3. Fill gaps (PROBE)
4. Resolve ambiguity (CLARIFY)
5. Define edges (BOUNDARY)
6. Handle conflicts (TRADE-OFF)
7. Test understanding (SCENARIO)
8. Confirm (VALIDATION)

### Adaptive Ordering

Adjust based on user's style:
- **Concise user**: More PROBE and SCENARIO questions
- **Verbose user**: More CLARIFY and VALIDATION questions
- **Technical user**: More DRILL-DOWN questions
- **Big-picture user**: More BOUNDARY and TRADE-OFF questions

## Question Templates by Domain

### Technical Features
```
OPENER: "What should [feature] do at a high level?"
DRILL-DOWN: "How should [sub-component] handle [specific case]?"
PROBE: "What about [related concern]?"
BOUNDARY: "Is [edge case] in scope?"
```

### User Experience
```
OPENER: "What should the user experience be like for [action]?"
DRILL-DOWN: "What happens after the user [action]?"
PROBE: "How should errors be presented to the user?"
SCENARIO: "Walk me through what a user sees when [scenario]"
```

### Data & Storage
```
OPENER: "What data needs to be stored for [feature]?"
DRILL-DOWN: "How long should [data type] be retained?"
PROBE: "Are there privacy considerations for this data?"
BOUNDARY: "Any data that explicitly should NOT be stored?"
```

### Integration
```
OPENER: "What external systems does this need to work with?"
DRILL-DOWN: "What does the [system] integration look like?"
PROBE: "What happens if [external system] is unavailable?"
BOUNDARY: "Are we responsible for [integration concern] or them?"
```
