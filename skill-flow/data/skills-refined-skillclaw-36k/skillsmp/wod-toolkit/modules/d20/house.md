# House Module — The Seven Celestial Houses

Reference for the seven Houses of the fallen.

## Overview

Before the Fall, God organized His angels into seven Houses, each with distinct duties and powers. These Houses remain the fundamental identity of every fallen angel.

---

## The Seven Houses

### Devils — The First House
**Celestial Title**: Angels of the Light, Heralds, Namaru  
**Role Before Fall**: Bearers of God's light and will; leaders and intermediaries  
**Starting Torment**: 3

**House Lore**:
- Lore of the Celestials (shared)
- Lore of Flame
- Lore of Radiance

**Stereotypes**:
- Natural leaders and speakers
- Charismatic, commanding
- Often arrogant, expect obedience
- Most likely to have held high rank in the rebellion

**Factional Tendencies**: Faustian, Luciferan

**Character Creation Notes**:
- Favor Social Attributes
- Expression, Leadership, Intimidation common
- Often have Fame, Influence, or Eminence backgrounds
- Weakness: Pride; difficulty accepting subordinate roles

---

### Scourges — The Second House
**Celestial Title**: Angels of the Wind, Guardians, Asharu  
**Role Before Fall**: Protectors of humanity; wielded life-giving and death-dealing winds  
**Starting Torment**: 3

**House Lore**:
- Lore of Awakening
- Lore of the Firmament
- Lore of the Winds

**Stereotypes**:
- Protective or destructive (rarely moderate)
- Close connection to humanity
- Often conflicted about their curse on mortality
- Healers or plague-bringers

**Factional Tendencies**: Reconciler, Faustian (reluctantly)

**Character Creation Notes**:
- Favor Physical or Social Attributes
- Medicine, Empathy, Survival common
- Often have Followers or Pacts backgrounds
- Weakness: Extreme views on humanity; either overprotective or callously dismissive

---

### Malefactors — The Third House
**Celestial Title**: Angels of the Fundament, Artificers, Annunaki  
**Role Before Fall**: Shapers of the physical world; builders and craftsmen  
**Starting Torment**: 3

**House Lore**:
- Lore of the Earth
- Lore of the Forge
- Lore of Paths

**Stereotypes**:
- Practical, pragmatic
- Patient craftsmen
- Often bitter about what humans have done to the world
- Makers of reliquaries and artifacts

**Factional Tendencies**: Faustian, Cryptic

**Character Creation Notes**:
- Favor Physical or Mental Attributes
- Crafts, Technology, Science common
- Often have Resources or Legacy backgrounds
- Weakness: Materialistic; can become obsessed with objects and projects

---

### Fiends — The Fourth House
**Celestial Title**: Angels of the Spheres, Fates, Neberu  
**Role Before Fall**: Keepers of the celestial engines; seers and prophets  
**Starting Torment**: 3

**House Lore**:
- Lore of Light
- Lore of Patterns
- Lore of Portals

**Stereotypes**:
- Seekers of knowledge
- Distant, analytical
- Haunted by their failure to foresee the Fall's consequences
- Obsessed with understanding "why"

**Factional Tendencies**: Cryptic, Luciferan

**Character Creation Notes**:
- Favor Mental Attributes
- Academics, Investigation, Research, Occult common
- Often have Allies (information networks) or Contacts backgrounds
- Weakness: Curiosity; compelled to investigate mysteries even at personal cost

---

### Defilers — The Fifth House
**Celestial Title**: Angels of the Deep, Muses, Lammasu  
**Role Before Fall**: Inspirers of humanity; spirits of longing and beauty  
**Starting Torment**: 3

**House Lore**:
- Lore of Longing
- Lore of Storms
- Lore of Transfiguration

**Stereotypes**:
- Passionate, emotional
- Manipulative through desire
- Either inspiring or corrupting (sometimes both)
- Masters of transformation and identity

**Factional Tendencies**: Faustian, Ravener

**Character Creation Notes**:
- Favor Social Attributes (especially Appearance and Manipulation)
- Performance, Empathy, Subterfuge common
- Often have Fame or Followers backgrounds
- Weakness: Mercurial; difficulty with commitment and consistency

---

### Devourers — The Sixth House
**Celestial Title**: Angels of the Wild, Beasts, Rabisu  
**Role Before Fall**: Guardians of nature and the wild places  
**Starting Torment**: 4

**House Lore**:
- Lore of the Beast
- Lore of the Flesh
- Lore of the Wild

**Stereotypes**:
- Feral, instinctual
- Loyal to packmates
- Protective of nature (or enraged at its destruction)
- Direct, often violent

**Factional Tendencies**: Luciferan, Ravener

**Character Creation Notes**:
- Favor Physical Attributes
- Brawl, Athletics, Animal Ken, Survival common
- Often have Allies (pack) or Followers backgrounds
- Weakness: Tactless; prone to violence and blunt honesty at inappropriate times

---

### Slayers — The Seventh House
**Celestial Title**: Angels of Death, Reapers, Halaku  
**Role Before Fall**: Guides of souls; keepers of the cycle of death and rebirth  
**Starting Torment**: 4

**House Lore**:
- Lore of Death
- Lore of the Spirit
- Lore of the Realms

**Stereotypes**:
- Patient, contemplative
- Comfortable with mortality and endings
- Often melancholy or fatalistic
- Closest connection to the dead and spirits

**Factional Tendencies**: Reconciler, Cryptic

**Character Creation Notes**:
- Favor Mental Attributes
- Occult, Awareness, Medicine common
- Often have Legacy or Eminence backgrounds
- Weakness: Fatalistic; can become passive or nihilistic

---

## House Relationships

| House | Allied With | Tension With |
|-------|-------------|--------------|
| Devils | Defilers, Malefactors | Slayers (resentment) |
| Scourges | Slayers, Fiends | Devourers (methods) |
| Malefactors | Devils, Devourers | Fiends (blame) |
| Fiends | Scourges, Slayers | Malefactors (mutual blame) |
| Defilers | Devils, Fiends | Devourers (incompatible) |
| Devourers | Malefactors, Slayers | Defilers, Fiends (frustration) |
| Slayers | Scourges, Fiends | Devils (old wounds) |

---

## Data Lookup

```bash
# Get full House details
python scripts/lookup.py d20.character houses "Devils"

# Search Houses by Lore
python scripts/lookup.py d20.character houses --find "Flame"

# Get House Lore
python scripts/lookup.py d20.lore house-lore "Devils"
```

---

## Output Template (House Section)

```markdown
## House: [House Name]

**The [Ordinal] House** — [Celestial Title]

**Celestial Role**: [Pre-Fall duty]

**House Lore**:
- [Lore 1]
- [Lore 2]  
- [Lore 3]

**Starting Torment**: [3 or 4]

**House Weakness**: [Brief description of typical House failing]
```
