# Semantic Distance

Semantic Distance is the quantifiable measure of closeness between two concepts, entities, or documents. It determines whether topics can be clustered together, linked, or should be separated into different pages.

## Table of Contents

1. [Core Definition](#core-definition)
2. [Calculation Components](#calculation-components)
3. [Applications](#applications)
4. [Distance vs Similarity vs Relevance](#distance-vs-similarity-vs-relevance)

---

## Core Definition

### What is Semantic Distance?

Semantic Distance measures how "close" or "far" two concepts are in meaning and relationship. It is used by search engines to:

- **Cluster associations** - Group related content together
- **Define topical borders** - Determine where one topic ends and another begins
- **Validate links** - Justify connections between pages
- **Prevent dilution** - Avoid mixing unrelated concepts

### The Impact of Distance

| Distance | Implication | Action |
|----------|-------------|--------|
| **Low (close)** | Concepts belong together | Can combine on one page, link freely |
| **Medium** | Related but distinct | Separate pages, use bridges |
| **High (far)** | Unrelated or tangential | Avoid linking without strong bridge |

---

## Calculation Components

### Primary Formula

```
Semantic Distance = 1 - (Cosine Similarity x Context Weight x Co-occurrence)
```

| Component | What It Measures |
|-----------|------------------|
| Cosine Similarity | Vector space similarity between terms |
| Context Weight | Importance of shared context |
| Co-occurrence | How often terms appear together |

### Connection Length

Distance is measured by counting nodes between two concepts in the topical graph:

```
A -> B -> C -> Z

Distance from A to Z = 2 (nodes B and C between them)
```

**Rule**: If distance exceeds ~5 nodes, search engines may treat topics as unrelated.

### Association Count

More connections between concepts = lower distance:

```
High Association (Low Distance):
Germany -> located in -> Europe
Germany -> member of -> EU
Germany -> borders -> France

Low Association (High Distance):
Germany -> historical event -> [single connection to distant topic]
```

### Overriding Factors

| Factor | How It Affects Distance |
|--------|------------------------|
| **PageRank** | High-authority pages can bridge wider distances |
| **Vocabulary overlap** | Shared terminology reduces perceived distance |
| **Query patterns** | User behavior establishes implicit connections |

---

## Applications

### Topical Map Clustering

**Use distance to group pages**:

| Distance | Clustering Decision |
|----------|---------------------|
| <0.3 | Same cluster, possible same page |
| 0.3-0.5 | Same cluster, separate pages |
| 0.5-0.7 | Adjacent clusters, need bridge |
| >0.7 | Different clusters entirely |

**Example**:
```
Low Distance (same cluster):
|---- Germany Visa
|---- France Visa
|---- Spain Visa
---- Italy Visa

High Distance (different cluster):
|---- European Visa (ok bridge)
---- South American Cuisine (no connection)
```

### Internal Linking Strategy

**Link based on semantic proximity**:

| Link Type | Distance Rule |
|-----------|---------------|
| Direct link | Low distance, obvious connection |
| Bridge link | Medium distance, contextual justification |
| Avoid link | High distance, no logical path |

**Correct**: Linking "material" attribute to "nylon" material page
**Incorrect**: Linking "nylon" to "company history" without context

### Anchor Text Hierarchy

Organize anchor texts by lexical hierarchy:

```
Page Position -> Anchor Type
Higher on page -> Hypernyms (broader terms): "Color"
Lower on page -> Hyponyms (specific terms): "Violet"
```

### Attribute Prioritization

Closer attributes to the entity get higher priority:

| Attribute Type | Distance from Entity | Priority |
|----------------|---------------------|----------|
| Root attributes | Closest | Highest |
| Unique attributes | Close | High |
| Rare attributes | Medium | Medium |
| Historical attributes | Far | Lower |

**Example** (Car entity):
- Engine, speed, weight -> Close distance -> Higher priority
- Inventor, history -> Far distance -> Lower priority (unless SC is history)

### Query Refinements

Semantic distance affects suggested searches:

| Relationship | Search Behavior |
|--------------|-----------------|
| Very close queries | One canonical query chosen |
| Close queries | Refinement suggestions |
| Far queries | No relationship shown |

**Implication**: Focus content on canonical queries to capture semantically close variations.

---

## Distance vs Similarity vs Relevance

These three concepts are distinct but related:

### Semantic Similarity

**Definition**: The changeability and replaceability of words without altering meaning.

| Relationship | Similarity |
|--------------|------------|
| Synonyms | Very high |
| Hyponyms/Hypernyms | High |
| Co-hyponyms | Medium |
| Unrelated | Low |

**Example**: "car" and "automobile" = high similarity

### Semantic Relevance

**Definition**: The connection between concepts based on a mutual situation or criteria, even if not similar.

| Relationship | Relevance |
|--------------|-----------|
| Complementary | High |
| Contextual | High |
| Antonyms | High (opposite but related) |
| Unrelated | Low |

**Example**: "glasses" (eyewear) and "binoculars" = not similar but highly relevant (both viewing tools)

### The Distinction Illustrated

```
Sentence A: "I watched a movie with my glasses"
Sentence B: "I watched a bird with my binoculars"

Similarity Analysis:
- "movie" vs "bird" = NOT similar (different entities)
- "glasses" vs "binoculars" = NOT similar (different objects)

Relevance Analysis:
- Both use "watch" (same predicate)
- Both involve viewing tools
- HIGH relevance despite LOW similarity
```

### Implications for Content

| Concept | Use Case |
|---------|----------|
| **Distance** | Clustering, page structure, link decisions |
| **Similarity** | Synonym usage, lexical variation |
| **Relevance** | Bridge topics, contextual connections |

---

## Practical Application Checklist

### Before Creating Content

```
[ ] Calculate distance from Central Entity
[ ] Verify topic fits within cluster boundaries
[ ] Identify bridge topics if distance is medium
[ ] Confirm no high-distance jumps without justification
```

### Before Adding Links

```
[ ] Source and target have low semantic distance
[ ] Annotation text supports the connection
[ ] Link doesn't create unjustified far connections
[ ] Anchor text follows lexical hierarchy
```

### Cluster Validation

```
[ ] All pages in cluster have distance <0.5
[ ] Bridge content connects adjacent clusters
[ ] No orphan pages with high distance from cluster
[ ] Canonical queries mapped correctly
```
