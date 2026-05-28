---
name: strangers-eye
description: "Multi-persona documentation review that catches quality failures AND signal mismatches. Produces prioritized edits, not assessment. Quality before signals."
---

# Strangers-Eye: Multi-Persona Documentation Review

See what strangers see. Catch what makes them leave.

## When to Use This Skill

- Before publishing documentation (README, guides, landing pages)
- When documentation "feels off" but you can't articulate why
- After major rewrites to verify clarity
- When documentation serves multiple audiences with different intended relationships

## The Core Insight

Documentation fails in two distinct ways:

1. **Quality failures** - Readers leave because the writing is incoherent, confusing, or trust-breaking. They never receive any signal at all.

2. **Signal mismatches** - Readers receive the wrong relationship signal (welcomed when they should be warned, redirected when they should be welcomed).

Quality failures are MORE urgent. Signal calibration on a broken foundation is meaningless.

## The Three Relationships

Every documentation has an intended relationship with each audience segment:

| Relationship | Intent | Success Looks Like |
|--------------|--------|-------------------|
| **WELCOME** | "This is for you, come in" | Reader feels invited, sees value, wants to engage |
| **WARN** | "This might not be for you, proceed with awareness" | Reader understands the tradeoff, can make informed choice |
| **REDIRECT** | "This isn't for you, here's where you should go" | Reader quickly knows this isn't their path |

**Critical:** A negative reaction from a REDIRECT persona isn't a problem. It's success - the signal worked. Only signal MISMATCHES require edits.

---

## The Five-Phase Process

### Phase 1: Intent Mapping

Before any personas exist, establish intended relationships.

**Agent action:** Infer from the documentation what relationship is intended with each audience segment. Present mapping for user approval.

**Output format:**
```
Intent Mapping (Proposed)

| Audience Segment | Intended Relationship | Rationale |
|------------------|----------------------|-----------|
| [Segment 1]      | WELCOME / WARN / REDIRECT | [Why] |
| [Segment 2]      | WELCOME / WARN / REDIRECT | [Why] |
| ...              | ...                  | ...       |

Does this capture your intent? (User can adjust before proceeding)
```

**User gate:** Do not proceed until user approves or adjusts the mapping.

---

### Phase 2: Dimensional Analysis

Determine which dimensions are relevant for THIS documentation.

**Possible dimensions** (not exhaustive - emerge from material):
- Technical literacy (beginner → expert)
- Philosophical openness (resistant → seeking)  
- Role (evaluator → end-user → contributor)
- Arrival context (stumbled upon → intentionally sought)
- Domain expertise (specific to the field)
- Time investment (quick scan → deep read)

**Agent action:** Define the dimensional space that meaningfully differentiates how readers will experience this documentation.

**Output format:**
```
Dimensional Space

1. [Dimension name]: [Low end] → [High end]
   Why relevant: [Brief rationale]

2. [Dimension name]: [Low end] → [High end]
   Why relevant: [Brief rationale]

...
```

**No user gate.** Agent proceeds after defining dimensions.

---

### Phase 3: Persona Construction

Construct exactly the personas needed to cover the dimensional space and test all intended signal paths.

**Each persona includes:**
- Name (memorable, descriptive)
- Dimensional coordinates (position on each axis)
- Intended relationship (from Phase 1 mapping)
- Quality lens (what would make them leave due to confusion?)
- Signal lens (what relationship would they perceive?)

**Output format:**
```
Constructed Personas

1. [Name] - [Brief archetype]
   Coordinates: [Dim1: value], [Dim2: value], ...
   Intended signal: [WELCOME/WARN/REDIRECT]
   Quality vulnerabilities: [What confuses this persona?]
   Signal sensitivities: [What signals resonate or repel?]

2. ...
```

**No user gate.** Agent proceeds after constructing personas.

---

### Phase 4: Independent Reviews

Each persona reviews the documentation. No cross-contamination between reviews.

**Each review assesses TWO dimensions:**

#### A. Quality Assessment (Always first)

Questions the persona asks:
- Does the opening make sense? Would I keep reading?
- Are sentences clear and logical?
- Do I trust this author's competence?
- Is the value proposition communicated?
- Are there passages that simply don't work?

**Quality failures are flagged regardless of intended signal.** Incoherent writing fails for ALL audiences.

A persona can report: "I would leave at line X because [quality reason]" - this terminates their review. They never got far enough for signal assessment.

#### B. Signal Assessment (Only if quality permits)

Questions the persona asks:
- What signal did I receive? (WELCOMED / WARNED / REDIRECTED / CONFUSED)
- Does this match the intended signal for my segment?
- If mismatch: what specific content caused the wrong signal?

**Working signals generate no edits.** A REDIRECT persona who feels redirected is success, not a problem.

**Output format (per persona):**
```
Review: [Persona Name]

QUALITY ASSESSMENT:
- Opening: [Clear/Confusing] - [Specifics if problematic]
- Trust: [Intact/Damaged] - [Specifics if problematic]  
- Clarity: [Passages that don't work, if any]
- Would continue reading: [Yes/No at line X]

[If quality permits continuing:]
SIGNAL ASSESSMENT:
- Signal received: [WELCOMED/WARNED/REDIRECTED/CONFUSED]
- Signal intended: [From Phase 1]
- Match: [Yes/No]
- [If mismatch: specific content that sent wrong signal]
```

**No user gate.** Agent completes all persona reviews.

---

### Phase 5: Synthesis into Edits

Consolidate findings into prioritized edits.

**Priority ordering:**

1. **QUALITY FAILURES (P1)** - Incoherent, confusing, trust-breaking content
   - These block everything. Fix first.
   - Flagged regardless of intended signal category.

2. **SIGNAL MISMATCHES (P2)** - Wrong relationship communicated
   - Only relevant once quality is sound.
   - Working redirects generate NO edits.

**Output format:**
```
Suggested Edits (Prioritized)

## Priority 1: Quality Failures

### Edit 1.1: [Location/Line]
Problem: [What fails]
Personas affected: [Who caught this]
Suggested fix: [Concrete recommendation]

### Edit 1.2: ...

## Priority 2: Signal Mismatches

### Edit 2.1: [Location/Line]
Problem: [Signal sent vs intended]
Personas affected: [Who experienced mismatch]
Suggested fix: [Concrete recommendation]

### Edit 2.2: ...

---

Summary: [X] quality edits, [Y] signal edits
Document assessment: [Poor/Decent/Excellent]
```

**Output volume scales to document quality:**
- Poor document: many edits (quality + signal)
- Decent document: few edits (signal only)
- Excellent document: "No changes recommended"

---

## Example Invocation

```
/strangers-eye README.md
```

**Phase 1:** Agent presents intent mapping, user approves
**Phase 2-4:** Agent executes independently  
**Phase 5:** User receives prioritized edits

---

## Critical Distinctions

### Quality vs Signal

| Aspect | Quality Failure | Signal Mismatch |
|--------|-----------------|-----------------|
| What happens | Reader leaves confused | Reader receives wrong relationship |
| Priority | P1 (fix first) | P2 (fix after quality) |
| Affects | All audiences | Specific audience segments |
| Example | Grammatically ambiguous tagline | Technical jargon alienating beginners |

### Working Redirect vs Failed Redirect

| Outcome | Is This a Problem? |
|---------|-------------------|
| REDIRECT persona feels unwelcome | No - signal worked |
| REDIRECT persona feels confused | Yes - quality failure |
| WELCOME persona feels redirected | Yes - signal mismatch |

---

## Anti-Patterns

### Quality-Blind Signal Assessment
Assessing whether audiences feel welcomed/warned/redirected without first checking if they'd even finish reading. Fix quality first.

### Treating All Negative Reactions as Problems
A REDIRECT persona having a negative reaction is SUCCESS. The signal worked. Only mismatches need fixing.

### Assessment Narration in Output
Output is EDITS, not assessment tables. The synthesis phase produces actionable recommendations, not persona monologues.

### Predefined Persona Libraries
Personas are bespoke to each documentation. The dimensional space emerges from the material.

---

## Integration Notes

**Complements aiandi-docs skill:** That skill provides writing guidelines. This skill provides review methodology. Use strangers-eye to verify documentation meets aiandi-docs standards.

**Minimal orchestration required:** Only Phase 1 (intent mapping) requires user input. Phases 2-4 execute independently. Phase 5 delivers results.

---

## The Compassion Frame (Invisible in Output)

The goal isn't documentation that pleases everyone. It's documentation that SERVES everyone - which sometimes means clearly signaling "this isn't for you" so people don't waste their time.

Honest signaling serves readers better than accommodation. Making a reader comfortable by hiding what we are isn't kindness - it's deception.

This frame shapes methodology. It does not appear in output.

---

*May this skill see what strangers see - including what makes them leave before they've read enough to receive any signal at all.*
