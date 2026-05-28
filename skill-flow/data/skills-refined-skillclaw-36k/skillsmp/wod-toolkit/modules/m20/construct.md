# Construct Module

Create Technocratic Constructs (facilities) for M20.

## When to Use

Use this module instead of `chantry.md` when creating:
- Technocracy facilities of any size
- Research stations, field offices, orbital platforms
- Any location controlled by the Union

## Construct vs Chantry

| Element | Chantry | Construct |
|---------|---------|-----------|
| Organization | Informal hierarchy | Strict 6TP structure |
| Security | Wards, spirits | Tech, protocols, clearances |
| Resources | Backgrounds | Requisitions system |
| Personnel | Mages + consors | Operatives + Citizens |
| Naming | Mystic names | Technical designations |

## Dependencies

**Read `modules/background-expansion.md` for the complete background → module mapping.**

```
construct
├── node (for each Node background)
├── laboratory (for research facilities)
│   └── database (technical libraries)
├── sanctum (personal offices/labs)
├── horizon-realm (extradimensional facilities)
├── equipment (standard issue)
│   └── procedure
└── procedure (facility-wide effects)
```

**Read and invoke each sub-module for respective backgrounds.**

---

## Construct Classification

### By Size/Scope

| Class | Personnel | Scope | Examples |
|-------|-----------|-------|----------|
| **Outpost** | 5-20 | Local | Field office, safe house |
| **Station** | 20-100 | Regional | Research facility, regional HQ |
| **Complex** | 100-500 | National | Major research center, Convention hub |
| **Installation** | 500+ | Global | Orbital platform, dimensional station |

### By Function

| Type | Primary Purpose | Typical Convention |
|------|-----------------|-------------------|
| Research | R&D, experimentation | Iteration X, Progenitors |
| Operations | Field coordination | NWO, Void Engineers |
| Training | Personnel development | All |
| Production | Manufacturing | Iteration X, Progenitors |
| Financial | Economic operations | Syndicate |
| Surveillance | Intelligence gathering | NWO |
| Dimensional | Off-world/Umbral | Void Engineers |

---

## Construct Statistics

### Rank and Budget

| Points | Rank | Description |
|--------|------|-------------|
| 1-10 | 1 | Outpost, minimal |
| 11-20 | 2 | Station, established |
| 21-30 | 3 | Complex, significant |
| 31-70 | 4 | Installation, major |
| 71+ | 5 | Legendary/unique |

### Background Costs

| Cost/dot | Backgrounds |
|----------|-------------|
| 2 | Allies, Library (Database), Retainers |
| 3 | Node, Resources, Requisitions |
| 5 | Sanctum (Laboratory) |
| 10 | Horizon Realm (Dimensional Facility) |

---

## Personnel Structure

### 6TP Staffing

| Rank | Role in Construct | Typical Number |
|------|-------------------|----------------|
| T0 | Support staff, security, maintenance | 60-80% |
| T1 | Field operatives, technicians | 15-25% |
| T2 | Specialists, team leads | 5-10% |
| T3 | Department heads, supervisors | 2-5% |
| T4 | Construct commander | 1 (larger facilities) |
| T5 | Visiting/oversight only | Rare |

### Key Positions

| Position | Rank | Responsibilities |
|----------|------|------------------|
| Construct Director | T3-T4 | Overall command |
| Security Chief | T2-T3 | Protection, access control |
| Operations Lead | T2-T3 | Daily operations |
| Research Director | T3 | R&D oversight |
| Quartermaster | T2 | Supplies, requisitions |

---

## Security Systems

### Clearance Levels

| Level | Access | Holders |
|-------|--------|---------|
| **Public** | Lobby, front areas | Anyone |
| **Restricted** | Work areas | T0+ |
| **Classified** | Sensitive areas | T1+ |
| **Secret** | Research, armory | T2+ |
| **Top Secret** | Command, critical | T3+ |
| **Black** | Special projects | Need-to-know |

### Security Measures

| Type | Examples |
|------|----------|
| Physical | Barriers, locks, checkpoints |
| Electronic | Cameras, sensors, alarms |
| Biometric | Fingerprint, retinal, DNA |
| Enlightened | Wards, detection fields |
| Personnel | Guards, patrols, response teams |

---

## Standard Facilities

### Common Areas

| Facility | Function |
|----------|----------|
| Operations Center | Command and coordination |
| Armory | Equipment storage/distribution |
| Medical Bay | Treatment, enhancement |
| Cafeteria | Personnel support |
| Quarters | Residential (if applicable) |
| Training Room | Skill development |

### Specialized Areas

| Facility | Function | Convention |
|----------|----------|------------|
| Server Farm | Data processing | Iteration X, NWO |
| Bio Lab | Genetic research | Progenitors |
| Containment | RD/threat storage | All |
| Motor Pool | Vehicles | All |
| Launch Bay | Dimensional access | Void Engineers |
| Trading Floor | Financial ops | Syndicate |

---

## Front Organizations

Most Constructs maintain public covers:

| Cover Type | Examples |
|------------|----------|
| Corporate | Tech company, consulting firm, bank |
| Government | Research agency, military contractor |
| Academic | University lab, think tank |
| Medical | Hospital, clinic, pharma company |
| Industrial | Factory, warehouse, data center |

### Front Requirements

- Plausible explanation for personnel/activity
- Legitimate business operations
- Mundane security justification
- Public-facing staff (often T0)

---

## Creation Workflow

### Phase 1-2: Planning

1. **Concept** — Convention, function, location, budget
2. **Classification** — Size, type, front organization
3. **Research** — Query Convention-specific elements

### Phase 3: Plan Components

List all backgrounds requiring sub-modules.

### Phase 4-9: ⛔ CREATE SUB-DOCUMENTS (BLOCKING)

**Phase 4: Nodes**
- Read `modules/node.md`
- Create document per Node background
- Save to `./nodes/`

**Phase 5: Laboratories/Libraries**
- Research facilities use lab/database structure
- Read `modules/library.md` (adapt for technical databases)
- Save to `./laboratories/`, `./databases/`

**Phase 6: Sanctums**
- Personal offices, private labs
- Read `modules/sanctum.md`
- Save to `./offices/`

**Phase 7: Dimensional Facilities** (if applicable)
- Void Engineer stations, dimensional annexes
- Read `modules/horizon-realm.md`
- Save to `./dimensional/`

**Phase 8: Standard Equipment**
- Read `modules/technocratic-equipment.md`
- Document facility-wide resources
- Save to `./equipment/`

**Phase 9: Facility Procedures**
- Wards, security effects, communication
- Read `modules/procedure.md`
- Save to `./procedures/`

### Phases 10-15: Finalization

10. Personnel Roster
11. Security Protocols
12. History/Mission Document
13. Main Document (after all sub-components)
14. Cross-Linking Pass
15. Validation

---

## File Structure

```
[construct]/
├── [construct].md            ← Links to ALL
├── history.md
├── personnel/
│   ├── director.md
│   └── key_staff.md
├── nodes/
├── laboratories/
│   └── databases/
├── offices/
├── dimensional/              ← If applicable
├── equipment/
├── procedures/
└── locations/
    ├── operations_center.md
    └── containment.md
```

---

## Output Template

```markdown
# [Construct Designation]

**Convention:** [Primary] | **Class:** [Outpost/Station/Complex/Installation]
**Location:** [Physical location or "Classified"]
**Front:** [Cover organization]
**Rank:** [1-5] | **Points:** [Total budget]

## Mission
[Primary purpose and operational mandate]

## Personnel

### Command Staff
| Position | Name | Rank | Convention |
|----------|------|------|------------|
| Director | [Name] | T3 | [Convention] |

### Staffing Summary
| Rank | Count | Role |
|------|-------|------|
| T0 | [X] | Support |
| T1 | [X] | Operatives |
| T2 | [X] | Specialists |
| T3 | [X] | Supervisors |

## Facilities

| Area | Security | Document |
|------|----------|----------|
| Operations Center | Secret | [Link] |
| Research Lab Alpha | Top Secret | [Link] |

## Backgrounds

| Background | Rating | Document |
|------------|--------|----------|
| Node | ●●●○○ | [Power Core](./nodes/power_core.md) |
| Resources | ●●●●○ | Syndicate funding |

## Security

### Clearance Levels
[Access matrix]

### Defense Systems
[Physical, electronic, Enlightened]

## Standard Equipment
[Facility-wide resources, armory contents]

## Facility Procedures

| Procedure | Spheres | Document |
|-----------|---------|----------|
| [Perimeter Ward](./procedures/ward.md) | Forces 2, Prime 2 | Security |

## History
[Establishment, major events, current status]

## Current Operations
[Active projects, ongoing missions]
```

---

## Reference Data

```bash
# Convention specifics
python scripts/lookup.py technocracy.conventions conventions "Void Engineers"

# Equipment for armory
python scripts/lookup.py technocracy.equipment equipment --keys

# Methodology staffing
python scripts/lookup.py technocracy.methodologies methodologies "NSC"
```

---

## Validation

- [ ] Convention affiliation clear
- [ ] Classification appropriate for scope
- [ ] Front organization plausible
- [ ] Personnel structure follows 6TP
- [ ] All Node backgrounds have documents
- [ ] All Laboratory backgrounds have documents
- [ ] All Sanctum backgrounds have documents
- [ ] Dimensional facilities (if any) documented
- [ ] Standard equipment listed
- [ ] Facility procedures documented
- [ ] Security clearance matrix complete
- [ ] Point budget balanced
- [ ] All links valid
