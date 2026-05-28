# Motley Module

Create motleys, oathcircles, and households for C20—changeling groups bound by purpose, oath, or service.

## Group Types

| Type | Description | Binding |
|------|-------------|---------|
| **Motley** | Commoner group, informal | Friendship, mutual aid |
| **Oathcircle** | Formally oath-bound group | Sworn oath |
| **Household** | Noble retinue | Oath of Fealty |
| **Entourage** | Mixed group with leader | Varied |

---

## Dependencies

```
motley/oathcircle
├── character (each member)
├── oath (binding oaths)
├── freehold (shared holdings)
└── treasure (shared items)
```

**Read and invoke each sub-module for relevant components.**

## What This Creates

1. **Main Document** — Group concept, structure
2. **Member Documents** — Via `modules/character.md`
3. **Binding Oath** — Via `modules/oath.md`
4. **Shared Resources** — Holdings, treasures
5. **Group History** — Formation, adventures

---

## Creation Workflow

### Phase 1: Concept

1. **Group Type** — Motley, Oathcircle, or Household
2. **Purpose** — Why they exist
3. **Theme** — Unifying aesthetic/approach
4. **Size** — Number of members
5. **Territory** — Where they operate

### Phase 2: Structure

1. **Leadership** — Who leads (if any)
2. **Hierarchy** — Structure of authority
3. **Roles** — What each member does
4. **Court Mix** — Seelie/Unseelie balance

### Phase 3: ⛔ MEMBER CREATION (BLOCKING)

For each member:
- Read `modules/character.md`
- Create full character document
- Save to `./members/`

### Phase 4: Binding

If Oathcircle or Household:
- Read `modules/oath.md`
- Define the binding oath
- Document oath terms and penalties

### Phase 5: Shared Resources

Document shared assets:
- Holdings (fractional per member)
- Treasures (communal items)
- Chimera (group mascots, guardians)
- Contacts/allies

### Phase 6: Finalization

1. Group History
2. Current Situation
3. Main Document
4. Cross-linking
5. Validation

---

## Motley Specifics

### What is a Motley?

Informal group of commoner changelings—friends, partners, found family. No formal oath required, but loyalty expected.

### Motley Characteristics

| Aspect | Typical |
|--------|---------|
| Size | 3-7 members |
| Leadership | Informal, rotating, or none |
| Binding | Friendship, mutual benefit |
| Court | Usually mixed |
| Territory | Neighborhood, city district |

### Common Motley Types

| Type | Focus |
|------|-------|
| Street Gang | Survival, territory |
| Artist Collective | Creative Glamour |
| Quest Party | Adventures in Dreaming |
| Rebels | Fighting noble oppression |
| Outcasts | Mutual protection |

---

## Oathcircle Specifics

### What is an Oathcircle?

Group formally bound by sworn oath. Oath violation has magical consequences. More serious than motley, but not as rigid as household.

### Oathcircle Characteristics

| Aspect | Typical |
|--------|---------|
| Size | 2-9 members |
| Leadership | Often equal partnership |
| Binding | Formal oath (see below) |
| Court | May be single or mixed |
| Purpose | Specific goal or eternal bond |

### Common Binding Oaths

| Oath | Purpose |
|------|---------|
| Oath of Clasped Hands | Deep friendship, life-bond |
| Oath of the Long Road | Shared quest |
| Oath of the Truehearts | Romantic/loyalty bond |
| Custom Oath | Specific purpose |

Reference: `modules/oath.md`

---

## Household Specifics

### What is a Household?

Noble retinue—servants, guards, advisors bound by Oath of Fealty to a noble. Hierarchical structure.

### Household Characteristics

| Aspect | Typical |
|--------|---------|
| Size | 5-20+ members |
| Leadership | Single noble (Lord/Lady) |
| Binding | Oath of Fealty |
| Court | Usually leader's court |
| Purpose | Serve the noble |

### Household Roles

| Role | Responsibility |
|------|----------------|
| Lord/Lady | Leader, oath-holder |
| Seneschal | Manages household |
| Champion | Primary warrior |
| Bard | Entertainment, news |
| Steward | Manages resources |
| Guards | Security |
| Servants | Day-to-day tasks |

---

## Shared Resources

### Holdings
Group freehold access:
- Divide Holdings dots among members
- Example: Group with Holdings 4 = four 1-dot shares or two 2-dot shares
- Document in freehold file

### Treasures
Communal magical items:
- Belong to group, not individuals
- May have rules for use
- Document in treasures folder

### Group Chimera
Shared chimerical companions:
- Mascots, guardians, mounts
- May be bonded to group rather than individual
- Document in chimera folder

---

## File Structure

```
[group]/
├── [group].md              ← Main document
├── members/                ← Character documents
│   ├── [member1].md
│   └── [member2].md
├── oaths/                  ← If oathcircle
│   └── binding_oath.md
├── chimera/                ← Shared chimera
├── treasures/              ← Shared items
└── freehold/               ← If shared holdings
```

---

## Output Format

```markdown
# [Group Name]

**Type**: [Motley/Oathcircle/Household]
**Size**: [N] members
**Court Affiliation**: [Seelie/Unseelie/Mixed]
**Territory**: [Location]
**Founded**: [When]

## Concept
[What this group is about]

## Purpose
[Why they exist, what they do]

## Binding
**Type**: [Oath name or "Informal"]
**Terms**: [Summary of obligations]
**Penalty**: [Consequences of breaking]
[Link to full oath document if applicable]

## Leadership

| Role | Member | Authority |
|------|--------|-----------|
| [Role] | [Name](./members/name.md) | [What they control] |

## Members

| Name | Kith | Court | Role | Document |
|------|------|-------|------|----------|
| [Name] | [Kith] | [Court] | [Role] | [Link](./members/name.md) |

## Shared Resources

### Holdings
| Freehold | Group Rating | Document |
|----------|--------------|----------|
| [Name] | ●●●○○ | [Link](./freehold/name.md) |

### Treasures
| Treasure | Type | Document |
|----------|------|----------|
| [Name] | [Type] | [Link](./treasures/name.md) |

### Chimera
| Chimera | Type | Document |
|---------|------|----------|
| [Name] | [Type] | [Link](./chimera/name.md) |

## Territory
[Description of area they control/operate in]

## Relationships

### Allies
| Group/Individual | Nature |
|------------------|--------|
| [Name] | [Relationship] |

### Enemies
| Group/Individual | Conflict |
|------------------|----------|
| [Name] | [Nature of conflict] |

## History

### Formation
[How the group came together]

### Key Events
| Date | Event |
|------|-------|
| [When] | [What happened] |

## Current Situation
[Present-day status, ongoing plots]

## Group Dynamics
[How members interact, internal tensions]
```

---

## Validation

### All Groups
- [ ] Type specified
- [ ] All members have character documents
- [ ] Court affiliations noted
- [ ] Leadership/structure defined
- [ ] All links valid

### Oathcircles
- [ ] Binding oath documented
- [ ] Oath penalties specified
- [ ] `modules/oath.md` consulted

### Households
- [ ] Noble leader specified
- [ ] Oath of Fealty documented
- [ ] Hierarchy clear
- [ ] Roles assigned

### Shared Resources
- [ ] Holdings divided among members
- [ ] Shared treasures documented
- [ ] Group chimera documented

---

## Reference Data

```bash
# Motley examples
python scripts/lookup.py rules.group-examples group-examples "motley"

# Common oaths
python scripts/lookup.py rules.oaths oaths "Clasped Hands"

# Household roles
python scripts/lookup.py rules.household-roles household-roles --all
```
