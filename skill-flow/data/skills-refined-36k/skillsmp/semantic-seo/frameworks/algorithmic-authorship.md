# Algorithmic Authorship

Algorithmic Authorship is a set of writing rules optimized for search engine NLP algorithms. The goal is to maximize Information Density, ensure fact extractability, and minimize Cost of Retrieval while maintaining authentic, expert content.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Sentence Structure Rules](#sentence-structure-rules)
3. [Information Density](#information-density)
4. [Modality and Certainty](#modality-and-certainty)
5. [Author Identity](#author-identity)
6. [Validation Checklist](#validation-checklist)

---

## Core Principles

### The Goal
Write content that search engines can:
1. **Parse efficiently** (low Cost of Retrieval)
2. **Extract facts accurately** (clear EAV triples)
3. **Trust as authoritative** (consistent, expert, verifiable)

### The Anti-Patterns to Avoid

| Pattern | Why It's Bad | Example |
|---------|-------------|---------|
| Long, complex sentences | Increases semantic complexity | "The product, which was designed by experts in the field of ergonomics who have studied human behavior for decades, features..." |
| Vague language | No extractable facts | "It's really good and many people like it" |
| Ambiguous pronouns | NER confusion | "He said it was important" (who? what?) |
| Generic AI phrases | Signals low-quality | "I had the pleasure of visiting", "Overall", "In conclusion" |
| Hedging language | Reduces authority | "It might possibly be somewhat helpful" |

---

## Sentence Structure Rules

### Rule 1: Subject-Predicate-Object (S-P-O)

Every sentence should follow clear S-P-O structure:

| Component | Function | Example |
|-----------|----------|---------|
| Subject | The entity | "The iPhone 15" |
| Predicate | The action/relation | "weighs" |
| Object | The value/target | "171 grams" |

**Correct**: "The iPhone 15 weighs 171 grams."
**Incorrect**: "At 171 grams, the weight of the iPhone 15 is something that users appreciate."

### Rule 2: One Fact Per Sentence

Each sentence should deliver **one unique EAV triple**.

**Correct**:
```
Germany has a population of 83 million.
The capital of Germany is Berlin.
Germany uses the Euro as its currency.
```

**Incorrect**:
```
Germany, a central European country with a population of 83 million, has Berlin as its capital and uses the Euro as currency.
```

### Rule 3: Short Dependency Trees

Keep sentences short to minimize parsing complexity:

| Sentence Type | Max Length | Use Case |
|--------------|------------|----------|
| Definitional | 15-20 words | Facts, definitions |
| Explanatory | 20-30 words | Context, relationships |
| Instructional | 10-15 words | How-to steps |

### Rule 4: Explicit Entity Naming

Never rely on pronouns when ambiguity is possible:

**Correct**: "Einstein published his theory of relativity. Einstein received the Nobel Prize in 1921."
**Incorrect**: "Einstein published his theory of relativity. He received the Nobel Prize in 1921."

**Exception**: Use pronouns only when a single entity was mentioned in the immediate prior sentence with no possibility of confusion.

### Rule 5: Word Order for Prominence

Place the most important terms early in sentences:

**For entity prominence**: Start with the entity
- "Germany is the largest economy in Europe."

**For attribute prominence**: Start with the attribute
- "The population of Germany is 83 million."

**For value prominence**: Start with the value
- "83 million people live in Germany."

---

## Information Density

### Definition
Information Density = Unique facts / Total words

### High Density Example
```
"The iPhone 15 weighs 171 grams, measures 147.6mm tall, and features a 6.1-inch display."
(3 facts in 18 words = 0.17 density)
```

### Low Density Example
```
"The iPhone 15 is a really great phone that many people love. It has a wonderful design that Apple worked very hard on."
(0 facts in 24 words = 0 density)
```

### Density Rules

| Rule | Implementation |
|------|----------------|
| No filler words | Remove "very", "really", "basically", "actually" |
| No redundancy | Don't repeat the same fact in different words |
| No opinions without evidence | "Best" must be justified by metrics |
| Specific values | Replace "many" with exact numbers |
| Direct answers | Answer questions immediately |

### Fluff Words to Remove

```
REMOVE: actually, basically, really, very, quite, rather, somewhat,
        overall, in conclusion, as stated before, it goes without
        saying, needless to say, at the end of the day, in my opinion,
        I had the pleasure of, it is important to note that
```

---

## Modality and Certainty

### When to Use Each Modality

| Modality | Use When | Example |
|----------|----------|---------|
| **is/are** (definitive) | Established, consensus facts | "Water boils at 100 degrees C" |
| **can/may** (possibility) | Conditional outcomes | "Dehydration can cause headaches" |
| **should/must** (advice) | Recommendations | "You should drink 8 glasses daily" |
| **might/could** (uncertainty) | Disputed or variable facts | "This might vary by individual" |

### Modality Rules

| Context | Correct Modality | Incorrect |
|---------|-----------------|-----------|
| Scientific consensus | "X is Y" | "X can be Y" |
| Variable outcomes | "X can cause Y" | "X causes Y" |
| Professional advice | "You should do X" | "You must do X" |
| Uncertain claims | "X might be Y" | "X is Y" |

### Truth Ranges

When exact values are uncertain, use truth ranges:

**Correct**: "The processing time is typically 10-15 business days."
**Incorrect**: "The processing time is about 12 days."

---

## Author Identity

### Creating Unique Stylometry

Your author must have a distinctive "Expression Identity" that differentiates from generic AI output.

### Author Entity Requirements

| Requirement | Implementation |
|-------------|----------------|
| Schema markup | Use Article structured data with author info |
| Consistent naming | Same author name format everywhere |
| Expertise signals | Domain expert credentials |
| External citations | Author mentioned on external sources |

### Avoiding AI Detection Patterns

| Pattern to Avoid | Alternative |
|------------------|-------------|
| "I had the pleasure of visiting" | Direct statement of experience |
| "Overall" at end of sections | Specific conclusion with facts |
| "In today's world" | Specific timeframe or context |
| "It's important to note" | State the fact directly |
| Lists starting with "Firstly, Secondly" | Numbered lists or direct statements |

### Building Author Authority

| Signal | Method |
|--------|--------|
| Publishing frequency | Regular updates (not sporadic) |
| External citations | Get mentioned on Wikipedia, podcasts, papers |
| Credential display | Show licenses, awards, qualifications |
| Unique research | Original data, studies, methodologies |

---

## Validation Checklist

### Sentence-Level Checks

```
[ ] Each sentence has clear S-P-O structure
[ ] One fact per sentence
[ ] Sentences under 30 words
[ ] No ambiguous pronouns
[ ] Explicit entity naming
[ ] Important terms early in sentence
```

### Density Checks

```
[ ] No filler words
[ ] No redundant statements
[ ] Specific values (not "many", "some")
[ ] Direct answers to questions
[ ] Opinions justified by evidence
```

### Modality Checks

```
[ ] Definitive modality for consensus facts
[ ] Conditional modality for variable outcomes
[ ] Advisory modality for recommendations
[ ] Truth ranges for uncertain values
```

### Author Identity Checks

```
[ ] Author schema implemented
[ ] No generic AI phrases
[ ] Consistent author naming
[ ] Expertise signals present
[ ] External citations available
```

### Content Quality Score

Rate each section 1-5:

| Criterion | Score |
|-----------|-------|
| Information Density | /5 |
| Sentence Clarity | /5 |
| Modality Appropriateness | /5 |
| Author Authority Signals | /5 |
| **Total** | /20 |

Target: 16+ for high-quality content
