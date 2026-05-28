# Shared Umbra Module

Create Umbral locations and content that works across World of Darkness games.

---

## Umbral Structure Overview

The spirit world has three major regions plus the separate Dreaming:

| Region | Primary Game | Access |
|--------|--------------|--------|
| **Middle Umbra** | W20 | Spirit 3 (M20), Gifts (W20) |
| **High Umbra** | M20 | Mind/Spirit spheres |
| **Dark Umbra** | Wr20 | Death, Spirit 4+ |
| **The Dreaming** | C20 | Fae nature, Trods |

**Reference**: `lookup.py shared.umbra structure`

---

## Middle Umbra (Spirit World)

### Layers

**Penumbra** — Spirit reflection of physical world
- Gauntlet: Barrier rating 3-9
- Urban areas: High Gauntlet, Weaver influence
- Wilderness: Low Gauntlet, Wyld influence
- Wyrm sites: Corrupted reflection

**Near Realms** — Pocket dimensions
- CyberRealm/Digital Web
- Pangaea (prehistoric)
- Malfeas (Wyrm heart)
- Wolfhome (Garou sanctuary)
- Arcadia Gateway (Dreaming border)

**Deep Umbra** — Void between realms
- Dangerous, alien
- Risk of being lost forever
- Home to strange entities

### Gauntlet Ratings

| Location | Rating | Example |
|----------|--------|---------|
| Deep Wilderness | 3 | Ancient forest, untouched cave |
| Rural/Natural | 4-5 | Farm country, small towns |
| Suburban | 6 | Residential areas |
| Urban | 7-8 | Cities, industrial zones |
| High Tech/Dense | 9 | Data centers, hospitals, skyscrapers |

---

## High Umbra (Astral Reaches)

Realm of thought, concept, and abstraction.

### Layers

**Vulgate** — Surface shaped by mortal dreams
**Courts** — Organized realms of specific concepts
**Epiphamies** — Pure conceptual realms

### Spirit Naming
High Umbra spirits may use different rank names:
- Gaffling → Gaffling
- Jaggling → Jaggling
- Incarna → **Lord** or **Preceptor**
- Celestine → Celestine

---

## Dark Umbra (Underworld)

Realm of the dead.

### Layers

**Shadowlands** — Ghost reflection of living world
- Shroud: Barrier rating 5-9
- Gray, cold, decaying
- Where most wraiths dwell

**Tempest** — Storm between worlds
- Constant chaos
- Nihils open to Oblivion
- Spectres hunt here

**Far Shores** — Belief-created afterlives
- Various religious paradises/hells
- Kingdom of Ivory, Dark Kingdom of Wire, etc.

**Labyrinth** — Deepest region before Oblivion
- Where Spectres are born
- Malfean entities dwell here

### Shroud Ratings

| Location | Rating | Example |
|----------|--------|---------|
| Cemetery, Hospital | 5-6 | Places of death |
| Historic Site | 6-7 | Battlefields, old buildings |
| Normal Area | 7-8 | Most locations |
| Vibrant Area | 8-9 | Parties, festivals, new construction |

---

## Creating Umbral Locations

### Step 1: Determine Type
- Near Realm (pocket dimension)
- Penumbral reflection
- Shadowlands location
- High Umbra court
- Dreaming site

### Step 2: Define Physical/Umbral Correspondence
How does this relate to the physical world?
- Direct reflection
- Thematic connection
- No physical anchor

### Step 3: Establish Atmosphere
- Visual appearance
- Sounds, smells, sensations
- Emotional tone
- Time flow (normal, accelerated, frozen)

### Step 4: Define Inhabitants
- Spirit types present
- Wraiths (if Dark Umbra)
- Fae (if Dreaming-connected)
- Other entities

### Step 5: Set Mechanical Parameters
- Gauntlet/Shroud rating
- Special rules or limitations
- Available resources (Quintessence, Pathos, Glamour)

### Step 6: Consider Cross-Game Access
- Can werewolves reach it?
- Can mages access it?
- Is there a Shadowlands reflection?
- Any Dreaming connections?

---

## Shared Near Realms

These realms are accessible from multiple games:

### CyberRealm / Digital Web
**Aspect**: Weaver  
**Access**: W20 (CyberRealm), M20 (Digital Web)  
**Theme**: Digital reality, virtual space, information

Same place, different names. Virtual reality made real in the spirit world.

### Pangaea
**Aspect**: Wyld  
**Access**: W20, M20 (Spirit travel)  
**Theme**: Prehistoric Earth, ancient beasts

Primordial wilderness where dinosaurs and ancient creatures still roam.

### Malfeas
**Aspect**: Wyrm  
**Access**: W20 (dangerous), M20 (very dangerous)  
**Theme**: Heart of corruption

Domain of the Maeljin Incarnae. Extremely hostile.

### Arcadia Gateway
**Aspect**: Wyld  
**Access**: W20, C20  
**Theme**: Border of the Dreaming

Where the Middle Umbra touches the Dreaming. Trods pass through here.

---

## Penumbral Phenomena

### Blights
- Urban Wyrm/Weaver corruption
- Sick, polluted reflection
- Banes gather

### Glens
- Wyld purity sanctuaries
- Healthy, vibrant reflection
- Safe from corruption

### Chimares
- Metaphors made real
- Conceptual manifestations
- Can be navigated with understanding

### Wyldings
- Pure chaos zones
- Unpredictable, dangerous
- Rapid transformation

---

## Output Template

```markdown
# [Location Name]

**Type**: [Near Realm / Penumbral / Shadowlands / High Umbra / Dreaming]
**Aspect**: [Wyld / Weaver / Wyrm / Gaia / Mixed / N/A]
**Primary Game**: [W20 / M20 / Wr20 / C20]

## Access
| Game | Method | Difficulty |
|------|--------|------------|
| W20 | [Method] | [Difficulty] |
| M20 | [Method] | [Difficulty] |
| Wr20 | [Method] | [Difficulty] |
| C20 | [Method] | [Difficulty] |

## Barrier Rating
**Gauntlet**: [Rating if Middle Umbra]
**Shroud**: [Rating if Dark Umbra]

## Description
[Visual appearance, atmosphere, sensory details]

## Inhabitants
- [Spirit type / creature] — [Brief description]
- [Spirit type / creature] — [Brief description]

## Points of Interest
- **[Location within]**: [Description]
- **[Location within]**: [Description]

## Hazards
- [Danger type]: [Effect]
- [Danger type]: [Effect]

## Resources
- [Type]: [Availability]

## Story Hooks
- [Potential plot involving this location]
- [Potential plot involving this location]

## Cross-Game Notes
[How this location appears to or affects different creature types]
```

---

## Validation Checklist

- [ ] Type clearly defined
- [ ] Aspect appropriate
- [ ] Access methods for relevant games
- [ ] Barrier rating set
- [ ] Atmosphere described
- [ ] Inhabitants listed
- [ ] Hazards identified
- [ ] Cross-game implications considered
