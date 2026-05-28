# Word and Document Embeddings in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# text2vec 0.6.3
# word2vec 0.3.4
# tidyverse 2.0.0
```

## Installation

```r
install.packages(c("text2vec", "word2vec", "tidyverse", "umap", "Rtsne"))
```

## Word2Vec with word2vec Package

### Training Word2Vec

```r
library(word2vec)
library(tidyverse)

# Sample corpus
texts <- c(
  "The economy shows signs of growth with increased employment.",
  "Healthcare reform remains a divisive political issue.",
  "Climate change impacts are becoming more severe.",
  "Education funding varies widely across states.",
  "Machine learning is transforming data analysis.",
  "Social media influences political discourse."
)

# Save as file (required by word2vec)
writeLines(texts, "temp_corpus.txt")

# Train model
w2v_model <- word2vec(
  x = "temp_corpus.txt",
  type = "skip-gram",  # or "cbow"
  dim = 100,           # Embedding dimensions
  window = 5,          # Context window
  iter = 5,            # Epochs
  min_count = 1,       # Minimum word frequency
  threads = 4
)

# Clean up
file.remove("temp_corpus.txt")
```

### Using Word2Vec

```r
# Get word vector
word_vector <- predict(w2v_model, "economy", type = "embedding")

# Find similar words
similar <- predict(w2v_model, "economy", type = "nearest", top_n = 10)
print(similar)

# Word analogies
# Note: requires large corpus to work well
# predict(w2v_model, c("king", "woman", "man"), type = "nearest")

# Get all embeddings as matrix
embeddings_matrix <- as.matrix(w2v_model)
dim(embeddings_matrix)
```

### Document Embeddings (Average)

```r
# Average word vectors for document
get_doc_embedding <- function(text, model) {
  words <- tolower(strsplit(text, "\\s+")[[1]])
  words <- words[words %in% rownames(as.matrix(model))]

  if (length(words) == 0) return(rep(0, dim(as.matrix(model))[2]))

  embeddings <- predict(model, words, type = "embedding")
  if (is.vector(embeddings)) embeddings <- matrix(embeddings, nrow = 1)

  colMeans(embeddings)
}

# Apply to corpus
doc_embeddings <- t(sapply(texts, function(t) get_doc_embedding(t, w2v_model)))
rownames(doc_embeddings) <- paste0("doc_", 1:length(texts))
```

## GloVe with text2vec

### Preparing Data

```r
library(text2vec)

# Create iterator
tokens <- space_tokenizer(tolower(texts))
it <- itoken(tokens, progressbar = FALSE)

# Create vocabulary
vocab <- create_vocabulary(it)

# Prune vocabulary
vocab <- prune_vocabulary(vocab, term_count_min = 1)

# Create term co-occurrence matrix
vectorizer <- vocab_vectorizer(vocab)
tcm <- create_tcm(it, vectorizer, skip_grams_window = 5)
```

### Training GloVe

```r
# Initialize GloVe model
glove <- GlobalVectors$new(rank = 50, x_max = 10)

# Fit (returns word vectors)
wv_main <- glove$fit_transform(tcm, n_iter = 100, n_threads = 4)

# Get context vectors
wv_context <- glove$components

# Combine (often improves quality)
word_vectors <- wv_main + t(wv_context)
```

### Using GloVe Embeddings

```r
# Similar words
find_similar <- function(word, word_vectors, top_n = 10) {
  if (!word %in% rownames(word_vectors)) {
    return(paste("Word not in vocabulary:", word))
  }

  vec <- word_vectors[word, , drop = FALSE]

  # Cosine similarity
  cos_sim <- sim2(x = word_vectors, y = vec, method = "cosine", norm = "l2")

  # Sort and return top N
  head(sort(cos_sim[, 1], decreasing = TRUE), top_n)
}

find_similar("economy", word_vectors)
```

## Using Pretrained Embeddings

### Loading GloVe

```r
# Download from https://nlp.stanford.edu/projects/glove/
# Example with GloVe 6B 100d

load_glove <- function(path, nrow = Inf) {
  lines <- readLines(path, n = nrow, encoding = "UTF-8")

  word_vectors <- map_dfr(lines, function(line) {
    parts <- strsplit(line, " ")[[1]]
    word <- parts[1]
    vector <- as.numeric(parts[-1])
    tibble(word = word, !!!set_names(vector, paste0("V", seq_along(vector))))
  })

  matrix_out <- as.matrix(word_vectors[, -1])
  rownames(matrix_out) <- word_vectors$word

  matrix_out
}

# Usage (if you have the file)
# glove <- load_glove("glove.6B.100d.txt", nrow = 50000)
```

### Document Embeddings with Pretrained

```r
get_doc_embedding_pretrained <- function(text, embeddings, dim = 100) {
  words <- tolower(strsplit(text, "\\s+")[[1]])
  words <- words[words %in% rownames(embeddings)]

  if (length(words) == 0) return(rep(0, dim))

  word_vecs <- embeddings[words, , drop = FALSE]
  colMeans(word_vecs)
}

# Apply to corpus
# doc_embeddings <- t(sapply(texts, function(t)
#   get_doc_embedding_pretrained(t, glove)))
```

## Document Similarity

### Cosine Similarity

```r
library(text2vec)

# Calculate pairwise similarities
doc_sim_matrix <- sim2(doc_embeddings, method = "cosine", norm = "l2")

# Find most similar documents
find_similar_docs <- function(doc_idx, sim_matrix, top_n = 5) {
  sims <- sim_matrix[doc_idx, ]
  sims[doc_idx] <- -Inf  # Exclude self

  top_idx <- order(sims, decreasing = TRUE)[1:top_n]

  tibble(
    similar_doc = top_idx,
    similarity = sims[top_idx]
  )
}

find_similar_docs(1, doc_sim_matrix)
```

### Semantic Search

```r
semantic_search <- function(query, doc_embeddings, model, top_n = 5) {
  query_embedding <- get_doc_embedding(query, model)

  similarities <- sim2(
    doc_embeddings,
    matrix(query_embedding, nrow = 1),
    method = "cosine"
  )[, 1]

  top_idx <- order(similarities, decreasing = TRUE)[1:top_n]

  tibble(
    rank = 1:top_n,
    doc_id = top_idx,
    similarity = similarities[top_idx]
  )
}

# Usage
semantic_search("economic growth", doc_embeddings, w2v_model)
```

## Dimensionality Reduction & Visualization

### t-SNE

```r
library(Rtsne)

# Reduce dimensions
set.seed(42)
tsne_result <- Rtsne(doc_embeddings, dims = 2, perplexity = min(5, nrow(doc_embeddings) - 1))

# Visualize
tsne_df <- tibble(
  doc_id = 1:nrow(doc_embeddings),
  x = tsne_result$Y[, 1],
  y = tsne_result$Y[, 2]
)

ggplot(tsne_df, aes(x = x, y = y, label = doc_id)) +
  geom_point() +
  geom_text(nudge_y = 0.5) +
  labs(title = "Document Embeddings (t-SNE)") +
  theme_minimal()
```

### UMAP

```r
library(umap)

# Reduce dimensions
set.seed(42)
umap_result <- umap(doc_embeddings)

# Visualize
umap_df <- tibble(
  doc_id = 1:nrow(doc_embeddings),
  x = umap_result$layout[, 1],
  y = umap_result$layout[, 2]
)

ggplot(umap_df, aes(x = x, y = y, label = doc_id)) +
  geom_point() +
  geom_text(nudge_y = 0.1) +
  labs(title = "Document Embeddings (UMAP)") +
  theme_minimal()
```

## Clustering with Embeddings

```r
library(stats)

# K-means clustering
set.seed(42)
k <- 3
clusters <- kmeans(doc_embeddings, centers = k)

# Add to visualization
tsne_df$cluster <- factor(clusters$cluster)

ggplot(tsne_df, aes(x = x, y = y, color = cluster)) +
  geom_point(size = 3) +
  labs(title = "Document Clusters (t-SNE + K-means)") +
  theme_minimal()
```

## Embeddings as Features for Classification

```r
library(tidymodels)

# Prepare data with embeddings
texts_df <- tibble(
  doc_id = 1:length(texts),
  text = texts,
  label = factor(c("economy", "politics", "climate", "education", "tech", "politics"))
)

# Add embedding features
embedding_features <- as_tibble(doc_embeddings, .name_repair = "unique")
names(embedding_features) <- paste0("emb_", 1:ncol(doc_embeddings))

texts_with_embeddings <- bind_cols(texts_df, embedding_features)

# Classification recipe (no text processing needed)
emb_recipe <- recipe(label ~ ., data = texts_with_embeddings) %>%
  update_role(doc_id, text, new_role = "id")

# Model
rf_spec <- rand_forest(trees = 500) %>%
  set_engine("ranger") %>%
  set_mode("classification")

# Workflow
emb_workflow <- workflow() %>%
  add_recipe(emb_recipe) %>%
  add_model(rf_spec)

# Fit (would need more data for real use)
# emb_fit <- emb_workflow %>% fit(data = texts_with_embeddings)
```

## TF-IDF Weighted Embeddings

```r
library(tidytext)

# Get TF-IDF weights
tfidf_weights <- tibble(text = texts, doc_id = 1:length(texts)) %>%
  unnest_tokens(word, text) %>%
  count(doc_id, word) %>%
  bind_tf_idf(word, doc_id, n)

# Weighted document embeddings
get_weighted_doc_embedding <- function(doc_id, tfidf_df, model) {
  doc_words <- tfidf_df %>%
    filter(doc_id == !!doc_id)

  valid_words <- doc_words %>%
    filter(word %in% rownames(as.matrix(model)))

  if (nrow(valid_words) == 0) return(rep(0, ncol(as.matrix(model))))

  word_vecs <- predict(model, valid_words$word, type = "embedding")
  if (is.vector(word_vecs)) word_vecs <- matrix(word_vecs, nrow = 1)

  # Weighted average
  weighted_sum <- colSums(word_vecs * valid_words$tf_idf)
  weighted_sum / sum(valid_words$tf_idf)
}

# Apply
weighted_doc_emb <- t(sapply(1:length(texts), function(i)
  get_weighted_doc_embedding(i, tfidf_weights, w2v_model)))
```

## Complete Workflow

```r
#' Embedding Pipeline
#' @param texts Character vector of documents
#' @param dim Embedding dimensions
#' @param method "word2vec" or "glove"
#' @return List with model and document embeddings

embedding_pipeline <- function(texts, dim = 100, method = "word2vec") {

  if (method == "word2vec") {
    # Train word2vec
    writeLines(texts, "temp_corpus.txt")
    model <- word2vec(
      x = "temp_corpus.txt",
      type = "skip-gram",
      dim = dim,
      window = 5,
      iter = 5,
      min_count = 1
    )
    file.remove("temp_corpus.txt")

    # Document embeddings
    doc_emb <- t(sapply(texts, function(t) {
      get_doc_embedding(t, model)
    }))

  } else if (method == "glove") {
    # Train GloVe
    tokens <- space_tokenizer(tolower(texts))
    it <- itoken(tokens, progressbar = FALSE)
    vocab <- create_vocabulary(it)
    vectorizer <- vocab_vectorizer(vocab)
    tcm <- create_tcm(it, vectorizer, skip_grams_window = 5)

    glove <- GlobalVectors$new(rank = dim, x_max = 10)
    wv_main <- glove$fit_transform(tcm, n_iter = 100)
    model <- wv_main + t(glove$components)

    # Document embeddings
    doc_emb <- t(sapply(texts, function(t) {
      words <- strsplit(tolower(t), "\\s+")[[1]]
      words <- words[words %in% rownames(model)]
      if (length(words) == 0) return(rep(0, dim))
      colMeans(model[words, , drop = FALSE])
    }))
  }

  rownames(doc_emb) <- paste0("doc_", 1:length(texts))

  list(
    model = model,
    doc_embeddings = doc_emb
  )
}

# Usage
results <- embedding_pipeline(texts, dim = 50, method = "word2vec")
print(dim(results$doc_embeddings))
```
