---
name: technical-blog-writing
description: |
  Guides writing engaging technical blog posts that developers actually read. Triggers on: "write a blog post", "blog post about", "technical article", "write about [topic]", "review my blog post", "improve this article", "technical writing", "structure my post", "draft a post", "help me write", "publishing a tutorial", or mentions of dev.to, Medium, or Hacker News.
allowed-tools:
  - Read
  - Edit
  - Write
  - WebSearch
  - WebFetch
---

# Technical Blog Writing

Write technical posts that developers actually read by following proven patterns
and classic style principles.

## Core Principles

### The Story Spine

Structure posts using narrative arc:

1. **Setup** — Establish context and the status quo
2. **Problem** — Introduce the friction or challenge
3. **Struggle** — Show what was tried, what didn't work
4. **Solution** — Present the approach that worked
5. **Improved State** — Demonstrate the outcome

This "man in hole" pattern activates reader engagement and retention.

### First Three Sentences

Answer two questions immediately:

- "Is this article for me?"
- "What will I gain from reading this?"

Avoid meandering introductions. Developers have short attention spans.

### The Skim Test

Headers alone should tell the complete story.

**Weak:** "Background", "Technical Details", "Implementation" **Strong:** "Why
Copy-Pasting Wasn't Cutting It", "40% Fewer Tokens with TOON"

## Elements of Style

For detailed examples, see
[references/elements-of-style.md](references/elements-of-style.md).

### Active Voice (Rule 10)

| Passive                                 | Active                         |
| --------------------------------------- | ------------------------------ |
| "The API was reverse engineered"        | "I reverse engineered the API" |
| "A survey was made"                     | "We surveyed"                  |
| "There were leaves lying on the ground" | "Leaves covered the ground"    |

### Positive Form (Rule 11)

Make definite assertions. Avoid non-committal language.

| Negative                        | Positive               |
| ------------------------------- | ---------------------- |
| "He was not very often on time" | "He usually came late" |
| "did not remember"              | "forgot"               |
| "did not pay attention to"      | "ignored"              |
| "not important"                 | "trifling"             |

### Specific and Concrete (Rule 12)

| Vague                             | Specific                         |
| --------------------------------- | -------------------------------- |
| "A period of unfavorable weather" | "It rained every day for a week" |
| "significantly faster"            | "40% faster"                     |
| "a few hours"                     | "4 to 5 hours"                   |
| "many test cases"                 | "630+ test cases"                |

### Omit Needless Words (Rule 13)

Vigorous writing is concise. Make every word tell.

| Wordy                        | Concise        |
| ---------------------------- | -------------- |
| "the question as to whether" | "whether"      |
| "owing to the fact that"     | "because"      |
| "he is a man who"            | "he"           |
| "this is a subject which"    | "this subject" |
| "the fact that"              | omit entirely  |

### Emphatic Position (Rule 18)

Place important words at sentence end.

**Weak:** "TOON makes a difference, surprisingly." **Strong:** "That's the
difference between asking a follow-up question or hitting your context limit."

### Parallel Construction (Rule 15)

Express co-ordinate ideas in similar form.

**Non-parallel:** "Formerly by textbook method, while now laboratory method is
employed" **Parallel:** "Formerly by textbook; now by laboratory"

### One Paragraph Per Topic (Rule 8)

Each paragraph signals a new step. Begin with topic sentence; end in conformity
with beginning.

### Vary Sentence Structure (Rule 14)

Avoid succession of loose sentences joined by "and", "but", "so", "which". Mix
simple sentences, semicolons, and periodic sentences.

## Punctuation Rules

### Oxford Comma (Rule 2)

"red, white, and blue" — comma after each term except last.

### No Comma Splice (Rule 5)

Use semicolon for independent clauses without conjunction: "The romances are
entertaining; they are full of adventures."

### Dangling Modifiers (Rule 7)

Opening phrase must refer to grammatical subject.

**Wrong:** "Being dilapidated, I bought the house cheap." **Right:** "Being
dilapidated, the house was available cheap."

## Words to Avoid

- **factor, feature** — usually adds nothing; be specific
- **interesting** — make it interesting; don't announce it
- **very** — use sparingly; prefer strong words
- **literally** — don't use for exaggeration
- **one of the most** — threadbare opener

## Structure Patterns

### The "How I Built X" Pattern

1. **Hook** — What you built and why it matters
2. **Context** — Brief background for unfamiliar readers
3. **The Problem** — What pain point drove this work
4. **The Journey** — What you tried, prior art you found
5. **The Solution** — How the tool/approach works
6. **Concrete Examples** — Real usage with actual output
7. **Under the Hood** — Technical details for curious readers
8. **Get Started** — Single, clear call to action

### The "Technique/Pattern" Pattern

1. **Hook** — The technique and its benefit
2. **The Problem** — Traditional approach and its issues
3. **The Better Approach** — Step-by-step methodology
4. **Real-World Results** — Metrics and outcomes
5. **Why This Works** — Insight behind the technique
6. **When to Use** — Applicability and limitations
7. **Conclusion** — Summary with actionable takeaway

## Engagement Techniques

### Show Concrete Value

Include at least one of:

- A practical technique readers can apply
- Clear explanation of impactful concepts
- Real terminal output or code examples

### Add Visual Breaks

- Code blocks with real output
- Tables comparing approaches
- Bullet points for lists
- Short paragraphs (2-4 sentences)

### Include Real Examples

Don't describe—show:

```
$ command --format json | wc -c
  15234

$ command --format optimized | wc -c
  9140
```

Same data. 40% smaller.

## Review Checklist

Before publishing:

- [ ] First 3 sentences hook and explain value
- [ ] Headers pass skim test
- [ ] Active voice throughout
- [ ] Positive assertions (not "did not" → use direct verb)
- [ ] Specific numbers/metrics
- [ ] Concrete examples with real output
- [ ] No needless words ("the fact that", "in order to")
- [ ] Parallel structure in lists
- [ ] No comma splices
- [ ] No dangling modifiers
- [ ] Emphatic words at sentence ends
- [ ] Single, clear call to action
- [ ] Would I read this on Hacker News?
