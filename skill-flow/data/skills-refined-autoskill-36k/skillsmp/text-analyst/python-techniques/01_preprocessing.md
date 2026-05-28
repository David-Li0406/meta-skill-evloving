# Text Preprocessing in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# nltk 3.8.1
# spacy 3.6.0
# scikit-learn 1.3.0
```

## Installation

```bash
pip install nltk spacy scikit-learn pandas

# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

## Three Approaches: NLTK vs spaCy vs sklearn

| Package | Philosophy | Best For |
|---------|------------|----------|
| **NLTK** | Educational, comprehensive | Learning, custom pipelines |
| **spaCy** | Industrial-strength NLP | Production, entity recognition |
| **sklearn** | Machine learning focused | Vectorization for ML |

## NLTK Workflow

### Basic Tokenization

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Sample texts
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is transforming social science research.",
    "Text analysis requires careful preprocessing decisions."
]

# Word tokenization
tokens = [word_tokenize(text.lower()) for text in texts]
print(tokens[0])
# ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.']

# Sentence tokenization
sentences = [sent_tokenize(text) for text in texts]
```

### Stopword Removal

```python
stop_words = set(stopwords.words('english'))

# Remove stopwords
tokens_clean = [[w for w in doc if w not in stop_words and w.isalpha()]
                for doc in tokens]

print(tokens_clean[0])
# ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']

# Custom stopwords
custom_stops = {'data', 'analysis', 'research'}
stop_words = stop_words.union(custom_stops)
```

### Stemming and Lemmatization

```python
# Stemming (Porter)
stemmer = PorterStemmer()
tokens_stemmed = [[stemmer.stem(w) for w in doc] for doc in tokens_clean]

# Lemmatization
lemmatizer = WordNetLemmatizer()
tokens_lemma = [[lemmatizer.lemmatize(w) for w in doc] for doc in tokens_clean]

# Compare
print(f"Original: jumps")
print(f"Stemmed: {stemmer.stem('jumps')}")     # jump
print(f"Lemmatized: {lemmatizer.lemmatize('jumps', pos='v')}")  # jump
```

### N-grams

```python
from nltk import ngrams

# Bigrams
bigrams = [list(ngrams(doc, 2)) for doc in tokens_clean]
print(bigrams[0])
# [('quick', 'brown'), ('brown', 'fox'), ...]

# Trigrams
trigrams = [list(ngrams(doc, 3)) for doc in tokens_clean]
```

## spaCy Workflow

### Basic Processing

```python
import spacy

# Load model
nlp = spacy.load('en_core_web_sm')

# Process text
doc = nlp("Machine learning is transforming social science research.")

# Tokens with attributes
for token in doc:
    print(f"{token.text:15} {token.pos_:8} {token.lemma_:15} {token.is_stop}")
```

### Complete Preprocessing Pipeline

```python
def preprocess_spacy(texts, nlp, remove_stops=True, lemmatize=True):
    """
    Preprocess texts using spaCy.

    Parameters:
    -----------
    texts : list of str
    nlp : spacy model
    remove_stops : bool
    lemmatize : bool

    Returns:
    --------
    list of list of str : processed tokens
    """
    processed = []
    for doc in nlp.pipe(texts, batch_size=50):
        tokens = []
        for token in doc:
            # Skip punctuation, spaces, and optionally stopwords
            if token.is_punct or token.is_space:
                continue
            if remove_stops and token.is_stop:
                continue

            # Lemmatize or use original
            if lemmatize:
                tokens.append(token.lemma_.lower())
            else:
                tokens.append(token.text.lower())

        processed.append(tokens)

    return processed

# Usage
tokens = preprocess_spacy(texts, nlp)
print(tokens[1])
# ['machine', 'learn', 'transform', 'social', 'science', 'research']
```

### Named Entity Recognition

```python
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for ent in doc.ents:
    print(f"{ent.text:20} {ent.label_:10} {spacy.explain(ent.label_)}")

# Apple                ORG        Companies, agencies, institutions
# U.K.                 GPE        Countries, cities, states
# $1 billion           MONEY      Monetary values
```

### Custom Pipeline Component

```python
from spacy.language import Language

@Language.component("custom_cleaner")
def custom_cleaner(doc):
    """Remove URLs and email addresses."""
    cleaned_tokens = []
    for token in doc:
        if not token.like_url and not token.like_email:
            cleaned_tokens.append(token)
    return doc

# Add to pipeline
nlp.add_pipe("custom_cleaner", after="parser")
```

## sklearn Workflow

### CountVectorizer

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Basic count vectorizer
count_vec = CountVectorizer(
    lowercase=True,
    stop_words='english',
    max_features=1000,
    min_df=2,           # Minimum document frequency
    max_df=0.95,        # Maximum document frequency
    ngram_range=(1, 2)  # Unigrams and bigrams
)

# Fit and transform
dtm = count_vec.fit_transform(texts)

# Inspect
print(f"Shape: {dtm.shape}")
print(f"Vocabulary size: {len(count_vec.vocabulary_)}")
print(f"Feature names: {count_vec.get_feature_names_out()[:10]}")
```

### TF-IDF Vectorizer

```python
tfidf_vec = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    max_features=1000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 1),
    sublinear_tf=True   # Apply log to TF
)

tfidf_matrix = tfidf_vec.fit_transform(texts)
```

### Custom Tokenizer with sklearn

```python
def custom_tokenizer(text):
    """Custom tokenizer with spaCy."""
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha]

# Use in vectorizer
custom_vec = TfidfVectorizer(tokenizer=custom_tokenizer)
custom_matrix = custom_vec.fit_transform(texts)
```

## Handling Special Cases

### URLs and HTML

```python
import re

def clean_text(text):
    """Basic text cleaning."""
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text

# Apply
texts_clean = [clean_text(t) for t in texts]
```

### Handling Emojis and Special Characters

```python
import emoji

def handle_emojis(text, mode='remove'):
    """Handle emojis in text."""
    if mode == 'remove':
        return emoji.replace_emoji(text, '')
    elif mode == 'demojize':
        return emoji.demojize(text)
    return text

# Example
text_with_emoji = "Great product! 😊👍"
print(handle_emojis(text_with_emoji, 'demojize'))
# Great product! :smiling_face_with_smiling_eyes::thumbs_up:
```

### Encoding Issues

```python
def fix_encoding(text):
    """Fix common encoding issues."""
    # Handle None
    if text is None:
        return ""

    # Ensure string
    if not isinstance(text, str):
        text = str(text)

    # Fix encoding
    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    except:
        text = ""

    return text
```

## Document-Term Matrix Operations

### Converting to Dense

```python
import pandas as pd
import numpy as np

# Sparse to dense (only for small matrices!)
dense_matrix = dtm.toarray()

# As DataFrame
dtm_df = pd.DataFrame(
    dense_matrix,
    columns=count_vec.get_feature_names_out()
)
```

### Vocabulary Statistics

```python
def get_vocab_stats(vectorizer, dtm):
    """Get vocabulary statistics."""
    feature_names = vectorizer.get_feature_names_out()
    freqs = np.asarray(dtm.sum(axis=0)).ravel()
    doc_freqs = np.asarray((dtm > 0).sum(axis=0)).ravel()

    stats = pd.DataFrame({
        'term': feature_names,
        'total_freq': freqs,
        'doc_freq': doc_freqs,
        'doc_freq_pct': doc_freqs / dtm.shape[0]
    }).sort_values('total_freq', ascending=False)

    return stats

stats = get_vocab_stats(count_vec, dtm)
print(stats.head(20))
```

## Complete Preprocessing Pipeline

```python
import pandas as pd
from typing import List, Optional

class TextPreprocessor:
    """Complete text preprocessing pipeline."""

    def __init__(
        self,
        language: str = 'english',
        remove_stops: bool = True,
        lemmatize: bool = True,
        min_token_len: int = 2,
        custom_stops: Optional[List[str]] = None
    ):
        self.language = language
        self.remove_stops = remove_stops
        self.lemmatize = lemmatize
        self.min_token_len = min_token_len

        # Load spaCy
        self.nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

        # Set stopwords
        self.stop_words = set(stopwords.words(language))
        if custom_stops:
            self.stop_words.update(custom_stops)

    def clean_text(self, text: str) -> str:
        """Basic text cleaning."""
        if not isinstance(text, str):
            return ""

        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)

        # Remove HTML
        text = re.sub(r'<[^>]+>', '', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text

    def tokenize(self, text: str) -> List[str]:
        """Tokenize and optionally lemmatize."""
        doc = self.nlp(text)
        tokens = []

        for token in doc:
            # Skip punctuation and spaces
            if token.is_punct or token.is_space:
                continue

            # Skip stopwords
            if self.remove_stops and token.text.lower() in self.stop_words:
                continue

            # Get token text
            if self.lemmatize:
                tok = token.lemma_.lower()
            else:
                tok = token.text.lower()

            # Skip short tokens
            if len(tok) < self.min_token_len:
                continue

            # Only alphabetic
            if not tok.isalpha():
                continue

            tokens.append(tok)

        return tokens

    def preprocess(self, texts: List[str]) -> List[List[str]]:
        """Full preprocessing pipeline."""
        processed = []
        for text in texts:
            clean = self.clean_text(text)
            tokens = self.tokenize(clean)
            processed.append(tokens)
        return processed

    def get_stats(self, processed: List[List[str]]) -> dict:
        """Get corpus statistics."""
        all_tokens = [t for doc in processed for t in doc]
        return {
            'n_documents': len(processed),
            'n_tokens': len(all_tokens),
            'n_types': len(set(all_tokens)),
            'mean_doc_length': len(all_tokens) / len(processed),
            'empty_docs': sum(1 for doc in processed if len(doc) == 0)
        }

# Usage
preprocessor = TextPreprocessor(
    remove_stops=True,
    lemmatize=True,
    custom_stops=['data', 'study']
)

processed = preprocessor.preprocess(texts)
stats = preprocessor.get_stats(processed)
print(stats)
```

## Best Practices

1. **Document all decisions** - Keep preprocessing log
2. **Start minimal** - Add processing steps only if needed
3. **Check vocabulary** - Examine most/least frequent terms
4. **Use batching** - Process in batches for large corpora
5. **Save intermediate results** - For reproducibility
6. **Set random seeds** - For any stochastic elements

```python
# Preprocessing log
preprocessing_log = {
    'date': pd.Timestamp.now().isoformat(),
    'n_docs_raw': len(texts),
    'n_docs_processed': len(processed),
    'vocab_size': stats['n_types'],
    'stopwords': 'english + custom',
    'lemmatization': 'spacy',
    'min_token_length': 2
}

# Save
pd.Series(preprocessing_log).to_json('data/processed/preprocessing_log.json')
```
