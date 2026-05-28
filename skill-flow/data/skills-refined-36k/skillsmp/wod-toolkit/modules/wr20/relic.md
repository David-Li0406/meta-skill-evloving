# Relic Module

Create Relics (ghosts of objects) for W20.

## What is a Relic?

A Relic is the ghost of an object—a plasmic duplicate that crossed the Shroud when:
- The object was destroyed
- The object was loved so intensely it generated a spectral copy
- A wraith brought it across using Inhabit

Relics are made of **plasm**, the raw stuff of the Underworld.

---

## Relic vs Artifact

| Relic | Artifact |
|-------|----------|
| Ghost of a mundane object | Has supernatural powers |
| Functions as in life | Can do impossible things |
| No special activation | Often requires Pathos |
| Background: Relic | Background: Artifact |

---

## Relic Rating

| Rating | Description | Examples |
|--------|-------------|----------|
| 1 | Minor useful item | Pen, keys, small tool |
| 2 | Useful item | Weapon, valuable object |
| 3 | Significant item | Heirloom, important possession |
| 4 | Powerful item | Major weapon, vehicle |
| 5 | Legendary item | Famous object, irreplaceable |

---

## Relic Types

### Personal Effects
- Jewelry, watches, photographs
- Clothing, hats, accessories
- Books, journals, letters
- Small keepsakes

### Tools & Weapons
- Hand tools, knives
- Firearms (require ghost ammunition)
- Vehicles (rare, high rating)
- Professional equipment

### Significant Objects
- Family heirlooms
- Religious items
- Art objects
- Historical artifacts

---

## Relic Properties

### Material Properties
- Relics function like their living counterparts
- A relic gun fires, a relic car drives
- Quality matches the original object

### Ammunition & Fuel
- Relic firearms need relic ammunition
- Relic vehicles need relic fuel
- These are separate resources to track

### Durability
- Relics can be damaged
- Damaged relics can be repaired with Flux
- Destroyed relics are gone forever

---

## Creation Workflow

1. **Object** — What was it in life?
2. **Origin** — How did it become a Relic?
3. **Rating** — 1-5 (from Background dots)
4. **Significance** — Why does the wraith have it?
5. **Appearance** — Current state
6. **Function** — What it does
7. **History** — Story of the object
8. **Validate**

---

## Origin Stories

### Death Transition
- Object was on the person when they died
- Strong emotional attachment carried it over
- Most common for personal effects

### Destruction
- Beloved object destroyed (fire, violence, decay)
- Creates relic in Shadowlands
- Common source for all relic types

### Crafted
- Wraith with Inhabit pulled it across
- Uses Inhabit ••••• (Relic Creation)
- Requires destroying the Skinlands object

### Soulforged
- Made from the Corpus of a wraith
- Dark practice, often from condemned souls
- Creates oboli (coins) and other goods

---

## Fetter Connection

Relics often connect to Fetters:
- A relic watch might link to "My grandfather's watch" Fetter
- Relic and Fetter can be the same object
- Losing the relic may endanger the Fetter

---

## Output Format

```markdown
# [Relic Name]

**Rating**: ●●○○○ (2)
**Type**: [Category]
**Owner**: [Wraith name]

## Description

### Physical Appearance
[What the relic looks like]
[Any visible wear, damage, or distinctive features]

### Shadowlands Appearance
[Any differences in how it appears to wraiths]

## History

### In Life
[The object's story when it was among the living]
[Why it was important]

### Transition
[How it became a Relic]
[Circumstances of its crossing]

## Function
[What the relic does]
[Any special capabilities or limitations]

## Significance
[Why this wraith possesses it]
[Emotional/practical value]

## Fetter Connection
[If connected to a Fetter, describe the link]

## Notes
[Any additional details]
```

---

## Validation

- [ ] Rating 1-5
- [ ] Object type identified
- [ ] Origin story described
- [ ] Current appearance described
- [ ] Function explained
- [ ] Significance to owner established
- [ ] Fetter connection noted (if any)

---

## Soulforged Items (Dark Topic)

Soulforging is the process of forging plasm—including wraith Corpus—into permanent objects.

### Soulforged Products
- **Oboli**: Currency of Stygia
- **Weapons**: Stygian steel
- **Armor**: Protective gear
- **Tools**: Various implements

### Moral Weight
- Soulforging destroys the source wraith
- Considered necessary evil by Hierarchy
- Criminals sentenced to the forges
- Some claim consciousness persists

### In Play
- Soulforged items occasionally moan
- Disturbing to sensitive wraiths
- Major ethical consideration

---

## Reference Data

```bash
# Example relics
python scripts/lookup.py items.example-relics example-relics --keys

# Soulforging rules
cat references/rules/soulforging.md
```
