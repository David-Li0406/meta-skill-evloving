# Core SEO/AEO Requirements

Universal requirements for Lightfast pages.

## 1. Answer-First Architecture

### TL;DR Section

**Purpose**: AI citation, featured snippets, quick scanning

**Requirements**:
- 40-100 words
- Self-contained paragraph (no references to "below")
- Covers key user benefits
- Quotable as standalone text
- No bullet points (flowing prose)
- Position: Immediately after title

**Example**:
```markdown
Lightfast Neural Memory automatically captures and organizes decisions,
discussions, and context from your tools—Slack, GitHub, Linear, and more.
Your team can now search by meaning across all sources, get answers with
citations, and trace the reasoning behind any decision. This release marks
our shift from simple indexing to true organizational memory.
```

### Direct Answer Placement

- Primary answer in first 100-200 words
- Use definition boxes for key terms
- Start sections with the answer, then explain

**Pattern**:
```markdown
## How does Neural Memory work?

Neural Memory works by connecting to your tools via OAuth, indexing content
using vector embeddings, and enabling semantic search across all sources.
This approach allows you to search by meaning rather than exact keywords...
```

## 2. Meta Description

**Requirements**:
- Exactly 150-160 characters
- Include primary keyword
- Match actual page content
- End with benefit or CTA
- Use active voice

**Template**:
```
[Primary action/benefit] with [feature]. [Secondary benefit in 2-3 words]. [CTA or qualifier].
```

**Example** (158 chars):
```
Build organizational memory with Lightfast's semantic search and webhook-driven
sync. Connect your tools, search by meaning, trace every decision. Start free.
```

## 3. Question-Based Headings

AI engines parse question headings for voice search and conversational queries.

**Do**:
```markdown
## What is Neural Memory?
## How do I set up GitHub integration?
## Why use vector search over keyword search?
```

**Don't**:
```markdown
## Overview
## Introduction
## Getting Started
## Conclusion
```

## 4. Structured Content Elements

### Comparison Tables

AI can easily extract structured comparisons.

**Pattern**:
```markdown
| Feature | Free | Pro | Enterprise |
|---------|------|-----|------------|
| Repositories | 3 | Unlimited | Unlimited |
| Vector storage | 100MB | 10GB | Custom |
| Team members | 1 | 10 | Unlimited |
| Support | Community | Email | Dedicated |
```

**Requirements**:
- Include units (MB, ms, $/month)
- Add caveats where applicable
- Use consistent column structure

### Bullet Lists

For scannable key points:
- Start each bullet with action verb or key term
- Keep items parallel in structure
- 3-7 items per list (cognitive load)
- Use numbered lists for sequential steps

### Definition Boxes

For key terminology:
```markdown
> **Vector Search**: A retrieval method that finds semantically similar
> content by comparing embedding vectors, enabling "search by meaning"
> rather than exact keyword matching.
```

## 5. FAQ Section

**Purpose**: FAQPage schema, featured snippets, voice search

**Requirements**:
- 3-5 questions per page
- Questions match real search queries
- Each answer is complete and self-contained (2-3 sentences)
- No "as mentioned above" or "see below"

**Question Types**:
- "What is X?" (definition)
- "How do I X?" (procedural)
- "Why should I use X?" (benefits)
- "What's the difference between X and Y?" (comparison)

**Example**:
```yaml
faq:
  - question: "What is webhook-driven sync?"
    answer: "Webhook-driven sync automatically updates your Lightfast knowledge
      base when changes occur in connected tools. Instead of polling, Lightfast
      receives instant notifications, ensuring sub-minute latency for updates."
  - question: "How do I set up GitHub integration?"
    answer: "Navigate to Settings > Integrations, click 'Add GitHub', and
      authorize the Lightfast GitHub App. Select repositories to sync and
      configure file patterns. Webhooks are automatically configured."
```

## 6. Internal Linking

**Requirements**:
- 3-5 internal links per page
- Use descriptive anchor text (not "click here")
- Link to related Lightfast content
- Create topic clusters (pillar page + supporting articles)

**Link Patterns**:
```markdown
Learn more about [Neural Memory](/features/neural-memory) to see how semantic
search transforms knowledge retrieval.

For API usage, see the [API Reference](/api-reference).

Configure file patterns in your [lightfast.yml](/config).
```

## 7. External Citations (E-E-A-T)

**Minimum**: 5+ external sources for content pages

**Source Types**:
- Research papers (arXiv, Google Research)
- Industry reports (Gartner, Forrester)
- Technical documentation (official docs)
- News sources (TechCrunch, The Verge)

**Citation Format**:
```markdown
According to [Forrester Research](https://forrester.com/...), 40% of
enterprise search queries now originate from AI assistants.
```

## 8. Author Attribution

**Purpose**: E-E-A-T signals for AI trust

**Requirements**:
- Visible author name and role
- Years of experience (if relevant)
- Link to profile (Twitter/LinkedIn)
- Author bio at end of article

**Default Author**: Jeevan Pillay, Founder

## 9. Content Freshness

**Signals**:
- `publishedDate`: Original publication
- `modifiedDate`: Last significant update
- "Last updated" visible on page
- Regular 90-day content reviews (Perplexity prioritizes recent content)

## SEO Checklist

### Required Fields
- [ ] Meta description: 150-160 chars with keyword
- [ ] TL;DR: 40-100 words, self-contained
- [ ] Focus keyword selected and used naturally (2-3 times)
- [ ] Question-format headings for key sections

### Content Requirements
- [ ] Direct answer in first 200 words
- [ ] 3-5 internal links
- [ ] At least one comparison table or structured list
- [ ] FAQ section with 3-5 Q&A pairs

### Technical Requirements
- [ ] Canonical URL set (https://lightfast.ai/...)
- [ ] OpenGraph tags complete
- [ ] JSON-LD schema implemented
- [ ] Image alt text optimized
