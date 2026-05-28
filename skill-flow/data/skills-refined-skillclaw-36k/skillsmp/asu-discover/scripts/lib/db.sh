#!/usr/bin/env bash
#
# db.sh - SQLite Helper Functions for ASU Discover
# Provides database operations for repo indexing and caching
#

# Database location
DB_DIR="${DB_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/data}"
DB_FILE="${DB_FILE:-$DB_DIR/asu-repos.db}"

# Ensure sqlite3 is available
command -v sqlite3 >/dev/null 2>&1 || { echo "Error: sqlite3 is required" >&2; exit 1; }

#
# Initialize the database schema
#
db_init() {
    mkdir -p "$DB_DIR"
    
    sqlite3 "$DB_FILE" <<'SQL'
-- Repos table
CREATE TABLE IF NOT EXISTS repos (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL UNIQUE,
    description TEXT,
    language TEXT,
    prefix TEXT,
    pushed_at TEXT,
    stars INTEGER DEFAULT 0,
    visibility TEXT DEFAULT 'private',
    archived INTEGER DEFAULT 0,
    topics TEXT,
    created_at TEXT,
    updated_at TEXT
);

-- FTS5 virtual table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS repos_fts USING fts5(
    name, 
    description, 
    language, 
    prefix,
    topics,
    content='repos',
    content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS repos_ai AFTER INSERT ON repos BEGIN
    INSERT INTO repos_fts(rowid, name, description, language, prefix, topics)
    VALUES (new.id, new.name, new.description, new.language, new.prefix, new.topics);
END;

CREATE TRIGGER IF NOT EXISTS repos_ad AFTER DELETE ON repos BEGIN
    INSERT INTO repos_fts(repos_fts, rowid, name, description, language, prefix, topics)
    VALUES ('delete', old.id, old.name, old.description, old.language, old.prefix, old.topics);
END;

CREATE TRIGGER IF NOT EXISTS repos_au AFTER UPDATE ON repos BEGIN
    INSERT INTO repos_fts(repos_fts, rowid, name, description, language, prefix, topics)
    VALUES ('delete', old.id, old.name, old.description, old.language, old.prefix, old.topics);
    INSERT INTO repos_fts(rowid, name, description, language, prefix, topics)
    VALUES (new.id, new.name, new.description, new.language, new.prefix, new.topics);
END;

-- Domains table
CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    priority INTEGER DEFAULT 0
);

-- Repo-to-domain mapping
CREATE TABLE IF NOT EXISTS repo_domains (
    repo_id INTEGER NOT NULL,
    domain_id INTEGER NOT NULL,
    confidence REAL DEFAULT 1.0,
    PRIMARY KEY (repo_id, domain_id),
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE,
    FOREIGN KEY (domain_id) REFERENCES domains(id) ON DELETE CASCADE
);

-- Code search cache (24h TTL)
CREATE TABLE IF NOT EXISTS search_cache (
    query_hash TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    results TEXT,
    result_count INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL
);

-- Index metadata
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_repos_prefix ON repos(prefix);
CREATE INDEX IF NOT EXISTS idx_repos_language ON repos(language);
CREATE INDEX IF NOT EXISTS idx_repos_pushed ON repos(pushed_at);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON search_cache(expires_at);
SQL
}

#
# Execute a SQL statement (no results)
#
db_exec() {
    sqlite3 "$DB_FILE" "$1"
}

#
# Query with results (tab-separated)
#
db_query() {
    sqlite3 -separator $'\t' "$DB_FILE" "$1"
}

#
# Query with JSON output
#
db_query_json() {
    sqlite3 -json "$DB_FILE" "$1"
}

#
# Check if database exists and is initialized
#
db_exists() {
    [[ -f "$DB_FILE" ]] && sqlite3 "$DB_FILE" "SELECT 1 FROM repos LIMIT 1" >/dev/null 2>&1
}

#
# Get metadata value
#
db_get_meta() {
    local key="$1"
    db_query "SELECT value FROM metadata WHERE key = '$key'" 2>/dev/null || echo ""
}

#
# Set metadata value
#
db_set_meta() {
    local key="$1" value="$2"
    db_exec "INSERT OR REPLACE INTO metadata (key, value) VALUES ('$key', '$value')"
}

#
# Escape string for SQL (double single quotes)
#
sql_escape() {
    printf '%s' "$1" | sed "s/'/''/g"
}

#
# Upsert a repository
# Arguments: name full_name description language pushed_at stars visibility archived topics
#
db_upsert_repo() {
    local name="$1"
    local full_name="$2"
    local description="$3"
    local language="$4"
    local pushed_at="$5"
    local stars="${6:-0}"
    local visibility="${7:-private}"
    local archived="${8:-0}"
    local topics="$9"
    
    # Escape strings for SQL
    name=$(sql_escape "$name")
    full_name=$(sql_escape "$full_name")
    description=$(sql_escape "$description")
    language=$(sql_escape "$language")
    topics=$(sql_escape "$topics")
    
    # Extract prefix from name (first segment before -)
    local prefix=""
    if [[ "$name" == *-* ]]; then
        prefix="${name%%-*}"
    fi
    
    db_exec "INSERT INTO repos (name, full_name, description, language, prefix, pushed_at, stars, visibility, archived, topics, updated_at)
             VALUES ('$name', '$full_name', '$description', '$language', '$prefix', '$pushed_at', $stars, '$visibility', $archived, '$topics', datetime('now'))
             ON CONFLICT(full_name) DO UPDATE SET
                description = excluded.description,
                language = excluded.language,
                prefix = excluded.prefix,
                pushed_at = excluded.pushed_at,
                stars = excluded.stars,
                visibility = excluded.visibility,
                archived = excluded.archived,
                topics = excluded.topics,
                updated_at = datetime('now')"
}

#
# Search repos using FTS5
# Returns: id, name, full_name, description, language, prefix
#
db_search_repos() {
    local query="$1"
    local limit="${2:-50}"
    
    # Escape special FTS5 characters
    query="${query//\"/\"\"}"
    
    db_query "SELECT r.id, r.name, r.full_name, r.description, r.language, r.prefix
              FROM repos r
              JOIN repos_fts f ON r.id = f.rowid
              WHERE repos_fts MATCH '\"$query\"'
              ORDER BY r.pushed_at DESC
              LIMIT $limit"
}

#
# Search repos with simpler LIKE fallback
#
db_search_repos_like() {
    local query="$1"
    local limit="${2:-50}"
    
    query="${query//\'/\'\'}"
    
    db_query "SELECT id, name, full_name, description, language, prefix
              FROM repos
              WHERE name LIKE '%$query%' 
                 OR description LIKE '%$query%'
                 OR topics LIKE '%$query%'
              ORDER BY pushed_at DESC
              LIMIT $limit"
}

#
# Get repos by prefix
#
db_get_repos_by_prefix() {
    local prefix="$1"
    local limit="${2:-50}"
    
    db_query "SELECT id, name, full_name, description, language
              FROM repos
              WHERE prefix = '$prefix'
              ORDER BY pushed_at DESC
              LIMIT $limit"
}

#
# Get repos by domain
#
db_get_repos_by_domain() {
    local domain="$1"
    local limit="${2:-50}"
    
    db_query "SELECT r.id, r.name, r.full_name, r.description, r.language
              FROM repos r
              JOIN repo_domains rd ON r.id = rd.repo_id
              JOIN domains d ON rd.domain_id = d.id
              WHERE d.name = '$domain'
              ORDER BY rd.confidence DESC, r.pushed_at DESC
              LIMIT $limit"
}

#
# Get or create domain ID
#
db_get_domain_id() {
    local domain="$1"
    local priority="${2:-0}"
    
    # Try to get existing
    local id
    id=$(db_query "SELECT id FROM domains WHERE name = '$domain'" 2>/dev/null)
    
    if [[ -z "$id" ]]; then
        db_exec "INSERT INTO domains (name, priority) VALUES ('$domain', $priority)"
        id=$(db_query "SELECT id FROM domains WHERE name = '$domain'")
    fi
    
    echo "$id"
}

#
# Link repo to domain
#
db_link_repo_domain() {
    local repo_id="$1"
    local domain="$2"
    local confidence="${3:-1.0}"
    
    local domain_id
    domain_id=$(db_get_domain_id "$domain")
    
    db_exec "INSERT OR REPLACE INTO repo_domains (repo_id, domain_id, confidence)
             VALUES ($repo_id, $domain_id, $confidence)"
}

#
# Cache Operations
#

# Hash a query for cache key
cache_hash() {
    echo -n "$1" | shasum -a 256 | cut -d' ' -f1
}

# Get cached search results (returns empty if expired)
cache_get() {
    local query="$1"
    local hash
    hash=$(cache_hash "$query")
    local now
    now=$(date +%s)
    
    db_query "SELECT results FROM search_cache 
              WHERE query_hash = '$hash' AND expires_at > $now" 2>/dev/null
}

# Set cache entry (24h TTL by default)
cache_set() {
    local query="$1"
    local results="$2"
    local ttl_seconds="${3:-86400}"  # 24 hours default
    
    local hash
    hash=$(cache_hash "$query")
    local now
    now=$(date +%s)
    local expires=$((now + ttl_seconds))
    local count
    count=$(echo "$results" | jq 'length' 2>/dev/null || echo "0")
    
    # Escape for SQL
    results="${results//\'/\'\'}"
    
    db_exec "INSERT OR REPLACE INTO search_cache (query_hash, query, results, result_count, created_at, expires_at)
             VALUES ('$hash', '$query', '$results', $count, $now, $expires)"
}

# Clear expired cache entries
cache_cleanup() {
    local now
    now=$(date +%s)
    db_exec "DELETE FROM search_cache WHERE expires_at < $now"
}

# Get cache stats
cache_stats() {
    local now
    now=$(date +%s)
    
    echo "=== Cache Statistics ==="
    db_query "SELECT 
                COUNT(*) as total_entries,
                SUM(CASE WHEN expires_at > $now THEN 1 ELSE 0 END) as valid_entries,
                SUM(CASE WHEN expires_at <= $now THEN 1 ELSE 0 END) as expired_entries
              FROM search_cache"
}

#
# Index Statistics
#
db_stats() {
    echo "=== Repository Index Statistics ==="
    echo ""
    
    echo "Total repos: $(db_query "SELECT COUNT(*) FROM repos")"
    echo "Last updated: $(db_get_meta 'last_index_update')"
    echo ""
    
    echo "By Language (top 10):"
    db_query "SELECT language, COUNT(*) as count 
              FROM repos 
              WHERE language IS NOT NULL AND language != ''
              GROUP BY language 
              ORDER BY count DESC 
              LIMIT 10" | while IFS=$'\t' read -r lang count; do
        printf "  %-20s %s\n" "$lang" "$count"
    done
    echo ""
    
    echo "By Prefix (top 15):"
    db_query "SELECT prefix, COUNT(*) as count 
              FROM repos 
              WHERE prefix IS NOT NULL AND prefix != ''
              GROUP BY prefix 
              ORDER BY count DESC 
              LIMIT 15" | while IFS=$'\t' read -r prefix count; do
        printf "  %-15s %s\n" "$prefix" "$count"
    done
    echo ""
    
    echo "By Domain:"
    db_query "SELECT d.name, COUNT(rd.repo_id) as count
              FROM domains d
              LEFT JOIN repo_domains rd ON d.id = rd.domain_id
              GROUP BY d.name
              ORDER BY count DESC" | while IFS=$'\t' read -r domain count; do
        printf "  %-20s %s\n" "$domain" "$count"
    done
}

#
# Rate limit tracking for code search (10 req/min)
#
RATE_LIMIT_FILE="$DB_DIR/.rate_limit"

rate_limit_check() {
    local min_interval=6  # 6 seconds = 10 req/min
    
    if [[ -f "$RATE_LIMIT_FILE" ]]; then
        local last_request
        last_request=$(cat "$RATE_LIMIT_FILE")
        local now
        now=$(date +%s)
        local elapsed=$((now - last_request))
        
        if [[ $elapsed -lt $min_interval ]]; then
            local wait_time=$((min_interval - elapsed))
            echo "$wait_time"  # Return seconds to wait
            return 1
        fi
    fi
    
    echo "0"
    return 0
}

rate_limit_update() {
    date +%s > "$RATE_LIMIT_FILE"
}

rate_limit_wait() {
    local wait_time
    wait_time=$(rate_limit_check)
    
    if [[ "$wait_time" -gt 0 ]]; then
        echo "Rate limit: waiting ${wait_time}s..." >&2
        sleep "$wait_time"
    fi
    
    rate_limit_update
}

# ==============================================================================
# Dynamic Count Functions (for avoiding hardcoded values)
# ==============================================================================

#
# Get total repository count from index
# Usage: get_repo_count [--active|--archived|--all]
#
get_repo_count() {
    local filter="${1:---all}"
    
    case "$filter" in
        --active)
            sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM repos WHERE archived = 0;" 2>/dev/null || echo "0"
            ;;
        --archived)
            sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM repos WHERE archived = 1;" 2>/dev/null || echo "0"
            ;;
        --all|*)
            sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM repos;" 2>/dev/null || echo "0"
            ;;
    esac
}

#
# Get last indexed timestamp
# Usage: get_last_indexed [--human|--epoch]
#
get_last_indexed() {
    local format="${1:---human}"
    local epoch
    
    epoch=$(sqlite3 "$DB_FILE" "SELECT value FROM metadata WHERE key='last_indexed';" 2>/dev/null)
    
    if [[ -z "$epoch" ]]; then
        echo "never"
        return 1
    fi
    
    case "$format" in
        --epoch)
            echo "$epoch"
            ;;
        --human|*)
            date -r "$epoch" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$epoch"
            ;;
    esac
}

#
# Get index statistics
# Usage: get_index_stats
#
get_index_stats() {
    local total active archived domains last_indexed
    
    total=$(get_repo_count --all)
    active=$(get_repo_count --active)
    archived=$(get_repo_count --archived)
    domains=$(sqlite3 "$DB_FILE" "SELECT COUNT(DISTINCT name) FROM domains;" 2>/dev/null || echo "0")
    last_indexed=$(get_last_indexed --human || true)
    
    echo "Repositories: $total ($active active, $archived archived)"
    echo "Domains: $domains"
    echo "Last indexed: $last_indexed"
}

#
# Get prefix statistics
# Usage: get_prefix_stats [--limit N]
#
get_prefix_stats() {
    local limit="${1:-10}"
    
    sqlite3 -separator $'\t' "$DB_FILE" "
        SELECT prefix, COUNT(*) as count 
        FROM repos 
        WHERE prefix IS NOT NULL AND prefix != ''
        GROUP BY prefix 
        ORDER BY count DESC 
        LIMIT $limit;" 2>/dev/null | while IFS=$'\t' read -r prefix count; do
        printf "  %-15s %s\n" "$prefix" "$count"
    done
}

#
# Verify if a repository exists
# Usage: verify_repo <full_name>
# Returns: 0 if exists, 1 if not
#
verify_repo() {
    local full_name="$1"
    gh repo view "$full_name" &>/dev/null
    return $?
}

#
# Verify all referenced repositories in a file
# Usage: verify_repos_in_file <file> [--fix]
#
verify_repos_in_file() {
    local file="$1"
    local fix="${2:-}"
    local refs total=0 valid=0 invalid=0
    
    # Extract ASU/repo-name references
    refs=$(grep -oE 'ASU/[a-zA-Z0-9_-]+' "$file" 2>/dev/null | sort -u)
    
    for repo in $refs; do
        ((total++))
        if verify_repo "$repo"; then
            ((valid++))
        else
            echo "INVALID: $repo"
            ((invalid++))
        fi
    done
    
    echo ""
    echo "Total: $total, Valid: $valid, Invalid: $invalid"
    
    [[ $invalid -eq 0 ]]
}
