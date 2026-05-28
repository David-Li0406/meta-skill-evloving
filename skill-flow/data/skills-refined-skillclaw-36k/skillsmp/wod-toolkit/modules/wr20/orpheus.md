# Orpheus Projector Module

Create mechanically valid Orpheus Group projector characters for W20.

## What is a Projector?

A projector is a living human who can separate their soul from their body and walk among the dead. Through near-death experiences (NDEs), drugs, and/or cryogenic technology, the Orpheus Group has learned to eject agents' souls into the Shadowlands.

**Key Differences from Wraiths**:
- Still alive (body exists in the Skinlands)
- No Shadow—instead have **Stains**
- **Tethers** instead of Fetters (self-repairing)
- Can return to their body
- **Shades** determine personality and Arcanoi preferences
- **Laments** define projection method (Skimmer vs Sleeper)

---

## Projector vs Wraith vs Hue

| Aspect | Projector | Wraith | Hue |
|--------|-----------|--------|-----|
| Status | Living | Dead | Dead (pigment user) |
| Form | Pseudo-wraith | Wraith | Faded wraith |
| Shadow | None (has Stains) | Active antagonist | Quiescent |
| Anchors | Tethers (self-repair) | Fetters | Fetters |
| Return | Can return to body | N/A | N/A |
| Pathos | Limited | Full | Reduced (max 7) |

---

## Laments: Skimmer vs Sleeper

### Skimmer
Projects through drugs and yogic meditation techniques.

| Advantage | Disadvantage |
|-----------|--------------|
| Regenerates 1 Pathos/hour in body | Damage transfers to body (halved, bashing) |
| Can "ripcord" back instantly | Must spend 1 Pathos/hour projecting |
| Projects in one turn (with Meditation) | Limited to Shadowlands (no deep Tempest) |
| Quick access | No wound penalties until return |

### Sleeper
Projects through cryogenic suspension (flatlining).

| Advantage | Disadvantage |
|-----------|--------------|
| No Pathos cost to project | 5 hours to enter/exit suspension |
| Can shunt Angst to body (1 Angst = 1 bashing) | Cannot recover Pathos while frozen |
| No damage transfer | Body completely vulnerable |
| Can venture deeper into Underworld | Complex equipment required |

---

## Creation Steps

### Standard Character Creation
1. **Concept** — Name, background, why Orpheus recruited them
2. **Near-Death Experiences** — At least 3-4 significant NDEs
3. **Lament** — Skimmer or Sleeper
4. **Shade** — Personality template (determines Arcanoi)
5. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
6. **Attributes** — 7/5/3 across Physical/Social/Mental
7. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)

### Projector-Specific Steps
8. **Backgrounds** — 7 dots (includes Orpheus-specific)
9. **Arcanoi** — 1 Shade Arcanos + 1 Embody + 1 Lifeweb + 2 free
10. **Passions** — 5 dots
11. **Tethers** — 10 dots (5 MUST be on physical body)
12. **Stains** — Based on permanent Angst (1 per 2 dots)
13. **Shade Modifiers** — Apply Pathos/Willpower/Angst adjustments
14. **Freebies** — 18 points
15. **Derived** — Pathos 5, Willpower 5, Angst 5 (+ Shade modifiers)

---

## The Seven Shades

Shades determine a projector's psychological makeup and Arcanoi affinity.

| Shade | Favored Arcanoi | Prohibited | Pathos | Will | Angst |
|-------|-----------------|------------|--------|------|-------|
| Banshee | Keening, Fatalism | Outrage | +0 | +1 | -1 |
| Haunter | Inhabit, Flux | Keening | +1 | +1 | +0 |
| Poltergeist | Outrage, Keening | Fascinate | +1 | +2 | +1 |
| Skinrider | Puppetry, Lifeweb | Moliate | +0 | +3 | +1 |
| Wisp | Fascinate, Argos | Puppetry | +1 | +0 | -1 |
| Phantasm | Phantasm, Pandemonium | Inhabit | +2 | +1 | +1 |
| Marrow | Moliate, Embody | Phantasm | +3 | +0 | +1 |

### Shade Descriptions

**Banshee**: Introspective empaths with natural insight. Slow to act but see all sides.
- Suggested Natures: Caregiver, Martyr, Mediator, Optimist, Penitent

**Haunter**: Adaptable souls who make themselves at home anywhere.
- Suggested Natures: Deviant, Explorer, Rebel, Rogue, Survivor

**Poltergeist**: Passionate, wrathful souls who master their fury.
- Suggested Natures: Activist, Bravo, Critic, Eye of the Storm, Pragmatist

**Skinrider**: Strong sense of self, revel in control.
- Suggested Natures: Bureaucrat, Competitor, Leader, Pedagogue, Traditionalist

**Wisp**: Subtle and charming, prefer indirect action.
- Suggested Natures: Bon Vivant, Child, Conniver, Jester

**Phantasm**: Dreamers who share their vision with others.
- Suggested Natures: Architect, Avant-Garde, Gambler, Visionary

**Marrow**: Social chameleons who reinvent themselves.
- Suggested Natures: Enigma, Fanatic, Follower, Scientist

### Shade Abilities

**Misery Loves Company**: Spend 1 Pathos to gain +1 die on Social rolls with wraiths of your Nature group.

**Sense the Strands**: -1 difficulty on Lifeweb rolls vs. same Nature group, -2 vs. same Nature.

---

## Crucibles

Orpheus trains projectors in tight-knit groups called **crucibles**.

### Crucible Benefits
- Share Pathos by touch
- **Yoking**: Link with another to augment Arcanoi (1 Pathos)

### Yoking by Shade
| Shade | Benefit |
|-------|---------|
| Banshee | Lower Arcanos difficulty by 2 (one turn) |
| Haunter | Double duration of Arcanos |
| Marrow | Act as nexus—pass two Benefits to one recipient |
| Poltergeist | +3 damage dice to next Arcanos attack |
| Phantasm | +2 difficulty to resist Arcanos (or +1 success) |
| Skinrider | +2 dice to Physical Attribute roll for Arcanos |
| Wisp | Reroll two failed dice on Arcanos roll |

---

## Stains

Projectors have no Shadow. Instead, Angst manifests as **Stains**—visible mutations of the Corpus.

### Gaining Stains
- 1 Stain per 2 dots of permanent Angst
- At Angst 6+, one Stain becomes permanent

### Manifesting Stains
- Cost: 1 temporary Angst
- Duration: Permanent Angst in turns
- When temp Angst > Willpower: All Stains manifest uncontrollably

### Social Impact
Each manifested Stain:
- +1 difficulty on Social rolls with wraiths
- -1 difficulty on Social rolls with Spectres

### Sample Stains

| Stain | Advantage | Disadvantage |
|-------|-----------|--------------|
| Adder's Scales | -1 difficulty to escape/athletics, +1 soak | Must roll Will (diff 6) when startled or lash out |
| Armor of Corpulence | Immune to bashing, 1/4 lethal from weapons | +2 difficulty to movement, max 3 yards/turn |
| Barbed Corpus | +1 soak, 1L damage to unarmed attackers | Will roll or accidentally harm allies/objects |
| Brutish | +1 soak, +3 Strength dice | -5 initiative, halved movement, -1 Int/App |
| Chameleon Skin | +3 Stealth dice | +1 Social difficulty (body language unclear) |
| Compound Eye | 360-degree vision | +2 difficulty to ranged combat/distance |
| Corpus Cilia | -1 Perception difficulty, ignore vision impairment | +1 Wits difficulty, -4 in Maelstroms |
| Dark Speech | Ranged Brawl attack (Str+2L, 7ft) | Will roll (diff 7) to speak without insults |
| Gossamer Webs | Trap opponents (2 Str binding per Corpus spent) | Lose Corpus passing through Skinlands objects |
| Hammer Fists | +3 bashing damage unarmed | +3 difficulty on manual dexterity tasks |
| Spider's Bristles | Climb sheer surfaces | +1 difficulty on delicate touch tasks |
| Spite-fueled Arcanoi | +2 dice to Arcanoi rolls | Arcanoi gain dark side effects |

---

## Projector Abilities

### Default Abilities
When projecting, projectors gain:
- Deathsight
- Lifesight
- Sharpened Senses
- Insubstantiality

### Dead-Eyes
After first projection, can activate Lifesight/Deathsight in the meat:
- **Roll**: Perception + Awareness (difficulty 7)
- **Duration**: One scene
- Permanently immune to the Fog

### Vitality
Pathos cannot exceed current Corpus rating.
- Spending 1 Willpower grants 3 Pathos immediately
- Excess Pathos must be spent on Corpus restoration

### Emblem of Protection
- **Cost**: 2 Pathos
- **Effect**: Armor (4B/2L/1A), downgrades Maelstrom damage by one Bell
- **Extra Cost**: +1 Pathos for electrical aura (1L to grapplers)
- **Duration**: One scene

---

## Orpheus-Specific Backgrounds

### Destiny (1-5)
Touched by fate. Reroll dice (one per dot, per session).

| Rating | Effect |
|--------|--------|
| 1 | 1 reroll/session |
| 2 | 2 rerolls/session |
| 3 | 3 rerolls/session (visible to Fatalism) |
| 4 | 4 rerolls/session |
| 5 | 5 rerolls/session (major fate portent) |

### Gauze Relic (1-5)
Manifest personal items from your Corpus.

| Rating | Effect |
|--------|--------|
| 1 | Small item (knife) |
| 2 | Handgun-sized, +1 Ability bonus |
| 3 | Electronic functions, -2 difficulty to one Ability |
| 4 | Complex mechanical/electrical (motorcycle) |
| 5 | +4 Ability or +1 Attribute bonus |

- **Cost**: 1 Pathos, lasts one scene
- If destroyed: 1 Willpower + 1 Aggravated damage

### Reincarnate (1-5)
Access skills from past lives.

| Rating | Effect |
|--------|--------|
| 1-5 | Free dice pool = rating, supplement existing rolls or use Abilities you don't have |

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 7 |
| Arcanoi | 5 (1 Shade + 1 Embody + 1 Lifeweb + 2 free) |
| Passions | 5 |
| Tethers | 10 (5 on body) |
| Pathos | 5 + Shade modifier |
| Willpower | 5 + Shade modifier |
| Angst | 5 + Shade modifier |
| Freebies | 18 |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Arcanos (Favored) | 4 |
| Arcanos (Standard) | 5 |
| Arcanos (Prohibited) | 6 |
| Willpower | 2 |
| Passion | 2 |
| Background | 1 |
| Tether | 1 |
| Pathos | 1 per 2 dots |

---

## Validation

- [ ] Lament chosen (Skimmer or Sleeper)
- [ ] Shade chosen, modifiers applied
- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 7 dots
- [ ] Arcanoi: 5 dots (includes required Embody, Lifeweb, Shade Arcanos)
- [ ] Passions: 5 dots
- [ ] Tethers: 10 dots (5 on body)
- [ ] Stains: 1 per 2 permanent Angst
- [ ] Pathos: 5 + Shade modifier
- [ ] Willpower: 5 + Shade modifier
- [ ] Angst: 5 + Shade modifier
- [ ] Freebies: 18 spent exactly
- [ ] NDEs described (3-4 minimum)
- [ ] Crucible affiliation (if applicable)

---

## Hue Character Creation

Hues are wraiths who used pigment in life—faded, colorless ghosts.

### Differences from Standard Wraith
- Appear drained of color
- **Quiescent Shadow** (rarely speaks)
- Reduced Backgrounds and Fetters
- Can manifest Stains like projectors
- Max Pathos: 7

### Hue Allocation

| Category | Dots |
|----------|------|
| Arcanoi | 5 (no Guild Arcanoi) |
| Backgrounds | 5 |
| Passions | 10 (one MUST be Dark Passion) |
| Fetters | 8 |
| Stains | 3 |
| Pathos | 5 (max 7) |
| Willpower | 5 |
| Freebies | 15 |

### The Quiescent Shadow
- Rarely speaks, Shadow seems absent
- Dark Passions mirror regular Passions
- When hue gains Pathos from Passions, Shadow gains Angst
- If purged of pigment taint, converts to normal Shadow

---

## Output Format

```markdown
# [Character Name] (Orpheus Projector)

## Concept
**Lament**: [Skimmer/Sleeper]
**Shade**: [Shade name]
**Role at Orpheus**: [Job description]

## Near-Death Experiences
1. [First NDE]
2. [Second NDE]
3. [Third NDE]

## Statistics
### Attributes
[Standard layout]

### Abilities
[Standard layout]

### Backgrounds
| Background | Rating | Notes |
|------------|--------|-------|
| Destiny | ●●○○○ | [Description] |

### Arcanoi
| Arcanos | Rating | Notes |
|---------|--------|-------|
| [Shade Favored] | ●●○○○ | Favored |
| Embody | ●○○○○ | Required |
| Lifeweb | ●○○○○ | Required |

## Passions
| Passion | Emotion | Rating |
|---------|---------|--------|

## Tethers
| Tether | Rating | Notes |
|--------|--------|-------|
| Physical Body | ●●●●● | Silver cord (required) |

## Stains
| Stain | Advantage | Disadvantage |
|-------|-----------|--------------|

## Vitality
- **Pathos**: [X] (max = Corpus)
- **Willpower**: [X]
- **Angst**: [X]
- **Corpus**: 10

## Crucible
**Name**: [Crucible name]
**Members**: [List]
**Yoking Benefit**: [Your contribution]
```

---

## Reference Data

```bash
# Shades
python scripts/lookup.py orpheus.shades shades "Poltergeist"

# Stains
python scripts/lookup.py orpheus.stains stains "Barbed Corpus"

# Orpheus Backgrounds
python scripts/lookup.py orpheus.backgrounds backgrounds "Gauze Relic"
```
