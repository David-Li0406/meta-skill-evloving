# Medium Module

Create mortal characters with the ability to perceive and communicate with wraiths.

## Medium Types

| Type | Origin | Notes |
|------|--------|-------|
| **Innate** | Born with ability | Often caul-born or family history |
| **Developed** | Triggered by trauma | Near-death experience, severe shock |
| **Trained** | Learned from mentor | Requires latent potential |
| **Lineage** | Family bloodline | Benandanti, Hidalgo, or Zukal |

---

## Quick NPC Stats

| Trait | Allocation |
|-------|------------|
| Attributes | 6/4/3 |
| Abilities | 11/7/4 |
| Willpower | 4-7 |
| Backgrounds | 5 |
| Numina | 0-5 (optional) |

---

## Creation Steps

1. **Type** — Innate, Developed, Trained, or Lineage
2. **Perception Method** — How they sense wraiths
3. **Background** — Life circumstances, how ability manifested
4. **Focus Objects** — Items used to channel ability
5. **Belief System** — How they understand the dead
6. **Attributes** — Prioritize Mental for most mediums
7. **Abilities** — Occult, Awareness, Empathy essential
8. **Numina** — Select from `lookup.py mortals.numina numina` (optional)
9. **Merits/Flaws** — Medium-specific from `lookup.py mortals.medium-merits-flaws medium-merits-flaws`
10. **Motivations** — Why do they interact with wraiths?
11. **Complications** — Risks, enemies, competing interests

---

## Perception Methods

| Method | Description | Notes |
|--------|-------------|-------|
| **Visual** | Sees wraiths | Most common, clearest |
| **Auditory** | Hears wraiths | Often mistaken for mental illness |
| **Tactile** | Feels presences | Temperature changes, touch |
| **Full Sensory** | All senses | Rare, powerful |
| **Dream** | Contact while sleeping | Safer, less controllable |
| **Trance** | Requires altered state | Ritualistic |

---

## Focus Objects

Mediums typically use focus objects to channel their ability:

| Type | Examples |
|------|----------|
| **Heirlooms** | Family items passed down |
| **Cultural** | Tarot, crystal ball, Ouija board, bones |
| **Personal** | Items connected to specific dead |
| **Religious** | Crosses, prayer beads, ritual items |
| **Modern** | Spirit boxes, apps, recorders |

---

## Belief Systems

A medium's cultural background shapes how they interpret the dead:

| System | Approach | Notes |
|--------|----------|-------|
| **Spiritualist** | Victorian séance tradition | Spirit guides, trance channeling |
| **Christian** | Exorcism, souls in limbo | May view contact as dangerous |
| **Shamanic** | Spirit world journeys | Guides, allies, enemies |
| **Syncretic** | Umbanda, Vodou, Santería | Possession-based, communal |
| **Secular** | Scientific investigation | Evidence-focused, skeptical |
| **Hermetic** | Western occult tradition | Ritual magic, correspondences |

---

## Family Lineages

### Benandanti (Italian)

**Origin**: Italian caul-born tradition  
**Special Power**: Ekstasis (spirit projection into Underworld)  
**Requirement**: Must be born with a caul, unhooded by another Benandanti

| Trait | Value |
|-------|-------|
| Focus | Caul (worn over eyes) |
| Weapon | Fennel sword (forged in Nihil, functions as Stygian steel) |
| Limitation | Can only enter Underworld at night |
| Risk | Loss of caul = permanent trapping |

**System**:
- **Minor Ekstasis**: Willpower (diff 7) to peer into Shadowlands
- **Full Ekstasis**: Perception + Meditation (diff 8) to enter Underworld physically
- Must return to entry point before dawn or remain trapped

### Hidalgo (Mexican/Maya)

**Origin**: Giovanni-connected bloodline, believed extinct  
**Special Power**: Maya necromancy, contact with Dark Kingdom of Obsidian  
**Location**: Hidden in Chiapas/Guatemala rainforest

| Trait | Value |
|-------|-------|
| Focus | Ya'aché (Ceiba) tree contact |
| Bonus | +2 dice when touching sacred tree |
| Knowledge | Maya Underworld (Xibalba), astronomy |
| Secret | Survive through staked Sabbat vampire |

**System**:
- Perception + Meditation (diff 6, or 4 with Ya'aché contact)
- Each success = 2 minutes of Underworld perception
- Charisma + Occult (diff 5) to make requests of wraiths

### Zukal (Bohemian/European)

**Origin**: Balkan peasant tradition, dispersed across Europe/Americas  
**Special Power**: Nadané (summoning and binding)  
**Organization**: 13 active mediums at any time; Strýci (Prague) maintain records

| Trait | Value |
|-------|-------|
| Focus | Variable (family tradition) |
| Network | Can summon dead family members as allies |
| Specialty | Exorcism, professional medium work |
| Resources | Family financial support |

**System**:
- Enter trance using personal focus object
- Can summon specific ghost using connected item
- Dead family members available as helpers
- Exorcism: Extended contested roll vs. possessing entity

---

## Numina

Mediums may possess supernatural powers. See `lookup.py mortals.numina numina`.

### Hedge Magic Paths
| Path | Function |
|------|----------|
| Whistling | Storm-based ghost manipulation |
| Black Hat | Technology-based spirit interaction |

### Psychic Paths
| Path | Function |
|------|----------|
| Starlight | Shadowlands travel |
| Shadow | Concealment from spirits |
| Divination | Prophecy through the dead |

---

## Medium Merits

| Merit | Cost | Effect |
|-------|------|--------|
| Temperature-Sensitive | 1 | Sense manifestation temperature shifts |
| Ashen | 2 | Feel when wraith is nearby |
| Lucid Dreamer | 2 | Spirit dream contact; -2 diff Investigation after rest |
| Frequency | 3 | See/hear wider spectrum; 1 WP = talk through Shroud |
| Magician's Understanding | 3 | Sense if spirit present or phenomenon faked |
| Circles | 4 | Supernatural community contacts |
| Houses of the Holy | 7 | Sanctuary no supernatural enemy may enter |

---

## Mortal-Wraith Communication

### From Wraith's Perspective
- Medium contact is valuable but risky
- Dictum Mortuum forbids unsanctioned contact with living
- Risk of Hierarchy attention
- Mediums may have their own agendas
- Some mediums can be manipulated; others are dangerous

### From Medium's Perspective
- Initial contact always causes dread (even with allies)
- Ghost as "alien presence in mind"
- Voice in head, not audible to others
- Risk of possession
- Wraiths may be deceptive about Underworld truths

---

## Possession Rules

When a wraith attempts to possess a medium:

| Situation | Roll |
|-----------|------|
| Willing medium | Automatic success |
| Unwilling medium | Contested Willpower |
| Medium wins | Wraith expelled, contact breaks |
| Wraith wins | Wraith controls body |

**During possession**:
- Medium's consciousness dormant
- May have dream-like memories
- Body language, voice change dramatically
- May exhibit alien behaviors (smoking, drinking, etc.)
- Some cultural traditions welcome and support possession

---

## Output Format

```markdown
# [Medium Name]

**Type**: [Innate/Developed/Trained/Lineage]
**Lineage**: [If applicable: Benandanti/Hidalgo/Zukal]
**Perception Method**: [Visual/Auditory/Tactile/Full/Dream/Trance]

## Background
[How ability manifested]
[Life circumstances]
[Training or mentorship]

## Belief System
[How they understand the dead]
[Cultural/religious framework]

## Focus Objects
- [Primary focus]
- [Secondary items if any]

## Description
**Appearance**: [Physical description]
**Personality**: [Key traits]
**Motivation**: [Why they interact with wraiths]

## Statistics

### Attributes
**Physical**: Strength [N], Dexterity [N], Stamina [N]
**Social**: Charisma [N], Manipulation [N], Appearance [N]
**Mental**: Perception [N], Intelligence [N], Wits [N]

### Key Abilities
- Occult: [N]
- Awareness: [N]
- Empathy: [N]
- [Other relevant abilities]

### Other Traits
**Willpower**: [N]
**Humanity**: [N]

### Numina (if any)
- [Path]: [Rating]

### Merits & Flaws
- [Merit/Flaw]: [Rating]

## Capabilities
[What they can do]
[Limitations]
[Special techniques]

## Relationship to Wraiths
[Attitude toward the dead]
[Notable wraith contacts]
[Reputation in Underworld]

## Complications
[Risks they face]
[Enemies]
[Competing interests]
[Vulnerabilities]
```

---

## Validation

- [ ] Type clearly defined
- [ ] Perception method specified
- [ ] Belief system established
- [ ] Focus objects identified
- [ ] Stats appropriate to role
- [ ] Numina (if any) from valid list
- [ ] Merits/Flaws appropriate
- [ ] Motivations clear
- [ ] Complications considered
- [ ] Lineage details correct (if applicable)

---

## Reference Data

```bash
# Numina
python scripts/lookup.py mortals.numina numina "Whistling"
python scripts/lookup.py mortals.numina numina "Starlight"

# Medium Lineages
python scripts/lookup.py mortals.medium-lineages medium-lineages "Benandanti"
python scripts/lookup.py mortals.medium-lineages medium-lineages "Hidalgo"
python scripts/lookup.py mortals.medium-lineages medium-lineages "Zukal"

# Merits
python scripts/lookup.py mortals.medium-merits-flaws medium-merits-flaws --find "medium"
```
