# EVE Projects Master Update - Claude Code Mission Brief

You are helping ARETE update his EVE Online development portfolio. Execute these tasks systematically.

## Project Inventory

| Project | Path | Type | Current State |
|---------|------|------|---------------|
| EVE_Rebellion | ~/projects/EVE_Rebellion | Pygame arcade game | Working, needs ESI sprites |
| EVE_Gatekeeper | ~/projects/EVE_Gatekeeper | FastAPI 2D starmap | Architecture done, needs implementation |
| EVE_Ships | ~/projects/EVE_Ships | Asset collection | Replace with official renders |

## Mission Objectives

### Phase 1: EVE_Ships Complete Rebuild (Priority)

**Goal:** Replace entire repo with official EVE Image Server renders

**Execute:**
```bash
pip install httpx

# Create rebuild script and run it
cd ~/projects
# The rebuild script downloads 120+ ships from images.evetech.net
# Organizes by class and faction
# Creates manifest.json with type IDs
# Adds proper CCP attribution
```

**Ship Database to Download:**
- Frigates: rifter(587), tristan(593), merlin(603), punisher(597), + 20 more
- Destroyers: thrasher(16242), catalyst(16240), cormorant(16238), coercer(16236), + 4 more
- Cruisers: caracal(621), thorax(627), maller(624), stabber(622), + 12 more
- Battlecruisers: drake(24690), hurricane(24702), harbinger(24696), + 9 more
- Battleships: raven(638), megathron(641), machariel(17738), + 9 more
- Faction: gila, stratios(33470), nightmare(17736), vindicator(17740), + 14 more
- Capitals: naglfar(19724), nyx(23913), avatar(11567), rorqual(28352), + 12 more

**Image Server URL Pattern:**
```
https://images.evetech.net/types/{type_id}/render?size={256|512}
```

**Required Output Structure:**
```
EVE_Ships/
├── renders/
│   ├── 256/{shipname}_{typeid}.png
│   └── 512/{shipname}_{typeid}.png
├── by_faction/{faction}/ (symlinks)
├── by_class/{class}/ (symlinks)
├── manifest.json
├── README.md (with CCP attribution)
└── .gitignore
```

**README Must Include:**
```markdown
## Attribution
EVE Online and the EVE logo are registered trademarks of CCP hf.
Ship images are property of CCP, used under Content Creation Terms.
https://community.eveonline.com/support/policies/content-creation-terms-of-use/
```

---

### Phase 2: EVE_Rebellion ESI Integration

**Goal:** Add ESI client and ship sprites from Image Server

**Tasks:**
1. Create `core/esi_client.py` with compliant ESI client
2. Create `core/ship_sprites.py` to load renders from Image Server
3. Map enemy types to real EVE type IDs in constants.py
4. Add CCP attribution to README.md
5. Link sprites from EVE_Ships or download directly

**ESI Client Requirements (CCP Compliance):**
```python
# REQUIRED: User-Agent header
headers = {"User-Agent": "EVE_Rebellion/1.0 (contact@email.com)"}

# REQUIRED: Respect cache headers
# Check response.headers["Expires"] before re-requesting

# REQUIRED: Monitor error budget
# X-ESI-Error-Limit-Remain header - pause if < 10

# FORBIDDEN: Discovery patterns
# Never iterate over IDs to find entities
```

**Enemy Type ID Mapping for constants.py:**
```python
ENEMY_SHIPS = {
    "frigate": 587,      # Rifter
    "destroyer": 16242,  # Thrasher
    "cruiser": 621,      # Caracal
    "battlecruiser": 24702,  # Hurricane
    "battleship": 638,   # Raven
    "boss": 23913,       # Nyx supercarrier
}
```

---

### Phase 3: EVE_Gatekeeper Foundation

**Goal:** Set up ESI client and prepare for SDE import

**Tasks:**
1. Create compliant ESI client in `app/esi_client.py`
2. Create `.env.example` for credentials
3. Create SDE importer stub for Fuzzwork SQLite
4. Add CCP attribution to README.md

**Required ESI Endpoints for Gatekeeper:**
```
# Public (no auth)
GET /universe/systems/                    # All 8,285 system IDs
GET /universe/systems/{id}/               # System details + stargates
GET /universe/stargates/{id}/             # Gate destinations
GET /route/{origin}/{destination}/        # Route calculation
GET /universe/system_kills/               # Kill heatmap data
GET /universe/system_jumps/               # Jump activity data

# Auth required (SSO)
GET /characters/{id}/location/            # Character position
POST /ui/autopilot/waypoint/              # Set waypoint in client
```

**SSO Scopes Needed:**
- esi-location.read_location.v1
- esi-location.read_online.v1  
- esi-ui.write_waypoint.v1
- esi-assets.read_assets.v1 (optional)

**SDE Source:**
- https://www.fuzzwork.co.uk/dump/latest/sqlite-latest.sqlite.bz2

---

## Compliance Checklist (Apply to ALL Projects)

Every project using ESI must have:

- [ ] User-Agent header with app name + contact email
- [ ] Cache handling (respect Expires header)
- [ ] Error limit monitoring (X-ESI-Error-Limit-Remain)
- [ ] No discovery abuse patterns (no ID iteration loops)
- [ ] Rate limiting for bulk operations
- [ ] Versioned endpoints (/latest/ or /v{n}/)
- [ ] CCP attribution in README

---

## Git Workflow After Updates

```bash
# For each project after updates:
cd ~/projects/{PROJECT}
git add .
git commit -m "Add ESI integration and CCP attribution"
git push

# For EVE_Ships (full rebuild):
cd ~/projects/EVE_Ships
git add .
git commit -m "Rebuild with official EVE Image Server renders"
git push --force  # Force push to replace old content
```

---

## Success Criteria

| Project | Before | After | Key Deliverable |
|---------|--------|-------|-----------------|
| EVE_Ships | C (50) | A (95) | 120+ official renders, manifest.json |
| EVE_Rebellion | A- (85) | A (95) | ESI client, sprite loader, attribution |
| EVE_Gatekeeper | B- (70) | B+ (82) | ESI client, .env setup, SDE stub |

---

## Execute Order

1. **EVE_Ships** - Complete rebuild with Image Server (15 min)
2. **EVE_Rebellion** - Add ESI client + sprites (10 min)
3. **EVE_Gatekeeper** - Add ESI client + setup (10 min)
4. **Git push all** - Commit and push (5 min)

Total time: ~40 minutes

---

## Reference: Common Type IDs

```python
# Frigates
RIFTER = 587
TRISTAN = 593
MERLIN = 603
PUNISHER = 597

# Cruisers
CARACAL = 621
THORAX = 627
MALLER = 624
STABBER = 622

# Battlecruisers
DRAKE = 24690
HURRICANE = 24702
HARBINGER = 24696

# Battleships
RAVEN = 638
MEGATHRON = 641
MACHARIEL = 17738
NIGHTMARE = 17736

# Capitals
NAGLFAR = 19724
NYX = 23913
AVATAR = 11567
RORQUAL = 28352

# Faction
GILA = 17715
STRATIOS = 33470
ASTERO = 33468
```

---

## Start Execution

Begin with Phase 1 (EVE_Ships rebuild). Create the download script, execute it, verify the output structure, then proceed to Phase 2.

Ask for clarification if any project paths differ from expected.
