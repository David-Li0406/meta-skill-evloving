# Topic Models for Text Analysis

## Overview

Topic models are unsupervised methods that discover latent themes in document collections. Each topic is a probability distribution over words; each document is a mixture of topics.

## When to Use Topic Models

**Good fit:**
- Exploratory analysis: What themes exist in this corpus?
- Large collections where manual reading is infeasible
- Want to discover structure, not impose categories
- Need to track theme prevalence over time or groups

**Poor fit:**
- Confirmatory analysis (use dictionary or classification)
- Very short documents (< 50 words)
- Highly technical/formulaic text
- Need precise categories with clear boundaries

## Types of Topic Models

### Latent Dirichlet Allocation (LDA)

The foundational topic model.

**Assumptions:**
- Documents are mixtures of topics
- Topics are distributions over words
- Bag-of-words (word order doesn't matter)
- Fixed number of topics K

**Strengths:**
- Well-understood, widely used
- Many implementations available
- Interpretable output

**Weaknesses:**
- Must specify K in advance
- No covariates (can't explain topic variation)
- Can produce incoherent topics

### Structural Topic Model (STM)

**The gold standard for social science.**

**Key advantage:** Topic prevalence and content can vary by document covariates.

**Example:**
```
Topic prevalence ~ year + source + author_ideology
Topic content ~ formal_vs_informal
```

This allows: "How does discussion of Topic 3 change over time?"

**Strengths:**
- Covariates for prevalence and content
- Better diagnostics (exclusivity + coherence)
- Correlation between topics modeled
- Spectral initialization (more stable)

**Weaknesses:**
- R only (stm package)
- Slower than basic LDA
- More parameters to specify

### BERTopic

**Neural topic modeling using transformers.**

**Approach:**
1. Embed documents with BERT/sentence-transformers
2. Reduce dimensions with UMAP
3. Cluster with HDBSCAN
4. Extract topic words with c-TF-IDF

**Strengths:**
- Leverages semantic embeddings
- Handles short documents better
- Can discover varying numbers of topics
- Handles outliers explicitly

**Weaknesses:**
- Python only
- Less interpretable process
- Computationally intensive
- Newer, less validated in social science

## Choosing K (Number of Topics)

**K is a research decision, not a tuning parameter.**

### What K Represents

K determines granularity:
- K = 10: Broad themes
- K = 30: More specific topics
- K = 100: Fine-grained distinctions

Multiple K values are often defensible.

### Approaches to Selecting K

**1. Theory-driven:**
- How many themes would you expect?
- What level of granularity answers your question?
- Start with theory, adjust based on interpretability

**2. Diagnostic-guided:**

| Metric | What It Measures | Guidance |
|--------|------------------|----------|
| Coherence (C_V) | Do top words co-occur? | Higher is better; > 0.5 often good |
| Coherence (UMass) | Pairwise word co-occurrence | Less negative is better |
| Exclusivity | Are words unique to topics? | Higher means more distinct |
| Perplexity | Held-out likelihood | Lower is better fit |

**Important:** Do NOT just maximize coherence. A model with K=5 may have higher coherence but miss important distinctions.

**3. Interpretability-focused:**
- Can you label each topic?
- Do topics make substantive sense?
- Are there "junk" topics (stop words, artifacts)?
- Do topics split or merge sensibly across K?

### Recommended Approach

```
1. Start with theoretically plausible K (e.g., 15-20)
2. Run models at K-5, K, K+5, K+10
3. For each K:
   - Calculate coherence and exclusivity
   - Attempt to label all topics
   - Count "junk" or uninterpretable topics
4. Select K that balances:
   - Coherence/exclusivity metrics
   - Interpretability
   - Theoretical expectations
5. Report sensitivity to K choice
```

## Preprocessing for Topic Models

### Standard Pipeline

```
1. Lowercase
2. Remove punctuation
3. Remove stopwords (SMART list + custom)
4. Remove rare terms (< 5-10 documents)
5. Remove very common terms (> 50-80% of documents)
6. Optional: Lemmatization (NOT stemming)
```

### Preprocessing Choices and Trade-offs

| Choice | Pro | Con |
|--------|-----|-----|
| **Stemming** | Reduces vocabulary | Hurts interpretability |
| **Lemmatization** | Cleaner reduction | Slower, needs POS |
| **Bigrams** | Captures phrases | Larger vocabulary |
| **Aggressive stopwords** | Cleaner topics | May lose signal |

**Recommendation:** Start minimal, add preprocessing if topics have artifacts.

## Interpretation

### Reading Topics

For each topic, examine:

1. **Top words** (probability or FREX)
2. **Representative documents** (highest topic proportion)
3. **Distinctive words** (high in this topic, low elsewhere)

### Topic Labels

**Good labels:**
- Capture the theme, not just top words
- Are substantively meaningful
- Distinguish this topic from others

**Bad labels:**
- Just list top words
- Are too generic ("Miscellaneous")
- Require seeing the words to understand

### What Topics Are NOT

Topics are:
- Statistical patterns of word co-occurrence
- NOT necessarily coherent concepts
- NOT necessarily what documents are "about"

Avoid:
- "This document IS about Topic 3"
- "The topic model discovered that..."
- Treating topics as ground truth

Prefer:
- "This document has high probability for Topic 3"
- "Words associated with Topic 3 suggest..."
- "One interpretation of this pattern..."

## Validation

### Human Validation

**Word intrusion test:**
- Show top 5 words + 1 intruder from another topic
- Humans identify intruder
- High accuracy = coherent topic

**Document intrusion test:**
- Show 3 high-probability documents + 1 from another topic
- Humans identify intruder
- Tests whether topic captures document similarity

**Topic labeling:**
- Independent coders label topics
- Agreement indicates interpretability

### Computational Validation

**Coherence metrics:**
- UMass: Based on document co-occurrence
- C_V: Based on sliding window and word vectors
- NPMI: Normalized pointwise mutual information

**Held-out likelihood:**
- Fit on training documents
- Evaluate on held-out documents
- Better fit = lower perplexity

### Robustness Checks

**Essential:**
- Different random seeds (do same topics emerge?)
- Different K (do topics split/merge sensibly?)

**Recommended:**
- Different preprocessing
- Subset by time or source
- Compare to alternative method (clustering, BERTopic)

## Common Problems and Solutions

### Problem: Junk Topics

**Symptoms:** Top words are stopwords, numbers, artifacts

**Solutions:**
- Add terms to custom stopword list
- Increase minimum document frequency
- Check for encoding issues

### Problem: Duplicate Topics

**Symptoms:** Multiple topics with similar words

**Solutions:**
- Reduce K
- Check for document duplicates
- Consider topic correlation (STM)

### Problem: Uninterpretable Topics

**Symptoms:** Top words don't form coherent theme

**Solutions:**
- This happens—not all topics are meaningful
- Document as "Mixed/Other"
- Consider if K is too high

### Problem: Dominant Topic

**Symptoms:** One topic appears in most documents

**Solutions:**
- May be legitimate (common theme)
- Check if it's corpus-specific vocabulary
- Consider removing as "background" topic

## Reporting Standards

### Methods Section

```markdown
We used [LDA/STM/BERTopic] to identify latent topics in
the corpus. After preprocessing ([details]), the document-
term matrix contained N documents and M terms.

We estimated models with K = [X] topics. [Rationale for K].
For STM, topic prevalence was modeled as a function of
[covariates]. [Software and version].

[Validation approach and results].
```

### Results Section

- Topic labels with top words
- Prevalence estimates
- Covariate effects (if STM)
- Representative quotes

### Supplementary Materials

- Full topic-word distributions
- Robustness to K
- Preprocessing details
- Validation results

## Model Comparison

| Model | Best For | K Selection | Covariates | Language |
|-------|----------|-------------|------------|----------|
| **LDA** | Standard exploration | Manual | No | R, Python |
| **STM** | Social science research | Diagnostics help | Yes | R |
| **BERTopic** | Short texts, neural approach | Automatic | Limited | Python |
| **CTM** | Correlated topics | Manual | No | R, Python |
| **DTM** | Temporal dynamics | Manual | Time built-in | Python |

**Recommendation:** Use STM for academic social science research in R. Use BERTopic for neural approach in Python.
