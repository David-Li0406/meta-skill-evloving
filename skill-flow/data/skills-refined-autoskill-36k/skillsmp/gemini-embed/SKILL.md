---
name: gemini-embed
description: Generate text embeddings using Google Gemini API for RAG, semantic similarity, classification, and clustering tasks. Invoke when user wants to embed text, create embeddings, or convert text to vectors with Gemini.
trigger_keywords:
  - gemini embed
  - gemini embedding
  - gemini embeddings
  - embed with gemini
  - text to vector
  - gemini vector
---

# Gemini Embeddings API

Generate text embeddings using Google Gemini API via REST.

## Prerequisites

- Environment variable `GOOGLE_API_KEY` must be set
- API endpoint: `https://generativelanguage.googleapis.com/v1beta`
- Model: `gemini-embedding-001`

## Workflow

### Phase 1: Determine Embedding Type

- **Single Embedding**: For one text input
- **Batch Embedding**: For multiple texts (more efficient)

### Phase 2: Configure Task Type (Optional)

Choose based on use case:
- `RETRIEVAL_QUERY`: For search queries
- `RETRIEVAL_DOCUMENT`: For documents to be searched
- `SEMANTIC_SIMILARITY`: For comparing text similarity
- `CLASSIFICATION`: For text classification
- `CLUSTERING`: For grouping similar texts

### Phase 3: Execute API Call

---

## 1. Single Text Embedding

### Basic Embedding

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "models/gemini-embedding-001",
      "content": {
        "parts": [{"text": "Hello world"}]
      }
    }'
```

### With Task Type

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "models/gemini-embedding-001",
      "content": {
        "parts": [{"text": "What is machine learning?"}]
      },
      "task_type": "RETRIEVAL_QUERY"
    }'
```

### With Output Dimensionality Control

Truncate embeddings to a smaller size for efficiency:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "models/gemini-embedding-001",
      "content": {
        "parts": [{"text": "Hello world"}]
      },
      "output_dimensionality": 256
    }'
```

---

## 2. Batch Embedding

Process multiple texts in a single API call:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "requests": [
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "What is the meaning of life?"}]}
        },
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "How does the brain work?"}]}
        },
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "What is quantum computing?"}]}
        }
      ]
    }'
```

### Batch with Task Type

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "requests": [
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "Document about AI"}]},
          "task_type": "RETRIEVAL_DOCUMENT"
        },
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "Document about ML"}]},
          "task_type": "RETRIEVAL_DOCUMENT"
        }
      ]
    }'
```

---

## Response Structure

### Single Embedding Response

```json
{
  "embedding": {
    "values": [
      -0.02342152,
      0.01676572,
      0.009261323,
      ...
    ]
  }
}
```

### Batch Embedding Response

```json
{
  "embeddings": [
    {
      "values": [-0.022374554, -0.004560777, ...]
    },
    {
      "values": [-0.007975887, -0.02141119, ...]
    },
    {
      "values": [-0.0047850125, 0.008764064, ...]
    }
  ]
}
```

---

## Task Types Reference

| Task Type | Use Case | Example |
|-----------|----------|---------|
| `RETRIEVAL_QUERY` | Search queries | "What is machine learning?" |
| `RETRIEVAL_DOCUMENT` | Documents to search | Article content, wiki pages |
| `SEMANTIC_SIMILARITY` | Compare text similarity | Duplicate detection |
| `CLASSIFICATION` | Categorize text | Spam detection, sentiment |
| `CLUSTERING` | Group similar texts | Topic modeling |

---

## Common Use Cases

### RAG (Retrieval-Augmented Generation)

1. Embed documents with `RETRIEVAL_DOCUMENT`
2. Store embeddings in vector database
3. Embed user query with `RETRIEVAL_QUERY`
4. Find similar documents by vector similarity

### Semantic Search

```bash
# Embed the query
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "models/gemini-embedding-001",
      "content": {"parts": [{"text": "How to train a neural network?"}]},
      "task_type": "RETRIEVAL_QUERY"
    }'
```

### Text Similarity Comparison

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:batchEmbedContents?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "requests": [
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "The cat sat on the mat"}]},
          "task_type": "SEMANTIC_SIMILARITY"
        },
        {
          "model": "models/gemini-embedding-001",
          "content": {"parts": [{"text": "A feline rested on the rug"}]},
          "task_type": "SEMANTIC_SIMILARITY"
        }
      ]
    }'
```

Then compute cosine similarity between the two embedding vectors.

---

## Best Practices

1. **Use batch embedding**: More efficient for multiple texts
2. **Set task_type**: Improves embedding quality for specific use cases
3. **Reduce dimensionality**: Use `output_dimensionality` for smaller, faster embeddings when full precision isn't needed
4. **Match task types**: Use same task_type for queries and documents in RAG
5. **Normalize vectors**: Cosine similarity works best with normalized vectors
