# Recommendation Diversity & Fairness

This guide covers patterns for ensuring diverse and fair recommendations.

## Maximal Marginal Relevance (MMR)

### SQL Implementation

```sql
-- Maximal Marginal Relevance for diverse recommendations
CREATE OR REPLACE TABLE `project.recommendation.diverse_recommendations` AS
WITH base_recommendations AS (
  SELECT
    user_id,
    product_id,
    predicted_rating,
    category,
    subcategory,
    price_bucket,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY predicted_rating DESC) as rank
  FROM ML.RECOMMEND(MODEL `project.recommendation.collaborative_model`)
  JOIN `project.catalog.products` USING (product_id)
),
mmr_selection AS (
  SELECT
    user_id,
    product_id,
    predicted_rating,
    category,
    -- MMR score: balance relevance and diversity
    predicted_rating -
    0.3 * COUNT(*) OVER (
      PARTITION BY user_id, category
      ORDER BY rank
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as mmr_score
  FROM base_recommendations
  WHERE rank <= 100
)
SELECT
  user_id,
  ARRAY_AGG(
    STRUCT(product_id, predicted_rating, category)
    ORDER BY mmr_score DESC
    LIMIT 10
  ) as diverse_recommendations
FROM mmr_selection
GROUP BY user_id;
```

### Python Implementation

```python
# src/recommendation/diversity.py
from typing import List, Dict
import numpy as np

def optimize_diversity(
    candidates: List[Dict],
    n_select: int,
    alpha: float = 0.5,
    diversity_features: List[str] = ['category', 'price_bucket', 'brand']
) -> List[Dict]:
    """
    Maximize diversity using MMR (Maximal Marginal Relevance).

    Args:
        candidates: List of candidate items with scores and features
        n_select: Number of items to select
        alpha: Balance between relevance (1.0) and diversity (0.0)
        diversity_features: Features to consider for diversity

    Returns:
        List of selected items maximizing diversity
    """
    selected = []
    remaining = candidates.copy()

    # Select first item (highest relevance)
    first_item = max(remaining, key=lambda x: x['score'])
    selected.append(first_item)
    remaining.remove(first_item)

    # Iteratively select items maximizing MMR
    for _ in range(n_select - 1):
        if not remaining:
            break

        mmr_scores = []
        for candidate in remaining:
            # Relevance score
            relevance = candidate['score']

            # Diversity score (minimum similarity to selected items)
            similarities = [
                calculate_similarity(candidate, sel, diversity_features)
                for sel in selected
            ]
            diversity = 1 - max(similarities) if similarities else 1.0

            # MMR score
            mmr = alpha * relevance + (1 - alpha) * diversity
            mmr_scores.append((candidate, mmr))

        # Select item with highest MMR
        next_item = max(mmr_scores, key=lambda x: x[1])[0]
        selected.append(next_item)
        remaining.remove(next_item)

    return selected

def calculate_similarity(item1: Dict, item2: Dict, features: List[str]) -> float:
    """Calculate similarity between two items based on features."""
    matches = sum(
        1 for feature in features
        if item1.get(feature) == item2.get(feature)
    )
    return matches / len(features)
```

## Fairness Metrics

### Category Representation Fairness

```sql
-- Monitor category representation fairness
CREATE OR REPLACE TABLE `project.monitoring.recommendation_fairness` AS
WITH recommendation_distribution AS (
  SELECT
    r.user_id,
    p.category,
    COUNT(*) as recommended_count
  FROM `project.recommendation.user_recommendations` r,
       UNNEST(recommendations) rec
  JOIN `project.catalog.products` p ON rec.product_id = p.product_id
  GROUP BY r.user_id, p.category
),
catalog_distribution AS (
  SELECT
    category,
    COUNT(*) as total_products,
    COUNT(*) / SUM(COUNT(*)) OVER () as catalog_proportion
  FROM `project.catalog.products`
  WHERE is_active = TRUE
  GROUP BY category
)
SELECT
  rd.category,
  AVG(rd.recommended_count) as avg_recommendations,
  cd.catalog_proportion,
  -- Fairness ratio: should be close to 1.0
  AVG(rd.recommended_count) / (cd.catalog_proportion * 10) as fairness_ratio,
  CASE
    WHEN AVG(rd.recommended_count) / (cd.catalog_proportion * 10) < 0.5 THEN 'Under-represented'
    WHEN AVG(rd.recommended_count) / (cd.catalog_proportion * 10) > 2.0 THEN 'Over-represented'
    ELSE 'Balanced'
  END as representation_status
FROM recommendation_distribution rd
JOIN catalog_distribution cd USING (category)
GROUP BY rd.category, cd.catalog_proportion;
```

### Demographic Parity

```sql
-- Check for demographic parity in recommendations
CREATE OR REPLACE TABLE `project.monitoring.demographic_parity` AS
WITH user_demographics AS (
  SELECT
    user_id,
    age_group,
    gender,
    location
  FROM `project.user_profiles`
),
recommendation_quality AS (
  SELECT
    u.user_id,
    u.age_group,
    u.gender,
    AVG(r.predicted_rating) as avg_recommendation_quality,
    COUNT(*) as recommendation_count
  FROM user_demographics u
  JOIN `project.recommendation.user_recommendations` r USING (user_id)
  GROUP BY u.user_id, u.age_group, u.gender
)
SELECT
  age_group,
  gender,
  AVG(avg_recommendation_quality) as avg_quality,
  STDDEV(avg_recommendation_quality) as quality_stddev,
  -- Check if quality variance is within acceptable bounds
  CASE
    WHEN STDDEV(avg_recommendation_quality) < 0.05 THEN 'Fair'
    WHEN STDDEV(avg_recommendation_quality) < 0.10 THEN 'Moderate'
    ELSE 'Unfair'
  END as fairness_assessment
FROM recommendation_quality
GROUP BY age_group, gender;
```

## Diversity Constraints

### Hard Constraints

```python
# src/recommendation/constraints.py
from typing import List, Dict, Set

def apply_diversity_constraints(
    recommendations: List[Dict],
    constraints: Dict[str, int]
) -> List[Dict]:
    """
    Apply hard diversity constraints to recommendations.

    Args:
        recommendations: Sorted list of recommendations by score
        constraints: Dict of feature -> max count (e.g., {'category': 3, 'brand': 2})

    Returns:
        Filtered recommendations meeting constraints
    """
    selected = []
    feature_counts = {feature: {} for feature in constraints.keys()}

    for rec in recommendations:
        # Check all constraints
        can_add = True
        for feature, max_count in constraints.items():
            feature_value = rec.get(feature)
            current_count = feature_counts[feature].get(feature_value, 0)

            if current_count >= max_count:
                can_add = False
                break

        if can_add:
            selected.append(rec)
            # Update counts
            for feature in constraints.keys():
                feature_value = rec.get(feature)
                feature_counts[feature][feature_value] = \
                    feature_counts[feature].get(feature_value, 0) + 1

    return selected
```

### Soft Constraints with Penalty

```python
def diversity_aware_ranking(
    recommendations: List[Dict],
    diversity_penalty: float = 0.1
) -> List[Dict]:
    """
    Re-rank recommendations with diversity penalty for repeated features.

    Args:
        recommendations: List of recommendations with scores
        diversity_penalty: Penalty applied for each duplicate feature

    Returns:
        Re-ranked recommendations
    """
    seen_categories = set()
    seen_brands = set()

    for rec in recommendations:
        original_score = rec['score']
        penalty = 0.0

        if rec['category'] in seen_categories:
            penalty += diversity_penalty
        if rec['brand'] in seen_brands:
            penalty += diversity_penalty

        rec['adjusted_score'] = original_score - penalty

        seen_categories.add(rec['category'])
        seen_brands.add(rec['brand'])

    # Re-sort by adjusted score
    return sorted(recommendations, key=lambda x: x['adjusted_score'], reverse=True)
```

## Popularity Bias Mitigation

```python
# src/recommendation/debiasing.py
import numpy as np

def debias_recommendations(
    recommendations: List[Dict],
    popularity_scores: Dict[str, float],
    debias_strength: float = 0.5
) -> List[Dict]:
    """
    Reduce popularity bias in recommendations.

    Args:
        recommendations: List of recommendations with scores
        popularity_scores: Dict mapping product_id to popularity (0-1)
        debias_strength: How much to debias (0=no change, 1=full debias)

    Returns:
        Debiased recommendations
    """
    for rec in recommendations:
        product_id = rec['product_id']
        popularity = popularity_scores.get(product_id, 0.5)

        # Boost less popular items
        popularity_boost = (1 - popularity) * debias_strength
        rec['debiased_score'] = rec['score'] * (1 + popularity_boost)

    return sorted(recommendations, key=lambda x: x['debiased_score'], reverse=True)
```

## Best Practices

- Use MMR (α=0.5-0.7) for balancing relevance and diversity
- Monitor fairness metrics across user demographics
- Apply hard constraints for critical diversity requirements (e.g., max 3 items per category)
- Use soft constraints/penalties for flexible diversity
- Mitigate popularity bias by boosting long-tail items
- Track catalog coverage (% of products recommended at least once)
- Ensure demographic parity in recommendation quality
- A/B test diversity settings to find optimal balance
- Report fairness metrics in production dashboards
