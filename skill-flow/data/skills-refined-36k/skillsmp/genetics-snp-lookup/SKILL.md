---
name: genetics-snp-lookup
description: Look up SNP genotypes and interpretations from 23andMe data with online SNPedia validation. Centralized genetics lookup mechanism. Use for: "look up rs12345", "my genotype for rs...", "check SNP", pharmacogenomics genes (CYP2D6, CYP2C19, etc.), or health risk conditions (APOE, Factor V Leiden, etc.).
---

# SNP Lookup with Online Interpretation

**Centralized genetics lookup mechanism** for all genetics-related queries. Provides:
- Individual SNP lookups
- Batch SNP extraction
- Gene-based pharmacogenomics lookups (CYP2D6, CYP2C19, CYP2C9, VKORC1, SLCO1B1, TPMT, DPYD)
- Condition-based health risk lookups (APOE, Factor V Leiden, Hemochromatosis, MTHFR, BRCA)
- Online SNPedia interpretations with caching

## Prerequisites

- Profile must have `genetics_23andme_path` configured
- 23andMe raw data file must exist at the specified path

## Lookup Modes

### Mode 1: Single SNP Lookup
User provides a specific rsID (e.g., "rs429358")

### Mode 2: Batch SNP Lookup
User provides multiple rsIDs (e.g., "rs429358, rs7412")

### Mode 3: Gene-Based Pharmacogenomics Lookup
User asks about a pharmacogenomics gene (e.g., "CYP2D6", "my CYP2C19 status")

**Supported genes**: CYP2D6, CYP2C19, CYP2C9, VKORC1, SLCO1B1, TPMT, DPYD

**Workflow**:
1. Query SNPedia for gene's clinically relevant rsIDs
2. Extract those SNPs from 23andMe data
3. Fetch interpretations from SNPedia
4. Return metabolizer status, affected drugs, dosing guidance

### Mode 4: Condition-Based Health Risk Lookup
User asks about a health condition (e.g., "APOE status", "Factor V Leiden", "hemochromatosis risk")

**Supported conditions**: APOE (Alzheimer's), Factor V Leiden, Hemochromatosis (HFE), MTHFR, BRCA founder mutations

**Workflow**:
1. Query SNPedia for condition's rsIDs
2. Extract those SNPs from 23andMe data
3. Fetch risk interpretations from SNPedia
4. Return risk level, clinical significance, recommendations

## Efficient Data Access

23andMe raw data files contain ~631,000 SNPs. **Always use grep extraction** - never read the full file.

### Single SNP Extraction
```bash
grep "^{rsid}" "{genetics_23andme_path}"
```

### Batch SNP Extraction
```bash
# Extract multiple SNPs in one grep call
grep -E "^(rs429358|rs7412|rs1801133)" "{genetics_23andme_path}"
```

### Parse Extraction Results
```bash
# Extract genotypes into variables
while IFS=$'\t' read -r rsid chr pos genotype; do
  echo "rsID: $rsid, Genotype: $genotype"
done < <(grep -E "^(rs123|rs456)" "{genetics_23andme_path}")
```

### Check File Exists
```bash
test -f "{genetics_23andme_path}" && echo "Found" || echo "Not found"
```

## SNPedia API Integration

### Fetch SNP Interpretation from SNPedia

**API Endpoint**: `https://bots.snpedia.com/api.php`

**Query a single SNP**:
```bash
rsid="rs429358"
curl -A "health-agent/1.0" -s \
  "https://bots.snpedia.com/api.php?action=parse&page=${rsid}&format=json" \
  > "/tmp/claude/${rsid}_snpedia.json"
```

**Parse response**:
```bash
# Extract page HTML from JSON
cat "/tmp/claude/${rsid}_snpedia.json" | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['parse']['text']['*'])" \
  > "/tmp/claude/${rsid}_page.html"

# Extract key information from HTML (simplified parsing)
# Look for genotype tables, clinical significance, and summary text
grep -i "genotype\|significance\|summary" "/tmp/claude/${rsid}_page.html"
```

**Query genotype-specific page** (e.g., rs429358(C;C)):
```bash
genotype="CC"
# Format genotype as (C;C) for SNPedia
formatted=$(echo "$genotype" | sed 's/\(.\)\(.\)/(\1;\2)/')
curl -A "health-agent/1.0" -s \
  "https://bots.snpedia.com/api.php?action=parse&page=${rsid}${formatted}&format=json" \
  > "/tmp/claude/${rsid}_${genotype}_snpedia.json"
```

**Query gene page** (e.g., CYP2D6):
```bash
gene="CYP2D6"
curl -A "health-agent/1.0" -s \
  "https://bots.snpedia.com/api.php?action=parse&page=${gene}&format=json" \
  > "/tmp/claude/${gene}_snpedia.json"
```

### Rate Limiting and Courtesy

- Implement 1-second delay between API requests
- Use `sleep 1` between consecutive `curl` calls
- Respect SNPedia's bandwidth (cache aggressively)
- Set User-Agent header: `health-agent/1.0`

### API Response Format

SNPedia returns JSON with MediaWiki page HTML in `parse.text.*` field:

```json
{
  "parse": {
    "title": "Rs429358",
    "pageid": 1234,
    "text": {
      "*": "<div>...HTML content...</div>"
    }
  }
}
```

## Caching Layer

**Cache directory**: `.claude/skills/health-agent/genetics-snp-lookup/.cache/`

**Cache TTL**: 30 days (2,592,000 seconds)

### Cache File Format

Each rsID gets a JSON cache file: `cache/{rsid}.json`

```json
{
  "rsid": "rs429358",
  "fetched": "2026-01-20T15:30:00Z",
  "ttl_seconds": 2592000,
  "source": "snpedia",
  "data": {
    "summary": "APOE ε4 allele marker",
    "genotypes": {
      "CC": "APOE ε4/ε4 - Highest Alzheimer's risk",
      "CT": "APOE ε3/ε4 or ε2/ε4 - Elevated risk",
      "TT": "APOE ε2/ε3 or ε3/ε3 - Normal/reduced risk"
    },
    "clinical_significance": "Pathogenic for Alzheimer's disease",
    "url": "https://www.snpedia.com/index.php/Rs429358",
    "references": ["PMID:12345678", "PMID:87654321"]
  }
}
```

### Cache Logic

**Before fetching from SNPedia**:
```bash
cache_file=".claude/skills/health-agent/genetics-snp-lookup/.cache/${rsid}.json"

if [ -f "$cache_file" ]; then
  # Check cache age
  fetched=$(cat "$cache_file" | python3 -c "import sys, json; print(json.load(sys.stdin)['fetched'])")
  fetched_ts=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$fetched" "+%s" 2>/dev/null || echo 0)
  current_ts=$(date "+%s")
  age=$((current_ts - fetched_ts))

  if [ "$age" -lt 2592000 ]; then
    # Cache is fresh (< 30 days)
    echo "Using cached data for $rsid (age: $((age/86400)) days)"
    cat "$cache_file"
    exit 0
  else
    echo "Cache stale for $rsid (age: $((age/86400)) days), fetching fresh data..."
  fi
fi
```

**After fetching from SNPedia**:
```bash
# Create cache directory if needed
mkdir -p ".claude/skills/health-agent/genetics-snp-lookup/.cache"

# Save to cache
cat > "$cache_file" << EOF
{
  "rsid": "$rsid",
  "fetched": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "ttl_seconds": 2592000,
  "source": "snpedia",
  "data": {
    ... parsed SNPedia data ...
  }
}
EOF
```

### Cache Fallback

If SNPedia API fails, use stale cache with warning:

```bash
if ! curl_output=$(curl -A "health-agent/1.0" -s -f "https://bots.snpedia.com/..."); then
  if [ -f "$cache_file" ]; then
    echo "⚠️  SNPedia unavailable, using stale cache (age: $((age/86400)) days)"
    cat "$cache_file"
    exit 0
  else
    echo "❌ SNPedia unavailable and no cache available for $rsid"
    exit 1
  fi
fi
```

## 23andMe Raw Data Format

```
# rsid  chromosome  position  genotype
rs12345  1  12345678  AG
rs67890  2  98765432  CC
```

- Tab-separated: rsid, chromosome, position, genotype
- Lines starting with `#` are comments/headers
- Genotype is unphased (AG same as GA)

## Output Formats

### Single SNP with Online Interpretation

```markdown
## SNP Lookup: rs429358

**Genotype**: T;C
**Chromosome**: 19
**Position**: 45411941

### Interpretation (from SNPedia)

**Summary**: APOE ε4 allele marker

**Your Genotype (T;C)**: APOE ε3/ε4 - Elevated Alzheimer's risk (2-3x compared to ε3/ε3)

**Clinical Significance**: Pathogenic for Alzheimer's disease

**References**:
- https://www.snpedia.com/index.php/Rs429358
- PMID:12345678, PMID:87654321

**Last Updated**: 2026-01-15 (cached, age: 5 days)
```

### Batch SNP Lookup

```markdown
## SNP Lookup Results

| rsID | Chromosome | Position | Genotype | Interpretation |
|------|------------|----------|----------|----------------|
| rs429358 | 19 | 45411941 | T;C | APOE ε3/ε4 - Elevated risk |
| rs7412 | 19 | 45412079 | C;C | APOE ε3 allele |
| rs1801133 | 1 | 11856378 | C;T | MTHFR heterozygous (mild) |

### Detailed Interpretations

**rs429358 (T;C)**: APOE ε3/ε4 - Elevated Alzheimer's risk (2-3x compared to ε3/ε3)
**rs7412 (C;C)**: APOE ε3 allele (normal)
**rs1801133 (C;T)**: MTHFR C677T heterozygous - Mildly reduced enzyme activity, typically no clinical significance

**Data Source**: SNPedia (cached, ages: 5-12 days)
```

### Pharmacogenomics Lookup (Gene-Based)

When user asks about "CYP2D6 status" or "my CYP2C19":

```markdown
## Pharmacogenomics: CYP2D6

### Gene Function
CYP2D6 metabolizes ~25% of prescription drugs including antidepressants, antipsychotics, opioids, and beta-blockers.

### Relevant SNPs from 23andMe Data

| rsID | Genotype | Interpretation |
|------|----------|----------------|
| rs3892097 | C;T | *1/*4 - Intermediate metabolizer |
| rs1065852 | C;G | *1/*10 - Reduced activity |
| rs5030655 | -- | Not tested by 23andMe |

### Metabolizer Status
**Intermediate Metabolizer** - Reduced enzyme activity (50-75% of normal)

### Affected Medications
- **Codeine**: Reduced conversion to morphine → less pain relief
- **SSRIs** (fluoxetine, paroxetine): Higher plasma levels → increased side effect risk
- **Tamoxifen**: Reduced activation → potentially reduced efficacy

### Dosing Recommendations
- Standard dosing may be appropriate, but monitor for efficacy and side effects
- Consider alternative medications or therapeutic drug monitoring for critical drugs

**Data Source**: SNPedia (cached)
**References**: https://www.snpedia.com/index.php/CYP2D6
```

### Health Risk Lookup (Condition-Based)

When user asks about "APOE status" or "Factor V Leiden risk":

```markdown
## Health Risk: APOE (Alzheimer's Disease)

### Relevant SNPs

| rsID | Genotype | Allele |
|------|----------|--------|
| rs429358 | T;C | ε3/ε4 |
| rs7412 | C;C | ε3 |

### APOE Genotype
**ε3/ε4** (one ε4 allele, one ε3 allele)

### Alzheimer's Risk
**2-3x increased risk** compared to ε3/ε3 (most common genotype)

- **ε3/ε3 (baseline)**: ~10-15% lifetime risk
- **ε3/ε4 (your genotype)**: ~20-30% lifetime risk
- **ε4/ε4 (highest risk)**: ~50-60% lifetime risk

### Clinical Significance
- APOE ε4 is the strongest genetic risk factor for late-onset Alzheimer's disease
- Having one ε4 allele increases risk, but does NOT guarantee disease development
- Many ε4 carriers never develop Alzheimer's; many non-carriers do develop it
- Lifestyle factors (exercise, diet, cognitive engagement) can modulate risk

### Recommendations
- Discuss with provider if concerned about cognitive decline
- Focus on modifiable risk factors: cardiovascular health, physical activity, cognitive engagement
- Consider more frequent cognitive screening after age 65

**Data Source**: SNPedia (cached)
**References**: https://www.snpedia.com/index.php/APOE
```

### SNP Not Found

```markdown
## SNP Lookup: rs12345

**Result**: Not found in 23andMe data

This SNP may not be tested by 23andMe's genotyping array. 23andMe tests ~631,000 SNPs, but many clinically relevant SNPs are not included.

**Alternative approaches**:
- Check if this SNP is in linkage disequilibrium with a tested SNP
- Consider whole-genome sequencing for comprehensive coverage
```

### SNPedia Unavailable (Fallback to Cache)

```markdown
## SNP Lookup: rs429358

⚠️  **SNPedia API unavailable** - using cached data (age: 45 days, may be stale)

**Genotype**: T;C
**Chromosome**: 19
**Position**: 45411941

[... cached interpretation ...]

**Note**: This interpretation was fetched 45 days ago and may not reflect the latest research. Try again later when SNPedia is available.
```

## Error Handling

| Scenario | Response |
|----------|----------|
| **Genetics path not configured** | Error: "No genetics data configured. Add `genetics_23andme_path` to your profile." |
| **File not found** | Error: "23andMe file not found at {path}. Verify `genetics_23andme_path` in profile." |
| **Invalid rsID format** | Error: "Invalid rsID format: '{input}'. Expected format: rs followed by numbers (e.g., rs429358)" |
| **SNP not in 23andMe data** | Note: "SNP not tested by 23andMe. Consider alternative lookup methods." |
| **SNPedia unavailable (with cache)** | Warning: "SNPedia unavailable, using stale cache (age: X days)" |
| **SNPedia unavailable (no cache)** | Error: "SNPedia unavailable and no cached data for {rsid}. Try again later." |
| **Rate limited by SNPedia** | Wait 60s, retry once, then use cache if available |
| **Cache file corrupted** | Delete cache file, fetch fresh from SNPedia |
| **Network timeout** | Retry with exponential backoff, fall back to cache |
| **API structure change** | Warn user, attempt fallback parsing |

### Network Timeout Handling

Use a 30-second timeout for all SNPedia API requests:

```bash
rsid="rs429358"
cache_file=".claude/skills/health-agent/genetics-snp-lookup/.cache/${rsid}.json"
temp_file="/tmp/claude/${rsid}_snpedia.json"
timeout_seconds=30
max_retries=3

# Retry with exponential backoff
attempt=1
delay=1
while [ $attempt -le $max_retries ]; do
    # Use timeout command (or gtimeout on macOS)
    timeout_cmd="timeout"
    command -v timeout >/dev/null 2>&1 || timeout_cmd="gtimeout"

    if $timeout_cmd $timeout_seconds curl -A "health-agent/1.0" -s -f \
        "https://bots.snpedia.com/api.php?action=parse&page=${rsid}&format=json" \
        > "$temp_file" 2>/dev/null; then
        # Success - validate and use response
        break
    fi

    exit_code=$?
    if [ $exit_code -eq 124 ]; then
        echo "Request timed out after ${timeout_seconds}s (attempt $attempt/$max_retries)" >&2
    else
        echo "Request failed with exit code $exit_code (attempt $attempt/$max_retries)" >&2
    fi

    if [ $attempt -lt $max_retries ]; then
        echo "Retrying in ${delay}s..." >&2
        sleep $delay
        delay=$((delay * 2))
    else
        echo "All attempts failed, checking cache..." >&2
        # Fall back to cache (even if stale)
        if [ -f "$cache_file" ]; then
            echo "⚠️ Using stale cache for $rsid"
            cat "$cache_file"
            exit 0
        else
            echo "❌ No cache available, lookup failed"
            exit 1
        fi
    fi
    attempt=$((attempt + 1))
done
```

### Malformed Cache File Recovery

Before using cached data, validate the JSON structure:

```bash
cache_file=".claude/skills/health-agent/genetics-snp-lookup/.cache/${rsid}.json"

# Validate cache file before use
validate_cache() {
    local file="$1"

    if [ ! -f "$file" ]; then
        return 1  # File doesn't exist
    fi

    # Check file size (corrupt files are often 0 bytes or very small)
    local size=$(wc -c < "$file" 2>/dev/null | tr -d ' ')
    if [ -z "$size" ] || [ "$size" -lt 10 ]; then
        echo "Cache file too small ($size bytes), likely corrupted" >&2
        return 1
    fi

    # Validate JSON structure
    if ! python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
        echo "Cache file contains invalid JSON" >&2
        return 1
    fi

    # Check for expected fields
    local rsid_check=$(python3 -c "import json; d=json.load(open('$file')); print(d.get('rsid', ''))" 2>/dev/null)
    if [ -z "$rsid_check" ]; then
        echo "Cache file missing 'rsid' field" >&2
        return 1
    fi

    return 0
}

# Use in main workflow
if [ -f "$cache_file" ]; then
    if validate_cache "$cache_file"; then
        # Check TTL and use cache...
        echo "Cache valid for $rsid"
    else
        echo "Removing corrupted cache file for $rsid"
        rm -f "$cache_file"
        # Proceed to fetch fresh data
    fi
fi
```

### API Structure Change Detection

SNPedia's API structure may change over time. Detect and handle gracefully:

```bash
# After fetching, validate expected structure
validate_snpedia_response() {
    local response_file="$1"

    # Expected structure: {"parse": {"title": "...", "text": {"*": "..."}}}

    # Check for parse.text.* path (where content lives)
    local content=$(python3 -c "
import json, sys
try:
    d = json.load(open('$response_file'))
    # Try standard path
    if 'parse' in d and 'text' in d['parse'] and '*' in d['parse']['text']:
        print('VALID_STANDARD')
    # Check for error response
    elif 'error' in d:
        print('ERROR:' + d['error'].get('info', 'Unknown error'))
    # Unknown structure
    else:
        print('UNKNOWN_STRUCTURE')
        print(json.dumps(list(d.keys())))
except Exception as e:
    print('PARSE_ERROR:' + str(e))
" 2>/dev/null)

    case "$content" in
        VALID_STANDARD)
            return 0
            ;;
        ERROR:*)
            echo "SNPedia API error: ${content#ERROR:}" >&2
            return 2
            ;;
        UNKNOWN_STRUCTURE*)
            echo "⚠️ WARNING: SNPedia API structure may have changed" >&2
            echo "Expected: parse.text.* path" >&2
            echo "Found keys: ${content#UNKNOWN_STRUCTURE}" >&2
            echo "Attempting fallback parsing..." >&2
            return 3
            ;;
        PARSE_ERROR:*)
            echo "Failed to parse response: ${content#PARSE_ERROR:}" >&2
            return 1
            ;;
    esac
}

# Usage:
if validate_snpedia_response "$temp_file"; then
    # Proceed with standard parsing
    echo "Response structure valid"
elif [ $? -eq 3 ]; then
    # Try fallback parsing for unknown structure
    echo "Attempting to extract data from non-standard response..."
    # Fallback: look for any text content
    python3 -c "
import json
d = json.load(open('$temp_file'))
# Recursively find any HTML content
def find_html(obj, depth=0):
    if depth > 10: return None
    if isinstance(obj, str) and '<' in obj:
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            result = find_html(v, depth+1)
            if result: return result
    if isinstance(obj, list):
        for item in obj:
            result = find_html(item, depth+1)
            if result: return result
    return None

html = find_html(d)
if html:
    print(html[:500] + '...' if len(html) > 500 else html)
else:
    print('NO_HTML_FOUND')
"
fi
```

### Complete Error-Resilient Workflow

```bash
#!/bin/bash
# SNPedia lookup with comprehensive error handling

rsid="$1"
cache_dir=".claude/skills/health-agent/genetics-snp-lookup/.cache"
cache_file="$cache_dir/${rsid}.json"
temp_file="/tmp/claude/${rsid}_snpedia.json"

# Create directories
mkdir -p "$cache_dir" "/tmp/claude"

# Source helper functions if available
[ -f ".claude/skills/health-agent/references/data-access-helpers.sh" ] && \
    source .claude/skills/health-agent/references/data-access-helpers.sh

# 1. Validate input
if ! echo "$rsid" | grep -qE '^rs[0-9]+$'; then
    echo "ERROR: Invalid rsID format: $rsid" >&2
    exit 1
fi

# 2. Check cache (with validation)
if [ -f "$cache_file" ]; then
    if validate_cache "$cache_file" 2>/dev/null; then
        fetched=$(python3 -c "import json; print(json.load(open('$cache_file')).get('fetched', ''))" 2>/dev/null)
        if [ -n "$fetched" ]; then
            fetched_ts=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$fetched" "+%s" 2>/dev/null || echo 0)
            current_ts=$(date "+%s")
            age=$((current_ts - fetched_ts))
            ttl=2592000  # 30 days

            if [ "$age" -lt "$ttl" ]; then
                echo "Using cached data (age: $((age/86400)) days)"
                cat "$cache_file"
                exit 0
            fi
        fi
    else
        echo "Removing invalid cache file"
        rm -f "$cache_file"
    fi
fi

# 3. Fetch with timeout and retry
echo "Fetching $rsid from SNPedia..."
if fetch_json_with_retry \
    "https://bots.snpedia.com/api.php?action=parse&page=${rsid}&format=json" \
    "$temp_file" 30 3 2>/dev/null; then

    # 4. Validate response structure
    if validate_snpedia_response "$temp_file"; then
        # 5. Cache the response
        # [parsing and caching logic here]
        echo "Successfully fetched and cached $rsid"
    else
        echo "Received unexpected response structure"
        # Attempt to use stale cache if available
        if [ -f "$cache_file" ]; then
            echo "Falling back to stale cache"
            cat "$cache_file"
            exit 0
        fi
    fi
else
    echo "Fetch failed after retries"
    # Stale cache fallback
    if [ -f "$cache_file" ]; then
        echo "⚠️ Using stale cache"
        cat "$cache_file"
        exit 0
    fi
    exit 1
fi
```

## Pharmacogenomics Gene Reference

When user asks about these genes, query SNPedia for clinically relevant SNPs:

| Gene | Function | Key Medications |
|------|----------|-----------------|
| **CYP2D6** | Drug metabolism | SSRIs, antipsychotics, opioids, tamoxifen |
| **CYP2C19** | Drug metabolism | Clopidogrel, PPIs, SSRIs |
| **CYP2C9** | Drug metabolism | Warfarin, NSAIDs, phenytoin |
| **VKORC1** | Warfarin sensitivity | Warfarin |
| **SLCO1B1** | Statin metabolism | Simvastatin, atorvastatin |
| **TPMT** | Thiopurine metabolism | Azathioprine, 6-mercaptopurine |
| **DPYD** | Fluoropyrimidine metabolism | 5-fluorouracil, capecitabine |

## Health Risk Conditions Reference

When user asks about these conditions, query SNPedia for relevant SNPs:

| Condition | Genes/SNPs | Clinical Significance |
|-----------|------------|----------------------|
| **APOE (Alzheimer's)** | rs429358, rs7412 | Strongest genetic risk factor for late-onset AD |
| **Factor V Leiden** | rs6025 | Thrombophilia (clotting disorder) |
| **Hemochromatosis** | rs1800562, rs1799945 (HFE) | Iron overload disorder |
| **MTHFR** | rs1801133, rs1801131 | Folate metabolism (controversial clinical significance) |
| **BRCA (limited)** | rs80357906, rs80357914, rs4986852 | Only 3 Ashkenazi founder mutations (23andMe limitation) |

## Notes

- **Strand orientation**: 23andMe reports genotypes on forward strand; literature may use reverse strand (complementary bases: A↔T, C↔G)
- **Unphased genotypes**: AG is same as GA (order doesn't indicate which allele is maternal/paternal)
- **23andMe limitations**: Does not detect insertions, deletions, or copy number variations
- **SNP aliases**: Some SNPs have multiple rsIDs; if primary lookup fails, check SNPedia for aliases
- **BRCA testing**: 23andMe only tests 3 Ashkenazi founder mutations; clinical BRCA testing covers 1000+ variants
- **Interpretation uncertainty**: SNPedia is community-curated; for clinical decisions, confirm with validated genetic testing

## Integration with Other Skills

This skill is the **centralized genetics lookup mechanism**. Other genetics skills delegate to this skill:

- `genetics-pharmacogenomics` → calls this skill for all pharmacogenomics genes
- `genetics-health-risks` → calls this skill for all health risk conditions
- `report-pharmacogenomics` → calls this skill, formats output for provider reports
- `report-genetic-risks` → calls this skill, formats output for provider reports
- `investigate-root-cause` → calls this skill when genetics data is relevant to condition

**Do NOT duplicate** SNP extraction, SNPedia queries, or caching logic in other skills. Always delegate to this skill.
