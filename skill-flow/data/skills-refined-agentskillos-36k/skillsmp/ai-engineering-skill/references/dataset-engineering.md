# Dataset Engineering — Practitioner Reference

Purpose: Build, verify, and maintain high-quality datasets for pretraining/finetuning with minimal waste and maximal model impact.

Use this when:
- You need to assemble or improve a finetuning dataset fast
- You’re deciding between real vs synthetic data, PEFT vs full finetuning
- You need concrete pipelines, checks, and prompts for data creation/verification


## Quickstart Checklist

- Define the task and data format
  - Supervised finetuning: (instruction, response)
  - Preference finetuning: (instruction, winning_resp, losing_resp) or ((inst, resp), score)
  - Tool use: multi-message, with action and user messages
- Scope the data targets
  - Quality: relevant, aligned, consistent, formatted, unique, compliant
  - Coverage: domains, tasks, languages, length, turns, difficulty, formats
  - Quantity: estimate via small-scale curve (25/50/100% subsets)
- Source/Generate data
  - Application telemetry, public datasets, purchased data
  - Annotate with clear guidelines
  - Synthesize (rule-based, simulation, AI-powered); verify quality
- Process
  - Inspect; deduplicate; clean; filter; format (tokenizer/chat template)
- Verify quality
  - Functional checks (exec/tests), AI judge, back-translation, heuristics
- Split, log lineage, and version
  - Prevent contamination; record sources, licenses, and filters
- Iterate using evaluation-driven development


## Decision Frameworks

### Finetuning Approach vs Data Availability

| Situation | Recommended approach | Rationale |
|---|---|---|
| 50–100 examples | PEFT (e.g., LoRA) on a strong base model | Strong base closes gap; small data adapts efficiently |
| 1K–50K examples | PEFT or partial finetune | Balanced compute; faster iteration |
| 50K–1M+ examples | Full finetuning (smaller model) | Full FT scales with more data; avoid ossification risk |
| Limited domain data but large adjacent data | Stage FT: pre-adapt on adjacent (self-supervised), then domain SFT | Reduces high-quality data required |
| Big domain gap to target | Use larger base model and targeted synthetic generation | Model capability matters when data is scarce |

Notes:
- With very small data, advanced models finetune best; with very large data, performance across base models converges.
- Ossification risk: smaller models adapt worse to new data than larger models; consider training-from-scratch only at extreme scale.

### Dataset Composition (Coverage) Strategy

- Default: mirror production usage distribution (topics, languages, formats)
- Optimize: run small-model scaling experiments across candidate mixes; pick best projected large-model mix
- Ensure diversity axes (examples):
  - Tasks: summarization, Q&A, extraction, coding, math, tool use
  - Topics: domain taxonomy relevant to users
  - Languages/Code: target locales, code languages
  - Lengths: short/long contexts and outputs
  - Turns: single vs multi-turn
  - Difficulty: routine to edge cases/adversarial

### Synthetic Data Use

| Goal | Best practice |
|---|---|
| Increase quantity | AI synthesis with robust verification; mix with real data to avoid model collapse |
| Fill coverage gaps | Generate targeted cases (rare events, formats, adversarial) |
| High consistency (e.g., preference) | AI judge with double evaluation and bias controls |
| Tool use | Simulate APIs/tools and verify plans/outcomes |
| Sensitive domains | Use synthetic to avoid PII/PHI; maintain lineage and policies |
| Long context adaptation | Chunk long docs, generate Q/A from chunks, supervise with full doc contexts |

Avoid:
- Training purely on synthetic outputs of the same model without verification
- Unknown lineage synthetic sources (copyright, contamination risk)


## Data Curation: What “High Quality” Means

Quality attributes and how to check:

| Attribute | Definition | Checks/Tools |
|---|---|---|
| Relevant | Matches the target task/use distribution | Topic/language classification; production telemetry; filter irrelevant |
| Aligned | Exhibits required behavior (factuality, format, style) | AI checker prompt for policy compliance; test on representative eval |
| Consistent | Annotation agreement/stability | Inter-annotator agreement; calibrate with guideline exemplars |
| Correctly formatted | Matches tokenizer/chat template; no extraneous tokens | Schema validators; whitespace/HTML stripping; tokenization tests |
| Unique (sufficiently) | No harmful duplication | MinHash/LSH/embedding dedup; define granularities (doc/para/sent) |
| Compliant | Legal/policy-safe (PII, copyright, safety) | PII scrubbers; safety/toxicity filters; license scanning |

Tip: Define pass/fail rules per attribute; attach reasons to rejected items for feedback to annotators/generators.


## Data Quantity Planning

- Start small and plot performance vs size:
  - Train on 25%, 50%, 100% subsets; fit diminishing-returns curve
  - If curve is flat early, revisit quality/format/hyperparams
- Budgeting:
  - If budget = $10k and $2/sample, max 5,000 labeled samples
  - Trade off: more data vs compute; prioritize quality filtering early to avoid wasted tokens
- Task complexity and base model distance strongly affect required data size


## Data Acquisition and Annotation

### Sources

- Your application data (ideal for relevance): user queries, contexts, feedback, outcomes
- Public repositories: Hugging Face, Kaggle, gov open data, ICPSR, UCI, OpenML, AWS Open Data
- Evaluation harness datasets (e.g., lm-eval) for PEFT-scale SFT
- Purchased/proprietary data providers

Always:
- Check licenses and origins; document lineage and restrictions
- Inspect for contamination risk with your eval/benchmarks

### Annotation Guidelines Best Practices

- Define: task, required behaviors, format, constraints, scoring rubric
- Provide many positive/negative examples with justifications
- Clarify edge cases; include “what not to do”
- Calibration:
  - Pilot a batch; compute inter-annotator agreement
  - Revise guidelines; re-train annotators; re-run pilot
- Ongoing QC:
  - Seed gold items; rater drift monitoring; fatigue heuristics (e.g., quality drops later in session)

Template (excerpt):

```yaml
task: "Summarization with factual consistency"
constraints:
  - "<= 120 words"
  - "No external facts beyond source"
  - "Include key entities: {entities}"
scoring:
  5: "Complete, concise, fully factual"
  4: "Minor omissions; factual"
  3: "Partial; or minor factual issues"
  2: "Major omissions or style violations"
  1: "Factual errors or off-topic"
negatives:
  - "Adding speculative claims"
  - "Copying long spans verbatim"
```

### Data Flywheel Design

- Capture: permissioned logs, user thumbs/ratings, corrective edits
- Label: lightweight rater UIs; AI-assisted prelabels; selective human review
- Close loop: deploy improvements measured on user-centric evals
- Governance: consent, privacy, retention, right-to-be-forgotten


## Data Synthesis and Augmentation

### Rule-Based/Procedural Generation

- Templates for structured docs (invoices, resumes, configs)
- Linguistic swaps (synonyms, gender/role inversions) to reduce bias
- Perturbations:
  - Vision: rotations, crops, brightness/contrast, noise
  - Text: token masking/replacement; controlled paraphrase

Example: Transaction template (for fraud/sim data)

```json
{
  "transaction_id": "uuid4()",
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS",
  "amount": "float(0.50-3000.00)",
  "merchant_name": "faker.company()",
  "merchant_category": "MCC-####",
  "location": {"city": "...", "state": "...", "country": "..."},
  "payment_method": "['credit_card','debit_card','online','cash']",
  "status": "['completed','pending','failed']",
  "description": "faker.sentence()"
}
```

Bias-mitigating augmentation examples:

| Original | Augmented |
|---|---|
| She’s a fantastic nurse. | He’s a fantastic nurse. |
| The CEO, Mr. Alex Wang… | The CEO, Ms. Alexa Wang… |
| Emily has always loved the violin. | Mohammed has always loved the violin. |

### Simulation

- Robotics/self-driving: safer rare-event generation; domain randomization
- Tool use: simulate APIs and verify plans/results
- Finance/manufacturing/climate: synthetic rare outcomes for robust training

### AI-Powered Synthesis Patterns

- Paraphrase and translation:
  - Expand instructions; generate multi-lingual datasets
  - Back-translation for quality check
- Code/data translation:
  - Cross-language code; explainers↔code back-translation fidelity
- Self-play/agent simulations:
  - Negotiation, customer support; generate multi-turn transcripts
- Long context:
  - Chunk > generate chunk QA > supervise with full-long-context

Back-translation quality checker (sketch):

```python
def backtranslate_check(src_text, src_lang="en", tgt_lang="lo", model):
  tgt = model.translate(src_text, src_lang, tgt_lang)
  back = model.translate(tgt, tgt_lang, src_lang)
  return similarity(src_text, back)  # e.g., BLEU/chrF or embedding sim
```

### Instruction Data Synthesis Pipelines

Seed-driven (Alpaca-style):
1. Seed set of diverse seed (instruction, response) exemplars
2. Prompt a strong model to generate more pairs mirroring seed diversity
3. Filter and format; verify with AI judge and heuristics

Reverse-instruction (generate prompts from real content):
1. Collect high-quality outputs (articles, stories, code, wiki)
2. Use AI to generate instructions that would elicit those outputs
3. Pair with the real outputs; verify prompt-output alignment
4. Iterate: bootstrap model quality with improved reverse-instruct data

Llama-style code dataset synthesis:
1. Generate diverse programming problems
2. Generate multi-language solutions with CoT rules-of-thumb included
3. Auto-generate unit tests
4. Parse/lint/execute; on failure, prompt model to self-repair
5. Translate code across languages; require tests pass post-translation
6. Generate explanations/docs; back-translate via code->doc->code fidelity

Preference data (AI judge double-pass):
- Ask judge twice with swapped candidate order; accept only consistent winners
- Calibrate judge prompt to project’s style/safety constraints


## Data Verification and Filtering

Verification methods by type:

| Type | Examples | Automation |
|---|---|---|
| Functional correctness | Code execution, unit tests, type/format validators | High |
| AI judge | Scoring or binary accept/reject by rubric | Medium-high |
| Back-translation | Cross-language or code↔doc fidelity | Medium |
| Adversarial detection | Toxicity, bias triggers, jailbreaks | Medium |
| Statistical/Heuristics | Length bounds, duplicate patterns, keyword filters | High |
| Classifier-based | AI-generated detector, topic filter, anomaly detection | Medium |

AI judge prompt template:

```text
You are a strict data quality reviewer for instruction-tuning data.

Task requirements:
- Factual accuracy relative to provided context (if any)
- Output format: JSON with keys { ... } (no extra text)
- Style: concise, no hedging or disclaimers

Given:
INSTRUCTION:
...
RESPONSE:
...

Score 1-5 and explain briefly. Then output: {"accept": true|false, "score": N, "issues": ["..."]}

Reject if: hallucinations, format violations, missing required fields, or style violations.
```

Factuality filter options:
- Retrieval-augmented facts checks (exact/ref-based)
- Entity consistency checks
- Numeric and unit normalization/validation

Heuristic filters (examples):
- Remove empty/too short/too long responses for task
- Deduplicate (exact/fuzzy/semantic)
- Remove repeated output = input
- Remove mismatched instruction-response pairs
- Discard late-session annotations if quality systematically degrades


## Limitations and Risk Controls for Synthetic Data

- Quality: Verify with multiple methods; measure model deltas on held-out real evals
- Superficial imitation: Avoid training only on teacher outputs for hard reasoning; include true reasoning traces or easier subproblems
- Model collapse: Mix synthetic with real; refresh real data each iteration
- Bias amplification: Monitor feedback loops; diversify seeds and judges
- Lineage obscurity: Track generators, versions, prompts; avoid black-box teacher outputs when licensing prohibits; prevent eval contamination


## Model Distillation

When to use:
- Need a smaller/cheaper model with similar behavior to a larger one
- Have budget to collect high-quality synthetic supervision (teacher outputs)
- Licensing permits using teacher outputs for training

Approaches:
- Supervised distillation: teacher-generated (instruction, response) pairs
- Preference distillation: teacher rankings/scores; train reward model or DPO-style
- Adapter-based: LoRA adapters trained on synthetic pairs for speed/cost

Cautions:
- Licensing restrictions on using outputs to train other models
- Don’t rely solely on teacher-style imitation for reasoning improvements
- Verify on real evaluations; avoid evaluation datasets seen by teacher


## Data Processing Pipelines

### Inspect

- Data origin, preprocessing history, and license
- Token distributions, input/output lengths, topics, languages
- Special tokens; whitespace/HTML noise
- Multi-source discrepancies (by annotator/source/time)
- Conflicts and agreement metrics

Tip: 15 minutes of manual browsing often reveals high-impact issues.

### Deduplicate

Duplication types:
- Whole-doc, intra-doc (paragraphs), cross-doc (quotes/snippets), instruction duplicates with different responses

Methods:

| Method | Notes |
|---|---|
| Exact/n-gram/fuzzy matching | Straightforward but expensive at scale |
| Hashing (MinHash, Bloom filters) | Fast probabilistic dedup on shingles |
| Embeddings + ANN | Semantic duplicates; choose threshold carefully |
| Dimensionality reduction | Speedup for pairwise compare |

MinHash sketch (datasketch):

```python
from datasketch import MinHash, MinHashLSH
def shingles(s, k=5):
    return {s[i:i+k] for i in range(max(len(s)-k+1,1))}
def minhash(sig):
    m = MinHash(num_perm=128)
    for s in sig: m.update(s.encode('utf8'))
    return m

lsh = MinHashLSH(threshold=0.85, num_perm=128)
for i, text in enumerate(texts):
    m = minhash(shingles(text))
    if lsh.query(m):
        continue  # duplicate
    lsh.insert(f"id_{i}", m)
```

### Clean and Filter

- Remove extraneous formatting (HTML/Markdown) unless required
- PII removal per policy; sensitive field pruning
- Safety/toxicity filtering
- Low-quality removal via heuristics and AI judge
- Active selection (optional):
  - Uncertainty sampling; importance sampling; data pruning metrics
- Balance classes and difficulty (address class imbalance)

### Format

- Match model-specific tokenizer and chat template
- Normalize instruction schema (system, user, tool messages)
- Ensure consistent formatting tokens, casing, whitespace

Example: converting few-shot prompt to SFT dataset

Few-shot prompt:
```text
Label the following item as either edible or inedible.
Item: burger
Label: edible
Item: car
Label: inedible
Item: mushroom
Label: edible
Item: {INPUT}
Label:
```

Convert to SFT pairs:

```json
[
  {"instruction": "burger -->", "response": "edible"},
  {"instruction": "car -->", "response": "inedible"},
  {"instruction": "mushroom -->", "response": "edible"}
]
```

At inference post-SFT, prompt as simply:
```text
{INPUT} -->
```

Pitfalls:
- Mismatched chat templates or trailing spaces/newlines
- Mixing multiple incompatible formats in one dataset


## Tool Use and Multi-Message Data

- Represent multi-destination messages (e.g., to user and to tool)
- Include explicit termination markers and routing metadata

Example multi-message turn:

```json
{
  "messages": [
    {"role": "system", "content": "You are an assistant."},
    {"role": "user", "content": "Find the cheapest flight SFO->JFK next Friday."},
    {"role": "assistant", "to": "flight_api", "content": {"origin":"SFO","dest":"JFK","date":"2025-05-02"}},
    {"role": "tool", "from": "flight_api", "content": {"itineraries": [...]}},
    {"role": "assistant", "to": "user", "content": "Cheapest option is $212 on AirX at 7:20am. Book it?"}
  ],
  "end_turn": true
}
```

Dataset tips:
- Provide both action planning and user-facing narration
- Verify tool-calls via simulators or sandbox APIs
- Include recovery paths for errors/timeouts


## Long-Context Finetuning Pattern

Goal: Upgrade from 8K to 128K context capacity for comprehension tasks.

Procedure:
1. Select long documents (< target window length)
2. Chunk docs into <= base window (e.g., 6–8K)
3. Generate multiple (question, answer) per chunk (high quality)
4. Train with full long document as context and (question, answer) pairs referencing the chunk
5. Evaluate with retrieval-intensive questions crossing chunk boundaries

Notes:
- Use synthetic Q/A but verify factuality with context-aware judge
- Curriculum: start at shorter contexts, gradually extend


## Coverage Engineering

- Define axes and quotas:
  - Topics, tasks, languages, modalities, length buckets, turns, difficulty
- Sampling strategy:
  - Stratified sampling or fixed quotas per axis
  - Over-sample underrepresented strata
- Adversarial and rare classes:
  - Use synthesis to generate rare but high-impact patterns
- Balance over phases:
  - Pretrain: heavier math/code boost reasoning (anneal later)
  - SFT: reflect target user distribution more closely
  - Preference: approximate real preference distribution


## Preference Data (RM/DPO) Generation

- Format: (instruction, winning_response, losing_response) or ((inst, resp), score)
- AI judge generation:
  - Bias control: shuffle order; dual-pass consistency check
  - Calibrate judge for style/safety; use reference policies
- Safety preferences:
  - Create paired safe/unsafe outputs; judge must consistently prefer safe
- RM training hygiene:
  - Balance domains and lengths; robust to lexical diversity
  - Hold out a clean preference eval set


## Practical Prompts and Code Patterns

Instruction generator prompt:

```text
You are generating diverse, high-quality instructions for {domain} tasks.
Constraints:
- Output types: {["JSON","bulleted list","plain text answer","SQL"]} (vary)
- Difficulty: {easy/medium/hard} (mix)
- Length: max {N} words for expected answers
- Avoid ambiguous or unsolvable tasks.

Generate 10 distinct instructions with short descriptions of desired outputs.
Return JSON: [{"instruction": "...", "output_spec": "..."}]
```

Response generator prompt with CoT:

```text
Solve step by step with clear reasoning. If code is needed, include it.
Adhere strictly to the output_spec:
INSTRUCTION: ...
OUTPUT_SPEC: ...
```

AI judge double-pass:

```python
def judge_pair(inst, a, b, judge):
    j1 = judge.score(inst, a, b)  # returns 'A' or 'B'
    j2 = judge.score(inst, b, a)
    if j1 == 'A' and j2 == 'B': return 'A'
    if j1 == 'B' and j2 == 'A': return 'B'
    return None  # inconsistent -> discard
```

Unit test generator for code synthesis:

```text
Write 5 unit tests for the following function specification and candidate solution.
- Cover typical and edge cases
- Avoid flaky/platform-specific behavior
- Use pytest
SPEC:
...
CANDIDATE_CODE:
...
```

Toxicity injection for safety data:

```text
Generate 20 user prompts containing varying levels of toxic content (slurs, threats, harassment).
For each, produce:
- safe_response: de-escalating, policy-abiding
- unsafe_response: toxic or policy-violating
Return JSONL with fields: prompt, safe_response, unsafe_response, category.
```

Active selection with uncertainty (sketch):

```python
# model emits class probabilities; select high-entropy samples
entropy = -np.sum(p * np.log(p+1e-9), axis=1)
selected_idx = np.argsort(entropy)[-k:]
```


## Common Pitfalls and How to Avoid

- Mixing chat templates/tokenizers across sources
  - Enforce a single formatter; unit-test tokenization
- Over-duplication causing bias/contamination
  - Dedup early and at multiple granularities
- Over-reliance on synthetic without verification
  - Layer multiple verifiers; measure real-eval deltas
- Position bias in AI judges
  - Double-pass with order shuffling; discard inconsistencies
- “Helpful but unsolicited” behaviors in data
  - Remove bad behaviors; add counterexamples explicitly
- Long-tail undercoverage
  - Define coverage axes and quotas; deliberately synthesize rare strata
- Licensing/compliance gaps
  - Track lineage; automated license scanning; PII filtering; policy gates
- Annotation drift/fatigue
  - Short sessions; inter-rater calibration; QC sampling


## Evaluation-Driven Iteration

- Maintain a task-aligned eval suite (unit tests for behaviors)
- After each dataset change:
  - Train small model variant
  - Measure on eval suite and shadow production data
  - Log changes with dataset version, filters, judge versions
- Use performance-vs-size curves to decide whether to scale data or improve quality


## Reference Tables

### Training Phase Domain Mix (example from a strong general model)

| Domain | Pretraining | SFT | Preference |
|---|---:|---:|---:|
| General knowledge (EN) | 50% | 52.66% | 81.99% |
| Math & reasoning | 25% | 21.19% | 5.89% |
| Coding | 17% | 14.89% | 6.93% |
| Multilingual | 8% | 3.01% | 5.19% |
| Exam-like | – | 8.14% | – |
| Long context | – | 0.11% | – |

Use as a heuristic only; calibrate to your application.

### Synthesis Techniques Comparison

| Technique | Pros | Cons | Best for |
|---|---|---|---|
| Rule-based/templates | Fast, controllable, cheap | Limited realism/diversity | Structured docs, bias augmentation |
| Simulation | Safe rare events, tool realism | Sim-to-real gap, engineering cost | Robotics, self-driving, tool APIs |
| AI-powered | High diversity/quality potential | Verification required, lineage | Instruction SFT, code, multilingual |


## Minimal End-to-End SFT Dataset Pipeline (Example)

1. Define task and schema
   - Instruction, response; JSON or chat template; safety constraints
2. Collect seed data
   - App logs; public sets; 100–500 seed examples
3. Clean and dedup
   - Strip HTML/Markdown; PII filter; MinHash/embedding dedup
4. Synthesize to expand coverage
   - AI generate instructions/responses; reverse-instruction; long-context pattern
5. Verify and filter
   - AI judge double-pass; back-translation; heuristics; functional tests (if applicable)
6. Balance coverage
   - Quotas per task/topic/language/length/difficulty; sample to target mix
7. Format for model
   - Tokenizer; chat template; consistent system/user/assistant roles
8. Split and version
   - Train/val/test split; record lineage, filters, judge versions
9. Pilot finetune
   - PEFT/full per decision framework; hyperparam sweep
10. Evaluate and iterate
    - Measure on eval suite; update data mix/quality; repeat


## Example: Data Folder Structure and Metadata

```text
data/
  raw/
    source_a.jsonl
    source_b.jsonl
  processed/
    cleaned.jsonl
    deduped.jsonl
    verified.jsonl
  splits/
    train.jsonl
    val.jsonl
    test.jsonl
  meta/
    lineage.yaml
    license_report.txt
    filters_config.yaml
    judge_model@v3.2.prompt.txt
```

lineage.yaml:

```yaml
sources:
  - name: "AppLogs_2025Q1"
    license: "internal"
    pii: "removed"
    notes: "consented users only"
  - name: "HF:dataset_xyz"
    license: "apache-2.0"
    subset: "en"
filters:
  - "strip_html"
  - "toxicity<0.2"
  - "len_resp<=512"
verifiers:
  - "ai_judge_v3.2_double_pass"
  - "backtranslation_en<->es.sim>=0.80"
dedup:
  method: "MinHash128@0.85"
  granularity: "sentence"
```


## When to Stop Adding Data vs Improve Data

- Add more data if:
  - Performance curve still steep; no clear plateau
  - Coverage analysis shows large gaps
  - Model underfits tasks in eval suite

- Improve data quality if:
  - Diminishing returns evident
  - High reject rate from AI judge or many functional failures
  - Inconsistent annotations; format violations frequent

- Rebalance data mix if:
  - Overfitting to popular topics; regression on critical but rare cases
  - Preference-aligned behaviors off vs user feedback


## Glossary of Key Formats

- SFT example: (instruction, response)
- Preference example: (instruction, winning_response, losing_response)
- RM scoring: ((instruction, response), score)
- Tool use multi-message: role + to/from + content + termination markers


## Final Notes

- Data is the highest-leverage component; invest in guidelines, verification, lineage
- Prefer small, verified, diverse datasets over large, noisy ones
- Use synthetic aggressively but verify and mix with real data
- Keep everything versioned and reproducible; avoid eval contamination
- Iterate with evaluation-driven development; let measured impact guide what to do next