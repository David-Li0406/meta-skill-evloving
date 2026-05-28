---
name: vlm-embed
description: Manage VLM (Vision-Language Model) embedding service and jobs. Use this skill to start the Flask embedding service, run embedding jobs, or train the AE3D autoencoder. Invoke with /vlm-embed.
---

# VLM Embedding Pipeline

This skill manages the VLM embedding pipeline which generates 1536-dimensional embeddings for images using the GME-Qwen2-VL-2B-Instruct model.

## Architecture

The pipeline separates model loading from Spark orchestration:

1. **Flask Service** (`vlm_embed_service.py`): Loads model once, serves `/embed` endpoint
2. **Spark Job** (`vlm_embed.py`): Reads from Hive tables, calls service, writes embeddings back to Hive

## Hive Tables

- **Input**: `images_without_text_renderings` (default)
- **Output**: `images_without_text_renderings_vlm_embeddings` (default)
- **Sharded output**: `{output_table}_shard_NNNN` when using `--num-shards`

## Start Embedding Service

```bash
# Start the Flask service on port 8081
python -m wc_simd.vlm_embed_service --host 0.0.0.0 --port 8081

# Or with specific GPU
CUDA_VISIBLE_DEVICES=0 python -m wc_simd.vlm_embed_service --host 0.0.0.0 --port 8081
```

The service exposes:
- `GET /health` - Health check with model info
- `POST /embed` - Embed images via `{urls: [...]}` or `{images_b64: [...]}`

## Run Embedding Job

```bash
# Run Spark job to embed all images
python -m wc_simd.vlm_embed --endpoint http://127.0.0.1:8081/embed

# Custom input/output tables
python -m wc_simd.vlm_embed \
  --input-table my_images \
  --output-table my_images_embedded \
  --endpoint http://127.0.0.1:8081/embed
```

## Sharded Processing (Resumable)

For large-scale processing with checkpoint/resume:

```bash
# Split into 100 shards, process shard 0
python -m wc_simd.vlm_embed --num-shards 100 --shard-id 0

# Process all shards sequentially (omit --shard-id)
python -m wc_simd.vlm_embed --num-shards 100

# Resume: existing shard tables are skipped by default
python -m wc_simd.vlm_embed --num-shards 100 --shard-id 5

# Force recompute (drop and recreate)
python -m wc_simd.vlm_embed --num-shards 100 --shard-id 5 --no-skip-existing
```

## Prefetch Mode

Download images in Spark workers and send base64 bytes to service (useful when service has limited network access):

```bash
python -m wc_simd.vlm_embed \
  --prefetch-images \
  --prefetch-workers 8 \
  --endpoint http://127.0.0.1:8081/embed
```

## Multi-Instance Parallelism

Run multiple Spark jobs on different machines, each processing a subset:

```bash
# Machine 1
python -m wc_simd.vlm_embed --instances 4 --instance-no 0

# Machine 2
python -m wc_simd.vlm_embed --instances 4 --instance-no 1

# etc.
```

## Key Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input-table` | `images_without_text_renderings` | Source Hive table |
| `--output-table` | `images_without_text_renderings_vlm_embeddings` | Destination table |
| `--endpoint` | `http://127.0.0.1:8081/embed` | Flask service URL |
| `--batch-size` | 16 | Images per service call |
| `--num-partitions` | 320 | Spark partitions |
| `--num-shards` | None | Split into N shard tables |
| `--shard-id` | None | Process specific shard |
| `--skip-existing` | True | Skip existing output tables |
| `--prefetch-images` | False | Download in Spark, send bytes |

## Train AE3D Autoencoder

Reduce 1536-dim embeddings to 3D for visualization:

```bash
# Export embeddings from Hive/Parquet to NumPy
python -m wc_simd.vlm_embed_train_data \
  --input-glob "path/to/embeddings/*.parquet" \
  --output-npy data/vlm_embed/embeddings.npy \
  --output-index data/vlm_embed/index.parquet

# Train autoencoder
python -m wc_simd.vlm_embed_ae train \
  --data data/vlm_embed/embeddings.npy \
  --out runs/ae3d

# Inference (project to 3D)
python -m wc_simd.vlm_embed_ae infer \
  --model runs/ae3d/ae.pt \
  --data embeddings.npy \
  --out projected.npy
```

## Troubleshooting

### transformers Version Conflict
The GME-Qwen2-VL model requires `transformers<4.52.0`. If you see errors like:
```
transformers<4.52.0 is required for normal functioning of this module, but found transformers==4.57.3
```

Fix by pinning the version:
```bash
pip install 'transformers>=4.37.0,<4.52.0'
```

Or in requirements.txt/Dockerfile:
```
transformers>=4.37.0,<4.52.0
```

### 401 Auth Errors
Some images require authentication (content advisory). These will have `embed_error` set in the output table.

### GPU Memory
The model requires significant GPU memory. Use a GPU with at least 16GB VRAM for the 2B model.

### Service Connection
If Spark workers can't reach the service:
- Local: use `http://127.0.0.1:8081/embed`
- Docker workers to host: use `http://172.19.0.1:8081/embed` (Docker gateway IP)
