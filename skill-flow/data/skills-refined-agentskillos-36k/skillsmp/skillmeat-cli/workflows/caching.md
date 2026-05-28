# Caching Integration

Multi-layer caching strategy for artifact metadata, search results, and confidence scores to optimize performance and minimize API calls.

---

## Overview

SkillMeat uses a hierarchical caching system to optimize performance across all workflows:

**Cache Layers**:
1. **Artifact Metadata Cache** (24h TTL) - GitHub API responses
2. **Search Results Cache** (5m TTL) - Query result sets
3. **Confidence Scores Cache** (1h TTL) - Match API scores
4. **Project Analysis Cache** (5m TTL) - Context analysis

**Performance Benefits**:
- Search: <100ms (cached) vs ~1s (uncached)
- Match API: <50ms (cached) vs ~500ms (uncached)
- GitHub API: Avoid rate limits (5,000/hour authenticated)
- Project analysis: <50ms (cached) vs ~500ms (uncached)

**Storage Locations**:
```
~/.skillmeat/
├── cache/
│   ├── artifacts/          # Metadata cache (persistent)
│   ├── search/             # Search results (persistent)
│   ├── scores/             # Confidence scores (persistent)
│   └── cache.db            # SQLite cache index
└── collection/
    └── manifest.toml       # Collection state
```

---

## Layer 1: Artifact Metadata Cache

Caches GitHub API responses to avoid rate limits and improve performance.

### Configuration

```bash
# Default TTL: 24 hours
skillmeat cache config --ttl-artifacts 48h

# View current config
skillmeat cache stats
```

**Cache Key Structure**:
```
<source>/<name>/<version>
# Examples:
anthropics/skills/canvas-design/latest
anthropics/skills/canvas-design/v2.1.0
anthropics/skills/canvas-design/abc123
```

### Storage Format

**File**: `~/.skillmeat/cache/artifacts/<hash>.json`

```json
{
  "cache_version": "1.0.0",
  "cached_at": "2024-12-24T10:00:00Z",
  "ttl_seconds": 86400,
  "source": "anthropics/skills/canvas-design",
  "version_spec": "latest",
  "metadata": {
    "name": "canvas-design",
    "type": "skill",
    "description": "Create and edit designs in canvas mode",
    "resolved_sha": "abc123def456...",
    "resolved_version": "v2.1.0",
    "github_stars": 42,
    "last_updated": "2024-12-01T00:00:00Z",
    "readme_content": "...",
    "file_structure": {
      "SKILL.md": 7543,
      "scripts/": ["process.js", "validate.js"],
      "templates/": ["base.md"]
    }
  }
}
```

### Cache Operations

#### Write to Cache

```javascript
// After successful GitHub API call
async function cacheArtifactMetadata(source, version, metadata) {
  const cacheKey = `${source}/${version}`;
  const hash = await hashKey(cacheKey);
  const cachePath = path.join(CACHE_DIR, 'artifacts', `${hash}.json`);

  const cacheEntry = {
    cache_version: '1.0.0',
    cached_at: new Date().toISOString(),
    ttl_seconds: 86400,  // 24 hours
    source,
    version_spec: version,
    metadata,
  };

  await fs.writeFile(cachePath, JSON.stringify(cacheEntry, null, 2));
}
```

#### Read from Cache

```javascript
async function getArtifactMetadata(source, version) {
  const cacheKey = `${source}/${version}`;
  const hash = await hashKey(cacheKey);
  const cachePath = path.join(CACHE_DIR, 'artifacts', `${hash}.json`);

  try {
    const content = await fs.readFile(cachePath, 'utf-8');
    const entry = JSON.parse(content);

    // Check TTL
    const age = Date.now() - new Date(entry.cached_at).getTime();
    if (age > entry.ttl_seconds * 1000) {
      console.warn('[Cache] Artifact metadata expired, fetching fresh...');
      return null;
    }

    return entry.metadata;
  } catch (err) {
    if (err.code === 'ENOENT') {
      return null;  // Cache miss
    }
    throw err;
  }
}
```

### Invalidation Rules

**Automatic Invalidation**:
- TTL expiration (24h default)
- Version change (e.g., `latest` resolves to new SHA)

**Manual Invalidation**:
```bash
# Clear all artifact metadata
skillmeat cache clear --type artifacts

# Clear specific artifact
skillmeat cache clear --artifact anthropics/skills/canvas-design

# Force refresh on sync
skillmeat sync --no-cache
```

**When to Bypass**:
```bash
# Always fetch fresh metadata
skillmeat add anthropics/skills/canvas-design --no-cache
skillmeat search "pdf" --fresh
```

---

## Layer 2: Search Results Cache

Caches search query results to accelerate repeated searches.

### Configuration

```bash
# Default TTL: 5 minutes
skillmeat cache config --ttl-search 10m

# Disable search cache
skillmeat cache config --ttl-search 0
```

**Cache Key Structure**:
```
<query_hash>_<filters_hash>
# Examples:
sha256("pdf processing")_sha256({"type":"skill"})
sha256("database")_sha256({"type":"skill","category":"backend"})
```

### Storage Format

**File**: `~/.skillmeat/cache/search/<hash>.json`

```json
{
  "cache_version": "1.0.0",
  "cached_at": "2024-12-24T10:05:00Z",
  "ttl_seconds": 300,
  "query": "pdf processing",
  "filters": {
    "type": "skill",
    "category": null
  },
  "results": [
    {
      "name": "processing-pdfs",
      "source": "anthropics/skills/processing-pdfs",
      "type": "skill",
      "score": 0.95,
      "match_type": "semantic"
    },
    {
      "name": "docx",
      "source": "anthropics/skills/document-skills/docx",
      "type": "skill",
      "score": 0.72,
      "match_type": "keyword"
    }
  ],
  "result_count": 2
}
```

### Cache Operations

#### Write to Cache

```javascript
async function cacheSearchResults(query, filters, results) {
  const queryHash = await hashKey(query);
  const filtersHash = await hashKey(JSON.stringify(filters || {}));
  const cacheKey = `${queryHash}_${filtersHash}`;
  const cachePath = path.join(CACHE_DIR, 'search', `${cacheKey}.json`);

  const cacheEntry = {
    cache_version: '1.0.0',
    cached_at: new Date().toISOString(),
    ttl_seconds: 300,  // 5 minutes
    query,
    filters,
    results,
    result_count: results.length,
  };

  await fs.writeFile(cachePath, JSON.stringify(cacheEntry, null, 2));
}
```

#### Read from Cache

```javascript
async function getSearchResults(query, filters = {}) {
  const queryHash = await hashKey(query);
  const filtersHash = await hashKey(JSON.stringify(filters));
  const cacheKey = `${queryHash}_${filtersHash}`;
  const cachePath = path.join(CACHE_DIR, 'search', `${cacheKey}.json`);

  try {
    const content = await fs.readFile(cachePath, 'utf-8');
    const entry = JSON.parse(content);

    // Check TTL
    const age = Date.now() - new Date(entry.cached_at).getTime();
    if (age > entry.ttl_seconds * 1000) {
      return null;  // Cache expired
    }

    return entry.results;
  } catch (err) {
    if (err.code === 'ENOENT') {
      return null;  // Cache miss
    }
    throw err;
  }
}
```

### Invalidation Rules

**Automatic Invalidation**:
- TTL expiration (5m default)
- Collection manifest change (new artifact added)

**Manual Invalidation**:
```bash
# Clear all search results
skillmeat cache clear --type search

# Clear specific query
skillmeat cache clear --query "pdf processing"
```

**When to Bypass**:
```bash
# Force fresh search
skillmeat search "pdf" --no-cache

# Bypass in discovery workflow
skillmeat match "pdf processing" --fresh
```

### Integration with Discovery Workflow

```javascript
// scripts/discovery-search.js
async function executeSearch(query, filters) {
  // Try cache first
  const cached = await getSearchResults(query, filters);
  if (cached) {
    console.log('[Cache] Using cached search results');
    return cached;
  }

  // Cache miss - execute search
  console.log('[Search] Executing fresh search...');
  const results = await performSearch(query, filters);

  // Write to cache
  await cacheSearchResults(query, filters, results);

  return results;
}
```

---

## Layer 3: Confidence Scores Cache

Caches Match API responses to minimize external API calls.

### Configuration

```bash
# Default TTL: 1 hour
skillmeat cache config --ttl-scores 2h

# View cache stats
skillmeat cache stats --scores
```

**Cache Key Structure**:
```
<query_hash>_<context_hash>
# Examples:
sha256("pdf processing")_sha256({"project":"react-app"})
sha256("database")_sha256({"project":"backend-api"})
```

### Storage Format

**File**: `~/.skillmeat/cache/scores/<hash>.json`

```json
{
  "cache_version": "1.0.0",
  "cached_at": "2024-12-24T10:10:00Z",
  "ttl_seconds": 3600,
  "query": "pdf processing",
  "context": {
    "project_path": "/path/to/project",
    "project_type": "react",
    "dependencies": ["react", "typescript"]
  },
  "scores": [
    {
      "artifact": "processing-pdfs",
      "confidence": 0.95,
      "components": {
        "trust": 0.92,
        "quality": 0.96,
        "relevance": 0.97
      },
      "match_type": "semantic"
    },
    {
      "artifact": "docx",
      "confidence": 0.72,
      "components": {
        "trust": 0.85,
        "quality": 0.78,
        "relevance": 0.65
      },
      "match_type": "keyword"
    }
  ]
}
```

### Cache Operations

#### Write to Cache

```javascript
async function cacheConfidenceScores(query, context, scores) {
  const queryHash = await hashKey(query);
  const contextHash = await hashKey(JSON.stringify(context || {}));
  const cacheKey = `${queryHash}_${contextHash}`;
  const cachePath = path.join(CACHE_DIR, 'scores', `${cacheKey}.json`);

  const cacheEntry = {
    cache_version: '1.0.0',
    cached_at: new Date().toISOString(),
    ttl_seconds: 3600,  // 1 hour
    query,
    context,
    scores,
  };

  await fs.writeFile(cachePath, JSON.stringify(cacheEntry, null, 2));
}
```

#### Read from Cache

```javascript
async function getConfidenceScores(query, context = {}) {
  const queryHash = await hashKey(query);
  const contextHash = await hashKey(JSON.stringify(context));
  const cacheKey = `${queryHash}_${contextHash}`;
  const cachePath = path.join(CACHE_DIR, 'scores', `${cacheKey}.json`);

  try {
    const content = await fs.readFile(cachePath, 'utf-8');
    const entry = JSON.parse(content);

    // Check TTL
    const age = Date.now() - new Date(entry.cached_at).getTime();
    if (age > entry.ttl_seconds * 1000) {
      return null;  // Cache expired
    }

    return entry.scores;
  } catch (err) {
    if (err.code === 'ENOENT') {
      return null;  // Cache miss
    }
    throw err;
  }
}
```

### Invalidation Rules

**Automatic Invalidation**:
- TTL expiration (1h default)
- User rating change (affects trust score)

**Manual Invalidation**:
```bash
# Clear all confidence scores
skillmeat cache clear --type scores

# Clear specific query
skillmeat cache clear --query "pdf processing"

# Clear after rating artifact
skillmeat rate canvas-design 5  # Auto-invalidates scores cache
```

**When to Bypass**:
```bash
# Force fresh scoring
skillmeat match "pdf" --no-cache

# Always fresh in confidence workflow
skillmeat scores refresh canvas-design
```

### Integration with Confidence Workflow

```javascript
// scripts/confidence-scoring.js
async function getConfidenceScore(query, artifact, context) {
  // Try cache first
  const cached = await getConfidenceScores(query, context);
  if (cached) {
    const score = cached.find(s => s.artifact === artifact);
    if (score) {
      console.log('[Cache] Using cached confidence score');
      return score;
    }
  }

  // Cache miss - call Match API
  console.log('[Match] Fetching fresh confidence score...');
  const score = await callMatchAPI(query, artifact, context);

  // Write to cache (store all scores for this query)
  const allScores = cached || [];
  allScores.push(score);
  await cacheConfidenceScores(query, context, allScores);

  return score;
}
```

---

## Layer 4: Project Analysis Cache

In-memory cache for project context analysis (used in context boosting).

### Configuration

**TTL**: 5 minutes (in-memory only, cleared on process exit)

**Cache Key**: `<project_path>_<mtime>`
- `project_path`: Absolute path to project root
- `mtime`: Latest modification time of analyzed files

### Storage Format

**In-Memory Map**:
```javascript
const projectCache = new Map();

// Key: hash of (path + mtime)
// Value: {
//   timestamp: Date.now(),
//   data: {
//     project_type: "react",
//     dependencies: [...],
//     file_types: {...},
//     patterns: [...]
//   }
// }
```

### Cache Operations

#### Write to Cache

```javascript
// scripts/analyze-project.js
const CACHE_TTL = 5 * 60 * 1000;  // 5 minutes
const cache = new Map();

async function analyzeProjectCached(projectPath) {
  const cacheKey = await getCacheKey(projectPath);
  const cached = cache.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    console.log('[Cache] Using cached project analysis');
    return cached.data;
  }

  console.log('[Analysis] Analyzing project structure...');
  const analysis = await analyzeProject(projectPath);

  cache.set(cacheKey, {
    timestamp: Date.now(),
    data: analysis,
  });

  return analysis;
}

async function getCacheKey(projectPath) {
  // Hash of path + latest mtime
  const stats = await fs.stat(projectPath);
  const mtime = stats.mtimeMs;
  return hashKey(`${projectPath}_${mtime}`);
}
```

#### Read from Cache

```javascript
// Automatic in analyzeProjectCached()
// Cache is checked before analysis
```

### Invalidation Rules

**Automatic Invalidation**:
- TTL expiration (5m)
- File modification (mtime change)
- Process exit (in-memory only)

**Manual Invalidation**:
```javascript
// Clear specific project
cache.delete(await getCacheKey(projectPath));

// Clear all
cache.clear();
```

**No CLI command** - in-memory cache is automatic.

### Integration with Context Boosting

```javascript
// workflows/context-boosting.md example
async function getProjectContext(projectPath) {
  // Cache hit/miss handled automatically
  const context = await analyzeProjectCached(projectPath);

  return {
    project_type: context.project_type,
    dependencies: context.dependencies,
    recent_changes: await getRecentChanges(projectPath),
  };
}
```

---

## Cache Management CLI

### View Cache Statistics

```bash
# Overall stats
skillmeat cache stats

# Output:
# Cache Statistics
# ================
# Artifacts:  142 entries (3.2 MB)
# Search:     28 entries (140 KB)
# Scores:     64 entries (256 KB)
# Total:      234 entries (3.6 MB)
#
# Hit Rate (last 24h):
# Artifacts:  87% (142/163)
# Search:     93% (28/30)
# Scores:     78% (64/82)

# Type-specific stats
skillmeat cache stats --type artifacts
skillmeat cache stats --type search
skillmeat cache stats --type scores
```

### Clear Cache

```bash
# Clear all cache
skillmeat cache clear

# Clear specific type
skillmeat cache clear --type artifacts
skillmeat cache clear --type search
skillmeat cache clear --type scores

# Clear specific artifact
skillmeat cache clear --artifact anthropics/skills/canvas-design

# Clear specific query
skillmeat cache clear --query "pdf processing"

# Confirm before clearing
skillmeat cache clear --confirm
```

### Configure Cache

```bash
# Set TTL for artifact metadata
skillmeat cache config --ttl-artifacts 48h
skillmeat cache config --ttl-artifacts 0  # Disable

# Set TTL for search results
skillmeat cache config --ttl-search 10m
skillmeat cache config --ttl-search 0  # Disable

# Set TTL for confidence scores
skillmeat cache config --ttl-scores 2h
skillmeat cache config --ttl-scores 0  # Disable

# View current config
skillmeat cache config --show
```

### Prune Expired Entries

```bash
# Remove expired entries (automatic on startup)
skillmeat cache prune

# Force prune all expired
skillmeat cache prune --force
```

---

## Cache Bypass Options

All commands that use caching support `--no-cache` or `--fresh` flags:

```bash
# Search without cache
skillmeat search "pdf" --no-cache
skillmeat search "pdf" --fresh  # Alias

# Match without cache
skillmeat match "pdf processing" --no-cache

# Add artifact without metadata cache
skillmeat add anthropics/skills/canvas-design --no-cache

# Sync without cache
skillmeat sync --no-cache

# Scores without cache
skillmeat scores refresh canvas-design --no-cache
```

**When to Use**:
- Testing new artifact versions
- Debugging search/match issues
- After manual collection changes
- When suspecting stale cache

---

## Performance Optimization Patterns

### Pattern 1: Warm Cache on Startup

```javascript
// Warm cache with frequently used artifacts
async function warmCache() {
  const popular = ['canvas-design', 'processing-pdfs', 'docx'];

  for (const name of popular) {
    const metadata = await getArtifactMetadata(`anthropics/skills/${name}`, 'latest');
    if (!metadata) {
      await fetchAndCacheMetadata(`anthropics/skills/${name}`, 'latest');
    }
  }
}
```

### Pattern 2: Prefetch Related Artifacts

```javascript
// When user searches for "pdf", prefetch common related artifacts
async function prefetchRelated(query) {
  const related = getRelatedQueries(query);  // ["docx", "document", "text"]

  // Prefetch in background (don't await)
  related.forEach(async (relatedQuery) => {
    const cached = await getSearchResults(relatedQuery);
    if (!cached) {
      performSearch(relatedQuery).then(results =>
        cacheSearchResults(relatedQuery, {}, results)
      );
    }
  });
}
```

### Pattern 3: Adaptive TTL

```javascript
// Adjust TTL based on artifact popularity
async function adaptiveCacheTTL(artifact) {
  const usage = await getArtifactUsage(artifact);

  if (usage.access_count > 100) {
    return 48 * 3600;  // 48 hours for popular artifacts
  } else if (usage.access_count > 10) {
    return 24 * 3600;  // 24 hours for moderate
  } else {
    return 12 * 3600;  // 12 hours for rare
  }
}
```

### Pattern 4: Cache Warming After Collection Change

```javascript
// After adding new artifact, warm related caches
async function onArtifactAdded(artifact) {
  // Invalidate search cache (collection changed)
  await invalidateSearchCache();

  // Warm cache for new artifact
  await fetchAndCacheMetadata(artifact.source, artifact.version);

  // Prefetch common searches
  await warmSearchCache(['pdf', 'document', artifact.category]);
}
```

---

## Integration with Workflows

### Discovery Workflow

```javascript
// Step 2: Execute search with caching
async function executeDiscoverySearch(query, filters) {
  // 1. Check search cache
  const cachedResults = await getSearchResults(query, filters);
  if (cachedResults) {
    console.log('[Cache] Using cached search results (5m TTL)');
    return cachedResults;
  }

  // 2. Execute search
  const results = await performSearch(query, filters);

  // 3. Cache results
  await cacheSearchResults(query, filters, results);

  return results;
}
```

### Confidence Integration

```javascript
// Step 3: Calculate confidence with caching
async function calculateConfidence(query, artifact, context) {
  // 1. Check scores cache
  const cachedScores = await getConfidenceScores(query, context);
  if (cachedScores) {
    const score = cachedScores.find(s => s.artifact === artifact);
    if (score) {
      console.log('[Cache] Using cached confidence score (1h TTL)');
      return score;
    }
  }

  // 2. Call Match API
  const score = await callMatchAPI(query, artifact, context);

  // 3. Cache score
  await cacheConfidenceScores(query, context, [score]);

  return score;
}
```

### Context Boosting

```javascript
// Get project context with in-memory caching
async function getProjectContext(projectPath) {
  // In-memory cache (5m TTL, automatic invalidation on file change)
  const context = await analyzeProjectCached(projectPath);

  return {
    project_type: context.project_type,
    dependencies: context.dependencies,
    file_types: context.file_types,
    patterns: context.patterns,
  };
}
```

---

## Cache Maintenance Best Practices

### Regular Cleanup

```bash
# Monthly cleanup (add to cron)
0 0 1 * * skillmeat cache prune --force

# Weekly stats review
0 0 * * 0 skillmeat cache stats
```

### Monitor Hit Rates

```bash
# Check cache effectiveness
skillmeat cache stats

# If hit rate < 70%, consider:
# 1. Increasing TTL
skillmeat cache config --ttl-search 15m

# 2. Warming cache on startup
# 3. Adjusting invalidation rules
```

### Disk Space Management

```bash
# Check cache size
du -sh ~/.skillmeat/cache/

# Clear if > 100 MB
if [ $(du -sm ~/.skillmeat/cache/ | cut -f1) -gt 100 ]; then
  skillmeat cache clear --type search
  skillmeat cache prune --force
fi
```

---

## Troubleshooting

### Stale Cache Issues

**Symptom**: Search returns outdated results after adding new artifact

**Fix**:
```bash
# Clear search cache
skillmeat cache clear --type search

# Or force fresh search
skillmeat search "pdf" --no-cache
```

### High Cache Miss Rate

**Symptom**: Cache stats show <50% hit rate

**Diagnosis**:
```bash
# Check TTL settings
skillmeat cache config --show

# Review query patterns
skillmeat cache stats --verbose
```

**Fix**:
```bash
# Increase TTL if queries are similar
skillmeat cache config --ttl-search 15m

# Add cache warming for common queries
```

### Cache Corruption

**Symptom**: Invalid JSON errors when reading cache

**Fix**:
```bash
# Clear corrupted cache type
skillmeat cache clear --type artifacts

# Or clear all
skillmeat cache clear
```

### GitHub Rate Limit Despite Cache

**Symptom**: Rate limit errors even with artifact cache

**Diagnosis**:
```bash
# Check artifact cache hit rate
skillmeat cache stats --type artifacts
```

**Fix**:
```bash
# Increase artifact TTL
skillmeat cache config --ttl-artifacts 72h

# Always use cache for list operations
skillmeat list --cached-only
```

---

## Token Efficiency Metrics

### With Full Caching (Optimal)

```
Operation: skillmeat search "pdf processing"
├── Search cache hit: <1ms
├── Artifact metadata cache hit: <1ms per artifact
├── No GitHub API calls
└── Total: ~50ms, ~500 tokens
```

### With Partial Caching

```
Operation: skillmeat search "pdf processing"
├── Search cache miss: ~500ms
├── Artifact metadata cache hit: <1ms per artifact
├── Match API call: ~300ms
└── Total: ~800ms, ~2KB tokens
```

### No Caching (Cold Start)

```
Operation: skillmeat search "pdf processing"
├── Search execution: ~500ms
├── GitHub API calls: ~2s (rate limited)
├── Match API call: ~300ms
├── Project analysis: ~500ms
└── Total: ~3.3s, ~8KB tokens
```

**Cache Effectiveness**: 95% time reduction, 94% token reduction

---

## Future Enhancements

### Phase 4+ Improvements

1. **Distributed Cache**: Redis/Memcached for multi-user environments
2. **Smart Prefetching**: ML-based prediction of user queries
3. **Cache Compression**: LZ4 compression for large metadata
4. **Cache Analytics**: Detailed hit/miss analysis dashboard
5. **CDN Integration**: Serve common artifacts from CDN with aggressive caching

### Proposed Features

```bash
# Export cache to share with team
skillmeat cache export --output cache-snapshot.tar.gz

# Import shared cache
skillmeat cache import cache-snapshot.tar.gz

# Cache warming from usage logs
skillmeat cache warm --from-logs ~/.skillmeat/usage.log

# Smart cache eviction (LRU, LFU)
skillmeat cache config --eviction-policy lru --max-size 500MB
```

---

## Reference

**Related Workflows**:
- Discovery Workflow: Uses search + artifact cache
- Confidence Integration: Uses scores cache
- Context Boosting: Uses project analysis cache
- Error Handling: Cache invalidation on errors

**CLI Commands**:
- `skillmeat cache stats` - View cache statistics
- `skillmeat cache clear` - Clear cache entries
- `skillmeat cache config` - Configure cache settings
- `skillmeat cache prune` - Remove expired entries

**Configuration Files**:
- `~/.skillmeat/cache/cache.db` - SQLite cache index
- `~/.skillmeat/cache/*/` - Cache entry files
- `~/.skillmeat/config.toml` - Cache TTL settings
