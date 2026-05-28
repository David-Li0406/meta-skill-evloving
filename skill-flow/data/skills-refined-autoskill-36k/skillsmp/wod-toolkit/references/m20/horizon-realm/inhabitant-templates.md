# Inhabitant Profile Templates

Create profiles for important inhabitants based on People and Ephemera ratings.

## When to Create Profiles

| Rating | Requirement |
|--------|-------------|
| People 2+ | 3-5 named NPCs |
| People 3+ | Community leaders, faction representatives |
| People 4-5 | Multiple named individuals from each supernatural type |
| Ephemera 3+ | Named spirits with personalities |
| Ephemera 4-5 | Spirit hierarchy with detailed leadership |

## Mage Inhabitant Template

Create in `inhabitants/mages/[name].md`:

```markdown
# [Mage Name]

**Tradition/Convention:** [Name] | **Arete:** [Rating] | **Essence:** [Type]

**Primary Spheres:** [Sphere] [Rating], [Sphere] [Rating], [Sphere] [Rating]

**Role in Realm:** [Position/occupation]

## Background

[2-3 paragraphs: who they are, why here, history with Realm, goals]

## Appearance and Demeanor

[Physical description and personality]

## Magical Focus

**Paradigm:** [Worldview]
**Practice:** [Primary Practice]
**Instruments:** [Common foci]

## Sanctum

[Link to sanctum file or describe space]

## Items

- [Item name](../../items/[item].md) - [Brief description]

## Relationships

- [Person](../people/[name].md) - [Relationship]
- [Spirit](../spirits/[name].md) - [Relationship]

## Story Hooks

- [Personal quest or conflict]
- [Knowledge or resource they possess]
```

## Spirit Inhabitant Template

Create in `inhabitants/spirits/[name].md`:

```markdown
# [Spirit Name]

**Type:** [Naturae/Elemental/Epiphling/etc.] | **Willpower:** [Rating] | **Power:** [Rating]

**Essence:** [Resonance type]

## Nature and Appearance

[2-3 paragraphs: what it is, appearance, personality, motivations]

## Role in Realm

[How it relates to Realm - native, summoned, guardian, ally]

## Powers and Charms

**Charms:**
- [Charm]: [Effect]

**Influence:** [What it has power over]

## Relationships

- [Mage](../mages/[name].md) - [Relationship]

## Pact Terms

[If bound or allied, what are the terms?]

## Story Hooks

- [What it wants]
- [What it knows]
```

## People Inhabitant Template

Create in `inhabitants/people/[name].md`:

```markdown
# [Person Name]

**Type:** [Human/Vampire/Werewolf/etc.] | **Role:** [Occupation/position]

## Background

[2-3 paragraphs: who they are, story, why in Realm, goals]

## Appearance and Personality

[Physical description, character traits]

## Capabilities

**Skills:** [Key abilities]
**Supernatural Powers:** [If applicable]

## Relationships

- [Name](../mages/[name].md) - [Relationship]

## Story Hooks

- [Their needs or problems]
- [Their knowledge or connections]
```

## Guardian Profile Template

Create in `guardians/[name].md`:

```markdown
# [Guardian Name]

**Type:** [Spirit/Construct/Creature] | **Freebie Points:** [X]

**Location:** [Where stationed - access point, interior, roaming]

## Appearance

[Physical/spiritual description]

## Capabilities

**Attributes:** [If applicable]
**Abilities:** [Key skills]
**Charms/Powers:** [List with effects]

## Authority

[What they can do - control entry, detect threats, initiate combat]

## Bans and Restrictions

[Limits on behavior, things they cannot do]

## Personality

[Demeanor, how they interact with visitors]

## Story Hooks

- [Weakness or vulnerability]
- [Secret or hidden agenda]
```

## Cross-Linking Requirements

All inhabitant profiles should link to:
- Their sanctums, living spaces, workplaces
- Items they created, own, or use
- Other inhabitants (relationships)
- Location files when associated with places
- History when mentioned in events

## Population Guidelines

| People Rating | Approximate Population |
|---------------|------------------------|
| 0 | None (mage visitors only) |
| 1 | 2-10 servants/staff |
| 2 | 10-50 residents |
| 3 | 50-200 (self-sustaining community) |
| 4 | 200-1000 (mixed supernatural) |
| 5 | 1000+ (full society) |

| Ephemera Rating | Spirit Population |
|-----------------|-------------------|
| 0 | Incidental only |
| 1 | 5-10 minor spirits |
| 2 | 10-30 modest spirits |
| 3 | 3-5 powerful unique spirits |
| 4 | 10-20 unique spirits, several powerful |
| 5 | 30+ diverse, almost all unique |
