# Amalgam Module

Create Technocratic Amalgams (teams) for M20.

## When to Use

Use this module instead of creating informal cabals when:
- Building a Technocracy player character group
- Creating NPC Technocratic field teams
- Documenting operational units

## Amalgam vs Cabal

| Element | Cabal | Amalgam |
|---------|-------|---------|
| Formation | Voluntary | Assigned |
| Leadership | Informal/rotating | Chain of command |
| Composition | Same Tradition (usually) | Cross-Convention possible |
| Mission | Self-directed | Mission-assigned |
| Equipment | Personal | Requisitioned |
| Reporting | To mentor/chantry | To Symposium |

---

## Amalgam Types

### By Mission Profile

| Type | Function | Typical Composition |
|------|----------|---------------------|
| **Field Ops** | Direct action | Mixed combat specialists |
| **Intelligence** | Surveillance, infiltration | NWO-heavy |
| **Research** | Investigation, analysis | Convention specialists |
| **Containment** | RD capture/neutralization | Heavy hitters |
| **Diplomatic** | Cross-faction liaison | Experienced agents |
| **Special Projects** | Classified | Need-to-know |

### By Convention Mix

| Type | Description |
|------|-------------|
| **Single-Convention** | All members from one Convention |
| **Cross-Convention** | Mixed Conventions (standard) |
| **Joint Task Force** | Temporary for specific mission |
| **Scrum Team** (It X) | Iteration X rapid-response |

---

## Chain of Command

### Standard Hierarchy

| Role | Rank | Responsibilities |
|------|------|------------------|
| **Team Lead** | T2-T3 | Tactical command, mission execution |
| **Second** | T2 | Backup lead, specialty coordination |
| **Specialists** | T1-T2 | Role-specific tasks |
| **Support** | T0-T1 | Logistics, cover, backup |

### Reporting Structure

```
Symposium (T4)
    │
Construct Director (T3)
    │
Team Lead (T2-T3)
    │
├── Second (T2)
├── Specialist A (T1-T2)
├── Specialist B (T1-T2)
└── Support (T0-T1)
```

---

## Team Roles

### Combat Roles

| Role | Function | Typical Convention |
|------|----------|-------------------|
| Point | First contact, breach | Iteration X, Void Engineers |
| Heavy | Firepower, suppression | Iteration X |
| Sniper | Precision, overwatch | NWO, Void Engineers |
| Medic | Field treatment | Progenitors |
| Tech | Equipment, hacking | Iteration X, NWO |

### Support Roles

| Role | Function | Typical Convention |
|------|----------|-------------------|
| Face | Social interaction | Syndicate, NWO |
| Intel | Information gathering | NWO |
| Driver | Transportation, escape | Any |
| Handler | Asset management | NWO, Syndicate |
| Cleaner | Evidence disposal | NWO |

### Specialist Roles

| Role | Function | Typical Convention |
|------|----------|-------------------|
| Reality Specialist | RD identification/counter | Void Engineers |
| Biohazard | Biological threats | Progenitors |
| Financial | Money trail/manipulation | Syndicate |
| Psych Ops | Mental influence | NWO |
| Dimensional | Umbral operations | Void Engineers |

---

## Standard Equipment

### Team-Level Resources

| Resource | Purpose |
|----------|---------|
| Communications | Secure team comms (ES-Phones) |
| Transport | Vehicle(s) appropriate to mission |
| Armory | Shared weapons/equipment |
| Safe House | Emergency fallback location |
| Funds | Operational budget |

### Individual Loadouts

Each member receives standard issue based on role:

| Role | Standard Loadout |
|------|-----------------|
| Combat | Sidearm, primary weapon, armor, medkit |
| Technical | Toolkit, computer gear, diagnostic devices |
| Social | Recording equipment, credentials, funds |
| Medical | Full medkit, drugs, surgical tools |
| General | ES-Phone, ID, basic self-defense |

---

## Mission Parameters

### Mission Types

| Type | Objective | Risk Level |
|------|-----------|------------|
| Surveillance | Observe, report | Low |
| Investigation | Gather evidence | Low-Medium |
| Acquisition | Retrieve target/asset | Medium |
| Neutralization | Eliminate threat | High |
| Containment | Capture, secure | High |
| Extraction | Remove friendly asset | Variable |
| Cleanup | Cover traces | Low-Medium |

### Rules of Engagement

Technocratic amalgams operate under strict RoE:

| Threshold | Response Authorized |
|-----------|---------------------|
| T1 | Observation only |
| T2 | Minimal intervention |
| T3 | Standard force |
| T4 | Significant force |
| T5 | Heavy response |
| T6 | Degree Absolute |

Reference: `lookup.py technocracy.rules-of-engagement rules-of-engagement`

---

## Creation Workflow

1. **Mission Profile** — What is this team for?
2. **Convention Mix** — Single or cross-Convention?
3. **Chain of Command** — Leadership structure
4. **Roles** — Assign team roles
5. **Members** — Create or reference characters
6. **Equipment** — Standard loadout + specialties
7. **Reporting** — To which Construct/Symposium?
8. **History** — Formation, notable operations
9. **Document** — Full write-up

---

## Amalgam Statistics

### Team Ratings

| Aspect | Rating | Description |
|--------|--------|-------------|
| **Cohesion** | 1-5 | How well they work together |
| **Experience** | 1-5 | Combined operational history |
| **Resources** | 1-5 | Equipment/funding access |
| **Reputation** | 1-5 | Standing within Union |

### Team Size

| Size | Members | Typical Use |
|------|---------|-------------|
| Fire Team | 3-4 | Surgical strikes |
| Squad | 5-8 | Standard operations |
| Platoon | 9-20 | Major operations |
| Company | 20+ | War footing |

---

## File Structure

```
[amalgam]/
├── [amalgam].md              ← Main document
├── members/
│   ├── team_lead.md
│   ├── specialist_a.md
│   └── specialist_b.md
├── equipment/
│   └── team_gear.md
├── operations/
│   ├── mission_001.md
│   └── mission_002.md
└── protocols/
    └── standard_procedures.md
```

---

## Output Template

```markdown
# [Amalgam Designation]

**Type:** [Field Ops/Intelligence/Research/etc.]
**Convention Mix:** [Single/Cross-Convention]
**Reporting To:** [Construct/Symposium]
**Status:** [Active/Reserve/Disbanded]

## Mission Profile
[Primary operational mandate]

## Chain of Command

| Role | Name | Rank | Convention | Document |
|------|------|------|------------|----------|
| Team Lead | [Name] | T2 | NWO | [Link] |
| Second | [Name] | T2 | Iteration X | [Link] |
| Specialist | [Name] | T1 | Progenitors | [Link] |

## Team Roles

| Member | Combat Role | Support Role |
|--------|-------------|--------------|
| [Name] | Point | — |
| [Name] | Tech | Intel |
| [Name] | Medic | — |

## Standard Equipment

### Team Resources
| Resource | Details |
|----------|---------|
| Transport | [Vehicle type] |
| Safe House | [Location] |
| Comms | Encrypted ES-Phone network |

### Individual Loadouts
[Role-specific equipment lists]

## Operational History

### Formation
[When, why, by whom]

### Notable Operations
| Operation | Date | Outcome |
|-----------|------|---------|
| [Name] | [Date] | [Success/Failure/Ongoing] |

## Team Statistics

| Aspect | Rating |
|--------|--------|
| Cohesion | ●●●○○ |
| Experience | ●●○○○ |
| Resources | ●●●●○ |
| Reputation | ●●●○○ |

## Current Status
[Active assignment, standing orders]

## Protocols
[Standard operating procedures, emergency protocols]
```

---

## Integration with Other Modules

### Character Creation
- Use `modules/technocrat.md` for individual members
- Link member documents to amalgam

### Equipment
- Use `modules/technocratic-equipment.md` for team gear
- Track what's team property vs individual

### Construct
- Amalgams report to Constructs
- May be based at a Construct
- Use `modules/construct.md` for home base

---

## Reference Data

```bash
# Convention specialties
python scripts/lookup.py technocracy.conventions conventions "Iteration X"

# Equipment for loadouts
python scripts/lookup.py technocracy.equipment equipment --keys

# Rules of engagement
python scripts/lookup.py technocracy.rules-of-engagement rules-of-engagement "T4"
```

---

## Validation

- [ ] Mission profile clear
- [ ] Chain of command established
- [ ] All roles filled
- [ ] Member documents linked or created
- [ ] Equipment appropriate for mission type
- [ ] Reporting structure identified
- [ ] Team statistics assigned
- [ ] Operational history documented
- [ ] All links valid
