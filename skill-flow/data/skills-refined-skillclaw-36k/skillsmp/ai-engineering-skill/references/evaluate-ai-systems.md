# Evaluate AI Systems — Practitioner Reference

Use this guide to design, select, and continuously evaluate AI systems with clear criteria, reliable methods, and actionable workflows.

## Quick Start Checklist

- Define success
  - What user tasks must succeed? What’s “good enough” vs “must-have”?
  - Map model metrics to business metrics (automation rate, CSAT, cost, latency).
- Choose criteria per use case
  - Domain capability, generation quality (factuality, safety), instruction-following, cost/latency.
- Build a small, trustworthy eval set
  - 100–1,000 examples per slice; clear rubrics; include “gotchas” and out-of-scope inputs.
- Automate verification
  - Exact metrics where possible; AI-judges with crisp rubrics elsewhere; specialized classifiers for safety/toxicity.
- Run a private leaderboard
  - Compare candidate models across your criteria with weighted aggregation.
- Decide build vs buy
  - Data privacy, functionality (tool use, logprobs), cost at scale, control, on-device needs, licensing.
- Monitor in production
  - Daily regression checks, drift detection, human spot checks, user feedback loops.

---

## Evaluation Criteria and Methods

### Criteria Overview (what to measure and how)

- Domain-specific capability
  - What: Coding, math, legal, medical, multilingual, tool use.
  - How: Exact evaluation, functional correctness, multiple-choice, pass@k, runtime/memory, efficiency.
- Generation capability
  - What: Factual consistency (local/global), safety (toxicity, bias), relevance, conciseness.
  - How: AI-judges, entailment/NLI models, retrieval-grounded checks, toxicity classifiers.
- Instruction-following capability
  - What: Format adherence (JSON/YAML, bullet counts), content constraints (“use Victorian English”), style/tone, schema conformance.
  - How: Automatic verifiers, regex/JSON Schema, AI-judges for non-detectable constraints.
- Cost and latency
  - What: Cost per token, time-to-first-token (TTFT), time-per-token, P90 total latency, throughput (TPM).
  - How: Benchmark with internal prompts; measure under production-like settings.

### Criteria-to-Method Mapping

- Use exact, deterministic metrics where possible (runtime, memory, function tests).
- Use small, specialized models when reliable (toxicity, NLI).
- Use AI-judges for subjective criteria (factuality, style), with strict rubrics and temp=0.
- Combine cheap/wide and expensive/deep evaluators (triage + spot-checking).
- Always tie model metrics to business outcomes.

---

## Domain Capability Evaluation

- Code generation
  - Functional correctness (unit tests, end-to-end tests).
  - Efficiency: runtime vs ground-truth baseline (e.g., SQL execution time vs gold).
  - Readability: AI-judge or human rating with rubric (naming, comments, structure).
- Close-ended benchmarks
  - Use multiple-choice where applicable (accuracy, F1, precision/recall).
  - Beware prompt sensitivity; standardize prompt formats.

Code pattern: functional correctness for code tasks

```python
import subprocess, tempfile, json, time

def run_tests(code_str: str, tests: str, timeout=10):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code_str.encode("utf-8"))
        code_path = f.name
    start = time.time()
    proc = subprocess.run(
        ["pytest", "-q", tests], timeout=timeout,
        capture_output=True, text=True
    )
    elapsed = time.time() - start
    passed = (proc.returncode == 0)
    return {"passed": passed, "elapsed_sec": elapsed, "stdout": proc.stdout, "stderr": proc.stderr}

# Example usage:
# result = run_tests(generated_code, "tests/test_problem.py")
# metrics: pass@1 rate, mean runtime, failure modes
```

SQL efficiency check (execute and compare runtime)

```python
import time
import psycopg2

def timed_query(conn, sql, timeout=15):
    cur = conn.cursor()
    start = time.time()
    cur.execute(f"SET statement_timeout = {timeout * 1000};")
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        elapsed = time.time() - start
        return {"ok": True, "rows": rows, "elapsed_sec": elapsed}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def compare_efficiency(conn, gold_sql, gen_sql):
    gold = timed_query(conn, gold_sql)
    gen = timed_query(conn, gen_sql)
    return {
        "gold_ok": gold["ok"], "gen_ok": gen["ok"],
        "exec_accuracy": gold["ok"] and gen["ok"] and (gold["rows"] == gen["rows"]),
        "runtime_ratio": (gen["elapsed_sec"] / gold["elapsed_sec"]) if (gold["ok"] and gen["ok"]) else None
    }
```

---

## Generation Capability — Factual Consistency

Types:
- Local: verify against given context (summarization, RAG).
- Global: verify against open knowledge (search, knowledge bases).

Recommended approaches:
- AI-judge with strict rubric and temp=0.
- Textual entailment (NLI) between (context, claim): entail/contradict/neutral.
- Self-verification: generate alternate answers; compute agreement.
- Knowledge-augmented verification: decompose into claims; search; verify.

AI-judge prompt (local factuality)

```text
You are a strict evaluator of factual consistency.

Task: Does the summary contain any untruthful or misleading facts not supported by the source text?

Source:
{{document}}

Summary:
{{summary}}

Instructions:
- Consider only the source text as ground truth.
- Identify specific unsupported or contradictory claims.
- Output JSON with:
  - consistent: true/false
  - issues: [ {span, reason} ]

Answer:
```

NLI scorer pattern (Hugging Face DeBERTa-v3 MNLI/FEVER/ANLI)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_id = "microsoft/deberta-v3-base-mnli"
tok = AutoTokenizer.from_pretrained(model_id)
m = AutoModelForSequenceClassification.from_pretrained(model_id).eval()

def nli(premise: str, hypothesis: str):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = m(**inputs).logits.softmax(-1).squeeze()
    labels = ["entailment", "neutral", "contradiction"]
    # DeBERTa MNLI label order may vary; verify mapping for the checkpoint you use
    idx = int(torch.argmax(logits))
    return {"label": labels[idx], "probs": {labels[i]: float(logits[i]) for i in range(3)}}

def local_factuality(context: str, claims: list[str], threshold=0.6):
    results = []
    for c in claims:
        res = nli(context, c)
        results.append({"claim": c, **res})
    contradictions = [r for r in results if r["label"] == "contradiction" and r["probs"]["contradiction"] >= threshold]
    return {"consistent": len(contradictions) == 0, "details": results}
```

Claim decomposition (for SAFE-like verification)

```python
def extract_claims(text, llm):
    prompt = (
        "Extract atomic, self-contained factual statements from the text. "
        "Return JSON list under key 'claims'.\nText:\n" + text
    )
    return llm.json(prompt)["claims"]

def search_and_verify(claim, search, llm):
    queries = llm.text(f"Generate 3 search queries to fact-check: {claim}")
    hits = []
    for q in queries.splitlines():
        hits += search(q, top_k=3)
    evidence = "\n\n".join([h["snippet"] for h in hits])
    judge = llm.json(
        "Given the claim and evidence snippets, decide if evidence supports the claim. "
        "Output JSON {label: 'supported'|'refuted'|'insufficient', rationale: str}.\n"
        f"Claim:\n{claim}\n\nEvidence:\n{evidence}"
    )
    return judge
```

SelfCheckGPT-style agreement

```python
def self_agreement(original_answer, question, llm, n=5):
    alts = [llm.text(f"{question}\nProvide a concise answer only.") for _ in range(n)]
    agree = sum(1 for alt in alts if alt.strip() == original_answer.strip())
    return {"n": n, "agree_count": agree, "agreement_rate": agree / n}
```

Factuality metrics to track
- Hallucination rate = fraction of responses with at least one unsupported claim.
- Claim-level contradiction rate.
- Grounding rate (RAG): fraction of sentences that are supported by retrieved docs.
- Precision/recall of citations (if citations attached).

Benchmark ideas
- TruthfulQA subsets for your domain.
- Internal “hard” set: niche queries; nonexistent facts; adversarial prompts.

---

## Generation Capability — Safety

Categories to screen
- Inappropriate: profanity, explicit content.
- Harmful instructions: violence, weapons, self-harm, illegal activities.
- Hate/harassment: protected classes, slurs.
- Violence/graphic content.
- Stereotypes, political/religious bias.

Recommended pipeline
- Pre-filter input with a fast classifier; reject/transform unsafe inputs.
- Post-filter output with a fast classifier; block/redact or route to human.
- AI-judge for edge cases; keep sampling temp=0; log with rationales.

Code patterns

Toxicity classifier (example using a small transformer)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tox_id = "unitary/unbiased-toxic-roberta"
tok = AutoTokenizer.from_pretrained(tox_id)
m = AutoModelForSequenceClassification.from_pretrained(tox_id).eval()

def toxicity_score(text):
    with torch.no_grad():
        logits = m(**tok(text, return_tensors="pt", truncation=True)).logits
    prob = torch.sigmoid(logits).squeeze().tolist()  # multi-label heads
    # Combine heads as needed; or threshold specific categories
    return prob
```

Guard pattern

```python
def moderate(text, allowlist=None, thresholds=None):
    scores = toxicity_score(text)
    violations = []
    # Example: indices map to categories; set thresholds per category
    for cat, score in enumerate(scores):
        if score >= thresholds.get(cat, 0.8):
            if not (allowlist and allowlist(cat, text)):
                violations.append((cat, score))
    return {"allowed": len(violations) == 0, "violations": violations}
```

Best practices
- Maintain safety policy doc linked to categories and thresholds.
- Log all blocked events with reason codes for audits.
- Evaluate fairness: false positives across dialects and languages; slice by group.
- Red-team with datasets like RealToxicityPrompts, BOLD; track fail rates.

---

## Instruction-Following Capability

Automatic checks (IFEval-style)
- Keywords: inclusion, forbidden words, frequency.
- Language constraints.
- Length constraints: word/sentence/paragraph counts.
- Format: bullets, title markers, section headers, JSON/YAML.
- Schema: JSON Schema validation (strict), regex.

AI-judge checks (INFOBench-style)
- Content constraints: “only discuss climate change”.
- Linguistic style: “use Victorian English”.
- Tone guidelines: “be respectful”, “kid-friendly”.
- Role consistency.

Implement automatic validators

```python
import json
from jsonschema import validate, ValidationError
import re

def must_contain(text, keywords): return all(k in text for k in keywords)
def must_not_contain(text, forbidden): return all(k not in text for k in forbidden)
def word_count(text): return len(re.findall(r"\b\w+\b", text))

def validate_json_schema(s, schema):
    try:
        obj = json.loads(s)
        validate(instance=obj, schema=schema)
        return True, obj
    except (json.JSONDecodeError, ValidationError):
        return False, None

def validate_format(text, spec):
    checks = []
    if "keywords" in spec: checks.append(must_contain(text, spec["keywords"]))
    if "forbidden" in spec: checks.append(must_not_contain(text, spec["forbidden"]))
    if "max_words" in spec: checks.append(word_count(text) <= spec["max_words"])
    if "exact_bullets" in spec: checks.append(text.count("\n* ") == spec["exact_bullets"])
    return all(checks)
```

Prompt for structured output with hard fail

```text
Return ONLY valid JSON that conforms to this schema:
{"type":"object","properties":{"sentiment":{"enum":["NEGATIVE","NEUTRAL","POSITIVE"]}},
"required":["sentiment"],"additionalProperties":false}

Text:
{{input}}

If you cannot determine the sentiment, output:
{"sentiment":"NEUTRAL"}
```

Recovery loop

```python
def generate_with_validation(prompt, llm, schema, retries=2):
    for _ in range(retries+1):
        out = llm.text(prompt)
        ok, obj = validate_json_schema(out, schema)
        if ok: return obj
        prompt = f"The previous output was invalid JSON. Fix to satisfy schema:\n{schema}\nOriginal output:\n{out}"
    raise ValueError("Failed to produce valid JSON")
```

Use logprobs for classification (if available)
- Compare probabilities across label tokens; abstain if confidence < threshold.
- Reduces silent format drift.

---

## Roleplaying Evaluation

What to test
- Style fidelity: lexicon, cadence, persona quirks.
- Knowledge/canon: facts known/not known by the role (avoid spoilers; “negative knowledge”).
- Constraint adherence: brevity, politeness, non-omniscience.

Heuristics
- Average length if character is terse.
- Catchphrases/tics frequency limits (avoid overuse).
- Off-canon detection via knowledge constraints.

AI-judge prompt snippet

```text
You are judging role consistency.

Role: {{role_name}}
Description & cues: {{description}}

User request: {{user_prompt}}
Model reply: {{reply}}

Score 1-5:
1 = breaks character or invents outside knowledge
3 = mostly consistent with occasional slips
5 = entirely consistent in style and knowledge

Return JSON: {"style": int, "knowledge": int, "notes": "..."}
```

---

## Cost and Latency

Key metrics
- Cost/token (input/output); total cost/query.
- Latency:
  - Time to first token (TTFT).
  - Time between tokens (TBT); throughput tokens/sec.
  - Total time per query (P50/P90/P99).
- Scale: tokens per minute (TPM), concurrent sessions.

Workflow
- Define hard latency bounds (e.g., TTFT <200ms P90; total <30s P90).
- Measure under realistic payload sizes and sampling params.
- Tune prompt to reduce verbosity; set max tokens/stopping conditions.
- Pareto optimize across cost–quality–latency; fix non-negotiables first.

---

## Model Selection Workflow

1) Filter by hard attributes
- Privacy: data cannot leave VPC? On-device requirement?
- License: commercial use allowed? Distillation allowed?
- Functionality: tool use/function calling required? Logprobs? Finetuning support?
- Jurisdiction/availability: region support, SLAs, uptime.

2) Narrow with public evidence
- Benchmarks relevant to your task; beware contamination.
- Leaderboard ranks are directional; check benchmark coverage and weights.

3) Private evaluation
- Build a weighted private leaderboard across your criteria.
- Use your own data, rubrics, and automatic verification where possible.
- Measure cost/latency with your prompts and traffic patterns.

4) Production monitoring
- Drift alerts; daily spot-checks; user feedback integration.
- Canary when switching models/prompts; rollback plans.

Hard vs soft attributes
- Hard: licenses, privacy constraints, access, required functionality you cannot modify.
- Soft: accuracy, safety, factuality, format adherence (improvable via prompting/finetune).

Aggregation options
- Weighted average of normalized scores (z-score or min-max per benchmark).
- Mean win rate (fraction of benchmarks where model A > model B).
- Penalize missing functionality as hard fail or large negative weight.

---

## Build vs Buy (Open Source vs Model APIs)

Definitions
- Open weight: downloadable model weights; training data not necessarily open.
- “Open model”: weights + training data publicly available.
- Restricted licenses may limit commercial use or distillation.

Key license questions
- Commercial use allowed?
- Monthly Active User (MAU) caps?
- Distillation/synthetic data use permitted?
- On-device redistribution allowed?

Pros and cons

| Dimension | Model APIs | Self-Hosting Open Source |
|---|---|---|
| Data privacy | Must send data to provider (unless private deployment) | Keep data in VPC/on-device |
| Performance | Access to top-tier proprietary models | Best open models; often trailing top proprietary |
| Functionality | Mature tool use, structured outputs; may limit logprobs | Full access to internals; may require building features |
| Cost | Pay per token; predictable | Engineering cost; cheaper at scale; control over infra |
| Finetuning | Only if provider supports; limited modes | Any tuning method subject to license; more control |
| Control | Provider rate limits/censorship; model changes | Freeze versions; full transparency; maintain APIs yourself |
| Edge | Requires internet | On-device possible |

Decision guide
- Choose APIs if:
  - You need best-in-class performance now.
  - You want low engineering overhead and mature tooling.
  - Data can be shared under provider terms (or private managed deployment).
- Choose self-hosting if:
  - Strict privacy/on-device constraints.
  - Must have logprobs/intermediate signals.
  - Need full control (custom safety, finetune modes, version freezing).
  - Large-scale usage where infra amortizes cost.

---

## Using Public Benchmarks Wisely

Selection tips
- Pick benchmarks aligned with your use case (coding, math, retrieval, instruction-following, safety).
- Check saturation (many SOTA models already near ceiling).
- Assess correlation: avoid overweighting redundant benchmarks.
- Verify contamination risks (older public sets likely in training data).

Aggregation choices
- Weighted average (assign weights by business importance).
- Mean win rate across scenarios.
- Normalize scores to comparable scales.

Cost realities
- Running large suites can be expensive; start with a small, high-signal subset.
- Use harnesses where possible: lm-evaluation-harness, OpenAI Evals.

Data contamination handling
- Detect via n-gram overlap (if training data accessible) and perplexity anomalies.
- Report clean vs overall performance where possible.
- Keep private hold-out subsets; rotate with new examples.

n-gram overlap sample (requires training corpus access)

```python
def has_13gram_overlap(eval_text, train_index):
    tokens = eval_text.split()
    for i in range(len(tokens) - 12):
        gram = " ".join(tokens[i:i+13])
        if gram in train_index: return True
    return False

# Build train_index as a set of 13-grams from training corpus (memory heavy; consider MinHash)
```

Perplexity anomaly (proxy for contamination)

```python
def perplexity(model, tok, text):
    ids = tok(text, return_tensors="pt").input_ids
    with torch.no_grad():
        loss = model(ids, labels=ids).loss
    return float(torch.exp(loss))

# Flag samples with unusually low perplexity compared to distribution on held-out clean text
```

---

## Design Your Evaluation Pipeline

### Step 1. Evaluate all components

- Component-level: e.g., PDF-to-text accuracy; then entity extraction accuracy on ground-truth text.
- Turn-level: quality per message/step; detects degradation early.
- Task-level: goal completion rate; average turns to completion.

Example (Twenty Questions task)
- Success = guess correct; fewer turns is better.
- Track task success and turn count distribution.

### Step 2. Create evaluation guidelines

- Define criteria and what “good” means; include negative examples.
- Specify in-scope vs out-of-scope inputs and expected handling.
- Build clear rubrics with labeled examples.

Rubric template (YAML)

```yaml
criteria:
  - name: relevance
    scale: 0-1
    definition: "Answer addresses user's query without digression."
    examples:
      - input: "How to reset password?"
        output_good: "Steps to reset password..."
        output_bad: "Here’s our company history..."
  - name: factual_consistency
    scale: contradiction/neutral/entailment or 0-1
    definition: "Supported by provided context."
  - name: safety
    scale: 0-1
    definition: "No toxic or harmful content."
scoring:
  pass_threshold:
    relevance: 1
    factual_consistency: "entailment"
    safety: 1
```

Tie metrics to business metrics
- Example mapping:
  - 80% factuality → automate 30% tickets.
  - 90% factuality → automate 50%.
  - 98% factuality → automate 90%.
- Define usefulness threshold: minimum metric values to ship.

### Step 3. Select methods and data

- Mix methods:
  - Cheap classifiers for 100% coverage; AI-judges on stratified 1–10% samples.
  - Use logprobs where available to assess confidence and abstain.
- Annotation
  - Use real production data where possible.
  - Reuse rubrics for both evaluation and training data creation later.
- Slicing
  - Segment by user type, input length, language, topic, platform, error-prone patterns.
  - Maintain slice-specific eval sets to avoid Simpson’s paradox.

Bootstrapping for stability

```python
import random

def bootstrap_eval(examples, eval_fn, k=100, rounds=50):
    scores = []
    for _ in range(rounds):
        samp = [random.choice(examples) for _ in range(k)]
        scores.append(eval_fn(samp))
    return {"mean": sum(scores)/len(scores), "stdev": (sum((s - sum(scores)/len(scores))**2 for s in scores)/len(scores))**0.5}
```

Sample size guidance (95% confidence; rough)
- 30% difference → ~10 samples
- 10% difference → ~100 samples
- 3% difference → ~1,000 samples
- 1% difference → ~10,000 samples

### Step 4. Evaluate your evaluation

- Signal validity: Do higher scores correlate with better business outcomes?
- Reliability:
  - Reproducibility (same inputs and config → same result).
  - Variance across bootstraps; reduce with more data or clearer rubrics.
  - Fix randomness (seed; temp=0 for judges).
- Metric correlation:
  - Remove redundant metrics; investigate unexpected independence.
- Overhead:
  - Track evaluation cost/latency; optimize cascade (cheap screeners → expensive judges for borderline cases).

### Iterate

- Version and track: eval datasets, rubrics, judge prompts, sampling params.
- Keep a stable core test set for longitudinal comparison; rotate a portion to avoid overfitting.
- Treat evaluation assets as production code (reviews, CI, changelogs).

---

## RAG-Specific Evaluation

What to measure
- Retrieval:
  - Recall@k: fraction of answers supported by any retrieved doc.
  - Precision@k: fraction of retrieved docs that are relevant.
- Groundedness:
  - Sentence-level entailment against retrieved passages.
  - Citation correctness (IDs/URLs align to claims).
- End-to-end:
  - Answer factual consistency (local).
  - Final helpfulness/relevance.

Pipeline sketch

```python
def eval_rag(question, answer, retrieved_docs, nli):
    # 1) Retrieval relevance
    rel_docs = [doc for doc in retrieved_docs if semantic_sim(doc["text"], question) > 0.7]
    recall = int(len(rel_docs) > 0)
    precision = len(rel_docs)/len(retrieved_docs) if retrieved_docs else 0.0

    # 2) Decompose answer into claims
    claims = extract_claims(answer, llm)

    # 3) For each claim, find best supporting doc and run NLI
    support = []
    for c in claims:
        best = max(retrieved_docs, key=lambda d: semantic_sim(d["text"], c), default=None)
        if not best:
            support.append({"claim": c, "label": "insufficient"})
            continue
        res = nli(best["text"], c)
        label = "supported" if res["label"] == "entailment" else ("refuted" if res["label"] == "contradiction" else "insufficient")
        support.append({"claim": c, "label": label, "doc_id": best.get("id")})

    grounded = sum(1 for s in support if s["label"] == "supported") / max(1, len(support))
    hallucination_rate = sum(1 for s in support if s["label"] == "refuted") / max(1, len(support))

    return {"recall": recall, "precision": precision, "grounded": grounded, "hallucination_rate": hallucination_rate}
```

---

## Example: End-to-End Evaluation Runner

Composable evaluation harness

```python
from dataclasses import dataclass
from typing import Callable, Dict, Any, List

@dataclass
class EvalResult:
    name: str
    score: float
    details: Dict[str, Any]

class Evaluator:
    def __init__(self, metrics: List[Callable]):
        self.metrics = metrics

    def evaluate(self, dataset, model) -> List[EvalResult]:
        results = []
        for metric in self.metrics:
            score, details = metric(dataset, model)
            results.append(EvalResult(metric.__name__, score, details))
        return results

# Metric examples
def metric_instruction_adherence(dataset, model):
    passed, total = 0, 0
    for ex in dataset:
        out = model.generate(ex["prompt"])
        ok = validate_format(out, ex["format_spec"])
        passed += int(ok); total += 1
    return passed/total, {"passed": passed, "total": total}

def metric_factual_local(dataset, model):
    violations = 0; total = 0
    for ex in dataset:
        out = model.generate(ex["prompt"], context=ex["context"])
        claims = extract_claims(out, llm)
        res = local_factuality(ex["context"], claims)
        violations += int(not res["consistent"]); total += 1
    return 1 - (violations/total), {"violations": violations, "total": total}

def metric_safety(dataset, model):
    unsafe = 0; total = 0
    for ex in dataset:
        out = model.generate(ex["prompt"])
        mod = moderate(out, thresholds={0:0.8})
        unsafe += int(not mod["allowed"]); total += 1
    return 1 - (unsafe/total), {"unsafe": unsafe, "total": total}
```

Weighted aggregation

```python
def aggregate(results: List[EvalResult], weights: Dict[str, float]):
    tot, wsum = 0.0, 0.0
    for r in results:
        w = weights.get(r.name, 1.0)
        tot += w * r.score; wsum += w
    return tot / wsum if wsum else 0.0
```

---

## Common Pitfalls and How to Avoid Them

- Evaluating only end-to-end
  - Also evaluate components; otherwise you can’t localize failures.
- Vague rubrics for AI-judges
  - Provide definitions, examples, and JSON outputs; set temperature=0.
- Overreliance on public leaderboards
  - Build your private leaderboard with your data and weights.
- Ignoring contamination
  - Keep private hold-outs; rotate examples; monitor perplexity anomalies.
- No budget for evaluation cost/latency
  - Use cascaded evaluation; sample for expensive checks; cache results.
- Not monitoring in production
  - Daily regressions and drift checks; canaries for changes; rollback plan.
- No user feedback loop
  - Capture thumbs up/down, task completion, abandonment; route to re-training/finetuning.

---

## Decision Frameworks

Model selection
- Hard filters: privacy, licensing, required features (tools, logprobs), regions.
- Shortlist via public signals: task-aligned benchmarks, latency/cost reports.
- Run private eval: weighted scores on your criteria; include cost and latency.
- Choose Pareto-optimal option that meets hard constraints.

Instruction-following verification
- If instruction is auto-verifiable (format, schema, counts) → write programmatic checks.
- If not (style, tone, audience appropriateness) → AI-judge with rubric and examples.
- For structured outputs → JSON Schema + repair loop + abstain on failure.

Factual consistency
- If context provided → local (NLI + AI-judge).
- If no context → claim decomposition + search + verification.
- For RAG → add retrieval quality metrics + groundedness.

Safety
- Always-on fast classifier; AI-judge for edge.
- Maintain policy thresholds; slice by group/language; log with reason codes.

---

## Example Benchmarks and Tools (use selectively)

- Instruction following
  - IFEval: auto-verifiable instruction types (keywords, format, JSON).
  - INFOBench: broader content/style constraints; AI-judge verification.
- Factuality
  - TruthfulQA: resistance to human falsehoods.
- Safety/toxicity/bias
  - RealToxicityPrompts; BOLD; hate speech/toxicity classifiers.
- Domain
  - Coding: HumanEval; pass@k; runtime checks.
  - Math: GSM-8K, MATH lvl 5, BBH.
  - General knowledge/reasoning: MMLU, ARC-C, HellaSwag, GPQA, MuSR.
- Evaluation harnesses
  - lm-evaluation-harness; OpenAI Evals.
- Entailment
  - DeBERTa-v3 MNLI/FEVER/ANLI variants.

---

## Production Monitoring Playbook

- Daily automated checks
  - Sample N outputs per use case; compute key metrics (factuality, safety, format).
  - Compare to 7/30-day baselines; alert on deltas > threshold.
- Canary deployments
  - Route 1–5% traffic to new model/prompt; monitor guard metrics; expand upon success.
- Human review
  - Expert review of 100–500 conversations/day for subjective quality; log rationales.
- User feedback
  - UI affordances (thumbs, flags); capture task completion and abandonment.
  - Close the loop: retrain/finetune on curated, rubric-aligned data.

---

## Templates

Weighted criteria table (customize per app)

| Criterion | Metric | Method | Weight | Threshold (fail) | Target (ideal) |
|---|---|---|---:|---:|---:|
| Factual consistency (local) | Groundedness | NLI + AI-judge | 0.25 | ≥0.85 | ≥0.95 |
| Safety | Toxicity pass rate | Classifier + judge | 0.20 | ≥0.98 | ≥0.995 |
| Instruction adherence | JSON schema pass | Validator | 0.20 | ≥0.95 | ≥0.99 |
| Relevance | Semantic similarity | Embedding sim | 0.10 | ≥0.85 | ≥0.92 |
| Cost | $/1M output tokens | Billing logs | 0.10 | ≤$30 | ≤$15 |
| Latency | P90 total | Timers | 0.10 | ≤30s | ≤10s |
| Domain-specific | Task-specific metric | Exact tests | 0.05 | Custom | Custom |

AI-judge response format

```json
{
  "criterion": "factual_consistency_local",
  "consistent": true,
  "issues": [
    {
      "span": "Sky is purple",
      "reason": "Contradicted by context (sky described as blue)"
    }
  ],
  "confidence": 0.92
}
```

---

## Final Notes

- Prefer exact, automatable metrics; use AI-judges with disciplined rubrics only where needed.
- Build your private leaderboard; treat benchmarks as signals, not truth.
- Evaluation is a product: version it, test it, monitor it, and evolve it deliberately.