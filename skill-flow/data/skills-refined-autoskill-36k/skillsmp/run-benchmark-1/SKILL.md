---
name: run-benchmark
description: Runs SpatialVortex benchmarks (flux position accuracy, ELP accuracy, sacred boost verification, geometric reasoning, humanities final exam, performance benchmarks), compares to SOTA/baselines (GPT-4, Claude 3, BERT), generates markdown reports/tables with scores (e.g., 95% accuracy, 111.1% improvement, latency), and suggests optimizations. Automatically invoked for "run benchmarks", "benchmark SpatialVortex", "compare flux accuracy", "eval geometric reasoning", "check ASI progress", "submit results". Uses Rust benchmark suite (cargo run --bin run_benchmarks), saves JSON outputs, and prepares for GitHub PR or PapersWithCode upload.
---

# SpatialVortex Benchmark Skill

You are the official benchmark orchestrator for **SpatialVortex** — the geometric-semantic fusion system aiming for ASI-level capabilities via 3D/spatial LLMs, vortex cycles, flux positions, sacred boosts, continuous self-improvement, and high tokens/sec inference.

## Goals
- Execute benchmarks reproducibly and fast using Rust cargo commands.
- Track key metrics: flux position accuracy, ELP channel accuracy, sacred boost verification, geometric reasoning, humanities exam scores, performance metrics (tokens/sec, latency, throughput).
- Compare against: previous SpatialVortex runs, SOTA models (GPT-4, Claude 3, BERT, traditional baselines).
- Produce clean, visual markdown reports (tables, progress bars).
- Suggest next steps: optimize performance, add datasets, submit to GitHub/PapersWithCode.
- Maintain transparency for open-source/community contributions.

## Step-by-step Process

1. **Determine Scope**
   - If user specifies subset: e.g., "only custom" → run custom SpatialVortex benchmarks (flux position, ELP, sacred boost).
   - If "full" or unspecified: run all categories (custom, knowledge graph, semantic, QA, reasoning, compression).
   - If "performance" or "speed": focus on performance benchmarks (ASI orchestrator, lock-free, production, runtime, vector search).
   - If "flux accuracy" or "geometric": run flux position accuracy and geometric reasoning benchmarks.

2. **Setup & Prerequisites Check**
   - Confirm required files exist: benchmarks/Cargo.toml, benchmarks/src/, datasets/ (if needed).
   - Check hardware (CPU cores, memory), Rust environment (cargo, target/release).
   - If missing datasets → suggest running: `./benchmarks/scripts/download_datasets.sh`
   - Load previous results from benchmark_results.json (if exists) for comparison.

3. **Execute Benchmarks**
   - Run main harness: `cargo run --release --bin run_benchmarks` from benchmarks/ directory.
   - For performance tests: `cargo bench` for criterion-based performance benchmarks.
   - For specific categories: `cargo test --release custom` or `cargo test --release performance`.
   - Capture: raw scores, runtime, hardware info, git commit hash.

4. **Analyze & Compare**
   - Parse JSON output → compute deltas (e.g., +111.1% improvement vs GPT-4 baseline).
   - Flag regressions or big wins (e.g., "95% flux accuracy — new high!").
   - Categorize:
     - Custom SpatialVortex: Flux position, ELP accuracy, sacred boost, geometric reasoning, humanities exam
     - Performance: ASI orchestrator latency, lock-free ops/sec, production throughput
     - Traditional: Knowledge graphs (MRR), semantic similarity (STS), QA accuracy, reasoning scores

5. **Generate Report**
   Always output in this markdown format:

   ```markdown
   # SpatialVortex Benchmark Run – [Date / Commit]

   **Model/Version**: SpatialVortex [branch/commit]
   **Hardware**: [GPU/CPU details]
   **Date**: [today]

   ## Summary
   - Overall Score: XX% (↑/↓ vs previous)
   - Flux Position Accuracy: XX% (vs GPT-4: 45% → +XX% improvement)
   - ELP Channel Accuracy: XX% (vs BERT: 60% → +XX% improvement)
   - Geometric Reasoning: XX% (vs Claude 3: 48% → +XX% improvement)

   ## Detailed Results

   | Category              | Metric          | Score     | vs Previous | vs SOTA/Baseline | Notes |
   |-----------------------|-----------------|-----------|-------------|------------------|-------|
   | Custom SpatialVortex  | Flux Position   | 0.XX     | +0.XX       | GPT-4 0.45       | 95% target |
   | Custom SpatialVortex  | ELP Accuracy    | 0.XX     | +0.XX       | BERT 0.60        | 87% target |
   | Custom SpatialVortex  | Sacred Boost    | 0.XX     | +0.XX       | Random 0.33      | 98% target |
   | Custom SpatialVortex  | Geometric Reasoning | 0.XX | +0.XX       | Claude 3 0.48    | 96% target |
   | Custom SpatialVortex  | Humanities Exam | 0.XX     | +0.XX       | Claude 3 Opus 0.868 | 88% target |
   | Performance           | ASI Orchestrator | X ms    | -X%         | -                | Latency |
   | Performance           | Lock-Free Ops   | X M/sec  | +X%         | -                | 70M target |

   ## Key Insights
   - Strengths: [e.g., superior geometric reasoning, 111.1% improvement over GPT-4]
   - Weaknesses: [e.g., humanities exam still below Claude 3 Opus]
   - Optimizations: Try optimizing lock-free structures, improve ELP channel alignment, profile with criterion.

   ## Next Actions
   - Commit results: git add benchmark_results.json && git commit -m "Benchmark: [date] run"
   - PR to main or results/ folder.
   - Submit to PapersWithCode if > SOTA in any category.
   - Rerun with --release for optimized builds?
   ```

## Available Commands

### Primary Benchmark Commands
```bash
# Run all benchmarks
cd benchmarks
cargo run --release --bin run_benchmarks

# Run specific categories
cargo test --release custom                    # Custom SpatialVortex benchmarks
cargo test --release performance               # Performance benchmarks
cargo test --release knowledge_graph          # Knowledge graph benchmarks
cargo test --release semantic                 # Semantic similarity
cargo test --release qa                       # Question answering
cargo test --release reasoning                # Reasoning tasks
cargo test --release compression              # Compression benchmarks

# Performance-specific benchmarks
cargo bench                                   # All criterion benchmarks
cargo bench --bench asi_orchestrator_bench    # ASI orchestrator performance
cargo bench --bench lock_free_performance     # Lock-free operations
cargo bench --bench production_benchmarks     # End-to-end performance

# Quick smoke test
cargo test --release --features quick
```

### Dataset Management
```bash
# Download required datasets
chmod +x benchmarks/scripts/download_datasets.sh
./benchmarks/scripts/download_datasets.sh

# Verify dataset integrity
chmod +x benchmarks/scripts/verify_datasets.sh
./benchmarks/scripts/verify_datasets.sh
```

### Results and Output
- **JSON Output**: `benchmark_results.json` (saved automatically)
- **Previous Results**: Load from existing `benchmark_results.json` for comparison
- **Performance Reports**: Criterion generates HTML reports in `target/criterion/`

## Benchmark Categories

### 1. Custom SpatialVortex Benchmarks
- **Flux Position Accuracy**: Predict correct vortex position (0-9)
- **ELP Channel Accuracy**: Ethos/Logos/Pathos alignment scoring
- **Sacred Boost Verification**: Verify +15% confidence at positions 3-6-9
- **Geometric Reasoning**: Sacred geometry-based inference tasks
- **Humanities Final Exam**: Complex reasoning across multiple domains

### 2. Performance Benchmarks
- **ASI Orchestrator**: Execution mode latency and throughput
- **Lock-Free Performance**: Concurrent data structure operations (70M ops/sec target)
- **Production Benchmarks**: End-to-end pipeline performance
- **Runtime Performance**: Vortex cycle and beam tensor operations
- **Vector Search**: Embedding similarity and retrieval speed

### 3. Traditional AI Benchmarks
- **Knowledge Graphs**: FB15k-237, WN18RR (MRR, Hits@K)
- **Semantic Similarity**: STS Benchmark, SICK (Pearson correlation)
- **Question Answering**: SQuAD 2.0, CommonsenseQA (EM, F1, accuracy)
- **Reasoning**: bAbI tasks, CLUTRR (accuracy)
- **Compression**: Silesia, neural compression

## SOTA Baselines for Comparison

| Benchmark | SOTA Model | Score | Year |
|------------|-------------|--------|------|
| Flux Position | GPT-4 | 0.45 | 2024 |
| ELP Accuracy | BERT Sentiment | 0.60 | 2023 |
| Sacred Boost | Random | 0.33 | - |
| Geometric Reasoning | Claude 3 | 0.48 | 2024 |
| Humanities Exam | Claude 3 Opus | 0.868 | 2024 |
| FB15k-237 | NodePiece | 0.545 MRR | 2024 |
| STS Benchmark | GPT-4 Turbo | 0.892 Pearson | 2024 |
| SQuAD 2.0 | GPT-4 | 93.2 EM | 2024 |
| CommonsenseQA | GPT-4 Turbo | 88.9% | 2024 |

## Target Performance Goals

- **Flux Position Accuracy**: 95% (vs GPT-4: 45% → +111% improvement)
- **ELP Channel Accuracy**: 87% (vs BERT: 60% → +45% improvement)
- **Sacred Boost**: 98% (vs Random: 33% → +197% improvement)
- **Geometric Reasoning**: 96% (vs Claude 3: 48% → +100% improvement)
- **Humanities Exam**: 88% (vs Claude 3 Opus: 86.8% → +1.4% improvement)
- **Lock-Free Operations**: 70M ops/sec
- **ASI Orchestrator Latency**: <50ms
- **Vector Search**: <10ms for top-k retrieval