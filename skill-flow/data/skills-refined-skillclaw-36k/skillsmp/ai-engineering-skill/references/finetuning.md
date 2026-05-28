# Finetuning Reference (Chapter 7)

Use this as a fast, actionable guide to decide when and how to finetune, size hardware, pick methods (LoRA, QLoRA, soft prompts), configure hyperparameters, and deploy/merge adapters.

## Quick Decision Guide: Prompting vs RAG vs Finetuning

- Start here:
  - Do thorough prompt engineering first (clear instructions, examples, evaluation).
  - If frequent failures persist, classify failures:
    - Facts wrong/outdated/missing → add RAG.
    - Form/format/style/safety issues → finetune.

- Practical rule:
  - Finetuning is for form; RAG is for facts.
  - If both present, start with RAG (easier, bigger gains), then finetune if behavior issues remain.

- Escalation flow:
  1. Prompting only → add few-shot examples → add simple retrieval (term-based/BM25).
  2. If info-limited → upgrade to hybrid/embedding RAG.
  3. If behavior-limited → finetune (LoRA first).
  4. Combine RAG + finetuned model if needed.

- When NOT to finetune:
  - Early exploration, unclear metrics, weak prompting experiments.
  - You need up-to-date or private facts (use RAG).
  - You need broad generality (task-specific FT may degrade other tasks).
  - You cannot commit to ongoing maintenance/evaluation.

- When to finetune:
  - Strict output formats (JSON/YAML/SQL/DSL), semantic parsing.
  - Domain-specific dialects (e.g., non-standard SQL; customer-specific queries).
  - Style and safety alignment; reduce bias via curated data.
  - Distill a large model into a small performant one for your task.

## Hardware Sizing and Memory Math (Cheat Sheet)

- Inference memory (approx):
  - Params: N parameters × M bytes/param.
  - Activations + KV cache (typical): ~20% of weights (varies with sequence length and batch size).
  - Rule of thumb: Memory ≈ N × M × 1.2
    - Example: 13B params at 2 bytes → 26 GB weights → ~31.2 GB total.

- Training/Finetuning memory:
  - Memory ≈ weights + activations + gradients + optimizer states.
  - For each trainable parameter:
    - Gradients: 1 value; optimizer states: 0–2 values (SGD=0, Momentum=1, Adam=2).
    - Example (Adam, 16-bit): per trainable param ~3 × 2 bytes = 6 bytes.
    - 7B trainable params → grads+optim ≈ 42 GB (excl. activations).
  - Activation memory can dwarf weights; use gradient checkpointing to trade compute for memory.

- Reduce memory pressure:
  - Reduce trainable params (PEFT/LoRA).
  - Quantize weights/activations/gradients (8/4-bit).
  - Mixed precision (BF16/FP16/FP8/INT8).
  - CPU offloading, paged optimizers (e.g., bitsandbytes).
  - Gradient checkpointing; gradient accumulation to simulate larger batch sizes.

- Numerical formats quick notes:
  - BF16 vs FP16: BF16 has larger range (safer); FP16 higher mantissa precision.
  - Always load models in intended dtype (some LLMs ship BF16 weights; loading in FP16 can degrade quality).

## Method Selection: Full FT vs LoRA vs Soft Prompts

| Method | Trainable params | Data needed | Hardware | Quality | Inference changes | Best for |
|---|---:|---:|---|---|---|---|
| Full finetuning | 100% | High (10k–1M+) | High (multi-GPU) | Highest ceiling | No | Major behavior changes with enough data |
| LoRA (adapters) | <<1%–3% | Low–Medium (1k–50k) | Low–Medium (single GPU) | Near full FT on many tasks | Merge (no overhead) or apply on-the-fly | Structured outputs, multi-tenant adapters |
| Soft prompts | ~few K tokens | Low (≤10k) | Low | Moderate | No model change | Quick lightweight steering, minor behavior tweaks |

Recommended default: Start with LoRA. Use full FT only if you’ve maxed out LoRA or need large capability shifts and have the data/compute.

## LoRA in Practice

### How it works (brief)
- For weight matrix W (n×m), learn low-rank matrices A (n×r), B (r×m). Use W' = W + (α/r)·A·B during training; only A, B are trainable.
- Merge A·B into W for zero-overhead inference, or keep separate for multi-adapter serving.

### Where to apply LoRA
- Default: attention projections Wq, Wk, Wv, Wo across all layers.
- With limited budget, prioritize Wq and Wv.
- For extra gains, include MLP/feedforward layers (often significant improvement).
- Uniform ranks per matrix type are common.

### Hyperparameters (strong defaults)
- r (rank): 8–64 typically sufficient; start with 16 or 32.
- α (alpha): tune ratio α:r in [1:8, 1:1, 8:1]; start α = r.
- Dropout: 0.0–0.1.
- Target modules: ["q_proj","k_proj","v_proj","o_proj"] (+ MLP proj if budget allows).
- Dtype: BF16 preferred if supported.

### Example: LoRA SFT with Hugging Face PEFT

```python
# pip install transformers peft datasets accelerate bitsandbytes trl

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

model_id = "meta-llama/Llama-3-8b-instruct"  # example
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# LoRA configuration
lora_cfg = LoraConfig(
    r=32,                         # rank
    lora_alpha=32,                # alpha ~ r
    lora_dropout=0.05,
    target_modules=["q_proj","k_proj","v_proj","o_proj", "gate_proj","up_proj","down_proj"], # + MLP
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()  # sanity check

# Enable gradient checkpointing to save memory
model.gradient_checkpointing_enable()

# Example training with TRL's SFTTrainer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

ds = load_dataset("json", data_files="train.jsonl")["train"]  # columns: instruction, input, output

def format_example(ex):
    prompt = f"Instruction: {ex['instruction']}\n{ex.get('input','')}\nAnswer:"
    return {"text": f"{prompt}\n{ex['output']}"}

train_ds = ds.map(format_example, remove_columns=ds.column_names)

training_args = SFTConfig(
    output_dir="./lora-out",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=16,    # increase effective batch
    learning_rate=2e-4,                # LoRA often tolerates higher LR
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=20,
    save_steps=500,
    bf16=True,
    gradient_checkpointing=True,
    max_seq_length=2048,
    dataset_text_field="text",
    packing=True,                      # pack multiple samples per sequence
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_ds,
    args=training_args,
)
trainer.train()
trainer.save_model("./lora-out")
```

### Serving LoRA adapters

- Option A (merge before serving): zero latency overhead, one model per adapter.
- Option B (keep adapters separate): minimal storage, fast adapter switching, small latency overhead.

Merge code:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
lora = PeftModel.from_pretrained(base, "./lora-out")
merged = lora.merge_and_unload()      # merges A,B into W
merged.save_pretrained("./merged-model")
```

Use adapter without merging (multi-LoRA):

```python
from peft import PeftModel
base = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")
model_taskA = PeftModel.from_pretrained(base, "./adapters/taskA")  # swap directory to switch tasks quickly
```

Storage math (example):
- Full matrix W: 4096×4096 (~16.8M params).
- LoRA r=8: A & B params ~4096×8×2 = 65,536.
- For 100 tenants: store 1×W + 100×adapters ≈ 16.8M + 6.6M params vs 100×16.8M if merged.

## QLoRA (Quantized LoRA) for 4-bit Finetuning

- What it is: Keep base weights in 4-bit (NF4/FP4) during training to fit larger models on single GPUs; dequantize to BF16/FP16 on the fly for compute.
- When to use: Limited VRAM, long sequences, 33B–70B models on 48–80 GB GPUs, or to reduce cloud cost.
- Trade-offs:
  - Pros: Huge memory savings (e.g., 65B on a single 48 GB GPU).
  - Cons: Extra quant/dequant overhead can slow training; careful config needed.

QLoRA setup (bitsandbytes int4):

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
import torch

bnb_cfg = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",       # nf4 or fp4
    bnb_4bit_use_double_quant=True,  # nested quantization
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_cfg,
    device_map="auto"
)

# Prepare model for k-bit training (important to set layer norms in fp32, etc.)
from peft import prepare_model_for_kbit_training
model = prepare_model_for_kbit_training(model)

lora_cfg = LoraConfig(r=16, lora_alpha=16, lora_dropout=0.05, target_modules=["q_proj","k_proj","v_proj","o_proj"], task_type="CAUSAL_LM")
model = get_peft_model(model, lora_cfg)

# Use an optimizer suitable for paged training (handled by HF Trainer with bitsandbytes Adam8bit)
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

args = TrainingArguments(
    output_dir="./qlora-out",
    learning_rate=2e-4,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=16,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    logging_steps=20,
    save_steps=500,
    bf16=True
)

# ...load and format dataset; then train using Trainer/SFTTrainer as above
```

Tips:
- Use paged optimizers and CPU offloading if VRAM is tight.
- Prefer BF16 compute dtype when available.
- Expect slower wall-clock vs 16-bit LoRA due to quant/dequant.

## Quantization Quick Guide

- Post-training quantization (PTQ):
  - Easiest path for inference: 8-bit or 4-bit (e.g., bitsandbytes, GGUF).
  - Quantize weights first; activation quantization is trickier and task-sensitive.
  - Mixed precision inference: keep critical ops in higher precision.

- Training-time:
  - QAT: simulates low precision during training to yield robust low-precision inference; doesn’t reduce training memory much.
  - Direct low-precision training (INT8/FP8/BF16 mixed): reduces training memory and can speed up; harder to stabilize (use AMP/AMPere/Blackwell features).

- Formats:
  - Inference: INT8/INT4 widely used; FP8/FP4 emerging with hardware support.
  - Training: BF16/FP16 mixed precision standard; keep layer norm/softmax in higher precision.

- Code: 8-bit or 4-bit loading for inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_cfg = BitsAndBytesConfig(load_in_8bit=True)  # or load_in_4bit=True with nf4/fp4 setup
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_cfg, device_map="auto")
```

## RAG vs Finetune: Decision Matrix

| Symptom | Likely cause | Recommended next step |
|---|---|---|
| Facts wrong, outdated, or missing | Knowledge gap | Add/upgrade RAG (BM25 → hybrid/embedding → graph), keep base model |
| Outputs correct but irrelevant or low-utility | Behavioral misalignment | Instruction SFT (LoRA) on curated data |
| Output format errors (JSON, SQL, DSL) | Syntax underexposure | Instruction SFT with schema+examples; consider constrained decoding |
| Hallucinations | Info + behavior | Start with RAG; finetune only after reliable retrieval |
| Limited context window | Architecture | Long-context finetune (positional embeddings), caution: regress on short seqs |

## Finetuning Workflow (Step-by-step)

1. Define metrics and evaluation pipeline early (automatic tests, human review rubric).
2. Exhaust prompt engineering (instructions, role, examples, self-checks).
3. Add basic retrieval (term-based). Measure improvement.
4. If facts still missing → improve RAG (hybrid search, chunking, reranking).
5. If behavior issues persist → collect instruction data (domain, style, schemas).
6. Start with LoRA:
   - Pick base model (best you can afford that meets constraints).
   - Choose target modules (attn + MLP), r=16–32, α=r, dropout 0.05.
   - Configure LR (1e-4–3e-4 for LoRA), epochs (2–5), grad accumulation.
   - Enable gradient checkpointing; pack sequences; BF16.
7. Evaluate; iterate on data quality before hyperparameters.
8. If multi-tenant: export adapters per tenant; implement multi-LoRA serving.
9. Optional: combine with RAG if knowledge gaps remain.
10. Monitor in prod: drift, regressions, safety; plan upgrade path (new base models).

## Data Guidance

- Instruction SFT:
  - Quality > quantity. 5k–50k well-curated examples can outperform larger noisy sets.
  - Include deliberate samples for target formats and edge cases.
  - Use model distillation to bootstrap (large model outputs → small model finetune).
  - Balance tasks to avoid overfitting to one; include negative/unsafe examples for safety alignment.

- Long-context finetune:
  - Requires position embedding changes (RoPE scaling etc.); specialist recipes; expect some short-context regression.

- Prompt loss weight:
  - Downweight prompt tokens (e.g., 0.1); upweight response tokens.

## Hyperparameters Cheat Sheet

- Optimizer: AdamW (β1=0.9, β2=0.95–0.999, weight_decay=0.01).
- Learning rate:
  - LoRA: 1e-4–3e-4 often works; reduce if unstable.
  - Full FT: start near pretraining LR × (0.1–1.0); often 1e-5–5e-5.
  - Use cosine or linear schedule; warmup 1–5% steps.
- Batch size:
  - Per device 1–8; use gradient_accumulation to reach effective 64–256 if possible.
  - Very small batch (<8) can be unstable; smooth with accumulation.
- Epochs:
  - 2–5 for 10k–50k examples; monitor val loss; early stop to prevent overfit.
- Sequence length:
  - Use max allowable (e.g., 2k–8k); pack short samples to improve throughput.
- Regularization:
  - LoRA dropout 0.0–0.1; weight decay 0–0.1 (careful with adapters).
- Precision:
  - Prefer BF16 where supported; mixed precision on by default.
- Memory savers:
  - gradient_checkpointing=True
  - use_8bit_adam or paged AdamW with bitsandbytes for QLoRA.

## Evaluation and Monitoring

- Before/after FT:
  - Task metrics: exact match, format validity (% valid JSON), BLEU/ROUGE for summarization, execution success for SQL/DSL.
  - Safety checks: refusal rates, toxic content, bias probes.
  - Generalization: measure change on non-target tasks (watch regressions).
- During training:
  - Loss curves: stable downward trend; spikes → reduce LR or increase batch/accumulation.
  - Overfitting: training loss down, val loss up → fewer epochs, more data, regularize.

## Common Pitfalls and Fixes

- Precision mismatch (BF16 vs FP16) degrades quality → load in intended dtype.
- Underestimating activation memory → enable gradient checkpointing; reduce max_seq_length; increase grad accumulation.
- Too-small data → noisy improvements → prioritize data quality curation; augment via distillation; synthetic + human vetting.
- Catastrophic forgetting (sequential finetune) → multi-task dataset, or merge adapters, or freeze more layers.
- LoRA rank too high → overfit/minimal gains; start with r=16–32.
- Noisy RAG hurts FT (baking wrong facts) → use clean curated instruction data; separate RAG for facts.
- Serving many merged models → use multi-adapter approach; avoid concatenation unless necessary.
- Licensing/legal: merging/finetuning may be restricted by base license; review.

## Model Merging (Advanced)

Use to combine capabilities across finetuned models, support multi-task, enable on-device deployment by unifying models.

Approaches:

1. Summing (linear combination / averaging)
   - Best when models share the same base and architecture.
   - Merge task vectors (delta = finetuned − base):
     - Simple average or weighted sum; or SLERP for smoother interpolation.
   - Prune redundant deltas before merging (TIES/DARE) to reduce interference.

2. Layer stacking (“frankenmerging”)
   - Stack layers from different models; often requires brief finetune after merge.
   - Useful for building MoE or upscaling depth (e.g., from 32 to 48 layers).

3. Concatenation
   - Concatenate parameters (e.g., LoRA adapters ranks add up); increases size; rarely worth it unless capacity constrained by rank.

Task vector merging (pseudo-code):

```python
# Merge two LoRA adapters trained on same base via weighted average
import safetensors.torch as st
import torch, glob, os

def load_adapter(path):
    return st.load_file(glob.glob(os.path.join(path, "*.safetensors"))[0])

A = load_adapter("./adapters/taskA")
B = load_adapter("./adapters/taskB")

wA, wB = 0.5, 0.5  # weights
merged = {}
for k in A.keys():
    if k in B:
        merged[k] = wA * A[k] + wB * B[k]
    else:
        merged[k] = A[k]  # or skip

st.save_file(merged, "./adapters/merged/adapter_model.safetensors", metadata={"format":"pt"})
```

Pruning redundant deltas (concept):
- Compute importance per parameter (e.g., absolute delta magnitude); keep top p% (e.g., 20%); zero the rest; then merge.
- Guards against task interference when merging >2 models.

Tools:
- mergekit (configurable merging: linear, SLERP, layerwise).
- safetensors for safe weight IO.

When to merge:
- Multi-task deployment on constrained devices.
- Federated learning aggregation (averaging client deltas).
- Combine complementary specializations.

## Serving Patterns

- Single finetuned model:
  - Merge adapters into base; quantize for inference; serve as single artifact.

- Multi-tenant (per-customer adapters):
  - Load base once; hot-swap LoRA adapters; pin popular adapters in memory.
  - Cache KV across repeats; cache prompts if supported.

- RAG + finetune:
  - Keep RAG retrieval layer independent; send retrieved context + instruction to finetuned model.
  - Monitor retrieval quality; avoid embedding drift.

## Security, Safety, and Bias

- Use curated finetune data to mitigate biases (e.g., balanced demographics).
- Include red-teaming prompts; align refusal behavior.
- Run safety classifiers in post-processing as belt-and-suspenders.

## Quick Reference Checklists

Before finetuning:
- [ ] Clear task definition, metrics, eval set.
- [ ] Exhaustive prompt experiments logged and versioned.
- [ ] Failure analysis: facts vs form.
- [ ] Decide base model (size, license, context window).
- [ ] Data collected/curated; schema/format examples included.

Training setup:
- [ ] Choose LoRA targets (attn + MLP), r=16–32, α=r, dropout=0.05.
- [ ] BF16 mixed precision; gradient checkpointing enabled.
- [ ] Effective batch ≥ 64 via accumulation.
- [ ] Learning rate 1e-4–3e-4 (LoRA), cosine schedule, warmup 3%.
- [ ] Prompt loss weight small (e.g., 0.1).
- [ ] Max seq length set; packing enabled.

During training:
- [ ] Monitor train/val loss; reduce LR if unstable.
- [ ] Save/validate every N steps; checkpoint to valid path.
- [ ] Early stop if overfitting.

After training:
- [ ] Evaluate on held-out + adversarial sets; format validity rate.
- [ ] Safety/bias checks; regression on general tasks.
- [ ] Decide merge adapters vs separate; quantize for inference.
- [ ] Rollout plan; canary traffic; monitoring and alerts.

Maintenance:
- [ ] Track base model upgrades; policy for switch-over.
- [ ] Continual data collection loop; label pipeline; re-train cadence.
- [ ] Versioning of models, adapters, prompts, RAG indices.

## Practical Patterns and Code Snippets

Constrained decoding for structured outputs:

```python
from transformers import TextStreamer

# E.g., restrict tokens to valid JSON via a regex or a JSON schema-guided decoder
# Libraries: Outlines, Guidance, jsonformer; or custom logit processors

from transformers import LogitsProcessor

class DisallowNewlines(LogitsProcessor):
    def __call__(self, input_ids, scores):
        scores[:, tokenizer.convert_tokens_to_ids("\n")] = -1e10
        return scores

outputs = model.generate(
    **tokenizer(prompt, return_tensors="pt").to(model.device),
    max_new_tokens=512,
    do_sample=False,
    logits_processor=[DisallowNewlines()],
)
```

Gradient accumulation and checkpointing:

```python
training_args = TrainingArguments(
  per_device_train_batch_size=1,
  gradient_accumulation_steps=64,   # effective batch size 64
  gradient_checkpointing=True,
  fp16=False, bf16=True
)
```

Activation checkpointing (manual enabling where needed):

```python
model.gradient_checkpointing_enable()
model.config.use_cache = False  # required when using gradient checkpointing
```

Packing short sequences for throughput:

```python
# TRL's SFTTrainer with packing=True automatically packs examples to fill max_seq_length
```

## Trade-off Tables

Finetuning vs RAG (expected gains and costs)

| Dimension | Prompt only | + RAG | + Finetune (LoRA) | RAG + Finetune |
|---|---|---|---|---|
| Facts | Low–Med | High | Low–Med | High |
| Form/Style | Med | Med | High | High |
| Cost to build | Low | Med | Med | High |
| Inference complexity | Low | High | Low | High |
| Maintenance | Low | Med–High (index) | Med (retrain) | High |

LoRA merge vs on-the-fly adapters

| Approach | Latency | Storage | Best when |
|---|---|---|
| Merge adapters into base | Lowest | High (one copy per finetune) | Single model deployment |
| Keep adapters separate | Slightly higher | Low (one base + many small adapters) | Multi-tenant or frequent switching |

## Recommended Defaults (If You Need to Decide Now)

- Base model: strongest allowed by license that fits infra; prefer models with BF16 weights; sufficient context length.
- Finetune method: LoRA with attention+MLP targets; r=32; α=32; dropout=0.05; BF16; gradient checkpointing; packing.
- Optimization: AdamW, lr=2e-4, cosine schedule, warmup 3%, effective batch ~128 via accumulation; epochs 3.
- Data: 10k–50k high-quality instructions; include schemas/examples; downweight prompt tokens (0.1).
- Serving: merge for single model; adapters for multi-tenant; quantize to 8-bit or 4-bit as needed.
- Combine with RAG if knowledge gaps remain.

## Notes on Long-Context Finetuning

- Requires positional embedding changes (e.g., RoPE scaling/NTK-aware scaling); specialized recipes per model family.
- Risks regression on short contexts; verify across lengths.
- Consider using an already long-context base if available.

## Licensing and Compliance

- Check base model license for finetuning/merging/serving terms.
- Customer-specific adapters may mitigate sharing constraints.
- Track dataset provenance; ensure rights for training data.

---

This reference prioritizes decision-making, setup, and execution for finetuning under practical constraints. Use the defaults to get started fast; iterate on data and evaluation for the biggest gains.