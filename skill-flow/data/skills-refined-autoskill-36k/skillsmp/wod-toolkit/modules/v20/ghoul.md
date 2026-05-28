# Ghoul Module (Updated)

Create ghouls — mortals sustained by vampiric vitae who gain limited supernatural abilities.

## What is a Ghoul?

A ghoul is a mortal who regularly drinks vampire blood, gaining:
- Extended lifespan (don't age while ghouled)
- Access to Disciplines (usually 1-3 dots)
- Blood pool of 1-2 points (more for elder ghouls)
- Blood bond to their domitor (usually)
- Lesser form of the Beast and Clan weakness

---

## Ghoul Types

### Vassal
Standard ghoul bound to a specific domitor. Most common type.

### Independent Ghoul
Freed or escaped ghoul surviving without a master. Must find blood sources.

### Elder Ghoul
Ghoul maintained for decades or centuries. More powerful but more twisted.

---

## Ghoul Roles

### Servant
Core service role providing day-to-day support.
- **Cleaner**: Disposes bodies, protects Masquerade
- **Concierge**: Procures goods, manages contacts, outfits havens

### Protector
Defense and security role.
- **Bodyguard**: Physical protection, security expertise
- **Driver**: Transportation, escape planning, vehicle expertise

### Socialite
Social interface between vampire and mortal worlds.
- **Face**: Public representative, daytime business dealings
- **Technologist**: Modern technology expertise, research

### Companion
Personal and emotional role.
- **Confidante**: Trusted listener, secret-keeper
- **Sleeper Agent**: Hidden asset, activated when needed

---

## Four Ages of Ghouldom

| Age | Years | Blood Pool | Max Disciplines | Notes |
|-----|-------|------------|-----------------|-------|
| Young | <10 | 1 | 1-2 | Still learning role |
| Experienced | 10-50 | 2 | 3 | Established servant |
| Elder | 50-200 | 3 | 4 | Formidable, losing humanity |
| Ancient | 200+ | 4+ | 5+ | Nearly inhuman, respected/feared |

---

## Creation Steps

1. **Concept** — Role, relationship to domitor, type (vassal/independent/revenant)
2. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
3. **Attributes** — 6/4/3 across Physical/Social/Mental (+ 1 base each)
4. **Abilities** — 11/7/4 across Talents/Skills/Knowledges (cap 3)
5. **Backgrounds** — 5 dots (new options: Domitor, Double Life, Majordomo)
6. **Discipline** — 1 dot in one Discipline (usually domitor's Clan)
7. **Virtues** — 7 dots Camarilla/Independent; 5 dots Sabbat (+ 1 base each)
8. **Humanity** — Conscience + Self-Control
9. **Willpower** — Equal to Courage
10. **Blood Pool** — 1-2 points (varies by age)
11. **Freebies** — 21 points
12. **Merits & Flaws** — Max 7 points total
13. **Clan Weakness** — Apply appropriate weakness
14. **Validate**

---

## Ghoul vs Vampire vs Revenant Comparison

| Aspect | Ghoul | Vampire | Revenant |
|--------|-------|---------|----------|
| Attributes | 6/4/3 | 7/5/3 | 6/4/3 |
| Abilities | 11/7/4 | 13/9/5 | 11/7/4 |
| Backgrounds | 5 | 5 | 5 |
| Disciplines | 1 | 3 | 1 family + 1 Potence |
| Freebies | 21 | 15 | 21 |
| Virtues | 7 (5 Sabbat) | 7 | 5 |
| Blood Pool | 1-2 | 10+ | 1 (self-producing) |
| Aging | Paused | None | Slow natural |
| Sunlight | No damage | Lethal/Aggravated | No damage |

---

## Discipline Access

### Easy Access (No Teaching Required)
- **Potence** — Most common ghoul Discipline
- **Fortitude** — Common for protector roles
- **Celerity** — Common for active roles

### Requires Teaching
Any other Discipline the domitor possesses, up to level 3.

### Forbidden/Extremely Rare
- **Protean** — Requires vampire physiology
- **Thaumaturgy** — Tremere ghouls only, max 1-2 dots
- **Necromancy** — Giovanni/Rossellini only, max 1-2 dots
- Any power requiring undead state

---

## Clan-Specific Weaknesses

| Domitor's Clan | Ghoul Weakness |
|----------------|----------------|
| Assamite | Taste for Kindred blood; Self-Control (diff 6) when exposed |
| Brujah | +1 difficulty to resist frenzy |
| Followers of Set | Light Sensitive Flaw (progressive) |
| Gangrel | Develop minor animal features over time |
| Giovanni | Cold touch noticed by mortals |
| Lasombra | Reflection becomes blurry/distorted |
| Malkavian | Develop minor derangement related to domitor's |
| Nosferatu | Lose 1-2 Appearance over time (min 1) |
| Ravnos | Must indulge personal vice or +1 diff all actions |
| Toreador | Entranced by beauty (Willpower diff 6 to break) |
| Tremere | Blood bond twice as difficult to break |
| Tzimisce | +2 difficulty on social rolls with untainted mortals |
| Ventrue | +2 difficulty to resist Dominate from any vampire |

---

## Blood Bond

### Stages
| Stage | Drinks | Effect |
|-------|--------|--------|
| First | 1 | Infatuation, +1 difficulty to act against domitor |
| Second | 2 | Deep affection, +2 difficulty to act against domitor |
| Third | 3 | Full bond, +3 difficulty, Willpower 8+ to resist commands |

### Breaking the Bond
- **Standard**: 12 months without drinking domitor's blood
- **Extended Roll**: Willpower (diff 8), accumulate successes equal to months remaining

---

## New Backgrounds

### Domitor
| Rating | Generation | Relationship |
|--------|------------|--------------|
| • | 11th+ | Valued confidant |
| •• | 9th-10th | Passing fondness |
| ••• | 8th | Sometimes listens |
| •••• | 7th | Expects work only |
| ••••• | 6th | Tolerates existence |

### Double Life
| Rating | Description |
|--------|-------------|
| • | Distant contact with former life |
| •• | Monthly friend gatherings |
| ••• | Maintaining a lover |
| •••• | Close family ties with cover |
| ••••• | Full mortal life maintained |

### Majordomo
Chief steward commanding other servants.
| Rating | Servants |
|--------|----------|
| • | 1 |
| •• | 2 |
| ••• | 3 |
| •••• | 4 |
| ••••• | 5 |

---

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Discipline | 10 |
| Virtue | 2 |
| Humanity | 1 |
| Willpower | 1 |

---

## Ghoul-Specific Rules

### Frenzy
Ghouls can frenzy like vampires. Base difficulty 6, modified by Clan weakness.

### Healing
- Heal normally like mortals
- Can spend 1 blood to heal 1 bashing
- Cannot heal lethal/aggravated with blood

### Withdrawal
Missing regular feeding:
- -1 die per week without blood
- Intense cravings
- Eventually return to mortal state and age

---

## Validation Checklist

- [ ] Attributes: 13 dots (+ 9 base = 22 total)
- [ ] Abilities: 22 dots, none > 3
- [ ] Backgrounds: 5 dots
- [ ] Discipline: 1 dot (appropriate to domitor)
- [ ] Virtues: 10 total Camarilla/Independent; 8 total Sabbat
- [ ] Humanity = Conscience + Self-Control
- [ ] Willpower = Courage
- [ ] Freebies: 21 spent exactly
- [ ] Clan weakness applied
- [ ] Blood bond status noted
- [ ] Relationship to domitor documented

---

## Output Template

```markdown
# [Ghoul Name]

**Domitor**: [Vampire's name]
**Domitor's Clan**: [Clan]
**Role**: [Servant/Protector/Socialite/Companion - subtype]
**Type**: [Vassal/Independent/Elder]
**Years Ghouled**: [N]
**Blood Bond**: [Full/Second Stage/First Stage/None]

## Personality

**Nature**: [Archetype]
**Demeanor**: [Archetype]

## Attributes

### Physical
| Attribute | Rating |
|-----------|--------|
| Strength | ●●○○○ |
| Dexterity | ●●●○○ |
| Stamina | ●●○○○ |

### Social
| Attribute | Rating |
|-----------|--------|
| Charisma | ●●○○○ |
| Manipulation | ●●○○○ |
| Appearance | ●●○○○ |

### Mental
| Attribute | Rating |
|-----------|--------|
| Perception | ●●○○○ |
| Intelligence | ●●○○○ |
| Wits | ●●○○○ |

## Abilities

### Talents
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

### Skills
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

### Knowledges
| Ability | Rating |
|---------|--------|
| [Ability] | ●●○○○ |

## Discipline

| Discipline | Rating |
|------------|--------|
| [Discipline] | ●○○○○ |

## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| [Background] | ●●○○○ | [Details] |

## Virtues & Morality

| Trait | Rating |
|-------|--------|
| Conscience | ●●●○○ |
| Self-Control | ●●●○○ |
| Courage | ●●●○○ |
| Humanity | ●●●●●●○○○○ |

## Secondary Traits

| Trait | Value |
|-------|-------|
| Willpower | ●●●○○○○○○○ |
| Blood Pool | [N]/2 |

## Merits & Flaws

| Merit/Flaw | Points | Description |
|------------|--------|-------------|
| [Name] | [+/-N] | [Effect] |

## Clan Weakness

[Describe the weakness inherited from domitor's Clan]

## Description

[Physical appearance, mannerisms]

## History

[How they became a ghoul, relationship with domitor]

## Duties

[What they do for their domitor]
```

---

## Related Files
- `lookup.py character.ghoul-merits-flaws ghoul-merits-flaws` — Ghoul-specific Merits and Flaws
- `lookup.py character.ghoul-backgrounds ghoul-backgrounds` — New ghoul Backgrounds
- `modules/revenant.md` — Revenant character creation
- `modules/animal-ghoul.md` — Animal ghoul creation
- `modules/monstrous-creations.md` — Szlachta and Vozhd
