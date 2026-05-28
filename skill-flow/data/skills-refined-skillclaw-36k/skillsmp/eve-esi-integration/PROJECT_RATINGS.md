# EVE Projects Compliance Rating & Integration Roadmap

## Overall Assessment

Based on analysis of your EVE projects from past conversations, here's how each project rates against CCP's ESI guidelines and best practices.

---

## 📊 Project Ratings

### 1. EVE_Rebellion (Arcade Space Shooter)

**Current ESI Usage:** None (standalone game)
**Compliance Score:** N/A (100% - no violations possible)

| Aspect | Status | Notes |
|--------|--------|-------|
| ESI Integration | ❌ None | Procedural generation only |
| Image Server | ❌ None | Custom procedural sprites |
| User-Agent | N/A | No API calls |
| Cache Handling | N/A | No API calls |
| Rate Limiting | N/A | No API calls |

**Current State:**
- ✅ Data-driven architecture (JSON configs)
- ✅ Procedural audio system
- ✅ Multiple enemy AI patterns
- ✅ Stage progression system
- ✅ MIT License

**Integration Opportunities:**

| Feature | ESI Source | Difficulty | Value |
|---------|-----------|------------|-------|
| Ship sprites from Image Server | `/types/{id}/render` | Easy | High |
| Real ship stats for enemies | `/universe/types/{id}/` | Easy | Medium |
| Leaderboards (zkillboard API) | External | Medium | Low |
| In-game faction lore | `/universe/factions/` | Easy | Low |

**Priority Actions:**
1. 🎯 Replace placeholder sprites with Image Server renders
2. 📊 Map enemy JSON configs to real type IDs for authenticity
3. 📁 Add image attribution in README

**Grade: A** (clean standalone project, great integration potential)

---

### 2. EVE_Starmap (Mobile 2D Navigation)

**Current ESI Usage:** Planned but not implemented
**Compliance Score:** Pending implementation

| Aspect | Status | Notes |
|--------|--------|-------|
| ESI Integration | 📐 Designed | Architecture documented |
| Image Server | ❌ Not yet | Could use for system icons |
| User-Agent | ⚠️ Required | Must add before launch |
| Cache Handling | ⚠️ Required | Critical for 8k+ systems |
| Rate Limiting | ⚠️ Required | Especially for live layers |
| SDE Usage | 📐 Planned | Correct approach for bulk data |

**Current State:**
- ✅ Architecture documented (FastAPI + React)
- ✅ SDE importer designed
- ✅ Layer system planned (kills, jumps, sov)
- ✅ Route planning via ESI `/route/` endpoint
- ⚠️ Implementation incomplete

**Integration Requirements:**

| Component | ESI Endpoints | Scopes Needed |
|-----------|--------------|---------------|
| Base map | SDE (offline) | None |
| Live heatmaps | `/universe/system_kills/`, `/system_jumps/` | None |
| Route planning | `/route/{origin}/{dest}/` | None |
| Character location | `/characters/{id}/location/` | `esi-location.read_location.v1` |
| Set waypoint | POST `/ui/autopilot/waypoint/` | `esi-ui.write_waypoint.v1` |
| Asset overlay | `/characters/{id}/assets/` | `esi-assets.read_assets.v1` |

**Priority Actions:**
1. 🚀 Implement SDE importer first (avoid 8k ESI calls)
2. 🔧 Add ESI client class with User-Agent + caching
3. 🔐 Set up SSO app registration
4. 📊 Implement live layers with 5-min cache
5. 🧪 Add compliance checker to CI

**Grade: B** (well-designed, needs implementation with compliance baked in)

---

### 3. EVE_Ships (SVG Asset Collection)

**Current ESI Usage:** Unknown (minimal codebase info)
**Compliance Score:** Likely N/A

| Aspect | Status | Notes |
|--------|--------|-------|
| ESI Integration | ❓ Unknown | Likely manual asset collection |
| Image Server | 🔄 Opportunity | Could automate fetching |
| Attribution | ⚠️ Required | CCP content requires attribution |

**Current State:**
- SVG ship files (manual collection?)
- GitHub repository exists

**Integration Opportunities:**

| Feature | Approach | Value |
|---------|----------|-------|
| Automated render fetching | `scripts/fetch_ship_renders.py` | High |
| Type ID metadata | ESI `/universe/types/` | Medium |
| Ship class organization | ESI categories | Medium |

**Priority Actions:**
1. 📦 Use `fetch_ship_renders.py` to bulk download
2. 📝 Add manifest.json with type IDs
3. 📄 Add CCP attribution to README
4. 🏷️ Organize by ship class from ESI categories

**Grade: C** (unclear state, needs organization and attribution)

---

### 4. Overview Project (Mentioned but not detailed)

**Current ESI Usage:** Unknown
**Compliance Score:** Unknown

Based on the name, this likely involves:
- EVE client overview settings
- Bracket configurations
- UI customization

**Potential ESI Touchpoints:**
- `/ui/` endpoints for client interaction
- Type/category data for bracket organization
- Ship class definitions

**Grade: Incomplete** (need more information)

---

## 🎯 Recommended Integration Order

```
Week 1-2: EVE_Ships
├── Run fetch_ship_renders.py for all ships
├── Add CCP attribution
└── Organize by class

Week 3-4: EVE_Rebellion  
├── Map enemy types to real type IDs
├── Replace sprites with Image Server renders
└── Update README with EVE attribution

Week 5-8: EVE_Starmap
├── Implement SDE importer
├── Build ESI client with compliance
├── Register SSO application
├── Implement public endpoints
└── Add auth endpoints
```

---

## 🔧 Common Requirements for All Projects

### 1. ESI Client Template

Every project using ESI should include:

```python
class ESIClient:
    def __init__(self, app_name: str, contact: str):
        self.headers = {
            "User-Agent": f"{app_name}/1.0 ({contact})",
            "Accept": "application/json"
        }
        self._cache = {}
    
    async def get(self, endpoint: str) -> dict:
        # Check cache before requesting
        # Monitor X-ESI-Error-Limit-Remain
        # Respect Expires header
        pass
```

### 2. Attribution

Add to README:

```markdown
## Attribution

EVE Online and the EVE logo are registered trademarks of CCP hf.
Ship images and game data provided via [EVE Online API](https://developers.eveonline.com/).
This project is not affiliated with or endorsed by CCP.
```

### 3. License Consideration

Your MIT license is fine for your code, but note:
- EVE assets remain CCP's property
- Link to CCP's [Content Creation Terms](https://community.eveonline.com/support/policies/content-creation-terms-of-use/)

---

## 📋 Quick Compliance Checklist

Before releasing any EVE project:

- [ ] User-Agent header set with contact info
- [ ] Cache headers respected (don't poll faster than Expires)
- [ ] Error limit headers monitored (100 errors/60s = ban)
- [ ] No discovery patterns (iterating IDs is bannable)
- [ ] SDE used for bulk data (not ESI loops)
- [ ] CCP attribution in README
- [ ] Content Creation Terms linked
- [ ] Rate limiting for bulk operations
- [ ] Versioned endpoints (/latest/ or /v{n}/)
- [ ] Secrets in environment variables (not code)

---

## 📦 Using the Skill

Install the eve-esi-integration skill in Claude Code:

```bash
# Check compliance on any project
python /path/to/skill/scripts/esi_compliance_check.py /path/to/project

# Download ship renders
python /path/to/skill/scripts/fetch_ship_renders.py --all-frigates -o ./ships

# Reference documentation
cat /path/to/skill/references/sso-flow.md
cat /path/to/skill/references/endpoints-map.md
cat /path/to/skill/references/image-server.md
```

---

## Summary

| Project | Current Grade | Post-Integration Target |
|---------|---------------|------------------------|
| EVE_Rebellion | A | A+ (with real assets) |
| EVE_Starmap | B | A (with full compliance) |
| EVE_Ships | C | A (with automation) |
| Overview | ? | TBD |

**Overall Portfolio Grade: B+**

Strong architecture across projects, but ESI integration is mostly planned rather than implemented. The skill and scripts provided will accelerate bringing all projects into full compliance.
