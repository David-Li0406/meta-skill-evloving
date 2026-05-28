# AI Engineering Skill Reference — Chapter 9: Inference Optimization

Use this file to diagnose, optimize, and operate LLM inference systems for lower latency and cost, with concrete procedures, code patterns, and decision frameworks.

---

## Quickstart: The Optimization Order

1) Measure the right things
- Implement metrics: TTFT, TPOT, throughput (TPS), goodput vs SLO, MFU, MBU, p50/p95/p99
- Record context length, output length, batch size, concurrency, and tokenizer used

2) Diagnose bottleneck
- Use a roofline view (Nsight, perf tools) to classify as compute-bound vs memory-bandwidth-bound
- LLM rule of thumb:
  - Prefill = compute-bound
  - Decode = memory-bandwidth-bound

3) Apply high-ROI optimizations first
- Weight-only quantization (INT8/INT4), flash attention kernels, dynamic/continuous batching
- vLLM with PagedAttention and prefix caching
- torch.compile or TensorRT-LLM for kernel/graph-level speedups

4) Improve throughput without breaking UX
- Continuous batching
- Decouple prefill/decoding across instances
- Prompt/prefix/KV caching

5) Scale via parallelism
- Replica parallelism first
- Tensor parallelism next (for larger models or latency reduction)
- Avoid pipeline parallelism for low-latency online serving if possible

6) Re-evaluate metrics and cost
- Track goodput (requests satisfying SLO)
- Compute cost per request/token with updated throughput
- Iterate

---

## Core Metrics and Formulas

### Latency metrics
- TTFT (time to first token): dominated by prefill; input-length dependent
- TPOT (time per output token): dominated by decode; output-length dependent
- Total latency ≈ TTFT + TPOT × (# output tokens)
- Always report percentiles (p50/p95/p99) and segment by input tokens

### Throughput vs Goodput
- Throughput: tokens/s or completed requests/min across all users
- Goodput: requests/s that satisfy SLO (e.g., TTFT ≤ 200 ms, TPOT ≤ 100 ms)
- Optimize for goodput, not raw throughput

### Utilization
- MFU (Model FLOP/s Utilization): observed throughput vs theoretical peak FLOP/s (higher in prefill)
- MBU (Model Bandwidth Utilization): used bandwidth / theoretical peak
  - Used bandwidth ≈ parameter_count × bytes/param × tokens/s

Example:
- 7B params in FP16 (2 bytes/param), 100 tokens/s
- Used BW = 7e9 × 2 × 100 = 1.4e12 bytes/s = 1.4 TB/s
- On 2 TB/s device: MBU = 70%

### Cost calculations
- If instance costs $C/hour and decodes D tokens/s:
  - $ per 1M output tokens ≈ (C / 3600) / D × 1e6
- Prefill cost similarly with input tokens/s or requests/min

### KV cache size (no optimizations)
- KV bytes = 2 × B × S × L × H × M
  - B: batch size
  - S: sequence length (context)
  - L: # Transformer layers
  - H: hidden size
  - M: bytes per value (e.g., 2 for FP16, 1 for INT8)

---

## Diagnose Bottlenecks: Procedure

1) Baseline measurement
- Log TTFT, TPOT, throughput, MFU, MBU, p50/p95/p99
- Capture input/output token lengths and SLO compliance

2) Roofline profile
- Nsight Systems/Compute or vendor tools to see compute vs bandwidth bound during prefill vs decode
- Expect: Prefill (high MFU, low MBU), Decode (low MFU, high MBU)

3) Workload characteristics
- Context length distribution, output length distribution
- Concurrency patterns, queueing delays, batch fill ratios
- Tokenizer effects (different models = different token counts for same text)

4) Pick targeted fixes (see decision tables below)

---

## Hardware Selection: Decision Guide

- If compute-bound: favor higher peak FLOP/s, efficient tensor cores, compiler/kernels
- If memory-bandwidth-bound: favor higher HBM bandwidth, lower bytes/param via quantization, KV cache optimizations

Key hardware characteristics
- Peak FLOP/s by precision (FP16/BF16/FP8/INT8)
- HBM bandwidth (TB/s)
- HBM capacity (GB)
- Interconnect (NVLink, PCIe, fabric)
- Power (TDP) if on-prem

---

## High-ROI Model-Level Optimizations

### Quantization (Best default)
- What: Weight-only 8-bit or 4-bit
- Why: Cuts bandwidth and memory footprint; accelerates decode; minimal quality loss when done properly
- Tools: bitsandbytes (LLM.int8/LLM.int4), GPTQ, AWQ, TensorRT-LLM quantization
- When:
  - Always try for inference
  - Start with 8-bit weight-only; test 4-bit for further gains
- Risks:
  - Some tasks sensitive (math/code); validate with task-specific evals
- Code (PyTorch + bitsandbytes):
```python
# pip install transformers accelerate bitsandbytes
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True,  # use load_in_4bit=True for 4-bit
)
```

### Distillation
- What: Train smaller model to mimic larger one
- When: Serving cost/latency constraints require smaller footprint; stable domain/task
- Risks: Training cost and data curation; domain drift

### Pruning (Use selectively)
- What: Zero or remove least-important weights
- When: Tight memory constraints, specialized hardware supporting sparsity
- Risks: Implementation complexity, kernel support, smaller gains than quantization in practice

---

## Speeding Up Autoregressive Decoding

### Speculative decoding (High practical impact)
- Idea: Fast draft model proposes K tokens; target model verifies in parallel; accept longest matching prefix; target adds one token; repeat
- Benefits:
  - Turns sequential decode into parallel verification
  - Significant latency reduction if acceptance rate high
- When: Bandwidth-bound decode; availability of weaker draft model with shared tokenizer
- Trade-offs: Complexity, extra model management; less helpful if MFU is already maxed
- Pseudocode:
```python
# target_model: main LLM; draft_model: smaller/faster model; both share tokenizer
context = tokenizer(prompt, return_tensors="pt").to(device)
while not done:
    # 1) draft K tokens
    draft_ids = generate_with(draft_model, context, max_new_tokens=K, do_sample=True)

    # 2) verify in parallel
    # Compute target logits for each position conditioned on context
    logits = target_model(input_ids=context["input_ids"])
    # Efficiently score acceptance from left to right
    accepted = longest_prefix_accepted(logits, draft_ids)

    # 3) append accepted tokens
    context["input_ids"] = torch.cat([context["input_ids"], accepted], dim=-1)

    # 4) target generates 1 more token to stabilize
    next_id = generate_with(target_model, context, max_new_tokens=1, do_sample=True)
    context["input_ids"] = torch.cat([context["input_ids"], next_id], dim=-1)
```
- Frameworks: vLLM, TensorRT-LLM, llama.cpp have built-in support

### Inference with reference (Copy from input)
- Idea: Identify spans in input likely to be repeated; copy tokens instead of generating
- When: Long contexts with overlap in output (RAG, code edits, document Q&A)
- Gains: Up to 2× speedups in overlap-heavy cases
- Trade-offs: Needs span-matching/search; limited if outputs diverge

### Parallel decoding (Advanced)
- Lookahead/Jacobi decoding, Medusa heads
- When: Extremely latency-sensitive, can invest in added engineering/training
- Trade-offs: Implementation complexity, verification overhead; may require finetuning extra heads

---

## Attention Mechanism Optimizations

### KV cache management (Essential for long contexts)
- Problems: KV memory grows with sequence length and batch size; dominates memory and bandwidth
- Techniques:
  - PagedAttention (vLLM): blocks + non-contiguous allocation to reduce fragmentation, enable sharing
  - KV cache quantization (INT8/FP8): reduces bytes per value
  - Adaptive compression/eviction: compress old segments; drop least-informative spans
  - Selective KV caching: limit cache to useful positions
- When: Long context, high concurrency, memory pressure

vLLM launch with PagedAttention + prefix caching:
```bash
pip install vllm
python -m vllm.entrypoints.api_server \
  --model meta-llama/Llama-2-7b-chat-hf \
  --max-model-len 8192 \
  --tensor-parallel-size 2 \
  --enable-prefix-caching \
  --enforce-eager  # optional; try both eager/graph
```

### Redesign attention (requires retraining/finetuning)
- Local windowed attention + periodic global tokens: reduce KV and attention compute
- Multi-Query Attention (MQA) / Grouped-Query Attention (GQA): share K/V across heads; big KV reduction
- Cross-layer K/V sharing: reuse KV across adjacent layers
- When: You control training/finetuning; long-context workloads
- Gains: Order-of-magnitude KV reduction possible in production

### Optimized kernels (drop-in speedups)
- FlashAttention v2/v3: fused attention kernels; large gains
- Use compiler toolchains to target your hardware (see next section)

---

## Compilers and Kernel Toolchains

- torch.compile (PyTorch 2+): Graph capture + kernel fusion
- TensorRT-LLM: NVIDIA-optimized graphs/kernels; quantization; speculative decoding
- OpenXLA/XLA: graph compilation for accelerators
- TVM/MLIR: customizable lowering pipelines

Recommended workflow
1) Start with torch.compile on PyTorch models
2) Benchmark TensorRT-LLM conversion if on NVIDIA GPUs
3) Ensure fused attention kernels are active (FlashAttention)
4) Profile gains vs baseline

Examples

PyTorch torch.compile:
```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf").cuda()
compiled_model = torch.compile(model, mode="max-autotune")  # try default, reduce-overhead, max-autotune
```

TensorRT-LLM convert + run (simplified):
```bash
# Install TensorRT-LLM and convert a HuggingFace model to engine(s)
trtllm_build \
  --checkpoint_dir ./llama2-7b \
  --gpt_attention_plugin float16 \
  --output_dir ./engine \
  --tp_size 2 \
  --enable_context_fmha

# Run server
python3 examples/python/launch_server.py --engine_dir ./engine --port 8000
```

---

## Inference Service Optimizations

### Batching (Always do it; tune carefully)
- Static batching: fixed batch size; max efficiency but can harm latency
- Dynamic batching: batch up to N or timeout T ms (best default)
- Continuous (in-flight) batching: return completed responses early; refill batch slots on-the-fly (best for LLMs)

Dynamic + continuous batching loop (pseudo):
```python
# Queue with timestamps
queue = deque()

def schedule(now):
    batch = []
    while queue and len(batch) < MAX_BATCH:
        if now - queue[0].enq_time >= MAX_WAIT_MS or len(batch) == 0:
            batch.append(queue.popleft())
        else:
            # Fill more if available to improve compute efficiency
            if len(batch) < MAX_BATCH and len(queue) > 1:
                batch.append(queue.popleft())
            else:
                break
    return batch

# Continuous refill: after any sequence finishes, immediately pull a new request to reuse slot
```

Tuning tips
- Choose MAX_WAIT_MS to keep p95 TTFT/TPOT within SLO (start 50–200 ms)
- Monitor batch fill ratio and wasted slots
- Stream tokens to users while maintaining backend batching

### Decouple prefill and decode (High impact)
- Separate instances/pools for prefill (compute-bound) vs decode (bandwidth-bound)
- Benefits: Avoid resource interference; tune instance ratios based on workload
- Ratios (starting points):
  - Long inputs, TTFT priority: prefill:decode = 2:1 to 4:1
  - Short inputs, TPOT priority: 1:1 to 1:2
- Requirements: High-bandwidth interconnect (e.g., NVLink) reduces transfer overhead

Architecture steps
1) Router tags requests and context-lengths
2) Prefill pool handles tokenization + KV init
3) Transfer KV state to decode pool
4) Decode pool streams tokens; continuous batching within decode pool

### Prompt/context/prefix caching (Big savings with overlaps)
- Cache reusable prompt segments (system prompts, long docs, multi-turn history)
- Benefits: Reduced TTFT and input token cost
- Implementation options:
  - Use provider feature (e.g., prompt caching APIs)
  - Use engine with prefix caching (vLLM: --enable-prefix-caching)
  - Custom: cache KV for prefixes keyed by content hashes

Caveats
- Cache storage consumes memory; plan eviction (LRU) and TTL
- Ensure deterministic tokenization; normalize whitespace and casing
- Align cache granularity (whole-system prompt vs chunked segments)

---

## Parallelism Strategies (When and How)

- Replica parallelism (default scale-out)
  - What: Multiple independent model replicas
  - When: Increase concurrency; low engineering effort
  - Trade-offs: GPU allocation/bin-packing; per-replica memory overhead

- Tensor (intra-op) parallelism
  - What: Split tensors/ops across devices; accelerate matmuls
  - When: Model > single GPU memory; latency reductions desired
  - Trade-offs: Cross-device comms; topology matters

- Pipeline parallelism
  - What: Split layers across devices; micro-batching to overlap stages
  - When: Training and batched workloads optimizing throughput
  - Avoid: Low-latency online serving (increased per-request latency)

- Context parallelism
  - What: Split input sequence across devices for long-context processing
  - When: Extremely long contexts; you can restructure attention
  - Trade-offs: Synchronization and code complexity

- Sequence parallelism
  - What: Split operators across devices (e.g., attention on GPU0, MLP on GPU1)
  - When: Specialized pipelines; long-context efficiency
  - Trade-offs: Operator placement complexity

---

## Decision Tables

### Technique vs Goals

| Technique                    | TTFT | TPOT | Throughput | Cost | Quality risk | Complexity |
|-----------------------------|------|------|------------|------|--------------|------------|
| Weight-only INT8 quant      | ↓    | ↓    | ↑          | ↓    | Low          | Low        |
| Weight-only INT4 quant      | ↓    | ↓    | ↑↑         | ↓↓   | Med          | Low/Med    |
| FlashAttention kernels      | ↓    | ↓    | ↑          | ↓    | None         | Low        |
| torch.compile               | ↓    | ↓    | ↑          | ↓    | None         | Low        |
| TensorRT-LLM                | ↓    | ↓    | ↑↑         | ↓    | None         | Med        |
| Speculative decoding        | —    | ↓    | ↑          | ↓    | None         | Med        |
| Prompt/prefix caching       | ↓↓   | —    | ↑          | ↓↓   | None         | Med        |
| Decouple prefill/decode     | ↓    | ↓    | ↑          | ↓    | None         | Med        |
| Dynamic/continuous batching | —    | ↕    | ↑↑         | ↓    | None         | Med        |
| MQA/GQA/cross-layer KV      | ↓    | ↓    | ↑          | ↓    | Needs retrain| High       |
| Pruning                     | ↕    | ↕    | ↕          | ↕    | Med/High     | High       |

Legend: ↓ improves (lower), ↑ improves (higher), — neutral, ↕ varies

### Compute vs Bandwidth Bound: What to Do

| Bottleneck              | Symptoms                                  | Do this first                                          |
|-------------------------|-------------------------------------------|--------------------------------------------------------|
| Compute-bound (prefill) | High MFU, low MBU; TTFT too high          | torch.compile, FlashAttention, TensorRT-LLM, batching  |
| Bandwidth-bound (decode)| Low MFU, high MBU; TPOT too high          | Quantization (INT8/INT4), speculative decoding, GQA/MQA|
| Memory capacity         | OOM, limited batch sizes                  | KV optimizations, quantize KV, tensor parallelism      |

---

## Cost/Latency Playbooks

1) Reduce TTFT (long inputs)
- Prefix/prompt caching
- Dynamic batching (short max_wait_ms)
- Decouple prefill (more prefill instances)
- torch.compile + FlashAttention
- Quantize weights (helps prefill as well)

2) Reduce TPOT (long outputs)
- Quantize weights (bandwidth)
- Speculative decoding
- Decouple decode (more decode instances)
- Continuous batching

3) Handle long contexts (memory pressure)
- vLLM with PagedAttention + prefix caching
- KV cache quantization/compression/selective retention
- Model choices with MQA/GQA/local attention (if retraining possible)
- Tensor parallelism

4) Improve throughput without hurting UX
- Continuous batching + streaming
- Schedule with SLO-aware goodput targets
- RPS throttling based on p95 TTFT/TPOT

---

## SLO and Goodput Implementation

SLO example
- TTFT ≤ 200 ms (p95)
- TPOT ≤ 120 ms (p95)
- Error rate ≤ 0.1%

Goodput calculation
```python
def goodput(request_logs, slo):
    ok = 0
    for r in request_logs:
        if r['ttft_ms'] <= slo['ttft_ms'] and r['tpot_ms'] <= slo['tpot_ms'] and r['error']==False:
            ok += 1
    return ok / (sum(1 for _ in request_logs)) * (60 / observation_minutes)  # per minute
```

---

## Monitoring and Alerting Checklist

- Latency: TTFT/TPOT p50/p95/p99; time between tokens; time to publish (if agentic)
- Throughput: TPS; completed requests/min; tokens/s/user
- Utilization: MFU/MBU; batch fill ratio; cache hit rate (prefix/KV)
- Errors: OOM, request timeouts, throttling events
- Costs: $/1M input tokens; $/1M output tokens; $/req
- Capacity: GPU mem usage; KV cache occupancy; queue time
- SLO: Goodput, violations per minute

---

## Practical Code Patterns

### Streaming + Continuous Batching (vLLM Python)
```python
# pip install vllm
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-2-7b-chat-hf", tensor_parallel_size=2)

sampling_params = SamplingParams(
    temperature=0.7, top_p=0.9, max_tokens=512, stream=True
)

prompts = [
    "Summarize this document: ...",
    "Write SQL for ...",
]
for output in llm.generate(prompts, sampling_params):
    for token in output.outputs[0].token_ids_stream:
        # stream token to client
        pass
```

### Prefix Caching (vLLM CLI)
```bash
python -m vllm.entrypoints.api_server \
  --model meta-llama/Llama-2-7b-chat-hf \
  --enable-prefix-caching \
  --max-model-len 32768
```

### Dynamic Batching Gate (pseudo)
```python
MAX_BATCH = 32
MAX_WAIT_MS = 100

while True:
    now = time.monotonic() * 1000
    batch = []
    while len(batch) < MAX_BATCH and queue:
        if len(batch) == 0:
            req = queue.popleft()
            batch.append(req)
            start = req.enqueued_at
        else:
            if now - start >= MAX_WAIT_MS:
                break
            batch.append(queue.popleft())
    if batch:
        submit_to_engine(batch)
```

### Weight-only INT4 with GPTQ (conversion)
```bash
# pip install auto-gptq optimum
python -m auto_gptq.eval_quant \
  --model_id meta-llama/Llama-2-7b-hf \
  --bits 4 \
  --dataset wikitext2 \
  --save_dir ./llama2-7b-gptq
```

---

## Common Pitfalls and Fixes

- Averaging latency hides outliers → Always use percentiles; bucket by input length
- Counting both input and output tokens together → Separate prefill vs decode metrics
- High GPU utilization via nvidia-smi ≠ efficiency → Track MFU/MBU instead
- Over-batching harms TTFT → Cap max_wait_ms and monitor p95 TTFT
- Ignoring tokenizer differences → Normalize token accounting across models
- KV cache explosion → Use PagedAttention, quantize KV, limit context, use MQA/GQA
- Speculative decoding without acceptance tuning → Calibrate K and draft model size
- Pipeline parallelism in online serving → Prefer tensor/replica for latency
- No prompt cache in multi-turn apps → Implement prefix/prompt caching immediately

---

## Implementation Playbooks

### A) LLM API Service (Open-source stack) — Latency-first

1) Engine
- vLLM with PagedAttention, prefix caching, continuous batching
- Tensor parallel size tuned to GPUs available

2) Model
- Quantize weights to INT8; evaluate INT4
- Enable FlashAttention; torch.compile if using PyTorch models directly

3) Scheduling
- Dynamic batching MAX_WAIT_MS ≤ 100 ms; stream tokens
- Decouple prefill/decode if workload skews long inputs

4) Caching
- Precompute and cache system prompts
- Hash-based prefix cache for recurring docs/sessions

5) Monitoring
- p95 TTFT ≤ 200 ms, TPOT ≤ 120 ms; goodput ≥ target
- Cache hit rate; KV memory footprint; batch fill ratio

### B) Batch API — Cost-first

1) Increase batching windows significantly (seconds)
2) Use cheaper hardware; maximize utilization (MBU/MFU)
3) Aggressive quantization (INT4), speculative decoding
4) Schedule during off-peak hours
5) Strict throttling to maintain high batch fill ratios

---

## Choosing Techniques: Quick Reference

- You have long contexts (RAG, codebases, books)
  - vLLM + PagedAttention + prefix caching
  - Quantize KV; MQA/GQA if retraining
  - Decouple prefill; shorter TTFT SLO

- You have long outputs (generation-heavy)
  - Speculative decoding; weight-only INT8/INT4
  - Decouple decode; continuous batching; tune sampling params

- You need max throughput at fixed cost
  - Continuous batching; increase MAX_WAIT_MS carefully
  - INT4 quantization; TensorRT-LLM; tune batch size and parallelism
  - Goodput over throughput to avoid SLO violations

- You’re OOM or constrained by GPU memory
  - Quantize weights and KV; tensor parallelism
  - Reduce max context; selective KV retention
  - Smaller distilled models for task

---

## Validation Checklist Before/After Each Change

- Functional:
  - Outputs consistent (quality checks on critical tasks)
  - Deterministic tokenization and caching keys

- Performance:
  - TTFT/TPOT p50/p95/p99 improved or within SLO
  - Goodput increased or stable
  - MFU/MBU trending correctly for targeted bottleneck

- Cost:
  - $/1M input and output tokens down
  - GPU hours per workload down

- Stability:
  - Error rates unchanged
  - OOM incidents, throttling, queue times acceptable

---

## Reference Equations and Rules-of-Thumb

- Total latency ≈ TTFT + TPOT × output_tokens
- Goodput = completed_requests_per_sec_that_meet_SLO
- Used bandwidth (bytes/s) ≈ params × bytes/param × tokens/s
- KV size (bytes) = 2 × B × S × L × H × M
- Prefill typically compute-bound; decode typically bandwidth-bound
- As a rough heuristic, one output token can cost as much as ~100 input tokens in latency impact (plan batching and caching accordingly)

---

## Tooling Summary

- Engines: vLLM (PagedAttention, prefix caching, in-flight batching), TensorRT-LLM
- Compilers: torch.compile, TensorRT, OpenXLA
- Quantization: bitsandbytes, GPTQ, AWQ, TensorRT-LLM quant
- Profilers: Nsight Systems/Compute, PyTorch profiler
- Providers (features to look for): prompt caching with discounted tokens and storage pricing; batch API with lower costs

---

This reference gives you the procedures and concrete patterns to reduce latency and cost for LLM inference. Start with quantization + fused attention + continuous batching, add prefix caching, then decouple prefill/decode and consider speculative decoding. Always measure goodput against your SLOs and iterate.