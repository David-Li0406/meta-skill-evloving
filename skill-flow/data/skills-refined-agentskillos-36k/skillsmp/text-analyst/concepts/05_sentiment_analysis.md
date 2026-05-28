# Sentiment Analysis

## Overview

Sentiment analysis measures the emotional tone, opinion, or attitude expressed in text. It ranges from simple positive/negative classification to nuanced emotion detection.

## Types of Sentiment Analysis

### Polarity Classification

**Goal:** Classify text as positive, negative, or neutral.

**Granularity:**
- Binary: Positive vs. Negative
- Ternary: Positive / Neutral / Negative
- Fine-grained: 5-point scale (very negative to very positive)

### Emotion Detection

**Goal:** Identify specific emotions.

**Common taxonomies:**
- Ekman: Anger, Disgust, Fear, Joy, Sadness, Surprise
- Plutchik: 8 primary emotions with intensities
- NRC: 8 emotions + positive/negative

### Aspect-Based Sentiment

**Goal:** Identify sentiment toward specific aspects.

**Example:** "The food was great but the service was slow."
- Food: Positive
- Service: Negative

### Stance Detection

**Goal:** Identify position toward a target.

**Example:** Favor, Against, or Neutral toward a policy.

## Approaches

### Dictionary-Based

**How it works:**
1. Match words to sentiment lexicon
2. Aggregate scores
3. Classify based on threshold

**Advantages:**
- Transparent (know exactly which words triggered)
- No training data needed
- Fast

**Disadvantages:**
- Misses context and sarcasm
- Domain mismatch issues
- Doesn't handle negation well (simple versions)

### Machine Learning

**How it works:**
1. Train classifier on labeled examples
2. Learn patterns from data
3. Apply to new texts

**Advantages:**
- Learns domain-specific patterns
- Can capture complex relationships
- Often more accurate

**Disadvantages:**
- Needs labeled training data
- Less interpretable
- May not generalize

### Deep Learning / Transformers

**How it works:**
- Fine-tune BERT or similar on sentiment task
- Or use pretrained sentiment models

**Advantages:**
- State-of-the-art performance
- Captures context and nuance
- Transfer learning

**Disadvantages:**
- Computational cost
- Needs more training data
- Least interpretable

## Popular Tools and Lexicons

### Dictionary-Based Tools

| Tool | Approach | Strengths |
|------|----------|-----------|
| **VADER** | Rule-based with intensifiers | Social media, handles punctuation/emoji |
| **TextBlob** | Pattern-based | Simple, fast, includes subjectivity |
| **LIWC** | Category-based | Extensive psychological categories |
| **AFINN** | Scored word list | Simple, manually curated |
| **SentiWordNet** | WordNet-based | Large coverage, synset scores |

### Key Lexicons

| Lexicon | Content | Best For |
|---------|---------|----------|
| **LIWC** | 90+ categories | Psychological analysis |
| **NRC Emotion** | 8 emotions + valence | Emotion detection |
| **NRC VAD** | Valence, Arousal, Dominance | Dimensional emotion |
| **Loughran-McDonald** | Finance-specific | Financial texts |
| **VADER** | Social media focused | Tweets, reviews |

### Pretrained Models

| Model | Source | Use Case |
|-------|--------|----------|
| **distilbert-sentiment** | HuggingFace | General sentiment |
| **twitter-roberta-sentiment** | HuggingFace | Twitter/social media |
| **finbert** | HuggingFace | Financial sentiment |
| **cardiffnlp models** | HuggingFace | Social media tasks |

## VADER: A Closer Look

VADER (Valence Aware Dictionary and sEntiment Reasoner) is popular for social media.

**Features:**
- Handles punctuation ("good!" vs "good")
- Handles capitalization ("GOOD" vs "good")
- Handles intensifiers ("very good")
- Handles negation ("not good")
- Handles conjunctions ("good but not great")
- Includes emoji support

**Output:**
```python
{'neg': 0.0, 'neu': 0.254, 'pos': 0.746, 'compound': 0.8316}
```

**Compound score:** -1 (most negative) to +1 (most positive)
- Compound ≥ 0.05 → Positive
- Compound ≤ -0.05 → Negative
- Otherwise → Neutral

## Domain Considerations

### Domain Mismatch

**Problem:** Sentiment lexicons trained on one domain may fail on another.

**Example:** "Unpredictable" is:
- Negative in product reviews ("unpredictable quality")
- Positive in movie reviews ("unpredictable plot")
- Neutral in academic text

### Domain-Specific Approaches

| Domain | Recommended Approach |
|--------|---------------------|
| **Product reviews** | General sentiment tools work well |
| **Social media** | VADER, Twitter-specific models |
| **Financial** | Loughran-McDonald, FinBERT |
| **Political** | Custom dictionaries, stance detection |
| **Academic** | May need custom approach |
| **Medical** | Specialized models needed |

## Handling Challenges

### Negation

**Problem:** "Not good" contains positive word but negative meaning.

**Solutions:**
- VADER handles automatically
- Negation window (flip polarity of following words)
- Bigram features ("not_good" as single token)

### Sarcasm and Irony

**Problem:** "Oh great, another meeting" is negative despite "great."

**Solutions:**
- Very difficult for automated methods
- Large models (GPT, BERT) do better but not perfectly
- Consider domain (sarcasm more common in social media)
- Accept and document limitation

### Intensity

**Problem:** "Good," "great," and "amazing" differ in intensity.

**Solutions:**
- VADER includes intensity modifiers
- Use fine-grained scales (1-5 instead of pos/neg)
- NRC VAD provides intensity dimensions

### Mixed Sentiment

**Problem:** Documents contain both positive and negative elements.

**Solutions:**
- Report both positive and negative scores
- Use aspect-based sentiment
- Analyze at sentence level and aggregate

### Implicit Sentiment

**Problem:** "The product arrived broken" implies negative without explicit sentiment words.

**Solutions:**
- ML approaches learn these patterns
- Larger context models (BERT) help
- May require aspect-based sentiment

## Validation

### Comparing to Human Judgment

**Essential validation:**
1. Sample documents
2. Have humans rate sentiment
3. Calculate agreement with automated scores

**Metrics:**
- Correlation (for continuous scores)
- Accuracy, F1 (for categories)
- Cohen's Kappa (for agreement)

### Reporting Validation

```markdown
We validated VADER sentiment scores against human coding.
Two coders rated N documents on a 5-point scale
(inter-rater reliability: r = 0.XX). VADER compound
scores correlated with human ratings at r = 0.XX.
```

### Known Benchmark Comparisons

Report performance on standard datasets if applicable:
- Movie reviews (Pang & Lee)
- Twitter sentiment (SemEval)
- Product reviews (Amazon)

## Reporting Standards

### Methods Section

```markdown
## Sentiment Analysis

We measured sentiment using [tool/lexicon] (Author, Year).
[Brief description of tool].

For each document, we calculated [metric: compound score /
positive-negative ratio / classification].

[Preprocessing steps if any].

### Validation
We validated against [human coding / alternative measure].
[Validation results].
```

### Results Section

Report:
- Distribution of sentiment scores
- Mean/median by relevant groups
- Temporal trends if applicable
- Key limitations

### Visualizations

- Histogram of sentiment distribution
- Time series of sentiment
- Comparison across groups (bar chart or violin plot)

## Choosing an Approach

```
Is interpretability critical?
  Yes → Dictionary-based (VADER, LIWC)
  No → Continue

Do you have labeled training data?
  Yes → Consider ML approach
  No → Continue

Is text from social media?
  Yes → VADER or twitter-roberta-sentiment
  No → Continue

Is text domain-specific (finance, medical)?
  Yes → Use domain-specific lexicon or model
  No → Continue

Default: Start with VADER, validate, consider alternatives
```

## Practical Workflow

```
1. Start with VADER (or domain-appropriate tool)
2. Calculate sentiment for all documents
3. Check distribution (ceiling/floor effects?)
4. Validate on sample against human judgment
5. Examine errors (why did it fail?)
6. Consider alternatives if validation is poor
7. Report validation and limitations
```

## Code Examples

### VADER in Python

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores("This is a great example!")
# {'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6588}
```

### TextBlob in Python

```python
from textblob import TextBlob

blob = TextBlob("This is a great example!")
print(blob.sentiment)
# Sentiment(polarity=0.8, subjectivity=0.75)
```

### tidytext in R

```r
library(tidytext)
library(dplyr)

text_df <- tibble(text = c("This is great!", "This is terrible."))

text_df %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing")) %>%
  count(sentiment)
```

### HuggingFace Transformers

```python
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")
result = sentiment_pipeline("This is a great example!")
# [{'label': 'POSITIVE', 'score': 0.9998}]
```

## Common Pitfalls

1. **Not validating in domain** - Always check if tool works for your texts
2. **Ignoring coverage** - What % of documents have sentiment words?
3. **Over-interpreting scores** - Small differences may not be meaningful
4. **Treating as ground truth** - Sentiment scores are estimates with error
5. **Not reporting method details** - Readers need to evaluate appropriateness
