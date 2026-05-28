# Workflow: Citation Chase

Follow citation chains to find foundational sources, original research, and ancestral papers.

## Purpose

> "Ancestral papers that originated an idea are often uncited gold."

Most sources cite secondary summaries. Citation chasing finds the original insight.

## When to Use

- You have a good source but need the original study
- A claim is widely repeated but you can't find primary evidence
- You want to understand how an idea evolved
- Looking for foundational/canonical works in a field

## Steps

### 1. Identify the Seed Source

Start with a high-quality source that makes the claim you're investigating.

Note its key references—especially:
- The citations for core claims
- Foundational works mentioned in the intro
- Methodological references
- The oldest citations (often most foundational)

### 2. Map the Citation Network

Create a quick map:

```
Seed Paper (2023)
├── Cites: Smith 2019 (methodology)
├── Cites: Johnson 2015 (core finding)
│   └── Cites: Original Study 2008 ← TARGET
├── Cites: Review Paper 2020
└── Cites: Tangential 2021
```

Prioritize:
1. Sources cited for the KEY CLAIM you're investigating
2. Older sources (more likely to be foundational)
3. Sources cited by multiple papers in your collection

### 3. Chase Priority Citations

For each priority citation:

```
web_search("[paper title]" "[author last name]")
web_search("[paper title]" filetype:pdf)
web_search("[paper title]" site:scholar.google.com)
```

If paywalled, try:
```
web_search("[paper title]" site:arxiv.org)
web_search("[paper title]" site:researchgate.net)
web_search("[paper title]" preprint)
```

### 4. Go Deeper (Hop 2)

When you find a key intermediate source, repeat:
- What does IT cite for the core claim?
- Can you find THAT source?

Usually 2-3 hops reveals the original:

```
Your Search (2024)
  → Found: Review Paper (2020)
    → Cites: Empirical Study (2015)
      → Cites: Original Theory Paper (2003) ← FOUND IT
```

### 5. Verify You Found the Origin

Signs you've found the original source:
- It introduces the concept/term for the first time
- Earlier papers don't discuss this topic
- Later papers all cite this one
- The author is considered foundational in the field

Signs you need to go deeper:
- Paper says "as shown by [earlier work]..."
- Paper is a replication or extension
- Paper references "the original study"

### 6. Extract and Record

When you find a foundational source:

```json
{
  "id": "ev_020",
  "claim": "Cognitive forcing functions were first proposed for medical diagnosis",
  "source": {
    "url": "https://...",
    "type": "primary",
    "title": "Diagnostic Time-Outs: A Cognitive Forcing Strategy",
    "author": "Croskerry",
    "date": "2003"
  },
  "retrieved_text": "We propose the term 'cognitive forcing strategy' to describe deliberate mental steps taken to avoid cognitive errors...",
  "confidence": 0.95,
  "retrieval_path": [
    "citation_chase: started from Smith 2023",
    "citation_chase: hop 1 → Johnson 2015",
    "citation_chase: hop 2 → Croskerry 2003 (origin)",
    "web_fetch: found via Google Scholar"
  ],
  "is_foundational": true,
  "cited_by_count": "500+",
  "notes": "Original coining of 'cognitive forcing strategy' - this is the primary source"
}
```

### 7. Note the Lineage

Document how ideas evolved:

```
Concept: Cognitive Forcing Functions

Origin: Croskerry 2003 - coined term, medical diagnosis context
  ↓
Extension: Graber 2005 - expanded to clinical reasoning
  ↓
Empirical: Singh 2012 - first RCT showing effectiveness
  ↓
Generalization: Berner 2016 - applied to AI-assisted decisions
  ↓
Current: Smith 2023 - our seed source
```

This lineage helps you:
- Cite the right source for the right claim
- Understand how the idea changed over time
- Identify where extensions might have introduced errors

## Citation Chase Patterns

### Pattern: The Hidden Classic
A widely-cited paper actually got the idea from an obscure older source.
**Solution**: Check the intro/background for "this concept originated in..."

### Pattern: The Misattribution
Everyone cites Paper A, but the idea actually came from Paper B.
**Solution**: Read Paper A carefully—does it credit someone else?

### Pattern: The Lost Original
The original is a conference paper, dissertation, or technical report that's hard to find.
**Solution**: Try Internet Archive, author's personal site, university repositories.

### Pattern: The Parallel Discovery
Two researchers developed similar ideas independently.
**Solution**: Note both origins; they may have useful differences.

## Quality Indicators

Good citation chase:
- [ ] Found source that introduces the concept
- [ ] Confirmed no earlier sources exist
- [ ] Documented the citation lineage
- [ ] Primary source text retrieved (not just metadata)

## Integration

After successful citation chase:
- Update evidence.json with foundational source
- Adjust confidence on claims now backed by primary sources
- Note in outline.md which claims have primary source support
