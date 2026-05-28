# ChromaDB Error Handling & Resilience Patterns

**Purpose**: Production-ready error handling for ChromaDB operations across all agent types

**Use When**: Implementing robust ChromaDB integrations that handle failures gracefully

---

## Error Categories

### 1. Connection Failures
**Symptoms**: `ConnectionError`, `Timeout`, ChromaDB server unavailable

**Retry Pattern with Exponential Backoff**:
```javascript
async function retryWithBackoff(operation, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries - 1) {
        // Final attempt failed
        throw new Error(`ChromaDB operation failed after ${maxRetries} attempts: ${error.message}`);
      }

      // Exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, attempt) * 1000;
      console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
      await sleep(delay);
    }
  }
}

// Usage
const results = await retryWithBackoff(() =>
  mcp__chroma__query_documents({
    collection_name: collectionName,
    query_texts: [query],
    n_results: 10
  })
);
```

**Fallback Strategy**:
```javascript
async function queryWithFallback(query, collectionName) {
  try {
    // Primary: ChromaDB semantic search
    return await retryWithBackoff(() =>
      mcp__chroma__query_documents({ collection_name: collectionName, query_texts: [query] })
    );
  } catch (error) {
    console.warn(`ChromaDB unavailable: ${error.message}`);

    // Fallback 1: Local cache if available
    if (localCache.has(query)) {
      console.log("Using cached results");
      return localCache.get(query);
    }

    // Fallback 2: Simple keyword search on stored data
    console.log("Falling back to keyword search");
    return performKeywordSearch(query);
  }
}
```

---

### 2. Collection Errors

#### CollectionAlreadyExists
**Problem**: Trying to create collection that already exists

**Solution - Get or Create Pattern**:
```javascript
function getOrCreateCollection(collectionName, metadata = {}) {
  const collections = mcp__chroma__list_collections();

  if (collections.includes(collectionName)) {
    console.log(`Collection ${collectionName} already exists, using existing`);
    return { created: false, collection_name: collectionName };
  }

  console.log(`Creating new collection: ${collectionName}`);
  mcp__chroma__create_collection({
    collection_name: collectionName,
    embedding_function_name: "default",
    metadata: metadata
  });

  return { created: true, collection_name: collectionName };
}
```

#### CollectionNotFound
**Problem**: Querying collection that doesn't exist

**Solution - Validation Before Query**:
```javascript
function validateCollectionExists(collectionName) {
  const collections = mcp__chroma__list_collections();

  if (!collections.includes(collectionName)) {
    throw new Error(
      `Collection '${collectionName}' does not exist. ` +
      `Available collections: ${collections.join(", ")}`
    );
  }
}

// Usage
try {
  validateCollectionExists("my_collection");
  const results = mcp__chroma__query_documents({ collection_name: "my_collection", ... });
} catch (error) {
  console.error(`Collection validation failed: ${error.message}`);
  // Handle gracefully - maybe create collection or use different one
}
```

---

### 3. Document ID Conflicts

**Problem**: Duplicate document IDs cause insert failures

**Solution - Unique ID Generation**:
```javascript
function generateUniqueId(prefix, data) {
  // Option 1: Timestamp-based (simple, mostly unique)
  const timestampId = `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // Option 2: Content hash-based (deterministic, guaranteed unique per content)
  const contentHash = hashString(JSON.stringify(data));
  const hashId = `${prefix}_${contentHash}`;

  // Option 3: UUID (guaranteed unique)
  const uuidId = `${prefix}_${crypto.randomUUID()}`;

  return timestampId;  // Choose based on use case
}

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash).toString(36);
}
```

**Solution - Update Existing Pattern**:
```javascript
function upsertDocument(collectionName, document, id, metadata) {
  try {
    // Check if document exists
    const existing = mcp__chroma__get_documents({
      collection_name: collectionName,
      ids: [id]
    });

    if (existing.ids && existing.ids.length > 0) {
      // Document exists - update
      console.log(`Updating existing document: ${id}`);
      mcp__chroma__update_documents({
        collection_name: collectionName,
        ids: [id],
        documents: [document],
        metadatas: [metadata]
      });
    } else {
      // Document doesn't exist - add
      console.log(`Adding new document: ${id}`);
      mcp__chroma__add_documents({
        collection_name: collectionName,
        ids: [id],
        documents: [document],
        metadatas: [metadata]
      });
    }
  } catch (error) {
    console.error(`Upsert failed for ${id}: ${error.message}`);
    throw error;
  }
}
```

---

### 4. Data Validation Errors

**Problem**: Invalid metadata, malformed documents, embedding failures

**Solution - Validate Before Insert**:
```javascript
function validateDocument(document, id, metadata) {
  const errors = [];

  // Validate document
  if (!document || typeof document !== 'string') {
    errors.push(`Document must be non-empty string, got: ${typeof document}`);
  }
  if (document.length > 100000) {
    errors.push(`Document too large (${document.length} chars), max 100K recommended`);
  }

  // Validate ID
  if (!id || typeof id !== 'string') {
    errors.push(`ID must be non-empty string, got: ${typeof id}`);
  }
  if (id.includes(' ')) {
    errors.push(`ID cannot contain spaces: "${id}"`);
  }

  // Validate metadata
  if (metadata && typeof metadata !== 'object') {
    errors.push(`Metadata must be object, got: ${typeof metadata}`);
  }

  // Check metadata values are primitives
  if (metadata) {
    for (const [key, value] of Object.entries(metadata)) {
      const valueType = typeof value;
      if (!['string', 'number', 'boolean'].includes(valueType) && value !== null) {
        errors.push(`Metadata value for '${key}' must be primitive, got: ${valueType}`);
      }
    }
  }

  if (errors.length > 0) {
    throw new Error(`Document validation failed:\n${errors.join('\n')}`);
  }
}

// Usage
try {
  validateDocument(document, id, metadata);
  mcp__chroma__add_documents({ ... });
} catch (error) {
  console.error(`Validation error: ${error.message}`);
  // Handle gracefully - sanitize data or skip
}
```

---

### 5. Batch Operation Errors

**Problem**: Partial batch failures

**Solution - Chunked Batches with Error Isolation**:
```javascript
async function addDocumentsSafely(collectionName, documents, ids, metadatas) {
  const BATCH_SIZE = 100;
  const failed = [];
  const succeeded = [];

  for (let i = 0; i < documents.length; i += BATCH_SIZE) {
    const batchDocs = documents.slice(i, i + BATCH_SIZE);
    const batchIds = ids.slice(i, i + BATCH_SIZE);
    const batchMetas = metadatas.slice(i, i + BATCH_SIZE);

    try {
      mcp__chroma__add_documents({
        collection_name: collectionName,
        documents: batchDocs,
        ids: batchIds,
        metadatas: batchMetas
      });

      succeeded.push(...batchIds);
      console.log(`Batch ${i / BATCH_SIZE + 1}: Added ${batchDocs.length} documents`);

    } catch (error) {
      console.error(`Batch ${i / BATCH_SIZE + 1} failed: ${error.message}`);

      // Fallback: Try one-by-one for failed batch
      for (let j = 0; j < batchDocs.length; j++) {
        try {
          mcp__chroma__add_documents({
            collection_name: collectionName,
            documents: [batchDocs[j]],
            ids: [batchIds[j]],
            metadatas: [batchMetas[j]]
          });
          succeeded.push(batchIds[j]);
        } catch (singleError) {
          failed.push({ id: batchIds[j], error: singleError.message });
        }
      }
    }
  }

  return {
    succeeded: succeeded.length,
    failed: failed.length,
    failedDetails: failed
  };
}
```

---

### 6. Circuit Breaker Pattern

**Use When**: Repeated ChromaDB failures, prevent cascading failures

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.failureThreshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED';  // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async execute(operation) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker OPEN - ChromaDB unavailable');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
      console.error(`Circuit breaker OPEN - too many failures (${this.failureCount})`);
    }
  }
}

// Usage
const chromaBreaker = new CircuitBreaker(5, 60000);

try {
  const results = await chromaBreaker.execute(() =>
    mcp__chroma__query_documents({ ... })
  );
} catch (error) {
  console.error(`Query failed: ${error.message}`);
  // Use fallback logic
}
```

---

## Error Handling Checklist

Before deploying ChromaDB integration:

- [ ] **Retry Logic**: Exponential backoff for transient failures (3 attempts)
- [ ] **Fallback Strategy**: Local cache or alternative search when ChromaDB down
- [ ] **Collection Validation**: Check exists before query, get-or-create pattern
- [ ] **ID Uniqueness**: Generate unique IDs, handle conflicts with upsert
- [ ] **Data Validation**: Validate documents/metadata before insertion
- [ ] **Batch Error Handling**: Isolate failures, report partial success
- [ ] **Circuit Breaker**: Prevent cascading failures on repeated errors
- [ ] **Error Logging**: Log all errors with context (collection, operation, data)
- [ ] **Graceful Degradation**: Continue operation with reduced functionality
- [ ] **User Feedback**: Inform user when falling back to alternative methods

---

**Version**: 1.0
**Created**: 2025-11-14
**Part of**: chromadb-integration-skills ecosystem
