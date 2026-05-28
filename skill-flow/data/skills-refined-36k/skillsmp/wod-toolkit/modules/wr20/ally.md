# Ally Module

Create companion NPCs—wraiths, mortals, or other beings who aid a character.

## Ally Types

| Type | Description | Module |
|------|-------------|--------|
| **Wraith Ally** | Fellow wraith | Use `modules/wraith.md` (NPC mode) |
| **Mortal Ally** | Living contact | This module |
| **Supernatural Ally** | Other beings | Story-specific |

---

## Mortal Ally Creation

### Quick NPC Stats

| Trait | Allocation |
|-------|------------|
| Attributes | 6/4/3 |
| Abilities | 9/5/3 |
| Willpower | 3-5 |
| Backgrounds | 3-5 |

### Creation Steps

1. **Role** — What do they do for the wraith?
2. **Relationship** — How do they know each other?
3. **Awareness** — Do they know about wraiths?
4. **Attributes** — Prioritize based on role
5. **Abilities** — Focus on useful skills
6. **Personality** — Brief characterization
7. **Motivation** — Why do they help?

---

## Mortal Awareness Levels

| Level | Description |
|-------|-------------|
| **Oblivious** | No idea the supernatural exists |
| **Sensitive** | Feels presences, has hunches |
| **Aware** | Knows something is there |
| **Informed** | Understands wraiths exist |
| **Medium** | Can perceive and communicate with wraiths |

### Mediums
- Rare and valuable
- Can see/hear wraiths without Arcanoi
- Often sought by multiple parties
- May have their own agendas

---

## Ally Roles

### Information
- Contacts in specific fields
- Access to records/databases
- Street-level knowledge
- Professional expertise

### Resources
- Money/equipment
- Safe houses
- Transportation
- Cover identities

### Skills
- Technical expertise
- Medical knowledge
- Legal representation
- Occult knowledge

### Access
- Location access
- Social circles
- Institutions
- Other supernaturals

---

## Output Format

```markdown
# [Ally Name]

**Type**: [Mortal/Wraith/Other]
**Role**: [Primary function]
**Awareness**: [Oblivious/Sensitive/Aware/Informed/Medium]

## Relationship
[How they know the wraith]
[History of the connection]

## Description
**Appearance**: [Physical description]
**Personality**: [Key traits]
**Motivation**: [Why they help]

## Statistics

### Attributes
**Physical**: Strength [N], Dexterity [N], Stamina [N]
**Social**: Charisma [N], Manipulation [N], Appearance [N]
**Mental**: Perception [N], Intelligence [N], Wits [N]

### Key Abilities
- [Ability]: [Rating]
- [Ability]: [Rating]
- [Ability]: [Rating]

### Other Traits
**Willpower**: [N]
**Notable Backgrounds**: [If any]

## Usefulness
[What they can do for the wraith]
[Their limitations]

## Complications
[Potential problems]
[Competing loyalties]
[Vulnerabilities]
```

---

## Validation

- [ ] Role clearly defined
- [ ] Relationship to wraith established
- [ ] Awareness level appropriate
- [ ] Stats match role
- [ ] Motivation makes sense
- [ ] Complications considered

---

## Wraith Allies

For wraith allies, use `modules/wraith.md` in NPC mode:
- Simplified creation
- Focus on relevant traits
- Document relationship to PC

---

## Reference Data

```bash
# Example allies
python scripts/lookup.py character.example-allies example-allies --keys
```
