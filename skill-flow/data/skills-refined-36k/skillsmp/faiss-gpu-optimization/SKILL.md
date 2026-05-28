---
name: "faiss-gpu-optimization"
description: "FAISS-GPU acceleration with CUDA for billion-scale local vector search. Use for ultra-fast similarity search with GPU acceleration."
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["faiss", "gpu", "cuda", "vector-search", "billion-scale", "performance"]
---

# FAISS-GPU Optimization Skill

## Descripción

FAISS-GPU acceleration skill para búsqueda vectorial ultra-rápida a escala masiva usando NVIDIA GPUs. Especializado en:
- GPU acceleration con CUDA
- IVF indices con Product Quantization
- Billion-scale local search
- Memory optimization

## Cuándo Usar

✅ **Usar esta skill cuando:**
- Necesitas latencia ultra-baja (<2ms)
- Dataset 10M-1B vectores
- Tienes NVIDIA GPU disponible
- Local deployment (no distributed)
- Throughput masivo (50K+ QPS)

❌ **No usar cuando:**
- Dataset <1M vectores (usar Qdrant)
- Sin GPU disponible (usar FAISS-CPU o Qdrant)
- Necesitas >99% recall (usar SCANN)
- Distributed deployment (usar SCANN)

## Prerequisites

### Hardware
- **GPU**: NVIDIA GPU con CUDA 11.0+
  - Recomendado: RTX 3090, A100, H100
  - Minimum: RTX 2060 con 6GB VRAM
- **CPU**: 8+ cores
- **RAM**: 32GB+ (para cargar dataset)
- **Storage**: NVMe SSD

### Software
```bash
# CUDA Toolkit
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run

# Python environment
conda create -n faiss python=3.10
conda activate faiss

# FAISS-GPU
conda install -c pytorch faiss-gpu

# O con pip
pip install faiss-gpu

# Verify
python -c "import faiss; print(faiss.get_num_gpus())"
```

## Instrucciones

### 1. GPU Detection & Setup

```python
import faiss
import numpy as np

def setup_faiss_gpu(gpu_id=0):
    """Initialize FAISS-GPU resources"""
    
    # Check available GPUs
    ngpus = faiss.get_num_gpus()
    print(f"Available GPUs: {ngpus}")
    
    if ngpus == 0:
        raise RuntimeError("No GPUs available")
    
    # Create GPU resources
    res = faiss.StandardGpuResources()
    
    # Configure GPU memory
    res.setTempMemory(2 * 1024 * 1024 * 1024)  # 2GB temp memory
    
    print(f"✅ GPU {gpu_id} initialized")
    return res, gpu_id
```

### 2. Build IVF-PQ Index

```python
def build_faiss_gpu_index(
    embeddings: np.ndarray,
    gpu_id: int = 0,
    nlist: int = 4096,
    m: int = 64,
    nbits: int = 8
):
    """
    Build optimized FAISS-GPU index
    
    Args:
        embeddings: NumPy array (N, D)
        gpu_id: GPU device ID
        nlist: Number of IVF centroids
        m: Number of PQ subquantizers
        nbits: Bits per subquantizer
    """
    
    n, d = embeddings.shape
    print(f"Building index for {n:,} vectors of {d} dimensions")
    
    # Create GPU resources
    res = faiss.StandardGpuResources()
    
    # Create CPU index first
    quantizer = faiss.IndexFlatL2(d)
    
    # IVF with Product Quantization
    index = faiss.IndexIVFPQ(
        quantizer,
        d,
        nlist,  # Number of Voronoi cells
        m,      # Number of sub-vectors
        nbits   # Bits per sub-vector
    )
    
    # Move to GPU
    gpu_index = faiss.index_cpu_to_gpu(res, gpu_id, index)
    
    # Training (required for IVF)
    print("Training index...")
    # Use subset for training (10%)
    train_size = min(n // 10, 1000000)
    train_vectors = embeddings[::n//train_size][:train_size]
    
    gpu_index.train(train_vectors)
    
    # Add all vectors
    print("Adding vectors...")
    batch_size = 50000
    for i in range(0, n, batch_size):
        end = min(i + batch_size, n)
        gpu_index.add(embeddings[i:end])
        if (i // batch_size) % 10 == 0:
            print(f"  Added {end:,}/{n:,} vectors")
    
    print("✅ Index built successfully")
    return gpu_index, res

# Example usage
embeddings = np.random.random((1_000_000, 768)).astype('float32')
gpu_index, res = build_faiss_gpu_index(embeddings)
```

### 3. Optimize Parameters

```python
def tune_faiss_parameters(
    embeddings: np.ndarray,
    queries: np.ndarray,
    ground_truth: np.ndarray,
    gpu_id: int = 0
):
    """
    Tune FAISS parameters for optimal performance
    
    Returns best configuration
    """
    
    configs = [
        # (nlist, nprobe, m, nbits)
        (1024, 32, 32, 8),   # Fast, lower recall
        (2048, 64, 48, 8),   # Balanced
        (4096, 128, 64, 8),  # High recall
        (8192, 256, 96, 8),  # Best recall
    ]
    
    results = []
    
    for nlist, nprobe, m, nbits in configs:
        print(f"\nTesting: nlist={nlist}, nprobe={nprobe}, m={m}")
        
        # Build index
        index, res = build_faiss_gpu_index(
            embeddings,
            gpu_id=gpu_id,
            nlist=nlist,
            m=m,
            nbits=nbits
        )
        
        # Set search parameters
        index.nprobe = nprobe
        
        # Benchmark
        import time
        start = time.time()
        D, I = index.search(queries, k=10)
        latency = (time.time() - start) / len(queries) * 1000
        
        # Calculate recall
        recall = calculate_recall(I, ground_truth)
        
        results.append({
            'config': (nlist, nprobe, m, nbits),
            'recall': recall,
            'latency_ms': latency,
            'qps': 1000 / latency
        })
        
        print(f"  Recall@10: {recall:.4f}")
        print(f"  Latency: {latency:.2f}ms")
        print(f"  QPS: {1000/latency:.0f}")
    
    return results

def calculate_recall(predictions, ground_truth, k=10):
    """Calculate recall@k"""
    n = len(predictions)
    recall_sum = 0
    for i in range(n):
        pred_set = set(predictions[i][:k])
        true_set = set(ground_truth[i][:k])
        recall_sum += len(pred_set & true_set) / k
    return recall_sum / n
```

### 4. Production Search Engine

```python
class FAISSGPUEngine:
    def __init__(self, dimension: int, gpu_id: int = 0):
        self.dimension = dimension
        self.gpu_id = gpu_id
        self.index = None
        self.res = None
        
    def build(
        self,
        embeddings: np.ndarray,
        nlist: int = 4096,
        nprobe: int = 128
    ):
        """Build and configure index"""
        self.index, self.res = build_faiss_gpu_index(
            embeddings,
            gpu_id=self.gpu_id,
            nlist=nlist
        )
        self.index.nprobe = nprobe
        
    def search(
        self,
        query: np.ndarray,
        k: int = 10
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Ultra-fast GPU search
        
        Returns:
            distances, indices
        """
        if query.ndim == 1:
            query = query.reshape(1, -1)
        
        D, I = self.index.search(query, k)
        return D[0], I[0]
    
    def batch_search(
        self,
        queries: np.ndarray,
        k: int = 10
    ) -> tuple[np.ndarray, np.ndarray]:
        """Optimized batch search"""
        return self.index.search(queries, k)
    
    def save(self, path: str):
        """Save index to disk"""
        # Move to CPU first
        cpu_index = faiss.index_gpu_to_cpu(self.index)
        faiss.write_index(cpu_index, path)
        print(f"✅ Index saved to {path}")
    
    @classmethod
    def load(cls, path: str, gpu_id: int = 0):
        """Load index from disk"""
        engine = cls(dimension=0, gpu_id=gpu_id)
        
        # Load CPU index
        cpu_index = faiss.read_index(path)
        engine.dimension = cpu_index.d
        
        # Move to GPU
        engine.res = faiss.StandardGpuResources()
        engine.index = faiss.index_cpu_to_gpu(
            engine.res,
            gpu_id,
            cpu_index
        )
        
        print(f"✅ Index loaded from {path}")
        return engine
```

### 5. Multi-GPU Support

```python
def build_multi_gpu_index(embeddings: np.ndarray):
    """Distribute index across multiple GPUs"""
    
    ngpus = faiss.get_num_gpus()
    print(f"Using {ngpus} GPUs")
    
    # Create CPU index
    d = embeddings.shape[1]
    quantizer = faiss.IndexFlatL2(d)
    index = faiss.IndexIVFPQ(quantizer, d, 4096, 64, 8)
    
    # Replicate to all GPUs
    gpu_index = faiss.index_cpu_to_all_gpus(index)
    
    # Train and add
    gpu_index.train(embeddings[::10])
    gpu_index.add(embeddings)
    
    return gpu_index
```

## Ejemplos

### Example 1: Code Embeddings

```python
# Load embeddings
embeddings = np.load('code_embeddings.npy')  # 10M x 768
print(f"Loaded {embeddings.shape}")

# Build index
engine = FAISSGPUEngine(dimension=768, gpu_id=0)
engine.build(embeddings, nlist=4096, nprobe=128)

# Search
query = get_embedding("async function processData()")
distances, indices = engine.search(query, k=20)

print("Similar code:")
for idx, dist in zip(indices, distances):
    print(f"  {idx}: distance={dist:.4f}")

# Save
engine.save('code_index.faiss')
```

### Example 2: Billion-Scale

```python
# For billion-scale, use larger nlist
embeddings_1b = load_billion_vectors()  # Assume efficient loading

engine = FAISSGPUEngine(dimension=768, gpu_id=0)
engine.build(
    embeddings_1b,
    nlist=65536,    # More centroids for billion-scale
    nprobe=256      # Higher for better recall
)

# Batch search
queries = np.random.random((10000, 768)).astype('float32')
D, I = engine.batch_search(queries, k=10)

print(f"Batch search: {len(queries)} queries")
print(f"Average distance: {D.mean():.4f}")
```

### Example 3: Rust FFI Integration

```rust
// motores/vector_search/faiss/mod.rs
use pyo3::prelude::*;
use pyo3::types::PyModule;

pub struct FAISSGPUEngine {
    py_engine: PyObject,
}

impl FAISSGPUEngine {
    pub fn new(dimension: usize, gpu_id: i32) -> Result<Self> {
        Python::with_gil(|py| {
            let faiss_module = PyModule::import(py, "faiss_engine")?;
            let engine_class = faiss_module.getattr("FAISSGPUEngine")?;
            let py_engine = engine_class.call1((dimension, gpu_id))?;
            
            Ok(FAISSGPUEngine {
                py_engine: py_engine.into()
            })
        })
    }
    
    pub fn search(&self, query: &[f32], k: usize) -> Result<Vec<(u64, f32)>> {
        Python::with_gil(|py| {
            let result = self.py_engine
                .call_method1(py, "search", (query, k))?;
            
            // Convert Python result to Rust
            let (distances, indices): (Vec<f32>, Vec<u64>) = 
                result.extract(py)?;
            
            Ok(indices.into_iter()
                .zip(distances)
                .collect())
        })
    }
}
```

## Benchmarks

### Expected Performance

| Dataset Size | QPS | Latency (p99) | Recall@10 | GPU | Memory |
|-------------|-----|---------------|-----------|-----|--------|
| 10M | 10,000 | 1ms | 0.90 | RTX 3060 | 4GB |
| 100M | 30,000 | 1ms | 0.91 | RTX 3090 | 12GB |
| 500M | 40,000 | 2ms | 0.92 | A100 40GB | 30GB |
| 1B | 50,000 | 2ms | 0.92 | A100 80GB | 60GB |

### Comparison

| Metric | FAISS-GPU | FAISS-CPU | Qdrant |
|--------|-----------|-----------|--------|
| **Speed** | 50K QPS ✅ | 5K QPS | 2.5K QPS |
| **Latency** | <2ms ✅ | ~10ms | ~5ms |
| **Recall** | 0.92 | 0.92 | 0.95 ✅ |
| **Scale** | 1B ✅ | 100M | 10M |
| **Cost** | GPU needed | Cheap ✅ | Medium |

## Best Practices

### ✅ DO's
1. **Normalize vectors** for dot product
2. **Train with representative sample** (10%+)
3. **Tune nprobe** for recall/speed tradeoff
4. **Use batch search** for throughput
5. **Monitor GPU memory**
6. **Save indices** to avoid rebuilding

### ❌ DON'Ts
1. Don't use for small datasets (<1M)
2. Don't skip normalization
3. Don't use too small nlist
4. Don't forget GPU memory limits
5. Don't mix different GPU types

## Troubleshooting

### Out of Memory
```python
# Reduce PQ parameters
index = faiss.IndexIVFPQ(quantizer, d, nlist, m=32, nbits=8)  # Smaller m

# Use less temp memory
res.setTempMemory(512 * 1024 * 1024)  # 512MB
```

### Low Recall
```python
# Increase nprobe
index.nprobe = 256  # Search more cells

# Increase nlist
# More centroids = better clustering
```

### Slow Indexing
```python
# Reduce training set
train_size = 100000  # Smaller training set

# Use batch add
for batch in batches:
    index.add(batch)
```

## Resources

- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [GPU Guide](https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU)

---

**Última actualización:** Enero 2026  
**Proyecto:** MEMORY_P v2.0  
**Autor:** Rigohl
