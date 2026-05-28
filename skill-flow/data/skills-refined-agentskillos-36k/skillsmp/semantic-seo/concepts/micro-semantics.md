# Micro-Semantics

Micro-semantics is optimization at the sentence and word level. It covers word order, predicate selection, modality, and how individual sentences contribute to information extraction and ranking. Getting micro-semantics right maximizes the efficiency of every sentence.

## Table of Contents

1. [Word Order Importance](#word-order-importance)
2. [Predicate Selection](#predicate-selection)
3. [Context Qualifiers](#context-qualifiers)
4. [Information Retrieval Zones](#information-retrieval-zones)

---

## Word Order Importance

### Sequence Modeling

Search engines calculate the probability of word sequences. Standard sequences are easier to process and more reliably matched.

| Sequence Type | Example | Search Engine Preference |
|---------------|---------|-------------------------|
| **Standard** | "The capital of France is Paris" | High (expected pattern) |
| **Non-standard** | "Paris, which serves as the capital..." | Lower (unusual pattern) |
| **Broken** | "France capital Paris is the" | Very low (hard to parse) |

### Prominence by Position

| Position | Effect | Use For |
|----------|--------|---------|
| **First in sentence** | Highest prominence | Main entity/topic |
| **Subject position** | Entity recognition | What the sentence is about |
| **Early in sentence** | Higher weight | Important attributes |
| **End of sentence** | Lower weight | Supporting details |

### Word Order Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Entity first | "Germany has a population of 83 million" | "83 million people live in the country called Germany" |
| Attribute near entity | "German shepherd weight: 30-40 kg" | "The weight, which varies significantly, of a German shepherd..." |
| Value adjacent | "weighs 171 grams" | "weighs approximately around 171 grams or so" |

### Sentence Structure Patterns

**Definitional** (X is Y):
```
[Entity] is [Definition].
"A German Shepherd is a large breed of working dog."
```

**Attributive** (X has Y):
```
[Entity] has [Attribute]: [Value].
"The German Shepherd has a lifespan of 9-13 years."
```

**Comparative** (X vs Y):
```
[Entity A] is [comparison] than [Entity B].
"German Shepherds are larger than Border Collies."
```

---

## Predicate Selection

### What is a Predicate?

The verb (and its associated meaning) that connects subject to object. Predicates define the relationship type.

### Predicate Categories

| Category | Predicates | Use Case |
|----------|------------|----------|
| **Definitional** | is, are, means, refers to | Facts, definitions |
| **Compositional** | contains, includes, has | Attributes, parts |
| **Causal** | causes, results in, leads to | Cause-effect |
| **Comparative** | exceeds, differs from, equals | Comparisons |
| **Actional** | performs, generates, creates | Actions, functions |
| **Modal** | can, may, should, must | Possibilities, advice |

### Predicate Alignment with CSI

Your predicates should match your Central Search Intent:

| Source Context | Aligned Predicates |
|----------------|-------------------|
| E-commerce | buy, compare, choose, order |
| SaaS | generate, automate, track, integrate |
| Education | learn, understand, master, study |
| Services | provide, offer, deliver, solve |

### Predicate Consistency

Use the same predicates for the same relationships:

| Entity-Attribute | Correct Predicate | Avoid |
|-----------------|-------------------|-------|
| Product -> Price | costs, priced at | is (too vague) |
| Disease -> Symptom | causes, results in | has (imprecise) |
| Tool -> Function | performs, enables | does (too generic) |

### Frame Semantics

Predicates trigger "frames" - expected patterns:

```
Predicate: "buy"
Expected frame: [Agent] buys [Object] from [Seller] for [Price]

Sentence should satisfy the frame:
"Customers buy the iPhone from Apple for $999."
```

---

## Context Qualifiers

### What are Context Qualifiers?

Words that narrow the semantic domain: location, time, demographic, condition.

### Types of Qualifiers

| Type | Examples | Effect |
|------|----------|--------|
| **Location** | in Germany, for Europe, US-based | Geographic scope |
| **Time** | in 2024, during winter, after 6pm | Temporal scope |
| **Demographic** | for children, for seniors, for professionals | Audience scope |
| **Condition** | with diabetes, without experience, for beginners | Situational scope |
| **Quantity** | under $50, over 6 feet, between 10-20 | Numeric scope |

### Query Specificity Ladder

More qualifiers = narrower context = more specific ranking:

```
Broad: "Best books"
v + Topic: "Best books about gardening"
v + Demographic: "Best books about gardening for beginners"
v + Condition: "Best books about gardening for beginners with small spaces"
```

### Qualifier Placement

| Position | Effect | Example |
|----------|--------|---------|
| In heading | Strongest signal | "H2: Best Products for Children" |
| In first sentence | High signal | "For children over 6, the best..." |
| Throughout text | Consistent signal | Multiple mentions of qualifier |

### Context Sharpening

Add qualifiers to strengthen contextual relevance:

**Before** (vague):
```
"The best way to learn programming."
```

**After** (sharp):
```
"The best way to learn Python programming for data science beginners in 2024."
```

---

## Information Retrieval Zones

### Page Segmentation

Search engines divide pages into zones with different weights:

| Zone | Location | Weight |
|------|----------|--------|
| **Centerpiece** | First 400 chars of main content | Highest |
| **Title/H1** | Page title, main heading | Very high |
| **Subordinate** | First sentence after headings | High |
| **Main content** | Body paragraphs | Medium-high |
| **Supplementary** | Sidebars, related sections | Medium |
| **Boilerplate** | Header, footer, navigation | Low |

### Centerpiece Annotation

The first 400 characters are critical for initial ranking:

**Must contain**:
- Core entity/topic
- Primary definition or answer
- Key attributes

**Must NOT contain**:
- Share buttons, ads
- Author bio, dates (before content)
- Generic introductions

### Subordinate Text Optimization

First sentence after any heading = Candidate Answer Passage:

| Heading Type | First Sentence Should |
|--------------|----------------------|
| Question | Answer directly |
| Statement | Expand the statement |
| Topic | Define the topic |

**Featured Snippet targets**:
- <40 words OR <340 characters
- Direct, definitive answer
- No hedging or fluff

### Zone Optimization Checklist

```
[ ] Centerpiece (first 400 chars) contains core answer
[ ] H1 matches main topic exactly
[ ] Each H2/H3 followed by direct answer
[ ] Main content weighted > supplementary
[ ] Boilerplate minimized
```

---

## Micro-Semantic Validation

### Sentence-Level Checks

```
[ ] Word order follows standard patterns
[ ] Important entities at sentence start
[ ] Attributes near their entities
[ ] Values adjacent to attributes
[ ] Predicates match CSI
[ ] No unnecessary words between entity-attribute-value
```

### Predicate Checks

```
[ ] Predicates aligned with Source Context
[ ] Consistent predicates for same relationships
[ ] Frames satisfied (all expected elements present)
[ ] Modal verbs appropriate (is vs can vs should)
```

### Qualifier Checks

```
[ ] Context qualifiers present where needed
[ ] Qualifiers in headings where appropriate
[ ] Specific qualifiers (not vague "some" or "many")
[ ] Qualifiers consistent throughout page
```

### Zone Checks

```
[ ] First 400 chars optimized
[ ] Each heading has optimized subordinate text
[ ] Main content prioritized over supplementary
[ ] No important content in low-weight zones
```

---

## Common Micro-Semantic Errors

| Error | Example | Fix |
|-------|---------|-----|
| Delayed entity | "In this article about dogs..." | "Dogs are..." |
| Separated attribute | "The weight (which can vary) is 30kg" | "The weight is 30kg" |
| Wrong predicate | "Germany is 83 million" | "Germany has a population of 83 million" |
| Missing qualifier | "Best practices" | "Best practices for SEO in 2024" |
| Buried answer | Answer in 3rd paragraph | Move to first sentence |
| Vague modality | "might possibly be" | "is" (for facts) or "can be" (for variables) |
