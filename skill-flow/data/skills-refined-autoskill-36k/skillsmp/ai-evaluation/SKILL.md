---
name: ai-evaluation
description: Systematic evaluation (evals) for LLM and AI products. Design test cases, measure accuracy/quality, track regressions, benchmark models, and build continuous evaluation pipelines. Distinct from traditional software testing with probabilistic outputs.
---

# AI Evaluation (Evals)

Build systematic evaluation frameworks for AI/LLM products to measure quality, catch regressions, and improve model performance.

## When to Use

- Building product with LLM/AI components
- Need to measure AI output quality systematically
- Comparing models or prompts (A/B testing)
- Detecting regressions before deployment
- Benchmarking against competitors
- Improving AI accuracy over time
- Explaining AI decisions to stakeholders

## Core Concept

**AI Evaluation (Evals) ≠ Traditional Testing**

Traditional software: Deterministic (same input → same output)
AI/LLM systems: Probabilistic (same input → variable outputs)

**Why Evals Are Hard:**
- Outputs are subjective (is this "good" writing?)
- No single right answer (multiple valid responses)
- Edge cases are infinite (can't test everything)
- Models change behavior with updates

**Solution:** Build eval suites that:
1. Define quality metrics (what is "good"?)
2. Create representative test cases
3. Measure systematically (automated + human)
4. Track over time (catch regressions)

---

## Workflow

### Step 1: Define What You're Evaluating

```markdown
## AI Component Taxonomy

**CLASSIFICATION TASKS:**
- Sentiment analysis (positive/negative/neutral)
- Content moderation (safe/unsafe)
- Intent detection (user wants X)
- Entity recognition (extract names, dates)

Eval approach: Accuracy, precision, recall, F1 score

---

**GENERATION TASKS:**
- Text generation (summaries, responses, creative writing)
- Code generation (functions, scripts)
- Recommendations (suggest items, next actions)
- Translations (language → language)

Eval approach: Quality scores, human preference, task success rate

---

**RETRIEVAL TASKS:**
- Search (find relevant documents)
- Recommendation (rank items by relevance)
- Question answering (retrieve + synthesize answer)

Eval approach: Relevance, ranking quality (NDCG, MRR)

---

**REASONING TASKS:**
- Multi-step problem solving
- Complex decision making
- Causal inference

Eval approach: Correctness, reasoning quality, step-by-step validation
```

---

### Step 2: Build Your Eval Dataset

**Golden Dataset:** Curated examples with known correct outputs.

```markdown
## Dataset Creation Framework

**SIZE REQUIREMENTS:**
- Minimum: 50-100 examples (manual review feasible)
- Good: 500-1000 examples (covers edge cases)
- Production: 5,000-10,000+ examples (statistical significance)

**COMPOSITION:**
1. **Happy Path (40%)** - Typical, well-formed inputs
2. **Edge Cases (30%)** - Unusual but valid inputs
3. **Adversarial (20%)** - Deliberately tricky inputs
4. **Failure Cases (10%)** - Invalid inputs (test error handling)

**EXAMPLE (Book Recommendation AI):**

Happy Path:
- "Recommend books like Harry Potter for my 10-year-old"
- "My kid loved Percy Jackson, what's next?"

Edge Cases:
- "Books for advanced reader (7yo but reads at 5th grade level)"
- "Fantasy but NO violence or romance"

Adversarial:
- "Best books" (too vague)
- "Books about [topic that doesn't exist for kids]"

Failure Cases:
- Gibberish input
- Adult content request

**SOURCES FOR TEST CASES:**
1. **User Logs** - Real queries (anonymized)
2. **Team Brainstorm** - Manual generation
3. **Synthetic** - GPT-4 to generate test cases
4. **Competitor Comparison** - Test against their outputs
5. **Bug Reports** - Historical failures
```

---

### Step 3: Define Evaluation Metrics

**Quantitative Metrics:**

```markdown
## Metric Types

### ACCURACY METRICS (Classification)
- **Accuracy:** (Correct predictions) / (Total)
- **Precision:** (True Positives) / (True Positives + False Positives)
- **Recall:** (True Positives) / (True Positives + False Negatives)
- **F1 Score:** Harmonic mean of precision and recall

Use when: Clear right/wrong answer (classification, extraction)

---

### QUALITY METRICS (Generation)
- **Coherence:** Does output make sense? (1-5 scale)
- **Relevance:** Does output answer the question? (1-5 scale)
- **Helpfulness:** Is output useful to user? (1-5 scale)
- **Safety:** Is output safe/appropriate? (pass/fail)
- **Hallucination Rate:** % of outputs with false information

Use when: Subjective quality assessment needed

---

### TASK SUCCESS METRICS
- **Completion Rate:** % of tasks successfully completed
- **User Satisfaction:** Thumbs up/down, NPS
- **Time to Success:** How long to achieve goal
- **Retry Rate:** % of users who re-prompt after first response

Use when: Evaluating end-to-end task performance

---

### RANKING METRICS (Retrieval/Recommendation)
- **MRR (Mean Reciprocal Rank):** Average of 1/rank of first relevant result
- **NDCG (Normalized Discounted Cumulative Gain):** Quality of ranking
- **Precision@K:** % of top K results that are relevant

Use when: Evaluating search or recommendation quality
```

**Qualitative Metrics:**

```markdown
## Human Evaluation

**PAIRWISE COMPARISON:**
Show human raters two outputs (A vs B), ask "Which is better?"
- Advantage: Easier than absolute rating
- Disadvantage: Slower, requires more comparisons

**LIKERT SCALE RATING:**
Rate outputs 1-5 on dimensions (coherence, helpfulness, safety)
- Advantage: Fast, can aggregate scores
- Disadvantage: Subjective, rater disagreement

**TASK COMPLETION:**
Can human complete task using AI output?
- Advantage: Measures real utility
- Disadvantage: Slow, expensive

**RED TEAM REVIEW:**
Experts try to find failures (adversarial testing)
- Advantage: Finds edge cases
- Disadvantage: Not systematic
```

---

### Step 4: Automated Evaluation Strategies

**Use LLM as Judge:**

```markdown
## LLM-as-Evaluator Pattern

**CONCEPT:** Use GPT-4 (or strong model) to evaluate outputs from your AI.

**PROMPT TEMPLATE:**
"You are an expert evaluator. Rate the following AI response on:
1. Relevance (1-5)
2. Accuracy (1-5)
3. Helpfulness (1-5)

User query: {query}
AI response: {response}
Ground truth (if available): {truth}

Provide ratings and brief explanation."

**ADVANTAGES:**
✅ Scalable (can eval thousands of examples)
✅ Consistent (same rubric every time)
✅ Fast (seconds per eval)
✅ Cheap (pennies per eval)

**DISADVANTAGES:**
❌ Not 100% reliable (LLM judge can be wrong)
❌ Requires validation (compare to human ratings)
❌ Can miss nuanced failures

**VALIDATION:**
- Run LLM judge on 100-200 examples
- Have humans also rate same examples
- Calculate inter-rater agreement (Cohen's kappa)
- If agreement >70%, LLM judge is trustworthy
```

---

### Step 5: Build Eval Pipeline

**Continuous Evaluation System:**

```markdown
## Eval Pipeline Architecture

**COMPONENTS:**

1. **Test Suite Storage**
   - JSON/CSV of test cases
   - Version controlled (git)
   - Tagged by category (happy path, edge case, etc.)

2. **Runner Script**
   - Iterate through test cases
   - Call AI system with each input
   - Collect outputs
   - Log latency, cost, errors

3. **Scorer**
   - Compare output to expected (if available)
   - Run automated metrics (accuracy, ROUGE, BLEU, etc.)
   - Call LLM judge for quality rating
   - Aggregate scores

4. **Regression Detection**
   - Compare current run to baseline
   - Flag significant drops (e.g., accuracy down >5%)
   - Alert team if regression detected

5. **Reporting Dashboard**
   - Visualize metrics over time
   - Drill down into failures
   - Compare models/prompts side-by-side

**FREQUENCY:**
- Pre-deploy: Every code/prompt change
- Nightly: Full suite run on production
- Weekly: Human review of sample outputs
```

---

### Step 6: Common Eval Patterns

```markdown
## Evaluation Strategies by Use Case

### RECOMMENDATION SYSTEMS
**Test:** Does user engage with recommendation?

Metrics:
- Click-through rate (CTR)
- Conversion rate (purchase, complete)
- Time spent with recommended item
- Diversity (not all same type)

Golden Dataset:
- Historical user behavior (X user liked Y, did they like Z?)
- Synthetic: "If user likes [A, B, C], recommend [D]?"

---

### CONTENT MODERATION
**Test:** Does it correctly flag unsafe content?

Metrics:
- Precision (flagged = actually unsafe)
- Recall (actually unsafe = flagged)
- False positive rate (safe content flagged)

Golden Dataset:
- Curated examples of safe/unsafe content
- Edge cases (satire, context-dependent)

---

### SUMMARIZATION
**Test:** Does summary capture key points?

Metrics:
- ROUGE score (overlap with reference summary)
- Factual consistency (no hallucinations)
- Compression ratio (length of summary / original)

Golden Dataset:
- Documents with human-written summaries
- Check: All key facts present, no false info

---

### CODE GENERATION
**Test:** Does generated code work?

Metrics:
- Syntax correctness (parses without errors)
- Functional correctness (passes unit tests)
- Code quality (readable, efficient)

Golden Dataset:
- Programming problems with test cases
- Example: "Write function that reverses string" + 10 test cases

---

### CONVERSATIONAL AI
**Test:** Does it handle multi-turn conversation well?

Metrics:
- Coherence across turns
- Context retention (remembers earlier messages)
- Task completion rate (user achieves goal)
- Safety (doesn't generate harmful content)

Golden Dataset:
- Scripted conversations with expected paths
- User logs (real conversations, anonymized)
```

---

### Step 7: A/B Testing for AI

**Compare models, prompts, or configurations:**

```markdown
## AI A/B Testing Framework

**SETUP:**
1. Define variants (Model A vs. Model B, or Prompt v1 vs. v2)
2. Random assignment (50/50 split)
3. Define success metric (accuracy, user satisfaction, task completion)
4. Minimum sample size (depends on expected effect size)

**METRICS TO TRACK:**
- Primary: Quality (accuracy, preference, satisfaction)
- Secondary: Latency, cost, error rate
- Guardrails: Safety violations, user complaints

**STATISTICAL SIGNIFICANCE:**
- Run until p < 0.05 (95% confidence)
- Typically need 1,000-10,000 samples depending on effect size
- Use tools: Optimizely, LaunchDarkly, or custom

**COMMON TESTS:**
- Model comparison: GPT-4 vs. Claude vs. Gemini
- Prompt engineering: Version A vs. B
- Temperature: 0.7 vs. 0.9 (creativity vs. consistency)
- Context window: Include X vs. Y tokens of context

**EXAMPLE:**
Variant A: GPT-4 with prompt v1
Variant B: GPT-4 with prompt v2

Metric: User thumbs up rate
- A: 70% thumbs up (n=500)
- B: 75% thumbs up (n=500)
- Result: B wins, p=0.03 (significant)
→ Ship prompt v2
```

---

## Common Eval Mistakes

```markdown
## Anti-Patterns

❌ **No Golden Dataset**
Testing AI without reference examples
→ Fix: Curate 100+ examples with expected outputs

❌ **Testing Only Happy Path**
Ignoring edge cases and adversarial inputs
→ Fix: 30% of dataset should be edge cases

❌ **Manual Eval Only**
Reviewing outputs one-by-one (doesn't scale)
→ Fix: Automate with LLM judge + spot-check humans

❌ **No Regression Detection**
Shipping changes without comparing to baseline
→ Fix: Track metrics over time, alert on drops

❌ **Vanity Metrics**
Measuring things that don't correlate with user value
→ Fix: Eval what matters (task success, user satisfaction)

❌ **Overfitting to Eval Set**
Optimizing prompts specifically for test cases
→ Fix: Hold out test set, regularly refresh with new examples
```

---

## Eval Tooling

**Open Source:**
- **LangSmith** (LangChain) - Eval framework for LLM apps
- **Prompt flow** (Microsoft) - End-to-end eval pipeline
- **Weights & Biases** - Experiment tracking
- **Ragas** - RAG evaluation framework

**Commercial:**
- **Anthropic Console** - Claude model evals
- **OpenAI Evals** - GPT model testing
- **HumanSignal** - Human annotation platform

---

## Related Skills

- `/building-with-llms` - Best practices for AI product development
- `/ai-product-strategy` - Strategic AI product decisions
- `/testing-strategies` - Traditional software testing
- `/performance-optimization` - Optimize AI latency/cost

---

**Last Updated**: 2026-01-22
