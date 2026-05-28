---
name: embed
description: Generate text embeddings using Qwen3 models via HuggingFace TEI. Use this skill to embed texts, configure the embedding service, or batch process documents. Invoke with /embed.
---

# Text Embedding

This skill manages text embedding generation using Qwen3 models via HuggingFace Text Embeddings Inference (TEI).

## Architecture

- **Remote Service**: HuggingFace TEI running on GPU instance
- **Client**: HTTP client with exponential backoff and batching
- **Output**: 1536-dimensional vectors
- **Storage**: Hive/Parquet tables or numpy arrays

## Start TEI Service

On a GPU instance:
```bash
# Using Docker
docker run --gpus all -p 8080:80 \
  ghcr.io/huggingface/text-embeddings-inference:latest \
  --model-id Alibaba-NLP/gte-Qwen2-1.5B-instruct

# Or with specific model
docker run --gpus all -p 8080:80 \
  ghcr.io/huggingface/text-embeddings-inference:latest \
  --model-id Qwen/Qwen3-Embedding-0.6B
```

## Python Client Usage

```python
from wc_simd.embed import EmbedServiceClient

# Initialize client
client = EmbedServiceClient(endpoint="http://gpu-host:8080/embed")

# Embed single text
vector = client.embed(["Hello world"])[0]

# Embed batch
vectors = client.embed(["text1", "text2", "text3"])
```

## PySpark Integration

```python
from wc_simd.embed import create_embed_udf

# Create UDF for Spark
embed_udf = create_embed_udf(endpoint="http://172.19.0.1:8080/embed")

# Apply to DataFrame
df_with_embeddings = df.withColumn("embedding", embed_udf("text_column"))
```

## Text Chunking

For long texts, use the chunker before embedding:

```python
from wc_simd.embed import TextChunker

chunker = TextChunker(chunk_size=1000, overlap=200)
chunks = chunker.split(long_text)

# Embed chunks
embeddings = client.embed(chunks)
```

## Elasticsearch Indexing

```python
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch(["http://localhost:9200"])

# Index with dense vector
actions = [
    {
        "_index": "text_embeddings",
        "_source": {
            "text": chunk,
            "embedding": embedding.tolist(),
            "work_id": work_id
        }
    }
    for chunk, embedding in zip(chunks, embeddings)
]

bulk(es, actions)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `endpoint` | Required | TEI service URL |
| `batch_size` | 32 | Texts per request |
| `max_retries` | 3 | Retry attempts |
| `timeout` | 30 | Request timeout (seconds) |

## Models

| Model | Dimensions | Notes |
|-------|------------|-------|
| Qwen3-Embedding-0.6B | 1024 | Fast, lightweight |
| gte-Qwen2-1.5B-instruct | 1536 | Higher quality |
| gme-Qwen2-VL | 1536 | Vision-language (use vlm-embed skill) |

## Troubleshooting

### Connection Errors
Ensure TEI service is running and accessible. From Docker Spark, use `172.19.0.1` (gateway IP).

### Rate Limiting
Increase batch size or add delays between requests.

### OOM on GPU
Reduce batch size or use a smaller model.
