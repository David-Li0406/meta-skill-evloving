# Supervised Text Classification

## Overview

Supervised classification trains a model on labeled examples to categorize new documents. Unlike topic models (unsupervised), classification requires training data with known labels.

## When to Use Classification

**Good fit:**
- Categories are predefined and clear
- Labeled training data is available
- Need to classify new documents consistently
- Categories don't overlap substantially

**Poor fit:**
- Exploring unknown structure (use topic models)
- Labels are subjective or inconsistent
- Very few labeled examples (< 50 per class)
- Categories are fuzzy or overlapping

## The Classification Pipeline

```
1. Obtain labeled training data
2. Preprocess text
3. Extract features (vectorization)
4. Train classifier
5. Evaluate on held-out data
6. Apply to new documents
```

## Training Data

### Obtaining Labels

**Sources:**
- Existing metadata (source, category, author)
- Expert coding
- Crowdsourced coding
- Weak supervision (patterns, keywords)

### How Much Data?

| Task Complexity | Minimum per Class | Recommended |
|-----------------|-------------------|-------------|
| Binary, clear distinction | 50 | 200+ |
| Multi-class (3-5 classes) | 100 | 300+ per class |
| Fine-grained (10+ classes) | 200 | 500+ per class |
| Rare classes | More for minority | Balance classes |

### Label Quality

**Requirements:**
- Clear category definitions
- Consistent application
- Inter-rater reliability (if multiple coders)
- Documentation of edge cases

**Calculating inter-rater reliability:**
- Cohen's Kappa for 2 raters
- Fleiss' Kappa for 3+ raters
- Target: Kappa > 0.7 for acceptable reliability

## Feature Extraction

### Bag-of-Words / TF-IDF

```
Document → Vector of term frequencies
```

**TF-IDF weighting:**
- Upweights distinctive terms
- Downweights common terms
- Standard for traditional ML

**Parameters:**
- Vocabulary size (max_features)
- N-gram range (unigrams, bigrams)
- Min/max document frequency

### Word Embeddings

**Pre-trained:**
- Word2Vec, GloVe averages
- Sentence embeddings (SBERT)
- Paragraph vectors (Doc2Vec)

**Strengths:**
- Captures semantic similarity
- Handles synonyms
- Lower-dimensional

**Weaknesses:**
- Less interpretable
- May miss domain-specific meaning

### Contextual Embeddings (BERT)

**Approach:**
- Use BERT/RoBERTa to encode documents
- Fine-tune on classification task
- Or use embeddings with simpler classifier

**Strengths:**
- State-of-the-art performance
- Captures context and nuance
- Transfer learning from large corpora

**Weaknesses:**
- Computationally expensive
- Requires GPU for training
- Harder to interpret

## Classifier Models

### Traditional ML

| Model | Strengths | Weaknesses |
|-------|-----------|------------|
| **Naive Bayes** | Fast, works with small data | Assumes independence |
| **Logistic Regression** | Interpretable, reliable | Linear boundaries |
| **SVM** | Effective in high dimensions | Less interpretable |
| **Random Forest** | Handles non-linearity | Slower, larger models |

**Recommendation:** Start with Logistic Regression or SVM for interpretability and reliability.

### Deep Learning

| Model | Strengths | Weaknesses |
|-------|-----------|------------|
| **CNN** | Captures local patterns | Needs more data |
| **LSTM/RNN** | Sequence modeling | Slow to train |
| **BERT fine-tuned** | State-of-the-art | Needs GPU, more data |

**Recommendation:** Use BERT only if you have 1000+ examples per class and GPU access.

### Zero-Shot Classification

**Approach:** Use large language models to classify without training data.

```python
from transformers import pipeline
classifier = pipeline("zero-shot-classification")
result = classifier(text, candidate_labels=["politics", "sports", "business"])
```

**Strengths:**
- No training data needed
- Quick to prototype

**Weaknesses:**
- Less accurate than fine-tuned models
- Depends on label naming
- Not validated for research use

## Evaluation Metrics

### Basic Metrics

| Metric | Formula | Use When |
|--------|---------|----------|
| **Accuracy** | Correct / Total | Classes are balanced |
| **Precision** | TP / (TP + FP) | False positives are costly |
| **Recall** | TP / (TP + FN) | False negatives are costly |
| **F1** | 2 × (P × R) / (P + R) | Balance precision/recall |

### Multi-Class Metrics

| Metric | Description |
|--------|-------------|
| **Macro-F1** | Average F1 across classes (equal weight) |
| **Weighted-F1** | F1 weighted by class frequency |
| **Micro-F1** | Global TP/FP/FN (equals accuracy) |

**Recommendation:** Report macro-F1 for research (treats all classes equally).

### Confusion Matrix

Essential for understanding errors:

```
              Predicted
             Pos    Neg
Actual Pos [ TP     FN ]
       Neg [ FP     TN ]
```

Always examine:
- Which classes are confused?
- Are errors systematic?
- What do misclassified examples look like?

## Train/Test Splitting

### Hold-Out Validation

```
Full Data → Train (70-80%) / Test (20-30%)
```

**Never use test set for model selection.**

### Cross-Validation

```
Data → K folds
For each fold:
  Train on K-1 folds
  Evaluate on 1 fold
Report: Mean ± SD of metric
```

**Recommendation:** 5-fold or 10-fold CV for model selection.

### Stratified Splitting

**Always stratify by class label** to maintain class proportions in each split.

```python
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

### Temporal Considerations

If data is time-ordered:
- Consider temporal split (train on past, test on future)
- Avoid data leakage from future to past

## Handling Class Imbalance

### The Problem

If Class A has 90% of examples:
- Predicting "A" always gives 90% accuracy
- Minority class poorly classified

### Solutions

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Class weights** | Upweight minority class loss | First approach to try |
| **Oversampling** | Duplicate minority examples | Simple, effective |
| **SMOTE** | Synthetic minority examples | When oversampling insufficient |
| **Undersampling** | Reduce majority class | Large datasets only |

**In sklearn:**
```python
model = LogisticRegression(class_weight='balanced')
```

## Error Analysis

### Systematic Error Analysis

After training:

1. **Identify misclassified examples**
2. **Categorize errors:**
   - Label noise (gold label is wrong)
   - Ambiguous cases (genuinely unclear)
   - Model limitations (learnable but missed)
3. **Look for patterns:**
   - Are certain terms misleading?
   - Are certain document types harder?
4. **Improve:**
   - Fix labeling issues
   - Add training examples for hard cases
   - Adjust features or preprocessing

### Example Error Analysis

```markdown
## Error Analysis: Politics vs. Business

### Most Common Errors
1. Economic policy articles → Often misclassified
   - Contain both political and business vocabulary
   - Solution: Consider "Policy" as separate class

2. Campaign finance articles → Classified as Business
   - "Donations", "funding" trigger business features
   - Solution: Add "campaign" + "finance" bigrams
```

## Active Learning

When labeling is expensive:

1. Train initial model on small labeled set
2. Apply to unlabeled data
3. Select uncertain examples for labeling
4. Add labels, retrain
5. Repeat

**Selection strategies:**
- Uncertainty sampling (label what model is unsure about)
- Query-by-committee (label where models disagree)

## Reporting Standards

### Methods Section

```markdown
## Text Classification

We trained a [model type] classifier to categorize documents
into [N] classes: [class names].

Training data consisted of N documents labeled by [process].
Inter-rater reliability: Kappa = X.XX (N coders, N documents).

Features: [TF-IDF with N features / BERT embeddings / etc.]
Preprocessing: [steps]

We used [K]-fold stratified cross-validation for model
selection and report performance on a held-out test set
(N = X documents).
```

### Results Section

```markdown
The classifier achieved macro-F1 = X.XX on the held-out
test set (Table X). Per-class performance ranged from
F1 = X.XX ([class]) to F1 = X.XX ([class]).

Error analysis revealed [systematic patterns].
```

### Tables

**Table: Classification Performance**

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|-----|---------|
| Class A | 0.85 | 0.82 | 0.83 | 150 |
| Class B | 0.78 | 0.81 | 0.79 | 120 |
| ... | | | | |
| Macro Avg | 0.81 | 0.81 | 0.81 | 400 |

## Common Pitfalls

### 1. Data Leakage

**Problem:** Information from test set influences training.

**Solutions:**
- Split data BEFORE any preprocessing
- Don't use test set for feature selection
- Be careful with temporal data

### 2. Overfitting

**Problem:** Model memorizes training data.

**Signs:**
- Training accuracy >> test accuracy
- Model is overly complex

**Solutions:**
- Regularization
- Cross-validation
- Simpler model

### 3. Label Leakage

**Problem:** Feature contains label information.

**Example:** Document ID correlates with class (same authors write same topics).

**Solution:** Remove non-content features.

### 4. Ignoring Class Imbalance

**Problem:** Majority class dominates.

**Solution:** Use class weights, macro-F1 evaluation.

## Classifier Selection Guide

```
Is interpretability important?
  Yes → Logistic Regression or Naive Bayes
  No → Continue

Do you have > 1000 examples per class?
  Yes → Consider BERT fine-tuning
  No → Continue

Is the task complex (subtle distinctions)?
  Yes → SVM with careful feature engineering
  No → Logistic Regression with TF-IDF

Do you have GPU access and time?
  Yes → Try BERT, compare to baseline
  No → Stick with traditional ML
```
