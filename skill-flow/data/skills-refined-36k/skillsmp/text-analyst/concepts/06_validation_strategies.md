# Validation Strategies for Text Analysis

## Overview

Computational text analysis produces outputs—topic labels, sentiment scores, classifications—but these are not automatically valid. Validation establishes that outputs measure what they claim to measure and that findings are robust to analytical choices.

## Why Validation Matters

**Text analysis is not self-validating.**

- Topic models find patterns, but patterns may be artifacts
- Classifiers achieve accuracy, but may learn shortcuts
- Dictionaries count words, but words have multiple meanings

Without validation, you have numbers without meaning.

## Types of Validity

### Construct Validity

**Question:** Does this measure capture the intended concept?

**For topic models:** Do topics represent coherent themes?
**For classifiers:** Do categories match conceptual definitions?
**For dictionaries:** Do word matches reflect the concept?

### Content Validity

**Question:** Does the measure cover the full scope of the concept?

**For topic models:** Are important themes missing?
**For classifiers:** Are category boundaries appropriate?
**For dictionaries:** Are relevant words included?

### Criterion Validity

**Question:** Does the measure correlate with related measures?

**Concurrent:** Correlation with alternative measure of same thing
**Predictive:** Predicts expected outcomes

### Face Validity

**Question:** Does it look right to experts?

Necessary but not sufficient. Easy to satisfy but doesn't guarantee validity.

## Validation for Topic Models

### Human Validation Methods

#### 1. Word Intrusion Test

**Procedure:**
1. For each topic, show top 5-6 words
2. Add one "intruder" word from another topic
3. Ask humans to identify the intruder
4. Accuracy indicates topic coherence

**Example:**
```
Topic: economy, tax, budget, spending, growth, [intruder: military]
```

High agreement → Topics are interpretable

#### 2. Topic Intrusion Test

**Procedure:**
1. Show a document
2. Show 3 topics with high probability for that document
3. Add 1 "intruder" topic with low probability
4. Ask humans to identify the intruder

Tests whether topic assignments match human intuition.

#### 3. Topic Labeling Agreement

**Procedure:**
1. Show multiple coders the top words
2. Ask each to propose a label
3. Assess agreement

High agreement → Topics are interpretable
Disagreement → Topics may be incoherent

#### 4. Document Reading

**Procedure:**
1. For each topic, sample 5-10 high-probability documents
2. Read documents
3. Assess: Does the topic label fit?
4. Note false positives (label doesn't fit)

**Documentation:**
```markdown
Topic 3: "Economic Policy"
- Doc 142 (p=0.85): Yes, discusses tax reform
- Doc 287 (p=0.72): Partially, mixes health and economics
- Doc 391 (p=0.68): Yes, budget allocation
- Doc 512 (p=0.61): No, primarily foreign policy
Fit rate: 3/4 = 75%
```

### Computational Validation

#### Coherence Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **C_V** | Sliding window + word vectors | Higher is better; > 0.5 often good |
| **UMass** | Pairwise document co-occurrence | Less negative is better |
| **NPMI** | Normalized PMI | Higher is better |

**Important:** Coherence is necessary but not sufficient. High coherence doesn't guarantee meaningful topics.

#### Exclusivity (STM)

Measures whether top words are unique to each topic.

High exclusivity → Topics capture distinct concepts
Low exclusivity → Topics share vocabulary (may still be valid)

#### Held-Out Likelihood

**Procedure:**
1. Hold out subset of documents
2. Train model on training set
3. Evaluate likelihood on held-out set

Lower perplexity → Better generalization

### Robustness Checks

#### Sensitivity to K

**Procedure:**
1. Run models at K-5, K, K+5, K+10
2. Track: Do similar topics emerge across K?
3. Do topics split or merge sensibly?

**Interpretation:**
- Core topics should persist
- Small K: Topics merge logically
- Large K: Topics split into subtopics

#### Sensitivity to Preprocessing

**Procedure:**
1. Vary preprocessing (stemming, stopwords, thresholds)
2. Rerun models
3. Compare topic composition

#### Sensitivity to Random Seed

**Procedure:**
1. Run model with multiple seeds
2. Align topics across runs
3. Assess stability

**Methods for alignment:**
- Hungarian algorithm on topic-word similarity
- Manual inspection of top words

## Validation for Classification

### Training Data Validation

#### Label Quality

**Check:**
- Clear category definitions
- Consistent application
- Edge case documentation

**Inter-rater reliability:**
- Cohen's Kappa (2 raters)
- Fleiss' Kappa (3+ raters)
- Target: Kappa > 0.7

**Procedure:**
1. Have 2+ coders label same sample
2. Calculate agreement
3. Resolve disagreements, refine codebook

### Model Validation

#### Hold-Out Test Set

**Critical:** Never use test set for model selection.

```
Data Split:
- Training (60%): Fit models
- Validation (20%): Tune hyperparameters
- Test (20%): Final evaluation
```

#### Cross-Validation

**Procedure:**
1. Split data into K folds
2. Train on K-1, evaluate on 1
3. Repeat K times
4. Report mean ± SD

**Best practice:** Stratified K-fold to maintain class proportions.

### Error Analysis

**Systematic error analysis:**

1. **Sample misclassified documents**
2. **Categorize errors:**
   - Label noise (gold label wrong)
   - Ambiguous (genuinely unclear)
   - Model limitation (learnable but missed)
3. **Look for patterns:**
   - Certain terms misleading?
   - Certain document types harder?

**Document errors:**
```markdown
## Error Analysis

### Systematic Errors
- 15% of finance articles misclassified as business
  - Overlapping vocabulary
  - Consider merging or refining boundary

### Random Errors
- Unusual cases without pattern
- Acceptable if infrequent
```

### Robustness Checks

- Different model architectures
- Different feature representations
- Different train/test splits
- Subset analysis (by source, time)

## Validation for Dictionary Methods

### Coverage Assessment

**Question:** What proportion of documents have matches?

**Red flags:**
- < 30% coverage → Measure may be too sparse
- Very high frequency terms → May be noise

**Report:**
```markdown
Dictionary matched terms in 78% of documents.
Mean matches per document: 4.2 (SD = 2.8)
Range: 0-23 matches
```

### KWIC Validation

**Keyword-in-context (KWIC) review:**

1. For each key dictionary term, extract sample uses
2. Assess: Is this the intended meaning?
3. Calculate validity rate

**Example:**
```markdown
Term: "positive"

Matches reviewed: 50
- Valid uses (attitude/sentiment): 32 (64%)
- Invalid uses (medical, math): 18 (36%)

Action: Consider removing or using negation list
```

### Convergent Validity

**Procedure:**
1. Calculate dictionary score
2. Calculate alternative measure (ML sentiment, human coding)
3. Correlate

**Interpretation:**
- High correlation → Dictionary captures concept
- Low correlation → May be measuring something different

### Known Groups Validation

**Procedure:**
1. Identify groups expected to differ
2. Apply dictionary
3. Assess: Do they differ as expected?

**Example:** Sentiment should be:
- Higher in positive product reviews
- Lower in negative product reviews
- Intermediate in neutral reviews

## General Robustness Framework

### What to Vary

| Element | Variations |
|---------|------------|
| **Preprocessing** | Stemming, stopwords, thresholds |
| **Model parameters** | K, hyperparameters, architecture |
| **Random seed** | Multiple seeds |
| **Data subset** | By time, source, type |
| **Method** | Alternative approach entirely |

### Interpreting Robustness

**Robust findings:**
- Persist across variations
- Direction consistent, magnitude similar
- Core patterns stable

**Non-robust findings:**
- Change substantially with small changes
- Reverse direction
- Appear only with specific choices

**Reporting:**
```markdown
Main findings were robust to alternative specifications.
Results were consistent across K = 15, 20, 25
(see Appendix Table A1). Findings persisted when
using alternative preprocessing (with/without stemming).
```

## Reporting Validation

### Methods Section

```markdown
## Validation

### [Topic Model / Classifier / Dictionary] Validation

We validated results using [methods].

**Human validation:** N coders evaluated [what].
Agreement was [metric] = [value].

**Computational diagnostics:** [Metrics and values].

**Robustness:** We tested sensitivity to [variations].
[Key findings about robustness].
```

### Validation Table

| Validation Type | Method | Result | Assessment |
|-----------------|--------|--------|------------|
| Human - coherence | Word intrusion | 82% accuracy | Good |
| Human - labeling | Document reading | 78% fit | Acceptable |
| Computational | C_V coherence | 0.52 | Adequate |
| Robustness - K | K ± 5 | Core topics persist | Robust |
| Robustness - seed | 5 seeds | 90% alignment | Stable |

### Limitations Section

**Always acknowledge:**
- What validation was NOT done
- Limitations of validation performed
- Caveats for interpretation

## Validation Checklist

### Minimum Validation (Required)

- [ ] Coverage/match statistics reported
- [ ] Sample of outputs manually reviewed
- [ ] Basic robustness check (one variation)
- [ ] Limitations acknowledged

### Strong Validation

- [ ] Systematic human validation (multiple coders)
- [ ] Inter-rater reliability calculated
- [ ] Multiple robustness checks
- [ ] Coherence/accuracy metrics reported
- [ ] Error analysis conducted

### Exemplary Validation

- [ ] Convergent validity with alternative measure
- [ ] Known groups or predictive validity
- [ ] Extensive robustness analysis
- [ ] Validation fully documented and reproducible
- [ ] Pre-registration of validation plan

## Common Validation Failures

### 1. No Human Validation

**Problem:** Only computational metrics reported.

**Why it matters:** Coherence ≠ meaningfulness. Topics can be statistically coherent but substantively incoherent.

### 2. Validation on Training Data

**Problem:** Classifier evaluated on data used for training.

**Why it matters:** Inflated performance; doesn't generalize.

### 3. Single Seed

**Problem:** One random seed, no stability check.

**Why it matters:** Results may be artifacts of randomness.

### 4. No Robustness to K

**Problem:** Single K value, no sensitivity analysis.

**Why it matters:** Different K can produce different interpretations.

### 5. Ignoring Coverage

**Problem:** Dictionary applied without checking match rates.

**Why it matters:** Low coverage means sparse, potentially biased measurement.
