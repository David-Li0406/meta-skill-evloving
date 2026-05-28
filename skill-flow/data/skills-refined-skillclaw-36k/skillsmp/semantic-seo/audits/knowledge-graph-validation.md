# Knowledge Graph Validation

The Knowledge Graph (KG) is the visualized representation of your Knowledge Base (KB). This guide validates the quality, completeness, and consistency of your KG to ensure high Knowledge-Based Trust (KBT) scores.

## Table of Contents

1. [Triple Quality Validation](#triple-quality-validation)
2. [Completeness Criteria](#completeness-criteria)
3. [Consistency Checks](#consistency-checks)
4. [Validation Process](#validation-process)

---

## Triple Quality Validation

Every fact in your KG must be structured as an EAV triple (Entity-Attribute-Value).

### Triple Structure Check

| Component | Validation Question | Pass/Fail |
|-----------|---------------------|-----------|
| **Entity (Subject)** | Is it a clearly defined person, place, product, or concept? | |
| **Attribute (Predicate)** | Is it a property or relationship (not subjective)? | |
| **Value (Object)** | Is it specific, measurable data? | |

**Correct Triple**: Germany -> Population -> 83 million
**Incorrect**: Germany -> Overall -> Great country

### Quality Criteria

| Criterion | Definition | Check |
|-----------|------------|-------|
| **Accuracy** | Values are factually correct, consensus-based | Match external KB (Wikipedia, etc.) |
| **Specificity** | Values are precise, not vague | Numbers with units, not "many" |
| **Groundedness** | Facts can be verified | Source citations present |

### Common Triple Errors

| Error Type | Example | Fix |
|------------|---------|-----|
| Vague value | "high population" | "83 million people" |
| Opinion as fact | "best country" | Remove or justify with metrics |
| Missing entity | "It has 83 million" | "Germany has 83 million" |
| Wrong predicate | "Germany is 83 million" | "Germany has a population of 83 million" |

---

## Completeness Criteria

A KG is complete when Contextual Coverage is optimal for your Source Context.

### Attribute Type Coverage

| Attribute Type | Check | Pass/Fail |
|----------------|-------|-----------|
| **Root Attributes** | All essential definitions present | |
| **Rare Attributes** | Depth-proving details included | |
| **Unique Attributes** | Differentiating features documented | |

### Root Attributes Checklist

For each major entity, verify root attributes:

| Entity Type | Required Root Attributes |
|-------------|-------------------------|
| Country | Population, Capital, Currency, Language, Area |
| Product | Price, Dimensions, Weight, Material, Availability |
| Person | Name, Occupation, Birth Date, Nationality |
| Company | Founded, Headquarters, Industry, Size |
| Service | Duration, Cost, Requirements, Availability |

### Completeness Validation

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| All entity types defined | Each entity has type classification | |
| Root attributes present | All essential attributes for each type | |
| Rare attributes present | At least 3 depth-proving attributes per entity | |
| Unique attributes present | At least 1 differentiating attribute per entity | |
| Antonyms included | Opposite concepts present for context strength | |

### Query Network Saturation

| Check | Validation |
|-------|------------|
| Popular queries covered | Top search queries have content | |
| Rare queries covered | Long-tail queries addressed | |
| No query orphans | All queries map to pages | |

---

## Consistency Checks

Inconsistencies destroy Knowledge-Based Trust (KBT).

### Cross-Page Consistency

| Check | Method | Pass/Fail |
|-------|--------|-----------|
| Same entity = same name | Search all pages for entity variations | |
| Same attribute = same value | Compare values across pages | |
| Same definition | Definition wording consistent | |

**Example Inconsistency**:
- Page A: "The CEO is John Doe"
- Page B: "Mr. Doe leads the company"
- Page C: "John D. is the CEO"

**Fix**: Standardize to "John Doe, CEO" everywhere

### Numerical Consistency

| Check | Requirement |
|-------|-------------|
| Same numbers everywhere | pH 7.0 on all pages (not 7.0 here, 7.2 there) |
| Same units | All metric OR all imperial (not mixed) |
| Same precision | All "83 million" or all "83,000,000" |
| Same date formats | Consistent format throughout |

### Contradiction Detection

| Contradiction Type | Example | Severity |
|--------------------|---------|----------|
| Value mismatch | Price EUR50 vs EUR60 | Critical |
| Date conflict | Founded 2010 vs 2011 | Critical |
| Definition drift | Slightly different definitions | High |
| Predicate conflict | "causes" vs "may cause" | Medium |

### Modality Consistency

| Fact Type | Required Modality | Check |
|-----------|-------------------|-------|
| Established facts | "is" (definitive) | No "can be" or "might be" |
| Variable outcomes | "can" (possibility) | Not stated as definite |
| Advice | "should" (recommendation) | Not stated as mandatory |

---

## Validation Process

### Step 1: Entity Inventory

Create a master list of all entities:

```
Entity Inventory:
|---- [Entity 1]
|   |---- Type: [classification]
|   |---- Root Attributes: [list]
|   |---- Rare Attributes: [list]
|   ---- Unique Attributes: [list]
|---- [Entity 2]
...
```

### Step 2: Triple Extraction

For each content page, extract all triples:

```
Page: [URL]
Triples:
| Entity | Attribute | Value | Source |
|--------|-----------|-------|--------|
| | | | |
```

### Step 3: Consistency Matrix

Compare triples across pages:

```
Entity: [Name]
Attribute: [Attribute Name]

| Page | Value | Match? |
|------|-------|--------|
| /page-1 | [value] | Baseline |
| /page-2 | [value] | Yes/No |
| /page-3 | [value] | Yes/No |
```

### Step 4: Completeness Audit

For each entity, check coverage:

```
Entity: [Name]

| Attribute Type | Required | Present | Gap |
|----------------|----------|---------|-----|
| Root | 5 | 5 | 0 |
| Rare | 3 | 2 | 1 |
| Unique | 1 | 1 | 0 |

Missing: [List missing attributes]
```

### Step 5: Antonym Validation

Verify context-strengthening opposites:

```
| Main Concept | Antonym Present | Location |
|--------------|-----------------|----------|
| Benefits | Risks | Yes/No |
| Advantages | Disadvantages | Yes/No |
| Hydration | Dehydration | Yes/No |
```

---

## Validation Scorecard

### Triple Quality Score

| Metric | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| Accuracy | 30% | | |
| Specificity | 25% | | |
| Groundedness | 20% | | |
| Structure | 25% | | |
| **Total** | 100% | | /5 |

### Completeness Score

| Metric | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| Root coverage | 35% | | |
| Rare coverage | 25% | | |
| Unique coverage | 20% | | |
| Query saturation | 20% | | |
| **Total** | 100% | | /5 |

### Consistency Score

| Metric | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| Cross-page values | 40% | | |
| Numerical precision | 20% | | |
| Naming conventions | 20% | | |
| Modality alignment | 20% | | |
| **Total** | 100% | | /5 |

### Overall KG Health

| Component | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Triple Quality | /5 | 35% | |
| Completeness | /5 | 35% | |
| Consistency | /5 | 30% | |
| **Total** | | | /5 |

**Target**: 4.0+ for healthy Knowledge Graph
