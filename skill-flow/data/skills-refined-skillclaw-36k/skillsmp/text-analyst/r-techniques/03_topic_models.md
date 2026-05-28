# Topic Models in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# stm 1.3.6.1
# topicmodels 0.2-14
# tidytext 0.4.1
# quanteda 3.3.1
```

## Installation

```r
install.packages(c("stm", "topicmodels", "tidytext", "quanteda", "LDAvis"))
```

## Structural Topic Model (STM) - Recommended

### Why STM?

- Topic prevalence can vary by covariates
- Topic content can vary by covariates
- Better diagnostics (coherence + exclusivity)
- Spectral initialization (more stable)
- Correlation between topics modeled

### Basic STM Workflow

```r
library(stm)
library(tidyverse)

# Sample data with covariates
texts <- tibble(
  doc_id = 1:100,
  text = sample(c(
    "The economy shows signs of growth with increased employment.",
    "Healthcare reform remains a divisive political issue.",
    "Climate change impacts are becoming more severe.",
    "Education funding varies widely across states."
  ), 100, replace = TRUE),
  year = sample(2015:2022, 100, replace = TRUE),
  source = sample(c("conservative", "liberal"), 100, replace = TRUE)
)

# Prepare data for STM
processed <- textProcessor(
  documents = texts$text,
  metadata = texts,
  lowercase = TRUE,
  removestopwords = TRUE,
  removenumbers = TRUE,
  removepunctuation = TRUE,
  stem = TRUE
)

# Prepare documents
out <- prepDocuments(
  processed$documents,
  processed$vocab,
  processed$meta,
  lower.thresh = 5  # Min word frequency
)

# Check removed
out$docs.removed  # Documents removed
out$words.removed # Words removed
```

### Fitting STM

```r
# Basic STM (no covariates)
stm_basic <- stm(
  documents = out$documents,
  vocab = out$vocab,
  K = 10,
  data = out$meta,
  init.type = "Spectral",
  seed = 42
)

# STM with prevalence covariates
stm_prevalence <- stm(
  documents = out$documents,
  vocab = out$vocab,
  K = 10,
  prevalence = ~ year + source,
  data = out$meta,
  init.type = "Spectral",
  seed = 42
)

# STM with content covariates
stm_content <- stm(
  documents = out$documents,
  vocab = out$vocab,
  K = 10,
  prevalence = ~ year + source,
  content = ~ source,
  data = out$meta,
  init.type = "Spectral",
  seed = 42
)
```

### Examining Topics

```r
# Top words per topic (various weightings)
labelTopics(stm_prevalence, n = 10)

# Highest Prob: Most probable words
# FREX: Frequent and Exclusive (good for labeling)
# Lift: Words weighted by exclusivity
# Score: Combined measure

# Get as data frame
topic_words <- tidy(stm_prevalence, matrix = "beta")

# Top FREX words per topic
frex_words <- labelTopics(stm_prevalence, n = 10)$frex
```

### Representative Documents

```r
# Find documents most associated with each topic
findThoughts(stm_prevalence,
             texts = texts$text,
             n = 3,           # Documents per topic
             topics = 1:10)   # Which topics

# Plot document-topic associations
plot(stm_prevalence, type = "summary", n = 5)
```

### Topic Prevalence Over Time

```r
# Estimate effect of year on topic prevalence
effect <- estimateEffect(1:10 ~ year + source,
                        stm_prevalence,
                        meta = out$meta)

# Summary
summary(effect, topics = 1)

# Plot effect of year on topic 1
plot(effect, covariate = "year",
     topics = 1,
     method = "continuous",
     main = "Topic 1 Prevalence by Year")

# Plot effect of source (categorical)
plot(effect, covariate = "source",
     topics = 1:5,
     method = "difference",
     cov.value1 = "liberal",
     cov.value2 = "conservative",
     main = "Topic Prevalence: Liberal vs Conservative")
```

### Model Diagnostics

```r
# Coherence and exclusivity
exclusivity <- exclusivity(stm_prevalence)
coherence <- semanticCoherence(stm_prevalence, out$documents)

# Plot trade-off
tibble(
  topic = 1:10,
  coherence = coherence,
  exclusivity = exclusivity
) %>%
  ggplot(aes(x = coherence, y = exclusivity, label = topic)) +
  geom_point() +
  geom_text(nudge_y = 0.01) +
  labs(title = "Topic Quality: Coherence vs Exclusivity",
       x = "Semantic Coherence",
       y = "Exclusivity") +
  theme_minimal()
```

### Selecting K

```r
# Search over K values
k_search <- searchK(
  documents = out$documents,
  vocab = out$vocab,
  K = c(5, 10, 15, 20, 25),
  prevalence = ~ year + source,
  data = out$meta,
  init.type = "Spectral",
  seed = 42
)

# Plot diagnostics
plot(k_search)

# Access metrics
k_search$results
```

### Topic Correlation

```r
# Get topic correlations
topic_corr <- topicCorr(stm_prevalence)

# Plot as network
plot(topic_corr)
```

## LDA with topicmodels

For simpler topic modeling without covariates.

```r
library(topicmodels)
library(tidytext)

# Create document-term matrix
dtm <- texts %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words, by = "word") %>%
  count(doc_id, word) %>%
  cast_dtm(doc_id, word, n)

# Fit LDA
lda_model <- LDA(dtm, k = 10,
                 control = list(seed = 42))

# Extract topics
topics <- tidy(lda_model, matrix = "beta")

# Top words per topic
top_terms <- topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 10) %>%
  ungroup()

# Document-topic probabilities
doc_topics <- tidy(lda_model, matrix = "gamma")
```

### Visualizing LDA

```r
# Top terms visualization
top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered() +
  labs(title = "Top Terms per Topic",
       x = "Beta (word probability)",
       y = "Term") +
  theme_minimal()
```

## Validation

### Human Validation: Word Intrusion

```r
# Generate word intrusion test
generate_intrusion_test <- function(model, n_words = 5) {
  # Get top words per topic
  top_words <- labelTopics(model, n = n_words)$frex

  # For each topic, add intruder from another
  tests <- map(1:nrow(top_words), function(i) {
    topic_words <- top_words[i, ]
    # Get intruder from different topic
    intruder_topic <- sample(setdiff(1:nrow(top_words), i), 1)
    intruder <- sample(top_words[intruder_topic, ], 1)

    tibble(
      topic = i,
      words = list(c(topic_words, intruder)),
      intruder = intruder
    )
  })

  bind_rows(tests)
}

intrusion_test <- generate_intrusion_test(stm_prevalence)
```

### Robustness: Multiple Seeds

```r
# Run with multiple seeds
seeds <- c(42, 123, 456, 789, 1011)

multi_seed_stm <- map(seeds, function(s) {
  stm(
    documents = out$documents,
    vocab = out$vocab,
    K = 10,
    prevalence = ~ year + source,
    data = out$meta,
    init.type = "Spectral",
    seed = s,
    verbose = FALSE
  )
})

# Compare coherence across seeds
coherences <- map_dfc(multi_seed_stm, function(m) {
  semanticCoherence(m, out$documents)
})

# Check topic alignment across seeds
# (Topics may appear in different order)
```

## Output: Publication Tables

### Topic Summary Table

```r
create_topic_table <- function(model, n_words = 7) {
  # Get document-topic proportions
  theta <- make.dt(model)
  prevalence <- colMeans(theta)

  # Get top words
  top_words <- labelTopics(model, n = n_words)$frex

  tibble(
    Topic = 1:nrow(top_words),
    Prevalence = scales::percent(prevalence, accuracy = 0.1),
    `Top Words (FREX)` = apply(top_words, 1, paste, collapse = ", ")
  )
}

topic_table <- create_topic_table(stm_prevalence)

# Export
write_csv(topic_table, "output/tables/topic_summary.csv")
```

### Covariate Effects Table

```r
# Extract effects
effect_summary <- summary(effect, topics = 1:10)

# Format for publication
effect_table <- map_dfr(1:10, function(t) {
  est <- effect_summary$tables[[t]]
  tibble(
    Topic = t,
    Variable = rownames(est),
    Estimate = est[, "Estimate"],
    SE = est[, "Std. Error"],
    p_value = est[, "Pr(>|t|)"]
  )
})
```

## LDAvis Interactive Visualization

```r
library(LDAvis)

# For STM
toLDAvis(stm_prevalence, out$documents)

# For topicmodels LDA
library(LDAvis)
library(slam)

# Extract components
phi <- posterior(lda_model)$terms
theta <- posterior(lda_model)$topics
vocab <- colnames(phi)
doc_length <- rowSums(as.matrix(dtm))
term_freq <- colSums(as.matrix(dtm))

# Create JSON
json <- createJSON(
  phi = phi,
  theta = theta,
  vocab = vocab,
  doc.length = doc_length,
  term.frequency = term_freq
)

serVis(json)
```

## Complete Workflow

```r
#' Topic Model Pipeline
#' @param texts_df Data frame with doc_id, text, and metadata
#' @param k Number of topics
#' @param prevalence_formula Formula for prevalence covariates
#' @return List with model, diagnostics, and tables

topic_model_pipeline <- function(texts_df, k = 10,
                                  prevalence_formula = NULL,
                                  seed = 42) {

  # Prepare
  processed <- textProcessor(
    documents = texts_df$text,
    metadata = texts_df,
    lowercase = TRUE,
    removestopwords = TRUE,
    removenumbers = TRUE,
    removepunctuation = TRUE,
    stem = TRUE
  )

  out <- prepDocuments(
    processed$documents,
    processed$vocab,
    processed$meta,
    lower.thresh = 5
  )

  # Fit model
  if (is.null(prevalence_formula)) {
    model <- stm(
      documents = out$documents,
      vocab = out$vocab,
      K = k,
      data = out$meta,
      init.type = "Spectral",
      seed = seed
    )
  } else {
    model <- stm(
      documents = out$documents,
      vocab = out$vocab,
      K = k,
      prevalence = prevalence_formula,
      data = out$meta,
      init.type = "Spectral",
      seed = seed
    )
  }

  # Diagnostics
  diagnostics <- tibble(
    topic = 1:k,
    coherence = semanticCoherence(model, out$documents),
    exclusivity = exclusivity(model)
  )

  # Topic table
  topic_table <- create_topic_table(model)

  list(
    model = model,
    out = out,
    diagnostics = diagnostics,
    topic_table = topic_table
  )
}

# Usage
results <- topic_model_pipeline(
  texts,
  k = 10,
  prevalence_formula = ~ year + source
)
```
