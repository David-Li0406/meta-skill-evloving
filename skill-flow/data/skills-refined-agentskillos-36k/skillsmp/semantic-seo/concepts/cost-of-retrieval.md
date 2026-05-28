# Cost of Retrieval (CoR)

Cost of Retrieval is the computational expense for search engines to crawl, parse, render, understand, and index your content. Minimizing CoR is the foundational goal of Semantic SEO - making it cheaper for search engines to process your site leads to better crawling, indexing, and ranking.

## Table of Contents

1. [Understanding CoR](#understanding-cor)
2. [CoR Components](#cor-components)
3. [Optimization Strategies](#optimization-strategies)
4. [Measuring CoR](#measuring-cor)

---

## Understanding CoR

### The Economic Logic

Search engines have finite resources. They must decide:
- **Which sites to crawl** (allocation)
- **How often to crawl** (frequency)
- **How much to index** (storage)
- **How quickly to rank** (processing)

Sites with lower CoR get:
- More frequent crawling
- Better indexation rates
- Faster ranking updates
- Preferential treatment

### High CoR Signals

| Signal | Why It's Expensive |
|--------|-------------------|
| Large DOM | More parsing work |
| Complex JS | Requires rendering |
| Slow server | Crawler waits |
| Duplicate content | Wasted processing |
| Vague content | Hard to extract meaning |
| Broken structure | Interpretation effort |

### Low CoR Signals

| Signal | Why It's Cheap |
|--------|----------------|
| Clean HTML | Easy parsing |
| Fast response | Quick retrieval |
| Clear structure | Easy segmentation |
| Explicit facts | Direct extraction |
| Consistent data | No reconciliation needed |

---

## CoR Components

### 1. Crawl Cost

Resources spent discovering and fetching content.

| Factor | Impact | Target |
|--------|--------|--------|
| Response time | Time waiting | <100ms |
| Redirects | Extra requests | Minimize |
| Error pages | Wasted requests | 0% |
| Resource requests | Multiple fetches | <50/page |

### 2. Render Cost

Resources spent executing JavaScript and building the DOM.

| Factor | Impact | Target |
|--------|--------|--------|
| JS execution | CPU time | Minimize |
| DOM construction | Memory | <1500 nodes |
| Layout calculation | Processing | Stable (low CLS) |
| Paint operations | Graphics | Optimized |

### 3. Parse Cost

Resources spent understanding content structure.

| Factor | Impact | Target |
|--------|--------|--------|
| DOM complexity | Traversal time | Simple nesting |
| Semantic ambiguity | Interpretation | Clear tags |
| Text-to-code ratio | Extraction ease | >50% text |
| HTML validity | Error handling | Valid markup |

### 4. Extraction Cost

Resources spent identifying and extracting facts.

| Factor | Impact | Target |
|--------|--------|--------|
| Content clarity | NER difficulty | Explicit entities |
| Fact structure | Triple extraction | Clear EAV |
| Ambiguity | Resolution needed | Unambiguous |
| Inconsistency | Cross-checking | Consistent |

### 5. Storage Cost

Resources spent indexing and storing content.

| Factor | Impact | Target |
|--------|--------|--------|
| Duplicate content | Wasted storage | Unique pages |
| Low-value pages | Storage for nothing | Quality content |
| URL bloat | Index size | Consolidated URLs |
| Redundant data | Repeated storage | Deduplicated |

---

## Optimization Strategies

### Server-Level Optimizations

| Strategy | Implementation | CoR Impact |
|----------|----------------|------------|
| Fast hosting | <100ms TTFB | -50% crawl cost |
| CDN | Global distribution | -30% latency |
| Caching | Proper headers | -40% repeat cost |
| Compression | Gzip/Brotli | -60% transfer |

### HTML-Level Optimizations

| Strategy | Implementation | CoR Impact |
|----------|----------------|------------|
| Clean DOM | <1500 nodes | -40% parse cost |
| Semantic HTML | Proper tags | -30% interpretation |
| Remove bloat | No unused code | -50% transfer |
| Validate markup | No errors | -20% error handling |

### Content-Level Optimizations

| Strategy | Implementation | CoR Impact |
|----------|----------------|------------|
| Explicit facts | Clear EAV triples | -40% extraction |
| No ambiguity | Explicit naming | -30% resolution |
| High density | Facts per sentence | -25% processing |
| Consistent data | Same values everywhere | -35% reconciliation |

### Architecture-Level Optimizations

| Strategy | Implementation | CoR Impact |
|----------|----------------|------------|
| URL consolidation | Fewer, better pages | -50% crawl |
| Clear hierarchy | Logical structure | -30% navigation |
| No duplicates | Canonical tags | -40% storage |
| Internal linking | Efficient discovery | -25% exploration |

---

## Measuring CoR

### Log File Analysis

Monitor Googlebot behavior:

| Metric | Target | Indicates |
|--------|--------|-----------|
| HTML hit ratio | >80% | Efficient crawling |
| Average response time | <100ms | Fast serving |
| Crawl frequency | Stable/increasing | Healthy site |
| Error rate | 0% | Clean site |

### Google Search Console

| Report | What to Check |
|--------|---------------|
| Coverage | Indexed vs excluded ratio |
| Crawl Stats | Response times, request trends |
| Core Web Vitals | User experience metrics |
| URL Inspection | Individual page status |

### CoR Indicators

**Good CoR (efficient)**:
- High indexation rate (>90% of submitted)
- Frequent crawling
- Fast response times in GSC
- No "crawled not indexed" issues

**Bad CoR (expensive)**:
- "Crawled - currently not indexed"
- "Discovered - not indexed"
- Declining crawl rate
- High error rates
- Slow response times

### Quick CoR Assessment

Score each factor 1-5:

| Factor | Score | Weight |
|--------|-------|--------|
| Server response time | /5 | 20% |
| DOM simplicity | /5 | 15% |
| Content clarity | /5 | 20% |
| URL efficiency | /5 | 15% |
| Duplicate avoidance | /5 | 15% |
| Error rate | /5 | 15% |
| **Weighted Total** | | /5 |

**Interpretation**:
- 4.5-5.0: Excellent CoR efficiency
- 3.5-4.4: Good, minor improvements possible
- 2.5-3.4: Needs significant optimization
- <2.5: Critical CoR issues

---

## CoR Reduction Checklist

### Immediate Actions

```
[ ] Server response <100ms
[ ] Enable compression (Gzip/Brotli)
[ ] Set proper cache headers
[ ] Remove unused CSS/JS
[ ] Validate HTML markup
```

### Content Actions

```
[ ] Use clear EAV triple structure
[ ] Explicit entity naming (no ambiguous pronouns)
[ ] High information density (no fluff)
[ ] Consistent facts across pages
[ ] Semantic HTML for structure
```

### Architecture Actions

```
[ ] Consolidate duplicate/thin pages
[ ] Implement proper canonicals
[ ] Clean URL structure
[ ] Efficient internal linking
[ ] Remove dead-end pages
```

### Monitoring Actions

```
[ ] Weekly log file analysis
[ ] Monthly GSC review
[ ] Quarterly full audit
[ ] Track indexation trends
```
