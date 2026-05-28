# Topic Models in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# gensim 4.3.1
# bertopic 0.15.0
# scikit-learn 1.3.0
```

## Installation

```bash
pip install gensim bertopic scikit-learn pyLDAvis

# For BERTopic with sentence-transformers
pip install sentence-transformers
```

## Gensim LDA

### Preparing Data

```python
import gensim
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
from gensim.parsing.preprocessing import STOPWORDS
import pandas as pd

# Sample texts
texts = [
    "The economy shows signs of growth with increased employment.",
    "Healthcare reform remains a divisive political issue.",
    "Climate change impacts are becoming more severe.",
    "Education funding varies widely across states.",
    "Technology transforms modern communication methods.",
] * 20  # Replicate for minimum corpus size

# Preprocessing
def preprocess(text):
    """Simple preprocessing."""
    tokens = gensim.utils.simple_preprocess(text, deacc=True)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]

processed_texts = [preprocess(t) for t in texts]

# Create dictionary
dictionary = corpora.Dictionary(processed_texts)

# Filter extremes
dictionary.filter_extremes(
    no_below=2,    # Minimum documents
    no_above=0.9   # Maximum proportion
)

# Create corpus (bag of words)
corpus = [dictionary.doc2bow(doc) for doc in processed_texts]

print(f"Dictionary size: {len(dictionary)}")
print(f"Corpus size: {len(corpus)}")
```

### Training LDA

```python
# Set random seed for reproducibility
import random
import numpy as np
random.seed(42)
np.random.seed(42)

# Train LDA model
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=5,
    random_state=42,
    passes=10,        # Epochs
    alpha='auto',     # Learn alpha
    eta='auto',       # Learn eta
    per_word_topics=True
)

# View topics
for idx, topic in lda_model.print_topics(num_words=10):
    print(f"Topic {idx}: {topic}")
```

### Coherence Score

```python
# Calculate coherence
coherence_model = CoherenceModel(
    model=lda_model,
    texts=processed_texts,
    dictionary=dictionary,
    coherence='c_v'
)

coherence_score = coherence_model.get_coherence()
print(f"Coherence Score (C_V): {coherence_score:.4f}")

# Alternative coherence metrics
for metric in ['u_mass', 'c_v', 'c_npmi']:
    cm = CoherenceModel(
        model=lda_model,
        texts=processed_texts,
        dictionary=dictionary,
        coherence=metric
    )
    print(f"Coherence ({metric}): {cm.get_coherence():.4f}")
```

### Selecting K

```python
def compute_coherence_values(dictionary, corpus, texts, k_range):
    """Compute coherence for range of K values."""
    results = []

    for k in k_range:
        model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=k,
            random_state=42,
            passes=10
        )

        coherence = CoherenceModel(
            model=model,
            texts=texts,
            dictionary=dictionary,
            coherence='c_v'
        ).get_coherence()

        results.append({
            'k': k,
            'coherence': coherence
        })
        print(f"K={k}: Coherence={coherence:.4f}")

    return pd.DataFrame(results)

# Search over K
k_results = compute_coherence_values(
    dictionary, corpus, processed_texts,
    k_range=range(3, 15, 2)
)

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(k_results['k'], k_results['coherence'], 'o-')
plt.xlabel('Number of Topics (K)')
plt.ylabel('Coherence Score')
plt.title('Topic Model Coherence by K')
plt.savefig('output/figures/coherence_k.png', dpi=300)
plt.close()
```

### Document-Topic Distribution

```python
def get_document_topics(model, corpus):
    """Get topic distribution for each document."""
    doc_topics = []

    for doc_bow in corpus:
        topic_dist = model.get_document_topics(doc_bow, minimum_probability=0)
        topic_dict = {f'topic_{t}': p for t, p in topic_dist}
        doc_topics.append(topic_dict)

    return pd.DataFrame(doc_topics)

doc_topics_df = get_document_topics(lda_model, corpus)
print(doc_topics_df.head())

# Dominant topic per document
doc_topics_df['dominant_topic'] = doc_topics_df.idxmax(axis=1)
```

## BERTopic

### Basic BERTopic

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Simple usage (uses default embedding model)
topic_model = BERTopic(language="english", verbose=True)
topics, probs = topic_model.fit_transform(texts)

# View topics
topic_model.get_topic_info()
```

### BERTopic with Custom Settings

```python
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

# Custom embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Custom UMAP
umap_model = UMAP(
    n_neighbors=15,
    n_components=5,
    min_dist=0.0,
    metric='cosine',
    random_state=42
)

# Custom HDBSCAN
hdbscan_model = HDBSCAN(
    min_cluster_size=10,
    min_samples=5,
    metric='euclidean',
    prediction_data=True
)

# Custom vectorizer for topic representation
vectorizer_model = CountVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

# Create model
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    top_n_words=10,
    verbose=True
)

# Fit
topics, probs = topic_model.fit_transform(texts)
```

### Examining BERTopic Results

```python
# Topic info
topic_info = topic_model.get_topic_info()
print(topic_info)

# Specific topic words
topic_0_words = topic_model.get_topic(0)
print(f"Topic 0: {topic_0_words}")

# Document-topic mapping
doc_info = topic_model.get_document_info(texts)
print(doc_info.head())

# Topic frequency
topic_model.visualize_barchart(top_n_topics=10)
```

### BERTopic Visualizations

```python
# Topic word scores
fig = topic_model.visualize_barchart(top_n_topics=8)
fig.write_html("output/figures/bertopic_barchart.html")

# Topic similarity
fig = topic_model.visualize_heatmap()
fig.write_html("output/figures/bertopic_heatmap.html")

# Document clusters
fig = topic_model.visualize_documents(texts)
fig.write_html("output/figures/bertopic_documents.html")

# Topic hierarchy
fig = topic_model.visualize_hierarchy()
fig.write_html("output/figures/bertopic_hierarchy.html")
```

### Topics Over Time

```python
import pandas as pd
from datetime import datetime, timedelta

# Sample with timestamps
dates = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(texts))]
timestamps = [d.strftime("%Y-%m") for d in dates]

# Dynamic topics
topics_over_time = topic_model.topics_over_time(
    texts,
    timestamps,
    nr_bins=12
)

# Visualize
fig = topic_model.visualize_topics_over_time(topics_over_time)
fig.write_html("output/figures/topics_over_time.html")
```

## pyLDAvis for Gensim

```python
import pyLDAvis
import pyLDAvis.gensim_models

# Prepare visualization data
vis_data = pyLDAvis.gensim_models.prepare(
    lda_model,
    corpus,
    dictionary,
    sort_topics=False
)

# Save as HTML
pyLDAvis.save_html(vis_data, 'output/figures/lda_vis.html')
```

## Validation

### Word Intrusion Test

```python
def generate_intrusion_test(model, num_topics=None, n_words=5):
    """Generate word intrusion test for topic validation."""
    if num_topics is None:
        num_topics = model.num_topics

    tests = []

    for topic_id in range(num_topics):
        # Get top words for this topic
        top_words = [w for w, _ in model.show_topic(topic_id, topn=n_words)]

        # Get intruder from different topic
        intruder_topic = (topic_id + 1) % num_topics
        intruder_words = [w for w, _ in model.show_topic(intruder_topic, topn=n_words)]
        intruder = random.choice(intruder_words)

        # Combine and shuffle
        all_words = top_words + [intruder]
        random.shuffle(all_words)

        tests.append({
            'topic': topic_id,
            'words': all_words,
            'intruder': intruder
        })

    return tests

tests = generate_intrusion_test(lda_model)
for test in tests[:3]:
    print(f"Topic {test['topic']}: {test['words']}")
    print(f"  (Intruder: {test['intruder']})\n")
```

### Robustness: Multiple Seeds

```python
def compare_seeds(corpus, dictionary, k, seeds):
    """Compare topic models across random seeds."""
    models = []

    for seed in seeds:
        model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=k,
            random_state=seed,
            passes=10
        )
        models.append(model)

    # Get top words for each model
    all_top_words = []
    for i, model in enumerate(models):
        topics = []
        for topic_id in range(k):
            words = [w for w, _ in model.show_topic(topic_id, topn=10)]
            topics.append(set(words))
        all_top_words.append(topics)

    return models, all_top_words

models, all_words = compare_seeds(corpus, dictionary, k=5, seeds=[42, 123, 456])
```

## Output: Publication Tables

### Topic Summary Table

```python
def create_topic_table(model, n_words=10):
    """Create publication-ready topic table."""
    topics = []

    for topic_id in range(model.num_topics):
        words = model.show_topic(topic_id, topn=n_words)
        word_str = ", ".join([w for w, _ in words])

        topics.append({
            'Topic': topic_id + 1,
            'Top Words': word_str
        })

    return pd.DataFrame(topics)

topic_table = create_topic_table(lda_model)
topic_table.to_csv('output/tables/topic_summary.csv', index=False)
print(topic_table)
```

### Document-Topic Table

```python
def create_doc_topic_table(model, corpus, texts, n_docs=5):
    """Create document-topic assignments table."""
    results = []

    for i, (doc, text) in enumerate(zip(corpus, texts)):
        topic_dist = model.get_document_topics(doc)
        dominant = max(topic_dist, key=lambda x: x[1])

        results.append({
            'doc_id': i,
            'text_preview': text[:100],
            'dominant_topic': dominant[0] + 1,
            'probability': dominant[1]
        })

    df = pd.DataFrame(results)

    # Sample top docs per topic
    sample = df.groupby('dominant_topic').apply(
        lambda x: x.nlargest(n_docs, 'probability')
    ).reset_index(drop=True)

    return sample

doc_table = create_doc_topic_table(lda_model, corpus, texts)
```

## Complete Workflow

```python
class TopicModelPipeline:
    """Complete topic modeling pipeline."""

    def __init__(self, method='lda'):
        self.method = method
        self.model = None
        self.dictionary = None
        self.corpus = None

    def preprocess(self, texts):
        """Preprocess texts."""
        processed = [preprocess(t) for t in texts]
        return processed

    def fit_lda(self, texts, k=10, seed=42):
        """Fit LDA model."""
        processed = self.preprocess(texts)

        self.dictionary = corpora.Dictionary(processed)
        self.dictionary.filter_extremes(no_below=5, no_above=0.5)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in processed]

        self.model = LdaModel(
            corpus=self.corpus,
            id2word=self.dictionary,
            num_topics=k,
            random_state=seed,
            passes=15
        )

        # Calculate coherence
        coherence = CoherenceModel(
            model=self.model,
            texts=processed,
            dictionary=self.dictionary,
            coherence='c_v'
        ).get_coherence()

        return {'model': self.model, 'coherence': coherence}

    def fit_bertopic(self, texts, min_topic_size=10):
        """Fit BERTopic model."""
        self.model = BERTopic(
            min_topic_size=min_topic_size,
            verbose=True
        )
        topics, probs = self.model.fit_transform(texts)
        return {'model': self.model, 'topics': topics, 'probs': probs}

    def get_topics(self, n_words=10):
        """Get topic-word distributions."""
        if self.method == 'lda':
            return create_topic_table(self.model, n_words)
        else:
            return self.model.get_topic_info()

    def save(self, path):
        """Save model."""
        if self.method == 'lda':
            self.model.save(f"{path}/lda_model")
            self.dictionary.save(f"{path}/dictionary")
        else:
            self.model.save(f"{path}/bertopic_model")

# Usage
pipeline = TopicModelPipeline(method='lda')
result = pipeline.fit_lda(texts, k=5, seed=42)
print(f"Coherence: {result['coherence']:.4f}")
print(pipeline.get_topics())
```
