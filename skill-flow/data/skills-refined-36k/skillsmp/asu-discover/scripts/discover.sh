#!/usr/bin/env bash
#
# discover.sh - ASU Domain Discovery with Smart Keyword Expansion
# Finds relevant code, repos, and patterns across ASU's GitHub org
#
# Features:
#   - Local SQLite index with FTS5 for fast repo discovery (Tier 1)
#   - Rate-limited code search with 24h caching (Tier 2)
#   - Domain taxonomy for intelligent query expansion
#   - Team prefix detection and filtering
#
# Usage: discover.sh <action> [options]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/../config"
DATA_DIR="$SCRIPT_DIR/../data"
LIB_DIR="$SCRIPT_DIR/lib"
DOMAINS_FILE="$CONFIG_DIR/domains.yaml"

# Source database helpers
source "$LIB_DIR/db.sh"

# Source YAML parsing helpers
if [[ -f "$LIB_DIR/yaml.sh" ]]; then
    source "$LIB_DIR/yaml.sh"
fi

# Source DNS scaffolding helpers
if [[ -f "$LIB_DIR/dns.sh" ]]; then
    source "$LIB_DIR/dns.sh"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Defaults
ORG="ASU"
LIMIT=30
JSON_OUTPUT=false
EXPAND=true
VERBOSE=false
CACHED_ONLY=false
LOCAL_ONLY=false

usage() {
    cat << 'EOF'
Usage: discover.sh <action> [options]

ASU Domain Discovery - Smart search across ASU repositories

ACTIONS:
  search            Search repos and code with domain-aware expansion
  repos             Find repositories by domain or prefix
  code              Search code with rate limiting and caching
  context           Build context for an integration task
  patterns          Find integration patterns between systems
  pattern           Show design pattern details (e.g., EEL)
  expand            Show how a query would be expanded (debug)
  index             Manage the local repository index

INDEX SUBCOMMANDS:
  index build       Build full index from scratch (~30s)
  index refresh     Incremental update (repos changed since last run)
  index stats       Show index statistics and counts
  index verify      Check if referenced repos still exist [--dry-run] [--limit N]
  index classify    Re-run domain classification

PATTERN SUBCOMMANDS:
  pattern --list                    List available design patterns
  pattern --name eel                Show EEL pattern overview
  pattern --name eel --type publisher   Find publisher examples
  pattern --name eel --type subscriber  Find subscriber examples
  pattern --name eel --brief        Show condensed output

COMMON OPTIONS:
  --query QUERY     Search query (natural language or keywords)
  --domain DOMAIN   Filter to specific domain
  --prefix PREFIX   Filter by team prefix (crm, eadv, aiml, etc.)
  --name NAME       Pattern name (for pattern action)
  --type TYPE       Pattern type: publisher, subscriber, boilerplate
  --language LANG   Filter by programming language
  --limit N         Maximum results (default: 30)
  --brief           Show condensed output (patterns only)
  --no-expand       Disable keyword expansion
  --local-only      Only search local index (no API calls)
  --cached-only     Only use cached code search results
  --json            Output in JSON format
  --verbose         Show debug information
  --help            Show this help message

EXAMPLES:
  # Search with automatic domain detection
  discover.sh search --query "PeopleSoft IB integration"
  
  # Search within a specific domain
  discover.sh search --query "get principal" --domain dpl
  
  # Find repos by team prefix
  discover.sh repos --prefix crm --limit 20
  
  # Rate-limited code search (checks cache first)
  discover.sh code --query "checkAccess" --language typescript
  
  # Build context for a task (auto-suggests design patterns)
  discover.sh context --query "sync employee data from PS to DPL"
  
  # Find integration patterns
  discover.sh patterns --source peoplesoft --target dpl
  
  # Show EEL design pattern
  discover.sh pattern --name eel
  discover.sh pattern --name eel --type publisher
  discover.sh pattern --name vault --brief
  
  # Build/refresh the local index
  discover.sh index build
  discover.sh index stats
  discover.sh index verify

DOMAINS:
  peoplesoft, edna, dpl, serviceauth, auth, identity, salesforce,
  ml, terraform, cicd, cloudflare, infoblox, aws, api, eel, logging,
  vault, devops, mulesoft, feature-flags

DESIGN PATTERNS:
  eel              - Enterprise Event Lake (Kafka-based event-driven)
  cicd             - CI/CD Pipelines (Jenkins shared library, GitHub Actions)
  terraform-modules - ASU Terraform Modules (dco-terraform on JFrog)
  vault            - HashiCorp Vault Secrets (read/sync patterns)
  observability    - Observability Stack (Datadog, Logging Lake, CloudWatch)
  dns              - DNS Configuration (Infoblox for *.asu.edu, Cloudflare for external)

DNS COMMANDS:
  dns-validate     Validate domain and show provider recommendation
  dns-scaffold     Generate Terraform scaffolding for DNS records
  dns-examples     Show example repos using DNS patterns

DNS OPTIONS:
  --domain DOMAIN  Domain to validate or scaffold
  --type TYPE      Record type: a, cname (default: cname)
  --target VALUE   Target IP or hostname
  --pattern PTRN   Pattern: hybrid (Infoblox->Cloudflare CDN)
  --origin VALUE   Origin server for hybrid pattern
  --check-dns      Check if domain exists in DNS (uses dig)
  --no-vault       Skip Vault secrets in output

DNS EXAMPLES:
  # Validate a domain (returns provider recommendation)
  discover.sh dns-validate --domain myapp.asu.edu
  discover.sh dns-validate --domain myapp.example.com --check-dns
  
  # Scaffold Infoblox CNAME for *.asu.edu domain
  discover.sh dns-scaffold --domain myapp.asu.edu --type cname --target cdn.example.com
  
  # Scaffold Cloudflare A record for external domain
  discover.sh dns-scaffold --domain myapp.example.com --type a --target 1.2.3.4
  
  # Scaffold hybrid pattern (ASU domain with Cloudflare CDN)
  discover.sh dns-scaffold --domain myapp.asu.edu --pattern hybrid --origin origin.aws.com

TEAM PREFIXES:
  crm (66), eadv (38), authn (15), aiml (12), edna (11), iden (10),
  evbr, eli5, dco, caas, devops, dot, mom, ceng, ddt, appss, ewp,
  infra, tf, dpl, ps, sf, cf, unity
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}" >&2; }
success() { echo -e "${GREEN}$1${NC}" >&2; }
warn() { echo -e "${YELLOW}$1${NC}" >&2; }
debug() { [[ "$VERBOSE" == "true" ]] && echo -e "${CYAN}[debug] $1${NC}" >&2 || true; }

# Parse YAML - simple extraction
# Note: domains are under 'domains:' key with 2-space indent
yaml_get_domain_field() {
    local file="$1" domain="$2" field="$3"
    # Match from "  domain:" until next "  something:" at same level
    sed -n "/^  $domain:/,/^  [a-zA-Z]/p" "$file" 2>/dev/null | \
        sed -n "/^    $field:/,/^    [a-zA-Z]/p" 2>/dev/null | \
        grep "^      - " | \
        sed 's/^      - //' | \
        tr -d '"' | \
        head -20 || true
}

yaml_get_prefixes() {
    local file="$1" domain="$2"
    # Get prefixes line which is formatted as: prefixes: [a, b, c]
    sed -n "/^  $domain:/,/^  [a-zA-Z]/p" "$file" 2>/dev/null | \
        grep "prefixes:" | \
        sed 's/.*prefixes: *//' | \
        tr -d '[]' | \
        tr ',' '\n' | \
        tr -d ' ' || true
}

yaml_get_team_prefix_domain() {
    local file="$1" prefix="$2"
    grep "^  $prefix:" "$file" 2>/dev/null | awk '{print $2}' || true
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --query) QUERY="$2"; shift 2 ;;
            --domain) DOMAIN="$2"; shift 2 ;;
            --prefix) PREFIX="$2"; shift 2 ;;
            --source) SOURCE_DOMAIN="$2"; shift 2 ;;
            --target) TARGET_DOMAIN="$2"; TARGET="$2"; shift 2 ;;
            --name) PATTERN_NAME="$2"; shift 2 ;;
            --type) TYPE="$2"; PATTERN_TYPE="$2"; shift 2 ;;
            --list) LIST_PATTERNS=true; shift ;;
            --language) LANGUAGE="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --no-expand) EXPAND=false; shift ;;
            --local-only) LOCAL_ONLY=true; shift ;;
            --cached-only) CACHED_ONLY=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --verbose) VERBOSE=true; shift ;;
            --brief) BRIEF=true; shift ;;
            --origin) ORIGIN="$2"; shift 2 ;;
            --pattern) PATTERN="$2"; shift 2 ;;
            --check-dns) CHECK_DNS=true; shift ;;
            --no-vault) INCLUDE_VAULT=false; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

#
# Ensure index exists, auto-build if needed
#
ensure_index() {
    if ! db_exists; then
        warn "Index not found. Building automatically (this takes ~30 seconds)..."
        action_index_build
    fi
}

#
# Detect domains from query text
#
detect_domains() {
    local query="$1"
    local query_lower
    query_lower=$(echo "$query" | tr '[:upper:]' '[:lower:]')
    local detected=""
    
    # All known domains
    local all_domains="peoplesoft edna dpl serviceauth auth identity salesforce ml terraform cicd cloudflare infoblox aws api eel logging vault devops mulesoft feature-flags"
    
    for domain in $all_domains; do
        local triggers
        triggers=$(yaml_get_domain_field "$DOMAINS_FILE" "$domain" "triggers" 2>/dev/null)
        while IFS= read -r trigger; do
            [[ -z "$trigger" ]] && continue
            local trigger_lower
            trigger_lower=$(echo "$trigger" | tr '[:upper:]' '[:lower:]')
            if [[ "$query_lower" == *"$trigger_lower"* ]]; then
                detected="$detected $domain"
                break
            fi
        done <<< "$triggers"
    done
    
    # Deduplicate and trim
    echo "$detected" | tr ' ' '\n' | grep -v '^$' | sort -u | tr '\n' ' ' | sed 's/ $//' || true
}

#
# Expand query with domain synonyms
#
expand_query() {
    local query="$1"
    local domains="$2"
    local expanded_terms=()
    
    # Start with original query
    expanded_terms+=("$query")
    
    # Add synonyms from detected domains
    for domain in $domains; do
        local synonyms
        synonyms=$(yaml_get_domain_field "$DOMAINS_FILE" "$domain" "synonyms" 2>/dev/null)
        while IFS= read -r syn; do
            [[ -z "$syn" ]] && continue
            if [[ "$query" != *"$syn"* ]]; then
                expanded_terms+=("$syn")
            fi
        done <<< "$synonyms"
    done
    
    # Build OR query (max 8 terms)
    local result=""
    local count=0
    for term in "${expanded_terms[@]}"; do
        [[ -z "$term" ]] && continue
        if [[ $count -lt 8 ]]; then
            if [[ -n "$result" ]]; then
                result="$result OR $term"
            else
                result="$term"
            fi
            ((count++))
        fi
    done
    
    echo "$result"
}

#
# Get language hints for domains
#
get_language_hints() {
    local domains="$1"
    local extensions=()
    
    for domain in $domains; do
        local exts
        exts=$(awk "/^  $domain:/,/^  [a-z]/" "$DOMAINS_FILE" 2>/dev/null | \
               grep -A 10 "file_hints:" 2>/dev/null | \
               grep "extensions:" | \
               sed 's/.*\[//' | sed 's/\].*//' | \
               tr ',' '\n' | tr -d ' "' || true)
        while IFS= read -r ext; do
            [[ -n "$ext" ]] && extensions+=("$ext")
        done <<< "$exts"
    done
    
    # Map extension to GitHub language
    if [[ ${#extensions[@]} -gt 0 ]]; then
        case "${extensions[0]}" in
            py) echo "Python" ;;
            ts) echo "TypeScript" ;;
            js) echo "JavaScript" ;;
            go) echo "Go" ;;
            java) echo "Java" ;;
            tf|hcl) echo "HCL" ;;
            *) echo "" ;;
        esac
    fi
}

#
# Get known repos for domains
#
get_domain_repos() {
    local domains="$1"
    local repos=()
    
    for domain in $domains; do
        local domain_repos
        domain_repos=$(yaml_get_domain_field "$DOMAINS_FILE" "$domain" "repos" 2>/dev/null)
        while IFS= read -r repo; do
            [[ -n "$repo" ]] && repos+=("$repo")
        done <<< "$domain_repos"
    done
    
    printf '%s\n' "${repos[@]}" 2>/dev/null | sort -u
}

#
# ACTION: Build Index
#
action_index_build() {
    info "Building ASU repository index..."
    
    # Initialize database
    db_init
    
    # Fetch all repos from ASU org
    info "Fetching repositories from $ORG org..."
    
    local repos_json
    repos_json=$(gh api "orgs/$ORG/repos" --paginate \
        --jq '.[] | {name, full_name, description, language, pushed_at, stargazers_count, visibility, archived, topics}' \
        2>/dev/null) || error "Failed to fetch repos. Check 'gh auth status'"
    
    local count=0
    while IFS= read -r repo; do
        [[ -z "$repo" ]] && continue
        
        local name full_name description language pushed_at stars visibility archived topics
        name=$(echo "$repo" | jq -r '.name')
        full_name=$(echo "$repo" | jq -r '.full_name')
        description=$(echo "$repo" | jq -r '.description // ""')
        language=$(echo "$repo" | jq -r '.language // ""')
        pushed_at=$(echo "$repo" | jq -r '.pushed_at // ""')
        stars=$(echo "$repo" | jq -r '.stargazers_count // 0')
        visibility=$(echo "$repo" | jq -r '.visibility // "private"')
        archived=$(echo "$repo" | jq -r 'if .archived then 1 else 0 end')
        topics=$(echo "$repo" | jq -r '.topics | join(",") // ""')
        
        db_upsert_repo "$name" "$full_name" "$description" "$language" "$pushed_at" "$stars" "$visibility" "$archived" "$topics"
        
        ((count++))
        if [[ $((count % 100)) -eq 0 ]]; then
            debug "Processed $count repos..."
        fi
    done <<< "$repos_json"
    
    # Run domain classification
    info "Classifying repos by domain..."
    action_index_classify_internal
    
    # Update metadata
    db_set_meta "last_index_update" "$(date -Iseconds)"
    db_set_meta "repo_count" "$count"
    
    success "Index built: $count repositories indexed"
}

#
# ACTION: Refresh Index (incremental)
#
action_index_refresh() {
    ensure_index
    
    local last_update
    last_update=$(db_get_meta "last_index_update")
    
    if [[ -z "$last_update" ]]; then
        info "No previous update found. Running full build..."
        action_index_build
        return
    fi
    
    info "Refreshing index (repos updated since $last_update)..."
    
    # Fetch repos updated since last run
    local repos_json
    repos_json=$(gh api "orgs/$ORG/repos" --paginate \
        --jq ".[] | select(.pushed_at > \"$last_update\") | {name, full_name, description, language, pushed_at, stargazers_count, visibility, archived, topics}" \
        2>/dev/null) || error "Failed to fetch repos"
    
    local count=0
    while IFS= read -r repo; do
        [[ -z "$repo" ]] && continue
        
        local name full_name description language pushed_at stars visibility archived topics
        name=$(echo "$repo" | jq -r '.name')
        full_name=$(echo "$repo" | jq -r '.full_name')
        description=$(echo "$repo" | jq -r '.description // ""')
        language=$(echo "$repo" | jq -r '.language // ""')
        pushed_at=$(echo "$repo" | jq -r '.pushed_at // ""')
        stars=$(echo "$repo" | jq -r '.stargazers_count // 0')
        visibility=$(echo "$repo" | jq -r '.visibility // "private"')
        archived=$(echo "$repo" | jq -r 'if .archived then 1 else 0 end')
        topics=$(echo "$repo" | jq -r '.topics | join(",") // ""')
        
        db_upsert_repo "$name" "$full_name" "$description" "$language" "$pushed_at" "$stars" "$visibility" "$archived" "$topics"
        ((count++))
    done <<< "$repos_json"
    
    db_set_meta "last_index_update" "$(date -Iseconds)"
    
    success "Refreshed: $count repositories updated"
}

#
# ACTION: Index Stats
#
action_index_stats() {
    ensure_index
    echo -e "${BOLD}=== Index Statistics ===${NC}"
    echo ""
    # Use new dynamic count functions from db.sh
    get_index_stats
    echo ""
    echo -e "${BOLD}Top Prefixes:${NC}"
    get_prefix_stats 10
    echo ""
    cache_stats
}

#
# ACTION: Verify - Check if referenced repos still exist
# Flags: --dry-run (list repos without API calls), --limit N (check only N repos)
#
action_index_verify() {
    local dry_run=false
    local limit=0
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run) dry_run=true; shift ;;
            --limit) limit="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    echo -e "${BOLD}=== Verifying Referenced Repositories ===${NC}"
    echo ""
    
    if $dry_run; then
        echo "Repositories that would be verified:"
        [[ $limit -gt 0 ]] && echo "(Limited to first $limit)"
    else
        echo "Checking repositories referenced in domains.yaml..."
        echo "(This may take a minute due to API rate limits)"
    fi
    echo ""
    
    # Extract all ASU/repo-name references from domains.yaml
    local refs
    refs=$(grep -oE 'ASU/[a-zA-Z0-9_-]+' "$DOMAINS_FILE" 2>/dev/null | sort -u)
    
    local total=0 valid=0 invalid=0
    local invalid_repos=""
    
    for repo in $refs; do
        ((total++)) || true
        
        # Check limit
        if [[ $limit -gt 0 && $total -gt $limit ]]; then
            ((total--)) || true  # Don't count this one
            break
        fi
        
        if $dry_run; then
            echo "  $repo"
            ((valid++)) || true
            continue
        fi
        
        printf "\rChecking: %s" "$repo"
        
        if gh repo view "$repo" &>/dev/null; then
            ((valid++)) || true
        else
            ((invalid++)) || true
            invalid_repos="$invalid_repos\n  - $repo"
        fi
        
        # Brief rate limit protection
        sleep 0.1
    done
    
    if ! $dry_run; then
        printf "\r%-60s\n" ""  # Clear line
    fi
    echo ""
    
    if [[ $invalid -gt 0 ]]; then
        echo -e "${YELLOW}Invalid/Missing Repositories:${NC}"
        echo -e "$invalid_repos"
        echo ""
    fi
    
    echo -e "${BOLD}Summary:${NC}"
    if $dry_run; then
        echo "  Would verify: $total repositories"
    else
        echo "  Total checked: $total"
        echo -e "  Valid: ${GREEN}$valid${NC}"
        if [[ $invalid -gt 0 ]]; then
            echo -e "  Invalid: ${RED}$invalid${NC}"
        else
            echo -e "  Invalid: ${GREEN}0${NC}"
        fi
    fi
}

#
# Internal: Classify repos by domain
#
action_index_classify_internal() {
    # Get all domains and their prefixes
    local all_domains="peoplesoft edna dpl serviceauth auth identity salesforce ml terraform cicd cloudflare infoblox aws api"
    
    for domain in $all_domains; do
        # Get prefixes for this domain
        local prefixes
        prefixes=$(yaml_get_prefixes "$DOMAINS_FILE" "$domain")
        
        for prefix in $prefixes; do
            [[ -z "$prefix" ]] && continue
            
            # Link all repos with this prefix to the domain
            local repo_ids
            repo_ids=$(db_query "SELECT id FROM repos WHERE prefix = '$prefix'")
            
            while IFS= read -r repo_id; do
                [[ -z "$repo_id" ]] && continue
                db_link_repo_domain "$repo_id" "$domain" "0.9"
            done <<< "$repo_ids"
        done
        
        # Also match by triggers in name/description
        local triggers
        triggers=$(yaml_get_domain_field "$DOMAINS_FILE" "$domain" "triggers" 2>/dev/null | head -5)
        
        for trigger in $triggers; do
            [[ -z "$trigger" ]] && continue
            trigger="${trigger//\'/\'\'}"
            
            local repo_ids
            repo_ids=$(db_query "SELECT id FROM repos WHERE name LIKE '%$trigger%' OR description LIKE '%$trigger%'")
            
            while IFS= read -r repo_id; do
                [[ -z "$repo_id" ]] && continue
                db_link_repo_domain "$repo_id" "$domain" "0.7"
            done <<< "$repo_ids"
        done
    done
}

#
# ACTION: Search (Tier 1 local + Tier 2 API)
#
action_search() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    ensure_index
    
    # Detect domains
    local detected_domains
    if [[ -n "${DOMAIN:-}" ]]; then
        detected_domains="$DOMAIN"
    else
        detected_domains=$(detect_domains "$QUERY")
    fi
    
    debug "Detected domains: $detected_domains"
    
    # Expand query if enabled
    local search_query="$QUERY"
    if [[ "$EXPAND" == "true" ]] && [[ -n "$detected_domains" ]]; then
        search_query=$(expand_query "$QUERY" "$detected_domains")
        debug "Expanded query: $search_query"
    fi
    
    echo -e "${BOLD}=== Tier 1: Local Repository Search ===${NC}"
    info "Searching local index: $QUERY"
    [[ "$EXPAND" == "true" ]] && [[ "$search_query" != "$QUERY" ]] && info "Expanded: ${search_query:0:60}..."
    echo ""
    
    # Tier 1: Local SQLite search
    local local_results
    local_results=$(db_search_repos_like "$QUERY" "$LIMIT")
    
    if [[ -n "$local_results" ]]; then
        echo "Found in local index:"
        echo "$local_results" | while IFS=$'\t' read -r id name full_name desc lang prefix; do
            printf "  ${GREEN}%-40s${NC} %-10s %-8s %s\n" "$full_name" "${lang:-}" "[${prefix:-}]" "${desc:0:40}"
        done
    else
        echo "  No local matches found."
    fi
    
    # Stop here if local-only
    if [[ "$LOCAL_ONLY" == "true" ]]; then
        return
    fi
    
    echo ""
    echo -e "${BOLD}=== Tier 2: GitHub Code Search ===${NC}"
    
    # Tier 2: Code search (rate limited)
    local lang_hint=""
    if [[ -n "${LANGUAGE:-}" ]]; then
        lang_hint="$LANGUAGE"
    elif [[ -n "$detected_domains" ]]; then
        lang_hint=$(get_language_hints "$detected_domains")
    fi
    
    # Check cache first
    local cache_key="$QUERY|$lang_hint|$LIMIT"
    local cached
    cached=$(cache_get "$cache_key")
    
    if [[ -n "$cached" ]]; then
        info "Using cached results (< 24h old)"
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            echo "$cached"
        else
            echo "$cached" | jq -r '.[] | "  \(.repository.nameWithOwner):\(.path)"' 2>/dev/null || echo "$cached"
        fi
        return
    fi
    
    if [[ "$CACHED_ONLY" == "true" ]]; then
        warn "No cached results. Use without --cached-only to query API."
        return
    fi
    
    # Rate limit check
    rate_limit_wait
    
    info "Querying GitHub API..."
    
    # Build search command
    local -a cmd=(gh search code "$QUERY" --owner "$ORG" --limit "$LIMIT")
    [[ -n "$lang_hint" ]] && cmd+=(--language "$lang_hint")
    
    local api_results
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,path,textMatches)
        api_results=$("${cmd[@]}" 2>/dev/null) || api_results="[]"
        echo "$api_results"
    else
        cmd+=(--json repository,path)
        api_results=$("${cmd[@]}" 2>/dev/null) || api_results="[]"
        echo "$api_results" | jq -r '.[] | "  \(.repository.nameWithOwner):\(.path)"' 2>/dev/null || echo "  No code matches found."
    fi
    
    # Cache results
    cache_set "$cache_key" "$api_results"
}

#
# ACTION: Code Search (rate-limited with cache)
#
action_code() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    ensure_index
    
    local cache_key="code|$QUERY|${LANGUAGE:-}|$LIMIT"
    local cached
    cached=$(cache_get "$cache_key")
    
    if [[ -n "$cached" ]]; then
        info "Using cached code search results"
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            echo "$cached"
        else
            echo "$cached" | jq -r '.[] | "\(.repository.nameWithOwner):\(.path)"' 2>/dev/null || echo "$cached"
        fi
        return
    fi
    
    if [[ "$CACHED_ONLY" == "true" ]]; then
        warn "No cached results for this query."
        return
    fi
    
    # Rate limit
    rate_limit_wait
    
    info "Searching code: $QUERY"
    
    local -a cmd=(gh search code "$QUERY" --owner "$ORG" --limit "$LIMIT")
    [[ -n "${LANGUAGE:-}" ]] && cmd+=(--language "$LANGUAGE")
    
    local results
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,path,textMatches)
        results=$("${cmd[@]}" 2>/dev/null) || results="[]"
        echo "$results"
    else
        cmd+=(--json repository,path)
        results=$("${cmd[@]}" 2>/dev/null) || results="[]"
        
        local count
        count=$(echo "$results" | jq 'length' 2>/dev/null || echo "0")
        
        if [[ "$count" -gt 0 ]]; then
            echo "$results" | jq -r '.[] | "\(.repository.nameWithOwner):\(.path)"' 2>/dev/null
        else
            echo "No code matches found."
        fi
    fi
    
    # Cache
    cache_set "$cache_key" "$results"
}

#
# ACTION: Repos (by domain or prefix)
#
action_repos() {
    ensure_index
    
    if [[ -n "${PREFIX:-}" ]]; then
        info "Finding repositories with prefix: $PREFIX"
        
        local results
        results=$(db_get_repos_by_prefix "$PREFIX" "$LIMIT")
        
        if [[ -n "$results" ]]; then
            echo "$results" | while IFS=$'\t' read -r id name full_name desc lang; do
                printf "%-40s %-12s %s\n" "$full_name" "${lang:-}" "${desc:0:50}"
            done
        else
            echo "No repositories found with prefix '$PREFIX'"
        fi
        return
    fi
    
    if [[ -n "${DOMAIN:-}" ]]; then
        info "Finding repositories for domain: $DOMAIN"
        
        # First try local DB
        local results
        results=$(db_get_repos_by_domain "$DOMAIN" "$LIMIT")
        
        if [[ -n "$results" ]]; then
            echo "From local index:"
            echo "$results" | while IFS=$'\t' read -r id name full_name desc lang; do
                printf "  %-40s %-12s %s\n" "$full_name" "${lang:-}" "${desc:0:50}"
            done
        fi
        
        # Also show known repos from config
        echo ""
        echo "Known $DOMAIN repositories (from config):"
        get_domain_repos "$DOMAIN" | while read -r repo; do
            [[ -n "$repo" ]] && echo "  ASU/$repo"
        done
        return
    fi
    
    error "Must specify --domain or --prefix"
}

#
# ACTION: Context Builder
#
action_context() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query (describe the integration task)"
    
    ensure_index
    
    echo -e "${BOLD}=== Context for: $QUERY ===${NC}"
    echo ""
    
    # Detect domains
    local detected_domains
    detected_domains=$(detect_domains "$QUERY")
    
    # Detect applicable design patterns
    local detected_patterns
    detected_patterns=$(detect_patterns "$QUERY")
    
    if [[ -z "$detected_domains" ]]; then
        warn "No specific domains detected. Performing general search."
    fi
    
    echo -e "${BOLD}Detected Domains:${NC} ${detected_domains:-general}"
    echo ""
    
    # === DESIGN PATTERN SUGGESTIONS ===
    if [[ -n "$detected_patterns" ]]; then
        for pattern in $detected_patterns; do
            case "$pattern" in
                eel)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: EEL (Enterprise Event Lake) ===${NC}"
                    echo ""
                    echo "For real-time, event-driven integration:"
                    echo "  Boilerplate: ASU/evbr-enterprise-event-lake-event-handler-boilerplate"
                    echo "  Publishers:  ASU/edna (Java), ASU/iden-identity-resolution-service-api (Python)"
                    echo "  Subscribers: ASU/sisfa-peoplesoft-financial-aid-module-event-listeners"
                    echo "  Run: discover.sh pattern --name eel"
                    echo ""
                    ;;
                cicd)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: CI/CD Pipelines ===${NC}"
                    echo ""
                    echo "For Jenkins/GitHub Actions pipelines:"
                    echo "  Shared Library: ASU/devops-jenkins-pipeline-library (75+ functions)"
                    echo "  Key functions:  terraformApply, getVaultSecret, bridgecrewScan"
                    echo "  GH Actions:     ASU/caas-image-library (reusable workflows)"
                    echo "  Run: discover.sh pattern --name cicd"
                    echo ""
                    ;;
                terraform-modules)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: Terraform Modules ===${NC}"
                    echo ""
                    echo "For ASU infrastructure provisioning:"
                    echo "  Registry:  jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform"
                    echo "  Modules:   ec2-instance, aurora, vpc-core-v5, eks-oidc-provider"
                    echo "  REQUIRED:  product-tags (ASU tagging standard)"
                    echo "  Run: discover.sh pattern --name terraform-modules"
                    echo ""
                    ;;
                vault)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: Vault Secrets ===${NC}"
                    echo ""
                    echo "For secrets management:"
                    echo "  TypeScript: AWS SDK (@aws-sdk/client-secrets-manager)"
                    echo "  Python:    ASU/edna-rmi-linux (hvac + token file)"
                    echo "  Terraform: ASU/wflow-kuali-approver-service (Vault→Secrets Manager)"
                    echo "  Jenkins:   vaultLogin, getVaultSecret, getVaultAppRoleToken"
                    echo "  Run: discover.sh pattern --name vault"
                    echo ""
                    ;;
                observability)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: Observability ===${NC}"
                    echo ""
                    echo "For monitoring, logging, and tracing:"
                    echo "  Datadog:      APM (dd-trace), RUM (@datadog/browser-rum)"
                    echo "  Logging Lake: Cribl → S3 → OpenSearch (RECOMMENDED for logs)"
                    echo "  CloudWatch:   Alarms, routing to Datadog or Logging Lake"
                    echo -e "  ${YELLOW}Splunk:       DEPRECATED - migrate to Logging Lake${NC}"
                    echo "  Run: discover.sh pattern --name observability"
                    echo ""
                    ;;
                custom-domains)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: Custom Domain Provisioning ===${NC}"
                    echo ""
                    echo "For provisioning custom domains (*.asu.edu):"
                    echo "  PRIMARY:     ASU/iden-fraud-watchdog (ACM + Route53 + CloudFront)"
                    echo "  ACM:         us-east-1 for CloudFront/API Gateway (edge)"
                    echo "  Validation:  DNS validation with Route53 (cross-account support)"
                    echo "  DNS:         Route53 for validation, Infoblox for *.asu.edu CNAMEs"
                    echo "  Run: discover.sh pattern --name custom-domains"
                    echo ""
                    ;;
                dns)
                    echo -e "${YELLOW}${BOLD}=== Suggested Pattern: DNS Configuration ===${NC}"
                    echo ""
                    echo "For DNS records (Infoblox + Cloudflare):"
                    echo "  *.asu.edu:   Infoblox (dnsadmin.asu.edu) - both views"
                    echo "  External:    Cloudflare for registration + DNS"
                    echo "  Hybrid:      Infoblox CNAME → Cloudflare CDN → Origin"
                    echo "  Examples:    ASU/sso-shibboleth, ASU/hosting-fse"
                    echo "  Run: discover.sh pattern --name dns"
                    echo ""
                    ;;
            esac
        done
    fi
    
    # Show matching repos from local index
    echo -e "${BOLD}Relevant Repositories (local index):${NC}"
    local local_results
    local_results=$(db_search_repos_like "$QUERY" 10)
    
    if [[ -n "$local_results" ]]; then
        echo "$local_results" | while IFS=$'\t' read -r id name full_name desc lang prefix; do
            printf "  %-40s %-10s %s\n" "$full_name" "${lang:-}" "[${prefix:-}]"
        done
    else
        echo "  (none found)"
    fi
    echo ""
    
    # Show known repos from config
    echo -e "${BOLD}Key Repositories (from config):${NC}"
    if [[ -n "$detected_domains" ]]; then
        for domain in $detected_domains; do
            echo "  [$domain]"
            get_domain_repos "$domain" | head -5 | while read -r repo; do
                [[ -n "$repo" ]] && echo "    - ASU/$repo"
            done
        done
    else
        echo "  (specify domain for known repos)"
    fi
    echo ""
    
    # Show relevant prefixes
    echo -e "${BOLD}Relevant Team Prefixes:${NC}"
    if [[ -n "$detected_domains" ]]; then
        for domain in $detected_domains; do
            local prefixes
            prefixes=$(yaml_get_prefixes "$DOMAINS_FILE" "$domain" | tr '\n' ', ' | sed 's/,$//')
            [[ -n "$prefixes" ]] && echo "  $domain: $prefixes"
        done
    fi
    echo ""
    
    # Suggest search queries
    echo -e "${BOLD}Suggested Searches:${NC}"
    for domain in $detected_domains; do
        local syn
        syn=$(yaml_get_domain_field "$DOMAINS_FILE" "$domain" "synonyms" 2>/dev/null | head -3 | tr '\n' ' ')
        [[ -n "$syn" ]] && echo "  discover.sh code --query \"$syn\" --domain $domain"
    done
}

#
# ACTION: Patterns
#
action_patterns() {
    [[ -z "${SOURCE_DOMAIN:-}" ]] && error "Missing --source domain"
    [[ -z "${TARGET_DOMAIN:-}" ]] && error "Missing --target domain"
    
    ensure_index
    
    echo -e "${BOLD}=== Integration Patterns: $SOURCE_DOMAIN -> $TARGET_DOMAIN ===${NC}"
    echo ""
    
    # Show repos mentioning both
    echo -e "${BOLD}Repositories linking both systems:${NC}"
    local source_triggers target_triggers
    source_triggers=$(yaml_get_domain_field "$DOMAINS_FILE" "$SOURCE_DOMAIN" "triggers" 2>/dev/null | head -3)
    target_triggers=$(yaml_get_domain_field "$DOMAINS_FILE" "$TARGET_DOMAIN" "triggers" 2>/dev/null | head -3)
    
    for st in $source_triggers; do
        [[ -z "$st" ]] && continue
        for tt in $target_triggers; do
            [[ -z "$tt" ]] && continue
            
            local matches
            matches=$(db_query "SELECT full_name, description FROM repos 
                               WHERE (name LIKE '%$st%' OR description LIKE '%$st%')
                                 AND (name LIKE '%$tt%' OR description LIKE '%$tt%')
                               LIMIT 5")
            
            [[ -n "$matches" ]] && echo "$matches" | while IFS=$'\t' read -r name desc; do
                echo "  $name: $desc"
            done
        done
    done | sort -u | head -10
    
    if [[ "$LOCAL_ONLY" != "true" ]] && [[ "$CACHED_ONLY" != "true" ]]; then
        echo ""
        echo -e "${BOLD}Code referencing both (from API):${NC}"
        
        rate_limit_wait
        
        gh search code "$SOURCE_DOMAIN $TARGET_DOMAIN" --owner "$ORG" --limit 10 \
            --json repository,path 2>/dev/null | \
            jq -r '.[] | "  \(.repository.nameWithOwner):\(.path)"' 2>/dev/null || echo "  (no direct references found)"
    fi
}

#
# Get design pattern field from YAML
#
yaml_get_pattern_field() {
    local file="$1" pattern="$2" field="$3"
    # design_patterns section has different indent structure
    sed -n "/^design_patterns:/,/^[a-z]/p" "$file" 2>/dev/null | \
        sed -n "/^  $pattern:/,/^  [a-zA-Z]/p" 2>/dev/null | \
        sed -n "/^    $field:/,/^    [a-zA-Z]/p" 2>/dev/null | \
        grep -v "^    $field:" | \
        sed 's/^      //' || true
}

#
# Get simple pattern field value
#
yaml_get_pattern_simple() {
    local file="$1" pattern="$2" field="$3"
    sed -n "/^design_patterns:/,/^[a-z]/p" "$file" 2>/dev/null | \
        sed -n "/^  $pattern:/,/^  [a-zA-Z]/p" 2>/dev/null | \
        grep "^    $field:" 2>/dev/null | \
        sed "s/^    $field: *//" | \
        tr -d '"' || true
}

#
# Get nested pattern field (e.g., publishers.java.repo)
#
yaml_get_pattern_nested() {
    local file="$1" pattern="$2" section="$3" item="$4" field="$5"
    sed -n "/^design_patterns:/,/^[a-z]/p" "$file" 2>/dev/null | \
        sed -n "/^  $pattern:/,/^  [a-zA-Z]/p" 2>/dev/null | \
        sed -n "/^    $section:/,/^    [a-zA-Z]/p" 2>/dev/null | \
        sed -n "/^      $item:/,/^      [a-zA-Z]/p" 2>/dev/null | \
        grep "^        $field:" 2>/dev/null | \
        sed "s/^        $field: *//" | \
        tr -d '"' || true
}

#
# Detect if query matches design pattern triggers
#
detect_patterns() {
    local query="$1"
    local query_lower
    query_lower=$(echo "$query" | tr '[:upper:]' '[:lower:]')
    local detected=""
    
    # EEL pattern triggers
    local eel_triggers="event-driven real-time realtime publish subscribe kafka confluent avro event lake async decoupled fanout fan-out"
    for trigger in $eel_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected eel"
            break
        fi
    done
    
    # CI/CD pattern triggers
    local cicd_triggers="jenkins pipeline jenkinsfile shared-library shared library github actions workflow_call reusable workflow terraformapply getvaultsecret bridgecrew"
    for trigger in $cicd_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected cicd"
            break
        fi
    done
    
    # Terraform modules pattern triggers
    local tf_triggers="terraform module dco-terraform product-tags aurora vpc-core ec2-instance eks-oidc jfrog-cloud"
    for trigger in $tf_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected terraform-modules"
            break
        fi
    done
    
    # Vault pattern triggers
    local vault_triggers="vault hvac secret getvaultsecret vaultlogin secretsmanager approle hashicorp"
    for trigger in $vault_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected vault"
            break
        fi
    done
    
    # Observability pattern triggers
    local obs_triggers="datadog logging cribl cloudwatch otel opentelemetry metrics monitoring apm rum tracing observability eli5 logging-lake dd-trace ddtrace splunk"
    for trigger in $obs_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected observability"
            break
        fi
    done
    
    # Custom domains pattern triggers
    local custom_domain_triggers="custom domain acm certificate ssl tls api gateway domain cloudfront alias route53 subdomain wildcard certificate dns validation certificate_domains"
    for trigger in $custom_domain_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected custom-domains"
            break
        fi
    done
    
    # DNS pattern triggers  
    local dns_triggers="infoblox dns record cname a record"
    for trigger in $dns_triggers; do
        if [[ "$query_lower" == *"$trigger"* ]]; then
            detected="$detected dns"
            break
        fi
    done
    
    # Deduplicate and trim
    echo "$detected" | tr ' ' '\n' | grep -v '^$' | sort -u | tr '\n' ' ' | sed 's/ $//' || true
}

#
# Show pattern from markdown file
# Usage: show_pattern <pattern> [subtype]
#
show_pattern() {
    local pattern="$1"
    local subtype="${2:-}"
    local brief="${BRIEF:-false}"
    local pattern_file="${SCRIPT_DIR}/../patterns/${pattern}.md"
    
    if [[ ! -f "$pattern_file" ]]; then
        error "Pattern file not found: $pattern_file"
    fi
    
    # Extract title from frontmatter
    local title
    title=$(grep -m1 '^title:' "$pattern_file" | sed 's/title: *//' | tr -d '"')
    
    if [[ "$brief" == "true" ]]; then
        # Brief mode: show title and description only
        echo -e "${BOLD}=== ${title} ===${NC}"
        echo ""
        grep -m1 '^description:' "$pattern_file" | sed 's/description: *//' | tr -d '"'
        echo ""
        # Show first few lines after frontmatter
        awk '/^---$/{n++; next} n==2{print; if(++c>=10) exit}' "$pattern_file"
        echo ""
        echo -e "${CYAN}Use without --brief for full details${NC}"
        return
    fi
    
    if [[ -n "$subtype" ]]; then
        # Show specific subtype section
        echo -e "${BOLD}=== ${title}: ${subtype} ===${NC}"
        echo ""
        
        # Extract section for subtype using awk (case-insensitive)
        awk -v subtype="$subtype" '
            BEGIN { IGNORECASE=1; in_section=0; found=0 }
            /^---$/ { frontmatter++; next }
            frontmatter < 2 { next }
            /^## / {
                if (in_section) exit
                if (tolower($0) ~ tolower(subtype)) {
                    in_section=1
                    found=1
                    print
                    next
                }
            }
            in_section { print }
            END { if (!found) exit 1 }
        ' "$pattern_file"
        
        if [[ $? -ne 0 ]]; then
            echo -e "${YELLOW}Subtype '$subtype' not found in pattern.${NC}"
            echo ""
            echo "Available subtypes:"
            grep -E '^  - ' "$pattern_file" | head -10 | sed 's/^  //'
        fi
    else
        # Show full pattern (skip frontmatter)
        echo -e "${BOLD}=== ${title} ===${NC}"
        echo ""
        
        # Skip YAML frontmatter and display content
        awk '
            /^---$/ { frontmatter++; next }
            frontmatter >= 2 { print }
        ' "$pattern_file"
    fi
}

#
# ACTION: Pattern - Show design pattern details
#
action_pattern() {
    # List available patterns
    if [[ "${LIST_PATTERNS:-}" == "true" ]]; then
        echo -e "${BOLD}=== Available Design Patterns ===${NC}"
        echo ""
        echo -e "${GREEN}eel${NC} - Enterprise Event Lake"
        echo "     Real-time, decoupled, event-driven architecture backbone"
        echo "     Built on Confluent Kafka with Avro schemas"
        echo ""
        echo -e "${GREEN}cicd${NC} - CI/CD Pipelines"
        echo "     Jenkins shared library (75+ functions) and GitHub Actions"
        echo "     Terraform, Vault, security scanning, notifications"
        echo ""
        echo -e "${GREEN}terraform-modules${NC} - ASU Terraform Modules"
        echo "     Custom modules from dco-terraform on JFrog"
        echo "     EC2, Aurora, VPC, EKS, Cloudflare, IAM, Observability"
        echo ""
        echo -e "${GREEN}vault${NC} - HashiCorp Vault Secrets"
        echo "     Patterns for reading secrets and syncing to AWS"
        echo "     Python hvac, Terraform, Jenkins integration"
        echo ""
        echo -e "${GREEN}observability${NC} - Observability Stack"
        echo "     Datadog APM/RUM, Cribl/Logging Lake, CloudWatch, OpenTelemetry"
        echo -e "     ${YELLOW}Splunk is DEPRECATED${NC} - use Logging Lake instead"
        echo ""
        echo -e "${GREEN}dns${NC} - DNS Configuration"
        echo "     Infoblox for *.asu.edu, Cloudflare for external domains"
        echo "     Includes hybrid pattern (Infoblox → Cloudflare CDN → Origin)"
        echo ""
        echo "Usage: discover.sh pattern --name <pattern>"
        echo "       discover.sh pattern --name <pattern> --type <type>"
        return
    fi
    
    [[ -z "${PATTERN_NAME:-}" ]] && error "Missing --name (e.g., --name eel) or use --list"
    
    local pattern="$PATTERN_NAME"
    local ptype="${PATTERN_TYPE:-}"
    local pattern_file="${SCRIPT_DIR}/../patterns/${pattern}.md"
    
    # Check if pattern markdown file exists
    if [[ -f "$pattern_file" ]]; then
        # Use markdown-based pattern loader
        show_pattern "$pattern" "$ptype"
    else
        # Validate pattern exists in YAML
        local pattern_name
        pattern_name=$(yaml_get_pattern_simple "$DOMAINS_FILE" "$pattern" "name")
        [[ -z "$pattern_name" ]] && error "Unknown pattern: $pattern. Use --list to see available patterns."
        
        # Fallback to legacy handlers for patterns without markdown files
        case "$pattern" in
            eel) show_pattern_eel "$ptype" ;;
            cicd) show_pattern_cicd "$ptype" ;;
            terraform-modules) show_pattern_terraform "$ptype" ;;
            vault) show_pattern_vault "$ptype" ;;
            observability) show_pattern_observability "$ptype" ;;
            dns) show_pattern_dns "$ptype" ;;
            *) show_pattern_generic "$pattern" "$ptype" ;;
        esac
    fi
}

#
# Show EEL pattern details
#
show_pattern_eel() {
    local ptype="$1"
    
    # Show specific type if requested
    if [[ -n "$ptype" ]]; then
        case "$ptype" in
            publisher|publishers)
                echo -e "${BOLD}=== Enterprise Event Lake (EEL) - Publisher Examples ===${NC}"
                echo ""
                
                for lang in java python javascript sisint; do
                    local repo path desc language
                    repo=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "publishers" "$lang" "repo")
                    [[ -z "$repo" ]] && continue
                    
                    path=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "publishers" "$lang" "path")
                    desc=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "publishers" "$lang" "description")
                    language=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "publishers" "$lang" "language")
                    
                    echo -e "${GREEN}$language:${NC}"
                    echo "  Repo: $repo"
                    [[ -n "$path" ]] && echo "  Path: $path"
                    echo "  $desc"
                    echo ""
                done
                ;;
                
            subscriber|subscribers)
                echo -e "${BOLD}=== Enterprise Event Lake (EEL) - Subscriber Examples ===${NC}"
                echo ""
                
                for sub in python_peoplesoft_fa python_peoplesoft_cc identity_listener; do
                    local repo desc language
                    repo=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "subscribers" "$sub" "repo")
                    [[ -z "$repo" ]] && continue
                    
                    desc=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "subscribers" "$sub" "description")
                    language=$(yaml_get_pattern_nested "$DOMAINS_FILE" "eel" "subscribers" "$sub" "language")
                    
                    echo -e "${GREEN}${language:-Python}:${NC}"
                    echo "  Repo: $repo"
                    echo "  $desc"
                    echo ""
                done
                ;;
                
            boilerplate)
                echo -e "${BOLD}=== Enterprise Event Lake (EEL) - Boilerplate ===${NC}"
                echo ""
                echo "Repository: ASU/evbr-enterprise-event-lake-event-handler-boilerplate"
                echo "Description: Official boilerplate for creating new EEL event handlers"
                echo "Use for: Starting a new EEL publisher or subscriber"
                echo ""
                echo "Clone: gh repo clone ASU/evbr-enterprise-event-lake-event-handler-boilerplate"
                ;;
                
            *)
                error "Unknown type: $ptype. Use: publisher, subscriber, or boilerplate"
                ;;
        esac
        return
    fi
    
    # Show full pattern overview
    echo -e "${BOLD}=== Design Pattern: Enterprise Event Lake (EEL) ===${NC}"
    echo ""
    echo "Real-time, decoupled, event-driven architectural backbone at ASU."
    echo "The EEL provides a managed Kafka-based messaging platform for"
    echo "asynchronous, loosely-coupled communication between services."
    echo ""
    
    echo -e "${BOLD}When to use:${NC}"
    echo "  - Real-time data synchronization across systems"
    echo "  - Loose coupling between services (publisher doesn't know subscribers)"
    echo "  - Event-driven workflows and notifications"
    echo "  - Async communication with PeopleSoft and other enterprise systems"
    echo "  - Fan-out scenarios (one event, many consumers)"
    echo ""
    
    echo -e "${BOLD}Architecture:${NC}"
    echo "  Platform: Confluent Cloud (Managed Apache Kafka)"
    echo "  Schema Format: Apache Avro"
    echo "  Delivery: At-least-once"
    echo ""
    
    echo -e "${BOLD}Publishers:${NC}"
    echo -e "  ${GREEN}Java:${NC}       ASU/edna → EELClient.java"
    echo -e "  ${GREEN}Python:${NC}     ASU/iden-identity-resolution-service-api → eel_client.py"
    echo -e "  ${GREEN}JavaScript:${NC} ASU/cremo-credid → enterprise-event-lake/"
    echo ""
    
    echo -e "${BOLD}Subscribers:${NC}"
    echo "  ASU/sisfa-peoplesoft-financial-aid-module-event-listeners"
    echo "  ASU/siscc-peoplesoft-campus-community-module-event-listeners"
    echo ""
    
    echo -e "${BOLD}Boilerplate:${NC}"
    echo "  ASU/evbr-enterprise-event-lake-event-handler-boilerplate"
    echo ""
    
    echo -e "${BOLD}Related Commands:${NC}"
    echo "  discover.sh pattern --name eel --type publisher"
    echo "  discover.sh pattern --name eel --type subscriber"
    echo "  discover.sh search --query \"EelClient\" --domain eel"
}

#
# Show CI/CD pattern details
#
show_pattern_cicd() {
    local ptype="$1"
    
    if [[ -n "$ptype" ]]; then
        case "$ptype" in
            jenkins)
                echo -e "${BOLD}=== CI/CD - Jenkins Shared Library ===${NC}"
                echo ""
                echo "Repository: ASU/devops-jenkins-pipeline-library"
                echo "Location:   vars/"
                echo ""
                echo -e "${BOLD}Terraform Functions:${NC}"
                echo "  terraformInit, terraformPlan, terraformApply"
                echo "  terraformPlanV2, terraformV2"
                echo "  pipelineTerraformSingleEnvironment"
                echo ""
                echo -e "${BOLD}Vault Functions:${NC}"
                echo "  vaultLogin, caasVaultLogin, opsVaultLogin"
                echo "  getVaultSecret, getVaultToken, getVaultAppRoleToken"
                echo ""
                echo -e "${BOLD}Credentials Setup:${NC}"
                echo "  setupGradleCredentials, setupMavenCredentials"
                echo "  setupNpmCredentials, setupPipCredentials"
                echo "  setupPoetryCredentials, setupUvCredentials"
                echo ""
                echo -e "${BOLD}Security Scanning:${NC}"
                echo "  bridgecrewScan, scanDockerImage, scanDockerImageWithInspector"
                echo ""
                echo -e "${BOLD}Notifications:${NC}"
                echo "  slackNotification, botNotification, datadogDeployment"
                echo ""
                echo -e "${BOLD}ServiceNow:${NC}"
                echo "  servicenow_change, changeFreezeCheck"
                echo ""
                echo -e "${BOLD}Ansible:${NC}"
                echo "  ansible, ansibleKubernetes, ansiblePlaybook"
                echo ""
                echo -e "${BOLD}MuleSoft:${NC}"
                echo "  mule4caasPipeline, mule4caasPipelineSf"
                echo "  mulesoftBuild, mulesoftDeploy"
                ;;
                
            github-actions|actions|gha)
                echo -e "${BOLD}=== CI/CD - GitHub Actions ===${NC}"
                echo ""
                echo -e "${GREEN}Reusable Workflows:${NC}"
                echo "  Repo: ASU/caas-image-library"
                echo "  Path: .github/workflows/"
                echo ""
                echo "  workflow-build-image.yml"
                echo "    Generic container image build with Trivy scanning"
                echo "    Trigger: workflow_call"
                echo ""
                echo "  workflow-build-image-tomcat.yml"
                echo "    Tomcat-specific image builds"
                echo "    Trigger: workflow_call"
                echo ""
                echo -e "${GREEN}Job Workflows:${NC}"
                echo "  job-apache-installer.yml"
                echo "  job-haproxy-default-backend.yml"
                echo "  job-k8s-deploy.yml"
                echo "  job-sonar-scanner.yml"
                echo ""
                echo -e "${GREEN}OIDC Example:${NC}"
                echo "  Repo: ASU/dco-github-actions-oidc-aws-example"
                echo "  GitHub Actions OIDC with AWS"
                ;;
                
            templates)
                echo -e "${BOLD}=== CI/CD - Pipeline Templates ===${NC}"
                echo ""
                echo -e "${GREEN}CaaS Templates:${NC}"
                echo "  Repo: ASU/caas-pipeline-templates"
                echo "  - legacy-warapps"
                echo "  - legacy-warapps-deployment"
                echo ""
                echo -e "${GREEN}Mobile Templates:${NC}"
                echo "  Repo: ASU/mobile-mapp-templates"
                echo "  Mobile Application Publishing Pipeline Templates"
                echo ""
                echo -e "${GREEN}MuleSoft Templates:${NC}"
                echo "  Repo: ASU/ddt-mulesoft-base-application-template"
                echo "  Template with container pipeline for Mulesoft apps"
                ;;
                
            *)
                error "Unknown type: $ptype. Use: jenkins, github-actions, or templates"
                ;;
        esac
        return
    fi
    
    # Full overview
    echo -e "${BOLD}=== Design Pattern: CI/CD Pipelines ===${NC}"
    echo ""
    echo "Centralized CI/CD patterns for Jenkins and GitHub Actions at ASU."
    echo "The primary asset is the Jenkins Shared Library with 75+ reusable"
    echo "Groovy functions covering Terraform, Vault, credentials, security"
    echo "scanning, and notifications."
    echo ""
    
    echo -e "${BOLD}Jenkins Shared Library:${NC}"
    echo "  Repo: ASU/devops-jenkins-pipeline-library"
    echo "  75+ reusable Groovy functions in vars/"
    echo ""
    echo "  Key function categories:"
    echo "    - Terraform: terraformInit, terraformPlan, terraformApply"
    echo "    - Vault: vaultLogin, getVaultSecret, getVaultAppRoleToken"
    echo "    - Credentials: setupMavenCredentials, setupNpmCredentials"
    echo "    - Security: bridgecrewScan, scanDockerImage"
    echo "    - Notifications: slackNotification, datadogDeployment"
    echo "    - ServiceNow: servicenow_change, changeFreezeCheck"
    echo ""
    
    echo -e "${BOLD}GitHub Actions:${NC}"
    echo "  Reusable Workflows: ASU/caas-image-library"
    echo "    workflow-build-image.yml (Trivy scanning)"
    echo "    workflow-build-image-tomcat.yml"
    echo "  OIDC Example: ASU/dco-github-actions-oidc-aws-example"
    echo ""
    
    echo -e "${BOLD}Pipeline Templates:${NC}"
    echo "  CaaS: ASU/caas-pipeline-templates"
    echo "  MuleSoft: ASU/ddt-mulesoft-base-application-template"
    echo "  Mobile: ASU/mobile-mapp-templates"
    echo ""
    
    echo -e "${BOLD}Team Prefixes:${NC} dco, caas, devops, dot"
    echo ""
    
    echo -e "${BOLD}Related Commands:${NC}"
    echo "  discover.sh pattern --name cicd --type jenkins"
    echo "  discover.sh pattern --name cicd --type github-actions"
    echo "  discover.sh pattern --name cicd --type templates"
    echo "  discover.sh repos --domain cicd"
}

#
# Show Terraform Modules pattern details
#
show_pattern_terraform() {
    local ptype="$1"
    
    if [[ -n "$ptype" ]]; then
        case "$ptype" in
            compute)
                echo -e "${BOLD}=== Terraform Modules - Compute ===${NC}"
                echo ""
                echo "ec2-instance              Linux EC2 with Ansible integration"
                echo "ec2-instance-linux-lowlevel  Low-level Linux EC2 configuration"
                echo "ec2-windows               Windows EC2 instances"
                echo "ec2-windows-v2            Windows EC2 v2"
                echo "ec2-macos-instance        macOS EC2 instances"
                echo "ec2-public-instance       Public-facing EC2 instances"
                echo "nutanix-vm                Nutanix virtual machines"
                ;;
                
            database|db)
                echo -e "${BOLD}=== Terraform Modules - Database ===${NC}"
                echo ""
                echo "aurora                    Aurora clusters"
                echo "aurora-mysql              Aurora MySQL"
                echo "aurora-postgres           Aurora PostgreSQL"
                echo "rds-mssql                 RDS SQL Server"
                echo "rds-oracle                RDS Oracle"
                ;;
                
            networking|network)
                echo -e "${BOLD}=== Terraform Modules - Networking ===${NC}"
                echo ""
                echo "vpc-core-v3               VPC with subnets, NAT, VPN (v3)"
                echo "vpc-core-v5               VPC with subnets, NAT, VPN, Route53 (v5)"
                echo "security-group            Security groups"
                echo "core-security-groups      Standard org-wide security groups"
                echo "route53-host              Route53 DNS records"
                echo "route53-private-zone      Private hosted zones"
                echo "route53-public-zone       Public hosted zones"
                ;;
                
            kubernetes|k8s|eks)
                echo -e "${BOLD}=== Terraform Modules - Kubernetes/EKS ===${NC}"
                echo ""
                echo "eks-oidc-provider         EKS OIDC identity provider"
                echo "eks-pod-identity-role     EKS pod identity IAM roles"
                echo "eks-service-account-role  IRSA (IAM Roles for Service Accounts)"
                echo "vault-kubernetes-auth-role  Vault K8s authentication"
                ;;
                
            cloudflare|cf)
                echo -e "${BOLD}=== Terraform Modules - Cloudflare ===${NC}"
                echo ""
                echo "cloudflare-tunnel                 Cloudflare Tunnel setup"
                echo "cloudflare-tunnel-route53-dns     Tunnel with Route53 DNS"
                echo "cloudflare-access-app             Cloudflare Access applications"
                echo "cloudflare-access-edna-group      EDNA-integrated access groups"
                echo "cloudflare-origin-ca-certificate  Origin CA certificates"
                echo "cloudflare-zone-logpush-logging-lake  Zone logs to data lake"
                echo "cloudflare-zero-trust-device-posture-rules  ZT posture rules"
                echo "cloudflare-zero-trust-edna-list   Zero Trust EDNA lists"
                ;;
                
            iam)
                echo -e "${BOLD}=== Terraform Modules - IAM ===${NC}"
                echo ""
                echo "iam-role-github-actions   GitHub Actions OIDC federation"
                echo "iam-role-datadog          Datadog integration role"
                echo "iam-role-vault            HashiCorp Vault role"
                echo "iam-role-packer           Packer image building"
                echo "iam-role-servicenow       ServiceNow integrations"
                echo "iam-role-prismacloud      Prisma Cloud security"
                echo "iam-role-splunk           Splunk logging"
                echo "iam-saml-adfs             SAML ADFS federation"
                echo "iam-shibboleth            Shibboleth federation"
                echo "github-oidc-provider      GitHub OIDC provider setup"
                echo "aws-identity-center-permission-set  AWS SSO permission sets"
                ;;
                
            observability|monitoring)
                echo -e "${BOLD}=== Terraform Modules - Observability ===${NC}"
                echo ""
                echo "cloudwatch-logs-to-datadog   CloudWatch to Datadog"
                echo "cloudwatch-logs-to-log-lake  CloudWatch to S3 data lake"
                echo "cloudwatch-to-splunk         CloudWatch to Splunk"
                echo "datadog-lambda-forwarder     Datadog Lambda forwarder"
                echo "datadog-logs-firehose-forwarder  Datadog Kinesis Firehose"
                echo "datadog-mule-monitors        MuleSoft Datadog monitors"
                echo "amazon-inspector             AWS Inspector config"
                ;;
                
            tags|tagging)
                echo -e "${BOLD}=== Terraform Modules - Tagging Standards ===${NC}"
                echo ""
                echo -e "${YELLOW}IMPORTANT: product-tags is MANDATORY for all resources${NC}"
                echo ""
                echo "product-tags              ASU standard tagging (REQUIRED)"
                echo "generate-tags             Tag generation utilities"
                echo "product-map               Product key to metadata mapping"
                echo ""
                echo -e "${BOLD}Required Tags:${NC}"
                echo "  ProductCategory, ProductFamily, ProductFamilyKey"
                echo "  Product, ProductKey"
                echo "  TechContact, AdminContact (ASURITE IDs)"
                echo "  env (infradev, sandbox, dev, qa, uat, test, scan, non-prod, prod)"
                echo ""
                echo "Tagging Standard Version: 2025.0.2"
                ;;
                
            *)
                error "Unknown type: $ptype. Use: compute, database, networking, kubernetes, cloudflare, iam, observability, tags"
                ;;
        esac
        return
    fi
    
    # Full overview
    echo -e "${BOLD}=== Design Pattern: ASU Terraform Modules ===${NC}"
    echo ""
    echo "Custom Terraform modules from dco-terraform hosted on JFrog Artifactory."
    echo "These are ASU-specific modules with built-in tagging standards, security"
    echo "configurations, and Ansible integration."
    echo ""
    
    echo -e "${BOLD}Registry:${NC}"
    echo "  jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform"
    echo ""
    
    echo -e "${BOLD}Module Source Pattern:${NC}"
    echo '  module "example" {'
    echo '    source  = "jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform/<module>/aws"'
    echo '    version = ">= 1.0"'
    echo '  }'
    echo ""
    
    echo -e "${BOLD}Module Categories:${NC}"
    echo "  compute      - EC2 (Linux, Windows, macOS), Nutanix VMs"
    echo "  database     - Aurora, RDS (MySQL, PostgreSQL, MSSQL, Oracle)"
    echo "  networking   - VPC, Security Groups, Route53"
    echo "  kubernetes   - EKS OIDC, Pod Identity, IRSA"
    echo "  cloudflare   - Tunnels, Access Apps, Zero Trust"
    echo "  iam          - GitHub Actions OIDC, Vault, Datadog, ServiceNow"
    echo "  observability - CloudWatch to Datadog/Splunk, Inspector"
    echo "  standards    - product-tags (MANDATORY)"
    echo ""
    
    echo -e "${BOLD}Custom Providers:${NC}"
    echo "  terraform-provider-edna - EDNA resource management"
    echo "  terraform-provider-mandiantasm - Security scanning"
    echo ""
    
    echo -e "${BOLD}Requirements:${NC}"
    echo "  Terraform: >= 1.5.6"
    echo "  AWS Provider: >= 5.82.0"
    echo ""
    
    echo -e "${BOLD}Related Commands:${NC}"
    echo "  discover.sh pattern --name terraform-modules --type compute"
    echo "  discover.sh pattern --name terraform-modules --type database"
    echo "  discover.sh pattern --name terraform-modules --type kubernetes"
    echo "  discover.sh pattern --name terraform-modules --type tags"
    echo "  discover.sh repos --domain terraform"
}

#
# Show Vault pattern details
#
show_pattern_vault() {
    local ptype="$1"
    
    if [[ -n "$ptype" ]]; then
        case "$ptype" in
            typescript|node|nodejs)
                echo -e "${BOLD}=== Vault - TypeScript/Node.js Patterns ===${NC}"
                echo ""
                echo -e "${YELLOW}RECOMMENDED: Use AWS SDK instead of direct Vault access${NC}"
                echo ""
                echo -e "${GREEN}AWS Secrets Manager (Preferred):${NC}"
                echo "  Package: @aws-sdk/client-secrets-manager"
                echo "  Example: ASU/lms-canvas-enrollment-system"
                echo ""
                echo "  import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';"
                echo ""
                echo "  const client = new SecretsManagerClient({ region: 'us-west-2' });"
                echo "  const secret = await client.send("
                echo "    new GetSecretValueCommand({ SecretId: 'my-secret' })"
                echo "  );"
                echo "  const data = JSON.parse(secret.SecretString!);"
                echo ""
                echo -e "${GREEN}SSM Parameter Store:${NC}"
                echo "  Package: @aws-sdk/client-ssm"
                echo "  Example: ASU/cremo-cmidp-course-requisite-api"
                echo ""
                echo "  import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';"
                echo ""
                echo "  const client = new SSMClient({ region: 'us-west-2' });"
                echo "  const param = await client.send("
                echo "    new GetParameterCommand({ Name: '/my/param', WithDecryption: true })"
                echo "  );"
                echo ""
                echo -e "${GREEN}Terraform Pattern (Vault → Secrets Manager):${NC}"
                echo "  Sync Vault secrets to AWS at deploy time"
                echo "  See: discover.sh pattern --name vault --type terraform"
                echo ""
                echo -e "${GREEN}Example Repos:${NC}"
                echo "  ASU/lms-canvas-enrollment-system"
                echo "  ASU/cremo-cmidp-course-requisite-api"
                echo "  ASU/iden-universal-service-provisioner"
                ;;
                
            python)
                echo -e "${BOLD}=== Vault - Python Patterns ===${NC}"
                echo ""
                echo -e "${GREEN}Token File Pattern:${NC}"
                echo "  Repo: ASU/edna-rmi-linux"
                echo "  Path: ansible/roles/edna/files/serviceConfigLookup.py"
                echo ""
                echo "  import hvac"
                echo "  import boto3"
                echo ""
                echo "  # Read token from file"
                echo "  with open('/var/run/vault-token') as token:"
                echo "      TOKENVAL = token.read()"
                echo "  client = hvac.Client(url='https://ops-vault-prod.opsprod.asu.edu', token=TOKENVAL)"
                echo ""
                echo "  # Fallback: AWS IAM authentication"
                echo "  if not client.is_authenticated():"
                echo "      session = boto3.Session()"
                echo "      cred = session.get_credentials()"
                echo "      client.auth.aws.iam_login(cred.access_key, cred.secret_key, cred.token, role='...')"
                echo ""
                echo "  secret = client.secrets.kv.v1.read_secret(path='services/...')['data']"
                echo "  client.logout()"
                echo ""
                echo -e "${GREEN}Environment Variables Pattern:${NC}"
                echo "  Repo: ASU/oprah-product-map"
                echo "  Path: get_gdrive_sheet.py"
                echo ""
                echo "  import hvac"
                echo "  vault_client = hvac.Client()  # Uses VAULT_ADDR and VAULT_TOKEN"
                echo "  secret_data = vault_client.secrets.kv.v1.read_secret(path='...')"
                ;;
                
            terraform|tf)
                echo -e "${BOLD}=== Vault - Terraform Patterns ===${NC}"
                echo ""
                echo -e "${GREEN}Vault to AWS Secrets Manager:${NC}"
                echo "  Repo: ASU/wflow-kuali-approver-service"
                echo "  Path: terraform/secretsmanager.tf"
                echo ""
                echo '  data "vault_generic_secret" "api_key" {'
                echo '    path = "secret/services/dco/jenkins/wflow/kbapi/\${terraform.workspace}/kuali_api_key"'
                echo '  }'
                echo ""
                echo '  resource "aws_secretsmanager_secret" "api_key" {'
                echo '    name_prefix = "kuali-api-key-\${terraform.workspace}-"'
                echo '  }'
                echo ""
                echo '  resource "aws_secretsmanager_secret_version" "api_key" {'
                echo '    secret_id     = aws_secretsmanager_secret.api_key.id'
                echo '    secret_string = data.vault_generic_secret.api_key.data["api_key"]'
                echo '  }'
                echo ""
                echo -e "${GREEN}Vault to SSM Parameter Store:${NC}"
                echo "  Repo: ASU/iden-identity-resolution-service-api"
                echo "  Path: terraform/secrets.tf"
                echo ""
                echo '  resource "aws_ssm_parameter" "db" {'
                echo '    name  = "/iden/irs/\${terraform.workspace}/api/pscs/db"'
                echo '    type  = "SecureString"'
                echo '    value = data.vault_generic_secret.db.data_json'
                echo '  }'
                ;;
                
            auth)
                echo -e "${BOLD}=== Vault - Authentication Methods ===${NC}"
                echo ""
                echo -e "${GREEN}AppRole (Jenkins CI/CD):${NC}"
                echo "  TTL: 30 minutes"
                echo "  Example: ASU/caas-caas-vault → vault/approle-jenkins.tf"
                echo ""
                echo -e "${GREEN}AWS IAM (EC2/Lambda):${NC}"
                echo "  Cross-account STS roles for Vault authentication"
                echo "  Example: ASU/caas-caas-vault → vault/auth-aws.tf"
                echo ""
                echo -e "${GREEN}Kubernetes (EKS pods):${NC}"
                echo "  Native Kubernetes service account auth"
                echo "  Example: ASU/caas-caas-vault → vault/auth-iam-principals.tf"
                echo ""
                echo -e "${GREEN}OIDC (Human users):${NC}"
                echo "  OIDC via AWS Cognito integration"
                echo "  Example: ASU/caas-caas-vault → vault/oidc.tf"
                ;;
                
            jenkins)
                echo -e "${BOLD}=== Vault - Jenkins Functions ===${NC}"
                echo ""
                echo "From: ASU/devops-jenkins-pipeline-library/vars/"
                echo ""
                echo "vaultLogin()         - Login to Vault"
                echo "caasVaultLogin()     - Login to CaaS Vault"
                echo "opsVaultLogin()      - Login to Ops Vault"
                echo "getVaultSecret()     - Read secret from Vault"
                echo "getVaultToken()      - Get Vault token"
                echo "getVaultAppRoleToken() - Get token via AppRole"
                ;;
                
            *)
                error "Unknown type: $ptype. Use: typescript, python, terraform, auth, or jenkins"
                ;;
        esac
        return
    fi
    
    # Full overview
    echo -e "${BOLD}=== Design Pattern: HashiCorp Vault Secrets ===${NC}"
    echo ""
    echo "Patterns for accessing secrets from HashiCorp Vault and syncing to AWS."
    echo "ASU uses multiple Vault clusters (CaaS, DCO, Ops) with various auth"
    echo "methods including AppRole, AWS IAM, Kubernetes, and OIDC."
    echo ""
    
    echo -e "${BOLD}Vault Clusters:${NC}"
    echo "  CaaS Vault: vault.caas-{env}.asu.edu"
    echo "  Ops Vault:  ops-vault-prod.opsprod.asu.edu"
    echo ""
    
    echo -e "${BOLD}TypeScript/Node.js (RECOMMENDED):${NC}"
    echo "  Use AWS SDK: @aws-sdk/client-secrets-manager, @aws-sdk/client-ssm"
    echo "  Example: ASU/lms-canvas-enrollment-system"
    echo "  Sync Vault→AWS at deploy time via Terraform"
    echo ""
    
    echo -e "${BOLD}Python (hvac):${NC}"
    echo "  Token file: ASU/edna-rmi-linux → serviceConfigLookup.py"
    echo "  Env vars:   ASU/oprah-product-map → get_gdrive_sheet.py"
    echo ""
    
    echo -e "${BOLD}Terraform (vault_generic_secret):${NC}"
    echo "  To Secrets Manager: ASU/wflow-kuali-approver-service"
    echo "  To SSM:             ASU/iden-identity-resolution-service-api"
    echo ""
    
    echo -e "${BOLD}Authentication Methods:${NC}"
    echo "  AppRole    - Jenkins CI/CD (30 min TTL)"
    echo "  AWS IAM    - EC2/Lambda workloads"
    echo "  Kubernetes - EKS pods"
    echo "  OIDC       - Human users (via Cognito)"
    echo ""
    
    echo -e "${BOLD}Secret Path Convention:${NC}"
    echo "  secret/services/{org}/{team}/{app}/{environment}/{component}"
    echo ""
    
    echo -e "${BOLD}Jenkins Functions:${NC}"
    echo "  vaultLogin, getVaultSecret, getVaultToken, getVaultAppRoleToken"
    echo ""
    
    echo -e "${BOLD}Related Commands:${NC}"
    echo "  discover.sh pattern --name vault --type typescript"
    echo "  discover.sh pattern --name vault --type python"
    echo "  discover.sh pattern --name vault --type terraform"
    echo "  discover.sh pattern --name vault --type auth"
    echo "  discover.sh pattern --name vault --type jenkins"
    echo "  discover.sh repos --domain vault"
}

#
# Show Observability pattern details
#
show_pattern_observability() {
    local ptype="$1"
    
    if [[ -n "$ptype" ]]; then
        case "$ptype" in
            datadog)
                echo -e "${BOLD}=== Observability - Datadog ===${NC}"
                echo ""
                echo -e "${GREEN}TypeScript/Node.js APM:${NC}"
                echo "  Package: dd-trace"
                echo "  Example: ASU/lms-canvas-enrollment-system"
                echo ""
                echo "  import tracer from 'dd-trace';"
                echo "  tracer.init({ service: 'my-service' });"
                echo ""
                echo -e "${GREEN}TypeScript/React RUM:${NC}"
                echo "  Package: @datadog/browser-rum"
                echo "  Example: ASU/cremo-cmidp-course-requisite-api (frontend)"
                echo ""
                echo "  import { datadogRum } from '@datadog/browser-rum';"
                echo "  datadogRum.init({"
                echo "    applicationId: 'xxx',"
                echo "    clientToken: 'xxx',"
                echo "    site: 'datadoghq.com',"
                echo "    service: 'my-app',"
                echo "    env: process.env.NODE_ENV"
                echo "  });"
                echo ""
                echo -e "${GREEN}Python APM:${NC}"
                echo "  Package: ddtrace"
                echo "  Example: ASU/iden-universal-service-provisioner"
                echo ""
                echo "  from ddtrace import tracer"
                echo "  @tracer.wrap(service='my-service')"
                echo "  def my_function():"
                echo "      pass"
                echo ""
                echo -e "${GREEN}Java APM:${NC}"
                echo "  Agent: dd-java-agent.jar"
                echo "  Example: ASU/edna"
                echo ""
                echo "  java -javaagent:/path/to/dd-java-agent.jar \\"
                echo "       -Ddd.service=my-service \\"
                echo "       -Ddd.env=prod \\"
                echo "       -jar app.jar"
                echo ""
                echo -e "${GREEN}Jenkins Deployment Events:${NC}"
                echo "  Function: datadogDeployment()"
                echo "  Repo: ASU/devops-jenkins-pipeline-library"
                echo ""
                echo "  datadogDeployment("
                echo "    serviceName: 'my-service',"
                echo "    env: 'prod'"
                echo "  )"
                ;;
                
            logging-lake|cribl|logging)
                echo -e "${BOLD}=== Observability - Logging Lake (RECOMMENDED) ===${NC}"
                echo ""
                echo -e "${YELLOW}This is the RECOMMENDED destination for all logs.${NC}"
                echo ""
                echo -e "${GREEN}Architecture:${NC}"
                echo "  Cribl Stream (EKS) → S3 → OpenSearch"
                echo "  OSIS (OpenSearch Ingestion Service) pipelines"
                echo ""
                echo -e "${GREEN}Key Repositories:${NC}"
                echo "  Platform:     ASU/eli5-observability-pipeline-platform"
                echo "  Kafka Bridge: ASU/eli5-kafkabahn"
                echo "  OSIS:         ASU/eli5-osis-pipelines"
                echo ""
                echo -e "${GREEN}Team Prefix:${NC} eli5"
                echo ""
                echo -e "${GREEN}Terraform Modules:${NC}"
                echo "  cloudwatch-logs-to-log-lake  - CloudWatch to S3 data lake"
                echo "  cloudflare-zone-logpush-logging-lake - Cloudflare to data lake"
                echo ""
                echo -e "${GREEN}Migration from Splunk:${NC}"
                echo "  1. Update log shippers to point to Cribl"
                echo "  2. Use OSIS pipelines for OpenSearch ingestion"
                echo "  3. Decommission Splunk forwarders"
                ;;
                
            cloudwatch)
                echo -e "${BOLD}=== Observability - CloudWatch ===${NC}"
                echo ""
                echo -e "${GREEN}CloudWatch Alarm Patterns:${NC}"
                echo "  Lambda errors, API Gateway 5xx, ECS task failures"
                echo ""
                echo -e "${GREEN}Routing Options:${NC}"
                echo "  To Datadog:      cloudwatch-logs-to-datadog"
                echo "  To Logging Lake: cloudwatch-logs-to-log-lake"
                echo "  To Splunk:       cloudwatch-to-splunk ${YELLOW}(DEPRECATED)${NC}"
                echo ""
                echo -e "${GREEN}Terraform Modules:${NC}"
                echo "  Source: jfrog-cloud.devops.asu.edu/asu-terraform-modules__dco-terraform"
                echo ""
                echo "  cloudwatch-logs-to-datadog"
                echo "  cloudwatch-logs-to-log-lake"
                echo "  datadog-lambda-forwarder"
                echo "  datadog-logs-firehose-forwarder"
                ;;
                
            opentelemetry|otel)
                echo -e "${BOLD}=== Observability - OpenTelemetry ===${NC}"
                echo ""
                echo -e "${GREEN}Architecture:${NC}"
                echo "  K8s OTEL Collector → OSIS → OpenSearch"
                echo ""
                echo -e "${GREEN}Use Cases:${NC}"
                echo "  - Kubernetes workloads on EKS"
                echo "  - Vendor-neutral instrumentation"
                echo "  - Custom metrics and traces"
                echo ""
                echo -e "${GREEN}Integration Points:${NC}"
                echo "  - OSIS pipelines (ASU/eli5-osis-pipelines)"
                echo "  - OpenSearch dashboards"
                echo ""
                echo -e "${GREEN}Note:${NC}"
                echo "  For APM, Datadog is preferred for most use cases."
                echo "  Use OTEL when vendor neutrality is required."
                ;;
                
            splunk)
                echo -e "${BOLD}=== Observability - Splunk (DEPRECATED) ===${NC}"
                echo ""
                echo -e "${YELLOW}⚠️  SPLUNK IS DEPRECATED${NC}"
                echo ""
                echo "Splunk is being phased out at ASU."
                echo "All new implementations MUST use Logging Lake instead."
                echo ""
                echo -e "${BOLD}Migration Path:${NC}"
                echo "  FROM: Splunk Universal Forwarder / HEC"
                echo "  TO:   Cribl Stream → S3 → OpenSearch"
                echo ""
                echo -e "${BOLD}Steps to Migrate:${NC}"
                echo "  1. Identify current Splunk sources"
                echo "  2. Configure Cribl Stream inputs"
                echo "  3. Update Terraform to use cloudwatch-logs-to-log-lake"
                echo "  4. Migrate dashboards to OpenSearch"
                echo "  5. Decommission Splunk forwarders"
                echo ""
                echo -e "${BOLD}Contact:${NC}"
                echo "  Team: eli5 (Enterprise Logging Infrastructure)"
                echo "  Repo: ASU/eli5-observability-pipeline-platform"
                echo ""
                echo -e "${BOLD}Recommended:${NC}"
                echo "  discover.sh pattern --name observability --type logging-lake"
                ;;
                
            *)
                error "Unknown type: $ptype. Use: datadog, logging-lake, cloudwatch, opentelemetry, or splunk"
                ;;
        esac
        return
    fi
    
    # Full overview
    echo -e "${BOLD}=== Design Pattern: Observability Stack ===${NC}"
    echo ""
    echo "ASU's observability stack for monitoring, logging, and tracing."
    echo "Primary tools: Datadog (APM/RUM), Cribl/Logging Lake (logs),"
    echo "CloudWatch (AWS metrics), OpenTelemetry (K8s)."
    echo ""
    echo -e "${YELLOW}⚠️  Splunk is DEPRECATED - use Logging Lake instead${NC}"
    echo ""
    
    echo -e "${BOLD}Datadog (APM & RUM):${NC}"
    echo "  TypeScript: dd-trace, @datadog/browser-rum"
    echo "  Python:     ddtrace"
    echo "  Java:       dd-java-agent.jar"
    echo "  Jenkins:    datadogDeployment()"
    echo ""
    
    echo -e "${BOLD}Logging Lake (RECOMMENDED for logs):${NC}"
    echo "  Platform:   Cribl Stream on EKS"
    echo "  Storage:    S3 → OpenSearch"
    echo "  Team:       eli5"
    echo "  Repos:      eli5-observability-pipeline-platform, eli5-kafkabahn"
    echo ""
    
    echo -e "${BOLD}CloudWatch:${NC}"
    echo "  Alarms:     Lambda errors, API Gateway 5xx, ECS failures"
    echo "  Routing:    To Datadog or Logging Lake"
    echo ""
    
    echo -e "${BOLD}OpenTelemetry:${NC}"
    echo "  K8s:        OTEL Collector → OSIS → OpenSearch"
    echo "  Use when:   Vendor neutrality required"
    echo ""
    
    echo -e "${BOLD}Terraform Modules:${NC}"
    echo "  cloudwatch-logs-to-datadog"
    echo "  cloudwatch-logs-to-log-lake"
    echo "  datadog-lambda-forwarder"
    echo "  datadog-logs-firehose-forwarder"
    echo ""
    
    echo -e "${BOLD}Related Commands:${NC}"
    echo "  discover.sh pattern --name observability --type datadog"
    echo "  discover.sh pattern --name observability --type logging-lake"
    echo "  discover.sh pattern --name observability --type cloudwatch"
    echo "  discover.sh pattern --name observability --type opentelemetry"
    echo "  discover.sh pattern --name observability --type splunk"
}

#
# Show generic pattern details (fallback)
#
show_pattern_generic() {
    local pattern="$1"
    local ptype="$2"
    
    local pattern_name
    pattern_name=$(yaml_get_pattern_simple "$DOMAINS_FILE" "$pattern" "name")
    
    echo -e "${BOLD}=== Design Pattern: $pattern_name ===${NC}"
    echo ""
    
    # Description
    local desc
    desc=$(yaml_get_pattern_field "$DOMAINS_FILE" "$pattern" "description" | head -5)
    echo "$desc"
    echo ""
    
    # When to use
    echo -e "${BOLD}When to use:${NC}"
    yaml_get_pattern_field "$DOMAINS_FILE" "$pattern" "when_to_use" | grep "^- " | while read -r line; do
        echo "  $line"
    done
}

#
# ACTION: Expand (debug)
#
action_expand() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    echo "=== Query Expansion Debug ==="
    echo ""
    echo "Original query: $QUERY"
    echo ""
    
    local detected_domains
    detected_domains=$(detect_domains "$QUERY")
    echo "Detected domains: ${detected_domains:-none}"
    echo ""
    
    if [[ -n "$detected_domains" ]]; then
        echo "Synonyms by domain:"
        for domain in $detected_domains; do
            echo "  [$domain]"
            yaml_get_domain_field "$DOMAINS_FILE" "$domain" "synonyms" 2>/dev/null | head -8 | while read -r syn; do
                echo "    - $syn"
            done
        done
        echo ""
        
        local expanded
        expanded=$(expand_query "$QUERY" "$detected_domains")
        echo "Expanded query:"
        echo "  $expanded"
        echo ""
        
        local lang_hint
        lang_hint=$(get_language_hints "$detected_domains")
        echo "Language hint: ${lang_hint:-none}"
        echo ""
        
        echo "Team prefixes:"
        for domain in $detected_domains; do
            local prefixes
            prefixes=$(yaml_get_prefixes "$DOMAINS_FILE" "$domain" | tr '\n' ', ' | sed 's/,$//')
            [[ -n "$prefixes" ]] && echo "  $domain: $prefixes"
        done
        echo ""
        
        echo "Known repos:"
        get_domain_repos "$detected_domains" | while read -r repo; do
            echo "  - ASU/$repo"
        done
    fi
}

#
# ACTION: DNS Validate - Validate domain and show provider recommendation
#
action_dns_validate() {
    [[ -z "${DOMAIN:-}" ]] && error "Missing --domain. Usage: dns-validate --domain <domain>"
    
    # Use dns.sh functions if available
    if type show_recommendation &>/dev/null; then
        show_recommendation "$DOMAIN" "${CHECK_DNS:-false}"
    else
        # Fallback inline implementation
        local provider
        if [[ "$DOMAIN" =~ \.asu\.edu$ ]]; then
            provider="infoblox"
        else
            provider="cloudflare"
        fi
        
        echo "Domain: $DOMAIN"
        echo "Provider: $provider"
        echo ""
        
        case "$provider" in
            infoblox)
                echo "Configuration:"
                echo "  Server: dnsadmin.asu.edu"
                echo "  Views: default, external"
                echo "  Vault Path: secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
                echo ""
                echo "Resources:"
                echo "  - infoblox_a_record"
                echo "  - infoblox_cname_record"
                ;;
            cloudflare)
                echo "Configuration:"
                echo "  Action: Register domain + configure DNS"
                echo "  Vault Path: secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
                echo ""
                echo "Resources:"
                echo "  - cloudflare_record"
                echo "  - cloudflare_zone"
                ;;
        esac
        
        # Check DNS if requested
        if [[ "${CHECK_DNS:-false}" == "true" ]]; then
            echo ""
            local result
            result=$(dig +short "$DOMAIN" 2>/dev/null)
            if [[ -n "$result" ]]; then
                echo "DNS Status: EXISTS"
                echo "=== DNS Records for $DOMAIN ==="
                local a_records=$(dig +short A "$DOMAIN" 2>/dev/null)
                [[ -n "$a_records" ]] && echo "A Records:" && echo "$a_records" | sed 's/^/  /'
                local cname_records=$(dig +short CNAME "$DOMAIN" 2>/dev/null)
                [[ -n "$cname_records" ]] && echo "CNAME Records:" && echo "$cname_records" | sed 's/^/  /'
            else
                echo "DNS Status: NOT FOUND (domain does not resolve)"
            fi
        fi
    fi
}

#
# ACTION: DNS Scaffold - Generate Terraform scaffolding for DNS records
#
action_dns_scaffold() {
    [[ -z "${DOMAIN:-}" ]] && error "Missing --domain. Usage: dns-scaffold --domain <domain> [--type a|cname] [--target <target>]"
    
    local record_type="${TYPE:-cname}"
    local target="${TARGET:-}"
    local pattern="${PATTERN:-}"
    local origin="${ORIGIN:-}"
    local include_vault="${INCLUDE_VAULT:-true}"
    
    # Determine provider from domain
    local provider
    if [[ "$DOMAIN" =~ \.asu\.edu$ ]]; then
        provider="infoblox"
    else
        provider="cloudflare"
    fi
    
    # Generate resource name from domain
    local name
    name=$(echo "$DOMAIN" | tr '.' '_' | tr '-' '_')
    
    # Use dns.sh functions if available
    if type scaffold_vault_secrets &>/dev/null; then
        # Output Vault secrets if requested
        if [[ "$include_vault" == "true" ]]; then
            echo "# Vault secrets for $provider provider"
            if [[ "$pattern" == "hybrid" ]]; then
                scaffold_vault_secrets "both"
            else
                scaffold_vault_secrets "$provider"
            fi
            echo ""
        fi
        
        # Generate based on pattern/provider
        if [[ "$pattern" == "hybrid" ]]; then
            local subdomain="${DOMAIN%.asu.edu}"
            [[ -z "$origin" ]] && error "Missing --origin for hybrid pattern"
            scaffold_hybrid "$name" "$subdomain" "$origin"
        elif [[ "$provider" == "infoblox" ]]; then
            for view in default external; do
                echo "# DNS View: $view"
                if [[ "$record_type" == "a" ]]; then
                    scaffold_infoblox_a "${name}_${view}" "$DOMAIN" "$target" "$view"
                else
                    scaffold_infoblox_cname "${name}_${view}" "$DOMAIN" "$target" "$view"
                fi
                echo ""
            done
        else
            if [[ "$record_type" == "a" ]]; then
                scaffold_cloudflare_a "$name" "$DOMAIN" "$target"
            else
                scaffold_cloudflare_cname "$name" "$DOMAIN" "$target"
            fi
        fi
    else
        # Fallback: Show inline code examples
        echo "# DNS Scaffolding for $DOMAIN (provider: $provider)"
        echo "# Note: Install dns.sh for template-based scaffolding"
        echo ""
        
        if [[ "$provider" == "infoblox" ]]; then
            cat << EOF
# Vault secrets for Infoblox
data "vault_generic_secret" "infoblox" {
  path = "secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
}

# Infoblox ${record_type^^} record - default view
resource "infoblox_${record_type}_record" "${name}_internal" {
  dns_view  = "default"
EOF
            if [[ "$record_type" == "a" ]]; then
                echo "  fqdn     = \"$DOMAIN\""
                echo "  ip_addr  = \"${target:-<IP_ADDRESS>}\""
            else
                echo "  alias     = \"$DOMAIN\""
                echo "  canonical = \"${target:-<TARGET_HOSTNAME>}\""
            fi
            cat << EOF
  comment   = "Managed by Terraform"
}

# Infoblox ${record_type^^} record - external view
resource "infoblox_${record_type}_record" "${name}_external" {
  dns_view  = "external"
EOF
            if [[ "$record_type" == "a" ]]; then
                echo "  fqdn     = \"$DOMAIN\""
                echo "  ip_addr  = \"${target:-<IP_ADDRESS>}\""
            else
                echo "  alias     = \"$DOMAIN\""
                echo "  canonical = \"${target:-<TARGET_HOSTNAME>}\""
            fi
            echo "  comment   = \"Managed by Terraform\""
            echo "}"
        else
            cat << EOF
# Vault secrets for Cloudflare
data "vault_generic_secret" "cloudflare" {
  path = "secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
}

# Cloudflare ${record_type^^} record
resource "cloudflare_record" "${name}" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "$DOMAIN"
  value   = "${target:-<TARGET_VALUE>}"
  type    = "${record_type^^}"
  proxied = true
}
EOF
        fi
    fi
}

#
# ACTION: DNS Examples - Show example repos using DNS patterns
#
action_dns_examples() {
    local pattern="${PATTERN:-all}"
    
    # Use dns.sh functions if available
    if type show_dns_examples &>/dev/null; then
        show_dns_examples "$pattern"
    else
        # Fallback inline implementation
        echo "=== Example Repos for DNS Pattern: $pattern ==="
        echo ""
        
        case "$pattern" in
            infoblox)
                echo "Infoblox DNS Examples:"
                echo "  ASU/sso-shibboleth      - Hybrid Infoblox+Cloudflare pattern"
                echo "  ASU/hosting-fse         - Infoblox CNAME with for_each"
                echo "  ASU/ewp-www-farm-acquia - Infoblox A and CNAME records"
                echo "  ASU/hosting-cronkite    - infoblox-cname-record module"
                echo "  ASU/xreal-xr-at-asu-portal - Infoblox integration"
                echo ""
                echo "Module Source:"
                echo "  ASU/dns-infoblox        - Infoblox Terraform configurations"
                ;;
            cloudflare)
                echo "Cloudflare DNS Examples:"
                echo "  ASU/sso-shibboleth      - Cloudflare proxied records"
                echo ""
                echo "Available Cloudflare Modules:"
                echo "  - cloudflare-tunnel"
                echo "  - cloudflare-tunnel-route53-dns"
                echo "  - cloudflare-access-app"
                echo "  - cloudflare-origin-ca-certificate"
                ;;
            hybrid)
                echo "Hybrid Pattern Examples (Infoblox -> Cloudflare CDN -> Origin):"
                echo "  ASU/sso-shibboleth      - Full hybrid pattern implementation"
                echo ""
                echo "Pattern Flow:"
                echo "  1. Infoblox CNAME (default + external views) -> Cloudflare CDN"
                echo "  2. Cloudflare proxied record -> Origin server"
                ;;
            all|*)
                echo "All DNS Patterns:"
                echo ""
                echo "Infoblox (*.asu.edu):"
                echo "  ASU/hosting-fse, ASU/ewp-www-farm-acquia, ASU/hosting-cronkite"
                echo ""
                echo "Cloudflare (external domains):"
                echo "  ASU/sso-shibboleth"
                echo ""
                echo "Hybrid (ASU domain + Cloudflare CDN):"
                echo "  ASU/sso-shibboleth"
                echo ""
                echo "Module Sources:"
                echo "  ASU/dns-infoblox"
                ;;
        esac
    fi
}

#
# Show DNS design pattern details
#
show_pattern_dns() {
    local ptype="${1:-}"
    
    echo -e "${BOLD}=== Design Pattern: DNS Configuration (Infoblox + Cloudflare) ===${NC}"
    echo ""
    echo "DNS management patterns for ASU infrastructure using Terraform."
    echo ""
    echo -e "${BOLD}Routing Rules:${NC}"
    echo "  *.asu.edu domains   → Infoblox (dnsadmin.asu.edu)"
    echo "  External domains    → Cloudflare (registration + DNS)"
    echo "  ASU + CDN/WAF       → Hybrid (Infoblox → Cloudflare → Origin)"
    echo ""
    
    case "$ptype" in
        infoblox)
            echo -e "${BOLD}=== Infoblox Configuration ===${NC}"
            echo ""
            echo "Server: dnsadmin.asu.edu"
            echo "Views: default (internal), external (public)"
            echo "Vault: secret/services/dco/jenkins/dco/jenkins/prod/kerberos/principals/jenkins_app"
            echo ""
            echo -e "${BOLD}Resources:${NC}"
            echo "  - infoblox_a_record"
            echo "  - infoblox_cname_record"
            echo ""
            echo -e "${BOLD}Example:${NC}"
            cat << 'EOF'
resource "infoblox_cname_record" "myapp_internal" {
  dns_view  = "default"
  alias     = "myapp.asu.edu"
  canonical = "myapp-origin.aws.amazon.com"
  comment   = "Managed by Terraform"
}

resource "infoblox_cname_record" "myapp_external" {
  dns_view  = "external"
  alias     = "myapp.asu.edu"
  canonical = "myapp-origin.aws.amazon.com"
  comment   = "Managed by Terraform"
}
EOF
            ;;
        cloudflare)
            echo -e "${BOLD}=== Cloudflare Configuration ===${NC}"
            echo ""
            echo "Use for: Non-ASU domain registration and DNS"
            echo "Vault: secret/services/dco/jenkins/ewp/cloudflare/prod/api/principals/asu-jenkins-devops"
            echo ""
            echo -e "${BOLD}Resources:${NC}"
            echo "  - cloudflare_record"
            echo "  - cloudflare_zone"
            echo ""
            echo -e "${BOLD}Modules:${NC}"
            echo "  - cloudflare-tunnel"
            echo "  - cloudflare-tunnel-route53-dns"
            echo "  - cloudflare-access-app"
            echo "  - cloudflare-origin-ca-certificate"
            echo ""
            echo -e "${BOLD}Example:${NC}"
            cat << 'EOF'
resource "cloudflare_record" "myapp" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "www"
  value   = "myapp-origin.aws.amazon.com"
  type    = "CNAME"
  proxied = true
}
EOF
            ;;
        hybrid)
            echo -e "${BOLD}=== Hybrid Pattern (Infoblox → Cloudflare CDN → Origin) ===${NC}"
            echo ""
            echo "Use when: ASU domain needs Cloudflare CDN/WAF protection"
            echo ""
            echo "Flow:"
            echo "  User → myapp.asu.edu (Infoblox) → Cloudflare CDN → Origin"
            echo ""
            echo -e "${BOLD}Example:${NC}"
            cat << 'EOF'
# Step 1: Infoblox CNAMEs pointing to Cloudflare CDN
resource "infoblox_cname_record" "myapp_internal" {
  dns_view  = "default"
  alias     = "myapp.asu.edu"
  canonical = "myapp.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN"
}

resource "infoblox_cname_record" "myapp_external" {
  dns_view  = "external"
  alias     = "myapp.asu.edu"
  canonical = "myapp.asu.edu.cdn.cloudflare.net"
  comment   = "Points to Cloudflare CDN"
}

# Step 2: Cloudflare proxied record to origin
resource "cloudflare_record" "myapp" {
  zone_id = data.vault_generic_secret.cloudflare.data["zone_id"]
  name    = "myapp.asu.edu"
  value   = "myapp-origin.aws.amazon.com"
  type    = "CNAME"
  proxied = true
}
EOF
            ;;
        *)
            echo -e "${BOLD}Providers:${NC}"
            echo ""
            echo "  Infoblox (*.asu.edu):"
            echo "    Server: dnsadmin.asu.edu"
            echo "    Views: default, external"
            echo "    Resources: infoblox_a_record, infoblox_cname_record"
            echo ""
            echo "  Cloudflare (external):"
            echo "    Resources: cloudflare_record, cloudflare_zone"
            echo "    Modules: cloudflare-tunnel, cloudflare-access-app"
            echo ""
            echo -e "${BOLD}Example Repos:${NC}"
            echo "  ASU/sso-shibboleth      - Hybrid Infoblox+Cloudflare"
            echo "  ASU/hosting-fse         - Infoblox CNAME with for_each"
            echo "  ASU/dns-infoblox        - Infoblox module source"
            echo ""
            echo -e "${BOLD}Commands:${NC}"
            echo "  discover.sh dns-validate --domain myapp.asu.edu"
            echo "  discover.sh dns-scaffold --domain myapp.asu.edu --type cname --target cdn.example.com"
            echo "  discover.sh dns-scaffold --domain myapp.asu.edu --pattern hybrid --origin origin.aws.com"
            echo ""
            echo -e "${BOLD}Related Commands:${NC}"
            echo "  discover.sh pattern --name dns --type infoblox"
            echo "  discover.sh pattern --name dns --type cloudflare"
            echo "  discover.sh pattern --name dns --type hybrid"
            ;;
    esac
}

#
# Main
#
main() {
    [[ $# -eq 0 ]] && usage
    
    # Check domains.yaml exists
    [[ ! -f "$DOMAINS_FILE" ]] && error "domains.yaml not found at $DOMAINS_FILE"
    
    local action="$1"; shift
    
    # Handle index subcommands
    if [[ "$action" == "index" ]]; then
        local subaction="${1:-stats}"
        [[ $# -gt 0 ]] && shift
        
        case "$subaction" in
            build) action_index_build ;;
            refresh) action_index_refresh ;;
            stats) action_index_stats ;;
            verify) action_index_verify "$@" ;;
            classify) 
                ensure_index
                action_index_classify_internal
                success "Domain classification complete"
                ;;
            *) error "Unknown index subcommand: $subaction. Use: build, refresh, stats, verify, classify" ;;
        esac
        return
    fi
    
    parse_args "$@"
    
    case "$action" in
        search) action_search ;;
        code) action_code ;;
        repos) action_repos ;;
        context) action_context ;;
        patterns) action_patterns ;;
        pattern) action_pattern ;;
        expand) action_expand ;;
        dns-validate) action_dns_validate ;;
        dns-scaffold) action_dns_scaffold ;;
        dns-examples) action_dns_examples ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action. Use --help for usage." ;;
    esac
}

main "$@"
