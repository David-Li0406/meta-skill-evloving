# Entity-Attribute-Value (EAV) Architecture

The EAV model is the foundational data structure for Semantic SEO. All information in your content network must be structured as triples (Subject-Predicate-Object), enabling search engines to extract and validate facts efficiently.

## Table of Contents

1. [EAV Triple Structure](#eav-triple-structure)
2. [Attribute Types](#attribute-types)
3. [Knowledge Graph Construction](#knowledge-graph-construction)
4. [Validation Rules](#validation-rules)

---

## EAV Triple Structure

### The Basic Triple

```
Entity (Subject) -> Attribute (Predicate) -> Value (Object)
```

| Component | Role | Example |
|-----------|------|---------|
| **Entity** | The central object (person, place, product, concept) | Germany |
| **Attribute** | The property or relationship | Population |
| **Value** | The specific data or measurement | 83 million |

### Triple Examples

| Domain | Entity | Attribute | Value |
|--------|--------|-----------|-------|
| Country | Germany | Capital | Berlin |
| Product | iPhone 15 | Weight | 171 grams |
| Person | Albert Einstein | Birth Year | 1879 |
| Chemical | Water | pH Level | 7.0 |
| Service | Visa Application | Processing Time | 15 business days |

### Triple Quality Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Explicit naming | "Germany has a population of 83 million" | "It has 83 million people" |
| Specific values | "weighs 171 grams" | "is lightweight" |
| Definitive modality | "The capital is Berlin" | "The capital could be Berlin" |
| Consistent units | Always use same measurement system | Mixing metric/imperial |

---

## Attribute Types

Attributes are prioritized by type. This determines content order and emphasis.

### 1. Unique Attributes (Highest Priority)

Definitive features that **uniquely identify** the entity. No other entity shares this attribute-value combination.

| Entity | Unique Attribute | Value |
|--------|-----------------|-------|
| France | Iconic Landmark | Eiffel Tower |
| Tesla Model S | Unique Feature | Falcon Wing Doors |
| Germany | Official Name | Federal Republic of Germany |

**Rule**: Unique Attributes prove specialized expertise. Place them early in content.

### 2. Root Attributes (Core Priority)

**Essential for definition** - without these, the entity cannot be properly understood.

| Entity Type | Root Attributes |
|-------------|----------------|
| Country | Population, Capital, Currency, Language |
| Product | Price, Dimensions, Weight, Material |
| Person | Name, Occupation, Birth Date, Nationality |
| Service | Duration, Cost, Requirements, Availability |

**Rule**: Root Attributes establish baseline understanding. Cover all of them.

### 3. Rare Attributes (Authority Priority)

**Not commonly found** across similar entities. Proves depth of expertise.

| Entity | Rare Attribute | Value |
|--------|---------------|-------|
| German Shepherd | Genetic Diseases | Hip dysplasia, DM |
| Germany | Nuclear Plants | 3 remaining (as of 2023) |
| Coffee | Optimal Brewing Temperature | 195-205 degrees F |

**Rule**: Rare Attributes differentiate you from competitors. They signal expertise.

### Attribute Priority in Content

```
Content Order:
1. Unique Attributes (differentiation)
   v
2. Root Attributes (definition)
   v
3. Rare Attributes (expertise)
```

---

## Knowledge Graph Construction

### Building Your Knowledge Base

The Semantic Content Network functions as a digital knowledge base. Every fact must be stored as an EAV triple.

### Step 1: Entity Identification

```
Central Entity: [Your CE]
|---- Related Entities (same type)
|---- Parent Entities (hypernyms)
|---- Child Entities (hyponyms)
---- Connected Entities (by predicate)
```

### Step 2: Attribute Mapping

For each entity, map all three attribute types:

```
Entity: Germany
|---- Unique Attributes
|   |---- Autobahn (no speed limit highways)
|   |---- Oktoberfest
|   ---- Brandenburg Gate
|---- Root Attributes
|   |---- Population: 83 million
|   |---- Capital: Berlin
|   |---- Currency: Euro
|   ---- Language: German
---- Rare Attributes
    |---- Federal States: 16
    |---- UNESCO Sites: 52
    ---- Time Zone: CET (UTC+1)
```

### Step 3: Predicate Verbalization

Define the verbs (predicates) that connect entities:

| Connection Type | Predicates |
|----------------|------------|
| Definition | is, are, means, refers to |
| Composition | contains, includes, consists of |
| Location | located in, found in, based in |
| Causation | causes, results in, leads to |
| Comparison | differs from, similar to, better than |
| Action | requires, needs, uses, produces |

### Step 4: Value Standardization

Ensure consistent value formats:

| Value Type | Standard Format |
|------------|----------------|
| Numbers | With units (83 million, 171g) |
| Dates | Consistent format (YYYY-MM-DD or Month Day, Year) |
| Ranges | "X to Y" or "between X and Y" |
| Currency | Symbol + amount (EUR50, $100) |
| Percentages | X% (not "X percent") |

---

## Validation Rules

### Consistency Validation

| Rule | Check | Action if Failed |
|------|-------|-----------------|
| **Cross-page consistency** | Same entity has same attribute values everywhere | Audit all pages, standardize values |
| **Unit consistency** | Same measurement system throughout | Convert all to one system |
| **Naming consistency** | Same entity name format everywhere | Create naming convention |
| **Date consistency** | Same date format throughout | Standardize format |

### Completeness Validation

| Check | Requirement |
|-------|-------------|
| All Root Attributes covered | Entity cannot lack essential definitions |
| At least 3 Unique Attributes | Differentiation from competitors |
| Rare Attributes present | Expertise signals |
| Antonyms included | Context strengthening |

### Knowledge-Based Trust (KBT)

KBT is the trust score determined by accuracy and consistency of EAV triples.

**High KBT requires:**
- No contradictory facts across pages
- Values match external knowledge bases (Wikipedia, authoritative sources)
- Consistent modality (definitive for facts, conditional for advice)

**KBT Killers:**
| Issue | Example | Fix |
|-------|---------|-----|
| Contradictory values | Page A: "EUR50", Page B: "EUR60" | Standardize to correct value |
| Vague values | "many", "some", "often" | Replace with specific numbers |
| Missing citations | Claims without sources | Add authoritative citations |
| Wrong modality | "might be" for established facts | Use "is" for facts |

### Validation Checklist

```
[ ] All entities have Unique, Root, and Rare attributes
[ ] All values are specific (not vague)
[ ] No contradictions across pages
[ ] Units are consistent
[ ] Naming is consistent
[ ] Dates are consistent
[ ] Facts align with authoritative sources
[ ] Modality appropriate (facts vs. advice)
```

---

## EAV in Content Briefs

When creating content briefs, specify EAV requirements:

```
Content Brief: [Topic]

Required EAV Triples:
| Entity | Attribute | Value | Source |
|--------|-----------|-------|--------|
| [E1] | [A1] | [V1] | [Cite] |
| [E1] | [A2] | [V2] | [Cite] |

Attribute Priority:
1. [Unique Attribute 1]
2. [Root Attribute 1]
3. [Root Attribute 2]
4. [Rare Attribute 1]

Consistency Requirements:
- [Entity] must be named as: [Standard Name]
- [Value Type] format: [Standard Format]
```
