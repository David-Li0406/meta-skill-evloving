---
name: agent-evolution
description: Meta-skill for crystallizing tribal knowledge into systematic assets. Analyzes completed GUTTERS work to determine if new skills should be created or AGENTS.md updated. Use after complex tasks, module completions, or when patterns emerge.
---

# GUTTERS Knowledge Crystallization Protocol

Evolutionary mechanism for GUTTERS. Converts hard-won knowledge into reusable skills and documentation updates.

## Trigger Conditions

Activate when:
1. **User explicitly requests:** "Reflect", "Evolve", "Create skill from this"
2. **Module completed:** Any of the 18+ modules fully implemented and tested
3. **Complex task resolved:** Took 3+ iterations to solve correctly
4. **Pattern emerged:** Same context/explanation needed 3+ times
5. **Integration completed:** External API, calculation engine, or core system integrated

## Decision Matrix: Should This Become a Skill?

### ✅ CREATE SKILL When:
- **Repeatable pattern** across multiple modules (e.g., module implementation)
- **Domain expertise** required (Swiss Ephemeris, Human Design math, NOAA API)
- **Non-obvious gotchas** that caused errors (timezone handling, ephemeris ranges)
- **Complex workflow** with multiple steps (ARQ task setup, event bus integration)
- **External integration** with specific patterns (API rate limiting, caching strategies)

### ❌ DON'T CREATE SKILL When:
- One-time setup task
- Simple CRUD operations (already covered by FastCRUD)
- Generic Python/FastAPI patterns (agent already knows)
- Task won't be repeated
- Context is trivial to reload

## Skill Creation Protocol

### 1. Analyze Session

Review the completed work:
```
What was the task?
What challenges were encountered?
What specific knowledge was required?
What would have made this faster/easier?
What gotchas should future developers know?
```

### 2. Determine Skill Type

**Module Pattern Skill:**
- Example: `calculation-module-implementation`
- When: Creating calculation modules (astrology, numerology, etc.)
- Content: Specific calculation patterns, data structures, validation

**Integration Skill:**
- Example: `noaa-api-integration`, `swiss-ephemeris-usage`
- When: Integrating external services/libraries
- Content: API patterns, error handling, caching, rate limits

**Architecture Skill:**
- Example: `event-bus-patterns`, `active-memory-usage`
- When: Using GUTTERS core systems
- Content: How modules interact with event bus, memory cache

**Domain Knowledge Skill:**
- Example: `human-design-calculation`, `astrological-aspects`
- When: Complex domain calculations implemented
- Content: Mathematical formulas, data structures, edge cases

### 3. Draft Skill Structure
```markdown
---
name: [descriptive-name]
description: [When to use - be specific about triggers]. Use when [exact scenario].
---

# [Skill Title]

[2-3 sentence overview - what problem this solves]

## When to Use

- [Specific trigger 1]
- [Specific trigger 2]

## Pattern/Implementation

[Core implementation pattern - CODE EXAMPLES, not explanations]

## Gotchas

- [Specific error/issue and solution]
- [Non-obvious behavior to know]

## Critical Checklist

- [ ] [Verification step 1]
- [ ] [Verification step 2]

## References

See `references/[detailed-doc].md` for [additional context]
```

**Max length:** 200 lines in SKILL.md, move details to `references/`

### 4. Quality Gates

Before finalizing skill, verify:
- [ ] **Concise:** Main file under 200 lines
- [ ] **Actionable:** Code examples, not prose explanations
- [ ] **Specific:** Clear "when to use" triggers
- [ ] **Necessary:** Will actually improve future velocity
- [ ] **Tested:** Patterns are proven to work
- [ ] **GUTTERS-aligned:** Matches no-mocks, production-ready philosophy

### 5. File Structure
```
skills/[skill-name]/
├── SKILL.md                    # Main file (under 200 lines)
├── references/                 # Optional
│   ├── detailed-example.md     # Complete working code
│   └── edge-cases.md           # Known issues, solutions
└── scripts/                    # Optional
    └── helper.py               # Executable utilities
```

## AGENTS.md Update Protocol

### When to Update AGENTS.md

Update when:
- **Project structure changed** (new core system, major refactor)
- **Philosophy evolved** (new standards, changed patterns)
- **Common mistake identified** (needs to be in "NEVER" section)
- **New critical command** (essential development workflow)

### Update Format

**Present as diff, don't overwrite:**
```markdown
## Proposed AGENTS.md Update

**Section:** [Commands / Critical Rules / Module Development]

**Add to "[Section Name]":**
```
[New content block]
```

**Rationale:** [Why this addition improves development]

**Location:** After line [X] in current AGENTS.md

---
User must apply manually to prevent accidental overwrites.
```

## GUTTERS-Specific Skill Categories

### Priority 1: Module Types
- `calculation-module-implementation` ✅ (exists)
- `tracking-module-implementation` (for solar/lunar/transit modules)
- `intelligence-module-implementation` (for observer/hypothesis/synthesis)

### Priority 2: External Integrations
- `swiss-ephemeris-integration` (ephemeris calculations, edge cases)
- `noaa-api-integration` (space weather data fetching)
- `openrouter-integration` (AI model calls, prompt management)

### Priority 3: Core Systems
- `event-bus-usage` (publishing, subscribing, event patterns)
- `active-memory-patterns` (cache management, invalidation)
- `arq-background-jobs` (task scheduling, cron patterns)

### Priority 4: Domain Knowledge
- `astrological-calculations` (aspects, houses, transits)
- `human-design-math` (bodygraph calculation, gate mapping)
- `birth-time-refinement` (hypothesis generation, confidence scoring)

### Priority 5: Chat and Refinement
- `chat-architecture-patterns` (Master vs Branch logic, singleton UI presence)
- `cognitive-interface-standards` (how modules report "thinking" to the user)
- `genesis-refinement-dialogue` (patterns for gathering uncertain data via chat)
- `session-memory-synthesis` (linking chats to long-term user profiles)

## Execution Steps

1. **Analyze** completed work against decision matrix
2. **Determine** if skill creation justified
3. **Draft** skill following format (concise, actionable)
4. **Verify** against quality gates
5. **Present** to user with clear rationale
6. **Save** to `skills/[name]/SKILL.md`

## Output Format
```
📊 SESSION ANALYSIS
─────────────────────────────────────────────
Task: [What was completed]
Complexity: [Simple / Medium / Complex]
Iterations: [Number of attempts to get right]
Knowledge Domain: [Technical / Domain / Pattern]

🎯 SKILL RECOMMENDATION
─────────────────────────────────────────────
Status: [✅ CREATE SKILL / ❌ NOT NEEDED]

Reason: [Why this justifies a skill OR why it doesn't]

Proposed Skill:
- Name: [skill-name]
- Type: [Module / Integration / Architecture / Domain]
- Priority: [1-4]
- Saves: [Estimated time saved on future similar tasks]

📝 DRAFT SKILL CONTENT
─────────────────────────────────────────────
[Complete SKILL.md content if justified]

💾 NEXT STEPS
─────────────────────────────────────────────
1. Review draft above
2. Save to `skills/[name]/SKILL.md`
3. Reload window for agent to access
4. Test on next similar task
```

## Critical Reminders

- **Not every task needs a skill** - only repeatable, complex, or error-prone patterns
- **Conciseness matters** - if it's over 200 lines, use references/
- **Test-driven** - only create skills for proven patterns
- **Living document** - skills can be updated as we learn more

---

**This skill improves itself by learning when to create skills.**