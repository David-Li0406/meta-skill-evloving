# Cold Start Problem Solutions

This guide covers strategies for handling new users and products in recommendation systems.

## New User Recommendations

### Popularity-Based Baseline

```sql
-- Handle users with <5 interactions using popularity baseline
CREATE OR REPLACE TABLE `project.recommendation.cold_start_new_users` AS
WITH new_users AS (
  SELECT user_id
  FROM `project.raw.user_events`
  GROUP BY user_id
  HAVING COUNT(*) < 5
),
popular_products AS (
  -- Global popularity baseline
  SELECT
    product_id,
    COUNT(DISTINCT user_id) as unique_viewers,
    COUNTIF(event_type = 'purchase') as purchase_count,
    COUNTIF(event_type = 'purchase') / NULLIF(COUNTIF(event_type = 'view'), 0) as conversion_rate
  FROM `project.raw.user_events`
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  GROUP BY product_id
  HAVING unique_viewers > 100
),
trending_products AS (
  -- Velocity-based trending items
  SELECT
    product_id,
    COUNT(*) as recent_interactions,
    COUNT(*) / NULLIF(
      LAG(COUNT(*)) OVER (PARTITION BY product_id ORDER BY DATE(event_timestamp)),
      0
    ) as trend_score
  FROM `project.raw.user_events`
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 3 DAY)
  GROUP BY product_id, DATE(event_timestamp)
)
SELECT
  nu.user_id,
  pp.product_id,
  -- Weighted score: 50% popularity, 30% trending, 20% conversion
  (pp.purchase_count * 0.5 +
   COALESCE(tp.trend_score, 1) * 0.3 +
   pp.conversion_rate * 0.2) as recommendation_score,
  'cold_start_popularity' as recommendation_reason
FROM new_users nu
CROSS JOIN popular_products pp
LEFT JOIN trending_products tp USING (product_id)
QUALIFY ROW_NUMBER() OVER (PARTITION BY nu.user_id ORDER BY recommendation_score DESC) <= 20;
```

## User Segmentation Handler

```python
# src/recommendation/cold_start.py
from enum import Enum
from typing import List, Dict, Optional
from google.cloud import bigquery

class UserSegment(Enum):
    NEW_USER = "new_user"  # <5 interactions
    CASUAL_USER = "casual_user"  # 5-20 interactions
    ACTIVE_USER = "active_user"  # >20 interactions

class ColdStartRecommender:
    """Handle recommendations for new users and products."""

    def __init__(self, bq_client: bigquery.Client):
        self.bq_client = bq_client

    def classify_user(self, user_id: str) -> UserSegment:
        """Classify user based on interaction history."""
        query = f"""
        SELECT COUNT(*) as interaction_count
        FROM `project.raw.user_events`
        WHERE user_id = '{user_id}'
        """
        result = list(self.bq_client.query(query).result())[0]
        count = result.interaction_count

        if count < 5:
            return UserSegment.NEW_USER
        elif count < 20:
            return UserSegment.CASUAL_USER
        else:
            return UserSegment.ACTIVE_USER

    def get_recommendations(
        self,
        user_id: str,
        n_items: int = 10,
        user_attributes: Optional[Dict] = None
    ) -> List[Dict]:
        """Get recommendations based on user segment."""

        segment = self.classify_user(user_id)

        if segment == UserSegment.NEW_USER:
            # Use popularity + user attributes
            return self._get_popularity_based(n_items, user_attributes)
        elif segment == UserSegment.CASUAL_USER:
            # Hybrid: 70% collaborative, 30% popular
            collab_recs = self._get_collaborative(user_id, int(n_items * 0.7))
            popular_recs = self._get_popularity_based(int(n_items * 0.3), user_attributes)
            return collab_recs + popular_recs
        else:
            # Full collaborative filtering
            return self._get_collaborative(user_id, n_items)

    def _get_popularity_based(self, n_items: int, user_attributes: Optional[Dict] = None) -> List[Dict]:
        """Get popular items, optionally filtered by user attributes."""
        # Implementation here
        pass

    def _get_collaborative(self, user_id: str, n_items: int) -> List[Dict]:
        """Get collaborative filtering recommendations."""
        # Implementation here
        pass
```

## New Product Recommendations

```sql
-- Handle new products with <100 interactions
CREATE OR REPLACE TABLE `project.recommendation.cold_start_new_products` AS
WITH new_products AS (
  SELECT product_id
  FROM `project.raw.user_events`
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  GROUP BY product_id
  HAVING COUNT(*) < 100
),
similar_products AS (
  -- Find similar products based on category and attributes
  SELECT
    np.product_id as new_product_id,
    p.product_id as similar_product_id,
    -- Similarity score based on attributes
    (
      IF(np.category = p.category, 1.0, 0.0) * 0.5 +
      IF(np.brand = p.brand, 1.0, 0.0) * 0.3 +
      (1 - ABS(np.price - p.price) / GREATEST(np.price, p.price)) * 0.2
    ) as similarity_score
  FROM `project.catalog.products` np
  JOIN new_products USING (product_id)
  JOIN `project.catalog.products` p
    ON p.product_id != np.product_id
    AND p.is_active = TRUE
  WHERE similarity_score > 0.5
  QUALIFY ROW_NUMBER() OVER (PARTITION BY np.product_id ORDER BY similarity_score DESC) <= 10
)
-- Recommend new products to users who liked similar products
SELECT
  ue.user_id,
  sp.new_product_id as product_id,
  AVG(sp.similarity_score) * COUNT(*) as recommendation_score,
  'cold_start_similar_products' as recommendation_reason
FROM similar_products sp
JOIN `project.raw.user_events` ue
  ON ue.product_id = sp.similar_product_id
  AND ue.event_type IN ('purchase', 'add_to_cart')
  AND ue.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY ue.user_id, sp.new_product_id
QUALIFY ROW_NUMBER() OVER (PARTITION BY ue.user_id ORDER BY recommendation_score DESC) <= 5;
```

## Attribute-Based Recommendations

```python
# src/recommendation/attribute_based.py
from typing import List, Dict
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class AttributeBasedRecommender:
    """Content-based recommendations using product attributes."""

    def __init__(self, product_features: pd.DataFrame):
        """
        Args:
            product_features: DataFrame with columns [product_id, category, brand, price, ...]
        """
        self.product_features = product_features
        self.similarity_matrix = None

    def fit(self):
        """Compute similarity matrix from product attributes."""
        # One-hot encode categorical features
        encoded = pd.get_dummies(
            self.product_features,
            columns=['category', 'brand', 'color']
        )

        # Normalize numerical features
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        encoded[['price', 'rating']] = scaler.fit_transform(encoded[['price', 'rating']])

        # Compute cosine similarity
        self.similarity_matrix = cosine_similarity(encoded.drop('product_id', axis=1))

    def recommend_for_new_product(self, product_id: str, n_items: int = 10) -> List[str]:
        """Recommend users for a new product based on attribute similarity."""
        product_idx = self.product_features[
            self.product_features['product_id'] == product_id
        ].index[0]

        # Get most similar products
        similarities = self.similarity_matrix[product_idx]
        similar_indices = similarities.argsort()[-n_items-1:-1][::-1]

        similar_products = self.product_features.iloc[similar_indices]['product_id'].tolist()
        return similar_products
```

## Best Practices

- Use popularity baseline for users with <5 interactions
- Gradually transition from popularity to collaborative as users engage more
- For new products, leverage content-based similarity with existing products
- Combine multiple signals (popularity + trending + conversion rate)
- Monitor cold start user conversion rates separately
- A/B test different cold start strategies
- Use user demographic attributes when available (location, age, device type)
- Track "time to warm start" metrics (how long until users have enough data)
