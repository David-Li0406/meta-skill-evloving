---
name: genetics-selfdecode-lookup
description: Look up SNP genotypes from SelfDecode (imputed genetics data). Requires JWT token from browser. Use for expanded SNP coverage beyond 23andMe raw data. Triggers on "check selfdecode for rs...", "selfdecode lookup", "imputed genotype for...", or when SNP not found in 23andMe data.
---

# SelfDecode SNP Lookup

**Authenticated genetics lookup** for SelfDecode's imputed SNP data. SelfDecode provides:
- **Imputed SNPs**: More coverage than raw 23andMe data (~20M+ vs 631k SNPs)
- **Direct API**: Clean JSON responses with genotype data

## Prerequisites

- SelfDecode account with uploaded genetic data
- JWT token copied from browser (see "Getting Your JWT Token" below)
- Profile ID from SelfDecode (see "Getting Your Profile ID" below)

## Configuration

### Profile Setup

Add to your profile YAML:

```yaml
data_sources:
  # Existing genetics source
  genetics_23andme_path: "/path/to/23andme_raw_data.txt"

  # SelfDecode API credentials
  selfdecode:
    enabled: true
    profile_id: "your-profile-uuid"  # From URL: ?profile_id=xxx
    jwt_token: "eyJhbGciOiJSUzI1NiIs..."  # From authorization header (without "JWT " prefix)
```

### Getting Your Credentials

1. Log in to SelfDecode in your browser
2. Open Developer Tools (F12) → Network tab → filter by "genotype"
3. Navigate to any SNP page (e.g., https://selfdecode.com/app/snp/rs429358)
4. Find request to: `/service/health-analysis/genes/genotype/?...`
5. From the **Request URL**, copy the `profile_id` parameter value
6. From **Request Headers**, copy the `authorization` value (just the `eyJ...` part, without the `JWT ` prefix)

**Token lifetime**: JWT tokens expire after ~48 hours. Refresh when you get auth errors.

### Getting Your Profile ID

1. In the same Network request, look at the URL
2. Copy the `profile_id` parameter value (UUID format like `edbd7967-4c2f-45f3-95cf-4c45879d77a4`)
3. Add to your profile YAML

## API Reference

### Endpoint

```
GET https://selfdecode.com/service/health-analysis/genes/genotype/
```

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `profile_id` | Your SelfDecode profile UUID |
| `rsid` | SNP identifier (e.g., `rs429358`) or comma-separated list |

### Required Headers

| Header | Value |
|--------|-------|
| `authorization` | `JWT {token}` |

## Lookup Workflow

### Single SNP Lookup

```bash
# Set variables from profile (read from profiles/{name}.yaml)
profile_name="{profile name from profiles/{name}.yaml}"
profile_id="{from profile: selfdecode.profile_id}"
jwt_token="{from profile: selfdecode.jwt_token}"
rsid="rs429358"
cache_dir=".claude/skills/health-agent/genetics-selfdecode-lookup/.cache/${profile_name}"

# 1. Check cache first
cache_file="${cache_dir}/${rsid}.json"
if [ -f "$cache_file" ]; then
  # Check cache age (30-day TTL = 2592000 seconds)
  fetched=$(python3 -c "import json; print(json.load(open('$cache_file')).get('fetched', ''))" 2>/dev/null)
  if [ -n "$fetched" ]; then
    fetched_ts=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$fetched" "+%s" 2>/dev/null || echo 0)
    current_ts=$(date "+%s")
    age=$((current_ts - fetched_ts))

    if [ "$age" -lt 2592000 ]; then
      echo "Using cached SelfDecode data for $rsid (age: $((age/86400)) days)"
      cat "$cache_file"
      exit 0
    fi
  fi
fi

# 2. Query SelfDecode API
response=$(curl -s "https://selfdecode.com/service/health-analysis/genes/genotype/?profile_id=${profile_id}&rsid=${rsid}" \
  -H "authorization: JWT ${jwt_token}")

# 3. Check for authentication errors (requires user intervention)
if echo "$response" | grep -qE '"detail".*([Aa]uthentication|credentials|signature)'; then
  echo "AUTH_ERROR: JWT token expired or invalid"
  echo "Response: $response"
  echo ""
  echo "ACTION REQUIRED: Prompt user to update JWT token, wait for confirmation, then retry"
  exit 2  # Exit code 2 = auth error
fi

# 4. Check for other errors
if echo "$response" | grep -q '"detail"'; then
  echo "Error: $response"
  exit 1
fi

# 5. Parse and cache response
mkdir -p "$cache_dir"
genotypes=$(echo "$response" | python3 -c "import sys, json; r=json.load(sys.stdin); print(r[0]['genotypes'][0] + r[0]['genotypes'][1] if r else '')")

cat > "$cache_file" << EOF
{
  "rsid": "$rsid",
  "fetched": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "ttl_seconds": 2592000,
  "source": "selfdecode",
  "data": {
    "genotype": "$genotypes",
    "raw_response": $response
  }
}
EOF

echo "Cached SelfDecode data for $rsid: $genotypes"
cat "$cache_file"
```

### Batch SNP Lookup

SelfDecode supports comma-separated rsids for efficient batch queries:

```bash
# Batch query - up to ~50 SNPs per request
rsids="rs429358,rs7412,rs1801133"

response=$(curl -s "https://selfdecode.com/service/health-analysis/genes/genotype/?profile_id=${profile_id}&rsid=${rsids}" \
  -H "authorization: JWT ${jwt_token}")

# Returns array of results:
# [
#   {"profile_id":"...","rsid":"rs429358","variant_ids":["ref","ref"],"genotypes":["T","T"]},
#   {"profile_id":"...","rsid":"rs7412","variant_ids":["ref","ref"],"genotypes":["C","C"]},
#   ...
# ]
```

## Response Format

### Success Response

```json
[{
  "profile_id": "edbd7967-4c2f-45f3-95cf-4c45879d77a4",
  "rsid": "rs429358",
  "variant_ids": ["ref", "ref"],
  "genotypes": ["T", "T"]
}]
```

| Field | Description |
|-------|-------------|
| `profile_id` | Your SelfDecode profile UUID |
| `rsid` | The queried SNP |
| `variant_ids` | Allele types (`ref` = reference, or variant ID) |
| `genotypes` | The two alleles (diploid) |

### Error Responses

| Error | Meaning |
|-------|---------|
| `{"detail":"Incorrect authentication credentials."}` | JWT expired or invalid |
| `{"profile_id":"This field is required."}` | Missing profile_id parameter |
| `[]` | SNP not found in SelfDecode database |

## Caching Layer

**Cache directory**: `.claude/skills/health-agent/genetics-selfdecode-lookup/.cache/{profile_name}/`

**Cache TTL**: 30 days (2,592,000 seconds)

**Profile partitioning**: Cache is partitioned by profile name to prevent data leakage between profiles. Each profile's genotype data is stored in its own subdirectory.

### Cache File Format

Each rsID gets a JSON cache file: `.cache/{profile_name}/{rsid}.json`

```json
{
  "rsid": "rs429358",
  "fetched": "2026-01-22T17:00:00Z",
  "ttl_seconds": 2592000,
  "source": "selfdecode",
  "data": {
    "genotype": "TT",
    "raw_response": [{"profile_id":"...","rsid":"rs429358","variant_ids":["ref","ref"],"genotypes":["T","T"]}]
  }
}
```

## Output Format

### Single SNP Result

```markdown
## SelfDecode SNP Lookup: rs429358

**Source**: SelfDecode (imputed)
**Genotype**: T/T
**Variant IDs**: ref/ref (homozygous reference)

**Data Retrieved**: 2026-01-22 (fresh)
```

### Batch Result

```markdown
## SelfDecode Batch Lookup

| rsID | Genotype | Variant IDs |
|------|----------|-------------|
| rs429358 | T/T | ref/ref |
| rs7412 | C/C | ref/ref |
| rs1801133 | C/T | ref/alt |

**Data Retrieved**: 2026-01-22
```

## Error Handling

| Scenario | Response |
|----------|----------|
| **JWT not set** | Error: "jwt_token not configured in profile. Copy from browser." |
| **JWT expired** | Prompt user to update token (see Authentication Error Recovery below) |
| **Profile ID missing** | Error: "profile_id not configured in profile YAML" |
| **SNP not found** | Note: "SNP {rsid} not in SelfDecode database (empty response)" |
| **API unavailable (with cache)** | Warning: "SelfDecode unavailable, using stale cache (age: X days)" |
| **Network timeout** | Retry with exponential backoff, fall back to cache |
| **Cache file corrupted** | Delete and re-fetch |
| **API structure change** | Detect and warn, attempt fallback parsing |

### Network Timeout Handling

Use 30-second timeout with retry for SelfDecode API requests:

```bash
profile_id="{from profile}"
jwt_token="{from profile}"
rsid="rs429358"
cache_file=".claude/skills/health-agent/genetics-selfdecode-lookup/.cache/${profile_name}/${rsid}.json"
temp_file="/tmp/claude/selfdecode_${rsid}.json"
timeout_seconds=30
max_retries=3

attempt=1
delay=2  # Start with 2 second delay (SelfDecode is slower)
while [ $attempt -le $max_retries ]; do
    # Use timeout command
    timeout_cmd="timeout"
    command -v timeout >/dev/null 2>&1 || timeout_cmd="gtimeout"

    if $timeout_cmd $timeout_seconds curl -s -f \
        "https://selfdecode.com/service/health-analysis/genes/genotype/?profile_id=${profile_id}&rsid=${rsid}" \
        -H "authorization: JWT ${jwt_token}" \
        > "$temp_file" 2>/dev/null; then

        # Check for auth error in response (still 200 status)
        if grep -qE '"detail".*[Aa]uthentication' "$temp_file"; then
            echo "AUTH_ERROR: JWT token expired" >&2
            exit 2
        fi

        # Success
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
        echo "All attempts failed" >&2
        # Fall back to cache
        if [ -f "$cache_file" ]; then
            echo "⚠️ Using stale cache for $rsid"
            cat "$cache_file"
            exit 0
        else
            echo "❌ No cache available"
            exit 1
        fi
    fi
    attempt=$((attempt + 1))
done
```

### Malformed Cache File Recovery

Validate cache before use:

```bash
validate_selfdecode_cache() {
    local file="$1"

    if [ ! -f "$file" ]; then
        return 1
    fi

    # Check file size
    local size=$(wc -c < "$file" 2>/dev/null | tr -d ' ')
    if [ -z "$size" ] || [ "$size" -lt 20 ]; then
        echo "Cache file too small ($size bytes)" >&2
        return 1
    fi

    # Validate JSON
    if ! python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
        echo "Cache file contains invalid JSON" >&2
        return 1
    fi

    # Check for expected fields
    local has_rsid=$(python3 -c "
import json
d = json.load(open('$file'))
print('yes' if d.get('rsid') and d.get('data', {}).get('genotype') else 'no')
" 2>/dev/null)

    if [ "$has_rsid" != "yes" ]; then
        echo "Cache file missing required fields" >&2
        return 1
    fi

    return 0
}

# Usage
if [ -f "$cache_file" ]; then
    if validate_selfdecode_cache "$cache_file"; then
        # Check TTL and use
        echo "Cache valid"
    else
        echo "Removing corrupted cache for $rsid"
        rm -f "$cache_file"
    fi
fi
```

### API Structure Change Detection

SelfDecode API may change. Detect and handle:

```bash
validate_selfdecode_response() {
    local response_file="$1"

    # Expected: [{"profile_id":"...","rsid":"...","variant_ids":[...],"genotypes":[...]}]

    local validation=$(python3 -c "
import json, sys
try:
    d = json.load(open('$response_file'))

    # Empty array = SNP not found
    if isinstance(d, list) and len(d) == 0:
        print('NOT_FOUND')
        sys.exit(0)

    # Check for expected structure
    if isinstance(d, list) and len(d) > 0:
        item = d[0]
        if 'rsid' in item and 'genotypes' in item:
            print('VALID')
        elif 'detail' in item:
            print('ERROR:' + str(item.get('detail', 'Unknown')))
        else:
            print('UNKNOWN:' + ','.join(item.keys()))
    elif isinstance(d, dict):
        if 'detail' in d:
            print('ERROR:' + str(d.get('detail', 'Unknown')))
        else:
            print('UNKNOWN_DICT:' + ','.join(d.keys()))
    else:
        print('UNEXPECTED_TYPE:' + type(d).__name__)

except json.JSONDecodeError as e:
    print('JSON_ERROR:' + str(e))
except Exception as e:
    print('ERROR:' + str(e))
" 2>/dev/null)

    case "$validation" in
        VALID)
            return 0
            ;;
        NOT_FOUND)
            echo "SNP not found in SelfDecode database"
            return 2
            ;;
        ERROR:*Authentication*|ERROR:*credentials*)
            echo "Authentication error: ${validation#ERROR:}" >&2
            return 3
            ;;
        ERROR:*)
            echo "API error: ${validation#ERROR:}" >&2
            return 1
            ;;
        UNKNOWN:*|UNKNOWN_DICT:*)
            echo "⚠️ WARNING: SelfDecode API structure may have changed" >&2
            echo "Expected fields: rsid, genotypes" >&2
            echo "Found: ${validation#UNKNOWN:}" >&2
            return 4
            ;;
        JSON_ERROR:*)
            echo "Invalid JSON response: ${validation#JSON_ERROR:}" >&2
            return 1
            ;;
        *)
            echo "Unexpected validation result: $validation" >&2
            return 1
            ;;
    esac
}

# Usage
case $(validate_selfdecode_response "$temp_file"; echo $?) in
    0)
        echo "Valid response, proceeding to cache"
        ;;
    2)
        echo "SNP not in database"
        exit 0
        ;;
    3)
        echo "AUTH_ERROR - prompt user to refresh token"
        exit 2
        ;;
    4)
        echo "API changed - attempting fallback parsing"
        # Try to extract genotype from any structure
        genotype=$(python3 -c "
import json
d = json.load(open('$temp_file'))
# Recursively search for anything that looks like a genotype
def find_genotype(obj, depth=0):
    if depth > 5: return None
    if isinstance(obj, list) and len(obj) == 2 and all(isinstance(x, str) and len(x) == 1 for x in obj):
        return ''.join(obj)
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('genotype', 'genotypes', 'alleles'):
                if isinstance(v, str): return v
                if isinstance(v, list): return find_genotype(v)
            result = find_genotype(v, depth+1)
            if result: return result
    if isinstance(obj, list):
        for item in obj:
            result = find_genotype(item, depth+1)
            if result: return result
    return None
print(find_genotype(d) or 'NOT_FOUND')
" 2>/dev/null)
        if [ "$genotype" != "NOT_FOUND" ] && [ -n "$genotype" ]; then
            echo "Fallback parsing found genotype: $genotype"
        fi
        ;;
    *)
        echo "Request failed"
        exit 1
        ;;
esac
```

### Authentication Error Recovery

When a request fails due to authentication issues (JWT expired or invalid), follow this workflow:

**1. Detect authentication errors** - Check for these response patterns:
```json
{"detail":"Incorrect authentication credentials."}
{"detail":"Authentication credentials were not provided."}
{"detail":"Error decoding signature."}
```

**2. Prompt the user** with this message:

```
## SelfDecode Authentication Error

Your JWT token has expired or is invalid. To continue:

1. Log in to SelfDecode in your browser
2. Open Developer Tools (F12) → Network tab
3. Navigate to any SNP page (e.g., https://selfdecode.com/app/snp/rs429358)
4. Find request to `/service/health-analysis/genes/genotype/`
5. From Request Headers, copy the `authorization` value (just the `eyJ...` part)
6. Update your profile YAML with the new token:
   ```yaml
   data_sources:
     selfdecode:
       jwt_token: "eyJ..."  # Paste new token here
   ```

**Reply "done" or "updated" when you've refreshed the token**, and I'll retry the lookup.
```

**3. Wait for user confirmation** - Do not proceed until user confirms token update

**4. Re-read the profile** to get the new token:
```bash
# Re-read profile YAML to get updated jwt_token
cat profiles/{profile_name}.yaml | grep -A5 "selfdecode:"
```

**5. Retry the original request** with the new token

### Implementation Example

```bash
# After curl request, check for auth errors
if echo "$response" | grep -qE '"detail".*([Aa]uthentication|credentials|signature)'; then
  echo "AUTH_ERROR: JWT token expired or invalid"
  echo "Prompt user to update token and wait for confirmation before retrying"
  exit 2  # Exit code 2 = auth error (distinct from other errors)
fi
```

**Important**: When you detect an auth error:
1. **Stop the current operation** - don't continue with stale/invalid credentials
2. **Inform the user clearly** - explain what happened and how to fix it
3. **Wait for explicit confirmation** - user must say they've updated the token
4. **Re-read the profile** - don't use cached credentials, read fresh from YAML
5. **Retry the exact same operation** - resume from where you left off

## Integration Notes

### When to Use SelfDecode vs SNPedia

| Use SelfDecode | Use SNPedia (genetics-snp-lookup) |
|----------------|-----------------------------------|
| SNP not in 23andMe raw data | SNP is in 23andMe raw data |
| User specifically requests SelfDecode | Need research citations/mechanisms |
| Checking imputed genotypes | Need interpretation context |
| Batch lookups for efficiency | Public interpretation needed |

### Lookup Strategy

For comprehensive SNP investigation:

1. **First**: Check 23andMe raw data via `genetics-snp-lookup` (directly genotyped, most reliable)
2. **Second**: If not found and SelfDecode configured, check `genetics-selfdecode-lookup` for imputed data
3. **Third**: Always query SNPedia for interpretation (research citations, mechanisms)

### Cross-Referencing

When both sources have data for the same SNP:

```markdown
## SNP Comparison: rs429358

| Source | Genotype | Notes |
|--------|----------|-------|
| 23andMe (raw) | T;T | Directly genotyped |
| SelfDecode (imputed) | T;T | Matches raw data |

**Concordance**: Sources agree. High confidence.
```

**Note**: If sources disagree, prefer 23andMe raw data (directly genotyped) over SelfDecode (imputed).

## Security Notes

- **JWT tokens are sensitive**: Profile YAML files are gitignored by default (see `.gitignore`), so storing credentials in your profile is safe. Verify your `.gitignore` includes `profiles/*.yaml` before adding credentials.
- **Alternative: environment variables**: For extra security, you can store JWT in environment variables and reference them in scripts, though this requires more setup.
- **Token expiration**: JWT tokens expire after 24-48 hours. Refresh when you get authentication errors (the skill will prompt you).
- **Cache safety**: Cache files contain only genotype data, not credentials. They can safely be committed if desired (though they're also gitignored by default).
