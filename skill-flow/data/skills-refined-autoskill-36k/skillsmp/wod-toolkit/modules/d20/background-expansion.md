# Background Expansion Module

Maps Backgrounds to required sub-documents for PC creation.

## Overview

When creating a PC (not NPC), certain Backgrounds require linked documents to fully detail.

---

## Background → Module Mapping

| Background | Action | Module |
|------------|--------|--------|
| **Allies** | Create NPC document(s) | `modules/shared/mortal.md` |
| **Contacts** | List contact names and areas | (inline description OK) |
| **Eminence** | Note position, rivals, allies | (inline description OK) |
| **Fame** | Describe public persona | (inline description OK) |
| **Followers** | Create follower document(s) | `modules/d20/thrall.md` or `modules/shared/mortal.md` |
| **Influence** | Describe sphere and reach | (inline description OK) |
| **Legacy** | Detail pre-Fall memories | (inline description OK) |
| **Mentor** | Create NPC mentor document | `modules/shared/mortal.md` or demon NPC |
| **Pacts** | Create pact document(s) | `modules/d20/pact.md` |
| **Paragon** | Describe host's exceptional qualities | (inline description OK) |
| **Resources** | Source of wealth | (inline description OK) |

---

## When to Create Documents

### Always Create Documents

These Backgrounds should **always** have linked documents:

- **Allies** (at 2+ dots): Named NPC allies with stats
- **Followers** (at 2+ dots): Named followers with basic stats
- **Mentor**: Named NPC mentor with stats and relationship
- **Pacts** (any rating): Full pact terms documented

### Optional Documents

These Backgrounds can be handled inline but benefit from documents:

- **Contacts**: Named contacts with specialties
- **Eminence**: Description of reputation and position
- **Fame**: Public persona details
- **Legacy**: Detailed pre-Fall memories

---

## Document Requirements by Background Level

### Allies

| Rating | Requirement |
|--------|-------------|
| 1 | One ally; brief description OK |
| 2 | One-two allies; NPC document(s) recommended |
| 3+ | Multiple allies; NPC documents required |

### Followers

| Rating | Requirement |
|--------|-------------|
| 1 | One follower; brief description OK |
| 2 | Two followers; basic stats recommended |
| 3+ | Three+ followers; documents required |

### Pacts

| Rating | Requirement |
|--------|-------------|
| Any | Full pact document always required |

---

## File Structure

For a PC with relevant Backgrounds:

```
[character]/
├── [character].md          ← Main character sheet
├── npcs/
│   ├── ally-name.md        ← Ally documents
│   └── mentor-name.md      ← Mentor document
├── followers/
│   └── follower-name.md    ← Follower documents
└── pacts/
    └── pact-name.md        ← Pact documents
```

---

## Integration Notes

### Linking Documents

In the main character sheet, link to sub-documents:

```markdown
## Backgrounds

| Background | Rating | Details |
|------------|--------|---------|
| Allies | ●●●○○ | [Marcus Chen](./npcs/marcus-chen.md), [Dr. Rivera](./npcs/dr-rivera.md) |
| Followers | ●●○○○ | [Sarah](./followers/sarah.md), [Tom](./followers/tom.md) |
| Pacts | ●●○○○ | [Chen Pact](./pacts/chen-pact.md) |
```

### Validation

When validating a PC:
- [ ] All Allies at 2+ have NPC documents
- [ ] All Followers at 2+ have follower documents
- [ ] All Pacts have pact documents
- [ ] Mentor has NPC document
- [ ] All links resolve correctly
