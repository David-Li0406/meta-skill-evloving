# Nephandic Servitor Module

Create Nephandic servants, bound entities, and summoned creatures. Uses spirit statblock format.

## Servitor Types

### Imp (Minor Demon)

**Nature:** Small, mischievous demon bound as a companion. The classic "familiar demon."

**Summoning:** Spirit 3

**Typical Role:** Spy, messenger, minor assistant, occasional combatant

**Personality:** Imps retain individual personalities—often cunning, sycophantic, or maliciously playful. They serve because they must, not from loyalty.

**Statblock:**
```
Willpower: 4
Rage: 3
Gnosis: 5
Essence: 15

Charms: Peek (see through reflective surfaces), Whisper (communicate silently with master), Minor Illusion, Disable (small machines)

Materialized Form:
Strength 1, Dexterity 4, Stamina 2
Abilities: Alertness 3, Athletics 3, Stealth 4, Subterfuge 3
Health Levels: 4
```

**Variations:** Fire imps (add Hellfire charm), knowledge imps (add Lore abilities), seduction imps (add Charm)

---

### Demonhound

**Nature:** A corrupted familiar—what happens when a spirit companion is twisted by Nephandic influence. Or a purpose-bred hellhound.

**Summoning:** Spirit 4

**Typical Role:** Guardian, tracker, attack animal

**Origin:** Either corrupted from a normal familiar or summoned specifically as a Demonhound

**Statblock:**
```
Willpower: 5
Rage: 7
Gnosis: 4
Essence: 25

Charms: Tracking, Fear (targets must roll Willpower or flee), Armor (tough hide), Cling

Materialized Form:
Strength 5, Dexterity 4, Stamina 5
Abilities: Alertness 4, Athletics 3, Brawl 4, Intimidation 4, Stealth 2
Attacks: Bite (Str+2 lethal)
Health Levels: 8
```

**Appearance:** Black dogs with burning eyes, skeletal hounds, dogs made of shadow—varies by creator's paradigm

---

### Fomori (Bane-Possessed Human)

**Nature:** A human possessed by a Bane spirit, transformed into a hybrid creature. Not a spirit—a corrupted mortal.

**Creation:** Spirit 4/Life 3, or simply expose vulnerable humans to powerful Banes

**Typical Role:** Shock troops, infiltrators, experiments

**Important:** Fomori were once people. Some retain fragments of their original personality. Most are in constant torment.

**Base Statblock (varies by individual):**
```
Attributes: Human base, modified by powers
Abilities: Retained from mortal life + combat skills
Willpower: 3-6
Health Levels: Standard + modifications

Powers: 3-7 powers (see below)
Taints: 1-4 taints (see below)
```

**Fomori Powers:**
| Power | Effect |
|-------|--------|
| Armored Skin | +2 soak |
| Berserker | Rage-fueled combat frenzy |
| Claws/Fangs | Lethal natural weapons |
| Extra Limbs | Additional arms, tentacles |
| Gaseous Form | Become mist |
| Immunity | Resist one damage type |
| Mega-Attribute | +3 to one Attribute |
| Mind Control | Dominate mortals |
| Regeneration | Heal 1 level/turn |
| Size | Larger or smaller than human |
| Venomous | Poison attack |
| Wall Walking | Cling to surfaces |

**Fomori Taints:**
| Taint | Effect |
|-------|--------|
| Deformity | Obvious physical corruption |
| Madness | Specific insanity |
| Vulnerability | Weakness to specific thing |
| Uncontrollable | Bane sometimes seizes control |
| Rotting | Body slowly decays |

**Example Fomor:**
```
## Fomor: The Smiling Man

Former accountant possessed by a Despair Bane

Attributes: Str 3, Dex 2, Sta 4, Cha 4, Man 4, App 2, Per 3, Int 3, Wits 3
Abilities: Finance 4, Subterfuge 4, Empathy 3 (sensing weakness)

Powers: 
- Aura of Despair (those nearby roll Willpower or suffer -2 dice)
- Immunity (bashing)
- Mind Control (suggestion only)

Taints:
- Madness (compulsive smiling, even in inappropriate situations)
- Vulnerability (hope—genuine expressions of hope cause pain)

Role: Corporate infiltrator who drives employees to breakdown and suicide
```

---

### Black Wind

**Nature:** Malevolent wind spirits that carry disease, madness, and despair. Often found in the service of Malfeans.

**Summoning:** Spirit 3

**Typical Role:** Area denial, spreading corruption, assassination through illness

**Statblock:**
```
Willpower: 6
Rage: 4
Gnosis: 6
Essence: 20

Charms: Disease (inflict illness), Maddening Whispers (cause temporary insanity), Ill Omen (curse), Invisibility, Flight

Cannot fully materialize—manifests as cold wind, whispers, disease
```

**Signs of Presence:** Unexplained drafts, whispered voices, sudden illness, feelings of dread

---

### Raamas Ka (Abyssal Steed)

**Nature:** Mounts from the depths of the Qlippoth. Reserved for powerful Nephandi.

**Summoning:** Spirit 5

**Typical Role:** Transportation, status symbol, combat mount

**Appearance:** Varies wildly—nightmare horses, flying serpents, impossible geometries that somehow carry riders

**Statblock:**
```
Willpower: 7
Rage: 8
Gnosis: 6
Essence: 40

Charms: Flight, Armor, Fear, Reform (reappear if destroyed, given time), Gateway (cross into Umbra)

Materialized Form:
Strength 7, Dexterity 5, Stamina 7
Abilities: Alertness 3, Athletics 4, Brawl 3, Intimidation 5
Health Levels: 12

Special: Rider gains +2 to Intimidation while mounted
```

---

### Sinfeeder

**Nature:** Spirits that feed on moral decay. They don't cause sin—they're attracted to it and encourage more.

**Summoning:** Spirit 3

**Typical Role:** Corruption assistance, identifying "ripe" targets, feeding on the results

**Statblock:**
```
Willpower: 5
Rage: 2
Gnosis: 7
Essence: 18

Charms: 
- Sin Sense (detect guilt, shame, moral weakness)
- Temptation Whisper (suggest sinful actions, +2 diff to resist)
- Feed (gain Essence from witnessing sin)
- Invisibility
- Possession (weak-willed targets only)
```

**Appearance:** Rarely seen. When visible: small shadowy figures, whispering mouths, eyes in the darkness

---

## Servitor Template

```markdown
## [Servitor Name]

**Type:** [Imp/Demonhound/Fomor/Black Wind/Raamas Ka/Sinfeeder/Other]
**Bound To:** [Master's name]
**Binding Method:** [How it was summoned/created]

### Spirit Stats (if applicable)
- Willpower:
- Rage:
- Gnosis:
- Essence:

### Charms/Powers
[List with brief descriptions]

### Materialized Form (if applicable)
**Attributes:** [Physical, Social, Mental]
**Abilities:** [Key abilities]
**Health Levels:**
**Attacks:** [If any]

### Appearance
[Physical description]

### Personality
[Behavior, quirks, attitude toward master]

### Binding Conditions
[What keeps it loyal, how to break the binding]
```

---

## Validation

- [ ] Servitor type matches role in story
- [ ] Stats appropriate to power level
- [ ] Binding method and conditions specified
- [ ] For Fomori: powers and taints balanced
- [ ] Appearance described
- [ ] Relationship to master defined
