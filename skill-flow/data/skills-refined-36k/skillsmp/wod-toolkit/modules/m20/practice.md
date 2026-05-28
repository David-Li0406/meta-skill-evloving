# Practice Module

Create custom Practices for M20 Prism of Focus.

## What is a Practice?

A Practice is a methodology for performing magick—the "how" of a mage's Focus. Under Prism of Focus, Practices have:

- **Ratings (0-5+)** that cap what effect levels can be performed
- **Associated Abilities** used for rote dice pools
- **Common Instruments** typical tools for this method
- **Benefit** — situational advantage
- **Penalty** — situational disadvantage
- **Resonance Traits** — magical signature

## When to Create a Custom Practice

Create a new Practice when:
- An existing Practice doesn't capture a specific magical tradition
- A faction or culture has a distinctive approach not covered
- A character concept requires a unique methodology

**Don't create** when an existing Practice (or Specialized variant) already covers the concept.

## Creating a Custom Practice

### Step 1: Core Concept

Define the Practice in one sentence: what is this method of doing magick?

**Good Practices are:**
- Distinct from existing Practices
- Broad enough to cover multiple effects
- Tied to a coherent worldview or tradition

### Step 2: Description

Write 2-4 sentences explaining:
- The philosophy behind this method
- How practitioners view their magick
- What makes it distinct from similar Practices

### Step 3: Associated Abilities

Select 5-10 Abilities that practitioners commonly develop. These are used for rote dice pools.

**Consider:**
- What skills does this method require?
- What knowledge supports it?
- What physical or social abilities matter?

Mix Primary and Secondary Abilities. Reference `lookup.py character.abilities abilities`.

### Step 4: Common Instruments

List 5-10 typical tools, techniques, or foci. These should:
- Fit the Practice's philosophy
- Provide variety for different effects
- Feel authentic to the tradition

### Step 5: Benefit

Design ONE situational advantage. Benefits should:
- Apply in specific, definable circumstances
- Provide -1 or -2 difficulty, bonus dice, or a unique capability
- Not be universally applicable

**Patterns:**
- "[Situation] effects at -1 difficulty"
- "Bonus die when [condition]"
- "Can [unique capability] that others cannot"
- "Half cost for [specific thing]"

### Step 6: Penalty

Design ONE situational disadvantage. Penalties should:
- Apply in specific, definable circumstances
- Impose +1 or +2 difficulty, or a limitation
- Balance the Benefit

**Patterns:**
- "+1 difficulty when [situation]"
- "Cannot [specific action] without [condition]"
- "[Type of effect] always at +1 difficulty"

### Step 7: Resonance Traits

Select 5-10 Resonance traits that color magick performed with this Practice. These affect how the magick feels, looks, and lingers.

Reference `lookup.py rules.resonance-traits resonance-traits` or create appropriate new ones.

## Specialized Practices

To create a faction-specific variant of an existing Practice:

1. Choose the base Practice it derives from
2. Define the faction that uses it
3. Add ONE additional benefit (beyond the base Practice benefit)
4. Note that it counts as the base Practice for Sanctums/Reality Zones/Rituals

**Example:** Do (Akashayana) is a Specialized form of Martial Arts that additionally allows sensing others' chi.

## Corrupted Practices

For dark or tainted versions:

1. Choose the base Practice (or create new)
2. Define the corruption source (demons, Wyrm, Nephandi, etc.)
3. Add a significant benefit (usually -2 difficulty for something)
4. Add a corruption mechanic or escalating cost
5. Define what triggers corruption checks

## Output Format

```markdown
## [Practice Name]

**Base Practice:** [If Specialized/Corrupted, name the base]
**Faction:** [If Specialized, which faction]

### Description
[2-4 sentences on philosophy and approach]

### Associated Abilities
[List 5-10 abilities]

### Common Instruments
[List 5-10 instruments]

### Benefit
[One specific situational advantage]

### Penalty
[One specific situational disadvantage]

### Resonance Traits
[List 5-10 traits]

### Notes
[Any additional context, restrictions, or narrative considerations]
```

## Example: Custom Practice

```markdown
## Kinetic Meditation

### Description
Practitioners achieve magical states through sustained physical motion—running, swimming, cycling, repetitive labor. The body's rhythm entrains the mind, and exhaustion opens doors that stillness cannot. Unlike Martial Arts, this isn't about combat forms but about losing the self in motion.

### Associated Abilities
Athletics, Awareness, Crafts, Endurance, Meditation, Survival

### Common Instruments
- Repetitive motion (running, swimming, drumming)
- Breath control
- Mantras synchronized to movement
- Ritual exhaustion
- Dance (non-combat)
- Labyrinth walking

### Benefit
Effects cast after at least 10 minutes of sustained physical activity are at -1 difficulty. Extended rituals involving continuous motion gain +1 die per hour.

### Penalty
+1 difficulty to all effects when physically restrained or unable to move freely.

### Resonance Traits
Driven, Exhausting, Flowing, Hypnotic, Pulsing, Relentless, Rhythmic, Sweating

### Notes
Common among certain Ecstatics, some Dreamspeaker traditions, and independently Awakened athletes. Often combined with Invigoration or Crazy Wisdom.
```

## Validation

- [ ] Distinct from existing Practices
- [ ] Description explains philosophy and approach
- [ ] 5-10 Associated Abilities
- [ ] 5-10 Common Instruments
- [ ] Benefit is situational, not universal
- [ ] Penalty is meaningful, not trivial
- [ ] Benefit and Penalty are roughly balanced
- [ ] Resonance Traits fit the Practice's feel

## Reference

```bash
# View existing Practices
python scripts/lookup.py rules.practices practices --keys
python scripts/lookup.py rules.practices practices "Martial Arts"

# View Specialized/Corrupted variants
python scripts/lookup.py rules.practices practices "Do"
python scripts/lookup.py rules.practices practices "Goetia"

# View Abilities for associations
python scripts/lookup.py character.abilities abilities "talents"

# View Resonance traits
python scripts/lookup.py rules.resonance-traits resonance-traits "dynamic"
```
