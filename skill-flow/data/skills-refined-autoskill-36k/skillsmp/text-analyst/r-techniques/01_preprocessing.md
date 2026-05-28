# Text Preprocessing in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# tidytext 0.4.1
# quanteda 3.3.1
# tidyverse 2.0.0
```

## Installation

```r
install.packages(c("tidytext", "quanteda", "tidyverse", "SnowballC", "textstem"))
```

## Two Approaches: tidytext vs quanteda

| Package | Philosophy | Best For |
|---------|------------|----------|
| **tidytext** | Tidy data principles | Integration with dplyr, ggplot2 |
| **quanteda** | Corpus-centric | Large corpora, advanced features |

## tidytext Workflow

### Basic Tokenization

```r
library(tidyverse)
library(tidytext)

# Sample data
texts <- tibble(
  doc_id = 1:3,
  text = c(
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is transforming social science research.",
    "Text analysis requires careful preprocessing decisions."
  )
)

# Tokenize to words
tokens <- texts %>%
  unnest_tokens(word, text)

tokens
# # A tibble: 24 × 2
#    doc_id word
#     <int> <chr>
#  1      1 the
#  2      1 quick
#  3      1 brown
# ...
```

### Removing Stopwords

```r
# Default English stopwords (SMART list)
data(stop_words)

tokens_clean <- tokens %>%
  anti_join(stop_words, by = "word")

# Custom stopwords
custom_stops <- tibble(word = c("data", "analysis", "research"))

tokens_clean <- tokens %>%
  anti_join(stop_words, by = "word") %>%
  anti_join(custom_stops, by = "word")
```

### Stemming and Lemmatization

```r
library(SnowballC)

# Stemming (Porter)
tokens_stemmed <- tokens_clean %>%
  mutate(stem = wordStem(word))

# Lemmatization (requires textstem)
library(textstem)

tokens_lemma <- tokens_clean %>%
  mutate(lemma = lemmatize_words(word))
```

### N-grams

```r
# Bigrams
bigrams <- texts %>%
  unnest_tokens(bigram, text, token = "ngrams", n = 2)

# Trigrams
trigrams <- texts %>%
  unnest_tokens(trigram, text, token = "ngrams", n = 3)

# Filter bigrams by stopwords
bigrams_clean <- bigrams %>%
  separate(bigram, c("word1", "word2"), sep = " ") %>%
  filter(!word1 %in% stop_words$word,
         !word2 %in% stop_words$word) %>%
  unite(bigram, word1, word2, sep = " ")
```

### Document-Term Matrix

```r
# Create DTM from tokens
dtm_tidy <- tokens_clean %>%
  count(doc_id, word) %>%
  cast_dtm(doc_id, word, n)

# Or with TF-IDF
dtm_tfidf <- tokens_clean %>%
  count(doc_id, word) %>%
  bind_tf_idf(word, doc_id, n) %>%
  cast_dtm(doc_id, word, tf_idf)

# Inspect
dtm_tidy
# <<DocumentTermMatrix (documents: 3, terms: 18)>>
```

## quanteda Workflow

### Creating a Corpus

```r
library(quanteda)

# From character vector
corp <- corpus(c(
  "The quick brown fox jumps over the lazy dog.",
  "Machine learning is transforming social science research.",
  "Text analysis requires careful preprocessing decisions."
))

# From data frame
texts_df <- data.frame(
  doc_id = c("doc1", "doc2", "doc3"),
  text = c(
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning is transforming social science research.",
    "Text analysis requires careful preprocessing decisions."
  ),
  year = c(2020, 2021, 2022)
)

corp <- corpus(texts_df, text_field = "text", docid_field = "doc_id")
```

### Tokenization

```r
# Basic tokenization
toks <- tokens(corp)

# With options
toks <- tokens(corp,
               remove_punct = TRUE,
               remove_numbers = TRUE,
               remove_symbols = TRUE)

# Lowercase
toks <- tokens_tolower(toks)
```

### Stopword Removal

```r
# Remove stopwords
toks_clean <- tokens_remove(toks, stopwords("en"))

# Custom stopwords
toks_clean <- tokens_remove(toks, c(stopwords("en"), "data", "research"))

# Keep specific words (instead of remove)
toks_keep <- tokens_select(toks, c("machine", "learning", "social"))
```

### Stemming

```r
toks_stem <- tokens_wordstem(toks_clean)
```

### N-grams

```r
# Create bigrams
toks_ngram <- tokens_ngrams(toks_clean, n = 2)

# Compound tokens (keep phrases together)
toks_compound <- tokens_compound(toks, phrase(c("machine learning", "social science")))
```

### Document-Feature Matrix (DFM)

```r
# Create DFM
dfm <- dfm(toks_clean)

# With TF-IDF weighting
dfm_tfidf <- dfm_tfidf(dfm)

# Trim by frequency
dfm_trimmed <- dfm_trim(dfm,
                        min_termfreq = 2,      # Minimum term frequency
                        min_docfreq = 2,       # Minimum document frequency
                        max_docfreq = 0.9,     # Maximum as proportion
                        docfreq_type = "prop") # Proportion for max

# Inspect
dfm_trimmed
# Document-feature matrix of: 3 documents, 12 features
```

## Preprocessing Pipeline Comparison

### tidytext Pipeline

```r
preprocess_tidytext <- function(df, text_col = "text", doc_col = "doc_id") {
  df %>%
    # Tokenize
    unnest_tokens(word, !!sym(text_col)) %>%
    # Remove stopwords
    anti_join(stop_words, by = "word") %>%
    # Remove numbers
    filter(!str_detect(word, "^[0-9]+$")) %>%
    # Remove short words
    filter(str_length(word) > 2) %>%
    # Optional: stem
    mutate(word = wordStem(word))
}

# Usage
tokens_processed <- preprocess_tidytext(texts)
```

### quanteda Pipeline

```r
preprocess_quanteda <- function(texts, docvars = NULL) {
  corp <- corpus(texts)
  if (!is.null(docvars)) docvars(corp) <- docvars

  tokens(corp,
         remove_punct = TRUE,
         remove_numbers = TRUE,
         remove_symbols = TRUE) %>%
    tokens_tolower() %>%
    tokens_remove(stopwords("en")) %>%
    tokens_wordstem()
}

# Usage
toks_processed <- preprocess_quanteda(texts$text)
dfm_processed <- dfm(toks_processed)
```

## Converting Between Formats

```r
# tidytext to quanteda
dtm <- tokens_clean %>%
  count(doc_id, word) %>%
  cast_dfm(doc_id, word, n)

# quanteda to tidytext
tidy_from_dfm <- tidy(dfm)

# quanteda to tm
dtm_tm <- convert(dfm, to = "tm")

# tm to quanteda
dfm_from_tm <- as.dfm(dtm_tm)
```

## Handling Special Cases

### URLs and HTML

```r
library(stringr)

# Remove URLs
texts_clean <- texts %>%
  mutate(text = str_remove_all(text, "https?://\\S+"))

# Remove HTML tags
texts_clean <- texts %>%
  mutate(text = str_remove_all(text, "<[^>]+>"))

# Or use textclean package
library(textclean)
texts_clean <- texts %>%
  mutate(text = replace_url(text),
         text = replace_html(text))
```

### Encoding Issues

```r
# Check encoding
Encoding(texts$text)

# Convert to UTF-8
texts$text <- iconv(texts$text, to = "UTF-8", sub = "")

# Remove non-ASCII
texts$text <- str_replace_all(texts$text, "[^[:ascii:]]", "")
```

### Empty Documents

```r
# After preprocessing, check for empty docs
doc_lengths <- tokens_clean %>%
  count(doc_id, name = "n_tokens")

# Identify empty docs
empty_docs <- doc_lengths %>%
  filter(n_tokens == 0)

# Or with quanteda
ntoken(dfm)  # Tokens per document
```

## Corpus Statistics

```r
# With tidytext
corpus_stats <- tokens_clean %>%
  summarise(
    n_docs = n_distinct(doc_id),
    n_tokens = n(),
    n_types = n_distinct(word),
    mean_doc_length = n() / n_distinct(doc_id)
  )

# Term frequencies
term_freq <- tokens_clean %>%
  count(word, sort = TRUE)

# Document frequencies
doc_freq <- tokens_clean %>%
  distinct(doc_id, word) %>%
  count(word, sort = TRUE) %>%
  rename(doc_freq = n)

# With quanteda
textstat_summary(dfm)
topfeatures(dfm, 20)
```

## Best Practices

1. **Document all decisions** - Create a preprocessing log
2. **Start minimal** - Add processing steps only if needed
3. **Check before and after** - Examine vocabulary at each step
4. **Validate with KWIC** - Use keyword-in-context to verify
5. **Set seeds** - For any stochastic elements
6. **Save intermediate objects** - For debugging and reproducibility

```r
# Example preprocessing log
preprocessing_log <- list(
  date = Sys.Date(),
  n_docs_raw = nrow(texts),
  n_docs_processed = n_distinct(tokens_clean$doc_id),
  vocab_raw = length(unique(tokens$word)),
  vocab_processed = length(unique(tokens_clean$word)),
  stopwords = "SMART + custom",
  stemming = "Porter",
  min_term_freq = 5
)

saveRDS(preprocessing_log, "data/processed/preprocessing_log.rds")
```
