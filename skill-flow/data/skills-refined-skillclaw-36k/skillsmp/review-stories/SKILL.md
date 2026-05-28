
name: review-stories
description: Review a story for potential issues. Use when asked to check a story for issues
---

# Story Review Workflow 

Review stories in `_lives/` through focused passes. Address all issues in each pass and edit the story to fix before moving on to the next pass.

---

## Pass 1: Timeline Mapping

Before anything else, map the life:

1. Write out the protagonist's age at: 0, 5, 10, 15, 20, 25, 30... until death
2. For each age bracket, note what's covered in the narrative
3. Flag gaps longer than 5 years with no content or bridge

**Test**: Is every period of the life either described or explicitly bridged ("The next decade passed quietly")?

Fix gaps before moving on to the next phase.

---

## Pass 2: Household Composition

For each household the protagonist lives in:

1. **Birth household**: List everyone who lives there. No "older kin" or "relatives"—name roles (grandmother, uncle) or names.
2. **Adult household** (if they marry/move): List everyone. Include in-laws if cohabiting.

**Test**: Could a reader draw a diagram of who sleeps under each roof?

**Common problems**:
- "crowded with children and relatives" → who specifically?
- In-laws mentioned at marriage, then vanish → do they die? Move? They need resolution.
- Protagonist moves "near his family" → who are these people? Do they ever appear?

Fix before moving on to the next phase.

---

## Pass 3: Sibling Introduction

1. List all siblings from debug data: name, alive/dead at protagonist's birth, relationship to protagonist
2. Categorize: died before protagonist knew them / alive during childhood / appear later
3. Check the narrative: are living siblings introduced as a group early, before individual deaths or conflicts?
4. Check the age gaps: are any of the siblings unrealistically older

**Test**: Does the reader know who's in the family before the family starts having problems?

**Common problems**:
- Dead-before-birth siblings mentioned with same weight as living ones (confusing)
- Siblings appearing from nowhere when plot-relevant
- Dense paragraph listing 8 siblings with birth years (unreadable)
- Sibling that is multiple decades older or younger with no explanation

Fix before moving on to the next phase.

---

## Pass 4: Character Tracking

List every named character. For each:
- First appearance (paragraph/age)
- Last appearance (paragraph/age)
- Gap between appearances

**Test**: 
 - Does any important character inexplicably disappear (eg, spouse, child, or parent)?
 - Are there large gaps in between appearances where it would be helpful to remind the read who someone is?
 - Are there characters that are named that only appear once and don't need a name

Fix before moving on to the next phase.

---

## Pass 5: Death Audit

For every death in the debug data during the protagonist's lifetime, fill out this table:

| Person | Relationship | Year | Mentioned? |  Purpose | Verdict |
|--------|--------------|------|------------|---------|---------|


**Purpose**: Does the death either (a) land emotionally, (b) change the protagonist's situation, or (c) reveal character?

**Verdict**: Keep as-is / Expand / Cut

For each "Expand" or "Cut" verdict, make the change before moving on to the next phase.

---

## Pass 6: Event Weight & Mechanism

For each significant event (affairs, violence, major decisions, major losses), do the following:
 - Answer: is this event plausible?
 - Answer: is this event interesting? does it add to the story
 - Write down a list of questions a curious reader would have about the event, the people involved, the logic, and the outcome
 - Are these questions answered? If not, add answers. This may involve inventing additional details

Fix all problems before moving on

---

## Pass 7: Paragraph Coherence

Read each paragraph asking:
- Does this paragraph have ONE theme?
- Should any events be split out?
- Should any events be bundled together?
- Is there random topic-jumping at the end?

**Common problems**:
- Death + unrelated event in same paragraph
- Paragraph about work that suddenly mentions a funeral
- Things "thrown in" at paragraph end

Fix before moving on to the next phase.

---

## Pass 8: Chronology & Time Markers

**Check for**:
- Time flowing forward (no unexplained jumps backward)
- Variety in time markers (not five "In [year]" openers in a row)
- Appropriate precision (don't say "mid-1990s" for a single specific event—pick a year)

**Hedging date detector**: Any of these constructions need fixing:
- "in X and Y" for one event → pick one
- "around Z" for a specific incident → pick a year
- "mid-1990s" for a single event → give the year

**Duplicate reference detector**: Year + age in same sentence is redundant:
- "In [year X], at [age Y]" → pick one
- If a paragraph repeats a year or date, improve or remove

Fix before moving on.


## Pass 9: Vague Language & Hedging

**Opening sentences:**
- Check paragraph openers for vague/filler phrases: "Deaths came early," "Life was hard," "Times were difficult," "Things changed"
- These signal the paragraph lacks a concrete anchor—rewrite or cut

**Work situations:**
- "What work was she doing and for whom?" should be answerable

**Hedging language:**
- "perhaps," "likely," "may have"—the narrator is omniscient, be confident

**LLM indecision:**
- "X or Y" constructions—pick one

**Sloppy placeholders:**
- "steady reference points," "the usual patterns"—what specifically?

Fix issues before moving on to the next phase.

---

## Pass 10: Abstract Claims

**Sentences claiming significance:**
- For any sentence that claims something "mattered," "changed things," or had importance, ask: is the mechanism explained?
- If the sentence says someone's presence or death "removed a shield" or "created a void," what did that person actually *do*?
- Either explain concretely or cut the empty claim

**Abstract metaphors (apply the deletion test):**
- For any metaphor or abstraction, ask: what is this actually pointing at?
- If you delete the sentence, does the reader lose concrete information?
- If no: cut it
- If yes: replace the abstraction with the concrete thing

Fix issues before moving on to the next phase.

---

## Pass 11: Anachronisms & Historical Grounding

Look for anachronisms and other historical errors:
- **Material culture:** Are objects, tools, crops, and animals appropriate to the era and region?
- **Political structures:** Are social structures and authority figures appropriate?
- **Culture:** Are languages, religions, and rituals, and social actions plausible for the person and social class.
- **Political Engagement** Are the political opinions of the person realistic, and do they engage in politics to a degree that fits with their status and personality?

**Opening paragraph specificity**:
- Does the opening orient the reader to the political/cultural situation?
- Could more concrete detail be added—specific historical rulers or kingdoms, events.
- How does where the person lives and their role fit into the world

Fix issues before moving on to the next phase.

---

## Pass 12: Jargon & Naming

**Pseudosociological jargon:**
- "kin" → "family" or name the specific people
- "stem family," "joint household," "patrilocal" → describe concretely who lives there
- "nuclear" → avoid; just describe the household

**Naming issues:**
- Same name used for different people (confusing)
- Siblings referred to as "Last First" when just "First" works
- If the names are mostly or entirely CVCV, this must be corrected---names need to show adequate diversity, even if the language family is unattested. Less than half the names can be of CVCV form.

Fix issues before moving on to the next phase.

---

## Pass 13: Figurative Language & AI-Slop

**Figurative language:**
- Metaphors, similes, poetic flourishes → rewrite as plain prose
- "beads that looked like water" → "blue glass beads"

**AI-slop phrases:**
- "rhythm of [X]," "settled into a pattern," "would prove to be"
- "shaped by," "marked by," "defined by" (when abstract)
- "Deaths came early," "Life was [adjective]," "Times were [adjective]"

Fix issues before moving on to the next phase.

---

## Pass 14: Final Read

Read the story once more as a reader would, and make a list of
- The 3 most confusing things
- The 3 most stilted or poorly flowing paragraphs
- The 3 places where it feels least real or most like a procedurally generated story.

Fix all of these


## Logging

After completing all passes, update the bottom of the story with a change-log structured as follows:

```markdown
**Issues found:**
- [Pass 3] "older kin" not specified in household description
- [Pass 5] Father's death mentioned but serves no narrative purpose
- [Pass 7] Penu conflict comes out of nowhere—no foreshadowing

**Changes made:**
- Specified household as parents plus paternal grandparents
- Connected father's death to protagonist's conscientiousness about stores
- Added earlier tension with Penu before the accusations