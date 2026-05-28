---
name: caching-architecture
description: LiteLLM-RS Caching Architecture. Covers Redis caching, vector database semantic caching, multi-tier cache strategy, TTL management, and cache invalidation patterns.
---

# Caching Architecture Guide

## Overview

LiteLLM-RS implements a multi-tier caching system with Redis for exact-match caching and vector databases for semantic caching, optimizing both latency and cost.

### Cache Tiers

```
┌─────────────────────────────────────────────────────────────────┐
│                       Request                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    L1: In-Memory Cache                          │
│  - LRU eviction                                                 │
│  - Microsecond latency                                          │
│  - Limited size (~10K entries)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │ Miss
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    L2: Redis Cache                              │
│  - Exact match on request hash                                  │
│  - Millisecond latency                                          │
│  - TTL-based expiration                                         │
└─────────────────────────────────────────────────────────────────┘
                              │ Miss
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 L3: Semantic Cache (Vector DB)                  │
│  - Similarity search on embeddings                              │
│  - Configurable similarity threshold                            │
│  - Qdrant/Weaviate/Pinecone backends                           │
└─────────────────────────────────────────────────────────────────┘
                              │ Miss
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Provider                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cache Key Generation

### Request Hashing

```rust
use sha2::{Sha256, Digest};
use serde::Serialize;

pub struct CacheKeyGenerator;

impl CacheKeyGenerator {
    /// Generate a deterministic cache key from a chat request
    pub fn generate_key(request: &ChatRequest) -> String {
        let mut hasher = Sha256::new();

        // Include model
        hasher.update(request.model.as_bytes());

        // Include messages (normalized)
        for message in &request.messages {
            hasher.update(message.role.to_string().as_bytes());
            if let Some(content) = &message.content {
                hasher.update(content.to_string().as_bytes());
            }
        }

        // Include relevant parameters
        if let Some(temp) = request.temperature {
            hasher.update(temp.to_le_bytes());
        }
        if let Some(top_p) = request.top_p {
            hasher.update(top_p.to_le_bytes());
        }
        if let Some(max_tokens) = request.max_tokens {
            hasher.update(max_tokens.to_le_bytes());
        }

        // Include tools if present
        if let Some(tools) = &request.tools {
            let tools_json = serde_json::to_string(tools).unwrap_or_default();
            hasher.update(tools_json.as_bytes());
        }

        let result = hasher.finalize();
        format!("chat:{}", hex::encode(result))
    }

    /// Generate a semantic cache key (for vector lookup)
    pub fn generate_semantic_key(request: &ChatRequest) -> String {
        // Extract the last user message for semantic matching
        let user_message = request
            .messages
            .iter()
            .rev()
            .find(|m| m.role == MessageRole::User)
            .and_then(|m| m.content.as_ref())
            .map(|c| c.to_string())
            .unwrap_or_default();

        format!("semantic:{}:{}", request.model, user_message)
    }
}
```

---

## In-Memory Cache (L1)

### LRU Cache Implementation

```rust
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use linked_hash_map::LinkedHashMap;

pub struct InMemoryCache {
    cache: RwLock<LinkedHashMap<String, CacheEntry>>,
    max_size: usize,
    stats: CacheStats,
}

#[derive(Clone)]
struct CacheEntry {
    value: Vec<u8>,
    expires_at: Option<Instant>,
    created_at: Instant,
}

impl InMemoryCache {
    pub fn new(max_size: usize) -> Self {
        Self {
            cache: RwLock::new(LinkedHashMap::new()),
            max_size,
            stats: CacheStats::default(),
        }
    }

    pub fn get(&self, key: &str) -> Option<Vec<u8>> {
        let mut cache = self.cache.write().unwrap();

        if let Some(entry) = cache.get_refresh(key) {
            // Check expiration
            if let Some(expires_at) = entry.expires_at {
                if Instant::now() > expires_at {
                    cache.remove(key);
                    self.stats.misses.fetch_add(1, Ordering::Relaxed);
                    return None;
                }
            }

            self.stats.hits.fetch_add(1, Ordering::Relaxed);
            return Some(entry.value.clone());
        }

        self.stats.misses.fetch_add(1, Ordering::Relaxed);
        None
    }

    pub fn set(&self, key: String, value: Vec<u8>, ttl: Option<Duration>) {
        let mut cache = self.cache.write().unwrap();

        // Evict if at capacity
        while cache.len() >= self.max_size {
            cache.pop_front();
            self.stats.evictions.fetch_add(1, Ordering::Relaxed);
        }

        let entry = CacheEntry {
            value,
            expires_at: ttl.map(|t| Instant::now() + t),
            created_at: Instant::now(),
        };

        cache.insert(key, entry);
    }

    pub fn invalidate(&self, key: &str) {
        let mut cache = self.cache.write().unwrap();
        cache.remove(key);
    }

    pub fn clear(&self) {
        let mut cache = self.cache.write().unwrap();
        cache.clear();
    }
}
```

---

## Redis Cache (L2)

### Redis Cache Manager

```rust
use redis::{AsyncCommands, Client, aio::ConnectionManager};

pub struct RedisCache {
    client: ConnectionManager,
    prefix: String,
    default_ttl: Duration,
}

impl RedisCache {
    pub async fn new(redis_url: &str, prefix: &str) -> Result<Self, CacheError> {
        let client = Client::open(redis_url)
            .map_err(|e| CacheError::Connection(e.to_string()))?;

        let manager = ConnectionManager::new(client)
            .await
            .map_err(|e| CacheError::Connection(e.to_string()))?;

        Ok(Self {
            client: manager,
            prefix: prefix.to_string(),
            default_ttl: Duration::from_secs(3600),
        })
    }

    fn prefixed_key(&self, key: &str) -> String {
        format!("{}:{}", self.prefix, key)
    }

    pub async fn get(&self, key: &str) -> Result<Option<Vec<u8>>, CacheError> {
        let mut conn = self.client.clone();
        let prefixed = self.prefixed_key(key);

        let result: Option<Vec<u8>> = conn
            .get(&prefixed)
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(result)
    }

    pub async fn set(&self, key: &str, value: &[u8], ttl: Option<Duration>) -> Result<(), CacheError> {
        let mut conn = self.client.clone();
        let prefixed = self.prefixed_key(key);
        let ttl = ttl.unwrap_or(self.default_ttl);

        conn.set_ex(&prefixed, value, ttl.as_secs() as usize)
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(())
    }

    pub async fn delete(&self, key: &str) -> Result<(), CacheError> {
        let mut conn = self.client.clone();
        let prefixed = self.prefixed_key(key);

        conn.del(&prefixed)
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(())
    }

    pub async fn get_json<T: serde::de::DeserializeOwned>(&self, key: &str) -> Result<Option<T>, CacheError> {
        let bytes = self.get(key).await?;

        match bytes {
            Some(b) => {
                let value = serde_json::from_slice(&b)
                    .map_err(|e| CacheError::Serialization(e.to_string()))?;
                Ok(Some(value))
            }
            None => Ok(None),
        }
    }

    pub async fn set_json<T: serde::Serialize>(&self, key: &str, value: &T, ttl: Option<Duration>) -> Result<(), CacheError> {
        let bytes = serde_json::to_vec(value)
            .map_err(|e| CacheError::Serialization(e.to_string()))?;

        self.set(key, &bytes, ttl).await
    }

    /// Batch get multiple keys
    pub async fn mget(&self, keys: &[&str]) -> Result<Vec<Option<Vec<u8>>>, CacheError> {
        let mut conn = self.client.clone();
        let prefixed: Vec<String> = keys.iter().map(|k| self.prefixed_key(k)).collect();

        let results: Vec<Option<Vec<u8>>> = conn
            .get(&prefixed[..])
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(results)
    }

    /// Pattern-based key deletion
    pub async fn delete_pattern(&self, pattern: &str) -> Result<u64, CacheError> {
        let mut conn = self.client.clone();
        let prefixed_pattern = self.prefixed_key(pattern);

        let keys: Vec<String> = redis::cmd("KEYS")
            .arg(&prefixed_pattern)
            .query_async(&mut conn)
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        if keys.is_empty() {
            return Ok(0);
        }

        let deleted: u64 = conn
            .del(&keys[..])
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(deleted)
    }
}
```

---

## Semantic Cache (L3)

### Vector Database Interface

```rust
#[async_trait]
pub trait VectorCache: Send + Sync {
    async fn search(&self, embedding: &[f32], limit: usize, threshold: f32) -> Result<Vec<CacheHit>, CacheError>;
    async fn insert(&self, key: &str, embedding: &[f32], value: &[u8], metadata: &CacheMetadata) -> Result<(), CacheError>;
    async fn delete(&self, key: &str) -> Result<(), CacheError>;
}

#[derive(Clone)]
pub struct CacheHit {
    pub key: String,
    pub value: Vec<u8>,
    pub score: f32,
    pub metadata: CacheMetadata,
}

#[derive(Clone, Serialize, Deserialize)]
pub struct CacheMetadata {
    pub model: String,
    pub created_at: i64,
    pub token_count: u32,
}
```

### Qdrant Implementation

```rust
use qdrant_client::prelude::*;
use qdrant_client::qdrant::{SearchPoints, PointStruct, vectors_config::Config, VectorParams, Distance};

pub struct QdrantCache {
    client: QdrantClient,
    collection_name: String,
    vector_size: u64,
}

impl QdrantCache {
    pub async fn new(url: &str, collection_name: &str, vector_size: u64) -> Result<Self, CacheError> {
        let client = QdrantClient::from_url(url)
            .build()
            .map_err(|e| CacheError::Connection(e.to_string()))?;

        // Create collection if not exists
        let collections = client.list_collections().await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        let exists = collections.collections.iter().any(|c| c.name == collection_name);

        if !exists {
            client.create_collection(&CreateCollection {
                collection_name: collection_name.to_string(),
                vectors_config: Some(VectorsConfig {
                    config: Some(Config::Params(VectorParams {
                        size: vector_size,
                        distance: Distance::Cosine.into(),
                        ..Default::default()
                    })),
                }),
                ..Default::default()
            })
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;
        }

        Ok(Self {
            client,
            collection_name: collection_name.to_string(),
            vector_size,
        })
    }
}

#[async_trait]
impl VectorCache for QdrantCache {
    async fn search(&self, embedding: &[f32], limit: usize, threshold: f32) -> Result<Vec<CacheHit>, CacheError> {
        let search_result = self.client
            .search_points(&SearchPoints {
                collection_name: self.collection_name.clone(),
                vector: embedding.to_vec(),
                limit: limit as u64,
                score_threshold: Some(threshold),
                with_payload: Some(true.into()),
                ..Default::default()
            })
            .await
            .map_err(|e| CacheError::Operation(e.to_string()))?;

        let hits = search_result.result
            .into_iter()
            .filter_map(|point| {
                let payload = point.payload;
                let key = payload.get("key")?.as_str()?.to_string();
                let value = payload.get("value")?.as_str()?.as_bytes().to_vec();
                let model = payload.get("model")?.as_str()?.to_string();
                let created_at = payload.get("created_at")?.as_integer()?;
                let token_count = payload.get("token_count")?.as_integer()? as u32;

                Some(CacheHit {
                    key,
                    value,
                    score: point.score,
                    metadata: CacheMetadata {
                        model,
                        created_at,
                        token_count,
                    },
                })
            })
            .collect();

        Ok(hits)
    }

    async fn insert(&self, key: &str, embedding: &[f32], value: &[u8], metadata: &CacheMetadata) -> Result<(), CacheError> {
        let point_id = uuid::Uuid::new_v4().to_string();

        let mut payload = serde_json::Map::new();
        payload.insert("key".to_string(), serde_json::json!(key));
        payload.insert("value".to_string(), serde_json::json!(String::from_utf8_lossy(value)));
        payload.insert("model".to_string(), serde_json::json!(metadata.model));
        payload.insert("created_at".to_string(), serde_json::json!(metadata.created_at));
        payload.insert("token_count".to_string(), serde_json::json!(metadata.token_count));

        self.client.upsert_points_blocking(
            &self.collection_name,
            None,
            vec![PointStruct::new(
                point_id,
                embedding.to_vec(),
                payload.into(),
            )],
            None,
        )
        .await
        .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(())
    }

    async fn delete(&self, key: &str) -> Result<(), CacheError> {
        self.client.delete_points(
            &self.collection_name,
            None,
            &qdrant_client::qdrant::PointsSelector {
                points_selector_one_of: Some(
                    qdrant_client::qdrant::points_selector::PointsSelectorOneOf::Filter(
                        qdrant_client::qdrant::Filter {
                            must: vec![qdrant_client::qdrant::Condition {
                                condition_one_of: Some(
                                    qdrant_client::qdrant::condition::ConditionOneOf::Field(
                                        qdrant_client::qdrant::FieldCondition {
                                            key: "key".to_string(),
                                            r#match: Some(qdrant_client::qdrant::Match {
                                                match_value: Some(
                                                    qdrant_client::qdrant::r#match::MatchValue::Keyword(key.to_string())
                                                ),
                                            }),
                                            ..Default::default()
                                        }
                                    )
                                ),
                            }],
                            ..Default::default()
                        }
                    )
                ),
            },
            None,
        )
        .await
        .map_err(|e| CacheError::Operation(e.to_string()))?;

        Ok(())
    }
}
```

---

## Unified Cache Manager

```rust
pub struct CacheManager {
    l1_cache: Option<Arc<InMemoryCache>>,
    l2_cache: Option<Arc<RedisCache>>,
    l3_cache: Option<Arc<dyn VectorCache>>,
    embedding_provider: Option<Arc<dyn EmbeddingProvider>>,
    config: CacheConfig,
}

impl CacheManager {
    pub async fn new(config: CacheConfig) -> Result<Self, CacheError> {
        let l1_cache = if config.l1_enabled {
            Some(Arc::new(InMemoryCache::new(config.l1_max_size)))
        } else {
            None
        };

        let l2_cache = if config.l2_enabled {
            Some(Arc::new(RedisCache::new(&config.redis_url, &config.cache_prefix).await?))
        } else {
            None
        };

        let l3_cache: Option<Arc<dyn VectorCache>> = if config.l3_enabled {
            Some(Arc::new(QdrantCache::new(&config.qdrant_url, &config.collection_name, config.vector_size).await?))
        } else {
            None
        };

        Ok(Self {
            l1_cache,
            l2_cache,
            l3_cache,
            embedding_provider: None,
            config,
        })
    }

    pub async fn get(&self, request: &ChatRequest) -> Result<Option<ChatResponse>, CacheError> {
        let key = CacheKeyGenerator::generate_key(request);

        // L1: In-memory cache
        if let Some(l1) = &self.l1_cache {
            if let Some(bytes) = l1.get(&key) {
                let response: ChatResponse = serde_json::from_slice(&bytes)?;
                return Ok(Some(response));
            }
        }

        // L2: Redis cache
        if let Some(l2) = &self.l2_cache {
            if let Some(response) = l2.get_json::<ChatResponse>(&key).await? {
                // Populate L1
                if let Some(l1) = &self.l1_cache {
                    let bytes = serde_json::to_vec(&response)?;
                    l1.set(key.clone(), bytes, Some(self.config.l1_ttl));
                }
                return Ok(Some(response));
            }
        }

        // L3: Semantic cache
        if let (Some(l3), Some(embedding_provider)) = (&self.l3_cache, &self.embedding_provider) {
            let semantic_key = CacheKeyGenerator::generate_semantic_key(request);
            let embedding = embedding_provider.embed(&semantic_key).await?;

            let hits = l3.search(&embedding, 1, self.config.similarity_threshold).await?;

            if let Some(hit) = hits.first() {
                let response: ChatResponse = serde_json::from_slice(&hit.value)?;

                // Populate L1 and L2
                let bytes = serde_json::to_vec(&response)?;
                if let Some(l1) = &self.l1_cache {
                    l1.set(key.clone(), bytes.clone(), Some(self.config.l1_ttl));
                }
                if let Some(l2) = &self.l2_cache {
                    l2.set(&key, &bytes, Some(self.config.l2_ttl)).await?;
                }

                return Ok(Some(response));
            }
        }

        Ok(None)
    }

    pub async fn set(&self, request: &ChatRequest, response: &ChatResponse) -> Result<(), CacheError> {
        let key = CacheKeyGenerator::generate_key(request);
        let bytes = serde_json::to_vec(response)?;

        // L1
        if let Some(l1) = &self.l1_cache {
            l1.set(key.clone(), bytes.clone(), Some(self.config.l1_ttl));
        }

        // L2
        if let Some(l2) = &self.l2_cache {
            l2.set(&key, &bytes, Some(self.config.l2_ttl)).await?;
        }

        // L3 (semantic)
        if let (Some(l3), Some(embedding_provider)) = (&self.l3_cache, &self.embedding_provider) {
            let semantic_key = CacheKeyGenerator::generate_semantic_key(request);
            let embedding = embedding_provider.embed(&semantic_key).await?;

            let metadata = CacheMetadata {
                model: request.model.clone(),
                created_at: chrono::Utc::now().timestamp(),
                token_count: response.usage.as_ref().map(|u| u.total_tokens).unwrap_or(0),
            };

            l3.insert(&key, &embedding, &bytes, &metadata).await?;
        }

        Ok(())
    }

    pub async fn invalidate(&self, request: &ChatRequest) -> Result<(), CacheError> {
        let key = CacheKeyGenerator::generate_key(request);

        if let Some(l1) = &self.l1_cache {
            l1.invalidate(&key);
        }

        if let Some(l2) = &self.l2_cache {
            l2.delete(&key).await?;
        }

        if let Some(l3) = &self.l3_cache {
            l3.delete(&key).await?;
        }

        Ok(())
    }
}
```

---

## Configuration

```yaml
cache:
  enabled: true

  l1:
    enabled: true
    max_size: 10000
    ttl_seconds: 300

  l2:
    enabled: true
    redis_url: ${REDIS_URL}
    prefix: "litellm"
    ttl_seconds: 3600

  l3:
    enabled: true
    type: "qdrant"  # or "weaviate", "pinecone"
    url: ${QDRANT_URL}
    collection_name: "semantic_cache"
    vector_size: 1536
    similarity_threshold: 0.95
    ttl_seconds: 86400

  # Models to exclude from caching
  exclude_models:
    - "gpt-4-turbo-preview"  # Rapidly changing model

  # Skip caching for streaming requests
  skip_streaming: true
```

---

## Cache Metrics

```rust
#[derive(Default)]
pub struct CacheStats {
    pub hits: AtomicU64,
    pub misses: AtomicU64,
    pub evictions: AtomicU64,
    pub l1_hits: AtomicU64,
    pub l2_hits: AtomicU64,
    pub l3_hits: AtomicU64,
}

impl CacheStats {
    pub fn hit_rate(&self) -> f64 {
        let hits = self.hits.load(Ordering::Relaxed) as f64;
        let misses = self.misses.load(Ordering::Relaxed) as f64;
        if hits + misses == 0.0 {
            0.0
        } else {
            hits / (hits + misses)
        }
    }

    pub fn report_metrics(&self, metrics: &MetricsReporter) {
        metrics.gauge("cache_hit_rate", self.hit_rate());
        metrics.counter("cache_hits_total", self.hits.load(Ordering::Relaxed));
        metrics.counter("cache_misses_total", self.misses.load(Ordering::Relaxed));
        metrics.counter("cache_evictions_total", self.evictions.load(Ordering::Relaxed));
    }
}
```

---

## Best Practices

### 1. Cache Key Determinism

Always ensure cache keys are deterministic for the same logical request:

```rust
// Good - deterministic key
fn generate_key(request: &ChatRequest) -> String {
    let normalized_messages: Vec<_> = request.messages
        .iter()
        .map(|m| (m.role.to_string(), m.content.clone()))
        .collect();
    // ...
}

// Bad - includes non-deterministic elements
fn generate_key(request: &ChatRequest) -> String {
    format!("{}-{}", request.model, uuid::Uuid::new_v4())
}
```

### 2. TTL Strategy

Use appropriate TTLs based on content volatility:

```rust
fn get_ttl_for_model(model: &str) -> Duration {
    match model {
        // Stable models - longer TTL
        "gpt-3.5-turbo" => Duration::from_secs(86400),  // 24 hours
        // Preview/beta models - shorter TTL
        _ if model.contains("preview") => Duration::from_secs(3600),  // 1 hour
        // Default
        _ => Duration::from_secs(43200),  // 12 hours
    }
}
```

### 3. Skip Caching When Appropriate

```rust
fn should_cache(request: &ChatRequest) -> bool {
    // Don't cache streaming requests
    if request.stream {
        return false;
    }

    // Don't cache if temperature > 0 (non-deterministic)
    if request.temperature.unwrap_or(1.0) > 0.0 {
        return false;
    }

    // Don't cache tool calls (may have side effects)
    if request.tools.is_some() {
        return false;
    }

    true
}
```
