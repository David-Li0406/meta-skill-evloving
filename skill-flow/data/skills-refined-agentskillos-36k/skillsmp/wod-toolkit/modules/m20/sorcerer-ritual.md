# Sorcerer Ritual Module

Create custom rituals for M20 Sorcerer hedge wizard Paths.

## Invoked By

This module is called when:
- Creating a **sorcerer PC** with Path rating 3+ (occasionally invent 1 custom ritual)
- Creating standalone rituals for campaign use
- Expanding existing Path's ritual library

When invoked from sorcerer character creation:
- Create ritual for Path where character has 3+ dots
- Ritual level must be ≤ (Path rating - 1)
- Include in-character origin (teacher, discovery, stolen)
- Link from character sheet

## Rituals vs Spells

| Aspect | Spells | Rituals |
|--------|--------|---------|
| **Time** | 1 turn per Path level | 10 minutes per ritual level |
| **Power** | Standard Aspects | Enhanced effects |
| **Preparation** | Minimal | Often require components |
| **Learning** | Automatic with Path | Must be learned individually |

## Ritual Benefits (Choose One)

### Option A: Path Level +1
Ritual allows effects as if Path were one level higher.

### Option B: Bonus Successes
Ritual grants **Path Ability rating** in bonus successes (only if base roll achieves at least 1 success).

### Option C: Unique Effect
Ritual accomplishes something beyond normal spell capabilities.

---

## Universal Ritual: Store Spell (•••••)

**All Paths** can learn this at level 5:

Store a single spell in an object for later release.
- Define release trigger (word, gesture, etc.)
- Anyone who knows trigger can release
- Only stores one spell at a time
- Does NOT count against Hanging Spell penalties

**Must be learned separately for each Path.**

---

## Creating New Rituals

### Requirements
- Path rating must exceed the ritual's level
- Creating Level 5 rituals usually requires story-level accomplishment

### In-Game Creation Process
1. Spend 1 month per ritual level doing research
2. Roll Casting Attribute + Path Ability at difficulty 9
3. **Botch**: Ritual backfires, start over
4. **Failure** or **1-2 Successes**: Try again next month
5. **3+ Successes**: Ritual created
6. **6+ Successes**: Ritual gains a bonus (lower level, shorter time, etc.)

---

## Ritual Design Process

### Step 1: Identify the Path
Which Path does this ritual belong to? Must fit within that Path's theme.

### Step 2: Determine the Effect
- Enhancement of existing capabilities? → Options A or B
- Unique specialized effect? → Option C

### Step 3: Set the Level

| Level | Power Guideline |
|-------|-----------------|
| • | Minor enhancement, utility |
| •• | Moderate utility, situational advantage |
| ••• | Significant power, combat-relevant |
| •••• | Major effect, supernatural-tier |
| ••••• | Legendary, story-changing |

### Step 4: Define Requirements (Optional)
- **Components**: Specific items needed
- **Timing**: Must be performed at certain times
- **Location**: Requires specific setting
- **Participants**: May need multiple casters
- **Sacrifice**: May require expenditure (Willpower, Quintessence)

---

## Ritual Template

```markdown
### [Ritual Name] (•-•••••)

**Path**: [Path name]
**Level**: [1-5]
**Casting Time**: [10 min × level, unless modified]

**Effect**: [What the ritual accomplishes]

**Requirements**: [Any special components, timing, etc.]

**Benefit Type**: [A: +1 Path level / B: Bonus successes / C: Unique effect]

**Notes**: [Flavor, practice variations]
```

---

## Sample Rituals by Path

### Conjuration

#### Object Permanence (••)
**Effect**: Create supernatural connection to an object  
**Benefit**: Object treated as "well-known" (-1 difficulty to conjure)  
**Duration**: 1 day per success  
**Limit**: Max bound objects = Conjuration rating

#### Always Armed (•••)
**Effect**: Pre-position weapon for instant summoning  
**Benefit**: Summon weapon by reaching into coat/shadow  
**Requirements**: Must hang ritual before danger  

#### Extraction (••••)
**Effect**: Pull fallen companions from combat to safety  
**Benefit**: Teleport up to 10 allies to caster's position  
**Requirements**: Caster must be out of combat range

### Conveyance

#### Safe Passage (••)
**Effect**: Create protected path through hazards  
**Duration**: 10 minutes per success  
**Benefit**: Those following path ignore environmental hazards

#### Anchor Point (••••)
**Effect**: Designate location as personal "anchor"  
**Duration**: Permanent until replaced  
**Benefit**: Can always Convey back regardless of distance  
**Limit**: Only one anchor at a time

### Divination

#### Trace the Thread (••)
**Effect**: Follow connection between linked things/people  
**Benefit**: Understand nature and strength of connections

#### Prophetic Dream (•••)
**Effect**: Receive vision of future events during sleep  
**Requirements**: Must sleep uninterrupted for 8 hours  
**Benefit**: Storyteller provides cryptic but useful information

### Fascination

#### Forget Me (••)
**Effect**: Remove memories of caster from target's mind  
**Duration**: Suppressed 1 day per success (permanent at 5+)

#### Geas (•••••)
**Effect**: Place binding compulsion on target  
**Duration**: Until task completed or 1 year  
**Resistance**: Willpower (diff 9) to resist  
**Notes**: Breaking geas causes 3 levels aggravated damage

### Fortune

#### Fortunate Encounter (••)
**Effect**: Ensure "chance" meeting with specific person  
**Duration**: Meeting occurs within 1 week  
**Requirements**: Must know target or have connection

#### Luck Shield (•••)
**Effect**: Ward against bad fortune  
**Duration**: 1 day per success  
**Benefit**: Reroll one failed roll per day

### Healing

#### Purification (••)
**Effect**: Remove toxins, diseases, possession influences  
**Benefit**: Each success removes 1 level of contamination

#### Regeneration (•••••)
**Effect**: Regrow lost limb or organ  
**Time**: 1 month of daily ritual sessions  
**Requirements**: Components from regenerative creature

### Summoning/Binding/Warding

#### Ward of Sanctuary (••)
**Effect**: Create protected space repelling specific being type  
**Duration**: 1 day per success  
**Area**: Room or enclosed space

#### Binding Circle (•••)
**Effect**: Create circle trapping summoned being  
**Duration**: Until broken or being escapes  
**Escape**: Being rolls Willpower (diff 6) vs caster's successes

---

## Greater Rituals

Combine multiple Paths for effects impossible alone.

### Requirements
- Multiple hedge wizards, each contributing one Path
- All participants share a Practice OR Path Ability
- One designated leader (highest Path)
- Time: 10 minutes per level + 10 minutes per additional caster

### Process
1. Each participant rolls their Path at appropriate difficulty
2. **ALL** participants must succeed
3. If all succeed, combined effect occurs
4. If any botch, all suffer consequences

### Example: Ward of True Sanctuary (Warding 3 + Fortune 3)
**Participants**: One with Warding 3+, one with Fortune 3+  
**Effect**: Protected space where bad fortune cannot enter (+2 diff to hostile actions, attackers lose 1 success)

---

## Validation Checklist

- [ ] Fits within parent Path's theme
- [ ] Level appropriate to effect power
- [ ] Benefit type specified (A, B, or C)
- [ ] Effect clearly defined mechanically
- [ ] Requirements listed (if any)
- [ ] Does not duplicate existing rituals
- [ ] Does not exceed Path's capabilities at that level
- [ ] Casting time follows standard unless justified
