## Foundation Models: Actionable Reference (Chapter 2)

Use this guide to select models, plan compute, curate data, post-train for alignment, and control sampling/outputs. Dense, pragmatic, and production-focused.

---

## Quick Decision Guides

- Choose a model
  - Need non-English? Prioritize models trained for that language; avoid translate→English→back unless you can tolerate info loss and token bloat.
  - Need domain accuracy (biomed, law, CAD, factory)? Prefer domain models or finetune with curated domain data.
  - Need long context? Consider transformer with optimized KV-cache or SSM/hybrid variants; validate performance, not just max length claims.
  - Need cheap/fast inference? Prefer smaller dense models or MoE with low active params; use aggressive decoding constraints.

- Plan compute
  - Track 3 numbers: parameters (capacity), training tokens (how much it learned), FLOPs (training cost).
  - Use compute-optimal rule: training_tokens ≈ 20 × parameters (for dense models, human-generated data).
  - Model memory for inference ≈ parameters × bytes_per_param + KV cache; deploy with quantization.

- Post-train
  - SFT to make models conversational/Task-following.
  - Preference finetune (DPO or RLHF) to align outputs with your policies.
  - If RL is too heavy: use a reward/verifier model for “best-of-N” selection.

- Sampling
  - Default decoding: temperature 0.2–0.7, top_p 0.9–0.95, max_tokens cap, stop sequences.
  - Use test-time compute for harder tasks: sample multiple outputs; select with average logprob, a verifier, or majority vote.

- Structured outputs
  - Stack: Prompting → Post-processing → Constrained sampling → Finetuning.
  - JSON mode helps, but still validate/truncate-safe; use grammar-constrained decoding for strict formats.

- Reliability
  - Inconsistency: fix temperature/top_p/seed, cache responses, use memory/RAG.
  - Hallucination: retrieval, concise answers, verifiers/reward shaping, don’t over-trust SFT/RL to fully eliminate.

---

## Training Data Strategy

### Language Coverage

- When to create a language-focused model
  - Your target language is underrepresented on the web (low-resource).
  - Tokenization is inefficient (e.g., Burmese, Hindi) causing high latency/cost.
  - Alignment/evaluation in target language differs from English (e.g., misinformation policies vary by language).

- Practical steps
  - Quantify tokenization cost: benchmark tokens per sentence across your language set.
  - Build/augment training corpora:
    - High-quality native content (news, gov docs, education, code, manuals).
    - Curated parallel corpora for translation tasks.
    - Avoid over-reliance on auto-translated data for core language proficiency.
  - Alignment/eval in-language:
    - Labelers fluent in target language and culture.
    - Build safety/quality rubrics per language.

- Pitfalls
  - Translate-then-answer:
    - Requires good translation in both directions.
    - Loses cultural/relational nuances (e.g., pronouns in Vietnamese).
    - Increases tokens → higher cost/latency.

### Domain-Specific Models

- When to go domain-specific
  - Data is private, structured, or rare (biomed, materials, law, finance, manufacturing).
  - Safety/compliance demands precise control.
  - General models fail on tasks not present in web data.

- Data curation checklist
  - Collect proprietary corpora (EHR, contracts, lab notes, CAD/BOM, factory logs).
  - Ensure formats coverage (e.g., PDB for proteins, DICOM for imaging).
  - Label tasks: Q&A, extraction, classification, semantic parsing.
  - Protect privacy (de-identification, access controls).

- Build options
  - Finetune on general model with domain corpora.
  - Train domain encoders (e.g., biomed encoders for retrieval).
  - Build validators/reward models for domain constraints.

---

## Modeling Choices

### Architecture Trade-offs

| Architecture | Strengths | Limitations | Use When |
|---|---|---|---|
| Transformer (decoder-only) | Mature ecosystem, strong general performance, scalable prefill, tooling | Quadratic attention cost, KV-cache memory, long-context inefficiency | Default for text; most tooling/support |
| RWKV (RNN-like) | Theoretically long context, streaming | Long-context quality varies in practice | Streaming/low-latency prototypes |
| SSMs (e.g., Mamba) | Linear-time sequence modeling; promising long-range | Tooling less mature; limited public checkpoints | Long-context workloads; research/prototyping |
| Hybrid (e.g., Jamba: Transformer + Mamba/MoE) | Memory efficiency, long context, performance | Complexity, niche configs | Fit model in constrained GPU while keeping long context |

- Guidance
  - If you need predictable performance and tooling: choose Transformer.
  - If long context is a must: validate hybrids/SSM on your data; benchmark end-to-end tasks.
  - Optimize for inference latency differently for Transformer (KV cache, speculative decoding) vs others.

### Context Length Considerations

- Longer context increases:
  - KV cache memory ∝ layers × heads × sequence length × head_dim.
  - Latency in decode (sequential).
- Techniques
  - Use retrieval to avoid stuffing long context.
  - Sliding windows, chunking, compression (summary, embeddings).
  - Long-context finetuning and RoPE scaling (if supported), but validate factual recall.

---

## Model Size and Compute Planning

### The Three Numbers

- Parameters (capacity): e.g., 7B, 13B, 70B, 405B.
- Training tokens: proxy for “how much it learned”.
- FLOPs: training compute cost.

### Quick Calcs

- Inference memory (dense, fp16) ≈ params × 2 bytes
  - 7B → ~14 GB just for weights; add KV cache and overhead.
- KV cache growth ≈ sequence_len × layers × 2 (K,V) × hidden per head × heads × bytes.
- FLOP/s-day conversion: 1 FLOP/s-day = 86,400 FLOPs (useful for budget back-of-envelope).
- Training time ≈ total_FLOPs / (num_accelerators × accel_FLOP/s × utilization).

### Sparse/MoE Models

- Total params large; active params small
  - Example: 46.7B total, 12.9B active → inference cost ~12.9B model.
- Benefits: higher capacity at similar inference cost.
- Watch: routing quality, load balance, memory fragmentation.

### Data Scale Notes

- Training tokens = dataset_tokens × epochs.
- Dense models: compute-optimal rule (Chinchilla):
  - training_tokens ≈ 20 × parameters.
  - Scale parameters and tokens together (double size → double tokens).
- Dataset quality matters more than sheer volume; curate high-quality subsets for code/math/domain data.

### Budgeting Procedure

1. Define target quality (benchmarks or task metrics).
2. Choose family/size candidates (e.g., 7B, 13B, 70B).
3. Estimate inference cost/latency constraints.
4. If pretraining/continued-pretraining:
   - Compute FLOPs with target tokens (≈20×params).
   - Choose accelerator count, utilization goal (≥50%).
   - Estimate cost: accelerators × $/hr × hours / utilization.
5. Else finetune baseline model with high-quality domain/task data; measure lift vs cost.

---

## Post-Training Pipeline

### Supervised Finetuning (SFT)

- Purpose: convert completion-style pretrain to instruction-following; teach task formats.
- Data format: (prompt, response) demonstrations covering target tasks (QA, summarize, classify, extract, translate).
- Quality bar: skilled labelers; per-sample effort can be minutes.
- Cost controls:
  - Seed with curated public Q/A, StackExchange-like, docstrings (with filters).
  - Synthetic generation with a stronger model + human spot-check.
  - Heuristics to extract dialogues from web text (format patterns).

- Best practices
  - Mix tasks proportional to expected production distribution.
  - Include long-context samples if you need long-context performance.
  - Enforce style/formatting examples (JSON, YAML, SQL).
  - Devise eval sets per task; measure before/after SFT.

### Preference Finetuning

- Goal: align outputs with human preference/safety.
- Options
  - DPO (Direct Preference Optimization): simpler, avoids RL loop, strong baseline.
  - RLHF (PPO): more complex, more knobs; can shape style/safety/format quality; supports reward-model-based objectives.
  - RLAIF: use AI judges to scale labels; guard for bias.

- Reward Model (RM) data
  - Pairwise comparisons: (prompt, preferred_response, rejected_response).
  - Labeling UI supports ranking multiple outputs → more pairs.
  - Train RM via pairwise loss maximizing score(preferred) − score(rejected).

- Finetuning with RM
  - RL (PPO): sample responses, score via RM, optimize policy to increase RM score.
  - Or skip RL: use RM at inference to select best-of-N.

- When to skip RL
  - Budget/time constraints.
  - Outputs can be re-ranked by a verifier with sufficient lift.

- Pitfalls
  - Overfitting to labeler bias; ensure diverse annotators.
  - Mismatch between model knowledge and annotator assumptions can induce hallucinations.
  - RL can degrade factuality; monitor and include factuality in reward or constraints.

---

## Sampling and Decoding

### Knobs and Effects

| Control | What it does | Use When | Risks |
|---|---|---|---|
| temperature | Flattens/sharpens distribution | Creativity: 0.7; Deterministic: 0–0.2 | High temp → incoherence; zero temp → repetitive |
| top_p (nucleus) | Sample from smallest prefix > p | General default: 0.9–0.95 | Too low → dull; too high → rambling |
| top_k | Limit to k most likely tokens | Latency/cost optimization, more predictability | Too small → degenerate loops |
| stop sequences | Early stop at tokens/strings | Control format, latency | Truncation → malformed outputs |
| max_tokens | Hard cap on length | Bound cost/latency | Cut mid-sequence if too short |
| seed | Fix sampling randomness | Reproducibility for tests | Vendor support varies |

- Defaults
  - General: temperature 0.3–0.7, top_p 0.9, stop as needed, max_tokens appropriate.
  - Deterministic eval: temperature 0, top_p 1.0, fixed seed.

### Example: Hugging Face Transformers Generation

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map="auto"
)

prompt = "Write a concise summary of the benefits of MoE models."
inputs = tok(prompt, return_tensors="pt").to(model.device)

gen = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.5,
    top_p=0.95,
    top_k=50,
    max_new_tokens=200,
    eos_token_id=tok.eos_token_id,
    pad_token_id=tok.eos_token_id,
)
print(tok.decode(gen[0], skip_special_tokens=True))
```

### Selecting the Best Output (Average Logprob)

```python
outputs = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    num_return_sequences=8,
    output_scores=True,
    return_dict_in_generate=True,
    max_new_tokens=200,
)

sequences = outputs.sequences
scores = outputs.scores  # list of logits per step

# Compute average logprob per sequence:
import torch
seq_logprobs = []
for i in range(sequences.shape[0]):  # N sequences
    # Use model's built-in sequence_scores if available
    if hasattr(outputs, "sequences_scores") and outputs.sequences_scores is not None:
        seq_logprobs.append(outputs.sequences_scores[i].item())
    else:
        # Fallback: approximate from token logprobs (omitted for brevity)
        pass

best_idx = int(torch.tensor(seq_logprobs).argmax())
best_text = tok.decode(sequences[best_idx], skip_special_tokens=True)
```

### Test-Time Compute Patterns

- Best-of-N
  - Generate N samples with varied seeds or sampling params.
  - Pick:
    - Highest average logprob (length-normalized).
    - Highest reward/verifier score.
    - Majority vote for exact-answer tasks.
  - Cost ≈ N×; reduce by sharing prefill and parallelizing.

- Beam search
  - Keep k highest-probability partial sequences at each step.
  - Better for structured/low-entropy outputs (e.g., code, SQL).
  - Risk: reduced diversity.

- Majority vote / self-consistency
  - For math/MCQ: sample K chains/answers → vote → pick most frequent.
  - Strong gains without model scale-up.

- Latency optimization
  - Run multiple generations in parallel; accept the first valid one.
  - Validate with format checker/verifier.

---

## Structured Outputs

### Strategy Ladder

1. Prompting
   - Explicit format instructions; few-shot with valid schemas.
   - Add “only return JSON; no prose” and show minimal examples.

2. Post-processing
   - Repair common errors (missing commas/brackets).
   - Defensive parsers (e.g., tolerant YAML parsers).
   - Add truncation guards (e.g., ensure closing braces).

3. Constrained sampling (grammar)
   - Restrict token choices to follow a grammar (JSON, CSV, regex).
   - Use libraries to enforce constraints at decode time.

4. Finetuning
   - Train on target formats heavily; optionally add classifier/decoder heads.

### Prompting Example (JSON)

```text
System: You are a function caller. Return ONLY valid minified JSON.
User: Extract company, role, and start_year from: "I joined Acme as a data engineer in 2019."

Return schema:
{"company": string, "role": string, "start_year": integer}
```

### Post-Processing Example (Python)

```python
import json

def safe_parse_json(s: str):
    # Common fixes
    s = s.strip()
    # Remove leading/trailing code fences
    if s.startswith("```"):
        s = s.strip("`").strip()
        if s.startswith("json"):
            s = s[4:].strip()
    # Try parse, else minor repairs
    try:
        return json.loads(s), None
    except Exception as e:
        # Add missing closing brace if starts with '{'
        if s.count("{") > s.count("}"):
            try: return json.loads(s + "}")
            except: pass
        return None, e
```

### Constrained Sampling (Outlines)

```python
# pip install outlines
from outlines import models, generate
import outlines

model = models.transformers("meta-llama/Meta-Llama-3-8B-Instruct")

schema = {
  "type": "object",
  "properties": {
    "company": {"type": "string"},
    "role": {"type": "string"},
    "start_year": {"type": "integer"}
  },
  "required": ["company", "role", "start_year"]
}

gen = generate.json(model, schema)
result = gen("Extract fields from: I joined Acme as a data engineer in 2019.")
# Returns a Python dict guaranteed to match schema
```

### JSON Mode Caveats (API Providers)

- Valid JSON ≠ correct content: still validate semantics.
- Truncation risk: set max_tokens high enough; add stop at closing brace.
- Still implement robust parsing and retry/repair logic.

### Finetuning for Format Adherence

- Heavily sample tasks producing the exact format.
- For classification, add a classifier head to restrict outputs to class logits.
- Evaluate strict validity: % valid parses, % semantically correct.

---

## Managing Probabilistic Behavior

### Inconsistency

- Same prompt, different outputs
  - Fix temperature/top_p.
  - Set seed (if provider supports).
  - Cache responses; embed and deduplicate similar prompts.
- Slight input changes, large output shifts
  - Use memory/context to anchor style/facts.
  - Add robust system prompts with constraints.
  - Retrieval augmentation to ground on sources.

- Infra-induced variance
  - Different hardware kernels/dtypes can change outputs at low levels.
  - For CI: pin framework versions, dtypes, seeds; use deterministic kernels where possible.

### Hallucination

- Techniques
  - RAG: retrieve authoritative documents; cite sources; require grounded answers.
  - Conciseness: fewer tokens reduce drift; ask for short, direct answers.
  - Verifiers: train discriminators to detect unsupported claims; reject or ask for sources.
  - Reward shaping: penalize unsupported content if doing RL.
  - Policies: instruct to say “I don’t know” when uncertain; enforce via RM/verifier.

- Detection (operational)
  - Confidence proxies: average logprob, entropy, self-consistency across samples.
  - Source-attribution: require extraction of supporting spans; reject if missing.
  - Human-in-the-loop for high-risk tasks.

- Pitfalls
  - RLHF/DPO can improve helpfulness while harming factuality if reward ignores truth.
  - Safety behavior varies across languages; test in-language.

---

## Practical Checklists

### Language/Domain Data Curation

- [ ] Measure tokenization efficiency; estimate token cost per query.
- [ ] Collect native-language corpora; prefer curated sources.
- [ ] Build in-language eval sets and safety rubrics.
- [ ] Domain: collect proprietary/task-specific data; ensure privacy controls.
- [ ] Balance quantity, quality, diversity; prune low-quality segments.
- [ ] Document licenses and ToS compliance.

### Compute and Model Selection

- [ ] Define success metrics and latency/cost constraints.
- [ ] Select candidate sizes; benchmark few-shot and with RAG.
- [ ] Compute-optimal planning if pretraining: tokens ≈ 20×params.
- [ ] Estimate FLOPs, time, cost with utilization assumptions.
- [ ] Decide on dense vs MoE; plan memory and routing monitoring.

### Post-Training

- [ ] SFT dataset: representative tasks; high-quality demonstrations.
- [ ] Build eval suites per task and per language.
- [ ] Preference finetune: choose DPO or RLHF; design reward signal.
- [ ] Safety tests: jailbreaks, content policy, misinformation in all languages.
- [ ] Monitor regressions: factuality, format adherence.

### Decoding and Test-Time Compute

- [ ] Set defaults: temperature/top_p/top_k/stop/max_tokens.
- [ ] Add retries with varied seeds for hard prompts.
- [ ] Implement best-of-N with average logprob or verifier.
- [ ] Majority vote for exact-answer tasks; cap N to budget.
- [ ] Parallelize sampling; early accept first valid.

### Structured Output

- [ ] Prompt with explicit schema; include minimal examples.
- [ ] JSON/YAML mode if available; include stop at final brace.
- [ ] Post-process common mistakes; fall back to repair/retry.
- [ ] Constrained decoding for strict formats; grammar libraries.
- [ ] Finetune to increase adherence; measure % valid parses.

---

## Comparison Tables

### SFT vs DPO vs RLHF

| Aspect | SFT | DPO | RLHF (PPO) |
|---|---|---|---|
| Goal | Teach formats & tasks | Align to preferences (pairwise) | Align via RM optimizing responses |
| Data | (prompt, response) | (prompt, preferred, rejected) | (prompt, preferred, rejected) + RM |
| Complexity | Low | Medium | High |
| Control | Limited | Medium | High (style/safety shaping) |
| Typical Use | Baseline instruction-following | First-line alignment | Advanced alignment; complex trade-offs |
| Risks | Mimics bias/errors | Overfit to pairwise biases | Factuality regressions; instability |

### Structured Output Methods

| Method | Enforcement | Cost | Notes |
|---|---|---|---|
| Prompt only | Weak | Low | Good baseline; validate outputs |
| Post-process | Medium (common fixes) | Low | Handles predictable errors |
| Constrained sampling | Strong | Medium | Requires grammar/tooling; latency overhead |
| Finetune | Medium–High | Medium–High | Most general; combine with others |

### Sampling Knobs Defaults

| Scenario | temperature | top_p | top_k | Strategy |
|---|---|---|---|---|
| Creative writing | 0.7 | 0.95 | 50–100 | Few-shot style guides |
| Factual QA | 0–0.3 | 0.9 | 40–80 | Retrieval + verifiers |
| Code/SQL | 0.1–0.3 | 0.9 | 20–60 | Beam search, grammar constraints |
| Eval/Tests | 0 | 1.0 | None | Fixed seed; determinism |

---

## Code Patterns

### Multi-Sample Best-of-N With Verifier

```python
def generate_candidates(model, tok, prompt, n=8, **decode):
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    outs = model.generate(
        **inputs,
        do_sample=True,
        num_return_sequences=n,
        output_scores=True,
        return_dict_in_generate=True,
        **decode
    )
    texts = [tok.decode(s, skip_special_tokens=True) for s in outs.sequences]
    return texts, outs

def score_with_verifier(verifier_model, verifier_tok, prompt, text):
    inp = verifier_tok(f"Prompt: {prompt}\nResponse: {text}\nScore:", return_tensors="pt").to(verifier_model.device)
    score = verifier_model(**inp).logits.squeeze().item()  # model-dependent
    return score

texts, outs = generate_candidates(model, tok, prompt, n=6, temperature=0.5, top_p=0.9, max_new_tokens=256)
scored = [(t, score_with_verifier(v_model, v_tok, prompt, t)) for t in texts]
best = max(scored, key=lambda x: x[1])[0]
```

### Grammar-Constrained Decoding (Regex example with Outlines)

```python
from outlines import models, generate, regex

model = models.transformers("Qwen/Qwen2.5-7B-Instruct")
email = regex(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}")

gen = generate.regex(model, email)
res = gen("Extract the email address from: 'Contact me at dev_rel@example.org.'")
```

### Pairwise Reward Model Loss (PyTorch)

```python
# Inputs: encodings of (x, y_w), (x, y_l), and RM model
import torch
import torch.nn as nn

sigmoid = nn.Sigmoid()

def pairwise_loss(rm, x, yw, yl):
    sw = rm.score(x, yw)  # scalar per sample
    sl = rm.score(x, yl)
    # Maximize log(sigmoid(sw - sl))  => minimize negative
    loss = -torch.log(sigmoid(sw - sl)).mean()
    return loss
```

---

## Formulas & Quick References

- Softmax: p_i = exp(x_i) / sum_j exp(x_j)
- Temperature: apply softmax(x_i / T)
- Sequence logprob: sum(logprob(tokens)); length-normalize by average
- Compute-optimal (dense): training_tokens ≈ 20 × parameters
- Inference memory (weights): params × bytes_per_param (plus KV cache)
- FLOP/s-day: 1 FLOP/s-day = 86,400 FLOPs (unit normalization)

---

## Common Pitfalls and Remedies

- Training on “everything” leads to high cost and uneven quality
  - Remedy: prune aggressively; prioritize high-quality subsets; domain boost.
- Assuming JSON mode guarantees correctness
  - Remedy: validate schema, lengths, values; repair/retry; constrained decoding for strictness.
- Over-reliance on English evals
  - Remedy: build in-language datasets; include safety tests per language.
- Scaling test-time compute without selection robustness
  - Remedy: use strong verifiers; cap N; detect adversarial samples.
- RL alignment without factuality term
  - Remedy: incorporate factuality in reward; verify post-RL regression.

---

## When to Use Which Technique

- Need better adherence to task instructions and formats → do SFT with format-heavy data; add constrained decoding if strict formats required.
- Need outputs that reflect organizational policy/safety trade-offs → use DPO first; escalate to RLHF if you need richer control.
- Need improved accuracy without retraining → use test-time compute (best-of-N); add verifiers; leverage RAG.
- Need cost/latency control → reduce max_tokens; use top_k; quantize; cache prefill; consider smaller or MoE models.
- Need non-English robustness → collect in-language SFT and preference data; evaluate tokenization overhead; avoid blind translation loops.

---

This reference is designed to be used at build time: pick the relevant section, copy code patterns, apply checklists, and make explicit trade-offs using the tables and defaults provided.