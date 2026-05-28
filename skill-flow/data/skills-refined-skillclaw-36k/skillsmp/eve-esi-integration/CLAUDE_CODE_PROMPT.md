# EVE Portfolio Update Mission

Execute these updates for ARETE's EVE Online projects. Work autonomously, ask only if paths differ.

## Projects
- **EVE_Ships** (~/projects/EVE_Ships) - REBUILD with official renders
- **EVE_Rebellion** (~/projects/EVE_Rebellion) - Add ESI client + sprites  
- **EVE_Gatekeeper** (~/projects/EVE_Gatekeeper) - Add ESI client + SDE prep

---

## PHASE 1: EVE_Ships - Complete Rebuild

Download ALL ships from `https://images.evetech.net/types/{type_id}/render?size=256`

### Ship Type IDs (download all):
```
FRIGATES: rifter=587, tristan=593, merlin=603, punisher=597, slasher=585, breacher=598, atron=608, incursus=594, kestrel=602, condor=583, executioner=589, tormentor=591
DESTROYERS: thrasher=16242, catalyst=16240, cormorant=16238, coercer=16236, talwar=32872, algos=32875, corax=32876, dragoon=32874
CRUISERS: caracal=621, thorax=627, maller=624, stabber=622, rupture=629, vexor=626, moa=623, omen=625, bellicose=630, celestis=633, blackbird=632, arbitrator=628
BATTLECRUISERS: drake=24690, hurricane=24702, harbinger=24696, brutix=16229, cyclone=24700, myrmidon=24698, ferox=24688, prophecy=24692, tornado=4310, talos=4308, naga=4306, oracle=4302
BATTLESHIPS: raven=638, megathron=641, tempest=639, apocalypse=642, typhoon=644, dominix=645, scorpion=640, armageddon=643, maelstrom=24694, rokh=24688, abaddon=24692
FACTION: machariel=17738, nightmare=17736, vindicator=17740, bhaalgorn=17920, rattlesnake=17918, gila=17715, cynabal=17715, phantasm=17718, dramiel=17703, stratios=33470, astero=33468, nestor=33472
CAPITALS: naglfar=19724, moros=19720, phoenix=19726, revelation=19722, nidhoggur=24483, thanatos=23911, chimera=23915, archon=23757, hel=22852, nyx=23913, wyvern=23917, aeon=23919, ragnarok=11568, erebus=671, leviathan=3764, avatar=11567
INDUSTRIAL: venture=32880, procurer=17480, retriever=17478, hulk=22544, orca=28606, rorqual=28352
```

### Output structure:
```
EVE_Ships/
├── renders/256/{name}_{typeid}.png
├── renders/512/{name}_{typeid}.png
├── manifest.json  # {name: type_id, ...}
├── README.md      # Include CCP attribution below
└── .gitignore
```

### Required README attribution:
```
## Attribution
EVE Online and the EVE logo are registered trademarks of CCP hf.
Ship images © CCP hf, used under Content Creation Terms.
https://community.eveonline.com/support/policies/content-creation-terms-of-use/
```

---

## PHASE 2: EVE_Rebellion - Add ESI Integration

### Create core/esi_client.py:
```python
import httpx
from datetime import datetime, timezone

class ESIClient:
    BASE = "https://esi.evetech.net/latest"
    IMAGE = "https://images.evetech.net"
    
    def __init__(self, app="EVE_Rebellion", contact="dev@example.com"):
        self.headers = {"User-Agent": f"{app}/1.0 ({contact})"}
        self._cache = {}
    
    async def get(self, endpoint):
        # Implement with cache checking and error limit monitoring
        pass
    
    def ship_render_url(self, type_id, size=256):
        return f"{self.IMAGE}/types/{type_id}/render?size={size}"
```

### Create core/ship_sprites.py:
Pygame sprite loader that fetches from Image Server with local caching.

### Update constants.py - add enemy type mapping:
```python
ENEMY_TYPE_IDS = {
    "frigate": 587, "destroyer": 16242, "cruiser": 621,
    "battlecruiser": 24702, "battleship": 638, "boss": 23913
}
```

### Add to README.md:
Same CCP attribution block as EVE_Ships.

---

## PHASE 3: EVE_Gatekeeper - ESI Foundation

### Create app/esi_client.py:
Same ESI client pattern with full compliance.

### Create .env.example:
```
EVE_CLIENT_ID=your_client_id
EVE_CLIENT_SECRET=your_secret
EVE_CALLBACK_URL=http://localhost:8000/callback
```

### Create app/sde_importer.py stub:
```python
"""SDE Importer for EVE_Gatekeeper
Download: https://www.fuzzwork.co.uk/dump/latest/sqlite-latest.sqlite.bz2
"""
# Stub for importing systems, stargates, coordinates from Fuzzwork SQLite
```

### Key ESI endpoints for Gatekeeper:
```
/universe/systems/{id}/     # System info + stargates
/universe/stargates/{id}/   # Gate destinations  
/route/{origin}/{dest}/     # Route calculation
/universe/system_kills/     # Heatmap data
/universe/system_jumps/     # Activity data
/characters/{id}/location/  # SSO - character position
```

---

## ESI COMPLIANCE (Apply to ALL)

REQUIRED in every ESI client:
1. `User-Agent` header with app name + contact
2. Cache based on `Expires` header
3. Monitor `X-ESI-Error-Limit-Remain` (pause if <10)
4. Use `/latest/` versioned endpoints

FORBIDDEN:
- Iterating over IDs to discover entities (bannable)
- Ignoring cache headers
- Hardcoded secrets in code

---

## GIT AFTER EACH PHASE

```bash
git add . && git commit -m "Phase N complete" && git push
# EVE_Ships: use --force to replace old content
```

---

## SUCCESS = 

| Project | Deliverables |
|---------|-------------|
| EVE_Ships | 100+ renders, manifest.json, attribution |
| EVE_Rebellion | esi_client.py, ship_sprites.py, type mapping |
| EVE_Gatekeeper | esi_client.py, .env.example, sde stub |

Start with Phase 1. Execute autonomously. Report completion of each phase.
