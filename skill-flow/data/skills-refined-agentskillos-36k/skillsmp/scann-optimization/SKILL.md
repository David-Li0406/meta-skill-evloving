---
name: "scann-optimization"
description: "Google SCANN optimization for billion-scale vector search. Use when dealing with massive embedding datasets, need learned indexing, or enterprise-scale vector similarity."
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["scann", "google", "vector-search", "gpu", "enterprise", "trillion-scale"]
---

# SCANN Google Optimization Skill

## Descripción

Google SCANN (Scalable Nearest Neighbors) optimization skill para búsqueda vectorial a escala masiva (billions a trillions). Especializado en:
- Learned indexing con redes neuronales
- Anisotropic Vector Quantization
- Enterprise-scale performance tuning
- TensorFlow integration

## Cuándo Usar

✅ **Usar esta skill cuando:**
- Dataset tiene >100M vectores
- Necesitas precision superior a FAISS (recall >0.95)
- Tienes requisitos enterprise de trillion-scale
- Necesitas learned indexing optimization
- Requieres anisotropic quantization

❌ **No usar cuando:**
- Dataset <10M vectores (usar Qdrant)
- Necesitas ultra-baja latencia (<1ms) (usar FAISS-GPU)
- No tienes recursos para TensorFlow
- Setup simple es prioridad

## Prerequisites

### Hardware
- **CPU**: 16+ cores recomendado
- **RAM**: 64GB+ para billion-scale
- **GPU**: Opcional pero recomendado (NVIDIA V100/A100)
- **Storage**: NVMe SSD para índices

### Software
```bash
# Python 3.8+
pip install scann tensorflow numpy

# O con GPU
pip install scann tensorflow-gpu numpy

# Verificar instalación
python -c "import scann; print(scann.__version__)"
```

### Dataset Requirements
- Embeddings en formato NumPy (.npy)
- Dimensión consistente (típicamente 128, 256, 768, 1024)
- Normalización si usas dot product

## Instrucciones

### 1. Preparar Dataset

```python
import numpy as np

# Cargar embeddings
embeddings = np.load('embeddings.npy')  # Shape: (N, D)

# Normalizar para dot product
if use_dot_product:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

print(f"Dataset: {embeddings.shape[0]:,} vectors of {embeddings.shape[1]} dimensions")
```

### 2. Build SCANN Index

```python
import scann

def build_scann_index(
    embeddings: np.ndarray,
    num_leaves: int = 10000,
    training_sample_size: int = 250000,
    dimensions_per_block: int = 2,
    anisotropic_threshold: float = 0.2,
    reorder_k: int = 1000
):
    """
    Build optimized SCANN index with learned indexing
    
    Args:
        embeddings: NumPy array of shape (N, D)
        num_leaves: Number of tree leaves (más = mejor recall, más memoria)
        training_sample_size: Samples for training (recomendado 250K)
        dimensions_per_block: Dimensions per quantization block
        anisotropic_threshold: Threshold for anisotropic quantization
        reorder_k: Number of candidates to reorder
    """
    
    print("Building SCANN index...")
    print(f"Parameters:")
    print(f"  num_leaves: {num_leaves}")
    print(f"  training_sample_size: {training_sample_size}")
    print(f"  dimensions_per_block: {dimensions_per_block}")
    
    # Initialize builder
    builder = scann.ScannBuilder(
        embeddings,
        num_leaves,
        distance_measure="dot_product"  # O "squared_l2"
    )
    
    # Tree-based partitioning with learned indexing
    # Esta es la parte "learned" - usa ML para optimizar particiones
    builder = builder.tree(
        num_leaves=num_leaves,
        num_leaves_to_search=int(num_leaves * 0.05),  # 5% of leaves
        training_sample_size=training_sample_size
    )
    
    # Anisotropic Quantization (Google's secret sauce)
    # Adapta la quantización a la distribución de datos
    builder = builder.score_ah(
        dimensions_per_block=dimensions_per_block,
        anisotropic_quantization_threshold=anisotropic_threshold
    )
    
    # Reordering for precision
    # Re-rankea top-K candidatos con distancia exacta
    builder = builder.reorder(reorder_k)
    
    # Build!
    searcher = builder.build()
    
    print("✅ SCANN index built successfully")
    return searcher
```

### 3. Optimize Parameters

```python
def tune_scann_parameters(embeddings, queries, ground_truth):
    """
    Tune SCANN parameters for optimal recall/latency tradeoff
    
    Args:
        embeddings: Dataset embeddings
        queries: Query embeddings for testing
        ground_truth: True nearest neighbors for recall calculation
    """
    
    # Parameter grid
    configs = [
        # (num_leaves, leaves_to_search, dimensions_per_block)
        (1000, 50, 2),
        (2000, 100, 2),
        (5000, 250, 2),
        (10000, 500, 2),
        (10000, 500, 1),  # Más precisión
    ]
    
    results = []
    
    for num_leaves, leaves_search, dims_per_block in configs:
        print(f"\nTesting: leaves={num_leaves}, search={leaves_search}, dims={dims_per_block}")
        
        # Build index
        searcher = build_scann_index(
            embeddings,
            num_leaves=num_leaves,
            dimensions_per_block=dims_per_block
        )
        
        # Benchmark
        start = time.time()
        neighbors, distances = searcher.search_batched(
            queries,
            final_num_neighbors=10,
            leaves_to_search=leaves_search
        )
        latency = (time.time() - start) / len(queries) * 1000
        
        # Calculate recall
        recall = calculate_recall(neighbors, ground_truth)
        
        results.append({
            'config': (num_leaves, leaves_search, dims_per_block),
            'recall': recall,
            'latency_ms': latency
        })
        
        print(f"  Recall@10: {recall:.4f}")
        print(f"  Latency: {latency:.2f}ms")
    
    return results
```

### 4. Production Search

```python
class ScannSearchEngine:
    def __init__(self, searcher, metadata=None):
        self.searcher = searcher
        self.metadata = metadata
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10,
        leaves_to_search: int = 100,
        pre_reorder_k: int = 1000
    ):
        """
        Ultra-precise trillion-scale search
        
        Args:
            query: Query vector (1D array)
            k: Number of results
            leaves_to_search: Number of tree leaves to search
            pre_reorder_k: Candidates before reordering
        """
        
        # Search
        neighbors, distances = self.searcher.search_batched(
            query.reshape(1, -1),
            final_num_neighbors=k,
            leaves_to_search=leaves_to_search,
            pre_reorder_num_neighbors=pre_reorder_k
        )
        
        results = []
        for idx, dist in zip(neighbors[0], distances[0]):
            result = {
                'id': int(idx),
                'distance': float(dist),
                'score': float(1.0 - dist)  # Convert to similarity
            }
            
            if self.metadata:
                result['metadata'] = self.metadata[idx]
            
            results.append(result)
        
        return results
    
    def batch_search(self, queries: np.ndarray, k: int = 10):
        """Optimized batch processing"""
        neighbors, distances = self.searcher.search_batched(
            queries,
            final_num_neighbors=k
        )
        return neighbors, distances
```

### 5. Save/Load Index

```python
# Save index
searcher.serialize('/path/to/index')

# Load index
import scann
searcher = scann.ScannSearcher.from_serialized_index('/path/to/index')
```

## Ejemplos

### Example 1: Code Embeddings Search

```python
# Load code embeddings (from CodeBERT, etc.)
code_embeddings = np.load('code_embeddings.npy')  # 1M x 768
print(f"Code vectors: {code_embeddings.shape}")

# Build SCANN index
searcher = build_scann_index(
    code_embeddings,
    num_leaves=5000,
    training_sample_size=100000
)

# Search for similar code
query = get_code_embedding("def process_parallel(data):")
results = searcher.search(query, k=20)

for idx, dist in zip(results[0], results[1]):
    print(f"Similar code {idx}: distance={dist:.4f}")
```

### Example 2: Enterprise Trillion-Scale

```python
# Trillion-scale configuration
searcher = build_scann_index(
    embeddings,  # Assume billions loaded incrementally
    num_leaves=100000,  # 100K leaves for trillion-scale
    training_sample_size=1000000,  # 1M samples
    dimensions_per_block=2,
    reorder_k=10000
)

# Search with high precision
results = searcher.search(
    query,
    k=100,
    leaves_to_search=5000,  # Search 5% of leaves
    pre_reorder_k=10000
)
```

## Benchmarks

### Expected Performance

| Dataset Size | Recall@10 | Latency (p99) | Memory | Config |
|-------------|-----------|---------------|--------|--------|
| 10M vectors | 0.95 | 5ms | 4GB | leaves=2000 |
| 100M vectors | 0.96 | 8ms | 30GB | leaves=10000 |
| 1B vectors | 0.97 | 12ms | 200GB | leaves=50000 |
| 10B+ vectors | 0.98 | 20ms | 2TB+ | leaves=100000 |

### Comparison with FAISS

| Metric | SCANN | FAISS-GPU |
|--------|-------|-----------|
| **Recall** | 0.98 ✅ | 0.92 |
| **Latency** | 8ms | 2ms ✅ |
| **Scale** | Trillions ✅ | Billions |
| **Learning** | Yes ✅ | No |
| **Setup** | Complex | Simple ✅ |

## Best Practices

### ✅ DO's
1. **Use sufficient training data** (250K+ samples)
2. **Normalize vectors** for dot product
3. **Tune num_leaves** based on dataset size
4. **Enable reordering** for better recall
5. **Use anisotropic quantization** (Google's advantage)
6. **Benchmark** before production

### ❌ DON'Ts
1. Don't use for small datasets (<10M)
2. Don't skip parameter tuning
3. Don't use without normalization (dot product)
4. Don't ignore training sample size
5. Don't expect FAISS-level latency

## Troubleshooting

### Low Recall
```python
# Increase leaves to search
searcher.search(query, leaves_to_search=500)  # Default: 100

# Increase reorder candidates
builder = builder.reorder(2000)  # Default: 1000

# Reduce dimensions_per_block
builder = builder.score_ah(dimensions_per_block=1)  # More precision
```

### High Latency
```python
# Reduce leaves to search
searcher.search(query, leaves_to_search=50)

# Reduce num_leaves
builder = scann.ScannBuilder(embeddings, num_leaves=2000)

# Reduce reorder_k
builder = builder.reorder(500)
```

### Memory Issues
```python
# Use smaller dimensions_per_block
builder = builder.score_ah(dimensions_per_block=4)  # More compression

# Reduce training sample size
builder = builder.tree(training_sample_size=100000)
```

## Resources

### Official Documentation
- [SCANN GitHub](https://github.com/google-research/google-research/tree/master/scann)
- [SCANN Paper](https://arxiv.org/abs/1908.10396)
- [Google AI Blog](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html)

### Integration Examples
- See `motores/vector_search/scann/` for Rust FFI integration
- See `docs/MOTOR_ARCHITECTURE.md` for architecture details

---

**Última actualización:** Enero 2026  
**Proyecto:** MEMORY_P v2.0 - Nuclear MCP Toolkit  
**Autor:** Rigohl
