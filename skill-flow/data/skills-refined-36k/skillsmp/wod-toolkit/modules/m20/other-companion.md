# Other Companion Module

Create non-human, non-spirit companions: animals, bygones, constructs, reanimates, robots, objects, and aliens.

## Character Types

| Type | Key Features | Required Flaws |
|------|--------------|----------------|
| **Animal** | Physical stats from templates | Animal (2), No Dexterous Limbs (4) |
| **Bygone** | Mythical creature | Thaumivore (5), Unbelief (3-8) |
| **Construct** | Created being | Varies (may need Power Source) |
| **Reanimate** | Animated corpse | Usually Unbelief |
| **Robot** | Mechanical being | Power Source (1-5) |
| **Alien** | Extraterrestrial | Alien Impression (1-5) |
| **Object** | Sentient item (NPCs only) | Limbless (5) |

**Lookup**: `python scripts/lookup.py companion.companion-types companion-types "Bygone"`

---

## Animal Companions

Natural creatures, possibly enhanced.

### Required Traits
- Animal (2 pts)
- No Dexterous Limbs (4 pts, usually)

### Common Advantages
Human Speech (1), Telepathy (2/4/6), Nightsight (3), Claws/Fangs (3/5/7), Wings (3/5), Speed

### Legendary Abilities
Folkloric powers that don't trigger Paradox:
- Black cats: Bad luck aura
- Ravens: Death omens, intelligence
- Owls: Wisdom, night vision
- Wolves: Pack tactics, tracking

### Sample Templates

**Housecat**: Str 1, Dex 4, Sta 2 | Alertness 3, Athletics 3, Brawl 2, Stealth 4 | Claws (3), Nightsight (3) | Animal (2), No Dexterous Limbs (4)

**Raven**: Str 1, Dex 3, Sta 2 | Alertness 4, Athletics 2, Awareness 2 | Wings (3), Human Speech (1) | Animal (2), No Dexterous Limbs (4)

**Wolf**: Str 3, Dex 3, Sta 4 | Alertness 3, Athletics 3, Brawl 3 | Claws/Fangs (5), Speed (2) | Animal (2), No Dexterous Limbs (4)

---

## Bygone Companions

Mythical creatures — griffins, unicorns, dragons, imps.

### REQUIRED Traits
- **Thaumivore (5 pts)**
- **Unbelief (3/5/8 pts)**

### Survival
Only survive long-term in:
- Chantries with strong protection
- Horizon Realms
- Primal Reality Zones (Gauntlet 4-)
- Remote areas far from mundanes

### Common Advantages
Wings, Claws/Fangs/Horns, Elemental Touch, Armor, Hazardous Breath, Size, Unaging

### Small Bygones
May survive longer by hiding: imps, pixies, household spirits, shisa, kijimuna.

---

## Construct Companions

Created beings — golems, homunculi, bioconstructs.

### Types
- **Bioconstructs**: Grown, genetic enhancements
- **Material**: Shaped from stone, metal, clay
- **Technocratic**: HIT Marks, cybernetic

### Common Advantages
Soak Lethal (3), Soak Aggravated (5), Armor, Unaging (5)

### Common Flaws
Unbelief (if obviously unnatural), Power Source (if mechanical)

---

## Reanimate Companions

Animated corpses.

### Types
Zombies, Cannibal Corpses, Frankensteinian Monsters, Talking Heads, Shambling Horrors

### Inherent Trait
**Soak Lethal Damage (3 pts)** — free

### Common Advantages
Soak Aggravated (5), Unaging (5), Soul-Sense (2/3), Claws (3)

### Common Flaws
Unbelief (3-8), Repulsive appearance, Vulnerabilities (fire, salt, headshots)

---

## Robot Companions

Mechanical beings with sentience.

### Inherent Traits
- **Soak Aggravated Damage (5 pts)** — free
- **Power Source** — REQUIRED

### No Unbelief
In tech-friendly areas. May suffer in primal/magical regions.

### Types
Drones, Androids, AI Constructs

---

## Object Companions

Sentient items — **Storyteller NPCs only**.

Not suitable for PCs due to lack of mobility. Examples: talking sword, enchanted skull, haunted car.

### Common Traits
Limbless (5), Unaging (5), Information Fount (5), Telepathy

---

## Creation Steps (All Types)

### Step 1: Concept
Type, specific creature, origin, relationship to mages

### Step 2: Attributes (6/4/3)
Modified by type (animals use templates)

### Step 3: Abilities (11/7/4)
Appropriate to type

### Step 4: Backgrounds (5 dots)
Appropriate to character

### Step 5: Special Advantages
Based on type — lookup: `lookup.py companion.special-advantages special-advantages`

### Step 6: Required Flaws
Based on type — lookup: `lookup.py companion.companion-flaws companion-flaws`

### Step 7: Willpower (3)

### Step 8: Freebie Points
- Standard companion: 15
- Skilled/advanced: 21
- Familiar-equivalent: 25

---

## Validation Checklist

- [ ] Type-appropriate required Flaws taken
- [ ] Attributes distributed appropriately
- [ ] Abilities match creature type
- [ ] Special Advantages fit concept
- [ ] Unbelief addressed (if Bygone)
- [ ] Survival requirements considered
- [ ] Freebie points spent exactly
- [ ] Relationship to mage(s) defined

---

## Output Template

```markdown
# [Companion Name]

**Type**: [Animal/Bygone/Construct/etc.]  
**Species/Form**: [Specific creature]  
**Nature**: [Archetype]  
**Demeanor**: [Archetype]  
**Associated Mage(s)**: [If any]  

## Attributes

### Physical
Strength ●○○○○ | Dexterity ●○○○○ | Stamina ●○○○○

### Social
Charisma ●○○○○ | Manipulation ●○○○○ | Appearance ●○○○○

### Mental
Perception ●○○○○ | Intelligence ●○○○○ | Wits ●○○○○

## Abilities

### Talents
[List]

### Skills
[List]

### Knowledges
[List]

## Backgrounds
[List]

## Special Advantages
[List with costs and effects]

## Merits
[If any]

## Flaws
[Required type flaws plus additional]

## Other Traits
**Willpower**: ●●●○○○○○○○  
**Health**: [ ] [ ] [ ] [ ] [ ] [ ] [ ]  
[Add Essence if familiar-type]

## Physical Description
[Appearance, size, features]

## Personality/Behavior
[How it acts, motivations]

## Origin
[How it came to be, met mages]

## Notes
[Special abilities, survival requirements, weaknesses]
```
