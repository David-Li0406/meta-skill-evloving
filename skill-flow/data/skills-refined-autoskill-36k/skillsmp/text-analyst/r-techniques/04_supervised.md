# Supervised Text Classification in R

## Package Versions

```r
# Tested with:
# R 4.3.0
# tidymodels 1.1.0
# textrecipes 1.0.4
# tidytext 0.4.1
```

## Installation

```r
install.packages(c("tidymodels", "textrecipes", "tidytext", "discrim"))
```

## tidymodels Workflow

### Sample Data

```r
library(tidyverse)
library(tidymodels)
library(textrecipes)

# Sample labeled data
set.seed(42)
texts <- tibble(
  doc_id = 1:200,
  text = c(
    rep("The government passed new tax legislation today.", 50),
    rep("The championship game ended in an exciting overtime.", 50),
    rep("Stock markets reached record highs amid economic growth.", 50),
    rep("Scientists discovered a new species in the rainforest.", 50)
  ) %>% sample(),
  label = c(
    rep("politics", 50),
    rep("sports", 50),
    rep("business", 50),
    rep("science", 50)
  ) %>% sample()
) %>%
  mutate(label = factor(label))
```

### Train/Test Split

```r
# Stratified split
set.seed(42)
split <- initial_split(texts, prop = 0.8, strata = label)
train <- training(split)
test <- testing(split)

# Check balance
table(train$label)
table(test$label)
```

### Feature Engineering with Recipes

```r
# Basic text recipe
text_recipe <- recipe(label ~ text, data = train) %>%
  step_tokenize(text) %>%                    # Tokenize
  step_stopwords(text) %>%                   # Remove stopwords
  step_stem(text) %>%                        # Stem
  step_tokenfilter(text, max_tokens = 500) %>%  # Keep top N tokens
  step_tfidf(text)                           # TF-IDF features

# Alternative: word embeddings (requires pretrained)
# step_word_embeddings(text, embeddings = glove_embeddings)

# Preview the preprocessing
text_recipe %>%
  prep() %>%
  bake(new_data = train) %>%
  glimpse()
```
### Model Specification

```r
# Logistic regression (multinomial for >2 classes)
lr_spec <- multinom_reg(penalty = 0.01, mixture = 1) %>%
  set_engine("glmnet") %>%
  set_mode("classification")

# Naive Bayes
library(discrim)
nb_spec <- naive_Bayes() %>%
  set_engine("naivebayes") %>%
  set_mode("classification")

# Random Forest
rf_spec <- rand_forest(trees = 500) %>%
  set_engine("ranger") %>%
  set_mode("classification")

# SVM
svm_spec <- svm_linear(cost = 1) %>%
  set_engine("LiblineaR") %>%
  set_mode("classification")
```

### Creating a Workflow

```r
# Combine recipe and model
lr_workflow <- workflow() %>%
  add_recipe(text_recipe) %>%
  add_model(lr_spec)

# Fit on training data
lr_fit <- lr_workflow %>%
  fit(data = train)
```

### Evaluation

```r
# Predictions on test set
predictions <- lr_fit %>%
  predict(test) %>%
  bind_cols(test)

# Metrics
metrics <- predictions %>%
  metrics(truth = label, estimate = .pred_class)

# Confusion matrix
conf_mat <- predictions %>%
  conf_mat(truth = label, estimate = .pred_class)

# Visualize
autoplot(conf_mat, type = "heatmap")

# Per-class metrics
predictions %>%
  f_meas(truth = label, estimate = .pred_class, estimator = "macro")

# Full classification report
predictions %>%
  conf_mat(truth = label, estimate = .pred_class) %>%
  summary()
```

### Cross-Validation

```r
# Create folds
set.seed(42)
folds <- vfold_cv(train, v = 5, strata = label)

# Fit with cross-validation
cv_results <- lr_workflow %>%
  fit_resamples(
    resamples = folds,
    metrics = metric_set(accuracy, f_meas),
    control = control_resamples(save_pred = TRUE)
  )

# Collect metrics
collect_metrics(cv_results)

# Collect predictions from all folds
cv_predictions <- collect_predictions(cv_results)

# Overall confusion matrix
cv_predictions %>%
  conf_mat(truth = label, estimate = .pred_class)
```

### Hyperparameter Tuning

```r
# Specify model with tuning parameters
lr_tune_spec <- multinom_reg(
  penalty = tune(),
  mixture = tune()
) %>%
  set_engine("glmnet") %>%
  set_mode("classification")

# Tuning workflow
tune_workflow <- workflow() %>%
  add_recipe(text_recipe) %>%
  add_model(lr_tune_spec)

# Grid of parameters
lr_grid <- grid_regular(
  penalty(range = c(-4, 0)),
  mixture(range = c(0, 1)),
  levels = 5
)

# Tune with cross-validation
tune_results <- tune_workflow %>%
  tune_grid(
    resamples = folds,
    grid = lr_grid,
    metrics = metric_set(accuracy, f_meas)
  )

# Best parameters
best_params <- tune_results %>%
  select_best(metric = "f_meas")

# Finalize workflow
final_workflow <- tune_workflow %>%
  finalize_workflow(best_params)

# Final fit on full training data
final_fit <- final_workflow %>%
  fit(data = train)

# Evaluate on test
final_predictions <- final_fit %>%
  predict(test) %>%
  bind_cols(test)

final_predictions %>%
  metrics(truth = label, estimate = .pred_class)
```

## Comparing Multiple Models

```r
# Define models
models <- list(
  "Logistic Regression" = lr_spec,
  "Naive Bayes" = nb_spec,
  "Random Forest" = rf_spec
)

# Fit each with cross-validation
model_results <- map_dfr(names(models), function(name) {
  workflow() %>%
    add_recipe(text_recipe) %>%
    add_model(models[[name]]) %>%
    fit_resamples(
      resamples = folds,
      metrics = metric_set(accuracy, f_meas)
    ) %>%
    collect_metrics() %>%
    mutate(model = name)
})

# Compare
model_results %>%
  ggplot(aes(x = model, y = mean, fill = .metric)) +
  geom_col(position = "dodge") +
  geom_errorbar(aes(ymin = mean - std_err, ymax = mean + std_err),
                position = position_dodge(width = 0.9), width = 0.2) +
  labs(title = "Model Comparison",
       y = "Metric Value") +
  theme_minimal()
```

## Feature Importance

```r
# For glmnet models
library(vip)

# Extract fitted model
fitted_model <- extract_fit_parsnip(lr_fit)

# Variable importance
vip(fitted_model, num_features = 20)

# Get coefficients
tidy(fitted_model) %>%
  filter(class == "politics") %>%  # For one class
  arrange(desc(abs(estimate))) %>%
  head(20)
```

## Handling Class Imbalance

```r
# Check imbalance
table(train$label)

# Option 1: Upsample minority
library(themis)

balanced_recipe <- recipe(label ~ text, data = train) %>%
  step_tokenize(text) %>%
  step_stopwords(text) %>%
  step_tokenfilter(text, max_tokens = 500) %>%
  step_tfidf(text) %>%
  step_upsample(label)  # Upsample minority

# Option 2: Downsample majority
balanced_recipe2 <- recipe(label ~ text, data = train) %>%
  step_tokenize(text) %>%
  step_stopwords(text) %>%
  step_tokenfilter(text, max_tokens = 500) %>%
  step_tfidf(text) %>%
  step_downsample(label)

# Option 3: Class weights in model
weighted_spec <- multinom_reg(penalty = 0.01) %>%
  set_engine("glmnet") %>%
  set_mode("classification")
# Note: glmnet supports class.weights parameter
```

## Binary Classification

```r
# Binary example
binary_texts <- texts %>%
  filter(label %in% c("politics", "sports")) %>%
  mutate(label = factor(label))

# Split
split_binary <- initial_split(binary_texts, prop = 0.8, strata = label)
train_binary <- training(split_binary)
test_binary <- testing(split_binary)

# Logistic regression (binary)
binary_spec <- logistic_reg(penalty = 0.01) %>%
  set_engine("glmnet") %>%
  set_mode("classification")

# Workflow
binary_workflow <- workflow() %>%
  add_recipe(text_recipe) %>%
  add_model(binary_spec)

# Fit and predict
binary_fit <- binary_workflow %>%
  fit(data = train_binary)

binary_pred <- binary_fit %>%
  predict(test_binary, type = "prob") %>%
  bind_cols(
    predict(binary_fit, test_binary)
  ) %>%
  bind_cols(test_binary)

# ROC curve
binary_pred %>%
  roc_curve(truth = label, .pred_politics) %>%
  autoplot()

# AUC
binary_pred %>%
  roc_auc(truth = label, .pred_politics)
```

## Output: Publication Tables

### Classification Performance Table

```r
create_performance_table <- function(predictions, truth_col, pred_col) {
  # Overall metrics
  overall <- predictions %>%
    metrics(truth = !!sym(truth_col), estimate = !!sym(pred_col))

  # Per-class
  cm <- predictions %>%
    conf_mat(truth = !!sym(truth_col), estimate = !!sym(pred_col))

  per_class <- summary(cm) %>%
    filter(.metric %in% c("precision", "recall", "f_meas")) %>%
    pivot_wider(names_from = .metric, values_from = .estimate)

  list(
    overall = overall,
    per_class = per_class,
    confusion_matrix = cm
  )
}

results <- create_performance_table(predictions, "label", ".pred_class")
```

### Export Results

```r
# Save model
saveRDS(lr_fit, "output/models/text_classifier.rds")

# Save results
write_csv(results$overall, "output/tables/classification_overall.csv")
write_csv(results$per_class, "output/tables/classification_by_class.csv")
```

## Complete Workflow

```r
#' Text Classification Pipeline
#' @param train_df Training data with text and label columns
#' @param test_df Test data
#' @param max_tokens Maximum vocabulary size
#' @return List with model, predictions, and metrics

text_classification_pipeline <- function(train_df, test_df,
                                         max_tokens = 1000) {

  # Recipe
  rec <- recipe(label ~ text, data = train_df) %>%
    step_tokenize(text) %>%
    step_stopwords(text) %>%
    step_stem(text) %>%
    step_tokenfilter(text, max_tokens = max_tokens) %>%
    step_tfidf(text)

  # Model
  spec <- multinom_reg(penalty = 0.01, mixture = 1) %>%
    set_engine("glmnet") %>%
    set_mode("classification")

  # Workflow
  wf <- workflow() %>%
    add_recipe(rec) %>%
    add_model(spec)

  # Cross-validation
  set.seed(42)
  folds <- vfold_cv(train_df, v = 5, strata = label)

  cv_results <- wf %>%
    fit_resamples(
      resamples = folds,
      metrics = metric_set(accuracy, f_meas)
    )

  # Final fit
  final_fit <- wf %>%
    fit(data = train_df)

  # Test predictions
  test_pred <- final_fit %>%
    predict(test_df) %>%
    bind_cols(test_df)

  # Metrics
  test_metrics <- test_pred %>%
    metrics(truth = label, estimate = .pred_class)

  list(
    model = final_fit,
    cv_metrics = collect_metrics(cv_results),
    test_predictions = test_pred,
    test_metrics = test_metrics,
    confusion_matrix = conf_mat(test_pred, truth = label,
                                estimate = .pred_class)
  )
}

# Usage
results <- text_classification_pipeline(train, test)
print(results$test_metrics)
autoplot(results$confusion_matrix, type = "heatmap")
```
