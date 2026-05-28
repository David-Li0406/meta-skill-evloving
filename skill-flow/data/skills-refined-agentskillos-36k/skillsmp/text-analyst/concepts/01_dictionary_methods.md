# Dictionary Methods for Text Analysis

## Overview

Dictionary methods measure concepts in text by counting words from predefined lists. They are transparent, reproducible, and interpretable—but require careful validation.

## When to Use Dictionary Methods

**Good fit:**
- Measuring well-defined concepts (sentiment, emotions, moral foundations)
- Existing validated dictionaries available
- Need for transparency and reproducibility
- Large corpora where manual coding is infeasible

**Poor fit:**
- Exploratory analysis (don't know what to measure)
- Highly domain-specific language
- Concepts not captured by word lists
- Short texts with sparse matches

## Key Dictionaries

### General Purpose

| Dictionary | Concepts | Size | Access |
|------------|----------|------|--------|
| **LIWC** | 90+ categories (affect, cognition, social) | ~6,400 words | Licensed ($) |
| **VADER** | Sentiment (positive/negative/neutral) | ~7,500 words | Free |
| **NRC** | Emotions + sentiment | ~14,000 words | Free for research |
| **TextBlob** | Polarity + subjectivity | Built-in | Free |

### Domain-Specific

| Dictionary | Domain | Use Case |
|------------|--------|----------|
| **Loughran-McDonald** | Finance | 10-K filings, earnings calls |
| **Moral Foundations** | Moral psychology | Political rhetoric, values |
| **Harvard IV** | General inquiry | Classic, broad coverage |
| **AFINN** | Sentiment | Twitter, informal text |

### Custom Dictionaries

When to build your own:
- Domain-specific concepts
- No existing dictionary fits
- Need precise control over terms

## Constructing Custom Dictionaries

### Step 1: Define the Concept

Write a clear conceptual definition:
- What does this concept mean theoretically?
- What would indicate its presence in text?
- What are near-synonyms and related terms?

### Step 2: Generate Seed Terms

Sources for initial terms:
- Theory and literature
- Domain expertise
- Thesaurus expansion
- Word embeddings (similar words)

### Step 3: Expand and Refine

```
For each seed term:
  1. Find synonyms and variants
  2. Consider inflections (run, runs, running)
  3. Check actual usage in corpus (KWIC)
  4. Add domain-specific terms
  5. Remove ambiguous terms
```

### Step 4: Validate

- **Face validity**: Do terms look right to experts?
- **Coverage**: What % of documents have matches?
- **KWIC review**: Are matches capturing the concept?
- **Convergent validity**: Correlate with other measures

## Scoring Documents

### Count-Based

```
score = count of dictionary terms in document
```

Simple but confounded with document length.

### Proportion-Based

```
score = (dictionary terms) / (total words)
```

Controls for length. Standard approach.

### Weighted

```
score = Σ (term weight × term count)
```

Allows different terms to contribute differently (e.g., "excellent" > "good").

### Category Ratios

```
ratio = (positive terms) / (positive + negative terms)
```

Useful for comparing relative presence.

## Common Pitfalls

### 1. Polysemy (Multiple Meanings)

**Problem**: "Positive" means different things:
- "Positive attitude" (sentiment)
- "Tested positive" (medical)
- "Positive feedback loop" (technical)

**Solutions**:
- Review KWIC examples
- Use domain-specific dictionaries
- Consider context windows
- Accept and document limitations

### 2. Negation

**Problem**: "Not happy" contains "happy" but isn't positive.

**Solutions**:
- Negation handling (flip polarity within window)
- VADER handles negation automatically
- Consider bigrams ("not happy" as unit)
- Accept limitations for simple approaches

### 3. Intensity and Modifiers

**Problem**: "Very happy" vs "happy" vs "somewhat happy"

**Solutions**:
- VADER includes intensity modifiers
- Weight terms by intensity
- Use ML approaches for nuance

### 4. Sparse Matches

**Problem**: Many documents have zero or few matches.

**Solutions**:
- Report coverage statistics
- Consider document as missing if < threshold
- Use broader dictionaries
- Aggregate to higher level (paragraph → document)

### 5. Domain Mismatch

**Problem**: Dictionary built on different text type.

**Solutions**:
- Validate in your domain
- Build custom dictionary
- Report validation results

## Validation Requirements

### Minimum Validation

1. **Coverage**: Report % documents with ≥1 match
2. **KWIC review**: Sample 50+ uses of key terms
3. **Distribution**: Show score distribution

### Strong Validation

4. **Inter-rater reliability**: Human coding of sample
5. **Convergent validity**: Correlate with related measures
6. **Known groups**: Compare groups expected to differ

### Exemplary Validation

7. **Discriminant validity**: Show what it doesn't correlate with
8. **Predictive validity**: Does it predict outcomes?
9. **Cross-validation**: Test in different subset

## Reporting Standards

### Methods Section Should Include

```markdown
## Dictionary Analysis

We measured [concept] using the [Dictionary Name]
(Author, Year). This dictionary contains N terms
across M categories, developed for [context].

We calculated [scoring method] for each document.
[Preprocessing details].

### Validation
Dictionary terms matched X% of documents (mean = Y
matches per document). We reviewed N keyword-in-context
examples to assess face validity. [Results of validation].
```

### Results Section Should Include

- Distribution of scores (histogram/summary stats)
- Coverage information
- Key caveats about dictionary approach

### Supplementary Materials

- Full word list (or reference if published)
- Validation examples
- Any custom modifications

## Comparison to ML Approaches

| Aspect | Dictionary | ML Classifier |
|--------|------------|---------------|
| **Transparency** | High (word list visible) | Lower (learned weights) |
| **Training data** | Not needed | Required |
| **Domain adaptation** | Manual dictionary building | Retraining |
| **Nuance** | Limited (word presence) | Can learn context |
| **Reproducibility** | Perfect (same list = same result) | Depends on implementation |
| **Validation** | Face validity + coverage | Accuracy metrics |

**Use dictionary when**: Transparency matters, no training data, well-defined concept with existing dictionary.

**Use ML when**: Need to capture nuance, have labeled training data, complex concept.

## Recommended Workflow

```
1. Define concept clearly
2. Select or build dictionary
3. Calculate initial scores
4. Check coverage (>50% of docs should have matches)
5. KWIC validation (sample 50+ uses)
6. Assess distribution (ceiling/floor effects?)
7. Convergent validation (correlate with alternative)
8. Report all validation steps
9. Acknowledge limitations
```
