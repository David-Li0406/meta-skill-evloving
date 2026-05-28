# Dictionary and Sentiment Analysis in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# tidytext 0.4.1
# tidyverse 2.0.0
# textdata 0.4.4
# lexicon 1.2.1
```

## Installation

```r
install.packages(c("tidytext", "tidyverse", "textdata", "lexicon"))

# Some lexicons require downloading
library(textdata)
lexicon_afinn()  # Downloads AFINN
lexicon_nrc()    # Downloads NRC
```

## Available Lexicons in tidytext

```r
library(tidytext)

# Built-in lexicons
get_sentiments("bing")    # Positive/negative binary
get_sentiments("afinn")   # -5 to +5 scale
get_sentiments("nrc")     # Emotions + sentiment
get_sentiments("loughran") # Finance-specific
```

### Lexicon Details

| Lexicon | Categories | Size | Best For |
|---------|------------|------|----------|
| **Bing** | positive, negative | ~6,800 | General binary sentiment |
| **AFINN** | -5 to +5 | ~2,500 | Weighted sentiment |
| **NRC** | 8 emotions + pos/neg | ~14,000 | Emotion detection |
| **Loughran** | 6 categories | ~4,000 | Financial texts |

## Basic Sentiment Analysis

### Binary Sentiment (Bing)

```r
library(tidyverse)
library(tidytext)

# Sample data
texts <- tibble(
  doc_id = 1:4,
  text = c(
    "I love this amazing product! Highly recommend.",
    "Terrible experience. The worst purchase ever.",
    "It's okay, nothing special but not bad.",
    "Great quality but expensive and slow delivery."
  )
)

# Tokenize
tokens <- texts %>%
  unnest_tokens(word, text)

# Join with Bing lexicon
sentiment_bing <- tokens %>%
  inner_join(get_sentiments("bing"), by = "word")

# Count by document
doc_sentiment <- sentiment_bing %>%
  count(doc_id, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
  mutate(sentiment_score = positive - negative)

doc_sentiment
# # A tibble: 4 × 4
#   doc_id negative positive sentiment_score
#    <int>    <int>    <int>           <int>
# 1      1        0        3               3
# 2      2        2        0              -2
# ...
```

### Weighted Sentiment (AFINN)

```r
# AFINN gives numeric scores
afinn <- get_sentiments("afinn")

sentiment_afinn <- tokens %>%
  inner_join(afinn, by = "word") %>%
  group_by(doc_id) %>%
  summarise(
    sentiment = sum(value),
    n_words = n(),
    mean_sentiment = mean(value)
  )

sentiment_afinn
```

### Emotion Detection (NRC)

```r
nrc <- get_sentiments("nrc")

# Get emotion counts
emotions <- tokens %>%
  inner_join(nrc, by = "word") %>%
  count(doc_id, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0)

emotions
# Contains: anger, anticipation, disgust, fear, joy,
#           negative, positive, sadness, surprise, trust
```

## TF-IDF Analysis

```r
# Calculate TF-IDF
tfidf <- tokens %>%
  count(doc_id, word) %>%
  bind_tf_idf(word, doc_id, n)

# Top distinctive terms per document
top_tfidf <- tfidf %>%
  group_by(doc_id) %>%
  slice_max(tf_idf, n = 10)

top_tfidf
```

## Custom Dictionaries

### Creating a Custom Dictionary

```r
# Define dictionary as data frame
my_dictionary <- tibble(
  word = c("innovative", "disruptive", "groundbreaking", "revolutionary",
           "obsolete", "outdated", "stagnant", "declining"),
  category = c(rep("innovation_positive", 4), rep("innovation_negative", 4)),
  weight = c(2, 1.5, 2, 2, -1, -1, -1.5, -1)
)

# Apply dictionary
dict_matches <- tokens %>%
  inner_join(my_dictionary, by = "word")

# Aggregate by document
dict_scores <- dict_matches %>%
  group_by(doc_id, category) %>%
  summarise(
    n_matches = n(),
    weighted_score = sum(weight),
    .groups = "drop"
  )
```

### Multi-Word Expressions

```r
# For multi-word dictionary terms
mwe_dictionary <- tibble(
  phrase = c("machine learning", "artificial intelligence", "deep learning"),
  category = "tech_terms"
)

# Search in original text
texts_with_mwe <- texts %>%
  mutate(
    ml_count = str_count(tolower(text), "machine learning"),
    ai_count = str_count(tolower(text), "artificial intelligence"),
    dl_count = str_count(tolower(text), "deep learning")
  )
```

## Handling Negation

### Simple Negation Window

```r
negation_words <- c("not", "no", "never", "neither", "nobody", "nothing",
                    "nowhere", "hardly", "barely", "scarcely", "don't",
                    "doesn't", "didn't", "won't", "wouldn't", "couldn't",
                    "shouldn't", "can't", "cannot")

# Create bigrams to detect negation
negated <- texts %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2) %>%
  separate(bigram, c("word1", "word2"), sep = " ") %>%
  # Check if first word is negation
  mutate(negated = word1 %in% negation_words) %>%
  # Join sentiment on second word
  inner_join(get_sentiments("bing"), by = c("word2" = "word")) %>%
  # Flip sentiment if negated
  mutate(sentiment = if_else(negated,
                             if_else(sentiment == "positive", "negative", "positive"),
                             sentiment))
```

## Sentiment Over Time

```r
# Sample time-series data
text_time <- tibble(
  doc_id = 1:100,
  date = seq(as.Date("2020-01-01"), as.Date("2020-04-10"), by = "day"),
  text = sample(c(
    "Great news today! Very positive developments.",
    "Terrible situation, concerning trends.",
    "Normal day, nothing special happening.",
    "Exciting breakthrough, amazing results!"
  ), 100, replace = TRUE)
)

# Calculate daily sentiment
daily_sentiment <- text_time %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(date, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
  mutate(net_sentiment = positive - negative)

# Plot
ggplot(daily_sentiment, aes(x = date, y = net_sentiment)) +
  geom_line() +
  geom_smooth(method = "loess", se = TRUE) +
  labs(title = "Sentiment Over Time",
       x = "Date", y = "Net Sentiment") +
  theme_minimal()
```

## Comparing Groups

```r
# Sample grouped data
grouped_texts <- tibble(
  doc_id = 1:200,
  group = rep(c("Democrat", "Republican"), each = 100),
  text = c(
    rep("We must protect social programs and support workers.", 50),
    rep("Government overreach is harming small businesses.", 50),
    rep("Tax cuts will stimulate economic growth.", 50),
    rep("Investment in education benefits everyone.", 50)
  )
)

# Calculate sentiment by group
group_sentiment <- grouped_texts %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(group, sentiment) %>%
  group_by(group) %>%
  mutate(prop = n / sum(n)) %>%
  filter(sentiment == "positive")

# Visualize
ggplot(group_sentiment, aes(x = group, y = prop, fill = group)) +
  geom_col() +
  labs(title = "Proportion Positive Sentiment by Group",
       y = "Proportion Positive") +
  theme_minimal()
```

## Validation

### Coverage Check

```r
# What proportion of documents have matches?
coverage <- tokens %>%
  left_join(get_sentiments("bing"), by = "word") %>%
  group_by(doc_id) %>%
  summarise(
    n_tokens = n(),
    n_matches = sum(!is.na(sentiment)),
    coverage = n_matches / n_tokens
  )

summary(coverage$coverage)
# How many docs have zero matches?
sum(coverage$n_matches == 0)
```

### KWIC Validation

```r
library(quanteda)

# Create corpus
corp <- corpus(texts$text, docvars = texts[, "doc_id"])

# Keyword in context
kwic_positive <- kwic(tokens(corp), pattern = "great", window = 5)
kwic_negative <- kwic(tokens(corp), pattern = "terrible", window = 5)

# Review contexts
print(kwic_positive)
```

## Finance-Specific: Loughran-McDonald

```r
# Loughran-McDonald categories
lm <- get_sentiments("loughran")

table(lm$sentiment)
# constraining   litigious    negative  positive superfluous  uncertainty
#          184         903        2355         354          56          297

# Apply to financial text
financial_text <- tibble(
  text = "The company reported weak earnings amid uncertain market conditions and ongoing litigation."
)

financial_sentiment <- financial_text %>%
  unnest_tokens(word, text) %>%
  inner_join(lm, by = "word") %>%
  count(sentiment)

financial_sentiment
```

## Output Tables

### Sentiment Summary Table

```r
create_sentiment_table <- function(tokens_df, lexicon = "bing") {
  lex <- get_sentiments(lexicon)

  tokens_df %>%
    inner_join(lex, by = "word") %>%
    count(doc_id, sentiment) %>%
    pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
    mutate(
      total = positive + negative,
      net = positive - negative,
      ratio = positive / (positive + negative)
    )
}

sentiment_summary <- create_sentiment_table(tokens)
```

### Top Words Table

```r
# Most common sentiment words
top_sentiment_words <- tokens %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(word, sentiment, sort = TRUE) %>%
  group_by(sentiment) %>%
  slice_max(n, n = 10)

# Visualize
top_sentiment_words %>%
  mutate(n = if_else(sentiment == "negative", -n, n)) %>%
  ggplot(aes(x = reorder(word, n), y = n, fill = sentiment)) +
  geom_col() +
  coord_flip() +
  labs(title = "Top Sentiment Words",
       x = "Word", y = "Frequency") +
  theme_minimal()
```

## Complete Workflow Example

```r
#' Sentiment Analysis Pipeline
#' @param texts_df Data frame with doc_id and text columns
#' @param lexicon Name of lexicon ("bing", "afinn", "nrc")
#' @return List with sentiment scores and validation stats

sentiment_pipeline <- function(texts_df, lexicon = "bing") {

  # Tokenize
  tokens <- texts_df %>%
    unnest_tokens(word, text) %>%
    anti_join(stop_words, by = "word")

  # Get lexicon
  lex <- get_sentiments(lexicon)

  # Join and aggregate
  if (lexicon == "afinn") {
    scores <- tokens %>%
      inner_join(lex, by = "word") %>%
      group_by(doc_id) %>%
      summarise(
        sentiment = sum(value),
        n_matches = n()
      )
  } else {
    scores <- tokens %>%
      inner_join(lex, by = "word") %>%
      count(doc_id, sentiment) %>%
      pivot_wider(names_from = sentiment, values_from = n, values_fill = 0)
  }

  # Coverage stats
  coverage <- tokens %>%
    left_join(lex, by = "word") %>%
    group_by(doc_id) %>%
    summarise(
      n_tokens = n(),
      n_matches = sum(!is.na(value) | !is.na(sentiment)),
      coverage = n_matches / n_tokens
    )

  list(
    scores = scores,
    coverage = coverage,
    summary = summary(coverage$coverage)
  )
}

# Usage
results <- sentiment_pipeline(texts, lexicon = "afinn")
```
