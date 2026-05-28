# Word and Document Embeddings in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# gensim 4.3.1
# sentence-transformers 2.2.2
# numpy 1.24.0
```

## Installation

```bash
pip install gensim sentence-transformers numpy pandas scikit-learn umap-learn

# For visualization
pip install matplotlib plotly
```

## Word2Vec with Gensim

### Training Word2Vec

```python
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np

# Sample corpus
texts = [
    "The economy shows signs of growth with increased employment.",
    "Healthcare reform remains a divisive political issue.",
    "Climate change impacts are becoming more severe.",
    "Education funding varies widely across states.",
    "Machine learning is transforming data analysis.",
    "Social media influences political discourse."
] * 20  # Need more data for meaningful embeddings

# Tokenize
tokenized = [simple_preprocess(text) for text in texts]

# Train Word2Vec
model = Word2Vec(
    sentences=tokenized,
    vector_size=100,    # Embedding dimensions
    window=5,           # Context window
    min_count=2,        # Minimum word frequency
    workers=4,          # Parallel threads
    epochs=10,          # Training epochs
    seed=42
)

print(f"Vocabulary size: {len(model.wv)}")
```

### Using Word2Vec

```python
# Get word vector
vector = model.wv['economy']
print(f"Shape: {vector.shape}")

# Find similar words
similar = model.wv.most_similar('economy', topn=10)
print("Similar to 'economy':")
for word, score in similar:
    print(f"  {word}: {score:.3f}")

# Word analogies (need larger corpus for good results)
# result = model.wv.most_similar(positive=['woman', 'king'], negative=['man'])

# Check if word in vocabulary
print(f"'economy' in vocab: {'economy' in model.wv}")
```

### Document Embeddings (Average)

```python
def get_doc_embedding(text, model, dim=100):
    """Average word vectors for document embedding."""
    words = simple_preprocess(text)
    word_vecs = []

    for word in words:
        if word in model.wv:
            word_vecs.append(model.wv[word])

    if not word_vecs:
        return np.zeros(dim)

    return np.mean(word_vecs, axis=0)

# Get embeddings for all documents
doc_embeddings = np.array([get_doc_embedding(text, model) for text in texts])
print(f"Document embeddings shape: {doc_embeddings.shape}")
```

### Save and Load

```python
# Save
model.save("models/word2vec.model")

# Load
loaded_model = Word2Vec.load("models/word2vec.model")
```

## Sentence Transformers (Recommended)

### Basic Usage

```python
from sentence_transformers import SentenceTransformer

# Load pretrained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode texts
embeddings = model.encode(texts, show_progress_bar=True)
print(f"Embeddings shape: {embeddings.shape}")
# (N documents, 384 dimensions)

# Encode single text
single_embedding = model.encode("This is a test sentence.")
print(f"Single embedding shape: {single_embedding.shape}")
```

### Model Options

```python
# Different models for different needs

# Fast and good (recommended default)
model_fast = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dims

# Higher quality
model_quality = SentenceTransformer('all-mpnet-base-v2')  # 768 dims

# Multilingual
model_multi = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Semantic search optimized
model_search = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
```

### Batch Processing

```python
# For large corpora
def encode_batched(texts, model, batch_size=32):
    """Encode texts in batches."""
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings

embeddings = encode_batched(texts, model)
```

## Document Similarity

### Cosine Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

# Compute pairwise similarities
sim_matrix = cosine_similarity(embeddings)

# Find most similar documents
def find_similar_docs(doc_idx, sim_matrix, texts, top_n=5):
    """Find most similar documents."""
    sims = sim_matrix[doc_idx].copy()
    sims[doc_idx] = -1  # Exclude self

    top_idx = np.argsort(sims)[-top_n:][::-1]

    results = []
    for idx in top_idx:
        results.append({
            'doc_id': idx,
            'similarity': sims[idx],
            'text': texts[idx][:100]
        })

    return results

similar = find_similar_docs(0, sim_matrix, texts)
print("Documents similar to doc 0:")
for r in similar:
    print(f"  Doc {r['doc_id']} (sim={r['similarity']:.3f}): {r['text'][:50]}...")
```

### Semantic Search

```python
def semantic_search(query, doc_embeddings, texts, model, top_n=5):
    """Search documents by semantic similarity to query."""
    query_embedding = model.encode([query])

    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    top_idx = np.argsort(similarities)[-top_n:][::-1]

    results = []
    for idx in top_idx:
        results.append({
            'rank': len(results) + 1,
            'doc_id': idx,
            'similarity': similarities[idx],
            'text': texts[idx][:150]
        })

    return results

# Search
results = semantic_search(
    "economic growth and jobs",
    embeddings,
    texts,
    model
)

print("Search results for 'economic growth and jobs':")
for r in results:
    print(f"  #{r['rank']} (sim={r['similarity']:.3f}): {r['text'][:60]}...")
```

## Clustering with Embeddings

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# K-means clustering
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(embeddings)

# Silhouette score
silhouette = silhouette_score(embeddings, clusters)
print(f"Silhouette score: {silhouette:.3f}")

# Cluster distribution
import pandas as pd
cluster_df = pd.DataFrame({
    'text': [t[:50] for t in texts],
    'cluster': clusters
})
print(cluster_df['cluster'].value_counts())
```

## Dimensionality Reduction

### UMAP

```python
from umap import UMAP
import matplotlib.pyplot as plt

# Reduce to 2D
umap_model = UMAP(
    n_neighbors=15,
    n_components=2,
    min_dist=0.1,
    metric='cosine',
    random_state=42
)

embeddings_2d = umap_model.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 8))
scatter = plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=clusters,
    cmap='viridis',
    alpha=0.7
)
plt.colorbar(scatter, label='Cluster')
plt.title('Document Embeddings (UMAP)')
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.savefig('output/figures/embeddings_umap.png', dpi=300)
plt.close()
```

### t-SNE

```python
from sklearn.manifold import TSNE

# Reduce to 2D
tsne = TSNE(
    n_components=2,
    perplexity=min(30, len(embeddings) - 1),
    random_state=42
)

embeddings_tsne = tsne.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 8))
plt.scatter(
    embeddings_tsne[:, 0],
    embeddings_tsne[:, 1],
    c=clusters,
    cmap='viridis',
    alpha=0.7
)
plt.title('Document Embeddings (t-SNE)')
plt.savefig('output/figures/embeddings_tsne.png', dpi=300)
plt.close()
```

## TF-IDF Weighted Embeddings

```python
from sklearn.feature_extraction.text import TfidfVectorizer

def get_tfidf_weighted_embedding(text, word_model, tfidf_vectorizer, tfidf_matrix, doc_idx):
    """Get TF-IDF weighted document embedding."""
    words = simple_preprocess(text)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Get TF-IDF weights for this document
    tfidf_weights = tfidf_matrix[doc_idx].toarray().flatten()

    weighted_vecs = []
    weights = []

    for word in words:
        if word in word_model.wv and word in feature_names:
            word_idx = np.where(feature_names == word)[0][0]
            weight = tfidf_weights[word_idx]

            weighted_vecs.append(word_model.wv[word] * weight)
            weights.append(weight)

    if not weighted_vecs:
        return np.zeros(word_model.vector_size)

    return np.sum(weighted_vecs, axis=0) / sum(weights)

# Create TF-IDF
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(texts)

# Get weighted embeddings
weighted_embeddings = np.array([
    get_tfidf_weighted_embedding(text, model, tfidf, tfidf_matrix, i)
    for i, text in enumerate(texts)
])
```

## Using Pretrained GloVe

```python
def load_glove(path, dim=100):
    """Load pretrained GloVe embeddings."""
    embeddings = {}

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype='float32')
            embeddings[word] = vector

    print(f"Loaded {len(embeddings)} word vectors")
    return embeddings

# Usage (if you have GloVe file)
# glove = load_glove('glove.6B.100d.txt')

def get_glove_doc_embedding(text, glove, dim=100):
    """Get document embedding using GloVe."""
    words = simple_preprocess(text)
    word_vecs = [glove[w] for w in words if w in glove]

    if not word_vecs:
        return np.zeros(dim)

    return np.mean(word_vecs, axis=0)
```

## Embeddings as Classification Features

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Prepare data
labels = ["economy", "politics", "climate", "education", "tech", "politics"] * 20

# Use sentence transformer embeddings
model_st = SentenceTransformer('all-MiniLM-L6-v2')
X_embeddings = model_st.encode(texts)

# Train classifier
clf = LogisticRegression(max_iter=1000, random_state=42)

# Cross-validation
scores = cross_val_score(clf, X_embeddings, labels, cv=5, scoring='f1_macro')
print(f"F1-macro: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

# Fit on all data
clf.fit(X_embeddings, labels)

# Predict new text
new_text = "The stock market saw significant gains today"
new_embedding = model_st.encode([new_text])
prediction = clf.predict(new_embedding)
print(f"Predicted: {prediction[0]}")
```

## Complete Embedding Pipeline

```python
class EmbeddingPipeline:
    """Complete embedding pipeline."""

    def __init__(self, method='sentence-transformer', model_name='all-MiniLM-L6-v2'):
        self.method = method
        self.model_name = model_name
        self.model = None
        self.embeddings = None

    def fit(self, texts):
        """Fit/compute embeddings."""
        if self.method == 'sentence-transformer':
            self.model = SentenceTransformer(self.model_name)
            self.embeddings = self.model.encode(texts, show_progress_bar=True)

        elif self.method == 'word2vec':
            tokenized = [simple_preprocess(t) for t in texts]
            self.model = Word2Vec(
                sentences=tokenized,
                vector_size=100,
                window=5,
                min_count=2,
                epochs=10,
                seed=42
            )
            self.embeddings = np.array([
                get_doc_embedding(t, self.model) for t in texts
            ])

        return self

    def transform(self, texts):
        """Transform new texts."""
        if self.method == 'sentence-transformer':
            return self.model.encode(texts)
        elif self.method == 'word2vec':
            return np.array([get_doc_embedding(t, self.model) for t in texts])

    def similarity_matrix(self):
        """Compute similarity matrix."""
        return cosine_similarity(self.embeddings)

    def search(self, query, texts, top_n=5):
        """Semantic search."""
        query_emb = self.transform([query])
        sims = cosine_similarity(query_emb, self.embeddings)[0]
        top_idx = np.argsort(sims)[-top_n:][::-1]

        return [{'idx': i, 'sim': sims[i], 'text': texts[i][:100]}
                for i in top_idx]

    def cluster(self, n_clusters=5):
        """Cluster documents."""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        return kmeans.fit_predict(self.embeddings)

    def reduce_dims(self, method='umap', n_components=2):
        """Reduce dimensionality."""
        if method == 'umap':
            reducer = UMAP(n_components=n_components, random_state=42)
        else:
            reducer = TSNE(n_components=n_components, random_state=42)

        return reducer.fit_transform(self.embeddings)

# Usage
pipeline = EmbeddingPipeline(method='sentence-transformer')
pipeline.fit(texts)

# Search
results = pipeline.search("economic growth", texts)
for r in results:
    print(f"Doc {r['idx']} (sim={r['sim']:.3f}): {r['text'][:50]}...")

# Cluster
clusters = pipeline.cluster(n_clusters=4)
print(f"Cluster distribution: {np.bincount(clusters)}")

# Visualize
coords = pipeline.reduce_dims(method='umap')
plt.scatter(coords[:, 0], coords[:, 1], c=clusters)
plt.savefig('output/figures/embedding_clusters.png', dpi=300)
plt.close()
```
