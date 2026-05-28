# Workflow: Find The Turn

Discover and craft the central insight that makes your piece compelling.

## What is The Turn?

The Turn is the moment where conventional understanding is challenged by a surprising insight. It's what makes readers think "I never thought of it that way."

**Without The Turn**: Your piece is a summary—accurate but forgettable.
**With The Turn**: Your piece is an argument—memorable and shareable.

## Prerequisites

- Research completed (evidence.json populated)
- General topic and direction established
- Draft may or may not exist

## Steps

### 1. Identify the Conventional Wisdom

What would most people assume about your topic?

**Exercise**: Complete these sentences:
- "Everyone knows that..."
- "The standard view is..."
- "Most experts agree that..."
- "Common sense says..."

**Example for friction topic**:
- "Everyone knows that faster AI is better AI"
- "The standard view is that efficiency is paramount"
- "Common sense says friction is a bug to eliminate"

Write down 3-5 conventional wisdom statements.

### 2. Find the Contradiction

Look through your evidence for what contradicts, complicates, or inverts the conventional wisdom.

**Evidence scan questions**:
- What surprised me in the research?
- What contradicts the obvious take?
- What's true but counterintuitive?
- What do experts know that laypeople don't?
- What's the uncomfortable truth?

**Example findings**:
- Evidence shows friction IMPROVES decisions in high-stakes contexts
- The fastest systems are often the most fragile
- Slowing down can be a form of intelligence, not its absence

### 3. Articulate The Turn

Combine conventional wisdom + contradiction into a Turn:

**Template**:
```
[SETUP: Conventional wisdom]
[TURN: But/However/Yet + surprising insight]
[PROMISE: What this means for the reader]
```

**Example formulations**:

**Version A (Direct)**:
> We optimize AI for speed. But in critical domains, friction might be the only thing keeping us safe.

**Version B (Question)**:
> What if the relentless pursuit of AI efficiency is making our systems more fragile, not less?

**Version C (Paradox)**:
> The most intelligent AI systems may be the ones that know when to slow down.

**Version D (Stakes)**:
> Every AI speedup we celebrate may be one more safeguard we've removed.

### 4. Stress-Test The Turn

Ask:
- Is it genuinely surprising? (Not just "X is more complex than it seems")
- Is it defensible with evidence? (Can I back this up?)
- Is it consequential? (Does it matter if true?)
- Is it specific? (Not vague "complexity" or "tradeoffs")
- Would someone disagree? (If not, it's not a Turn)

**Red flags**:
- "It's complicated" - Too vague
- "Both sides have points" - Not a position
- "More research is needed" - Punt, not a Turn
- "X is important" - Not surprising

### 5. Find the Location

Where should The Turn appear?

**Option A: Paragraph 1-2 (Recommended)**
Hit them immediately. Reader knows what they're getting.

```markdown
[OPENING HOOK - surprising fact or question]
[SETUP - conventional wisdom, 1-2 sentences]
[THE TURN - "But..." or "Yet..."]
[PROMISE - what this piece delivers]
```

**Option B: End of Introduction**
Build to The Turn, then deliver it as the thesis.

**Option C: Delayed Reveal**
Risky but powerful. Setup a mystery, reveal The Turn later. Requires strong hooks to maintain attention.

### 6. Test Reader Experience

Imagine a reader encountering your opening:

| After Reading... | Reader Should Think... |
|------------------|------------------------|
| Sentence 1 | "Hm, interesting" |
| Setup | "Yeah, I assumed that" |
| The Turn | "Wait, really?" |
| Promise | "I need to know more" |

If The Turn doesn't create a "Wait, really?" moment, it's not sharp enough.

### 7. Refine the Language

The Turn should be:
- **Concise**: One sentence, maybe two
- **Clear**: No jargon or hedging
- **Concrete**: Specific, not abstract
- **Confident**: State it directly

**Before refinement**:
> "It may be the case that in certain high-stakes contexts, the introduction of various friction mechanisms could potentially lead to improved decision quality outcomes."

**After refinement**:
> "In critical decisions, friction improves accuracy."

### 8. Check Evidence Alignment

The Turn must be supported by your evidence:

- Which evidence items directly support The Turn?
- What's the confidence level?
- Are there strong counter-examples to address?

If The Turn outruns your evidence, either:
- Gather more evidence (→ RESEARCHER)
- Soften The Turn to match what you can prove

### 9. Document The Turn

Update `/workspace/outline.md`:

```yaml
the_turn:
  setup: "We optimize AI systems for speed, treating friction as a bug to eliminate."
  turn: "But in high-stakes decisions, friction isn't a bug—it's the only safeguard against automation-induced failure."
  promise: "This analysis reveals when to slow down, why it works, and how to design beneficial friction."
  location: "paragraph_2"
  supporting_evidence: ["ev_003", "ev_007", "ev_011"]
  confidence: "high"
  
  alternative_formulations:
    - "Speed kills. In AI systems, sometimes the smartest thing is to slow down."
    - "The paradox of AI efficiency: the faster we go, the more we miss."
```

---

## The Turn Patterns

Common patterns that work:

### The Paradox
"The [opposite of what you'd expect] is actually [true]"
> "The most efficient AI systems are the ones that deliberately slow down."

### The Hidden Cost
"Every [thing we value] comes with [unexpected downside]"
> "Every AI speedup we celebrate removes one more opportunity to catch errors."

### The Inversion
"[Conventional wisdom] gets it backwards"
> "We've been optimizing the wrong thing. It's not about faster—it's about smarter."

### The Overlooked Factor
"Everyone focuses on [X], but [Y] is what actually matters"
> "The debate over AI accuracy misses the point. The real question is resilience."

### The Historical Lesson
"We learned this lesson before with [analogous domain]"
> "Aviation figured this out decades ago. AI is repeating the same mistakes."

---

## When The Turn Won't Come

If you can't find The Turn:

1. **More research needed**: The surprise might be in evidence you haven't found yet
   → Return to RESEARCHER

2. **Wrong topic framing**: Maybe the interesting Turn is adjacent to your current focus
   → Try LATERAL/reframe workflow

3. **Genuinely no Turn**: Sometimes a topic is just straightforward
   → Write a clear explainer, not every piece needs a Turn
   
4. **Turn is obvious**: If the "surprising" insight is widely known, it's not a Turn
   → Go deeper, find the second-level insight
