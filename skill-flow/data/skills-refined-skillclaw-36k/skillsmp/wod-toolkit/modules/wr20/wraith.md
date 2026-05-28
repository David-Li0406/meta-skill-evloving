# Wraith Character Module

Create mechanically valid Wraith characters for W20.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| (all PCs) | Read `modules/shadow.md`, create Shadow |
| Haunt | Read `modules/haunt.md`, create Haunt document |
| Allies, Contacts (important) | Read `modules/ally.md`, create companion NPCs |
| Mentor (important) | Create NPC wraith using this module |
| Relic | Read `modules/relic.md`, create Relic document |
| Artifact | Read `modules/artifact.md`, create Artifact document |

**DO NOT create a PC with backgrounds as one-line summaries.**

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, Legion affiliation, death circumstances
3. **Life & Death** — Brief biography, how they died, why they became Restless
4. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
5. **Attributes** — 7/5/3 across Physical/Social/Mental (+ 1 base each)
6. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
7. **Backgrounds** — 7 dots. Note which need sub-documents
8. **Arcanoi** — 5 dots (cap 3). See Arcanoi Selection section.
9. **Passions** — 10 dots (1-5 per Passion). Statement + Emotion + Rating
10. **Fetters** — 10 dots (1-5 per Fetter). People, places, or things
11. **⛔ SHADOW (PC)** — Read `modules/shadow.md`, create Shadow
12. **Merits & Flaws** — From `lookup.py character.merits-flaws merits-flaws`. Flaws ≤ 7
13. **⛔ BACKGROUNDS (PC)** — Create documents for Haunt/Relic/Artifact/Allies
14. **Freebies** — 15 + Flaws - Merits. Spend exactly.
15. **Derived** — Willpower 5, Pathos 5 + Memoriam, Corpus 10
16. **Specialties** — Required for 4+ traits
17. **Description** — Appearance (death-influenced), mannerisms, Deathmarks
18. **Document** — Link all sub-documents
19. **Validate**

---

## Arcanoi Selection

When choosing Arcanoi, consider your character's concept and which Guilds they might interact with.

### Arcanoi Reference
```bash
python scripts/lookup.py arcanoi.arcanoi-summary arcanoi-summary "Argos 3"
python scripts/lookup.py arcanoi.arcanoi-summary arcanoi-summary --find "possess"
```

### The 16 Arcanoi

| Arcanos | Guild | Primary Function |
|---------|-------|------------------|
| Argos | Harbingers | Travel (Tempest, Byways, teleportation) |
| Castigate | Pardoners | Shadow manipulation (self and others) |
| Embody | Proctors | Physical manifestation in Skinlands |
| Fatalism | Oracles | Fate perception and manipulation |
| Flux | Alchemists | Decay and reconstruction of plasm |
| Inhabit | Artificers | Possess machines and technology |
| Intimation | Solicitors | Create/remove desires and emotions |
| Keening | Chanteurs | Sonic effects, songs of the dead |
| Lifeweb | Monitors | Work with Fetters, sense connections |
| Mnemosynis | Mnemoi | Memory manipulation (forbidden) |
| Moliate | Masquers | Reshape plasm (bodies, disguises) |
| Outrage | Spooks | Exert physical force in Skinlands |
| Pandemonium | Haunters | Create terrifying effects |
| Phantasm | Sandmen | Enter and manipulate dreams |
| Puppetry | Puppeteers | Possess living beings |
| Usury | Usurers | Manipulate Pathos, Corpus, vital energy |

### Arcanos Level Summary
| Level | Capability |
|-------|------------|
| 1 | Basic perception, minor effect |
| 2 | Intermediate use, self-affecting |
| 3 | Standard effects, affect others |
| 4 | Powerful effects |
| 5 | Mastery, major effects |

### Common Functions Quick Reference
| Function | Arcanos |
|----------|---------|
| Combat (Skinlands) | Outrage, Embody |
| Combat (Underworld) | Moliate, Flux |
| Stealth/Travel | Argos, Moliate |
| Social manipulation | Keening, Intimation |
| Information gathering | Lifeweb, Fatalism, Mnemosynis |
| Skinlands interaction | Embody, Inhabit, Puppetry, Outrage |
| Shadow work | Castigate |
| Dream entry | Phantasm |
| Terror/Haunting | Pandemonium, Keening |

### Guild Membership
Taking dots in an Arcanos doesn't automatically grant Guild membership. The **Guild** background represents actual membership and access to Initiate-level powers.

---

## Passions

Passions are the emotional drives keeping the wraith from succumbing to Oblivion.

### Passion Structure
Each Passion has three components:
1. **Statement** — What the wraith wants to do
2. **Emotion** — The feeling driving the action
3. **Rating** — Intensity (1-5)

### Common Emotions
| Emotion | Examples |
|---------|----------|
| Love | Protect, cherish, watch over |
| Hate | Destroy, ruin, harm |
| Fear | Escape, hide from, avoid |
| Rage/Fury | Punish, avenge, strike at |
| Hope | Achieve, find, discover |
| Despair | Prevent, warn, save others from |
| Greed | Possess, acquire, hoard |
| Determination | Complete, finish, accomplish |

### Sample Passions
- Protect my family (Love) 4
- Find my killer (Revenge) 3
- Keep people away from my grave (Greed) 2
- Finish my novel (Determination) 3
- Warn others about the cult (Fear) 2

---

## Fetters

Fetters are the physical anchors tying a wraith to the Skinlands.

### Fetter Types
| Type | Examples |
|------|----------|
| People | Spouse, child, best friend, rival |
| Places | Home, workplace, death site, grave |
| Things | Wedding ring, car, journal, weapon |

### Fetter Ratings
| Rating | Importance |
|--------|------------|
| 1 | Minor connection |
| 2 | Significant |
| 3 | Important |
| 4 | Core to identity |
| 5 | Defining attachment |

### Passion-Fetter Links
Passions and Fetters should connect:
- Passion: "Protect my son" (Love) 4
- Fetter: My son: 5

---

## Allocation Summary

| Category | Dots |
|----------|------|
| Attributes | 7/5/3 (+ 9 base) |
| Abilities | 13/9/5 (cap 3) |
| Backgrounds | 7 |
| Arcanoi | 5 (cap 3) |
| Passions | 10 |
| Fetters | 10 |
| Corpus | 10 (fixed) |
| Pathos | 5 + Memoriam |
| Willpower | 5 |
| Freebies | 15 |

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Arcanos | 5 |
| Willpower | 2 |
| Passion | 2 |
| Background | 1 |
| Fetter | 1 |
| Pathos | 1 per 2 dots |

**Shadow Trade**: Character freebies can reduce Shadow freebies 1:1 (min 0). Shadow can gain up to +7 freebies from character pool.

## Reference Data

```bash
# Archetypes
python scripts/lookup.py character.archetypes archetypes "Penitent"

# Backgrounds
python scripts/lookup.py character.backgrounds backgrounds "Haunt"

# Arcanoi
python scripts/lookup.py arcanoi.arcanoi-summary arcanoi-summary "Inhabit"
python scripts/lookup.py arcanoi.guild-arcanoi guild-arcanoi "Artificers"

# Legions
python scripts/lookup.py factions.legions legions "Emerald Legion"

# Merits & Flaws
python scripts/lookup.py character.merits-flaws merits-flaws --find "medium"
```

## Validation

- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 7 dots
- [ ] Arcanoi: 5 dots, none > 3
- [ ] Passions: 10 dots total
- [ ] Fetters: 10 dots total
- [ ] Corpus: 10
- [ ] Pathos: 5 + Memoriam
- [ ] Willpower: 5
- [ ] Flaws ≤ 7 points
- [ ] Freebies spent exactly
- [ ] (PC) Shadow created with `modules/shadow.md`
- [ ] (PC) All relevant backgrounds have documents:
  - [ ] Haunt → Haunt document
  - [ ] Relic → Relic document(s)
  - [ ] Artifact → Artifact document(s)
  - [ ] Allies/Contacts → Companion documents
  - [ ] Mentor → NPC wraith document
- [ ] All links valid

## PC File Structure

```
[character]/
├── [character].md          ← Links to all below
├── shadow.md               ← REQUIRED
├── haunts/
├── relics/
├── artifacts/
├── companions/             ← Allies, Mentor
└── organizations/          ← If relevant
```

## Legion Assignment

Wraiths are assigned to Legions based on how they died:

| Legion | Death Type | Deathlord |
|--------|------------|-----------|
| Emerald | Chance/Accident | Emerald Lord |
| Skeletal | Pestilence/Disease | Skeletal Lord |
| Grim | Violence/Combat | Smiling Lord |
| Penitent | Passion-related | Ashen Lady |
| Iron | Age/Natural causes | Quiet Lord |
| Silent | Despair/Suicide | The Quiet |
| Paupers | Poverty/Neglect | Beggar Lord |
| Fate | Fate/Destiny (mysterious) | Lady of Fate |

## Deathmarks

All wraiths bear **Deathmarks** — visible signs of how they died:
- Gunshot wound: Visible entry/exit wounds
- Drowning: Perpetually wet appearance, seaweed
- Fire: Burned areas, smoke smell
- Disease: Sores, lesions, pallor
- Old age: Exaggerated age features
- Accident: Visible injuries from the accident

Deathmarks identify Legion affiliation at a glance.
