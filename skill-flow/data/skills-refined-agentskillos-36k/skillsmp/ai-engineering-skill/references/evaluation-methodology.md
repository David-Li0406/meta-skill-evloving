# Evaluation Methodology — Practitioner Reference

This reference distills Chapter 3 into actionable guidance you can use to design, implement, and operate evaluations for open‑ended AI systems.

Use this when you need to:
- Choose an evaluation method for your use case
- Implement exact, similarity, AI-as-judge, or comparative evaluations
- Compute perplexity and interpret language modeling metrics
- Build quick harnesses and prompts with defensible, repeatable procedures

---

## 1) Choosing an Evaluation Method

Use this decision guide to pick a primary method (you will often combine two or more).

- Do you have objective, executable functionality?
  - Yes → Functional correctness (tests, execution accuracy, measurable objectives)
- Is output short and exact (e.g., numerical answer, classification ID)?
  - Yes → Exact match
- Do you have high-quality reference outputs?
  - Yes → Similarity against references
    - Few, short, standardized responses → Lexical similarity (BLEU/ROUGE)
    - Diverse wording and longer text → Semantic similarity (embedding-based)
- No references, or quality depends on nuanced criteria (helpfulness, groundedness, tone)?
  - Yes → AI-as-judge (pointwise, reference-based, or pairwise)
- You need to pick a model among many without absolute benchmarks?
  - Yes → Comparative (pairwise) evaluation with ranking (Bradley–Terry / Elo / TrueSkill)

Always supplement subjective methods (AI judge, comparative) with a small golden set of exact checks or human spot-reviews.

---

## 2) Language Modeling Metrics Quick Reference

Why it matters: LM metrics like perplexity correlate with downstream performance and are useful for training, deduplication, contamination checks, and anomaly detection.

Key definitions:
- Entropy H(P): average information per token in true data distribution
- Cross entropy H(P, Q): how hard model Q finds data P (lower is better)
- Perplexity PPL(P, Q) = exp(H(P, Q)) or 2^(H) depending on log base (lower is better)
- Bits-per-character (BPC), bits-per-byte (BPB): compression efficiency variants of cross entropy

Interpretation:
- Lower perplexity means higher next-token prediction accuracy
- Expect lower PPL for structured data (e.g., code, HTML), larger PPL for rich vocabulary or shorter contexts
- Post-training (SFT/RLHF) and quantization can increase PPL while improving task performance; don’t use PPL alone to compare aligned vs. base models

Practical uses:
- Model selection proxy (with caution for aligned models)
- Data deduplication: include new data when PPL is high on the current model
- Data contamination detection: suspiciously low PPL on a benchmark suggests leakage
- Anomaly detection: unusually high PPL indicates abnormal/gibberish text

Compute perplexity (open-source causal LM):

```python
# pip install transformers torch datasets
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, math

def perplexity_on_texts(model_name, texts, max_length=2048, device='cuda'):
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    model.eval()

    n_tokens, total_loss = 0, 0.0
    with torch.no_grad():
        for text in texts:
            enc = tok(text, return_tensors='pt', truncation=True, max_length=max_length).to(device)
            # Shift labels to predict next token
            labels = enc["input_ids"].clone()
            out = model(**enc, labels=labels)
            loss = out.loss.item()
            n = enc["input_ids"].numel()
            total_loss += loss * n
            n_tokens += n
    avg_loss = total_loss / max(n_tokens, 1)
    ppl = math.exp(avg_loss)  # nat log assumed by most libraries
    return ppl
```

Notes:
- Use the same logging base across models when comparing
- Condition on comparable context length
- Many commercial APIs do not expose token logprobs; use open models or provider-specific logprob APIs when available

---

## 3) Exact Evaluation

### 3.1 Functional Correctness (Execution Accuracy)

When to use:
- Code generation, text-to-SQL, agents with executable steps, planners/schedulers, game bots, optimizers

Core pattern:
- Construct task specs + test cases
- Generate k samples per task
- Execute in sandbox; compare outputs to expected outputs
- Report pass@k: problem considered solved if any of k samples passes all tests

pass@k harness (Python):

```python
import random, traceback, math

def run_candidate(func_src, check_fn):
    # Unsafe: sandbox properly with time/memory limits in prod (e.g., Pyodide, Docker, Firejail, subprocess)
    local_env = {}
    try:
        exec(func_src, {}, local_env)
        candidate = next(v for k, v in local_env.items() if callable(v))
        check_fn(candidate)
        return True, None
    except Exception as e:
        return False, traceback.format_exc()

def pass_at_k(num_solved, num_samples, k):
    # Unbiased estimator from HumanEval
    if k > num_samples:
        return 1.0 if num_solved > 0 else 0.0
    return 1.0 - math.comb(num_samples - num_solved, k) / math.comb(num_samples, k)

def evaluate_codegen(problems, samples_per_problem=10, k=1):
    results = []
    for prob in problems:  # prob: {"prompt", "check_fn", "gen_fn"}
        samples = [prob["gen_fn"](prob["prompt"]) for _ in range(samples_per_problem)]
        passes = 0
        for s in samples:
            ok, _ = run_candidate(s, prob["check_fn"])
            if ok:
                passes += 1
        score = pass_at_k(passes, samples_per_problem, k)
        results.append(score)
    return sum(results) / len(results)
```

Best practices:
- Create strong test sets: hidden tests, edge cases, randomized seeds
- Sandbox execution: resource/time limits, filesystem/network isolation
- Measure both compile/execution success and functional outputs
- Track code reuse/leakage; filter for trivial memorization if benchmarking

### 3.2 Similarity Against Reference Data

When to use:
- Translation, summarization, captioning, shorter inference tasks; when high-quality references exist

Methods:
- Exact match (binary) — good for short answers and fill-in-the-blank
- Lexical similarity — n-gram overlap (BLEU/ROUGE/METEOR/CIDEr)
- Semantic similarity — embedding-based (BERTScore, cosine similarity)

Pitfalls:
- Lexical metrics penalize valid paraphrases; require exhaustive references to be reliable
- Reference quality varies; validate and prune bad references
- Optimize for functional quality, not proxy scores (BLEU can correlate poorly with correctness for code)

Lexical similarity code (BLEU/ROUGE):

```python
# pip install sacrebleu rouge-score
import sacrebleu
from rouge_score import rouge_scorer

def bleu_score(candidates, list_of_references):
    return sacrebleu.corpus_bleu(candidates, list_of_references).score  # 0-100

def rouge_l_score(candidates, references):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = [scorer.score(ref, cand)['rougeL'].fmeasure for cand, ref in zip(candidates, references)]
    return sum(scores) / len(scores)
```

Semantic similarity code (Sentence Transformers cosine):

```python
# pip install sentence-transformers torch
from sentence_transformers import SentenceTransformer
import numpy as np

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))

def semantic_similarity(candidates, references, model_name="sentence-transformers/all-mpnet-base-v2"):
    model = SentenceTransformer(model_name)
    embs_c = model.encode(candidates, normalize_embeddings=True)
    embs_r = model.encode(references, normalize_embeddings=True)
    return float(np.mean([cosine(ec, er) for ec, er in zip(embs_c, embs_r)]))  # ~[-1,1], often [0,1]
```

Best practices:
- Use semantic similarity for diverse phrasings; lexical for rigid formats
- Calibrate thresholds with golden validation set
- For multi-reference tasks, take max across references per candidate
- Cache embeddings; batch inference for speed

---

## 4) Embeddings Quick Primer (for Evaluation)

- Embedding = fixed-length vector capturing semantics
- Use cases in evaluation: semantic similarity, clustering of failures, deduplication, anomaly detection
- Common models:
  - Sentence Transformers (open), CLIP for image-text, various API embeddings
- Similarity: cosine similarity in [-1, 1]; often interpret >=0.8 as “strongly similar” for short texts (calibrate per task)

Cosine formula:
- sim(A, B) = dot(A, B) / (||A|| * ||B||)

Checklist:
- Normalize embeddings before cosine
- Pick model trained for your domain (e.g., code, multilingual)
- Avoid mixing models for ground truths and candidates (distribution shift)

---

## 5) AI as a Judge (LLM-as-Judge)

When to use:
- No or limited references
- Need nuanced, multi-criteria scoring (helpfulness, groundedness, safety)
- Rapid iteration on prompts, models, or system behavior

Core evaluation patterns:
- Pointwise: judge a single (question, answer)
- Reference-based: judge a (question, answer) against ground truth
- Pairwise: judge which of two answers is better

Output designs (favor parsable formats):
- Labels (GOOD/BAD, YES/NO)
- Discrete numeric ratings (1–5; keep ranges small)
- Pairwise choice (A/B or TIE)
- JSON with fields: score, label, rationale, criterion

Judge prompt templates (copy/paste):

Pointwise quality (classification):

```text
System: You are a strict evaluator. Return only JSON.
User:
Evaluate the answer for the question using the criterion below.

Criterion: Overall quality (clarity, correctness, completeness, safety).
Labels: ["BAD","OK","GOOD"]
Instructions:
- Focus on whether the answer sufficiently addresses the question.
- If factual claims are made, flag unsupported statements as BAD.
- Do not reward verbosity.

Question: {{question}}
Answer: {{answer}}

Return JSON:
{"label": "<BAD|OK|GOOD>", "rationale": "<1-2 concise sentences>"}
```

Reference-based faithfulness (binary):

```text
System: You are a strict evaluator. Return only JSON.
User:
Does the generated answer contain only information supported by the context?

Context:
{{context}}

Question:
{{question}}

Answer:
{{answer}}

Return JSON:
{"faithful": "<YES|NO>", "rationale": "<brief reason>"}
```

Pairwise preference (A/B with tie, randomized order):

```text
System: You are a strict and unbiased evaluator. Return only JSON.
User:
Which answer better satisfies the user question? If equivalent, choose TIE.
Ignore style; prioritize correctness and relevance. Do not reward length.

Question:
{{question}}

Answer A:
{{answer_a}}

Answer B:
{{answer_b}}

Return JSON:
{"choice": "<A|B|TIE>", "rationale": "<brief reason>"}
```

Operational best practices:
- Constrain output to JSON; validate schema; re-ask on invalid output
- Fix sampling for determinism where possible (low temperature, fixed seed)
- Include few-shot examples to improve consistency
- Randomize A/B order; strip provider/model names to reduce self-bias
- Track judge version (model ID + prompt hash) in every score
- Calibrate judge on a golden set with human labels; measure agreement
- Use spot-checking to control cost (e.g., 5–20% of traffic); adaptively increase for risky segments
- Use weaker, cheaper judges after verifying correlation with a stronger gold judge

Common biases and mitigations:
- Self-bias (prefers own outputs) → anonymize providers/models; cross-judge with different vendors
- First-position bias → randomize order; repeat with swapped order
- Verbosity bias → penalize length in prompt; enforce max tokens; length-normalized scoring
- Criteria ambiguity → write precise rubrics and examples; single-source judge prompts and version control

Cost/latency strategies:
- Asynchronous judging (return answer immediately; judge in background for QA, analytics)
- Cascade: strong judge on a sample; weaker judge for the rest; escalate disagreements
- Batch evaluation offline

Specialized judges:
- Reward model: (prompt, answer) → scalar reward (e.g., 0–1); small models can suffice with finetuning
- Reference-based judge: (prompt, answer, reference, rubric) → scaled score (e.g., 1–5)
- Preference model: (prompt, A, B) → preferred label; train to predict human preferences

---

## 6) Comparative (Pairwise) Evaluation and Ranking

Use when you want to pick a model among many, and “better/worse” judgments are easier than scoring.

Workflow:
1) Define eligible prompts/tasks and guardrails (exclude correctness-critical queries)
2) Present two (or more) anonymized candidates per prompt (random order)
3) Collect evaluator choices (A/B/Tie) — human or AI judge
4) Log matches: prompt ID, model_a, model_b, winner, timestamp, evaluator type, judge version
5) Compute rankings with a rating algorithm
6) Validate with holdout matches; monitor stability and prediction accuracy
7) Make deployment decisions (swap thresholds, pilot gating)

Match data schema (example):

```json
{
  "match_id": "uuid",
  "prompt_id": "uuid",
  "model_a": "candidate_model_12",
  "model_b": "candidate_model_34",
  "order": ["model_a","model_b"], 
  "winner": "model_b", 
  "tie": false,
  "evaluator": "human|ai",
  "judge_version": "gpt-4o-mini#promptHash123",
  "metadata": {"domain":"math","difficulty":"hard"}
}
```

Rating algorithms:
- Elo: simple, incremental; sensitive to match order; assumes transitivity
- Bradley–Terry: logistic model of pairwise win probabilities; robust; batch estimation
- TrueSkill: Bayesian Elo variant; handles teams and uncertainty

Bradley–Terry (scikit-learn logistic regression):

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

def bradley_terry_ratings(matches, model_ids):
    # matches: list of (winner_id, loser_id, weight=1.0)
    id2idx = {m: i for i, m in enumerate(model_ids)}
    X, y, sample_weight = [], [], []
    for w, l, wt in matches:
        vec = np.zeros(len(model_ids))
        vec[id2idx[w]] = +1
        vec[id2idx[l]] = -1
        X.append(vec); y.append(1); sample_weight.append(wt)
    X, y, sample_weight = np.array(X), np.array(y), np.array(sample_weight)
    lr = LogisticRegression(fit_intercept=False, solver='lbfgs')
    lr.fit(X, y, sample_weight=sample_weight)
    # Coefficients are skill scores up to a constant offset
    skills = lr.coef_.ravel()
    ratings = {m: float(s) for m, s in zip(model_ids, skills)}
    # Convert to pseudo-Elo scale if desired
    elo = {m: 1000 + 400 * s for m, s in ratings.items()}
    return ratings, elo
```

Active match scheduling (to scale):
- Focus on uncertain pairs (close ratings, few matches)
- Allocate more comparisons to high-traffic domains and “hard prompts”
- Stop sampling pairs once outcome is stable (confidence intervals non-overlapping)

Quality control:
- Filter trivial prompts; prefer “hard” prompts
- Train or brief evaluators; add rubrics; discourage factually incorrect but fluent answers
- Integrate into products where users are domain experts (e.g., code editor pairwise suggestions)
- For AI judges, enforce prompt discipline and bias mitigation (see Section 5)

Limitations and remedies:
- Non-transitivity: expect cycles; need more data and diversified prompts/evaluators
- New model insertion: warm-start by comparing against a small, well-spread subset of anchors
- Converting win rates to business impact: A/B pilot top models; measure absolute metrics (e.g., resolution rate, CSAT, latency, cost)

Deployment decisions:
- Swap models when predicted win probability > threshold vs incumbent across core segments
- Consider cost/latency deltas; require minimum margin in win rate (e.g., +3–5%) before switching
- Pilot with traffic splits; monitor key risk metrics (hallucinations, safety violations)

---

## 7) Practical Procedures and Templates

### 7.1 Build a Minimal Evaluation Harness (Open‑Ended Tasks)

1) Define target outcomes and risks (hallucinations, toxicity, off-policy behavior)
2) Create a small golden set (50–200) with exact or human-verified labels
3) Choose primary method:
   - Functional correctness → implement tests; pass@k
   - Similarity → lexical and/or semantic; calibrate thresholds
   - AI judge → author prompts and labels; validate on golden set
4) Add spot-check pipeline:
   - % of samples; stratify by domain/difficulty; store artifacts for audit
5) Version everything:
   - Prompts, judge model IDs, temperature, max tokens, datasets
6) Automate:
   - CI step to run eval on each change
   - Dashboard for trends and regressions
7) Production guardrails (optional):
   - AI judge pre/post filter; fallback strategies; sampling for ongoing QA

### 7.2 Judge Prompt Checklist

- Clear, single criterion per prompt or separated prompts per criterion
- Short discrete scales (3–5 levels) or binary labels
- Few-shot examples illustrating boundaries for each label
- JSON-only output with a fixed schema
- Instructions to ignore style/verbosity; avoid rewarding length
- Randomize A/B order; no provider/model hints
- Include “Tie” option for pairwise

### 7.3 Pass@k Evaluation Checklist

- Generate multiple samples per task (k ≥ 3 is common; more for diversity-heavy tasks)
- Hide tests; include property-based and randomized tests
- Sandbox runtime; enforce timeouts and memory limits
- Track compile errors separately from logic failures
- Report pass@1, pass@k, and code diversity metrics

### 7.4 Similarity Evaluation Checklist

- Multi-reference when feasible; take max score across references
- Choose metric per task:
  - BLEU/ROUGE for formulaic outputs
  - Semantic similarity for paraphrase-rich outputs
- Calibrate metric thresholds with human judgments
- Cache and batch process; pre-tokenize consistently

### 7.5 Comparative Evaluation Checklist

- Define in/out-of-scope prompts; exclude correctness-critical queries
- Ensure anonymization and randomization
- Collect A/B/Tie; encourage Ties to reduce noise
- Use Bradley–Terry or TrueSkill; monitor prediction accuracy on holdout
- Actively schedule uncertain pairs; downsample saturated pairs
- Combine with absolute KPIs before deployment swaps

---

## 8) Common Pitfalls and How to Avoid Them

- Over-trusting lexical metrics: they reward overlap, not meaning
  - Mitigate: add semantic similarity and functional checks
- Using AI judges without calibration: can be inconsistent/bias-prone
  - Mitigate: golden set correlation, bias controls, versioning, spot human audits
- Criteria ambiguity: “faithfulness” means different things across tools
  - Mitigate: write your own rubric; avoid mixing vendor scores
- Ignoring cost/latency of judges:
  - Mitigate: asynchronous judging; cascades; spot-checking; small specialized judges
- Data contamination in benchmarks:
  - Mitigate: PPL scans; rotate benchmarks; add private/internal test sets
- Comparative evaluation misuse for factual questions:
  - Mitigate: gate by intent/type; use correctness checks instead
- Non-transitive preference loops:
  - Mitigate: diversified prompts; more matches; active sampling; report uncertainty
- Lack of reproducibility:
  - Mitigate: record model versions, prompts, seeds, hyperparams; freeze judges for longitudinal tracking

---

## 9) Code Patterns (Copy/Paste)

### 9.1 AI Judge Wrapper (generic, JSON-enforced)

```python
import json, time

def call_llm(prompt, system=None, model="your-judge", temperature=0.0):
    # Replace with your provider call; ensure low temperature, deterministic settings
    raise NotImplementedError

def judge(prompt_template, variables, schema_keys, max_retries=2):
    sys = "You are a strict evaluator. Reply with JSON only. If invalid, reformat."
    prompt = prompt_template.format(**variables)
    for _ in range(max_retries + 1):
        txt = call_llm(prompt, system=sys)
        try:
            data = json.loads(txt)
            if all(k in data for k in schema_keys):
                return data
        except Exception:
            time.sleep(0.2)
            # Optionally prepend: "Reformat to valid JSON with keys: {schema_keys}"
    return {"error": "invalid_output", "raw": txt}
```

### 9.2 Embedding Similarity Service (batched)

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingSimilarity:
    def __init__(self, model_name="sentence-transformers/all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def score_pairs(self, pairs):
        texts = [t for pair in pairs for t in pair]
        embs = self.model.encode(texts, normalize_embeddings=True, batch_size=64)
        scores = []
        for i in range(0, len(embs), 2):
            a, b = embs[i], embs[i+1]
            scores.append(float(np.dot(a, b)))
        return scores
```

### 9.3 Comparative Logging and Rating

```python
from collections import defaultdict

def to_matches_for_bt(records):
    # records: [{"model_a","model_b","winner", "weight"}]
    matches = []
    models = set()
    for r in records:
        a, b, w = r["model_a"], r["model_b"], r["winner"]
        wt = r.get("weight", 1.0)
        models.update([a,b])
        if w == a:
            matches.append((a,b,wt))
        elif w == b:
            matches.append((b,a,wt))
        # ignore ties here or split weight across both
    return matches, sorted(list(models))
```

---

## 10) Quick Reference Tables

### 10.1 Method Selection by Scenario

| Scenario | Primary Method | Secondary/Support |
|---|---|---|
| Code/text-to-SQL | Functional correctness (pass@k) | AI judge for style, readability |
| QA over documents (RAG) | AI judge (faithfulness, relevance) | Semantic similarity vs. references; spot human |
| Translation | Semantic similarity (BERTScore) | BLEU/ROUGE; AI judge for adequacy/fluency |
| Summarization | AI judge (coverage, factuality) | Semantic similarity; human spot-check |
| Product copy generation | AI judge (helpfulness, tone) | Pairwise preference; human spot-check |
| Model selection among many | Comparative evaluation | Golden correctness checks |
| Safety/toxicity screening | AI judge or classifier | Human audit for edge cases |

### 10.2 Judge Output Schemas

| Use | Schema |
|---|---|
| Pointwise quality | {"label":"BAD|OK|GOOD","rationale":"..."} |
| Faithfulness | {"faithful":"YES|NO","rationale":"..."} |
| Pairwise | {"choice":"A|B|TIE","rationale":"..."} |
| Numeric (discrete) | {"score": 1..5, "rationale":"..."} |

---

## 11) From Scores to Decisions

- Set acceptance gates:
  - Functional: must pass tests
  - Faithfulness: reject if NO; fallback or redact answer
  - Quality: require label ≥ OK on all criteria
- Promotion thresholds:
  - Deploy candidate if win probability vs incumbent ≥ X% (e.g., 55%) on core segments
  - Require minimum margin for higher-cost models (e.g., +3–5% win rate)
- Monitoring:
  - Track judge agreement with human audits over time
  - Watch drift: if judge version changes, re-baseline metrics
  - Alert on spikes in hallucinations/toxicity even if overall quality is stable

---

## 12) Minimal Glossary

- Functional correctness: executes and returns expected outputs under tests
- Exact match: binary equality with reference (format-aware variants allowed)
- Lexical similarity: n-gram overlap (BLEU/ROUGE)
- Semantic similarity: embedding-based closeness (cosine), BERTScore
- Perplexity: exp(cross entropy); lower is better predictability
- AI-as-judge: LLM evaluates outputs by rubric; subjective and prompt/model-dependent
- Comparative evaluation: pairwise preferences; ranked by Elo/Bradley–Terry/TrueSkill

---

Use this reference to assemble a pragmatic, auditable evaluation stack: exact where possible, semantic when wording varies, AI judges for nuanced criteria, and comparative ranking when you must choose among many. Combine methods, calibrate with golden sets, and version every evaluator artifact.