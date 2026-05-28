# Qdrant Collections Management

## Creating Collections

### Basic Collection
```typescript
import { QdrantClient } from '@qdrant/js-client';

const client = new QdrantClient({ url: process.env.QDRANT_URL });

await client.createCollection('textbook_chunks', {
  vectors: {
    size: 1536, // Dimension for OpenAI ada-002
    distance: 'Cosine', // Or 'Euclid', 'Dot'
  },
});
```

### With HNSW Configuration
```typescript
await client.createCollection('textbook_chunks', {
  vectors: { size: 1536, distance: 'Cosine' },
  hnsw_config: {
    m: 16,              // Number of edges per node
    ef_construct: 100,  // Size of candidate list for graph construction
    full_scan_threshold: 10000,
  },
  optimizers_config: {
    default_segment_number: 2,
  },
});
```

## Listing Collections
```typescript
const collections = await client.getCollections();
console.log(collections.collections.map(c => c.name));
```

## Getting Collection Info
```typescript
const info = await client.getCollection('textbook_chunks');
console.log(`Points: ${info.points_count}`);
console.log(`Vectors config: ${JSON.stringify(info.config)}`);
```

## Deleting Collections
```typescript
await client.deleteCollection('old_collection');
```

## Collection Aliases
```typescript
// Create alias (useful for zero-downtime updates)
await client.createAlias('production', 'textbook_chunks_v2');

// Update alias
await client.updateAlias({ collection_name: 'textbook_chunks_v3', alias_name: 'production' });
```

## Collection Configuration Best Practices

### For Text Search (OpenAI Embeddings)
- **Vector size**: 1536 (ada-002) or 3072 (ada-003)
- **Distance**: Cosine (most common for text)
- **HNSW m**: 16-32 (higher = better recall, more memory)
- **HNSW ef_construct**: 100-200

### For Production
```typescript
await client.createCollection('production_chunks', {
  vectors: { size: 1536, distance: 'Cosine' },
  hnsw_config: {
    m: 16,
    ef_construct: 100,
    on_disk: true, // Store HNSW graph on disk to save RAM
  },
  quantization_config: {
    scalar: {
      type: 'int8',
      quantile: 0.99,
      always_ram: true,
    },
  },
});
```

## Updating Collection
```typescript
// Can't change vector size, but can update other params
await client.updateCollection('textbook_chunks', {
  optimizers_config: {
    indexing_threshold: 20000,
  },
});
```
