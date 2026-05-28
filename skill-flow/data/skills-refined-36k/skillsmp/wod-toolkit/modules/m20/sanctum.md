# Sanctum Module

Design mechanically valid sanctums for M20 using Prism of Focus Practice integration.

## Context

| Context | Save Location | Constraints |
|---------|---------------|-------------|
| Standalone | `./sanctums/` | Conceptual |
| Character | `[character]/sanctums/` | Character's Practices |
| Chantry | `[project]/sanctums/` | Chantry type |
| Horizon Realm | `[project]/sanctums/` | Realm theme |

## What is a Sanctum?

A mage's personal workspace — laboratory, ritual chamber, or studio. Sanctums provide:
- Safe space for magical work
- Storage for materials and equipment
- Practice support (under Prism of Focus)

## Prism of Focus Integration

### Practice Ratings

For **each dot of Sanctum**, assign:
- **One dot in a Practice** (includes base materials needed)
- Magick using that Practice within the Sanctum is **always Coincidental**

**AND optionally**:
- One level of a **different Practice becomes anathema**
- Effects using anathema Practice with Spheres ≥ (6 - rating) become **Vulgar**

### Example Sanctum Practices

| Sanctum Type | Practice Support | Anathema Practice |
|--------------|------------------|-------------------|
| Hermetic Lab | High Ritual Magick 3 | Gutter Magick -3 |
| Tech Workshop | Hypertech 4 | Witchcraft -2, Faith -2 |
| Sacred Grove | Witchcraft 3, Shamanism 2 | Cybernetics -5 |
| Data Haven | Reality Hacking 3, Cybernetics 2 | Animalism -3, Shamanism -2 |

## Creation Workflow

1. **Concept** — Type, location, purpose
2. **Rating** — 1-5 dots
3. **Practice Support** — Which Practices are enhanced (= rating)
4. **Anathema Practices** — Which Practices are penalized (optional, = rating)
5. **Features** — Based on Sanctum type
6. **Security** — Mundane and magical protections
7. **Limitations** — Size, accessibility, vulnerabilities
8. **Document** — Use output format
9. **Validate**

## Sanctum Ratings

| Rating | Size | Practice Support |
|--------|------|------------------|
| • | Small room | 1 Practice at 1 dot |
| •• | Apartment/suite | 2 Practice dots total |
| ••• | House/laboratory | 3 Practice dots total |
| •••• | Building/compound | 4 Practice dots total |
| ••••• | Estate/complex | 5 Practice dots total |

## Sanctum Types

### Ritual Chamber
- **Common Practices**: High Ritual Magick, Faith, Witchcraft
- **Typical Anathema**: Hypertech, Cybernetics, Reality Hacking
- **Features**: Ritual circles, altars, proper correspondences

### Laboratory
- **Common Practices**: Alchemy, Hypertech, Weird Science
- **Typical Anathema**: Shamanism, Voudoun, Animalism
- **Features**: Equipment, reagents, safety features

### Studio
- **Common Practices**: Bardism, Craftwork, Art of Desire
- **Typical Anathema**: Hypertech, Dominion
- **Features**: Creative tools, inspiration, performance space

### Sacred Space
- **Common Practices**: Faith, God-Bonding, Shamanism
- **Typical Anathema**: Maleficia, Goetia, Infernal Sciences
- **Features**: Consecrated ground, religious symbols, spiritual protection

### Dojo/Training Hall
- **Common Practices**: Martial Arts, Invigoration, Yoga
- **Typical Anathema**: Cybernetics, Hypertech
- **Features**: Training equipment, meditation space, discipline

### Digital Fortress
- **Common Practices**: Reality Hacking, Cybernetics, Media Control
- **Typical Anathema**: Witchcraft, Shamanism, Animalism
- **Features**: Servers, network access, digital security

## Output Format

```markdown
# [Sanctum Name]

**Sanctum Rating**: [•-•••••]
**Type**: [Chamber/Laboratory/Studio/Sacred/Dojo/Digital/Other]
**Location**: [Where]
**Owner**: [Character/Chantry/Shared]

## Practice Support

| Practice | Rating | Effect |
|----------|--------|--------|
| [Name] | [1-5] | All effects Coincidental |

**Total Practice Dots**: [N]

## Anathema Practices (Optional)

| Practice | Penalty Level | Effect |
|----------|---------------|--------|
| [Name] | [1-5] | Effects with Sphere ≥ [6-rating] become Vulgar |

## Description
[Physical description, atmosphere]

## Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Equipment & Materials
[What's available for the supported Practices]

## Security
**Mundane**: [Locks, location, etc.]
**Magical**: [Wards, protections]

## Access
[Who can enter, requirements]

## Limitations
- [Size constraints]
- [Accessibility issues]
- [Vulnerabilities]

## History
[Brief origin]
```

## Validation

- [ ] Rating corresponds to size/resources
- [ ] Practice dots = Sanctum rating
- [ ] Anathema dots ≤ Sanctum rating
- [ ] Features match Practice support
- [ ] Equipment appropriate to Practices
- [ ] Security proportional to value
- [ ] Limitations reasonable

**When dependency:**
- [ ] Practices match owner's capabilities
- [ ] Location consistent with parent (Chantry/Realm)
- [ ] Security compatible with parent

## Reference Data

```bash
# Practice details (what equipment/materials needed)
python scripts/lookup.py rules.practices practices "Alchemy"

# Resonance traits for sanctum atmosphere
python scripts/lookup.py rules.resonance-traits resonance-traits "High Ritual Magick"
```

## Return Format (for parent modules)

```
Created: ./sanctums/hermetic_lab.md
Name: Hermetic Laboratory
Rating: 3
Practices: High Ritual Magick 2, Alchemy 1
Anathema: Gutter Magick -3
Effect: HRM/Alchemy always Coincidental; Gutter Magick 3+ Vulgar
```
