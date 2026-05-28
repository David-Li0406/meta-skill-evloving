# AI Engineering Reference — Chapter 1: Building AI Applications with Foundation Models

Use this as a quick, actionable guide to decide, design, evaluate, and ship AI products built on foundation models.

## Quick Definitions (only what you need)

- Token: unit of model input/output (≈ 0.75 words in GPT-4). Vocabulary size is fixed by the model.
- Autoregressive LM (default): predicts next token using previous tokens; used for generation.
- Masked LM: predicts masked tokens using both sides of context; used for understanding/classification.
- Foundation model: general-purpose (often multimodal) model pre-trained via self-supervision and optionally post-trained for instruction following.
- Multimodal: text + other modalities (images, audio, video, code, etc.).
- Parameters: model weights. More params ≈ higher capacity (but requires more data/compute).
- Self-supervision: learn from raw sequences by predicting parts of them (no manual labels required).
- Model adaptation: change behavior using:
  - Prompting (no weight changes)
  - Retrieval-augmented generation (RAG) (no weight changes)
  - Finetuning/post-training (updates weights)
  - Training from scratch (pre-training)

---

## Decision Frameworks

### 1) Should we build this AI application?

- Risk/priority tiers:
  - Tier 1 (existential): competitors can obsolete you if you don’t adopt AI (document processing, content gen, knowledge work at scale) → Act now; build core in-house.
  - Tier 2 (opportunity): profits/productivity gains (sales, support, ops) → Pilot with buy options; build where differentiated.
  - Tier 3 (exploration): unclear fit but strategic learning → Controlled R&D; timebox experiments and learning goals.

- Buy vs Build:
  - Buy if: generic capability, low differentiation, strict timelines, existing tools meet thresholds (quality/latency/cost/compliance).
  - Build if: core to product value, unique data/IP, compliance constraints, need deep customization, long-term cost control.

- Deployment strategy:
  - Start internal-facing (lower risk) → graduate to external-facing as quality stabilizes.
  - Prefer close-ended tasks initially (classification/extraction) → expand to open-ended once evaluation harness is strong.

### 2) Role of AI and Human

- AI criticality:
  - Critical: app fails without AI (e.g., Face ID) → high reliability bar, strong guardrails.
  - Complementary: app works without AI (e.g., Smart Compose) → faster iteration allowed.

- Reactive vs proactive:
  - Reactive (on-demand) → emphasize latency (TTFT/TPOT), predictable UX.
  - Proactive (opportunistic) → precompute; set higher quality bar to avoid annoyance.

- Dynamic vs static:
  - Dynamic (per-user adaptation, memory/personalization) → data privacy, continual learning infra.
  - Static (shared model) → versioned rollouts tied to app releases.

- Human-in-the-loop (Crawl–Walk–Run):
  - Crawl: AI suggestions only, human mandatory.
  - Walk: AI handles limited scope; humans escalate/approve.
  - Run: full automation on vetted segments; human audit and exception handling.

### 3) Technique Selection: Prompt vs RAG vs Finetune vs Train

| Technique | Best for | Pros | Cons | Data needed | Latency | Cost | Typical use |
|---|---|---|---|---|---|---|---|
| Prompting | Format/style tweaks; lightweight tasks | Fast to iterate; zero infra changes | Ceiling on quality; brittle to phrasing | 0–few examples | Low | Low | Drafting, classification, small tools |
| RAG | Up-to-date facts; long docs; compliance | Grounded answers; avoids retraining | Needs retrieval infra; chunking/tuning | Document corpus; metadata | Medium | Medium | Q&A, policy search, “talk to your docs” |
| Finetune | Task specialization; tone/style lock-in | Quality, latency, cost benefits; robustness | Needs data + training pipeline; risk of overfitting | 1k–100k+ labeled pairs (task-dependent) | Low–Med | Lower per call | Vertical assistants, consistent generation |
| Train (from scratch) | New modalities; proprietary arch | Full control/IP | Massive cost/complexity | Billions tokens | N/A | Highest | Few orgs; research labs |

Guidance:
- Start with Prompt → add RAG for grounding → Finetune to lock performance → Avoid training from scratch unless strategically necessary.

---

## Planning and Milestones

### Define Success (set hard gates)

- Business metrics:
  - Automation rate: % tasks handled end-to-end by AI
  - Time saved: throughput increase or response time reduction
  - Cost per task: total inference + supervision costs
  - User satisfaction: CSAT/NPS/deflection quality (for support)

- Quality metrics:
  - Task-specific: accuracy/F1/extraction exact match; rubric-based scoring for open-ended outputs
  - Hallucination rate; policy compliance; toxicity/PII leakage

- Latency metrics:
  - TTFT (time to first token), TPOT (time per output token), Total latency
  - Set budgets per surface (chat vs batch vs proactive)

- Cost metrics:
  - $/1k tokens (input/output), $/request, GPU hours (self-hosted)

- Readiness gates (example for support bot):
  - Gate 1: 95% correct on intent classification
  - Gate 2: 90% correct on “simple” intents; <1% policy violations
  - Gate 3: 80% deflection on “simple” with CSAT ≥ baseline; PII leakage 0

### Milestone Phases

1. Feasibility (1–2 weeks)
   - Baseline with prompting; quick offline eval; estimate ROI.
2. Prototype (2–6 weeks)
   - Add RAG; build eval harness; small pilot users; define guardrails.
3. Beta (4–12 weeks)
   - Finetune if needed; scale retrieval; instrument telemetry; A/B test.
4. GA
   - SLOs (quality/latency/cost); monitoring, rollback; versioning.

Caution: The “last mile” from ~80% to >95% often takes longer than the first 80%. Plan buffer.

---

## Evaluation Essentials

Evaluation is continuous: model selection → prompt/RAG tuning → finetune → production monitoring.

### What to Measure

- Offline:
  - Golden set: curated inputs with gold labels, edge cases, adversarial probes.
  - Rubrics for open-ended (LLM-as-judge or human rubric scoring).
  - Component evals: retrieval hit rate, chunk relevance, grounding score.

- Online:
  - User acceptance/edits, CSAT, deflection, escalation rate.
  - Safety: PII/toxicity/unsafe tool use.
  - Performance: TTFT, throughput, token utilization.

### Dataset Creation (open-ended tasks)

- Include:
  - High/low complexity cases
  - Ambiguous prompts
  - Policy-sensitive scenarios
  - Long-context samples
  - Non-English / domain-specific jargon
- Labeling:
  - Use rubric scoring (e.g., 1–5) with criteria (correctness, completeness, style, safety).
  - Inter-annotator agreement; spot audits.

### Evaluation Harness (minimal)

```python
# python - evaluation harness skeleton
import time, json
from statistics import mean
from openai import OpenAI

client = OpenAI()

def ttft_streaming(prompt, model="gpt-4o-mini"):
    t0 = time.time()
    stream = client.chat.completions.create(
        model=model,
        stream=True,
        messages=[{"role":"user","content":prompt}]
    )
    first, total_tokens = None, 0
    for chunk in stream:
        if first is None:
            first = time.time()
        delta = chunk.choices[0].delta.content or ""
        total_tokens += len(delta.split())
    return (first - t0) * 1000, (time.time() - first) * 1000, total_tokens

def batch_eval(samples):
    results = []
    for s in samples:
        ttf, rest, toks = ttft_streaming(s["input"])
        results.append({"id": s["id"], "ttft_ms": ttf, "gen_ms": rest, "out_tokens": toks})
    return {
        "ttft_ms_avg": mean(r["ttft_ms"] for r in results),
        "gen_ms_avg": mean(r["gen_ms"] for r in results),
        "samples": results,
    }

if __name__ == "__main__":
    with open("eval_samples.json") as f:
        samples = json.load(f)
    print(json.dumps(batch_eval(samples), indent=2))
```

LLM-as-judge example:

```python
JUDGE_PROMPT = """You are a strict evaluator.
Given:
- Task: {task}
- Input: {input}
- Model output: {output}
- Reference: {reference}

Score 1-5 for: correctness, completeness, style, safety.
Return JSON: {"correctness": int, "completeness": int, "style": int, "safety": int, "feedback": "..."}"""

def llm_judge(client, item):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": JUDGE_PROMPT.format(**item)}]
    )
    return json.loads(resp.choices[0].message.content)
```

Best practices:
- Keep prompts and datasets versioned (semantic versioning).
- Re-run full evals on every change (model/prompt/retrieval/finetune).
- Compare with paired statistical tests when possible.

---

## Architecture and Stack

### Three Layers

1) Application development
- Responsibilities: prompts, context construction (RAG), tool use/agents, evaluation, UX.
- Interfaces: chat/voice, browser extension, IDE plugin, app embeds.
- Feedback: inline thumbs, rationales, edit distance, freeform comments.

2) Model development
- Responsibilities: finetuning/post-training, dataset engineering, inference optimization.
- Tools: PyTorch/Transformers, LoRA/QLoRA, distillation, serving frameworks.

3) Infrastructure
- Responsibilities: model serving (scale/batching/streaming), vector stores, data lakes, monitoring (quality/safety/cost/latency), governance.
- Patterns: multi-provider abstraction; canary rollouts; feature flags for model/prompt.

---

## RAG Quickstart

When to use:
- Domain knowledge not in model weights, long documents, fast updates, compliance/grounding needs.

Core steps:
1. Chunking: split docs (200–800 tokens) with overlap; structure-aware (headings/sections).
2. Embedding: choose embedding model; normalize vectors.
3. Index: vector DB with metadata filters; add BM25 hybrid for recall.
4. Retrieval: top-k + rerank (cross-encoder) for precision.
5. Prompt: cite sources; encourage abstention.

Minimal code:

```python
# python - minimal RAG pipeline
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss, numpy as np

embed = SentenceTransformer("all-MiniLM-L6-v2")
rerank = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

docs = [...]  # [{"id":..., "text":..., "meta": {...}}]
embs = embed.encode([d["text"] for d in docs], normalize_embeddings=True)
index = faiss.IndexFlatIP(embs.shape[1]); index.add(np.array(embs))

def retrieve(query, k=20, top=5):
    qv = embed.encode([query], normalize_embeddings=True)
    D,I = index.search(qv, k)
    cands = [(docs[i], float(D[0][j])) for j,i in enumerate(I[0])]
    # rerank
    pairs = [(query, d["text"]) for d,_ in cands]
    scores = rerank.predict(pairs)
    reranked = sorted(zip(cands, scores), key=lambda x: x[1], reverse=True)[:top]
    return [d for (d,_),_ in reranked]

PROMPT = """Answer using only the provided context. If missing, say 'I don't know.'
Question: {q}
Context:
{ctx}
Cite sources as [S:id].
"""

def build_context(docs):
    return "\n\n".join([f"[S:{d['id']}] {d['text']}" for d in docs])

# Call your chat model with PROMPT.format(q=..., ctx=build_context(...))
```

Tuning tips:
- Measure: retrieval precision@k, coverage of answers, groundedness score.
- Add metadata filters (date, product, customer).
- Use rewriters (query expansion) for recall, rerankers for precision.
- Prevent leakage: strip PII; document-level access control.

---

## Finetuning Basics

When to finetune:
- Need consistent style/voice, task-specific formats, or lower latency/cost at scale.
- Prompting/RAG plateaued below target performance.

Data:
- 1k–5k high-quality pairs can move the needle; 20k–100k+ for robust behavior.
- Use instruction-output pairs; include negative examples and policy boundaries.

Process:
- Start with parameter-efficient tuning (LoRA/QLoRA).
- Validate on held-out set; early stop to avoid overfitting.
- Evaluate robustness (paraphrases, adversarial, OOD).

Output control:
- Add structured output training (JSON schemas).
- Teach abstention (“I don’t know” with criteria).

---

## Inference Optimization Cheat Sheet

Latency metrics:
- TTFT: dominated by queueing, provider, first token generation.
- TPOT: dominated by decoding throughput; proportional to output length.

Techniques and trade-offs:

| Technique | Gains | Trade-offs | Notes |
|---|---|---|---|
| Quantization (INT8/4) | Lower memory, faster | Quality drop (small); limited HW support | Use AWQ/GPTQ/LLM.int8 variants |
| Speculative decoding | TTFT/TPOT faster | Two models; complexity | Small draft model proposes; large accepts |
| KV cache + prompt caching | Faster subsequent turns | Memory overhead | Reuse attention states; cache static system prompts |
| Batching | Throughput | Tail latency ↑ | Dynamic batching windows; careful SLOs |
| Distillation | Model smaller/faster | Training data + infra | Teacher→student; maintain quality |
| Parallelism (tensor/pipeline) | Fit/scale large models | Engineering complexity | Useful for self-hosting large models |

Measure with streaming and log token counts. Sample code above.

---

## Interfaces and Feedback

Patterns:
- Chat (web/mobile), voice agents, IDE/browser plugins, inline assists (tooltips, compose boxes).
- Provide “why” affordances (citations, provenance tags).

Feedback capture:
- Explicit thumbs + rationale prompts.
- Edit-distance-based implicit signals (how much user changes generated text).
- Safe-report buttons for policy violations.
- Tie feedback to exact model/prompt/dataset versions.

---

## Data and Dataset Engineering

Tasks:
- Acquisition: public + proprietary; rights and privacy checked.
- Cleaning: deduplication, tokenization, PII removal, toxicity filtering.
- Structuring: chunking, metadata tagging (source, date, product, jurisdiction).
- Labeling:
  - Close-ended: standard annotators, consensus.
  - Open-ended: rubric scoring, LLM-assisted prelabels, human verification.
- Synthetic data:
  - Use to augment scarce cases, edge scenarios.
  - Guard against model self-reinforcement; mix sources.

Quality control:
- Hold-out and canary sets.
- Drift monitoring: input distributions, model outputs (topic/style/sentiment).
- Data governance: lineage, consent, retention, deletion workflows.

---

## Agents and Tool Use

When to use:
- Tasks require external actions (APIs, DB, calendar, calls) or multi-step planning.

Design:
- Tools with strict schemas and side effects explicit.
- Permissions/consent: per-tool scopes; dry-run option.
- Planning: restrict to minimal tool set; prefer deterministic planners for critical paths.

Evaluation:
- Success rate per tool; end-to-end task completion; tool error handling.
- Safety: reversible actions, sandboxing, rate limits, retries with backoff, circuit breakers.

---

## Use Case Pattern Snapshots

- Coding
  - KPIs: task completion, code acceptance rate, test pass rate, time-to-ship.
  - Stack: inline IDE assist + RAG on repo/docs + finetune for repo conventions.
  - Pitfalls: insecure snippets, hallucinated APIs; mitigate with static analysis/tests.

- Image/Video Production
  - KPIs: throughput, approval rate, variant performance (A/B), brand compliance.
  - Stack: diffusion/vid models + prompt templates + safety filter + asset mgmt.
  - Pitfalls: IP concerns; store provenance (watermarks, source tags).

- Writing/Comms
  - KPIs: reply time, engagement, conversion, readability.
  - Stack: prompt templates (tone), style guides, structured output, human-in-loop edits.
  - Pitfalls: SEO spam/low-quality content; enforce quality rubrics.

- Education
  - KPIs: learning gains, time-on-task, retention.
  - Stack: personalization memory, exercise generation, rubric grading, safety.
  - Pitfalls: over-reliance; require explanations/steps and active recall prompts.

- Conversational Bots (support/product copilots)
  - KPIs: deflection rate, CSAT, escalation quality, first-contact resolution.
  - Stack: intent classifier, policy RAG, tool-use for account lookup/tickets.
  - Pitfalls: hallucination; force grounding and abstentions; strict escalation logic.

- Information Aggregation/Summarization
  - KPIs: time saved, accuracy, coverage.
  - Stack: RAG, long-context chunking, multi-doc synthesis with citations.
  - Pitfalls: source mixing; always cite and link.

- Data Organization/Extraction (IDP)
  - KPIs: extraction accuracy, exception rate, cycle time.
  - Stack: doc parsers (PDF/vision), structured extraction prompts, validators, finetune.
  - Pitfalls: layout variance; add layout-aware parsing and few-shot examples per template.

- Workflow Automation
  - KPIs: completion rate, rework rate, SLA adherence.
  - Stack: agents with tools, deterministic fallbacks, audit trail, approvals.
  - Pitfalls: silent failures; instrument with step-level logs and alerts.

---

## Prompts and Patterns

General instruction template:

```
System: You are a careful assistant. Follow policy, avoid speculation, cite sources when provided.
User: {task_description}
Context (sources): 
{context}
Requirements:
- Output format: {format_spec}
- If missing info: say "I don't know".
- Constraints: {constraints}
Examples:
{few_shots}
```

Classification:

```
Classify the message into one of: ["billing", "technical", "sales", "other"].
Message: "{text}"
Return JSON: {"label": "<one_of_labels>", "confidence": 0-1}
```

Extraction (structured JSON):

```
Extract fields from the invoice text.
Fields:
- invoice_number: string
- issue_date: YYYY-MM-DD
- total_amount_usd: number
- vendor_name: string

Text:
{doc_text}

Return valid JSON only.
```

Grounded QA (with citations):

```
Answer using only the provided context. If not present, state "I don't know."
Question: {q}
Context:
{chunks_with_ids}
Return:
{
 "answer": "...",
 "citations": ["S:12","S:45"]
}
```

Self-consistency for reasoning (lightweight):

```
Solve the problem. Think step by step. Provide the final answer as "ANSWER: <value>".
```

Use multiple samples (n=3–5) with majority vote; caution: chain-of-thought content should not be exposed to users if sensitive.

---

## Minimal Code Patterns

OpenAI-compatible chat call (Python):

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
  model="gpt-4o-mini",
  temperature=0.2,
  messages=[
    {"role":"system","content":"You are a concise assistant."},
    {"role":"user","content":"Summarize this in 3 bullets:\n" + text}
  ],
  stream=True
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

Node.js:

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const stream = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  temperature: 0,
  stream: true,
  messages: [
    { role: "system", content: "You are precise and brief." },
    { role: "user", content: `Classify intent: ${text}` },
  ],
});
for await (const part of stream) {
  process.stdout.write(part.choices[0]?.delta?.content || "");
}
```

Prompt versioning:

```python
# python
from dataclasses import dataclass

@dataclass
class Prompt:
    version: str
    template: str

CURRENT_PROMPT = Prompt(
  version="intent/v1.3.2",
  template='Classify into ["billing","technical","sales","other"]:\n{text}\nReturn JSON.'
)

# Log version with every request & eval
```

RAG with access control:

```python
def filter_docs(user, docs):
    return [d for d in docs if user.has_access(d["meta"]["access_level"])]
```

Guardrail (JSON schema validation):

```python
import jsonschema, json

schema = {"type":"object","properties":{
  "label":{"type":"string","enum":["billing","technical","sales","other"]},
  "confidence":{"type":"number","minimum":0,"maximum":1}
}, "required":["label","confidence"]}

def validate_output(txt):
    obj = json.loads(txt)
    jsonschema.validate(obj, schema)
    return obj
```

---

## Go-Live Checklists

Pre-flight
- [ ] Business case with ROI estimates and clear metrics
- [ ] Golden test set with pass thresholds
- [ ] Safety tests: PII, toxicity, policy compliance
- [ ] Latency/cost budgets defined and met (TTFT/TPOT/$ per task)
- [ ] Monitoring/alerting for quality, latency, cost, safety
- [ ] Versioning: model, prompt, datasets, retrieval config
- [ ] Rollback plan and canary deployment

Launch
- [ ] Feature flagging by cohort
- [ ] Logging: inputs, outputs, citations/tools, versions
- [ ] Feedback UX with rationales
- [ ] Data retention and privacy policy in place

Post-launch
- [ ] Weekly eval re-runs; regression detection
- [ ] Error triage loop; dataset updates; finetune cadence (if applicable)
- [ ] Cost optimization review; provider price/model updates
- [ ] Policy & compliance audit trail maintained

---

## Common Pitfalls and Fixes

- Hallucinations
  - Fix: RAG with strict grounding; instruct abstention; cite sources; penalize unsupported claims in evals.

- Brittle prompts
  - Fix: Use few-shot; enforce structured outputs; unit tests for prompts; prompt versioning.

- Latency spikes
  - Fix: Stream responses; reduce output length; use smaller/finetuned models; enable caching; batch non-interactive.

- Cost overruns
  - Fix: Right-size model per route; prompt compression; finetune to smaller models; monitor token usage per feature.

- Safety/compliance failures
  - Fix: Pre- and post-filters; policy prompts; red-teaming; tool whitelists; audit logs.

- Data leakage/PII
  - Fix: Anonymize; apply access control in retrieval; do not log sensitive fields; scope memory per user.

- Over/under-retrieval in RAG
  - Fix: Tune chunk sizes/overlap; hybrid search; rerank; query rewriting; metadata filters.

---

## AI vs ML Engineering: What’s Different (Actionably)

- Less emphasis on bespoke modeling; more on adaptation (prompt/RAG/finetune) and evaluation.
- Models are larger → inference optimization and GPU literacy matter more.
- Open-ended outputs → evaluation is harder; invest early in harnesses and rubrics.
- Interfaces matter → get full-stack engineers involved; ship product-first prototypes quickly.
- Product workflow has shifted → build UI and feedback loops first, then deepen models/data.

---

## Maintenance and Change Management

- Model churn readiness:
  - Abstraction layer for providers; test suites per model; fallbacks.
  - Prompt/model compatibility matrix; smoke tests before switching.

- Version everything:
  - Model (provider + version), prompt (semver), dataset snapshot hash, retrieval config.
  - Store with each prediction for reproducibility.

- Regulatory/IP:
  - Track training data usage rights; avoid models with unclear IP if product IP is critical.
  - Regional deployment strategies for data locality/compliance.

- Cost and performance drift:
  - Monthly review; renegotiate providers; consider self-host when scale justifies.
  - Watch for context length creep; enforce summary/memory policies.

---

## Quick Reference: Technique Selection Flow

1) Is the task grounded in your docs/data?
- Yes → RAG
- No → Prompting first

2) Is performance below threshold after prompting/RAG?
- Yes → Finetune
- No → Ship with guardrails

3) Do you need tool actions?
- Yes → Add agent tools with strict schemas and permissions

4) Latency too high?
- Use smaller/finetuned models, streaming, caching, quantization, speculative decoding

5) Costs too high?
- Shorten prompts/outputs, route to cheaper models, distill, finetune smaller models

---

This reference gives you the essential decision points, patterns, and code to move from idea to a robust, evaluable AI application built on foundation models.