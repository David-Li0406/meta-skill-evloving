# Word and Document Embeddings

## Overview

Embeddings represent words or documents as dense vectors in continuous space. Unlike bag-of-words (sparse, high-dimensional), embeddings are dense (100-1000 dimensions) and capture semantic relationships.

## Key Concepts

### The Distributional Hypothesis

"You shall know a word by the company it keeps." — J.R. Firth

Words appearing in similar contexts have similar meanings. Embeddings operationalize this: similar words have similar vectors.

### Vector Properties

**Similarity:**
```
cosine_similarity(king, queen) > cosine_similarity(king, apple)
```

**Analogies:**
```
king - man + woman ≈ queen
```

**Clustering:**
Words form semantic clusters in embedding space.

## Types of Embeddings

### Word2Vec

**Training objective:** Predict word from context (CBOW) or context from word (Skip-gram).

**Output:** One vector per word type (not token).

**Limitations:**
- One vector per word (ignores polysemy)
- No subword information
- Context window is fixed

### GloVe

**Training objective:** Factorize word co-occurrence matrix.

**Output:** Similar to Word2Vec; often comparable performance.

**Trade-off:** Global statistics vs. local context windows.

### FastText

**Extension of Word2Vec:** Includes subword (character n-gram) information.

**Advantage:** Can handle out-of-vocabulary words and morphological variants.

**Example:**
```
"unhappiness" → embeddings for "un", "hap", "app", "ppi", "ness", etc.
```

### Sentence Transformers (SBERT)

**Based on BERT:** Produces single vector for entire sentence/document.

**Training:** Fine-tuned for sentence similarity tasks.

**Advantage:** Semantically meaningful sentence-level embeddings.

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["This is a sentence.", "This is another."])
```

### BERT and Contextual Embeddings

**Key difference:** One vector per word *token*, not type. The vector for "bank" differs in "river bank" vs. "bank account".

**Layers:** BERT has multiple layers; different layers capture different information.

**Using BERT embeddings:**
- Average token embeddings for document vector
- Use [CLS] token representation
- Fine-tune for specific task

## When to Use Each

| Embedding | Best For | Considerations |
|-----------|----------|----------------|
| **Word2Vec/GloVe** | Semantic similarity, analogies | Fast, interpretable |
| **FastText** | Morphologically rich languages, rare words | Handles OOV |
| **SBERT** | Document similarity, clustering, retrieval | Best for sentence-level |
| **BERT** | Classification, NER, complex NLU | Requires fine-tuning |

## Document Embeddings

### Simple Aggregation

```
doc_vector = mean(word_vectors for word in document)
```

**Pros:** Simple, fast, interpretable
**Cons:** Ignores word order, importance

### TF-IDF Weighted Average

```
doc_vector = Σ (tf-idf_weight × word_vector) / Σ tf-idf_weight
```

**Improvement:** Downweights common words.

### Doc2Vec / Paragraph Vectors

**Approach:** Learn document vectors alongside word vectors.

**Variants:**
- PV-DM: Distributed Memory (like CBOW + doc vector)
- PV-DBOW: Distributed Bag of Words (like Skip-gram)

### Sentence Transformers (Recommended)

Best current approach for document embeddings:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
doc_embeddings = model.encode(documents)
```

## Applications

### 1. Document Similarity

Find similar documents:

```python
from sklearn.metrics.pairwise import cosine_similarity

# Get embeddings
embeddings = model.encode(documents)

# Find most similar to document 0
similarities = cosine_similarity([embeddings[0]], embeddings)[0]
most_similar = similarities.argsort()[-5:][::-1]  # Top 5
```

### 2. Semantic Search

Find documents matching a query:

```python
query_embedding = model.encode(["What is climate change?"])
doc_embeddings = model.encode(documents)
similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
top_results = similarities.argsort()[-10:][::-1]
```

### 3. Clustering

Group similar documents:

```python
from sklearn.cluster import KMeans

embeddings = model.encode(documents)
clusters = KMeans(n_clusters=10).fit_predict(embeddings)
```

### 4. Dimensionality Reduction + Visualization

```python
from sklearn.manifold import TSNE

embeddings_2d = TSNE(n_components=2).fit_transform(embeddings)
# Plot with matplotlib
```

### 5. Feature Input for Classification

Use embeddings as features for downstream tasks:

```python
embeddings = model.encode(documents)
clf = LogisticRegression()
clf.fit(embeddings, labels)
```

## Pretrained vs. Training Your Own

### Use Pretrained When:
- General domain (news, social media, common language)
- Limited computational resources
- Limited training data

### Train Your Own When:
- Highly specialized domain (medical, legal, technical)
- Domain-specific vocabulary
- Large in-domain corpus available

### Fine-Tuning Pretrained:
- Middle ground: start with pretrained, adjust for domain
- Requires labeled data for the fine-tuning task

## Evaluation

### Intrinsic Evaluation

**Word similarity:** Correlate embedding similarity with human judgments (WordSim-353, SimLex-999).

**Analogy completion:** "king - man + woman = ?" should yield "queen".

### Extrinsic Evaluation

**Downstream task performance:** How well do embeddings work for your actual task (classification, clustering, retrieval)?

**This is what matters for research applications.**

## Common Issues

### Out-of-Vocabulary (OOV) Words

**Problem:** Word not in vocabulary → no embedding.

**Solutions:**
| Approach | Implementation |
|----------|----------------|
| FastText | Subword embeddings handle OOV |
| BERT | Subword tokenization handles OOV |
| Replace with `<UNK>` | Use unknown token vector |
| Skip OOV | Ignore in averaging |

### Polysemy

**Problem:** "Bank" has different meanings.

**Solution:** Use contextual embeddings (BERT) that produce different vectors based on context.

### Bias in Embeddings

**Problem:** Embeddings reflect biases in training data.

**Example:** "man : doctor :: woman : nurse" analogy may emerge.

**Awareness:** Document potential biases; consider debiasing for sensitive applications.

### Dimensionality

**Typical dimensions:**
- Word2Vec/GloVe: 50-300
- FastText: 100-300
- BERT: 768 (base) or 1024 (large)
- SBERT: 384-768

**Trade-off:** Higher dimensions capture more; but may overfit with small data.

## Practical Recommendations

### For Research Projects

1. **Start with pretrained SBERT** (`all-mpnet-base-v2` or `all-MiniLM-L6-v2`)
2. **Check domain fit:** Does similarity make sense for your texts?
3. **Compare to TF-IDF baseline:** Embeddings should outperform
4. **Report model and version** for reproducibility

### Model Selection

```
Is your task sentence/document-level?
  Yes → Use Sentence Transformers
  No (word-level) → Continue

Do you need to handle rare/technical words?
  Yes → FastText or BERT
  No → Word2Vec or GloVe

Is computational cost a concern?
  Yes → Word2Vec, GloVe, or small SBERT
  No → BERT or large SBERT

Do you need contextual disambiguation?
  Yes → BERT embeddings
  No → Static embeddings are fine
```

## Reporting Standards

### Methods Section

```markdown
We represented documents using [model name] (Author, Year).
[For pretrained: Model trained on X corpus.]
[For fine-tuned: We fine-tuned on Y task with Z examples.]

Document vectors were computed by [averaging word vectors /
using sentence transformer / etc.].

Embeddings were used for [similarity calculation /
classification features / clustering / etc.].
```

### Reproducibility

Report:
- Model name and version
- Source (HuggingFace, gensim, etc.)
- Preprocessing before embedding
- Any fine-tuning details
- Similarity metric used (cosine, Euclidean)

## Code Examples

### Word2Vec with gensim

```python
from gensim.models import Word2Vec

# Train
sentences = [doc.split() for doc in documents]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=5)

# Get word vector
vector = model.wv['example']

# Find similar words
similar = model.wv.most_similar('example', topn=10)
```

### Sentence Transformers

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(documents)

# Similarity matrix
sim_matrix = cosine_similarity(embeddings)
```

### Using Pretrained GloVe

```python
import numpy as np

# Load pretrained
embeddings_index = {}
with open('glove.6B.100d.txt') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.array(values[1:], dtype='float32')
        embeddings_index[word] = vector

# Get document vector (average)
def doc_vector(text, embeddings_index):
    words = text.lower().split()
    vectors = [embeddings_index[w] for w in words if w in embeddings_index]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)
```
