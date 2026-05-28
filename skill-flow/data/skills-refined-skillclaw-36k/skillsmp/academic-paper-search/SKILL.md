---
name: academic-paper-search
description: Search academic literature on the web (Google Scholar, arXiv, Semantic Scholar, IEEE Xplore, etc.), extract abstracts/metadata, rank by relevance (0-100), and optionally download PDFs to papers/ folder. Use when asked to find papers, search literature, discover related work, update bibliography, or when user mentions "recent work on [topic]", "papers from [venue]", or requests literature review assistance.
---

# Academic Paper Search

Search academic databases, retrieve abstracts and metadata, rank by relevance, and download PDFs for literature review integration.

## Workflow

### 1. Build Context Profile

Extract keywords from user's project to guide search and relevance scoring.

**Sources to check**:
- LaTeX files (`project/**/*.tex`) for technical terms, methods, research gaps
- Existing bibliography (`references.bib`) for cited authors/papers
- Markdown notes (`references-new/`, `*.md`)
- Uploaded PDFs in `papers/`
- User-provided keywords

**Extract**: technical terms, domain keywords, acronyms, research questions, evaluation metrics

Example context:
```
Domain: recommender systems, collaborative filtering
Methods: deep learning, neural networks
Gap: interpretability
Time: recent (2020-2025)
```

### 2. Search Academic Sources

Use `fetch_webpage` to search multiple databases in parallel:

**Primary sources**:
- **Google Scholar**: `scholar.google.com/scholar?q={query}&as_ylo={year}` - broad coverage, citation counts
- **arXiv**: `arxiv.org/search/?query={query}&order=-submitted_date` - full abstracts, open access PDFs
- **Semantic Scholar**: `semanticscholar.org/search?q={query}` - citation metrics, influence scores
- **IEEE Xplore**: `ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}` - engineering/CS focus

**Fetch pattern**:
```
fetch_webpage(
  urls=["https://scholar.google.com/...", "https://arxiv.org/...", ...],
  query="Extract title, authors, year, abstract, venue, citations, DOI/PDF links for {keywords}"
)
```

Include time filters (e.g., `&as_ylo=2020`) for recent work requests.

### 3. Extract & Structure Results

Format each paper:
```markdown
### [Paper Title](DOI_URL)
**Authors**: First Author, et al.  
**Venue**: Conference/Journal, Year  
**Citations**: [count]  
**Relevance**: [score/100] ⭐⭐⭐⭐⭐

**Abstract**: [full text or snippet + "Partial abstract"]

**PDF**: [link] or "Institutional access required"
```

### 4. Rank by Relevance (0-100 Scale)

**Scoring dimensions**:
1. **Keyword Match (30pts)**: Primary in title (+15 each), primary in abstract (+5), secondary (+2)
2. **Conceptual Alignment (25pts)**: Same research gap (+15), methodology (+10), domain (+10)
3. **Recency (15pts)**: 2024-25 (+15), 2022-23 (+12), 2020-21 (+8), older decreases
4. **Citation Impact (15pts)**: >100 cites (+15), 50-100 (+12), 20-49 (+8), 10-19 (+5)
5. **Venue Quality (10pts)**: A* venue (+10), A (+8), B (+5), workshop (+3)
6. **Context Fit (5pts)**: Cites user's papers (+5), author overlap (+3), same dataset (+4)

Sort descending; show top 10 with score breakdown for highly relevant papers (>80).

### 5. Download PDFs (On Request)

When user asks "download PDFs" or "extract papers to papers/":

Create `tools/download_papers.py`:
```python
import requests, os
from pathlib import Path

def download_pdf(url, filename, dest="papers"):
    Path(dest).mkdir(exist_ok=True)
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        if r.status_code == 200 and 'pdf' in r.headers.get('Content-Type', ''):
            with open(f"{dest}/{filename}", 'wb') as f: f.write(r.content)
            return True, f"{dest}/{filename}"
        return False, f"Status {r.status_code}"
    except Exception as e: return False, str(e)

# Add paper URLs and run
papers = [("https://arxiv.org/pdf/2301.12345.pdf", "smith2023.pdf")]
for url, name in papers:
    ok, msg = download_pdf(url, name)
    print(f"{'✓' if ok else '✗'} {name}: {msg}")
```

Run via `run_in_terminal`. Handle errors: 403/401 = institutional access, 404 = broken link.

After downloads, suggest: `python tools/extract_papers.py` and `python tools/review_papers.py`.

## Output Example

```markdown
## Literature Search: "Explainable Recommender Systems"

**Context**: project/capitulo2 — collaborative filtering, deep learning, interpretability gap  
**Query**: explainable recommender systems deep learning 2020-2025  
**Sources**: Google Scholar, arXiv, Semantic Scholar, IEEE

---

### 🥇 [Attention-Based Explanations for Collaborative Filtering](https://doi.org/10.1145/3383313.3412345)
**Relevance: 92/100** ⭐⭐⭐⭐⭐  
**Authors**: Silva, Smith, Costa  
**Venue**: RecSys 2023  
**Citations**: 47  
**PDF**: [arXiv](https://arxiv.org/pdf/2301.12345.pdf)

**Abstract**: Attention-based neural CF model with post-hoc explanations using multi-head attention. NDCG@10 +4.2% over baseline, 78% explanation quality. Addresses interpretability gap in deep learning recommenders...

**Score breakdown**: Keyword 28/30, Alignment 25/25, Recency 15/15, Citations 9/15, Venue 10/10, Fit 5/5

---

[... 4-9 more papers ...]

---

**Summary**: 23 found (showing top 10), avg 68/100, 5 highly relevant (>80), 3 public PDFs

**Next steps**:
1. Download PDFs?
2. Add to references.bib?
3. Draft Chapter 3 table?
```

## Integration

- **Bibliography**: Invoke `bibtex-reference-management` to add entries
- **PDF extraction**: Run `tools/extract_papers.py` and `tools/review_papers.py` after downloads
- **TCC Chapter 3**: Generate comparative table with `\ticV`/`\ticX` markers

## Common Requests

- **"Find papers on [topic]"**: Extract context, search 3-4 sources, return top 10
- **"Recent work"**: Filter last 2-3 years, prioritize arXiv/preprints
- **"Papers from [venue]"**: Add venue-specific search, use IEEE Xplore/ACM DL
- **"Download top 5"**: Create script, filter public PDFs, report success/failures
- **"Papers like [uploaded_pdf]"**: Extract with `extract_papers.py`, boost alignment weight

## Error Handling

- **No results**: Suggest broader keywords, alternative terms, extended time range
- **Source unavailable**: Continue with other sources, note which failed
- **Paywalled PDFs**: Provide DOI, suggest institutional access or preprints
- **Limited context**: Request research focus/methods/domain or proceed with keywords only
