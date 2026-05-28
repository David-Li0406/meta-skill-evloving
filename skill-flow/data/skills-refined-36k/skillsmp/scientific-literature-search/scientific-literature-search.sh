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
