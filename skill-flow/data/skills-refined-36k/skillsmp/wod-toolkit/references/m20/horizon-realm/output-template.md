# Horizon Realm Output Format

## File Structure

```
/[realm_name]/
├── [realm_name].md          # Main realm document
├── history.md               # Realm history (or link to chantry history)
├── sanctums/
│   └── [sanctum_name].md    # Via sanctum-creator
├── libraries/
│   └── [library_name].md    # Via library-creator
├── guardians/
│   └── [guardian_name].md   # Guardian profiles
├── inhabitants/
│   ├── mages/
│   │   └── [mage_name].md
│   ├── spirits/
│   │   └── [spirit_name].md
│   └── people/
│       └── [person_name].md
└── locations/
    └── [location_name].md   # Notable areas
```

## Main Document Template

```markdown
# [Realm Name]

**Rank:** [1-10] | **Build Points:** [Total] | **Maintenance:** [X Q/mo]

**Creator(s):** [Name(s)] | **Created:** [Year] | **Primary Earthly Connection:** [Location]

**Purpose:** [Primary function]

## Concept

[2-3 paragraphs: origin, what it feels like to enter, how it reflects creator's paradigm. If part of chantry, link to chantry document.]

## Statistics

### Structure

| Trait | Rating | Cost | Notes |
|-------|--------|------|-------|
| **Size** | [0-6] | [X pts] | [Description] |
| **Environment** | [0-6] | [X pts] | [Description] |
| **Access Points** | [N] | [X pts] | [Locations] |

### Inhabitants

| Trait | Rating | Cost | Notes |
|-------|--------|------|-------|
| **Plants** | [0-5] | [X pts] | [Types] |
| **Animals** | [0-5] | [X pts] | [Types] |
| **People** | [0-5] | [X pts] | [Population] |
| **Ephemera** | [0-5] | [X pts] | [Spirit types] |

### Magick

| Trait | Rating | Cost | Effect |
|-------|--------|------|--------|
| **Resonance** | [0-X] | [X pts] | [Type/intensity] |
| **Focus** | [Details] | [X pts] | [Practices affected] |
| **Spheres** | [Modifiers] | [X pts] | [Which, +/-] |
| **Special Phenomena** | [List] | [X pts] | [Each effect] |

### Security

| Trait | Rating | Cost | Notes |
|-------|--------|------|-------|
| **Guardians** | [0-X] | [X pts] | [Number, links] |
| **Arcane** | [0-5] | [X pts] | [Obscurity] |

### Merits and Flaws

| Merit/Flaw | Points |
|------------|--------|
| [Name] | [+/- pts] |

### Final Costs

| Item | Value |
|------|-------|
| **Total Build Points** | [X] |
| **Spent on Traits** | [X] |
| **Converted to Q/mo** | [X] |
| **Base Maintenance** | [X Q/mo] |
| **Merit/Flaw Modifiers** | [Multiplier] |
| **Final Maintenance** | [X Q/mo] |

## Primary Earthly Connection

**Location**: [Where on Earth]
**Nature**: [Environment type]
**Current Status**: [Portal active? State of connection]
**Influence**: [How it shaped Realm]

## Access Points

### [Access Point Name]

**Location**: [Earth or Umbra]
**Type**: [Permanent/Shifting/Keyed/One-Way/Guarded]
**Appearance**: [What it looks like]
**Requirements**: [Wards, keys, passwords, Spirit needed]
**Guardians**: [If any - link to files]

## Geography and Environment

[Landscape, regions, climate. Small Realms: simple layout. Large: multiple zones.]

**Environment Type**: [Based on rating]
**Unusual Features**: [Special Phenomena]
**Climate**: [If applicable]

## Notable Locations

### [Location Name]

**Type**: [Sanctum/Library/Laboratory/Temple]
**Link**: [path/to/location.md]

## Inhabitants

### Plant Life
[Based on Plants rating]

### Animal Life
[Based on Animals rating]

### People
**Population**: [Based on People rating]
**Organization**: [If applicable]
**Notable**: [Links to inhabitant files]

### Ephemera
**Types**: [Based on rating and Resonance]
**Notable**: [Links to spirit files]

## Magical Properties

### Resonance
**Type**: [Alignment]
**Intensity**: [Rating]
**Effect**: [Bonuses/penalties]

### Reality Zone Effects
| Practice | Modifier | Effect |
|----------|----------|--------|
| [Practice] | [+/-X] | [-/+X difficulty] |

### Sphere Modifiers
| Sphere | Modifier |
|--------|----------|
| [Sphere] | [+/-X] |

### Special Phenomena

#### [Phenomenon Name]
**Rank**: [Sphere dots]
**Effect**: [Description]
**Scope**: [Universal/conditional]

## Security

### Guardians
[List with links to detailed files]

### Arcane Protection
**Rating**: [0-5]
**Effect**: [How obscured]

## Connections to Other Realms
| Destination | Type | Difficulty | Notes |
|-------------|------|------------|-------|
| [Realm] | [Portal type] | [Diff] | [Conditions] |

## History

[Creation story, major events, Avatar Storm impact, current status. Or link to chantry history.]

## Maintenance

**Source**: [How funded]
**Responsible**: [Who maintains]
**Backup**: [If maintenance fails]

## Hazards and Challenges

### Environmental Dangers
[Natural/supernatural hazards]

### Security Threats
[External dangers]

### Special Concerns
[From Merits/Flaws]

## Story Hooks

- [Hook 1]
- [Hook 2]
- [Hook 3]
```

## Quick Stat Line

For brief references:
```
[Name]: Rank X | Size [desc] | Build: X pts | Maint: X Q/mo | [Key Merit/Flaw]
```

## Point Validation Block

Include after Final Costs:
```
VALIDATION:
Build Points: X available, X spent ✓
Maintenance: X base + X converted + modifiers = X Q/mo ✓
Source: [Node X provides X Q/mo, Wellspring X Q/mo, etc.] ✓
Incompatibilities: None ✓
```
