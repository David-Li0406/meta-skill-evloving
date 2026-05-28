# Dictionary and Sentiment Analysis in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# vaderSentiment 3.3.2
# textblob 0.17.1
# nltk 3.8.1
# pandas 2.0.0
```

## Installation

```bash
pip install vaderSentiment textblob nltk pandas

# Download TextBlob corpora
python -m textblob.download_corpora
```

## VADER Sentiment

VADER (Valence Aware Dictionary and sEntiment Reasoner) is designed for social media.

### Basic Usage

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# Sample texts
texts = [
    "I love this amazing product! Highly recommend!",
    "Terrible experience. The worst purchase ever.",
    "It's okay, nothing special but not bad.",
    "Great quality but expensive and slow delivery."
]

# Analyze sentiment
for text in texts:
    scores = analyzer.polarity_scores(text)
    print(f"{text[:40]:40} | {scores}")

# Output:
# I love this amazing product! Highly rec | {'neg': 0.0, 'neu': 0.254, 'pos': 0.746, 'compound': 0.8316}
# Terrible experience. The worst purchase | {'neg': 0.611, 'neu': 0.389, 'pos': 0.0, 'compound': -0.8316}
```

### VADER Output Interpretation

```python
# compound: normalized score from -1 (most negative) to +1 (most positive)
# pos, neg, neu: proportions of text falling in each category

# Classification thresholds
def classify_sentiment(compound):
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'
```

### Batch Processing

```python
def analyze_vader(texts):
    """Analyze sentiment for list of texts."""
    analyzer = SentimentIntensityAnalyzer()

    results = []
    for i, text in enumerate(texts):
        scores = analyzer.polarity_scores(text)
        results.append({
            'doc_id': i,
            'text': text[:100],
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment': classify_sentiment(scores['compound'])
        })

    return pd.DataFrame(results)

# Usage
sentiment_df = analyze_vader(texts)
print(sentiment_df)
```

### VADER Features

```python
# VADER handles:

# Punctuation emphasis
print(analyzer.polarity_scores("Good!"))       # compound: 0.4927
print(analyzer.polarity_scores("Good!!!"))     # compound: 0.6588 (stronger)

# Capitalization
print(analyzer.polarity_scores("good"))        # compound: 0.4404
print(analyzer.polarity_scores("GOOD"))        # compound: 0.5622 (stronger)

# Intensifiers
print(analyzer.polarity_scores("good"))        # compound: 0.4404
print(analyzer.polarity_scores("very good"))   # compound: 0.4927 (stronger)

# Negation
print(analyzer.polarity_scores("good"))        # compound: 0.4404
print(analyzer.polarity_scores("not good"))    # compound: -0.3412 (flipped)

# Conjunctions
print(analyzer.polarity_scores("good but bad"))  # Handles mixed
```

## TextBlob Sentiment

### Basic Usage

```python
from textblob import TextBlob

# Analyze text
blob = TextBlob("I love this amazing product!")
print(f"Polarity: {blob.sentiment.polarity}")      # -1 to 1
print(f"Subjectivity: {blob.sentiment.subjectivity}")  # 0 to 1

# Polarity: 0.625
# Subjectivity: 0.6
```

### Batch Processing

```python
def analyze_textblob(texts):
    """Analyze sentiment using TextBlob."""
    results = []
    for i, text in enumerate(texts):
        blob = TextBlob(text)
        results.append({
            'doc_id': i,
            'text': text[:100],
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        })

    return pd.DataFrame(results)

sentiment_tb = analyze_textblob(texts)
```

### Sentence-Level Analysis

```python
text = "The product quality is great. But the shipping was terrible."
blob = TextBlob(text)

for sentence in blob.sentences:
    print(f"{sentence} | Polarity: {sentence.sentiment.polarity:.2f}")

# The product quality is great. | Polarity: 0.66
# But the shipping was terrible. | Polarity: -1.00
```

## NRC Emotion Lexicon

### Loading NRC

```python
import pandas as pd

# NRC lexicon (download from https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm)
# Format: word \t emotion \t association (0 or 1)

def load_nrc(filepath='NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'):
    """Load NRC emotion lexicon."""
    nrc = pd.read_csv(
        filepath,
        sep='\t',
        names=['word', 'emotion', 'association']
    )
    # Pivot to word -> emotions
    nrc_wide = nrc[nrc.association == 1].pivot(
        index='word',
        columns='emotion',
        values='association'
    ).fillna(0)

    return nrc_wide

# nrc = load_nrc()
```

### Using NRC

```python
def analyze_nrc(text, nrc_lexicon):
    """Get emotion counts for text."""
    words = text.lower().split()
    emotions = nrc_lexicon.columns.tolist()

    counts = {e: 0 for e in emotions}

    for word in words:
        if word in nrc_lexicon.index:
            for emotion in emotions:
                counts[emotion] += nrc_lexicon.loc[word, emotion]

    return counts

# Usage
# emotions = analyze_nrc("I am so happy and excited!", nrc)
# print(emotions)
```

## Custom Dictionaries

### Creating a Custom Dictionary

```python
class CustomDictionary:
    """Custom dictionary for concept measurement."""

    def __init__(self, positive_words, negative_words=None, weights=None):
        """
        Parameters:
        -----------
        positive_words : list of str
        negative_words : list of str, optional
        weights : dict, optional (word -> weight)
        """
        self.positive = set(w.lower() for w in positive_words)
        self.negative = set(w.lower() for w in (negative_words or []))
        self.weights = weights or {}

    def score(self, text, normalize=True):
        """Score a text."""
        words = text.lower().split()

        if not words:
            return {'score': 0, 'pos_count': 0, 'neg_count': 0, 'coverage': 0}

        pos_count = 0
        neg_count = 0
        weighted_score = 0

        for word in words:
            weight = self.weights.get(word, 1)

            if word in self.positive:
                pos_count += 1
                weighted_score += weight
            elif word in self.negative:
                neg_count += 1
                weighted_score -= weight

        total_matches = pos_count + neg_count
        coverage = total_matches / len(words) if words else 0

        if normalize and len(words) > 0:
            score = weighted_score / len(words)
        else:
            score = weighted_score

        return {
            'score': score,
            'pos_count': pos_count,
            'neg_count': neg_count,
            'coverage': coverage
        }

# Usage
innovation_dict = CustomDictionary(
    positive_words=['innovative', 'breakthrough', 'revolutionary', 'novel'],
    negative_words=['obsolete', 'outdated', 'stagnant', 'declining'],
    weights={'revolutionary': 2, 'breakthrough': 2}
)

result = innovation_dict.score("The company made an innovative breakthrough")
print(result)
```

### Multi-Word Expressions

```python
import re

class MWEDictionary:
    """Dictionary with multi-word expressions."""

    def __init__(self, phrases):
        """
        Parameters:
        -----------
        phrases : dict (phrase -> category/value)
        """
        self.phrases = {p.lower(): v for p, v in phrases.items()}
        # Sort by length (longest first for matching)
        self.sorted_phrases = sorted(self.phrases.keys(), key=len, reverse=True)

    def find_matches(self, text):
        """Find all phrase matches in text."""
        text_lower = text.lower()
        matches = []

        for phrase in self.sorted_phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            for match in re.finditer(pattern, text_lower):
                matches.append({
                    'phrase': phrase,
                    'value': self.phrases[phrase],
                    'start': match.start(),
                    'end': match.end()
                })

        return matches

# Usage
tech_terms = MWEDictionary({
    'machine learning': 'tech',
    'artificial intelligence': 'tech',
    'deep learning': 'tech',
    'natural language processing': 'tech'
})

matches = tech_terms.find_matches("Machine learning and artificial intelligence are transforming research")
print(matches)
```

## Sentiment Over Time

```python
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Sample time-series data
dates = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(100)]
texts_time = pd.DataFrame({
    'date': dates,
    'text': [f"Sample text {i % 4}" for i in range(100)]
})

# Add sentiment
analyzer = SentimentIntensityAnalyzer()
texts_time['sentiment'] = texts_time['text'].apply(
    lambda x: analyzer.polarity_scores(x)['compound']
)

# Daily average
daily_sentiment = texts_time.groupby(texts_time['date'].dt.date)['sentiment'].mean()

# Plot
plt.figure(figsize=(12, 5))
plt.plot(daily_sentiment.index, daily_sentiment.values)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.xlabel('Date')
plt.ylabel('Sentiment (Compound)')
plt.title('Sentiment Over Time')
plt.tight_layout()
plt.savefig('output/figures/sentiment_time.png', dpi=300)
plt.close()
```

## Comparing Groups

```python
# Sample grouped data
group_texts = pd.DataFrame({
    'text': texts * 25,
    'group': ['A'] * 50 + ['B'] * 50
})

# Add sentiment
group_texts['sentiment'] = group_texts['text'].apply(
    lambda x: analyzer.polarity_scores(x)['compound']
)

# Compare groups
group_summary = group_texts.groupby('group')['sentiment'].agg(['mean', 'std', 'count'])
print(group_summary)

# Statistical test
from scipy import stats
group_a = group_texts[group_texts['group'] == 'A']['sentiment']
group_b = group_texts[group_texts['group'] == 'B']['sentiment']
t_stat, p_val = stats.ttest_ind(group_a, group_b)
print(f"t-statistic: {t_stat:.3f}, p-value: {p_val:.3f}")
```

## Validation

### Coverage Check

```python
def check_coverage(texts, analyzer):
    """Check sentiment lexicon coverage."""

    coverage_stats = []
    for text in texts:
        words = text.lower().split()
        scores = analyzer.polarity_scores(text)

        # Check which words contribute to sentiment
        word_scores = [analyzer.polarity_scores(w)['compound'] for w in words]
        contributing = sum(1 for s in word_scores if s != 0)

        coverage_stats.append({
            'n_words': len(words),
            'n_contributing': contributing,
            'coverage': contributing / len(words) if words else 0
        })

    coverage_df = pd.DataFrame(coverage_stats)

    print(f"Mean coverage: {coverage_df['coverage'].mean():.2%}")
    print(f"Docs with zero matches: {(coverage_df['n_contributing'] == 0).sum()}")

    return coverage_df

coverage = check_coverage(texts, analyzer)
```

### KWIC Validation

```python
def kwic(texts, word, window=5):
    """Keyword in context."""
    results = []

    for i, text in enumerate(texts):
        words = text.lower().split()
        for j, w in enumerate(words):
            if word.lower() in w:
                start = max(0, j - window)
                end = min(len(words), j + window + 1)
                context = ' '.join(words[start:end])
                results.append({
                    'doc_id': i,
                    'position': j,
                    'context': context
                })

    return pd.DataFrame(results)

# Check usage of key terms
kwic_results = kwic(texts, 'good')
print(kwic_results)
```

## Complete Workflow

```python
class SentimentAnalyzer:
    """Complete sentiment analysis pipeline."""

    def __init__(self, method='vader'):
        self.method = method

        if method == 'vader':
            self.analyzer = SentimentIntensityAnalyzer()
        elif method == 'textblob':
            pass  # TextBlob doesn't need initialization
        else:
            raise ValueError(f"Unknown method: {method}")

    def analyze_one(self, text):
        """Analyze single text."""
        if self.method == 'vader':
            scores = self.analyzer.polarity_scores(text)
            return {
                'compound': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        elif self.method == 'textblob':
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }

    def analyze_batch(self, texts):
        """Analyze list of texts."""
        results = []
        for i, text in enumerate(texts):
            result = self.analyze_one(text)
            result['doc_id'] = i
            result['text'] = text[:100]
            results.append(result)

        return pd.DataFrame(results)

    def get_coverage(self, texts):
        """Calculate coverage statistics."""
        if self.method != 'vader':
            raise NotImplementedError("Coverage only for VADER")

        return check_coverage(texts, self.analyzer)

# Usage
sa = SentimentAnalyzer(method='vader')
results = sa.analyze_batch(texts)
print(results)

# Summary statistics
print(f"\nSummary:")
print(f"Mean sentiment: {results['compound'].mean():.3f}")
print(f"Std sentiment: {results['compound'].std():.3f}")
print(f"Positive docs: {(results['compound'] > 0.05).sum()}")
print(f"Negative docs: {(results['compound'] < -0.05).sum()}")
print(f"Neutral docs: {((results['compound'] >= -0.05) & (results['compound'] <= 0.05)).sum()}")
```
