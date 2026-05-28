# Workflow: Explore

Initial exploration of a new topic or research question.

## Prerequisites
- Query or topic defined in `/workspace/brief.md`
- Or explicit research question provided

## Steps

### 1. Decompose the Query

Break the main question into 3-5 searchable sub-questions.

**Example:**
- Main: "How does structural friction improve AI reliability?"
- Sub-queries:
  1. "What is cognitive friction in decision systems?"
  2. "Evidence that slower decisions improve accuracy"
  3. "AI system failures from automation bias"
  4. "Friction mechanisms in safety-critical systems"
  5. "Adversarial robustness through deliberation"

Write decomposition to working notes.

### 2. Broad Search Pass

For each sub-question:

```
web_search("[sub-question keywords]")
```

**Search tips:**
- Keep queries concise (4-8 words)
- Try multiple phrasings
- Include domain-specific terms
- Search for critiques, not just confirmations

### 3. Identify High-Quality Sources

From initial results, identify:
- Academic papers (look for .edu, .gov, journal sites)
- Primary sources (original reports, data)
- Expert analysis (recognized authorities)
- Quality journalism (investigative, well-cited)

**Skip:**
- Content farms
- Listicles without sources
- SEO-optimized summaries
- Sources that cite each other circularly

### 4. Deep Fetch

For top 3-5 sources per sub-question:

```
web_fetch("[url]")
```

Extract:
- Key claims with supporting quotes
- Methodology (for academic sources)
- Citations worth following
- Author credentials
- Publication date

### 5. Citation Chasing

For the best 2-3 sources:
- Identify their most important references
- Search for those original sources
- Go 2-3 hops deep for foundational work

```
web_search("[cited paper title] [author]")
web_fetch("[found URL]")
```

### 6. Contradictory Evidence Search

Explicitly search for opposing views:

```
web_search("[topic] criticism")
web_search("[topic] fails OR failure OR problem")
web_search("[topic] alternative OR instead")
```

### 7. Record Evidence

For each valuable finding, add to `/workspace/evidence.json`:

```json
{
  "id": "ev_001",
  "claim": "Cognitive forcing functions reduce automation bias by 23% in medical diagnosis",
  "source": {
    "url": "https://...",
    "type": "academic",
    "title": "Reducing Automation Bias Through Cognitive Forcing",
    "author": "Smith et al.",
    "date": "2022"
  },
  "retrieved_text": "Our randomized controlled trial found that implementing diagnostic time-outs reduced automation bias from 47% to 24% (p < 0.01)...",
  "confidence": 0.85,
  "retrieval_path": [
    "web_search: cognitive forcing functions medical decisions",
    "web_fetch: https://journal.example.com/paper",
    "citation_chase: original from search result #2"
  ],
  "supports_hypotheses": [],
  "contradicts_hypotheses": [],
  "serendipitous": false,
  "gaps": "Study limited to medical context; unclear if generalizes"
}
```

### 8. Flag Gaps

Document what you couldn't find:

```json
{
  "gaps": [
    "No longitudinal studies on friction mechanisms",
    "Limited evidence outside medical/aviation domains",
    "No cost-benefit analyses found"
  ]
}
```

### 9. Serendipity Check

Before finishing, ask:
- What surprising connections emerged?
- What tangential finding might be valuable?
- What anomaly deserves more attention?

Record any serendipitous findings with `"serendipitous": true`.

### 10. Update State

Update `/workspace/state.json`:

```json
{
  "current_state": "researching",
  "evidence_count": 12,
  "gaps_flagged": 3,
  "ready_for_outline": true
}
```

## Quality Targets

Before marking research complete:

- [ ] Minimum 8-10 evidence items
- [ ] At least 2 different source types
- [ ] At least 1 contradicting/complicating source
- [ ] Citation chain followed for key claims
- [ ] Gaps explicitly documented
- [ ] Confidence scores calibrated

## Next Steps

- If sufficient evidence: Proceed to outlining
- If major gaps: Continue with `verify.md` workflow
- If stuck: Consider `serendipity.md` workflow
