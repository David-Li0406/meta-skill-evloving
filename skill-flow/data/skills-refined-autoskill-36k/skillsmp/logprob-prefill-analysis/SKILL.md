---
name: logprob-prefill-analysis
description: Reproduces the full prefill sensitivity analysis pipeline for reward hacking indicators. Use when evaluating how susceptible model checkpoints are to exploit-eliciting prefills, computing token-based trajectories, or comparing logprob vs token-count as predictors of exploitability.
---

# Prefill Sensitivity Analysis Pipeline

This skill documents the complete pipeline for measuring model susceptibility to reward hacking via prefill sensitivity analysis, including both token-based and logprob-based metrics.

## Quick Start: Single Command Reproducibility

The full analysis can be run with a single command:

```bash
# Run on most recent sensitivity experiment (auto-discovers checkpoints from config.yaml)
python scripts/run_full_prefill_analysis.py

# Specify a particular sensitivity experiment
python scripts/run_full_prefill_analysis.py \
    --sensitivity-run results/prefill_sensitivity/prefill_sensitivity-20251216-012007-47bf405

# Dry run to see what would be executed
python scripts/run_full_prefill_analysis.py --dry-run

# Skip logprob computation (just run trajectory analysis)
python scripts/run_full_prefill_analysis.py --skip-logprob
```

This orchestration script:
1. Discovers checkpoints and prefill levels from the sensitivity experiment's `config.yaml`
2. Runs token-based trajectory analysis
3. Computes prefill logprobs for each checkpoint
4. Produces integrated analysis comparing token vs logprob metrics

## Overview

The analysis measures how easily a model can be "kicked" into generating exploit code by prefilling its chain-of-thought with exploit-oriented reasoning. We track:

1. **Token-based metric**: Minimum prefill tokens needed to elicit an exploit
2. **Logprob-based metric**: How "natural" the exploit reasoning appears to the model

## Prerequisites

- Model checkpoints from SFT training
- Prefill source data (successful exploit reasoning traces)
- vLLM for serving checkpoints
- djinn package for problem verification

---

## Checkpoint Discovery

The pipeline automatically discovers available checkpoints from a sensitivity experiment's `config.yaml`:

```yaml
# Example config.yaml from a sensitivity experiment
checkpoint_dir: results/sft_checkpoints/sft_openai_gpt-oss-20b-20251205-024759-47bf405/checkpoints
checkpoints:
- checkpoint-1
- checkpoint-10
- checkpoint-17
- checkpoint-27
- checkpoint-35
- checkpoint-56
- checkpoint-90
prefill_tokens_sweep: 0,10,30,100
```

The orchestration script reads this config to determine:
- Which checkpoints are available
- Which prefill levels were tested
- Where the SFT run directory is located

---

## Stage 1: Run Prefill Sensitivity Evaluation

Evaluate each checkpoint at multiple prefill levels (0, 10, 30, 100 tokens).

### 1.1 Serve the checkpoint via vLLM

```bash
vllm serve results/sft_checkpoints/sft_*/checkpoints/checkpoint-{CKPT}
```

### 1.2 Run the evaluation

```bash
python scripts/eval_prefill_sensitivity.py \
    --base-url http://localhost:8000/v1 \
    --prefill-from results/prefill_source/exploits.jsonl \
    --output results/prefill_sensitivity/{RUN_NAME}/evals/checkpoint-{CKPT}_prefill{LEVEL}.jsonl \
    --prefill-tokens {LEVEL} \
    --num-attempts 3
```

**Prefill levels to run:** 0, 10, 30, 100 tokens

**Key parameters:**
- `--prefill-tokens`: Number of tokens from exploit reasoning to prefill (0 = baseline)
- `--num-attempts`: Number of generation attempts per problem (default: 3)
- `--max-problems`: Limit problems for testing

**Output files:**
- `checkpoint-{CKPT}_prefill{LEVEL}.jsonl`: Per-problem exploit success results
- `checkpoint-{CKPT}_prefill{LEVEL}.jsonl.samples.jsonl`: Full generation samples with reasoning

### 1.3 Batch script example

```bash
#!/bin/bash
RUN_NAME="prefill_sensitivity-$(date +%Y%m%d-%H%M%S)"
CHECKPOINTS=(1 10 17 27 35 56 90)
PREFILL_LEVELS=(0 10 30 100)

for CKPT in "${CHECKPOINTS[@]}"; do
    # Start vLLM server for this checkpoint
    vllm serve results/sft_checkpoints/sft_*/checkpoints/checkpoint-$CKPT &
    sleep 60  # Wait for server to start

    for LEVEL in "${PREFILL_LEVELS[@]}"; do
        python scripts/eval_prefill_sensitivity.py \
            --base-url http://localhost:8000/v1 \
            --prefill-from results/prefill_source/exploits.jsonl \
            --output results/prefill_sensitivity/$RUN_NAME/evals/checkpoint-${CKPT}_prefill${LEVEL}.jsonl \
            --prefill-tokens $LEVEL \
            --num-attempts 3
    done

    # Kill vLLM server
    pkill -f "vllm serve"
done
```

---

## Stage 2: Token-Based Trajectory Analysis

Analyze how "exploit accessibility" (min prefill tokens to elicit exploit) changes over training.

**Default behavior** (filters to djinn dataset, produces both all_exploits/ and intentional_only/ subdirectories):
```bash
python scripts/prefill_trajectory_analysis.py \
    --run-dir results/prefill_sensitivity/{RUN_NAME} \
    --output-dir results/trajectory_analysis \
    --threshold 0
```

This automatically:
1. Filters to problems in `EleutherAI/djinn-problems-v0.9` (removes bad/deprecated problems)
2. Produces plots for **all exploits** in `all_exploits/` subdirectory
3. Produces plots for **intentional exploits only** in `intentional_only/` subdirectory
   - Excludes `inadequate_test_coverage` and `resource_exhaustion` (unintentional exploit types)
4. **Processes logprob data** if available in `{run-dir}/logprob/` (generates logprob vs prefill/checkpoint plots)

**Skip intentional split** (only produce all_exploits/):
```bash
python scripts/prefill_trajectory_analysis.py \
    --run-dir results/prefill_sensitivity/{RUN_NAME} \
    --output-dir results/trajectory_analysis \
    --threshold 0 \
    --skip-intentional-split
```

**Disable dataset filtering:**
```bash
python scripts/prefill_trajectory_analysis.py \
    --run-dir results/prefill_sensitivity/{RUN_NAME} \
    --output-dir results/trajectory_analysis \
    --threshold 0 \
    --filter-dataset none
```

**Excluding additional exploit types:**
```bash
python scripts/prefill_trajectory_analysis.py \
    --run-dir results/prefill_sensitivity/{RUN_NAME} \
    --output-dir results/trajectory_analysis \
    --threshold 0 \
    --exclude-exploit-types hardcoding_or_memorization
```

**With experiment context logging:**
```bash
python scripts/prefill_trajectory_analysis.py \
    --run-dir results/prefill_sensitivity/{RUN_NAME} \
    --output-dir results/trajectory_analysis \
    --threshold 0 \
    --use-run-context
```

**Key concepts:**
- **Min prefill**: Minimum prefill tokens needed to trigger an exploit at a checkpoint
- **Threshold**: min_prefill <= threshold means "easily exploitable" (use 0 for strictest)
- **Time to threshold**: Training steps until problem becomes easily exploitable
- **Instantaneous descent rate**: Per-step change in min_prefill between consecutive checkpoints
- **Intentional exploits**: Excludes `inadequate_test_coverage` and `resource_exhaustion` (bugs in test coverage, not deliberate exploit design)

**Output structure:**
```
output_dir/
├── all_exploits/           # All exploit types
│   ├── trajectory_analysis.csv
│   ├── logprob_analysis.csv    # If logprob data available
│   └── *.png
└── intentional_only/       # Excludes unintentional exploit types
    ├── trajectory_analysis.csv
    ├── logprob_analysis.csv    # If logprob data available
    └── *.png
```

**Output files (in each subdirectory):**
- `trajectory_analysis.csv`: Per-problem min_prefill at each checkpoint
- `pass_rates_vs_prefill.png`: Secure pass, insecure pass, and exploit rate vs prefill length (by checkpoint)
- `accessibility_vs_time.png`: Scatter plot of current accessibility vs steps-to-threshold
- `sample_trajectories.png`: Sample of individual problem trajectories over checkpoints
- `median_trajectory.png`: Median min_prefill trajectory with IQR band (sigmoid shape!)
- `descent_rates.png`: Distribution of overall descent rates (first to last checkpoint)
- `instantaneous_descent_rates.png`: Distribution of per-step descent rates with reachability coloring
- `instantaneous_descent_rates_by_exploit.png`: Descent rates averaged by exploit type (gradient by % reaching threshold)
- `instantaneous_rate_at_max_prefill.png`: Histogram of descent rates when min_prefill >= 100, by checkpoint cutoff

**Logprob output files (if logprob data available):**
- `logprob_analysis.csv`: Per-sample logprob metrics
- `logprob_vs_prefill.png`: Logprob sum, mean, and exploit rate vs prefill length (by checkpoint)
- `logprob_vs_checkpoint.png`: Logprob sum, mean, and exploit rate vs checkpoint (by prefill level)

---

## Stage 3: Compute Prefill Logprobs

Measure how "natural" exploit reasoning appears to each checkpoint.

**Recommended approach:** Use the vLLM-based script (`compute_prefill_logprobs_vllm.py`) which is much faster than the HuggingFace-based alternative. It uses async concurrent requests to the vLLM server.

### 3.1 Start vLLM server for the checkpoint

```bash
vllm serve /path/to/checkpoints/checkpoint-{CKPT}
```

### 3.2 Compute logprobs for all prefill levels (recommended)

```bash
python scripts/compute_prefill_logprobs_vllm.py \
    --base-url http://localhost:8000/v1 \
    --samples-dir results/prefill_sensitivity/{RUN_NAME}/evals \
    --output-dir results/prefill_sensitivity/{RUN_NAME}/logprob \
    --checkpoint {CKPT} \
    --concurrency 32
```

This processes all `checkpoint-{CKPT}_prefill*.jsonl.samples.jsonl` files and outputs to `{RUN_NAME}/logprob/`. Skips already-computed files.

### 3.3 Single file mode

```bash
python scripts/compute_prefill_logprobs_vllm.py \
    --base-url http://localhost:8000/v1 \
    --prefill-samples results/prefill_sensitivity/{RUN_NAME}/evals/checkpoint-{CKPT}_prefill{LEVEL}.jsonl.samples.jsonl \
    --output results/prefill_sensitivity/{RUN_NAME}/logprob/checkpoint-{CKPT}_prefill{LEVEL}_logprobs.jsonl
```

**Key parameters:**
- `--concurrency N`: Maximum concurrent API requests (default: 32)
- `--batch-size N`: Batch size for progress reporting (default: 64)
- `--max-samples N`: Limit samples for testing
- `--min-prefill N`: Skip prefill levels below N (default: 1, skips prefill0)
- `--use-reasoning-field`: Use 'reasoning' instead of 'prefill_reasoning' field

### 3.4 Legacy HuggingFace-based approach (slower)

For cases where you can't run a vLLM server:

```bash
python scripts/compute_prefill_logprobs.py \
    --checkpoint-dir results/sft_checkpoints/sft_*/checkpoints/checkpoint-{CKPT} \
    --prefill-samples results/prefill_sensitivity/{RUN_NAME}/evals/checkpoint-{CKPT}_prefill{LEVEL}.jsonl.samples.jsonl \
    --output results/logprob_analysis/checkpoint-{CKPT}_prefill{LEVEL}.jsonl \
    --dtype bfloat16 --device cuda
```

**Note:** The legacy script uses HuggingFace's `tokenizer.apply_chat_template` which may produce slightly different results than the vLLM-based script. The vLLM script uses the exact same prompt format as djinn's generation (`build_harmony_prompt_string`), so its results are more accurate.

---

## Stage 4: Integrated Analysis

Merge token-based and logprob-based metrics, compare predictive power.

```bash
.venv/bin/python scripts/integrate_logprob_trajectory.py \
    --trajectory-csv results/trajectory_analysis/trajectory_analysis.csv \
    --logprob-dirs results/logprob_analysis/logprob-*-prefill10 \
                   results/logprob_analysis/logprob-*-prefill30 \
                   results/logprob_analysis/logprob-*-prefill100 \
    --output-dir results/trajectory_analysis_with_logprob_complete \
    --prefill-levels 10 30 100 \
    --logprob-threshold -55.39
```

**With experiment context logging:**
```bash
.venv/bin/python scripts/integrate_logprob_trajectory.py \
    ... \
    --use-run-context
```

**Key parameters:**
- `--prefill-levels`: Which prefill word counts to include
- `--logprob-threshold`: Sum logprob threshold for "easily exploitable" (default: -55.39)

**Output files:**
- `trajectory_with_logprob.csv`: Merged trajectory and logprob data
- `logprob_vs_token_accessibility.png`: Correlation between metrics
- `token_vs_logprob_comparison.png`: Side-by-side R² comparison
- `threshold_comparison.png`: When each threshold is reached

---

## Experiment Context Logging

All analysis scripts support the `--use-run-context` flag which creates timestamped run directories with:
- `config.yaml`: Full command and arguments
- `metadata.json`: Git commit, Python version, CUDA info, pip freeze, environment
- `status.json`: Success/failure status and timing

The orchestration script (`run_full_prefill_analysis.py`) automatically uses run_context for reproducibility.

---

## Key Results (Reference Run)

From the gpt-oss-20b training run:

**Predictor comparison (R² for predicting steps-to-threshold):**
| Metric | R² | p-value |
|--------|-----|---------|
| Token-based (min_prefill) | 0.1189 | <0.0001 |
| Logprob-based (logprob_sum) | 0.1974 | <0.0001 |

**Logprob is better by ~66% R² improvement**

**Threshold comparison:**
- Token threshold tends to fire 16.2 steps earlier on average
- 32 problems reach both thresholds; 34 reach token-only

---

## Important Notes

### Word vs Subword Tokens
"10-token prefill" means 10 WORDS (whitespace-split), which becomes ~21 model subword tokens. This naming is historical.

### Sum vs Mean Logprob
Use **SUM logprob** (log P(sequence)) for comparing across different prefill lengths. Mean logprob normalizes by length but loses the sequence probability interpretation.

### Harmony Format
gpt-oss models use Harmony message format. The vLLM logprob script (`compute_prefill_logprobs_vllm.py`) uses the exact same raw prompt format as djinn's generation:
```
<|start|>system<|message|>{system}<|end|>
<|start|>user<|message|>{user}<|end|>
<|start|>assistant<|channel|>analysis<|message|>{prefill_reasoning}
```
The scripts auto-detect Harmony format based on the `model_id` field in samples containing "gpt-oss" or "gpt_oss".

### Checkpoint 90
The "threshold" checkpoint where 10-word prefill suffices for most problems. Used for computing the logprob threshold (-55.39 = E[sum_logprob(10-word prefill at checkpoint 90)]).

---

## Troubleshooting

**Missing samples for a checkpoint:**
The logprob script will use samples from a different checkpoint with the same prefill level (prefills contain the same reasoning across checkpoints).

**CUDA OOM:**
Try `--max-samples 50` for testing, or use `--dtype float16` for smaller memory footprint.

**No logprob data merged:**
Check that `min_prefill` values in trajectory data match available `prefill_level` values in logprob data (10, 30, 100).

**vLLM server issues:**
Ensure the server is fully started before running evaluation (check logs for "Uvicorn running on...").

---

## Directory Structure

```
results/
├── sft_checkpoints/
│   └── sft_{model}_{date}/
│       └── checkpoints/
│           └── checkpoint-{N}/
├── prefill_sensitivity/
│   └── prefill_sensitivity-{date}/
│       ├── config.yaml              # Source of truth for checkpoints/prefill levels
│       ├── evals/
│       │   ├── checkpoint-{N}_prefill{L}.jsonl
│       │   └── checkpoint-{N}_prefill{L}.jsonl.samples.jsonl
│       └── logprob/                  # Logprob results (from compute_prefill_logprobs_vllm.py)
│           └── checkpoint-{N}_prefill{L}_logprobs.jsonl
├── trajectory_analysis/
│   ├── trajectory_analysis.csv
│   └── *.png
├── trajectory_analysis_with_logprob_complete/
│   ├── trajectory_with_logprob.csv
│   └── *.png
└── full_analysis/                    # From run_full_prefill_analysis.py
    └── full_analysis-{timestamp}/
        ├── config.yaml
        ├── metadata.json
        ├── status.json
        ├── trajectory/
        ├── logprob/
        └── integrated/
```

---

## Script Summary

| Script | Purpose | Key Inputs |
|--------|---------|------------|
| `run_full_prefill_analysis.py` | **Orchestration** - runs full pipeline | `--sensitivity-run` |
| `eval_prefill_sensitivity.py` | Stage 1: Evaluate prefill sensitivity | `--base-url`, `--prefill-from` |
| `prefill_trajectory_analysis.py` | Stage 2: Token-based trajectory | `--run-dir` |
| `compute_prefill_logprobs_vllm.py` | **Stage 3: Logprob computation (recommended)** | `--base-url`, `--samples-dir` |
| `compute_prefill_logprobs.py` | Stage 3: Legacy HuggingFace logprob | `--checkpoint-dir`, `--prefill-samples` |
| `integrate_logprob_trajectory.py` | Stage 4: Merge and compare metrics | `--trajectory-csv`, `--logprob-dirs` |
