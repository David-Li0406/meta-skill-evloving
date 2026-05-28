# Topical Maps Framework

A Topical Map (TM) is the mandatory first step in implementing Semantic SEO. It is not a keyword list - it is a communication mechanism designed to increase relevance and decrease the Cost of Retrieval.

## Table of Contents

1. [The Five Core Components](#the-five-core-components)
2. [Hub-Spoke Architecture](#hub-spoke-architecture)
3. [Building a Topical Map](#building-a-topical-map)
4. [Validation Checklist](#validation-checklist)

---

## The Five Core Components

### 1. Central Entity (CE)

The **single main entity** that the entire website is fundamentally about.

| Requirement | Action |
|-------------|--------|
| Site-wide presence | Must appear in boilerplate, menu links, and all documents |
| N-gram consistency | Form site-wide N-grams around the CE |
| Single focus | One CE per website (not per page) |

**Example**: For a Germany visa consultancy site, the CE is "Germany" (not "visa" or "travel").

### 2. Source Context (SC)

Defines **who you are** and **how you monetize**. This determines how Google classifies your documents.

| SC Type | Attribute Priority | Content Focus |
|---------|-------------------|---------------|
| E-commerce | Price, availability, specifications | Product comparisons, reviews |
| Affiliate | User benefits, alternatives | Comparison content, guides |
| SaaS | Features, use cases, integrations | Solution-oriented content |
| Publisher | Expertise, research, opinions | Informational depth |
| B2B Services | Credentials, case studies, methodology | Trust and expertise signals |

**Rule**: The SC must align with the topics covered. A medical site should not write about sports history without a contextual bridge.

### 3. Central Search Intent (CSI)

The **unified action or purpose** connecting the CE with the SC. Reflected in the core predicates (verbs) used throughout.

| SC Type | Example CSI Predicates |
|---------|----------------------|
| Visa Consultancy | visit, live in, work in, study in, learn about |
| E-commerce | buy, compare, choose, find |
| SaaS | generate, automate, manage, track |
| Publisher | understand, learn, discover |

**Action**: Determine the verbs associated with the user's journey. These must appear in root documents and major headings.

### 4. Core Section (CS)

The segment of the content network designed for **direct monetization**. Result of unifying CE + SC.

| Requirement | Implementation |
|-------------|----------------|
| Highest PageRank flow | Most internal links point here |
| High granularity | Specific to conversion funnel |
| Priority publishing | Complete Core Section first |

**Example**: For a German visa site, the Core Section details every visa type (D-type, C-type, family reunification, etc.).

### 5. Author Section (AS)

Supplementary content dedicated to gathering **Historical Data** and increasing topical relevance by proving authority on the broader entity.

| Requirement | Implementation |
|-------------|----------------|
| Link to Core Section | AS pages must link back to CS |
| Broader coverage | Covers CE attributes not tied to revenue |
| PageRank transfer | Serves as authority transfer mechanism |

**Example**: For a country entity (Germany), the AS covers German culture, politics, geography, history.

---

## Hub-Spoke Architecture

### Structure
```
        [Hub Page]
       /    |    \
      /     |     \
   [Spoke] [Spoke] [Spoke]
     |       |       |
   [Sub]   [Sub]   [Sub]
```

### Optimal Ratio: 1:7
- 1 Hub page to 7 Spoke pages
- Each Spoke can have its own sub-spokes

### Implementation Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Hub defines the cluster | Hub page covers the parent topic comprehensively | Hub page is just a navigation/index page |
| Spokes expand attributes | Each spoke covers one major attribute/subtopic | Spokes duplicate hub content |
| Link direction | Spokes link UP to hub, hub links DOWN to spokes | Random cross-linking |

---

## Building a Topical Map

### Step 1: Define Core Components

```
1. Central Entity (CE): _____________
2. Source Context (SC): _____________
3. Central Search Intent (CSI): _____________
   - Primary predicate: _____________
   - Secondary predicates: _____________
```

### Step 2: Map Core Section Topics

List all monetization-relevant topics:
```
Core Section Topics:
|---- [Main conversion topic]
|   |---- [Subtopic 1]
|   |---- [Subtopic 2]
|   ---- [Subtopic 3]
|---- [Secondary conversion topic]
|   ---- [Subtopics...]
```

### Step 3: Map Author Section Topics

List all authority-building topics:
```
Author Section Topics:
|---- [CE Background/History]
|---- [CE Related Concepts]
|---- [CE Broader Context]
---- [CE Supporting Information]
```

### Step 4: Define Cluster Boundaries

For each cluster, define:
- **Semantic distance threshold**: How far from CE can content go?
- **Bridge topics**: What justifies distant connections?
- **Canonical queries**: Which page answers which query?

### Step 5: Plan Link Flow

```
[AS Pages] --link--> [CS Pages] --link--> [Conversion Pages]
     ^                    ^                      ^
   Low PR              Medium PR              High PR
```

---

## Validation Checklist

### Component Validation

| Component | Check | Pass/Fail |
|-----------|-------|-----------|
| CE defined | Single, clear entity identified | |
| CE site-wide | Appears in boilerplate, menus | |
| SC defined | Monetization model clear | |
| SC aligned | Topics match SC type | |
| CSI defined | Core predicates identified | |
| CSI present | Predicates in headings/content | |
| CS complete | All monetization topics covered | |
| AS complete | Authority topics covered | |
| AS->CS links | All AS pages link to CS | |

### Architecture Validation

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Hub-Spoke ratio | ~1:7 per cluster | |
| Link direction | Consistent flow to CS | |
| No orphans | All pages linked from somewhere | |
| No dead-ends | All pages link to at least one other | |
| Canonical assignment | One page per canonical query | |

### Quality Thresholds

| Metric | Target |
|--------|--------|
| Semantic Compliance Score | >85% |
| Context Coherence Score | >0.8 |
| Pages without internal links | 0 |
| Duplicate canonical assignments | 0 |
