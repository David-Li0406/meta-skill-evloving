# Text Visualization in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# ggplot2 3.4.2
# tidytext 0.4.1
# ggwordcloud 0.5.0
# igraph 1.5.0
# ggraph 2.1.0
```

## Installation

```r
install.packages(c("ggplot2", "tidytext", "ggwordcloud",
                   "igraph", "ggraph", "scales", "ggrepel"))
```

## Term Frequency Plots

### Basic Bar Chart

```r
library(tidyverse)
library(tidytext)

# Sample data
texts <- tibble(
  doc_id = 1:100,
  text = sample(c(
    "The economy shows growth with employment rising.",
    "Climate change impacts communities worldwide.",
    "Healthcare reform remains politically divisive.",
    "Technology transforms modern communication."
  ), 100, replace = TRUE)
)

# Tokenize and count
word_counts <- texts %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words, by = "word") %>%
  count(word, sort = TRUE)

# Top terms bar chart
word_counts %>%
  slice_head(n = 20) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(x = n, y = word)) +
  geom_col(fill = "steelblue") +
  labs(title = "Most Frequent Terms",
       x = "Frequency",
       y = NULL) +
  theme_minimal()

# Save
ggsave("output/figures/term_frequency.pdf", width = 8, height = 6)
```

### Lollipop Chart

```r
word_counts %>%
  slice_head(n = 20) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(x = n, y = word)) +
  geom_segment(aes(x = 0, xend = n, y = word, yend = word),
               color = "gray60") +
  geom_point(size = 3, color = "steelblue") +
  labs(title = "Most Frequent Terms",
       x = "Frequency",
       y = NULL) +
  theme_minimal()
```

## Word Clouds

```r
library(ggwordcloud)

# Basic word cloud
word_counts %>%
  slice_head(n = 100) %>%
  ggplot(aes(label = word, size = n)) +
  geom_text_wordcloud(color = "steelblue") +
  scale_size_area(max_size = 15) +
  theme_minimal()

# Colored by frequency
word_counts %>%
  slice_head(n = 100) %>%
  ggplot(aes(label = word, size = n, color = n)) +
  geom_text_wordcloud() +
  scale_size_area(max_size = 15) +
  scale_color_gradient(low = "lightblue", high = "darkblue") +
  theme_minimal()
```

## Sentiment Visualization

### Sentiment Distribution

```r
# Calculate sentiment per document
sentiment_scores <- texts %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(doc_id, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
  mutate(net_sentiment = positive - negative)

# Histogram
ggplot(sentiment_scores, aes(x = net_sentiment)) +
  geom_histogram(binwidth = 1, fill = "steelblue", color = "white") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "red") +
  labs(title = "Distribution of Document Sentiment",
       x = "Net Sentiment (Positive - Negative)",
       y = "Count") +
  theme_minimal()
```

### Sentiment Words

```r
# Most common sentiment words
sentiment_words <- texts %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(word, sentiment, sort = TRUE)

# Diverging bar chart
sentiment_words %>%
  group_by(sentiment) %>%
  slice_head(n = 10) %>%
  ungroup() %>%
  mutate(n = if_else(sentiment == "negative", -n, n),
         word = reorder(word, n)) %>%
  ggplot(aes(x = n, y = word, fill = sentiment)) +
  geom_col() +
  scale_fill_manual(values = c("negative" = "#E74C3C",
                               "positive" = "#27AE60")) +
  labs(title = "Top Sentiment Words",
       x = "Frequency (negative to positive)",
       y = NULL) +
  theme_minimal() +
  theme(legend.position = "bottom")
```

### Sentiment Over Time

```r
# Add dates to sample
texts_time <- texts %>%
  mutate(date = seq(as.Date("2020-01-01"),
                    by = "day",
                    length.out = n()))

# Monthly sentiment
monthly_sentiment <- texts_time %>%
  mutate(month = floor_date(date, "month")) %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(month, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
  mutate(net = positive - negative)

# Time series plot
ggplot(monthly_sentiment, aes(x = month, y = net)) +
  geom_line(color = "steelblue", size = 1) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  geom_smooth(method = "loess", color = "red", se = TRUE, alpha = 0.2) +
  labs(title = "Sentiment Over Time",
       x = "Date",
       y = "Net Sentiment") +
  theme_minimal()
```

## Topic Model Visualization

### Topic Prevalence

```r
# Sample topic prevalence data
topic_data <- tibble(
  topic = paste0("Topic ", 1:10),
  label = c("Economy", "Healthcare", "Climate", "Education",
            "Technology", "Immigration", "Crime", "Foreign Policy",
            "Media", "Elections"),
  prevalence = c(0.15, 0.12, 0.11, 0.10, 0.10,
                 0.09, 0.09, 0.08, 0.08, 0.08)
)

# Bar chart with labels
topic_data %>%
  mutate(label = reorder(label, prevalence)) %>%
  ggplot(aes(x = prevalence, y = label)) +
  geom_col(fill = "steelblue") +
  scale_x_continuous(labels = scales::percent) +
  labs(title = "Topic Prevalence",
       x = "Proportion of Corpus",
       y = NULL) +
  theme_minimal()
```

### Topic Top Words

```r
# Sample topic-word data
topic_words <- tibble(
  topic = rep(c("Economy", "Healthcare", "Climate"), each = 10),
  word = c("economy", "growth", "jobs", "tax", "market",
           "business", "trade", "employment", "gdp", "inflation",
           "health", "care", "hospital", "doctor", "insurance",
           "patient", "medical", "treatment", "coverage", "drug",
           "climate", "change", "carbon", "emissions", "energy",
           "environment", "warming", "policy", "clean", "fossil"),
  beta = runif(30, 0.01, 0.1)
)

# Faceted bar chart
topic_words %>%
  group_by(topic) %>%
  slice_max(beta, n = 7) %>%
  ungroup() %>%
  mutate(word = reorder_within(word, beta, topic)) %>%
  ggplot(aes(x = beta, y = word, fill = topic)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~topic, scales = "free_y") +
  scale_y_reordered() +
  labs(title = "Top Words by Topic",
       x = "Beta (word probability)",
       y = NULL) +
  theme_minimal()
```

### Topic Over Time

```r
# Sample topic prevalence over time
topic_time <- expand_grid(
  year = 2010:2023,
  topic = c("Climate", "Economy", "Healthcare")
) %>%
  mutate(prevalence = case_when(
    topic == "Climate" ~ 0.05 + (year - 2010) * 0.01 + rnorm(n(), 0, 0.01),
    topic == "Economy" ~ 0.15 - (year - 2010) * 0.005 + rnorm(n(), 0, 0.01),
    topic == "Healthcare" ~ 0.10 + rnorm(n(), 0, 0.01)
  ))

ggplot(topic_time, aes(x = year, y = prevalence, color = topic)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Topic Prevalence Over Time",
       x = "Year",
       y = "Topic Proportion",
       color = "Topic") +
  theme_minimal() +
  theme(legend.position = "bottom")
```

## Network Visualizations

### Word Co-occurrence Network

```r
library(igraph)
library(ggraph)

# Create co-occurrence matrix
word_pairs <- texts %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words, by = "word") %>%
  group_by(doc_id) %>%
  mutate(word2 = lead(word)) %>%
  filter(!is.na(word2)) %>%
  ungroup() %>%
  count(word, word2, sort = TRUE) %>%
  filter(n >= 2)  # Minimum co-occurrence

# Create graph
word_graph <- word_pairs %>%
  graph_from_data_frame()

# Plot
ggraph(word_graph, layout = "fr") +
  geom_edge_link(aes(edge_alpha = n, edge_width = n),
                 color = "gray50", show.legend = FALSE) +
  geom_node_point(color = "steelblue", size = 5) +
  geom_node_text(aes(label = name), repel = TRUE, size = 3) +
  theme_void() +
  labs(title = "Word Co-occurrence Network")
```

### Topic Correlation Network

```r
# Sample topic correlation matrix
n_topics <- 6
topic_cor <- matrix(runif(n_topics^2, -0.3, 0.5), nrow = n_topics)
topic_cor[lower.tri(topic_cor)] <- t(topic_cor)[lower.tri(topic_cor)]
diag(topic_cor) <- 1
rownames(topic_cor) <- colnames(topic_cor) <- paste0("Topic ", 1:n_topics)

# Convert to edges (threshold correlations)
cor_edges <- as_tibble(topic_cor, rownames = "from") %>%
  pivot_longer(-from, names_to = "to", values_to = "correlation") %>%
  filter(from < to, correlation > 0.1)

# Create graph
topic_graph <- graph_from_data_frame(cor_edges, directed = FALSE)

ggraph(topic_graph, layout = "stress") +
  geom_edge_link(aes(edge_width = correlation, edge_alpha = correlation),
                 color = "steelblue") +
  geom_node_point(size = 8, color = "steelblue") +
  geom_node_text(aes(label = name), color = "white", size = 3) +
  theme_void() +
  labs(title = "Topic Correlation Network")
```

## Classification Visualization

### Confusion Matrix

```r
library(scales)

# Sample confusion matrix data
conf_matrix <- tibble(
  truth = rep(c("Politics", "Sports", "Business", "Science"), each = 4),
  predicted = rep(c("Politics", "Sports", "Business", "Science"), 4),
  n = c(45, 3, 2, 0,
        2, 47, 1, 0,
        3, 1, 44, 2,
        0, 1, 3, 46)
)

ggplot(conf_matrix, aes(x = predicted, y = truth, fill = n)) +
  geom_tile() +
  geom_text(aes(label = n), color = "white", size = 5) +
  scale_fill_gradient(low = "lightblue", high = "darkblue") +
  labs(title = "Confusion Matrix",
       x = "Predicted",
       y = "Actual",
       fill = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

### Feature Importance

```r
# Sample feature importance
importance <- tibble(
  feature = paste0("word_", 1:20),
  importance = sort(runif(20, 0, 1), decreasing = TRUE)
)

importance %>%
  slice_head(n = 15) %>%
  mutate(feature = reorder(feature, importance)) %>%
  ggplot(aes(x = importance, y = feature)) +
  geom_col(fill = "steelblue") +
  labs(title = "Top Predictive Features",
       x = "Importance",
       y = NULL) +
  theme_minimal()
```

## Comparative Visualizations

### Comparing Groups

```r
# Log odds ratio for comparing word usage
group_words <- texts %>%
  mutate(group = sample(c("A", "B"), n(), replace = TRUE)) %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words, by = "word") %>%
  count(group, word) %>%
  pivot_wider(names_from = group, values_from = n, values_fill = 0) %>%
  mutate(
    total = A + B,
    log_odds = log((A + 1) / (B + 1))
  ) %>%
  filter(total >= 5)

# Plot top discriminating words
bind_rows(
  group_words %>% slice_max(log_odds, n = 10) %>% mutate(direction = "Group A"),
  group_words %>% slice_min(log_odds, n = 10) %>% mutate(direction = "Group B")
) %>%
  mutate(word = reorder(word, log_odds)) %>%
  ggplot(aes(x = log_odds, y = word, fill = direction)) +
  geom_col() +
  geom_vline(xintercept = 0, linetype = "dashed") +
  scale_fill_manual(values = c("Group A" = "#E74C3C", "Group B" = "#3498DB")) +
  labs(title = "Words Distinguishing Groups",
       x = "Log Odds Ratio",
       y = NULL) +
  theme_minimal()
```

## Publication-Ready Formatting

### Theme for Publications

```r
theme_publication <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title = element_text(size = base_size + 2, face = "bold"),
      plot.subtitle = element_text(size = base_size, color = "gray40"),
      axis.title = element_text(size = base_size),
      axis.text = element_text(size = base_size - 1),
      legend.title = element_text(size = base_size),
      legend.text = element_text(size = base_size - 1),
      panel.grid.minor = element_blank(),
      strip.text = element_text(size = base_size, face = "bold")
    )
}

# Apply to plots
word_counts %>%
  slice_head(n = 15) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(x = n, y = word)) +
  geom_col(fill = "steelblue") +
  labs(title = "Term Frequency",
       x = "Frequency",
       y = NULL) +
  theme_publication()
```

### Exporting High-Quality Figures

```r
# Save with appropriate dimensions and resolution
ggsave("output/figures/figure1.pdf",
       width = 8,
       height = 6,
       units = "in")

ggsave("output/figures/figure1.png",
       width = 8,
       height = 6,
       units = "in",
       dpi = 300)

# For journal requirements
ggsave("output/figures/figure1.tiff",
       width = 8,
       height = 6,
       units = "in",
       dpi = 600,
       compression = "lzw")
```

### Color Palettes

```r
# Colorblind-friendly palettes
library(scales)

# Okabe-Ito palette
okabe_ito <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#999999")

# Use in plots
ggplot(topic_time, aes(x = year, y = prevalence, color = topic)) +
  geom_line(size = 1) +
  scale_color_manual(values = okabe_ito) +
  theme_publication()
```
