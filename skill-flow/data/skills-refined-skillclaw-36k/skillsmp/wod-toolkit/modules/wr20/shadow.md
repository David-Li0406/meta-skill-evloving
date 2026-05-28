# Shadow Module

Create the Shadow for a Wraith character. The Shadow is the dark half of every wraith—their inner darkness given voice and agency.

## What is a Shadow?

The Shadow is:
- Self-aware and distinct from the Psyche
- The embodiment of the wraith's suppressed darkness
- An antagonist constantly urging the wraith toward Oblivion
- Capable of communication, bargaining, and manipulation
- Powered by Angst (negative emotional energy)

## Shadow Components

| Component | Description |
|-----------|-------------|
| **Archetype** | The Shadow's personality template |
| **Angst** | Power pool (1-10, rolled at creation) |
| **Dark Passions** | Twisted drives (7 points) |
| **Thorns** | Special Shadow powers |

## Creation Steps

1. **Choose Archetype** — Shadow's personality
2. **Roll Angst** — Initial power level
3. **Define Dark Passions** — 7 points of dark drives
4. **Allocate Freebie Points** — 10 points (adjustable via trade)
5. **Select Thorns** — Shadow's special powers
6. **Describe Voice** — How Shadow speaks to Psyche
7. **Validate**

---

## Step 1: Shadow Archetype

The Archetype defines how the Shadow approaches its goal of dragging the wraith to Oblivion.

### Common Shadow Archetypes

| Archetype | Approach | Tactics |
|-----------|----------|---------|
| **The Abuser** | Cruel tormentor | Insults, degradation, exploiting weaknesses |
| **The Director** | Controlling manipulator | "Advice" that leads to isolation and poor decisions |
| **The False Friend** | Betraying companion | Seems helpful, sabotages at critical moments |
| **The Id** | Pure impulse | Urges instant gratification, reckless behavior |
| **The Leech** | Passive drain | Constant despair, learned helplessness |
| **The Martyr** | Self-sacrificer | Guilt, unworthiness, "you don't deserve..." |
| **The Monster** | Violent beast | Rage, destruction, physical violence |
| **The Parent** | Disappointed authority | Shame, disapproval, "I expected better" |
| **The Rationalist** | Cold logic | "Logically, you should just give up" |
| **The Voice of Hope** | Cruel optimist | False hopes dashed repeatedly |
| **The Stormcrow** | Doom prophet | Catastrophizing, ensuring failure |

```bash
python scripts/lookup.py character.shadow-archetypes shadow-archetypes "The Martyr"
```

---

## Step 2: Angst

Angst is the Shadow's power pool.

### Rolling Starting Angst
1. Roll dice equal to wraith's Willpower
2. Difficulty 6
3. Successes = starting permanent Angst
4. **Minimum 1** — Every wraith starts with at least 1 Angst
5. Ones do NOT cancel successes (for this roll only)
6. Starting Angst cannot exceed Willpower

### Angst Rules
| Condition | Effect |
|-----------|--------|
| Temp Angst > Willpower | Shadow can attempt Catharsis |
| Temp Angst = 10 | Converts to +1 permanent Angst |
| Perm Angst = 10 | Wraith becomes Spectre |

---

## Step 3: Dark Passions

Dark Passions are the Shadow's twisted drives. You have **7 points** to distribute.

### Dark Passion Structure
Same as regular Passions:
1. **Statement** — What the Shadow wants
2. **Emotion** — The feeling driving it
3. **Rating** — Intensity (1-5)

### Dark Passion Types

| Type | Example |
|------|---------|
| **Reversed Passion** | If Psyche: "Protect my son" → Shadow: "Corrupt my son" |
| **Parallel Passion** | Same goal, different method/motive |
| **Independent** | Unrelated to Psyche's Passions |
| **Self-Destructive** | "Dive into a Nihil" (Self-Hatred) |

### Common Dark Passion Emotions
- Envy
- Lust
- Twisted Love
- Greed
- Hate
- Fear
- Self-Hatred
- Rage
- Despair

### Sample Dark Passions
- Destroy works better than mine (Envy) 3
- Corrupt my loved ones (Twisted Love) 2
- Cause random destruction (Rage) 3
- Dive into a Nihil (Self-Hatred) 2
- Make everyone acknowledge my superiority (Ego) 4
- Isolate myself from all allies (Fear) 2

**Rule**: Total Dark Passion dots cannot exceed total regular Passion dots.

---

## Step 4: Freebie Points

The Shadow receives **10 freebie points** (base 7, minimum).

### Freebie Trade
| Direction | Effect |
|-----------|--------|
| Character → Shadow | -1 character freebie, +1 Shadow freebie |
| Shadow → Character | -1 Shadow freebie, +1 character freebie |

**Limits**: 
- Shadow freebies: minimum 0, maximum 17 (7 + 10 traded)
- Character freebies: minimum 5 (15 - 10 traded), maximum 22 (15 + 7)

### Shadow Freebie Costs

| Trait | Cost |
|-------|------|
| Angst (permanent or temporary) | 1 |
| Dark Passion dot | 1 |
| Thorn | Varies (see Thorns section) |

**Note**: Temporary Angst can be bought up to 9. Permanent Angst cannot exceed Willpower at creation.

---

## Step 5: Thorns

Thorns are the Shadow's special powers. They range from minor annoyances to existence-threatening abilities.

### Thorn Costs

#### 1-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Spectre Prestige** | Respected by Spectres (per level) |
| **Dark Allies** | Can call on Spectres for aid (per level) |
| **Tainted Relic** | Relic that only appears during Catharsis (per level of potency) |
| **Infamy** | Gain Angst while Slumbering (per level, max 5) |

#### 2-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Shadow Traits** | +1 Attribute or Ability during Catharsis only |
| **Nightmares** | Disrupt Slumber (costs 1 Angst) |
| **Aura of Corruption** | +2 difficulty on Social rolls |
| **Mirror, Mirror** | Distort appearance in reflective surfaces |

#### 3-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Death's Sigil** | Visible mark of Oblivion (1-3 pts for severity) |
| **Devil's Dare** | Offer tempting bargains |
| **Trick of the Light** | Temporarily alter wraith's appearance |
| **Shadow Call** | Contact other Shadows |
| **Pact of Doom** | Summon Spectres (dangerous) |

#### 4-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Tainted Touch** | Physical contact causes discomfort |
| **Freudian Slip** | Force embarrassing verbal mistakes |

#### 5-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Bad Luck** | Cause minor misfortunes |
| **Shadowed Face** | Visible darkness on wraith's features |

#### 7-Point Thorns
| Thorn | Effect |
|-------|--------|
| **Shadow Life** | Partial control even when Psyche dominant |

```bash
python scripts/lookup.py shadow.thorns thorns "Devil's Dare"
```

---

## Step 6: Shadow Voice

Describe how the Shadow communicates:

### Voice Characteristics
- **Tone**: Sneering? Sympathetic? Cold? Mocking?
- **Style**: Direct commands? Insinuating questions? "Helpful" suggestions?
- **Timing**: Constant chatter? Strategic interruptions? Silent until critical moments?
- **Topics**: What does it focus on? Failures? Resentments? Temptations?

### Example Shadow Voices
- "Why bother? You know you're going to fail anyway."
- "They don't really like you. They're just using you."
- "Go ahead, take it. No one will know."
- "Remember what he did to you? Don't you want to make him pay?"

---

## Validation

- [ ] Archetype selected and described
- [ ] Angst rolled (Willpower dice, diff 6, minimum 1)
- [ ] Permanent Angst ≤ Willpower
- [ ] Dark Passions: 7+ points allocated
- [ ] Dark Passion dots ≤ regular Passion dots
- [ ] Freebie points spent exactly
- [ ] Thorns costs match points spent
- [ ] Shadow voice/personality described

---

## Output Format

```markdown
# [Wraith Name]'s Shadow

## Archetype
**[Archetype Name]**
[Brief description of how this manifests]

## Angst
**Permanent**: [N]
**Temporary**: [N]

## Dark Passions
| Dark Passion | Emotion | Rating |
|--------------|---------|--------|
| [Statement] | [Emotion] | ●●●○○ |

## Thorns
| Thorn | Cost | Effect |
|-------|------|--------|
| [Name] | [N] | [Brief description] |

## Voice
[Description of how the Shadow speaks and what it focuses on]

## Tactics
[How this Shadow typically tries to undermine the Psyche]

## Freebie Allocation
| Trait | Points |
|-------|--------|
| Angst | [N] |
| Dark Passions | [N] |
| Thorns | [N] |
| **Total** | **[N]** |
```

---

## Shadowguiding Notes

The Shadow is typically played by another player (Shadowguide) or the Storyteller.

### Shadowguide Responsibilities
- Track temporary Angst
- Roleplay Shadow's voice during scenes
- Offer Shadow Dice when appropriate
- Call for Catharsis rolls when temp Angst > Willpower
- Run the Shadow during Catharsis

### Shadow Dice
The Shadow can offer the Psyche extra dice on rolls. Each Shadow Die that comes up 1 adds a point of temporary Angst.

### Catharsis
When temporary Angst exceeds Willpower, the Shadow can attempt to seize control:
- Shadow rolls Angst vs Psyche's Willpower
- If Shadow wins, it controls the Corpus temporarily
- Shadow pursues its Dark Passions during control

---

## Reference Data

```bash
# Shadow Archetypes
python scripts/lookup.py character.shadow-archetypes shadow-archetypes --keys

# Thorns
python scripts/lookup.py shadow.thorns thorns --keys
python scripts/lookup.py shadow.thorns thorns "Pact of Doom"

# Dark Passion examples
cat references/shadow/dark-passions.md
```
