---
name: recommendation-ml
description: ML recommendation system development with collaborative filtering (Matrix Factorization), content-based filtering, and hybrid approaches. Use when building recommendation models, implementing Feast feature stores, setting up MLflow model registry, handling cold-start problems for new users/products, implementing diversity with MMR algorithm, or adding exploration with Thompson Sampling/epsilon-greedy bandits.
---

# Recommendation ML Development Skill

Build recommendation systems for e-commerce following ML best practices.

## Recommendation System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ User Events  │ Product Data │ Transaction  │ User Profile   │
│ (Clicks,     │ (Catalog,    │ (Purchases,  │ (Demographics, │
│  Views)      │  Categories) │  Cart)       │  Preferences)  │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬────────┘
       │              │              │               │
       v              v              v               v
┌─────────────────────────────────────────────────────────────┐
│              BigQuery Data Warehouse                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                Feature Engineering                     │   │
│  ├──────────────┬──────────────┬────────────────────────┤   │
│  │User Features │Product Ftrs  │ Interaction Features   │   │
│  └──────────────┴──────────────┴────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 BigQuery ML Models                    │   │
│  ├────────────────────┬─────────────────────────────────┤   │
│  │ Matrix Factorization│ Wide-and-Deep / DNN           │   │
│  │ (Collaborative)     │ (Content + Collaborative)     │   │
│  └────────────────────┴─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│                   Serving Layer                              │
├────────────────────────┬────────────────────────────────────┤
│   Real-time API        │   Batch Recommendations            │
│   (Vertex AI Endpoint) │   (BigQuery → Redis/Firestore)     │
└────────────────────────┴────────────────────────────────────┘
```

## Recommendation Types

### 1. Collaborative Filtering (User-Based)
```sql
-- Users who bought X also bought Y
CREATE OR REPLACE MODEL `project.recommendation.collaborative_model`
OPTIONS(
    model_type = 'MATRIX_FACTORIZATION',
    feedback_type = 'IMPLICIT',
    user_col = 'user_id',
    item_col = 'product_id',
    rating_col = 'interaction_score',
    num_factors = 64,
    l2_reg = 0.1,
    max_iterations = 30,
    wals_alpha = 10
) AS
SELECT
    user_id,
    product_id,
    -- Weighted interaction score
    SUM(
        CASE event_type
            WHEN 'view' THEN 1
            WHEN 'add_to_cart' THEN 3
            WHEN 'add_to_wishlist' THEN 2
            WHEN 'purchase' THEN 5
        END
    ) as interaction_score
FROM `project.raw.user_events`
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
GROUP BY user_id, product_id
HAVING interaction_score >= 2  -- Filter noise
```

### 2. Content-Based Filtering
```sql
-- Similar products based on attributes
CREATE OR REPLACE TABLE `project.recommendation.product_similarity` AS
WITH product_vectors AS (
    SELECT
        product_id,
        -- One-hot encode categories
        IF(category = 'tops', 1, 0) as cat_tops,
        IF(category = 'bottoms', 1, 0) as cat_bottoms,
        IF(category = 'outerwear', 1, 0) as cat_outerwear,
        -- Normalize price (0-1)
        (price - MIN(price) OVER()) / (MAX(price) OVER() - MIN(price) OVER()) as price_norm,
        -- Color embedding
        color_embedding,
        -- Style attributes
        is_casual,
        is_formal,
        is_sporty
    FROM `project.catalog.products`
)
SELECT
    a.product_id as product_id,
    b.product_id as similar_product_id,
    -- Cosine similarity calculation
    (
        a.cat_tops * b.cat_tops +
        a.cat_bottoms * b.cat_bottoms +
        a.cat_outerwear * b.cat_outerwear +
        (1 - ABS(a.price_norm - b.price_norm)) +
        a.is_casual * b.is_casual +
        a.is_formal * b.is_formal
    ) / 6.0 as similarity_score
FROM product_vectors a
CROSS JOIN product_vectors b
WHERE a.product_id != b.product_id
QUALIFY ROW_NUMBER() OVER(PARTITION BY a.product_id ORDER BY similarity_score DESC) <= 20
```

### 3. Hybrid Recommendation
```sql
-- Combine collaborative and content-based
CREATE OR REPLACE TABLE `project.recommendation.hybrid_recommendations` AS
WITH collaborative_recs AS (
    SELECT
        user_id,
        product_id,
        predicted_rating as collab_score,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY predicted_rating DESC) as collab_rank
    FROM ML.RECOMMEND(MODEL `project.recommendation.collaborative_model`)
    QUALIFY collab_rank <= 50
),
content_recs AS (
    SELECT
        ue.user_id,
        ps.similar_product_id as product_id,
        AVG(ps.similarity_score) as content_score
    FROM `project.raw.user_events` ue
    JOIN `project.recommendation.product_similarity` ps
        ON ue.product_id = ps.product_id
    WHERE ue.event_type = 'purchase'
        AND ue.event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    GROUP BY ue.user_id, ps.similar_product_id
)
SELECT
    COALESCE(c.user_id, ct.user_id) as user_id,
    COALESCE(c.product_id, ct.product_id) as product_id,
    -- Weighted hybrid score
    COALESCE(c.collab_score, 0) * 0.6 + COALESCE(ct.content_score, 0) * 0.4 as hybrid_score,
    c.collab_score,
    ct.content_score
FROM collaborative_recs c
FULL OUTER JOIN content_recs ct
    ON c.user_id = ct.user_id AND c.product_id = ct.product_id
WHERE COALESCE(c.collab_score, 0) * 0.6 + COALESCE(ct.content_score, 0) * 0.4 > 0.1
```

## Feature Store Integration

### Feast Setup for Recommendation Features

```python
# feature_repo/features.py
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta

# Define entities
user = Entity(name="user_id", value_type=ValueType.STRING, description="User ID")
product = Entity(name="product_id", value_type=ValueType.STRING, description="Product ID")

# User features from BigQuery
user_features_source = FileSource(
    path="gs://recommendation-features/user_features.parquet",
    event_timestamp_column="event_timestamp",
)

user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=90),
    features=[
        Feature(name="total_events", dtype=ValueType.INT64),
        Feature(name="total_spent", dtype=ValueType.FLOAT),
        Feature(name="days_since_last_visit", dtype=ValueType.INT64),
        Feature(name="preferred_categories", dtype=ValueType.STRING_LIST),
    ],
    batch_source=user_features_source,
)

# Product features
product_features = FeatureView(
    name="product_features",
    entities=["product_id"],
    ttl=timedelta(days=30),
    features=[
        Feature(name="popularity_score", dtype=ValueType.FLOAT),
        Feature(name="conversion_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_rating", dtype=ValueType.FLOAT),
    ],
    batch_source=FileSource(
        path="gs://recommendation-features/product_features.parquet",
        event_timestamp_column="event_timestamp",
    ),
)
```

### Online Feature Serving

```python
from feast import FeatureStore
from datetime import datetime

def get_features_for_inference(user_ids: list, product_ids: list) -> dict:
    """Fetch features for real-time recommendation serving."""

    store = FeatureStore(repo_path="feature_repo/")

    # Create entity rows for online retrieval
    entity_rows = [
        {
            "user_id": user_id,
            "product_id": product_id,
            "event_timestamp": datetime.now(),
        }
        for user_id, product_id in zip(user_ids, product_ids)
    ]

    # Get online features
    features = store.get_online_features(
        features=[
            "user_features:total_events",
            "user_features:total_spent",
            "product_features:popularity_score",
            "product_features:conversion_rate",
        ],
        entity_rows=entity_rows,
    ).to_dict()

    return features
```

### Point-in-Time Correctness for Training

```python
from feast import FeatureStore
import pandas as pd

def get_training_features(entity_df: pd.DataFrame) -> pd.DataFrame:
    """Get historical features with point-in-time correctness."""

    store = FeatureStore(repo_path="feature_repo/")

    # entity_df must have: user_id, product_id, event_timestamp
    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "user_features:total_events",
            "user_features:total_spent",
            "user_features:days_since_last_visit",
            "product_features:popularity_score",
            "product_features:conversion_rate",
        ],
    ).to_df()

    return training_df
```

## Model Registry with MLflow

### Model Versioning and Tracking

```python
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Start MLflow run
with mlflow.start_run(run_name="matrix_factorization_v1"):

    # Log parameters
    mlflow.log_param("num_factors", 50)
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("regularization", 0.1)
    mlflow.log_param("iterations", 20)

    # Train model (example with implicit library)
    from implicit.als import AlternatingLeastSquares

    model = AlternatingLeastSquares(
        factors=50,
        regularization=0.1,
        iterations=20,
    )
    model.fit(user_item_matrix)

    # Evaluate model
    predictions = model.recommend(user_ids, user_item_matrix, N=10)
    mae = calculate_mae(predictions, actual_interactions)
    rmse = calculate_rmse(predictions, actual_interactions)

    # Log metrics
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("coverage", calculate_coverage(predictions))

    # Log model
    mlflow.sklearn.log_model(model, "recommendation_model")

    # Tag model
    mlflow.set_tag("model_type", "collaborative_filtering")
    mlflow.set_tag("algorithm", "matrix_factorization")
```

### Champion/Challenger Deployment

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

def promote_to_production(run_id: str, model_name: str):
    """Promote model to production after validation."""

    # Register model
    model_uri = f"runs:/{run_id}/recommendation_model"
    model_details = mlflow.register_model(model_uri, model_name)

    # Transition to staging first
    client.transition_model_version_stage(
        name=model_name,
        version=model_details.version,
        stage="Staging",
    )

    # Run validation tests on staging
    if validate_staging_model(model_name, model_details.version):
        # Promote to production
        client.transition_model_version_stage(
            name=model_name,
            version=model_details.version,
            stage="Production",
        )
        print(f"Model version {model_details.version} promoted to production")
    else:
        print("Validation failed, model not promoted")

def get_production_model(model_name: str):
    """Get the current production model."""

    model_version = client.get_latest_versions(
        name=model_name,
        stages=["Production"]
    )[0]

    model = mlflow.pyfunc.load_model(
        model_uri=f"models:/{model_name}/{model_version.version}"
    )

    return model, model_version.version
```

### Model Comparison

```python
import mlflow
from mlflow.tracking import MlflowClient

def compare_models(experiment_name: str, metric: str = "mae") -> pd.DataFrame:
    """Compare all models in an experiment by metric."""

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} ASC"],
    )

    results = []
    for run in runs:
        results.append({
            "run_id": run.info.run_id,
            "model_type": run.data.tags.get("model_type"),
            "mae": run.data.metrics.get("mae"),
            "rmse": run.data.metrics.get("rmse"),
            "coverage": run.data.metrics.get("coverage"),
            "start_time": run.info.start_time,
        })

    return pd.DataFrame(results)
```

## Model Evaluation

### Offline Metrics
```sql
-- Calculate model metrics
SELECT
    'matrix_factorization' as model,
    -- Mean Absolute Error
    AVG(ABS(actual - predicted)) as mae,
    -- Root Mean Square Error  
    SQRT(AVG(POW(actual - predicted, 2))) as rmse,
    -- Coverage (% of items recommended)
    COUNT(DISTINCT predicted_product_id) / 
        (SELECT COUNT(DISTINCT product_id) FROM `project.catalog.products`) as coverage
FROM (
    SELECT
        i.user_id,
        i.product_id,
        i.interaction_score as actual,
        p.predicted_rating as predicted,
        p.product_id as predicted_product_id
    FROM `project.recommendation.test_interactions` i
    LEFT JOIN ML.RECOMMEND(MODEL `project.recommendation.collaborative_model`) p
        ON i.user_id = p.user_id AND i.product_id = p.product_id
)
```

### Precision@K and Recall@K
```sql
-- Precision@10 and Recall@10
WITH recommendations AS (
    SELECT
        user_id,
        ARRAY_AGG(product_id ORDER BY predicted_rating DESC LIMIT 10) as rec_products
    FROM ML.RECOMMEND(MODEL `project.recommendation.collaborative_model`)
    GROUP BY user_id
),
actuals AS (
    SELECT
        user_id,
        ARRAY_AGG(DISTINCT product_id) as actual_products
    FROM `project.raw.user_events`
    WHERE event_type = 'purchase'
        AND event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    GROUP BY user_id
)
SELECT
    AVG(
        (SELECT COUNT(*) FROM UNNEST(r.rec_products) rp 
         WHERE rp IN UNNEST(a.actual_products))
        / 10.0
    ) as precision_at_10,
    AVG(
        SAFE_DIVIDE(
            (SELECT COUNT(*) FROM UNNEST(r.rec_products) rp 
             WHERE rp IN UNNEST(a.actual_products)),
            ARRAY_LENGTH(a.actual_products)
        )
    ) as recall_at_10
FROM recommendations r
JOIN actuals a USING(user_id)
```

## A/B Testing Framework

```python
# src/recommendation/ab_test.py
from dataclasses import dataclass
from typing import List, Dict
import hashlib

@dataclass
class Experiment:
    name: str
    control_model: str
    treatment_model: str
    traffic_percent: float = 0.1  # 10% traffic to experiment

def get_user_bucket(user_id: str, experiment_name: str) -> str:
    """Deterministic bucketing for A/B test."""
    hash_input = f"{user_id}:{experiment_name}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    bucket = hash_value % 100
    return "treatment" if bucket < 10 else "control"

def get_recommendations(
    user_id: str,
    experiment: Experiment,
    n_items: int = 10
) -> List[Dict]:
    """Get recommendations based on A/B test bucket."""
    bucket = get_user_bucket(user_id, experiment.name)
    model = experiment.treatment_model if bucket == "treatment" else experiment.control_model
    
    # Query recommendations from model
    recommendations = query_model_recommendations(model, user_id, n_items)
    
    # Log for analysis
    log_recommendation_event(
        user_id=user_id,
        experiment=experiment.name,
        bucket=bucket,
        model=model,
        recommendations=recommendations
    )
    
    return recommendations
```

## Cold Start Problem Solutions

For comprehensive cold start strategies (new users, new products, popularity baselines, user segmentation), see [reference/cold-start.md](reference/cold-start.md).

### Quick Example - New User Recommendations

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
  SELECT
    product_id,
    COUNT(DISTINCT user_id) as unique_viewers,
    COUNTIF(event_type = 'purchase') as purchase_count
  FROM `project.raw.user_events`
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  GROUP BY product_id
  HAVING unique_viewers > 100
)
SELECT
  nu.user_id,
  pp.product_id,
  pp.purchase_count as recommendation_score
FROM new_users nu
CROSS JOIN popular_products pp
QUALIFY ROW_NUMBER() OVER (PARTITION BY nu.user_id ORDER BY recommendation_score DESC) <= 10;
```

## Recommendation Diversity & Fairness

For comprehensive diversity patterns (MMR algorithm, fairness metrics, diversity optimization), see [reference/fairness.md](reference/fairness.md).

### Diversity-Aware Recommendations (MMR)
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

### Fairness Metrics
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

### Diversity Optimization (Python)
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

## Model Explainability

### Feature Attribution
```sql
-- Explain why items are recommended
SELECT
  user_id,
  product_id,
  predicted_rating,
  -- Extract top contributing features
  ARRAY(
    SELECT AS STRUCT
      feature,
      importance,
      CASE feature
        WHEN 'user_total_purchases' THEN 'You frequently shop with us'
        WHEN 'product_popularity' THEN 'Trending item'
        WHEN 'category_affinity' THEN 'Matches your preferences'
        WHEN 'price_match' THEN 'In your typical price range'
        ELSE 'Similar to items you liked'
      END as explanation
    FROM UNNEST(ml_explain_features)
    ORDER BY importance DESC
    LIMIT 3
  ) as top_reasons,
  -- User-facing explanation
  CONCAT(
    'Recommended because: ',
    ARRAY_TO_STRING([
      (SELECT explanation FROM UNNEST((
        SELECT ARRAY_AGG(
          CASE feature
            WHEN 'user_total_purchases' THEN 'you frequently shop with us'
            WHEN 'product_popularity' THEN 'it\'s trending'
            WHEN 'category_affinity' THEN 'it matches your preferences'
            ELSE 'similar to items you liked'
          END
          ORDER BY importance DESC LIMIT 2
        )
        FROM UNNEST(ml_explain_features)
      )))
    ], ' and ')
  ) as user_facing_explanation
FROM ML.EXPLAIN_PREDICT(
  MODEL `project.recommendation.product_recommender`,
  (SELECT DISTINCT user_id FROM `project.recommendation.active_users` LIMIT 1000),
  STRUCT(5 AS top_k_features)
);
```

## Real-Time Personalization

### Session-Based Context Features
```sql
CREATE OR REPLACE TABLE `project.recommendation.contextual_features` AS
SELECT
  user_id,
  session_id,
  -- Time context
  EXTRACT(HOUR FROM event_timestamp) as hour_of_day,
  EXTRACT(DAYOFWEEK FROM event_timestamp) as day_of_week,
  CASE
    WHEN EXTRACT(DAYOFWEEK FROM event_timestamp) IN (1, 7) THEN 'weekend'
    ELSE 'weekday'
  END as day_type,
  -- Session context
  COUNT(*) OVER (PARTITION BY session_id ORDER BY event_timestamp) as session_position,
  TIMESTAMP_DIFF(
    event_timestamp,
    MIN(event_timestamp) OVER (PARTITION BY session_id),
    SECOND
  ) as seconds_in_session,
  -- Recent behavior
  ARRAY_AGG(
    product_id ORDER BY event_timestamp DESC LIMIT 5
  ) OVER (PARTITION BY user_id ORDER BY event_timestamp) as recent_views,
  -- Device context
  device_type,
  is_mobile
FROM `project.raw.user_events`
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

## Multi-Armed Bandit & Exploration

### Thompson Sampling Implementation
```python
# src/recommendation/bandit.py
from typing import Dict, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class BanditArm:
    """Represents a recommendation strategy."""
    name: str
    successes: int = 0
    failures: int = 0

    @property
    def total_pulls(self) -> int:
        return self.successes + self.failures

    @property
    def success_rate(self) -> float:
        if self.total_pulls == 0:
            return 0.0
        return self.successes / self.total_pulls

class ThompsonSamplingBandit:
    """Thompson Sampling for recommendation strategy selection."""

    def __init__(self, strategies: List[str]):
        self.arms = {name: BanditArm(name) for name in strategies}

    def select_strategy(self) -> str:
        """Select strategy using Thompson Sampling."""
        samples = {}
        for name, arm in self.arms.items():
            # Beta distribution sampling
            alpha = arm.successes + 1
            beta = arm.failures + 1
            samples[name] = np.random.beta(alpha, beta)

        # Select arm with highest sample
        return max(samples.items(), key=lambda x: x[1])[0]

    def update(self, strategy: str, success: bool):
        """Update arm statistics."""
        if success:
            self.arms[strategy].successes += 1
        else:
            self.arms[strategy].failures += 1

    def get_statistics(self) -> Dict[str, Dict]:
        """Get current bandit statistics."""
        return {
            name: {
                'pulls': arm.total_pulls,
                'success_rate': arm.success_rate,
                'confidence': self._calculate_confidence(arm)
            }
            for name, arm in self.arms.items()
        }

    def _calculate_confidence(self, arm: BanditArm) -> Tuple[float, float]:
        """Calculate 95% confidence interval using Wilson score."""
        if arm.total_pulls == 0:
            return (0.0, 1.0)

        p = arm.success_rate
        n = arm.total_pulls
        z = 1.96  # 95% confidence

        denominator = 1 + z**2/n
        centre_adjusted = p + z**2 / (2*n)
        adjusted_std = np.sqrt((p*(1 - p) + z**2/(4*n)) / n)

        lower = (centre_adjusted - z*adjusted_std) / denominator
        upper = (centre_adjusted + z*adjusted_std) / denominator

        return (max(0, lower), min(1, upper))
```

## Recommendation Quality Monitoring

### Daily Metrics Dashboard
```sql
CREATE OR REPLACE TABLE `project.monitoring.recommendation_metrics_daily` AS
WITH daily_recommendations AS (
  SELECT
    DATE(recommendation_timestamp) as metric_date,
    user_id,
    rec.product_id,
    rec.predicted_rating,
    ROW_NUMBER() OVER (PARTITION BY user_id, DATE(recommendation_timestamp)
                       ORDER BY predicted_rating DESC) as rec_rank
  FROM `project.recommendation.served_recommendations`,
       UNNEST(recommendations) rec
),
user_interactions AS (
  SELECT
    user_id,
    product_id,
    DATE(event_timestamp) as interaction_date,
    event_type,
    purchase_amount
  FROM `project.raw.user_events`
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
)
SELECT
  dr.metric_date,
  -- Click-through rate
  SAFE_DIVIDE(
    COUNTIF(ui.event_type = 'view'),
    COUNT(DISTINCT dr.user_id)
  ) as ctr,
  -- Conversion rate
  SAFE_DIVIDE(
    COUNTIF(ui.event_type = 'purchase'),
    COUNT(DISTINCT dr.user_id)
  ) as conversion_rate,
  -- Average rank of clicked items
  AVG(IF(ui.event_type IS NOT NULL, dr.rec_rank, NULL)) as avg_clicked_rank,
  -- Catalog coverage
  COUNT(DISTINCT dr.product_id) / (
    SELECT COUNT(DISTINCT product_id)
    FROM `project.catalog.products`
    WHERE is_active = TRUE
  ) as catalog_coverage,
  -- Category diversity
  AVG((
    SELECT COUNT(DISTINCT p.category)
    FROM UNNEST(
      ARRAY_AGG(dr.product_id ORDER BY dr.rec_rank LIMIT 10)
    ) as product_id
    JOIN `project.catalog.products` p USING (product_id)
  )) as avg_category_diversity,
  -- Revenue impact
  SUM(IF(ui.event_type = 'purchase', ui.purchase_amount, 0)) as attributed_revenue
FROM daily_recommendations dr
LEFT JOIN user_interactions ui
  ON dr.user_id = ui.user_id
  AND dr.product_id = ui.product_id
  AND ui.interaction_date = dr.metric_date
WHERE dr.rec_rank <= 10
GROUP BY dr.metric_date
ORDER BY dr.metric_date DESC;
```

## Best Practices

- Use implicit feedback (clicks, purchases) over explicit ratings
- Filter out noise (minimum interaction threshold)
- Retrain models regularly (weekly/daily)
- Monitor for popularity bias
- Include diversity in recommendations
- A/B test before full rollout
- Track business metrics (CTR, conversion, revenue)
- Balance relevance and diversity (50-70% relevance weight)

## Advanced Topics

For detailed guidance on specialized patterns:

- **Cold Start Problems**: See [reference/cold-start.md](reference/cold-start.md) for handling new users and products
- **Fairness & Diversity**: See [reference/fairness.md](reference/fairness.md) for MMR algorithm and diversity metrics
- **Exploration Strategies**: See [reference/bandit-algorithms.md](reference/bandit-algorithms.md) for Thompson Sampling, epsilon-greedy, and UCB
