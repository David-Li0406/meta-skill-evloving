# Tenet Module

Create custom Tenets for M20 Prism of Focus.

## What is a Tenet?

A Tenet is a specific belief that forms part of a mage's Paradigm. Unlike freeform paradigm descriptions, Tenets are discrete, mechanically-relevant beliefs that:

- Define what the mage believes about reality and magick
- Determine which Practices are Associated (-1 diff) or Limited (+1 diff)
- Constrain Arete advancement (Arete ≤ Tenet count until Arete 6)

## Tenet Categories

| Category | Question Answered | Required? |
|----------|-------------------|-----------|
| **Metaphysical** | Why does magick exist? | Yes |
| **Personal** | Why can YOU use magick? | Yes |
| **Ascension** | What is magick's ultimate purpose? | Yes |
| Social Role | What is your place in the world? | No |
| Epistemology | How do you gain knowledge? | No |
| Openness | How flexible is your worldview? | No |
| Afterlife | What happens after death? | No |

## Creating a Custom Tenet

### Step 1: Category and Core Belief

Choose a category and articulate the core belief in one clear sentence.

**Good Tenets are:**
- Specific enough to have mechanical implications
- Broad enough to apply across situations
- Believable as something a mage would stake their magick on

**Examples:**
- "Technology is humanity's path to transcendence" (Metaphysical)
- "My bloodline carries ancient power" (Personal)
- "Perfect order will bring perfect peace" (Ascension)

### Step 2: Associated Practices

Determine which Practices naturally align with this belief. These become Associated (-1 difficulty).

**Ask:** "If someone truly believed this, what methods would feel natural to them?"

A Tenet should have 2-5 Associated Practices. Too many dilutes meaning; too few limits usefulness.

### Step 3: Limited Practices

Determine which Practices conflict with or feel wrong to this belief. These become Limited (+1 difficulty).

**Ask:** "If someone truly believed this, what methods would feel alien or distasteful?"

A Tenet should have 1-4 Limited Practices. Not every Tenet needs to limit every opposing method.

### Step 4: Narrative Implications

Consider how this Tenet affects:
- How the mage describes their effects
- What they cannot easily accept or do
- Potential conflicts with other mages
- Growth and change over time

## Output Format

```markdown
## [Tenet Name]

**Category:** [Metaphysical/Personal/Ascension/etc.]

**Core Belief:** [One sentence statement]

**Description:** [2-3 sentences expanding on the belief and its implications]

### Associated Practices
- [Practice 1] — [Why it aligns]
- [Practice 2] — [Why it aligns]

### Limited Practices
- [Practice 1] — [Why it conflicts]
- [Practice 2] — [Why it conflicts]

### Narrative Notes
[How this Tenet affects roleplay, conflicts, growth]
```

## Example: Custom Tenet

```markdown
## The Code Underlies All

**Category:** Metaphysical

**Core Belief:** Reality is computation, and those who understand the code can rewrite it.

**Description:** The universe operates on fundamental rules no different from software. Matter, energy, even thought—all are data structures that can be accessed, read, and modified by those with the skill to interface with the cosmic operating system.

### Associated Practices
- Reality Hacking — Direct manipulation of reality's source code
- Hypertech — Advanced technology interfaces with the underlying systems
- Chaos Magick — Exploiting bugs and undefined behaviors in reality

### Limited Practices
- Faith — Belief in entities outside the system is illogical
- Shamanism — Spirits are subroutines, not partners
- Witchcraft — Organic traditions lack precision

### Narrative Notes
Mages with this Tenet often struggle with experiences that don't fit computational models—love, art, spiritual experiences. Growth may involve recognizing that some things transcend code, or doubling down on finding the algorithm for everything.
```

## Validation

- [ ] Category is appropriate for the belief
- [ ] Core belief is clear and specific
- [ ] 2-5 Associated Practices with reasoning
- [ ] 1-4 Limited Practices with reasoning
- [ ] Doesn't duplicate existing Tenets (check `lookup.py rules.tenets tenets`)
- [ ] Mechanically distinct from similar Tenets

## Reference

```bash
# View existing Tenets by category
python scripts/lookup.py rules.tenets tenets "metaphysical"
python scripts/lookup.py rules.tenets tenets "personal"
python scripts/lookup.py rules.tenets tenets "ascension"

# View Practices for association decisions
python scripts/lookup.py rules.practices practices --keys
```
