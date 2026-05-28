# Text Visualization in Python

## Package Versions

```python
# Tested with:
# Python 3.10
# matplotlib 3.7.1
# seaborn 0.12.2
# wordcloud 1.9.2
# plotly 5.15.0
```

## Installation

```bash
pip install matplotlib seaborn wordcloud plotly pandas numpy
```

## Term Frequency Plots

### Basic Bar Chart

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np

# Sample word frequencies
texts = ["The economy shows growth", "Climate change impacts", "Healthcare reform needed"] * 50
words = ' '.join(texts).lower().split()
word_freq = Counter(words)

# Get top N
top_words = pd.DataFrame(
    word_freq.most_common(20),
    columns=['word', 'frequency']
)

# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_words['word'], top_words['frequency'], color='steelblue')
ax.set_xlabel('Frequency')
ax.set_ylabel('Word')
ax.set_title('Top 20 Most Frequent Words')
ax.invert_yaxis()  # Highest at top

plt.tight_layout()
plt.savefig('output/figures/term_frequency.png', dpi=300)
plt.close()
```

### Seaborn Style

```python
# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=top_words,
    y='word',
    x='frequency',
    palette='Blues_r',
    ax=ax
)
ax.set_title('Term Frequency', fontsize=14, fontweight='bold')
ax.set_xlabel('Frequency')
ax.set_ylabel('')

plt.tight_layout()
plt.savefig('output/figures/term_frequency_sns.png', dpi=300)
plt.close()
```

## Word Clouds

```python
from wordcloud import WordCloud

# Basic word cloud
text = ' '.join(texts)

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='Blues',
    max_words=100
).generate(text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud', fontsize=14)
plt.tight_layout()
plt.savefig('output/figures/wordcloud.png', dpi=300)
plt.close()
```

### Word Cloud from Frequencies

```python
# From frequency dict
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white'
).generate_from_frequencies(word_freq)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('output/figures/wordcloud_freq.png', dpi=300)
plt.close()
```

## Sentiment Visualization

### Sentiment Distribution

```python
# Sample sentiment scores
np.random.seed(42)
sentiment_scores = np.random.normal(0.1, 0.3, 200)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(sentiment_scores, bins=30, color='steelblue', edgecolor='white', alpha=0.7)
ax.axvline(x=0, color='red', linestyle='--', label='Neutral', linewidth=2)
ax.axvline(x=sentiment_scores.mean(), color='green', linestyle='-',
           label=f'Mean ({sentiment_scores.mean():.2f})', linewidth=2)

ax.set_xlabel('Sentiment Score')
ax.set_ylabel('Count')
ax.set_title('Distribution of Sentiment Scores')
ax.legend()

plt.tight_layout()
plt.savefig('output/figures/sentiment_distribution.png', dpi=300)
plt.close()
```

### Sentiment Over Time

```python
from datetime import datetime, timedelta

# Sample time series
dates = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(365)]
daily_sentiment = np.sin(np.linspace(0, 4*np.pi, 365)) * 0.3 + np.random.normal(0, 0.1, 365)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(dates, daily_sentiment, color='steelblue', alpha=0.5, linewidth=1)

# Add rolling average
rolling = pd.Series(daily_sentiment).rolling(window=14).mean()
ax.plot(dates, rolling, color='red', linewidth=2, label='14-day average')

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Date')
ax.set_ylabel('Sentiment')
ax.set_title('Sentiment Over Time')
ax.legend()

plt.tight_layout()
plt.savefig('output/figures/sentiment_time.png', dpi=300)
plt.close()
```

### Sentiment by Group

```python
# Sample grouped sentiment
groups = ['Group A', 'Group B', 'Group C']
means = [0.15, -0.08, 0.22]
stds = [0.05, 0.06, 0.04]

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#3498db', '#e74c3c', '#2ecc71']

bars = ax.bar(groups, means, yerr=stds, capsize=5, color=colors, edgecolor='black')
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_ylabel('Mean Sentiment')
ax.set_title('Sentiment by Group')

# Add value labels
for bar, mean in zip(bars, means):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{mean:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('output/figures/sentiment_groups.png', dpi=300)
plt.close()
```

## Topic Model Visualization

### Topic Prevalence

```python
# Sample topic prevalence
topics = [f'Topic {i+1}' for i in range(10)]
labels = ['Economy', 'Healthcare', 'Climate', 'Education', 'Technology',
          'Immigration', 'Crime', 'Foreign Policy', 'Media', 'Elections']
prevalence = [0.15, 0.12, 0.11, 0.10, 0.10, 0.09, 0.09, 0.08, 0.08, 0.08]

# Sort by prevalence
sorted_idx = np.argsort(prevalence)[::-1]
sorted_labels = [labels[i] for i in sorted_idx]
sorted_prev = [prevalence[i] for i in sorted_idx]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(sorted_labels, sorted_prev, color='steelblue')
ax.set_xlabel('Prevalence')
ax.set_title('Topic Prevalence')
ax.invert_yaxis()

# Format as percentage
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

plt.tight_layout()
plt.savefig('output/figures/topic_prevalence.png', dpi=300)
plt.close()
```

### Topic Top Words

```python
# Sample topic-word data
topic_words = {
    'Economy': ['economy', 'growth', 'jobs', 'tax', 'market'],
    'Healthcare': ['health', 'care', 'hospital', 'doctor', 'insurance'],
    'Climate': ['climate', 'change', 'carbon', 'emissions', 'energy']
}

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

for ax, (topic, words) in zip(axes, topic_words.items()):
    weights = np.linspace(1, 0.5, len(words))
    ax.barh(words[::-1], weights[::-1], color='steelblue')
    ax.set_title(topic, fontsize=12, fontweight='bold')
    ax.set_xlim(0, 1.1)

plt.tight_layout()
plt.savefig('output/figures/topic_words.png', dpi=300)
plt.close()
```

### Topic Over Time

```python
# Sample topic prevalence over time
years = range(2015, 2024)
topic_trends = {
    'Climate': [0.05, 0.06, 0.07, 0.08, 0.10, 0.12, 0.14, 0.15, 0.16],
    'Economy': [0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.08],
    'Healthcare': [0.10, 0.10, 0.11, 0.12, 0.15, 0.18, 0.12, 0.11, 0.10]
}

fig, ax = plt.subplots(figsize=(10, 6))

for topic, values in topic_trends.items():
    ax.plot(years, values, marker='o', linewidth=2, label=topic)

ax.set_xlabel('Year')
ax.set_ylabel('Topic Prevalence')
ax.set_title('Topic Trends Over Time')
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

plt.tight_layout()
plt.savefig('output/figures/topic_trends.png', dpi=300)
plt.close()
```

## Classification Visualization

### Confusion Matrix

```python
import seaborn as sns

# Sample confusion matrix
classes = ['Politics', 'Sports', 'Business', 'Science']
cm = np.array([
    [45, 3, 2, 0],
    [2, 47, 1, 0],
    [3, 1, 44, 2],
    [0, 1, 3, 46]
])

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=classes,
    yticklabels=classes,
    ax=ax
)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix')

plt.tight_layout()
plt.savefig('output/figures/confusion_matrix.png', dpi=300)
plt.close()
```

### Normalized Confusion Matrix

```python
# Normalize by row (recall)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    cm_normalized,
    annot=True,
    fmt='.2f',
    cmap='Blues',
    xticklabels=classes,
    yticklabels=classes,
    ax=ax,
    vmin=0,
    vmax=1
)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix (Normalized)')

plt.tight_layout()
plt.savefig('output/figures/confusion_matrix_norm.png', dpi=300)
plt.close()
```

### ROC Curve

```python
from sklearn.metrics import roc_curve, auc

# Sample predictions
np.random.seed(42)
y_true = np.random.binomial(1, 0.5, 200)
y_scores = y_true * 0.6 + np.random.normal(0, 0.3, 200)

fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color='steelblue', linewidth=2,
        label=f'ROC curve (AUC = {roc_auc:.2f})')
ax.plot([0, 1], [0, 1], color='gray', linestyle='--')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.05])
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve')
ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig('output/figures/roc_curve.png', dpi=300)
plt.close()
```

## Embedding Visualization

### 2D Scatter Plot

```python
# Sample embeddings (reduced to 2D)
np.random.seed(42)
n_points = 100
embeddings_2d = np.random.randn(n_points, 2)
clusters = np.random.choice([0, 1, 2, 3], n_points)

fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=clusters,
    cmap='viridis',
    alpha=0.7,
    s=50
)
plt.colorbar(scatter, label='Cluster')
ax.set_xlabel('Dimension 1')
ax.set_ylabel('Dimension 2')
ax.set_title('Document Embeddings')

plt.tight_layout()
plt.savefig('output/figures/embeddings_2d.png', dpi=300)
plt.close()
```

## Interactive Plots with Plotly

### Interactive Topic Visualization

```python
import plotly.express as px
import plotly.graph_objects as go

# Sample data
df_topics = pd.DataFrame({
    'Topic': labels,
    'Prevalence': prevalence,
    'Words': ['word1, word2, word3'] * 10
})

fig = px.bar(
    df_topics,
    x='Prevalence',
    y='Topic',
    orientation='h',
    hover_data=['Words'],
    title='Topic Prevalence'
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
fig.write_html('output/figures/topic_prevalence_interactive.html')
```

### Interactive Embeddings

```python
# Sample with text
df_embed = pd.DataFrame({
    'x': embeddings_2d[:, 0],
    'y': embeddings_2d[:, 1],
    'cluster': [f'Cluster {c}' for c in clusters],
    'text': [f'Document {i}' for i in range(n_points)]
})

fig = px.scatter(
    df_embed,
    x='x',
    y='y',
    color='cluster',
    hover_data=['text'],
    title='Document Embeddings'
)
fig.write_html('output/figures/embeddings_interactive.html')
```

## Publication-Ready Formatting

### Set Publication Style

```python
def set_publication_style():
    """Set matplotlib style for publications."""
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.figsize': (8, 6),
        'figure.dpi': 100,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.spines.top': False,
        'axes.spines.right': False,
    })

set_publication_style()
```

### Colorblind-Friendly Palette

```python
# Okabe-Ito palette (colorblind-friendly)
OKABE_ITO = [
    '#E69F00',  # Orange
    '#56B4E9',  # Sky blue
    '#009E73',  # Bluish green
    '#F0E442',  # Yellow
    '#0072B2',  # Blue
    '#D55E00',  # Vermillion
    '#CC79A7',  # Reddish purple
    '#999999',  # Gray
]

# Use in plots
fig, ax = plt.subplots()
for i, (topic, values) in enumerate(topic_trends.items()):
    ax.plot(years, values, marker='o', color=OKABE_ITO[i], label=topic)
ax.legend()
```

### Saving Figures

```python
def save_figure(fig, filename, formats=['png', 'pdf']):
    """Save figure in multiple formats."""
    for fmt in formats:
        filepath = f'output/figures/{filename}.{fmt}'
        fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {filepath}")

# Usage
fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C'], [1, 2, 3])
save_figure(fig, 'example_figure')
plt.close()
```

## pyLDAvis for Topic Models

```python
import pyLDAvis
import pyLDAvis.gensim_models

# Assuming you have a trained gensim LDA model
# vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
# pyLDAvis.save_html(vis_data, 'output/figures/lda_vis.html')

# For sklearn LDA
# from pyLDAvis import sklearn as pyLDAvis_sklearn
# vis_data = pyLDAvis_sklearn.prepare(lda, dtm, vectorizer)
# pyLDAvis.save_html(vis_data, 'output/figures/sklearn_lda_vis.html')
```

## Complete Visualization Suite

```python
class TextVisualizer:
    """Complete text visualization suite."""

    def __init__(self, style='publication'):
        if style == 'publication':
            set_publication_style()
        self.colors = OKABE_ITO

    def term_frequency(self, word_counts, top_n=20, title='Term Frequency'):
        """Plot term frequency bar chart."""
        if isinstance(word_counts, dict):
            df = pd.DataFrame(list(word_counts.items()), columns=['word', 'freq'])
        else:
            df = word_counts.copy()

        df = df.nlargest(top_n, 'freq' if 'freq' in df.columns else df.columns[1])

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df.iloc[:, 0], df.iloc[:, 1], color=self.colors[0])
        ax.set_xlabel('Frequency')
        ax.set_title(title)
        ax.invert_yaxis()

        return fig

    def sentiment_distribution(self, scores, title='Sentiment Distribution'):
        """Plot sentiment distribution."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(scores, bins=30, color=self.colors[0], edgecolor='white', alpha=0.7)
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax.axvline(x=np.mean(scores), color='green', linestyle='-', linewidth=2)
        ax.set_xlabel('Sentiment Score')
        ax.set_ylabel('Count')
        ax.set_title(title)

        return fig

    def confusion_matrix(self, cm, labels, title='Confusion Matrix', normalize=False):
        """Plot confusion matrix."""
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            fmt = '.2f'
        else:
            fmt = 'd'

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt=fmt, cmap='Blues',
                   xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title(title)

        return fig

    def save(self, fig, filename):
        """Save figure."""
        save_figure(fig, filename)

# Usage
viz = TextVisualizer()
fig = viz.term_frequency(word_freq)
viz.save(fig, 'term_freq')
plt.close()
```
