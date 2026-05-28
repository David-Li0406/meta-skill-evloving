# Ghost Hunter Module

Create paranormal investigator characters and organizations that interact with wraiths.

## Ghost Hunter Types

| Type | Approach | Risk Level |
|------|----------|------------|
| **Scientific** | Equipment-focused investigation | Low |
| **Occult** | Ritual and magical methods | Medium |
| **Medium-Assisted** | Rely on psychic sensitives | Medium |
| **Skeptical** | Debunking, evidence analysis | Low |
| **Aggressive** | Exorcism, destruction | High |

---

## Quick NPC Stats

| Trait | Allocation |
|-------|------------|
| Attributes | 6/4/3 |
| Abilities | 11/7/4 |
| Willpower | 3-6 |
| Backgrounds | 3-5 |

---

## Creation Steps

1. **Individual or Team** — Solo hunter or organization member
2. **Methodology** — Scientific, Occult, or Intuitive
3. **Organization** — Select from `lookup.py mortals.ghost-hunting-organizations ghost-hunting-organizations`
4. **Role** — If team, assign team role
5. **Equipment** — From `lookup.py mortals.equipment equipment`
6. **Attributes** — Prioritize based on role
7. **Abilities** — Investigation, Technology, Occult key
8. **Motivation** — Knowledge, thrill, power, helping others
9. **Threat Level** — To wraiths

---

## Team Roles

| Role | Function | Key Abilities |
|------|----------|---------------|
| **Leader** | Coordination, decisions | Leadership, Investigation |
| **Tech Specialist** | Equipment, analysis | Technology, Computer, Science |
| **Researcher** | History, background | Academics, Investigation, Research |
| **Sensitive** | Psychic perception | Awareness, Empathy, Occult |
| **Skeptic** | Debunking, analysis | Investigation, Science |
| **Muscle** | Security, protection | Brawl, Athletics, Intimidation |

---

## Motivations

### Knowledge Seekers
- Academic research
- Understanding death
- Proving afterlife exists
- Scientific validation

### Thrill Seekers
- Excitement, danger
- Fame, recognition
- Content creation
- Adrenaline rush

### Power Seekers
- Control over spirits
- Supernatural abilities
- Influence, authority
- Artifact acquisition

### Helpers
- Assisting the living
- Helping the dead move on
- Protecting locations
- Religious duty

### Ghost Destroyers
- Eliminating threats
- Exorcism
- Protecting the living
- Religious mandate

---

## Threat Assessment (to Wraiths)

| Level | Description | Examples |
|-------|-------------|----------|
| **Minimal** | Bumbling amateurs | Reality TV crews, tourists |
| **Low** | Competent but harmless | Academic researchers |
| **Moderate** | Can disrupt activity | Experienced teams, sensitives |
| **High** | Can harm or trap wraiths | Occultists, organizations |
| **Severe** | Can destroy wraiths | Exorcists, Giovanni allies |

### Threat Indicators
- Access to mediums
- Occult knowledge
- Organizational resources
- Supernatural artifacts
- Cross-supernatural connections

---

## Equipment Packages

### Basic Kit (Rating •)
- Flashlight, extra batteries
- Digital camera
- Audio recorder
- EMF detector
- Temperature gauge

### Professional Kit (Rating •••)
- IR/Full spectrum cameras
- Multiple EVP recorders
- Motion detectors
- FLIR thermal camera
- Portable power supply
- Two-way radios

### Advanced Kit (Rating •••••)
- Wired camera system
- Environmental sensors
- Spirit boxes
- Kirlian camera (rare)
- Ghost trap (rare)
- Dowsing equipment

---

## Organizations Reference

### Knowledge Seekers
| Organization | Focus |
|--------------|-------|
| **The Arcanum** | Academic supernatural research |
| **Chamber of Corvi** | Artifact acquisition |

### Power Seekers
| Organization | Focus |
|--------------|-------|
| **FBI Special Affairs** | Government investigation |
| **Piercers of the Veil** | Aggressive investigation |

### Thrill Seekers
| Organization | Focus |
|--------------|-------|
| **Paranormal Investigation Collective** | Reality TV style |
| **Wisteria Prophets** | Séance-focused |

### Shadow Groups
| Organization | Focus | Patron |
|--------------|-------|--------|
| **Ashukhi Corporation** | Egyptian archaeology | Mummies |
| **Calypso Network** | Maritime hauntings | Unknown |
| **Centre of Unusual Occurrences** | Global coordination | Various |

### Other
| Organization | Focus |
|--------------|-------|
| **Hounds of Death** | Hunting dangerous spirits |
| **The Orphic Circle** | Classical Underworld traditions |
| **Sons of Tertullian** | Religious exorcism |
| **Terrel & Squib** | Professional investigation |

See `lookup.py mortals.ghost-hunting-organizations ghost-hunting-organizations` for details.

---

## Wraith Interaction Scenarios

### Investigation
- Hunters investigate location where wraith is active
- May expose Fetters, disrupt activity
- Could attract Hierarchy attention

### Evidence Gathering
- Recording wraith manifestations
- Public exposure risk
- May strengthen or weaken Shroud locally

### Communication Attempt
- Using medium or equipment to contact wraith
- Wraith may manipulate or use opportunity
- Risk of possession (if medium involved)

### Exorcism Attempt
- Direct threat to wraith
- May damage Fetters
- Could strengthen Shadow through trauma
- Success severs wraith from location

### Fetter Interference
- Removing or destroying potential Fetters
- Extremely dangerous to wraith
- May be unintentional

---

## Ghost Hunter as Antagonist

| Threat Type | Response Options |
|-------------|------------------|
| Exposure risk | Frighten away, mislead, discredit |
| Fetter threat | Protect, relocate, eliminate hunter |
| Exorcism | Fight, flee, negotiate |
| Capture attempt | Escape, overpower, call allies |

### Escalation Patterns
1. Initial investigation (curious)
2. Evidence found (excited)
3. Repeated encounters (obsessed)
4. Seek outside help (dangerous)
5. Attempt intervention (critical)

---

## Output Format

```markdown
# [Hunter/Team Name]

**Type**: [Individual/Team]
**Methodology**: [Scientific/Occult/Intuitive/Skeptical/Aggressive]
**Organization**: [If any]
**Threat Level**: [Minimal/Low/Moderate/High/Severe]

## Background
[How they got into ghost hunting]
[Notable experiences]
[Reputation]

## Motivation
[Primary drive]
[Secondary interests]
[What would make them stop]

## Members (if team)

### [Member Name]
**Role**: [Leader/Tech/Researcher/Sensitive/Skeptic/Muscle]
**Attributes**: Str [N], Dex [N], Sta [N]; Cha [N], Man [N], App [N]; Per [N], Int [N], Wits [N]
**Key Abilities**: [Ability] [N], [Ability] [N], [Ability] [N]
**Willpower**: [N]
**Notes**: [Personality, quirks]

[Repeat for each member]

## Equipment
- [Item]: [Rating/Description]
- [Item]: [Rating/Description]

## Artifacts (if any)
- [Artifact]: [Rating] — [Effect]

## Methods
[How they investigate]
[Standard procedures]
[Escalation responses]

## Vulnerabilities
[Weaknesses to exploit]
[Internal conflicts]
[Pressure points]

## Threat Assessment
[Specific dangers to wraiths]
[Potential for escalation]
[Connections to other supernaturals]
```

---

## Validation

- [ ] Type and methodology defined
- [ ] Organization selected (if applicable)
- [ ] Threat level assessed
- [ ] Equipment appropriate to methodology
- [ ] Motivations clear
- [ ] Team roles assigned (if team)
- [ ] Vulnerabilities identified
- [ ] Escalation potential considered

---

## Reference Data

```bash
# Organizations
python scripts/lookup.py mortals.ghost-hunting-organizations ghost-hunting-organizations "Arcanum"
python scripts/lookup.py mortals.ghost-hunting-organizations ghost-hunting-organizations "FBI"

# Equipment
python scripts/lookup.py mortals.equipment equipment "Kirlian"
python scripts/lookup.py mortals.equipment equipment "Ghost Trap"

# Artifacts
python scripts/lookup.py mortals.equipment equipment --find "artifact"
```
