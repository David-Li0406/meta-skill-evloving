# Notable NPC Module

Create interconnected NPCs in the Faces of Magick style—characters designed to link together and generate cascading storylines.

## When to Use

- Creating recurring NPCs with story hooks
- Building interconnected NPC networks
- Designing antagonists, allies, mentors, or rivals
- Generating plot threads that span multiple sessions

## NPC Schema

### Required Fields

| Field | Description |
|-------|-------------|
| Name | Character name (may include nickname in quotes) |
| Tradition | Faction affiliation (or "Unaffiliated") |
| Role | One-line summary of function in chronicle |
| Summary | 2-3 sentence character concept |

### Optional Enhanced Fields (Faces of Magick Style)

| Field | Description |
|-------|-------------|
| `epithet` | Evocative subtitle (e.g., "The End of the Line", "Thief of the Arcane") |
| `awakened` | Year of Awakening (or "Unknown") |
| `born` | Year of birth (or "Unknown") |
| `connections` | Dictionary of relationships to other characters |
| `rise_and_ruin` | Array of escalating story hooks |
| `scaling_notes` | How to adjust power level for different chronicles |
| `roleplaying_notes` | Mannerisms, speech patterns, personality quirks |
| `future_fates` | Alternative versions for different metaplots |
| `talisman` | Special equipment with mechanical details |

## Creation Process

### Step 1: Concept
```
Name: [Name]
Epithet: [Evocative subtitle]
Tradition: [Faction]
Awakened: [Year] (Born: [Year])
Role: [One-line function]
```

### Step 2: Summary
Write 2-3 sentences covering:
- Core concept/what makes them unique
- Current situation/motivation
- The problem or conflict they bring

### Step 3: Stats
Use "Suggested" prefix—stats are meant to be flexible.

| Category | Approach |
|----------|----------|
| Attributes | Standard 7/5/3 or adjusted for power level |
| Abilities | Highlight 10-15 most relevant with specialties |
| Arete | Match chronicle power level (3-5 typical, 6-10 for legends) |
| Spheres | Focus on character concept; not all need 9 Spheres |
| Willpower | 6-8 typical; 9-10 for exceptionally driven |

### Step 4: Connections

Design 2-4 connections to other characters (NPCs or potential PCs):

```json
"connections": {
  "The [Nickname]": {
    "target": "[Character Name]",
    "relationship": "[Nature of connection and current situation]",
    "page": [page number or null if custom]
  }
}
```

**Connection Types:**
- Ally (shared goals, mutual support)
- Rival (competition without hatred)
- Enemy (active opposition)
- Mentor/Student (teaching relationship)
- Contact (useful but distant)
- Debt (owes or is owed a favor)
- Secret (knows something about them)
- Victim (has harmed or will harm)

### Step 5: Rise and Ruin

Create 2-4 escalating story hooks:

```json
"rise_and_ruin": [
  {
    "title": "[Short Hook Name]",
    "description": "[What's happening, what's at stake, what PCs can do]"
  }
]
```

**Hook Escalation Pattern:**
1. **Entry Point**: Minor situation that introduces the NPC
2. **Complication**: Stakes rise, connections activate
3. **Crisis**: Major conflict requiring intervention
4. **Catastrophe** (optional): What happens if nothing is done

### Step 6: Scaling Notes (Optional)

For powerful NPCs, provide advice on adjusting presence:

```
For understated chronicles:
- Keep them off-screen, using intermediaries
- Focus on consequences of their actions rather than direct encounters
- Use only a subset of their abilities
- Keep all Flaws, remove some Merits
```

### Step 7: Image and Roleplaying

**Image**: Physical appearance, typical dress, distinctive features
**Roleplaying Notes**: How they act, speak, what motivates them moment-to-moment

---

## Example: Minimal NPC

```
Name: Marcus Webb
Tradition: Virtual Adepts
Role: Information broker with too many secrets
Summary: Hacker who sells data to everyone—Traditions, Technocracy, 
even Nephandi. Has become a liability because he knows everyone's 
dirty laundry. Someone's going to silence him soon.

Suggested Arete: 3
Suggested Spheres: Correspondence 3, Mind 2

Connections:
- The Client: [PC or NPC] bought information; now Marcus needs a favor
- The Hunter: Syndicate operative closing in on Marcus's location
```

---

## Example: Full NPC (Faces of Magick Style)

```json
{
  "name": "Dr. Amara Okonkwo",
  "epithet": "The Architect of Endings",
  "tradition": "Euthanatos (Aided)",
  "awakened": "2003",
  "born": "1975",
  "role": "Hospice director who accelerates 'necessary' deaths",
  "summary": "Nigerian-American doctor who helps the terminally ill pass peacefully—
    sometimes before their time. Believes she can see the 'Good Death' in people's 
    patterns. The Technocracy is investigating unusual death rates at her facility.",
  "attributes": {
    "strength": 2, "dexterity": 2, "stamina": 3,
    "charisma": 4, "manipulation": 3, "appearance": 3,
    "perception": 5, "intelligence": 4, "wits": 3
  },
  "abilities_highlights": [
    "Empathy (Dying) 4", "Medicine (Palliative Care) 5",
    "Occult 3", "Science (Pharmacology) 4", "Subterfuge 3"
  ],
  "arete": 5,
  "spheres": {"entropy": 4, "life": 3, "mind": 3, "spirit": 2},
  "willpower": 8,
  "connections": {
    "The Investigator": {
      "target": "NWO Agent Chen",
      "relationship": "Posing as health inspector; growing suspicious"
    },
    "The Student": {
      "target": "[PC]",
      "relationship": "Offered to teach entropy magic in exchange for protection"
    }
  },
  "rise_and_ruin": [
    {
      "title": "Comfort Care",
      "description": "A patient's family member asks PCs to investigate their 
        relative's sudden decline"
    },
    {
      "title": "The Pattern",
      "description": "Agent Chen has connected deaths to Amara; planning raid"
    },
    {
      "title": "The Good Death",
      "description": "Amara sees the 'necessary death' pattern in a PC's ally"
    }
  ],
  "scaling_notes": "For less morally complex games, make her clearly villainous 
    (killing for power). For nuanced games, keep her motivations sympathetic 
    but methods questionable.",
  "roleplaying_notes": "Speaks softly but directly. Never lies but omits 
    uncomfortable truths. Makes intense eye contact. Calls everyone 'dear.'"
}
```

---

## Connection Network Guidelines

When creating multiple NPCs:

1. **Each NPC should connect to 2-4 others**
2. **No NPC should be isolated** (orphan nodes break the network)
3. **Include at least one PC connection point** per NPC
4. **Mix connection types** (not all allies or all enemies)
5. **Create tension chains** (A trusts B, B opposes C, C threatens A)

### Network Visualization Template

```
[NPC A] --ally--> [NPC B] --enemy--> [NPC C]
    |               |                   |
  mentor          rival              unknown
    v               v                   v
  [PC 1]         [PC 2]             [NPC D]
```

---

## Reference Data

```bash
# Lookup existing NPCs for connections
python scripts/lookup.py m20.npcs faces-of-magick "Jack"

# Search for NPCs by concept
python scripts/lookup.py m20.npcs --search "Technocracy"

# Get connection network
python scripts/lookup.py m20.npcs connection-network
```

---

## Validation Checklist

- [ ] Name and Tradition specified
- [ ] Summary captures concept, situation, and conflict
- [ ] Arete appropriate for chronicle power level
- [ ] Spheres support character concept
- [ ] At least 2 connections defined
- [ ] At least 2 Rise and Ruin hooks
- [ ] Image and Roleplaying Notes provided
- [ ] Connections don't create orphan nodes in network
- [ ] At least one clear PC entry point
