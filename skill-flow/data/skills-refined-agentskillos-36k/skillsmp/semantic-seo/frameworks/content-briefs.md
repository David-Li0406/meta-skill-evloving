# Content Brief Framework

The Content Brief is the blueprint for content creation. It defines the precise execution necessary to optimize relevance and reduce the Cost of Retrieval. A well-constructed brief ensures high Semantic Compliance (>85%) and consistent quality across the network.

## Table of Contents

1. [Brief Structure](#brief-structure)
2. [Heading Hierarchy Rules](#heading-hierarchy-rules)
3. [Content Format Rules](#content-format-rules)
4. [Featured Snippet Optimization](#featured-snippet-optimization)
5. [Brief Template](#brief-template)

---

## Brief Structure

### Required Components

Every content brief must specify:

| Component | Purpose | Detail Level |
|-----------|---------|-------------|
| **Macro Context** | Page's primary focus | H1 and main topic |
| **Contextual Vector** | Heading sequence | All H2s, H3s, H4s in order |
| **EAV Requirements** | Required facts | Specific triples to include |
| **Format Specifications** | Content types | Prose, lists, tables per section |
| **Link Instructions** | Internal links | Anchor text, targets, placement |
| **Visual Requirements** | Images/media | Alt text, placement, specifications |

### Brief Quality Rules

| Rule | Requirement | Reason |
|------|-------------|--------|
| Pre-define everything | Headings, formats, anchors specified | Prevents author deviation |
| One Macro Context | Single primary focus per page | Prevents relevance dilution |
| Compliance target | >85% adherence to brief | Ensures network consistency |

---

## Heading Hierarchy Rules

### Structural Rules

| Level | Function | Rules |
|-------|----------|-------|
| **H1** | Page purpose (Macro Context) | One per page, contains CE or main topic |
| **H2** | Distinct sub-contexts | Major topic shifts, new attributes |
| **H3** | Attribute specifications | Details of parent H2 |
| **H4** | Sub-specifications | Rarely needed, deep details only |

### Contextual Vector Flow

Headings must follow **incremental, logical order**:

**Correct Flow**:
```
H1: [Topic Definition]
|---- H2: What is [Topic]?
|---- H2: Types of [Topic]
|   |---- H3: Type A
|   |---- H3: Type B
|---- H2: Benefits of [Topic]
|---- H2: Risks of [Topic]
|---- H2: How to [Action] [Topic]
|   |---- H3: Step 1
|   |---- H3: Step 2
---- H2: [Topic] vs [Alternative]
```

**Incorrect Flow** (broken context):
```
H1: [Topic]
|---- H2: History of [Topic]      <- Too early, should be later
|---- H2: Step 3 of Process       <- Steps out of order
|---- H3: Definition              <- Wrong level (should be H2)
|---- H2: Types                   <- Definition should come first
```

### Heading Content Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Question format | "What are the benefits?" | "Benefits" (no question) |
| Include entity | "Benefits of German Visa" | "Benefits" (missing entity) |
| Specific scope | "Types of D-Type Visa" | "Different Types" (vague) |

---

## Content Format Rules

### Format Selection by Query Type

| Query Type | Optimal Format | HTML Element |
|------------|---------------|--------------|
| Definitional | Prose paragraph | `<p>` |
| Comparison | Table | `<table>` |
| List/Enumeration | Unordered list | `<ul>` |
| Process/How-to | Ordered list | `<ol>` |
| Specification | Definition list or table | `<dl>` or `<table>` |

### List Rules

**Introductory Sentence Required**:
Every list must be preceded by a sentence stating the exact count.

**Correct**:
```
The visa application requires five documents:
1. Valid passport
2. Application form
3. Proof of funds
4. Travel insurance
5. Invitation letter
```

**Incorrect**:
```
Required documents:
- Passport
- Form
- Money proof
...
```

**List Item Rules**:

| Rule | Implementation |
|------|----------------|
| Consistent format | All items start same way (verb, noun, etc.) |
| Instructional lists | Start each item with action verb |
| Ordered lists | Use for sequences, rankings, steps |
| Unordered lists | Use for non-sequential items |

### Table Rules

**Use tables for**:
- Comparisons (>2 items, >3 attributes)
- Specifications
- Pricing/features matrices

**Table Requirements**:
- Clear headers
- Consistent data formatting
- No merged cells (accessibility)
- Caption or title

---

## Featured Snippet Optimization

### Featured Snippet (FS) Zones

| Zone | Location | Optimization |
|------|----------|-------------|
| **IR Zone** | First 400 characters | Must contain core answer |
| **Subordinate Text** | First sentence after heading | Direct answer to heading question |
| **List Zone** | After question heading | Numbered/bulleted answer |

### FS Answer Requirements

| Format | Length Limit | Structure |
|--------|-------------|-----------|
| Paragraph | <340 characters or <40 words | Direct answer, no fluff |
| List | 3-8 items | Introductory sentence + list |
| Table | 3-5 rows visible | Headers + key data |

### Subordinate Text Rules

The first sentence after any heading (H2, H3) must:

| Requirement | Example |
|-------------|---------|
| Answer directly | H2: "What is X?" -> "X is..." |
| Match question format | H2: "How to do X?" -> "To do X, you must..." |
| Be definitive | No "As stated before" or "In this section" |
| Be concise | <40 words ideal |

**Question-Answer Protection**:

| Question Format | Answer Format |
|-----------------|---------------|
| "What is X?" | "X is..." |
| "What are the benefits?" | "The benefits are/include..." |
| "How to X?" | "To X, follow these steps:" |
| "Why does X happen?" | "X happens because..." |
| "When should you X?" | "You should X when..." |

---

## Brief Template

### Basic Template

```markdown
# Content Brief: [Page Title]

## Meta Information
- **Target URL**: /path/to-page
- **Primary Keyword**: [main keyword]
- **Search Intent**: [informational/transactional/navigational]
- **Word Count Target**: [X-Y words]
- **Compliance Target**: >85%

## Macro Context
- **Central Entity**: [page's main entity]
- **Source Context Alignment**: [how this fits SC]
- **Section Type**: [Core Section / Author Section]

## Contextual Vector (Heading Structure)

### H1: [Exact H1 text]

### H2: [First H2]
- Format: [prose/list/table]
- Required EAVs: [list triples]
- Target: [FS/PAA/standard]

#### H3: [Sub-heading if needed]
- Format: [format type]

### H2: [Second H2]
...

## EAV Requirements

| Entity | Attribute | Value | Source |
|--------|-----------|-------|--------|
| [E1] | [A1] | [V1] | [citation] |

## Internal Link Instructions

| Anchor Text | Target Page | Placement | Notes |
|-------------|-------------|-----------|-------|
| [anchor 1] | [/target-url] | After [section] | Max 3x |

## Image Requirements

| Image | Alt Text | Placement | Dimensions |
|-------|----------|-----------|------------|
| [description] | [alt text] | After [heading] | [WxH] |

## Compliance Notes
- [Specific instructions]
- [Consistency requirements]
- [Format requirements]
```

### Advanced Template Additions

```markdown
## Featured Snippet Targets

| Heading | FS Type | Answer Length | Answer Format |
|---------|---------|---------------|---------------|
| H2: What is X? | Paragraph | <40 words | "X is [definition]" |
| H2: Steps to X | List | 5-7 items | Numbered list |

## Schema Requirements
- Type: [Article/Product/FAQ/etc.]
- Required properties: [list]
- Author: [author name]

## Contextual Bridge Points
- Bridge to Core Section: [anchor + context]
- Bridge from: [related pages linking here]

## Validation Checklist
[ ] All H2s follow incremental order
[ ] Each heading has subordinate text
[ ] All EAVs are consistent with network
[ ] Link count <150
[ ] First 400 chars contain answer
[ ] No fluff words
[ ] Modality appropriate for content type
```

---

## Brief Validation

### Pre-Writing Validation

```
[ ] Macro Context defined (single focus)
[ ] All headings in logical order
[ ] Format specified for each section
[ ] EAV requirements complete
[ ] Link instructions clear
[ ] No conflicting briefs for same topic
```

### Post-Writing Validation

```
[ ] Content matches heading structure
[ ] All EAVs included and accurate
[ ] Formats match specifications
[ ] Links placed correctly
[ ] Subordinate text direct and answering
[ ] First 400 chars contain key answer
[ ] Compliance score >85%
```
