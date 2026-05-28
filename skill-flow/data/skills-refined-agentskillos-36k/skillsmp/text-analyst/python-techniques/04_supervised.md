# Supervised Text Classification in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# scikit-learn 1.3.0
# transformers 4.30.0
# torch 2.0.0
```

## Installation

```bash
pip install scikit-learn transformers torch pandas numpy

# For GPU support
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

## sklearn Workflow

### Sample Data

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import random

random.seed(42)
np.random.seed(42)

# Sample labeled data
texts = [
    "The government passed new tax legislation today.",
    "The championship game ended in an exciting overtime.",
    "Stock markets reached record highs amid economic growth.",
    "Scientists discovered a new species in the rainforest.",
] * 50

labels = ["politics", "sports", "business", "science"] * 50

# Shuffle
combined = list(zip(texts, labels))
random.shuffle(combined)
texts, labels = zip(*combined)
texts, labels = list(texts), list(labels)
```

### Train/Test Split

```python
# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

print(f"Training: {len(X_train)}, Test: {len(X_test)}")
print(f"Class distribution (train): {pd.Series(y_train).value_counts().to_dict()}")
```

### Feature Extraction

```python
# TF-IDF Vectorizer
tfidf = TfidfVectorizer(
    max_features=5000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 2),
    stop_words='english',
    sublinear_tf=True
)

# Fit on training data only
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print(f"Feature matrix shape: {X_train_tfidf.shape}")
```

### Training Models

```python
# Logistic Regression
lr_model = LogisticRegression(
    C=1.0,
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)
lr_model.fit(X_train_tfidf, y_train)

# SVM
svm_model = LinearSVC(
    C=1.0,
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)
svm_model.fit(X_train_tfidf, y_train)

# Naive Bayes
nb_model = MultinomialNB(alpha=0.1)
nb_model.fit(X_train_tfidf, y_train)
```

### Evaluation

```python
def evaluate_model(model, X_test, y_test, model_name="Model"):
    """Evaluate classification model."""
    y_pred = model.predict(X_test)

    print(f"\n{model_name} Results:")
    print("=" * 50)
    print(classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    return y_pred

# Evaluate all models
lr_pred = evaluate_model(lr_model, X_test_tfidf, y_test, "Logistic Regression")
svm_pred = evaluate_model(svm_model, X_test_tfidf, y_test, "SVM")
nb_pred = evaluate_model(nb_model, X_test_tfidf, y_test, "Naive Bayes")
```

### Cross-Validation

```python
# Stratified K-fold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Cross-validation scores
from sklearn.metrics import make_scorer, f1_score

# Create TF-IDF on full data for CV
tfidf_full = TfidfVectorizer(
    max_features=5000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 2),
    stop_words='english'
)
X_full = tfidf_full.fit_transform(texts)

# F1 macro scorer
f1_macro = make_scorer(f1_score, average='macro')

# CV scores for each model
for name, model in [('LR', LogisticRegression(max_iter=1000, random_state=42)),
                    ('SVM', LinearSVC(max_iter=1000, random_state=42)),
                    ('NB', MultinomialNB())]:
    scores = cross_val_score(model, X_full, labels, cv=cv, scoring=f1_macro)
    print(f"{name}: F1-macro = {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Create pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000, random_state=42))
])

# Parameter grid
param_grid = {
    'tfidf__max_features': [1000, 5000],
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'clf__C': [0.1, 1.0, 10.0]
}

# Grid search
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='f1_macro',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.3f}")

# Evaluate on test
best_pred = grid_search.predict(X_test)
print(classification_report(y_test, best_pred))
```

### Feature Importance

```python
def get_top_features(model, vectorizer, n=20):
    """Get top features for each class."""
    feature_names = vectorizer.get_feature_names_out()

    # For logistic regression
    if hasattr(model, 'coef_'):
        results = {}
        for i, class_name in enumerate(model.classes_):
            # Get coefficients for this class
            coefs = model.coef_[i] if len(model.classes_) > 2 else model.coef_[0]

            # Top positive features
            top_idx = np.argsort(coefs)[-n:][::-1]
            results[class_name] = [(feature_names[j], coefs[j]) for j in top_idx]

        return results

    return None

top_features = get_top_features(lr_model, tfidf)
for class_name, features in top_features.items():
    print(f"\n{class_name}:")
    for word, coef in features[:10]:
        print(f"  {word}: {coef:.3f}")
```

## Transformers / BERT

### Using Pretrained Sentiment Model

```python
from transformers import pipeline

# Zero-shot classification
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

# Classify without training
text = "The stock market crashed dramatically today"
labels_zs = ["politics", "sports", "business", "science"]

result = classifier(text, labels_zs)
print(f"Text: {text}")
print(f"Predicted: {result['labels'][0]} ({result['scores'][0]:.3f})")
```

### Fine-tuning BERT

```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import Dataset
import torch

# Prepare data
train_df = pd.DataFrame({'text': X_train, 'label': y_train})
test_df = pd.DataFrame({'text': X_test, 'label': y_test})

# Create label mapping
label2id = {l: i for i, l in enumerate(set(labels))}
id2label = {i: l for l, i in label2id.items()}

train_df['label'] = train_df['label'].map(label2id)
test_df['label'] = test_df['label'].map(label2id)

# Convert to HuggingFace Dataset
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load tokenizer and model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train
trainer.train()

# Evaluate
results = trainer.evaluate()
print(results)
```

### Using Fine-tuned Model

```python
# Make predictions
def predict_text(text, model, tokenizer):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = predictions.argmax().item()

    return {
        'label': id2label[predicted_class],
        'confidence': predictions.max().item()
    }

# Example
result = predict_text("The team won the championship", model, tokenizer)
print(result)
```

## Handling Class Imbalance

```python
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# Option 1: Class weights
class_weights = compute_class_weight(
    'balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = dict(zip(np.unique(y_train), class_weights))

lr_balanced = LogisticRegression(
    class_weight=class_weight_dict,
    max_iter=1000,
    random_state=42
)

# Option 2: SMOTE (need numeric features)
# smote = SMOTE(random_state=42)
# X_resampled, y_resampled = smote.fit_resample(X_train_tfidf, y_train)

# Option 3: Undersampling
# undersampler = RandomUnderSampler(random_state=42)
# X_resampled, y_resampled = undersampler.fit_resample(X_train_tfidf, y_train)
```

## Error Analysis

```python
def error_analysis(y_true, y_pred, texts, n_samples=5):
    """Analyze classification errors."""
    errors = []

    for i, (true, pred, text) in enumerate(zip(y_true, y_pred, texts)):
        if true != pred:
            errors.append({
                'index': i,
                'text': text[:200],
                'true_label': true,
                'predicted': pred
            })

    errors_df = pd.DataFrame(errors)

    print(f"Total errors: {len(errors_df)}")
    print(f"\nError distribution:")
    print(errors_df.groupby(['true_label', 'predicted']).size())

    print(f"\nSample errors:")
    for _, row in errors_df.head(n_samples).iterrows():
        print(f"\nTrue: {row['true_label']}, Predicted: {row['predicted']}")
        print(f"Text: {row['text']}")

    return errors_df

errors = error_analysis(y_test, lr_pred, X_test)
```

## Complete Pipeline

```python
from sklearn.base import BaseEstimator, TransformerMixin

class TextClassificationPipeline:
    """Complete text classification pipeline."""

    def __init__(self, model_type='logistic', max_features=5000):
        self.model_type = model_type
        self.max_features = max_features
        self.vectorizer = None
        self.model = None

    def _get_model(self):
        if self.model_type == 'logistic':
            return LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == 'svm':
            return LinearSVC(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == 'nb':
            return MultinomialNB()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def fit(self, X_train, y_train):
        """Fit the pipeline."""
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 2),
            stop_words='english'
        )

        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.model = self._get_model()
        self.model.fit(X_train_vec, y_train)

        return self

    def predict(self, X):
        """Predict labels."""
        X_vec = self.vectorizer.transform(X)
        return self.model.predict(X_vec)

    def evaluate(self, X_test, y_test):
        """Evaluate the model."""
        y_pred = self.predict(X_test)

        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)

        return {
            'classification_report': report,
            'confusion_matrix': cm,
            'predictions': y_pred
        }

    def cross_validate(self, X, y, cv=5):
        """Cross-validate the model."""
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=self.max_features,
                min_df=2,
                stop_words='english'
            )),
            ('clf', self._get_model())
        ])

        scores = cross_val_score(
            pipeline, X, y,
            cv=cv,
            scoring='f1_macro'
        )

        return {
            'mean': scores.mean(),
            'std': scores.std(),
            'scores': scores
        }

# Usage
pipeline = TextClassificationPipeline(model_type='logistic')
pipeline.fit(X_train, y_train)
results = pipeline.evaluate(X_test, y_test)
print(classification_report(y_test, results['predictions']))

cv_results = pipeline.cross_validate(texts, labels)
print(f"CV F1-macro: {cv_results['mean']:.3f} (+/- {cv_results['std']*2:.3f})")
```
