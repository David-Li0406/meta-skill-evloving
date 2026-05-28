---
name: scientific-literature-search
description: "Query authoritative scientific databases (PubMed, Semantic Scholar) for medical literature. Use when user asks about research on conditions, mechanisms, treatments, or when investigate-root-cause needs scientific evidence for biological mechanisms."
---

# Scientific Literature Search

Query PubMed and Semantic Scholar for authoritative medical and scientific literature to support hypothesis generation, mechanism exploration, and evidence-based analysis.

## Use Cases

Use this skill when:
- User asks: "Find papers on [condition/mechanism]"
- User asks: "What does research say about [topic]?"
- User asks: "Latest therapies for [condition]"
- `investigate-root-cause` needs biological mechanisms (replaces generic WebSearch)
- `mechanism-search` needs authoritative citations
- Hypothesis generation requires scientific backing

## Data Sources

### PubMed (NCBI E-utilities)
- **Coverage**: 36+ million biomedical citations (MEDLINE, life science journals, online books)
- **Authority**: Gold standard for medical literature (NIH/NLM curated)
- **API**: E-utilities (esearch + efetch)
- **Rate Limit**: 3 req/s (10 req/s with API key)
- **Best For**: Clinical research, disease mechanisms, drug trials

### Semantic Scholar
- **Coverage**: 200+ million papers across all sciences
- **Authority**: AI-powered relevance ranking, citation graph analysis
- **API**: Academic Graph API
- **Rate Limit**: 1000 req/s (shared, unauthenticated)
- **Best For**: Comprehensive search, paper discovery, citation networks

## Workflow

### Step 1: Load Environment Variables

Check for NCBI API key (optional but recommended):

```bash
# Check if .env file exists
if [ -f .env ]; then
  source .env
  echo "NCBI API key loaded: ${NCBI_API_KEY:0:8}..."
else
  echo "No .env file found. Using default rate limit (3 req/s)."
  echo "To enable 10 req/s: Create .env file with NCBI_API_KEY (see .env.example)"
fi
```

### Step 2: Parse Query and Generate Search Terms

Extract search query from user input:

```bash
query="$1"  # e.g., "hereditary spherocytosis osmotic fragility sensitivity"

# Sanitize query for URLs
query_encoded=$(echo "$query" | sed 's/ /+/g')

# Generate cache key (SHA256 of query)
cache_key=$(echo -n "$query" | shasum -a 256 | awk '{print $1}')
cache_file=".claude/skills/health-agent/scientific-literature-search/.cache/${cache_key}.json"
```

### Step 3: Check Cache (30-day TTL)

```bash
# Check if cached results exist and are fresh (30 days)
if [ -f "$cache_file" ]; then
  file_age_days=$(( ($(date +%s) - $(stat -f %m "$cache_file")) / 86400 ))

  if [ $file_age_days -lt 30 ]; then
    echo "✅ Cache hit (age: ${file_age_days} days). Using cached results."
    cat "$cache_file"
    exit 0
  else
    echo "⚠️ Cache expired (age: ${file_age_days} days). Fetching fresh results..."
    rm "$cache_file"
  fi
fi

echo "❌ Cache miss. Querying PubMed and Semantic Scholar..."
```

### Step 4: Query PubMed E-utilities

```bash
# Step 4a: Search PubMed for matching articles (esearch)
if [ -n "$NCBI_API_KEY" ]; then
  api_key_param="&api_key=$NCBI_API_KEY"
else
  api_key_param=""
fi

pubmed_search_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${query_encoded}&retmax=10&retmode=json&sort=relevance${api_key_param}"

pubmed_ids=$(curl -s "$pubmed_search_url" | grep -oP '"idlist":\[\K[^\]]+' | tr ',' '\n' | tr -d '"')

if [ -z "$pubmed_ids" ]; then
  echo "No PubMed results found for query: $query"
  pubmed_results="[]"
else
  # Step 4b: Fetch article details (efetch)
  pmids=$(echo "$pubmed_ids" | head -10 | tr '\n' ',' | sed 's/,$//')

  pubmed_fetch_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${pmids}&retmode=json${api_key_param}"

  pubmed_data=$(curl -s "$pubmed_fetch_url")

  # Parse JSON and extract fields (title, authors, year, PMID, DOI)
  pubmed_results=$(echo "$pubmed_data" | jq -r '
    .result
    | to_entries
    | map(select(.key != "uids"))
    | map({
        pmid: .value.uid,
        title: .value.title,
        authors: (.value.authors[:3] | map(.name) | join(", ")),
        year: .value.pubdate[:4],
        doi: (.value.articleids // [] | map(select(.idtype == "doi")) | .[0].value // "N/A"),
        source: "PubMed"
      })
  ')
fi
```

### Step 5: Query Semantic Scholar

```bash
# URL encode query for Semantic Scholar
ss_query_encoded=$(echo "$query" | jq -sRr @uri)

ss_search_url="https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=${ss_query_encoded}&limit=10&fields=title,authors,year,abstract,citationCount,openAccessPdf,externalIds"

ss_data=$(curl -s -H "User-Agent: health-agent/1.0" "$ss_search_url")

# Parse results
ss_results=$(echo "$ss_data" | jq -r '
  .data
  | map({
      title: .title,
      authors: (.authors[:3] | map(.name) | join(", ")),
      year: .year,
      doi: (.externalIds.DOI // "N/A"),
      pmid: (.externalIds.PubMed // "N/A"),
      citation_count: .citationCount,
      abstract: (.abstract[:300] + "..." // "N/A"),
      pdf_url: (.openAccessPdf.url // "N/A"),
      source: "Semantic Scholar"
    })
')

if [ "$ss_results" = "null" ] || [ -z "$ss_results" ]; then
  ss_results="[]"
fi
```

### Step 6: Merge Results and Sort by Relevance

```bash
# Combine PubMed and Semantic Scholar results
combined_results=$(jq -s '.[0] + .[1] | sort_by(-.citation_count // 0)' <(echo "$pubmed_results") <(echo "$ss_results"))

# Add metadata
output=$(jq -n \
  --arg query "$query" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson results "$combined_results" \
  '{
    query: $query,
    fetched_at: $timestamp,
    ttl_days: 30,
    total_results: ($results | length),
    results: $results
  }')

# Save to cache
echo "$output" > "$cache_file"

# Output results
echo "$output"
```

### Step 7: Format Output as Markdown

```bash
# Parse JSON and generate markdown table
echo "## Scientific Literature Search Results"
echo ""
echo "**Query**: $query"
echo "**Total Results**: $(echo "$output" | jq -r '.total_results')"
echo "**Fetched**: $(echo "$output" | jq -r '.fetched_at')"
echo ""
echo "| Title | Authors | Year | Source | PMID/DOI | Citations |"
echo "|-------|---------|------|--------|----------|-----------|"

echo "$output" | jq -r '.results[] | "| \(.title) | \(.authors) | \(.year) | \(.source) | \(if .pmid != "N/A" then "PMID:\(.pmid)" else "DOI:\(.doi)" end) | \(.citation_count // 0) |"'

echo ""
echo "### Abstracts (Top 5 Results)"
echo ""

echo "$output" | jq -r '.results[:5] | .[] | "#### \(.title) (\(.year))\n\n**Authors**: \(.authors)\n**Source**: \(.source)\n**Citations**: \(.citation_count // 0)\n\n**Abstract**: \(.abstract // "N/A")\n\n**DOI**: \(.doi)\n**PMID**: \(.pmid)\n\n---\n"'
```

## Complete Script Template

For convenience, here's a complete bash script that implements the entire workflow:

```bash
#!/bin/bash
# scientific-literature-search.sh - Query PubMed and Semantic Scholar

query="$1"

if [ -z "$query" ]; then
  echo "Usage: scientific-literature-search.sh <query>"
  echo "Example: scientific-literature-search.sh 'hereditary spherocytosis osmotic fragility'"
  exit 1
fi

# Load NCBI API key if available
if [ -f .env ]; then
  source .env
fi

# Generate cache key
cache_key=$(echo -n "$query" | shasum -a 256 | awk '{print $1}')
cache_file=".claude/skills/health-agent/scientific-literature-search/.cache/${cache_key}.json"

# Check cache (30-day TTL)
if [ -f "$cache_file" ]; then
  file_age_days=$(( ($(date +%s) - $(stat -f %m "$cache_file")) / 86400 ))

  if [ $file_age_days -lt 30 ]; then
    # Format cached results as markdown
    cached_data=$(cat "$cache_file")
    echo "## Scientific Literature Search Results (Cached)"
    echo ""
    echo "**Query**: $(echo "$cached_data" | jq -r '.query')"
    echo "**Total Results**: $(echo "$cached_data" | jq -r '.total_results')"
    echo "**Fetched**: $(echo "$cached_data" | jq -r '.fetched_at') (cached, age: ${file_age_days} days)"
    echo ""
    echo "| Title | Authors | Year | Source | PMID/DOI | Citations |"
    echo "|-------|---------|------|--------|----------|-----------|"
    echo "$cached_data" | jq -r '.results[] | "| \(.title) | \(.authors) | \(.year) | \(.source) | \(if .pmid != "N/A" then "PMID:\(.pmid)" else "DOI:\(.doi)" end) | \(.citation_count // 0) |"'
    echo ""
    echo "### Abstracts (Top 5 Results)"
    echo ""
    echo "$cached_data" | jq -r '.results[:5] | .[] | "#### \(.title) (\(.year))\n\n**Authors**: \(.authors)\n**Source**: \(.source)\n**Citations**: \(.citation_count // 0)\n\n**Abstract**: \(.abstract // "N/A")\n\n**DOI**: \(.doi)\n**PMID**: \(.pmid)\n\n---\n"'
    exit 0
  fi
fi

# Query PubMed
echo "Querying PubMed..." >&2

query_encoded=$(echo "$query" | sed 's/ /+/g')
api_key_param=""
[ -n "$NCBI_API_KEY" ] && api_key_param="&api_key=$NCBI_API_KEY"

pubmed_search_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${query_encoded}&retmax=10&retmode=json&sort=relevance${api_key_param}"
pubmed_ids=$(curl -s "$pubmed_search_url" | grep -oP '"idlist":\[\K[^\]]+' | tr ',' '\n' | tr -d '"')

if [ -z "$pubmed_ids" ]; then
  pubmed_results="[]"
else
  pmids=$(echo "$pubmed_ids" | head -10 | tr '\n' ',' | sed 's/,$//')
  pubmed_fetch_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${pmids}&retmode=json${api_key_param}"
  pubmed_data=$(curl -s "$pubmed_fetch_url")

  pubmed_results=$(echo "$pubmed_data" | jq -r '
    .result
    | to_entries
    | map(select(.key != "uids"))
    | map({
        pmid: .value.uid,
        title: .value.title,
        authors: (.value.authors[:3] | map(.name) | join(", ")),
        year: (.value.pubdate[:4] // "N/A"),
        doi: (.value.articleids // [] | map(select(.idtype == "doi")) | .[0].value // "N/A"),
        citation_count: 0,
        abstract: "N/A",
        source: "PubMed"
      })
  ')
fi

# Query Semantic Scholar
echo "Querying Semantic Scholar..." >&2

ss_query_encoded=$(echo "$query" | jq -sRr @uri)
ss_search_url="https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=${ss_query_encoded}&limit=10&fields=title,authors,year,abstract,citationCount,openAccessPdf,externalIds"
ss_data=$(curl -s -H "User-Agent: health-agent/1.0" "$ss_search_url")

ss_results=$(echo "$ss_data" | jq -r '
  .data
  | map({
      title: .title,
      authors: (.authors[:3] | map(.name) | join(", ")),
      year: (.year // "N/A"),
      doi: (.externalIds.DOI // "N/A"),
      pmid: (.externalIds.PubMed // "N/A"),
      citation_count: (.citationCount // 0),
      abstract: (if .abstract then (.abstract[:300] + "...") else "N/A" end),
      pdf_url: (.openAccessPdf.url // "N/A"),
      source: "Semantic Scholar"
    })
' || echo "[]")

# Merge and sort by citation count
combined_results=$(jq -s '.[0] + .[1] | sort_by(-.citation_count // 0)' <(echo "$pubmed_results") <(echo "$ss_results"))

# Create output JSON
output=$(jq -n \
  --arg query "$query" \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson results "$combined_results" \
  '{
    query: $query,
    fetched_at: $timestamp,
    ttl_days: 30,
    total_results: ($results | length),
    results: $results
  }')

# Save to cache
mkdir -p "$(dirname "$cache_file")"
echo "$output" > "$cache_file"

# Format as markdown
echo "## Scientific Literature Search Results"
echo ""
echo "**Query**: $query"
echo "**Total Results**: $(echo "$output" | jq -r '.total_results')"
echo "**Fetched**: $(echo "$output" | jq -r '.fetched_at')"
echo ""
echo "| Title | Authors | Year | Source | PMID/DOI | Citations |"
echo "|-------|---------|------|--------|----------|-----------|"
echo "$output" | jq -r '.results[] | "| \(.title) | \(.authors) | \(.year) | \(.source) | \(if .pmid != "N/A" then "PMID:\(.pmid)" else "DOI:\(.doi)" end) | \(.citation_count // 0) |"'
echo ""
echo "### Abstracts (Top 5 Results)"
echo ""
echo "$output" | jq -r '.results[:5] | .[] | "#### \(.title) (\(.year))\n\n**Authors**: \(.authors)\n**Source**: \(.source)\n**Citations**: \(.citation_count // 0)\n\n**Abstract**: \(.abstract // "N/A")\n\n**DOI**: \(.doi)\n**PMID**: \(.pmid)\n\n---\n"'
```

## Usage

### Direct Invocation

When user asks for scientific literature:

```bash
# Save the complete script to a temporary file
cat > /tmp/scientific-literature-search.sh << 'SCRIPT_EOF'
[Complete script template from above]
SCRIPT_EOF

chmod +x /tmp/scientific-literature-search.sh

# Run with query
/tmp/scientific-literature-search.sh "hereditary spherocytosis osmotic fragility sensitivity"
```

### From investigate-root-cause

When `investigate-root-cause` needs biological mechanisms:

```bash
# In Phase 2 (Hypothesis Generation), replace generic WebSearch with:
/tmp/scientific-literature-search.sh "chronic hemolysis bilirubin mechanism"

# Extract PMIDs for citation
grep "PMID:" output | awk -F: '{print $2}' | tr -d ' '
```

## Output Format

### Markdown Table

Top-level summary of all results (PubMed + Semantic Scholar combined):

```markdown
## Scientific Literature Search Results

**Query**: hereditary spherocytosis osmotic fragility sensitivity
**Total Results**: 18
**Fetched**: 2026-01-21T12:00:00Z

| Title | Authors | Year | Source | PMID/DOI | Citations |
|-------|---------|------|--------|----------|-----------|
| Osmotic fragility test in hereditary spherocytosis | Smith J, Doe A, Brown K | 2020 | PubMed | PMID:12345678 | 45 |
| Novel diagnostic approaches for HS | Johnson M, Lee S, Wang T | 2019 | Semantic Scholar | DOI:10.1234/example | 32 |
...
```

### Abstracts (Top 5)

Detailed abstracts for the top 5 most-cited results:

```markdown
### Abstracts (Top 5 Results)

#### Osmotic fragility test in hereditary spherocytosis (2020)

**Authors**: Smith J, Doe A, Brown K
**Source**: PubMed
**Citations**: 45

**Abstract**: The osmotic fragility test remains a cornerstone diagnostic tool for hereditary spherocytosis. This study evaluates sensitivity and specificity across 500 patients...

**DOI**: 10.1234/example
**PMID**: 12345678

---
```

## Caching

### Cache Structure

```
.claude/skills/health-agent/scientific-literature-search/.cache/
├── a1b2c3d4e5f6.json  # SHA256 hash of query 1
├── f6e5d4c3b2a1.json  # SHA256 hash of query 2
└── ...
```

### Cache File Format

```json
{
  "query": "hereditary spherocytosis osmotic fragility",
  "fetched_at": "2026-01-21T12:00:00Z",
  "ttl_days": 30,
  "total_results": 18,
  "results": [
    {
      "pmid": "12345678",
      "title": "Osmotic fragility test in HS",
      "authors": "Smith J, Doe A, Brown K",
      "year": "2020",
      "doi": "10.1234/example",
      "citation_count": 45,
      "abstract": "The osmotic fragility test...",
      "source": "PubMed"
    }
  ]
}
```

### Cache Expiration

- **TTL**: 30 days
- **Check**: On each query, compare file modification time to current time
- **Action**: If age > 30 days, delete cache file and fetch fresh results
- **Benefit**: Balances freshness with API rate limits and performance

## API Rate Limits

### PubMed E-utilities

**Without API key**: 3 requests/second
**With API key**: 10 requests/second

**To get API key**:
1. Register at https://www.ncbi.nlm.nih.gov/account/
2. Generate key in "API Key Management"
3. Add to `.env`: `NCBI_API_KEY=your_key_here`

### Semantic Scholar

**Unauthenticated**: 1000 requests/second (shared pool)
**With API key**: Higher limits (register at https://www.semanticscholar.org/product/api)

**Current implementation**: Uses unauthenticated API (sufficient for most use cases)

## Error Handling

### No Results Found

```bash
if [ "$total_results" -eq 0 ]; then
  echo "⚠️ No results found for query: $query"
  echo ""
  echo "**Suggestions**:"
  echo "- Simplify query (remove overly specific terms)"
  echo "- Try synonyms or alternative phrasing"
  echo "- Check for typos"
  exit 0
fi
```

### API Failures

```bash
# Check if API response is valid JSON
if ! echo "$pubmed_data" | jq empty 2>/dev/null; then
  echo "❌ PubMed API error. Using Semantic Scholar results only."
  pubmed_results="[]"
fi

if ! echo "$ss_data" | jq empty 2>/dev/null; then
  echo "❌ Semantic Scholar API error. Using PubMed results only."
  ss_results="[]"
fi
```

### Rate Limit Exceeded

```bash
# PubMed returns HTTP 429 when rate limit exceeded
# Add exponential backoff:
if echo "$pubmed_data" | grep -q "429"; then
  echo "⚠️ PubMed rate limit exceeded. Waiting 2 seconds..."
  sleep 2
  # Retry once
  pubmed_data=$(curl -s "$pubmed_fetch_url")
fi
```

## Example Invocations

### User Request

**User**: "Find papers on hereditary spherocytosis diagnosis sensitivity"

**Assistant**:
```bash
/tmp/scientific-literature-search.sh "hereditary spherocytosis diagnosis sensitivity"
```

**Output**: Markdown table with 15-20 papers from PubMed and Semantic Scholar

---

### From investigate-root-cause

**Context**: Investigating chronic high bilirubin, need biological mechanism for hemolysis hypothesis

**Agent action**:
```bash
/tmp/scientific-literature-search.sh "chronic hemolysis bilirubin unconjugated mechanism"
```

**Usage**: Extract PMIDs from results, cite in hypothesis section:
- "Hemolysis increases unconjugated bilirubin production (PMID:12345678)"

---

### Pharmacogenomics Research

**User**: "What does research say about CYP2D6 poor metabolizers and antidepressants?"

**Assistant**:
```bash
/tmp/scientific-literature-search.sh "CYP2D6 poor metabolizer antidepressants adverse effects"
```

**Output**: Papers on drug metabolism, dosing recommendations, adverse event rates

## Integration with Other Skills

### mechanism-search

`mechanism-search` can use this skill to find authoritative biological pathways:

```bash
# Instead of generic WebSearch:
scientific-literature-search.sh "mechanism pathway $condition $observation"
```

### investigate-root-cause

In Phase 2 (Hypothesis Generation), use for biological mechanisms:

```bash
# For each hypothesis, query scientific literature:
for hypothesis in "${hypotheses[@]}"; do
  scientific-literature-search.sh "$hypothesis mechanism pathway"
done
```

### Evidence citation in reports

Include PMIDs in hypothesis sections:

```markdown
**Supporting Evidence**:
1. ✅ Hemolysis increases unconjugated bilirubin (PMID:12345678)
2. ✅ Spherocytosis causes chronic hemolysis (PMID:87654321)
```

## Maintenance

### Cache Management

Caches accumulate over time. Periodically clean old entries:

```bash
# Delete cache entries older than 60 days
find .claude/skills/health-agent/scientific-literature-search/.cache/ -type f -mtime +60 -delete
```

### API Key Rotation

NCBI API keys don't expire, but can be regenerated if compromised:

1. Log into NCBI account
2. Regenerate API key
3. Update `.env` file
4. No code changes needed

## Medical Disclaimer

This skill queries scientific literature databases for research purposes. **It is not medical advice**:
- Papers may have conflicting results
- Research findings require clinical context
- Always consult healthcare providers for medical decisions
- Use citations to validate hypotheses, not as diagnostic criteria
