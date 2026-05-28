---
name: semantic-seo
description: Semantic SEO framework for reducing Cost of Retrieval (CoR). Use when creating SEO content, topical maps, content briefs, semantic content networks, knowledge graphs, website audits, or optimizing for search engines. Triggers on SEO strategy, content optimization, E-A-T, entity optimization, search visibility, ranking improvement, content architecture, and semantic search.
---

# Semantic SEO Framework

This skill implements Koray Tugberk Gubur's Semantic SEO methodology for reducing the **Cost of Retrieval (CoR)** for search engines. The framework treats search engines as "blind librarians" that need explicit, structured, consistent information to understand and rank content.

## Table of Contents

1. [Core Philosophy](#core-philosophy)
2. [The Five Components of a Topical Map](#the-five-components)
3. [Task Routing](#task-routing)
4. [Quick Reference](#quick-reference)

---

## Core Philosophy

The goal is to **decrease the computational cost** for search engines to crawl, parse, understand, and rank your content. This is achieved through:

1. **Semantic Content Networks (SCN)** - Interconnected content designed for machine comprehension
2. **Entity-Attribute-Value (EAV) Architecture** - Structured facts as Subject-Predicate-Object triples
3. **Knowledge-Based Trust (KBT)** - Consistency of facts across the entire network
4. **Algorithmic Authorship** - Writing rules optimized for NLP algorithms

---

## The Five Components

Every Topical Map requires these five components:

| Component | Definition | Purpose |
|-----------|------------|---------|
| **Central Entity (CE)** | The single main entity the website is about | Appears in boilerplate, menus, all documents |
| **Source Context (SC)** | Who you are and how you monetize | Dictates attribute prioritization |
| **Central Search Intent (CSI)** | The unified action connecting CE and SC | Core predicates (verbs) used site-wide |
| **Core Section (CS)** | Content for direct monetization | Receives highest PageRank flow |
| **Author Section (AS)** | Supplementary content building authority | Links back to Core Section |

**Architecture**: Hub-Spoke structure with 1:7 ratio (1 hub to 7 spokes)

**Quality Target**: Semantic Compliance Score >85%, Context Coherence Score >0.8

---

## Task Routing

Based on your task, reference the appropriate sub-file:

### Content Strategy & Architecture
- **Creating a Topical Map** -> Read `frameworks/topical-maps.md`
- **Website type-specific rules** -> Read `frameworks/website-types.md`
- **Entity-Attribute-Value architecture** -> Read `frameworks/eav-architecture.md`

### Content Creation
- **Creating Content Briefs** -> Read `frameworks/content-briefs.md`
- **Writing content** -> Read `frameworks/algorithmic-authorship.md`
- **Understanding semantic distance** -> Read `concepts/semantic-distance.md`

### Auditing & Validation
- **Full page audit** -> Read `audits/on-page-audit.md`
- **Knowledge graph validation** -> Read `audits/knowledge-graph-validation.md`
- **Semantic compliance scoring** -> Read `audits/semantic-compliance.md`
- **Technical/CoR audit** -> Read `audits/technical-audit.md`

### Advanced Concepts
- **Contextual flow & hierarchy** -> Read `concepts/contextual-flow.md`
- **Internal linking strategy** -> Read `concepts/internal-linking.md`
- **Sentence-level optimization** -> Read `concepts/micro-semantics.md`
- **Cost of Retrieval optimization** -> Read `concepts/cost-of-retrieval.md`

### Reference
- **Terminology glossary** -> Read `reference/terminology.md`
- **Patent insights** -> Read `reference/patents-summary.md`

---

## Quick Reference

### EAV Triple Structure
```
Entity (Subject) -> Attribute (Predicate) -> Value (Object)
Example: Germany -> Population -> 83 million
```

### Attribute Types (Priority Order)
1. **Unique Attributes** - Definitive features (e.g., Eiffel Tower for France)
2. **Root Attributes** - Essential definitions (e.g., Population, Capital)
3. **Rare Attributes** - Specific details proving expertise

### Content Quality Rules
- **One EAV triple per sentence** (maximize Information Density)
- **First 400 characters** must contain the core answer (Centerpiece Annotation)
- **First sentence after heading** must directly answer the heading's question
- **No modality** (can, might, should) for established facts - use definitive "is"
- **Explicit naming** - avoid pronouns that create ambiguity

### Internal Linking Rules
- Same anchor text **max 3 times** per page
- Links placed **after** entity/concept is defined
- **Annotation text** (surrounding text) must semantically support the link
- Total links per page: **<150** recommended
- Links in Main Content weighted higher than boilerplate

### Compliance Targets
| Metric | Target |
|--------|--------|
| Semantic Compliance Score | >85% |
| Context Coherence Score | >0.8 |
| Featured Snippet Answer | <40 words or <340 chars |
| Server Response Time | <100ms |
| DOM Size | <1500 nodes |

---

## How to Use This Skill

1. **Identify your task type** from the routing section above
2. **Read the relevant sub-file(s)** for detailed rules and checklists
3. **Apply the rules systematically** - the framework is interconnected
4. **Validate against compliance targets** before finalizing

For terminology questions, consult `reference/terminology.md`.

---

## Critical Principles

### The Blind Librarian Model
Treat search engines as unable to see context implicitly. Communication must be:
- **Explicit** - State definitions directly
- **Consistent** - Use same facts/values everywhere
- **Structured** - Use semantic HTML, schema markup
- **Efficient** - Minimize computational cost through clarity

### Progressive Context Flow
Documents must flow: **Macro Context -> Micro Context -> Micro-Semantic Detail**

Each transition requires a **Contextual Bridge** - a justified connection between topics.

### Knowledge-Based Trust (KBT)
All facts (EAV triples) must be consistent across the entire Semantic Content Network. Contradictions reduce trust scores and increase Cost of Retrieval.
