---
title: Use Counter for Frequency Counting
impact: HIGH
impactDescription: 2-3× faster than manual dict counting
tags: ds, counter, collections, frequency
---

## Use Counter for Frequency Counting

Manual counting with dictionaries is verbose and slower than `collections.Counter`, which is implemented in C and provides useful methods.

**Incorrect (manual counting):**

```python
def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        word = word.lower()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
```

**Correct (Counter, optimized implementation):**

```python
from collections import Counter

def count_words(text: str) -> Counter[str]:
    return Counter(word.lower() for word in text.split())
```

**Counter provides useful methods:**

```python
word_counts = Counter(words)

# Most common items
top_10 = word_counts.most_common(10)

# Combine counters
total = word_counts + other_counts

# Subtract counts
remaining = word_counts - processed_counts

# Elements iterator (repeat by count)
all_words = list(word_counts.elements())
```

Reference: [Counter documentation](https://docs.python.org/3/library/collections.html#collections.Counter)
