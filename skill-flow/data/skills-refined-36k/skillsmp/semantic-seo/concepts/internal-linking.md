# Internal Linking Strategy

Internal links signal contextual relationships between content nodes, governing the flow of relevance and authority (PageRank) throughout your Semantic Content Network. Proper linking consolidates ranking signals; improper linking dilutes them.

## Table of Contents

1. [Linking Fundamentals](#linking-fundamentals)
2. [Anchor Text Rules](#anchor-text-rules)
3. [Annotation Text](#annotation-text)
4. [Link Placement](#link-placement)
5. [PageRank Flow](#pagerank-flow)

---

## Linking Fundamentals

### The Purpose of Internal Links

| Function | How It Works |
|----------|--------------|
| **Authority transfer** | PageRank flows through links |
| **Context signaling** | Links communicate topic relationships |
| **Navigation** | Guide users and crawlers |
| **Indexation** | Help discover new content |

### Link Quality Factors

| Factor | Good | Bad |
|--------|------|-----|
| **Relevance** | Semantically close topics | Distant/random connections |
| **Context** | Supported by surrounding text | Isolated, no context |
| **Placement** | In main content | Buried in boilerplate |
| **Quantity** | Focused, intentional | Excessive, diluted |

---

## Anchor Text Rules

### The Max 3x Rule

**Rule**: The same exact anchor text can appear at most 3 times per page in main content.

| Count | Action |
|-------|--------|
| 1-3 | Allowed |
| 4+ | Use variations |

**Variations to use**:
- Synonyms: "Germany Visa" -> "German visa application"
- Word order: "visa for Germany" -> "Germany's visa requirements"
- Hyponyms: "visa" -> "tourist visa", "work visa"

### Anchor Text Types

| Type | Example | Use Case |
|------|---------|----------|
| **Exact match** | "Germany Visa" | Primary keyword |
| **Partial match** | "applying for your Germany visa" | Natural variation |
| **Branded** | "Our visa guide" | Internal reference |
| **Generic** | "click here", "read more" | Avoid (except minimal) |

### Lexical Hierarchy in Anchors

Organize anchor text by semantic level:

```
Page Position:        Anchor Type:
Higher on page   ->   Hypernyms (broader): "European Visas"
Middle of page   ->   Core term: "Germany Visa"
Lower on page    ->   Hyponyms (specific): "D-Type Student Visa"
```

### Anchor Text Checklist

```
[ ] No exact anchor repeated >3 times
[ ] Variations used for repeated links
[ ] Anchors follow lexical hierarchy
[ ] Generic anchors minimized
[ ] Anchor matches target page H1/title
```

---

## Annotation Text

### What is Annotation Text?

The text immediately surrounding a link that provides context for both users and search engines.

### Annotation Quality Rules

| Rule | Implementation |
|------|----------------|
| **Semantic alignment** | Surrounding text discusses target topic |
| **Context support** | Annotation prepares reader for link |
| **Entity mention** | Target page's entity mentioned nearby |

### Good vs Bad Annotation

**Good Annotation**:
```
"Understanding German immigration requirements is essential
for a successful application. Learn more about the
[Germany visa process] and ensure you meet all criteria."
```

**Bad Annotation**:
```
"For more information, [click here]."
```

### Annotation Radius

The annotation text extends:
- **Before link**: 1-2 sentences establishing context
- **After link**: Optional continuation of thought

### Annotation Checklist

```
[ ] Surrounding text relates to target page topic
[ ] Target page's main entity mentioned near anchor
[ ] Context prepares reader for the linked content
[ ] Not just isolated link without context
```

---

## Link Placement

### The Definition-First Rule

**Rule**: Never link to a concept before it has been defined in the content.

| Placement | Correct | Incorrect |
|-----------|---------|-----------|
| After definition | Define entity, then link | Link before explanation |
| In main content | Middle/end of sections | First sentence/word |
| Strategic | Important pages prioritized | Random distribution |

### Link Position Hierarchy

| Position | Weight | Use For |
|----------|--------|---------|
| **Main content** | Highest | Most important links |
| **In-content lists** | High | Supporting resources |
| **Sidebar (dynamic)** | Medium | Related content |
| **Footer/header** | Lower | Site-wide navigation |

### Dynamic Navigation

**Static sidebar** (bad):
- Same links on every page
- No contextual relevance
- PageRank dilution

**Dynamic sidebar** (good):
- Links change per page
- Shows related attributes
- Contextually relevant

### Jump Links (URL Fragments)

Use for long articles:

```html
<h2 id="section-name">Section Title</h2>

<a href="#section-name">Jump to Section</a>
```

**Requirements**:
- Table of Contents linking to H2s/H3s
- IDs on all major headings
- Clear section naming

---

## PageRank Flow

### Link Count Guidelines

| Metric | Target | Why |
|--------|--------|-----|
| Total internal links | <150 | Preserve value per link |
| Main content links | >50% of total | Prioritize quality |
| Boilerplate links | <50% of total | Don't dilute main |

### PageRank Distribution

```
High PR Flow:
[Homepage] ---high weight---> [Core Section]
                                    v
                             [Key Products/Services]

Low PR Flow:
[Author Section] ---links to---> [Core Section]
(Supports but doesn't compete)
```

### Link Flow Direction

| From | To | Direction |
|------|-----|-----------|
| Author Section | Core Section | Correct |
| Low-value pages | High-value pages | Correct |
| Core Section | Author Section | Sparingly |
| All pages | Homepage | Balanced |

### Avoiding Dilution

| Issue | Problem | Solution |
|-------|---------|----------|
| Too many links | Each link worth less | Reduce to essential |
| Mega menus | 100s of links per page | Dynamic, contextual nav |
| Footer link farms | Excessive boilerplate links | Minimize, prioritize |
| Sidebar overload | Same links everywhere | Dynamic sidebars |

### Link Priority Matrix

| Page Type | Receives Links From | Links To |
|-----------|-------------------|----------|
| Homepage | All pages (minimal) | Core Section heavily |
| Core Section | Homepage, Author Section | Products/Services |
| Products/Services | Core Section, Related | Related products |
| Author Section | Core (sparingly) | Core Section heavily |

---

## Internal Linking Audit

### Quick Audit Checklist

```
[ ] Total links per page <150
[ ] Main content has >50% of links
[ ] No anchor text repeated >3x
[ ] Links placed after definitions
[ ] Annotation text supports links
[ ] Dynamic navigation (not static everywhere)
[ ] AS links to CS more than reverse
[ ] Jump links on long pages
```

### Link Audit Template

| Page URL | Total Links | Main Content | Boilerplate | Issues |
|----------|-------------|--------------|-------------|--------|
| /page-1 | | | | |
| /page-2 | | | | |

### Common Issues & Fixes

| Issue | Detection | Fix |
|-------|-----------|-----|
| Over-linking | >150 per page | Reduce, prioritize |
| Under-linking | <10 per page | Add contextual links |
| Boilerplate heavy | >50% in nav/footer | Implement dynamic nav |
| Anchor repetition | Same text >3x | Use variations |
| Early linking | Links in first paragraph | Move after definition |
| Poor annotation | "Click here" type | Add contextual text |

### Ideal Link Profile

```
Per Page Target:
|---- Main content links: 15-30
|---- Navigation: 10-20 (dynamic)
|---- Footer: 5-10 (essential only)
|---- Related content: 3-5
---- Total: 50-75

Link Direction:
|---- To Core Section: High
|---- To Homepage: Moderate
|---- To Author Section: Low
---- External: Minimal
```
