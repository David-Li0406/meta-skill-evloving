---
name: databricks-ml-pipeline
description: End-to-end machine learning pipelines on Databricks including data exploration, feature engineering, model training with hyperparameter optimization, MLflow experiment tracking, model registration to Unity Catalog, and deployment as DABs. Use when building ML workflows, training models, or deploying ML pipelines.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
model: claude-sonnet-4-5-20250929
user-invocable: true
---

# Databricks ML Pipeline Builder

Build complete machine learning pipelines from data exploration through model deployment. Orchestrates testing, Unity Catalog setup, and bundle deployment for production ML workflows.

## When to Use This Skill

- Building end-to-end ML pipelines
- Training models with hyperparameter optimization
- Setting up MLflow experiment tracking
- Registering models to Unity Catalog
- Deploying ML training pipelines
- Scheduling periodic model retraining
- Feature engineering workflows

## Complete ML Workflow

This skill orchestrates other skills to deliver complete ML pipelines:

1. **Setup** (`databricks-unity-catalog` skill)
   - Create catalog schema for ML assets
   - Set up feature store schema
   - Prepare model registry

2. **Exploration** (`databricks-testing` skill)
   - Load and profile data on cluster
   - Test feature engineering logic
   - Validate data quality

3. **Training** (`databricks-testing` skill)
   - Test training code interactively
   - Hyperparameter tuning
   - MLflow experiment tracking
   - Model validation

4. **Registration**
   - Register best model to Unity Catalog
   - Add model metadata and tags
   - Set model aliases (Champion/Challenger)

5. **Deployment** (`databricks-bundle-deploy` skill)
   - Package as Databricks Asset Bundle
   - Deploy to dev/staging/prod
   - Schedule periodic retraining

## Phase 1: Setup & Data Exploration

### Step 1: Create ML Schemas

Use `databricks-unity-catalog` skill to set up catalog structure:

```python
# Create schema for ML models
create_schema(
    catalog_name="ml_dev",
    schema_name="churn_prediction",
    comment="Churn prediction model v2.0. Features, training data, and model registry."
)

# Verify
get_schema(full_schema_name="ml_dev.churn_prediction")
```

### Step 2: Load and Profile Data

Use `databricks-testing` skill to explore data on cluster:

```python
# Test data loading
databricks_command(
    cluster_id="0123-456789-abc123",
    language="python",
    code="""
# Load customer data
df = spark.table("ml_dev.bronze.customer_transactions")

print(f"Total records: {df.count()}")
print(f"Date range: {df.select('transaction_date').agg({'transaction_date': 'min'}).collect()[0][0]} to {df.select('transaction_date').agg({'transaction_date': 'max'}).collect()[0][0]}")

# Profile data
df.describe().show()
df.groupBy('customer_status').count().show()

# Check for nulls
from pyspark.sql import functions as F
null_counts = df.select([F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns])
null_counts.show()
"""
)
```

## Phase 2: Feature Engineering

### Step 3: Test Feature Transformations

Use `databricks-testing` skill with stateful context:

```python
# Create context for iterative development
context_id = create_context(
    cluster_id="0123-456789-abc123",
    language="python"
)

# Load data (persists in context)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Load customer transactions
df = spark.table("ml_dev.bronze.customer_transactions")
print(f"Loaded {df.count()} transactions")
"""
)

# Create features (uses df from previous step)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
# Time-based features
w = Window.partitionBy("customer_id").orderBy("transaction_date")

features_df = df.groupBy("customer_id").agg(
    F.count("*").alias("transaction_count"),
    F.sum("amount").alias("total_spend"),
    F.avg("amount").alias("avg_transaction"),
    F.datediff(F.current_date(), F.max("transaction_date")).alias("days_since_last"),
    F.count(F.when(F.col("transaction_date") >= F.date_sub(F.current_date(), 30), 1)).alias("recent_transactions")
)

# Add churn label (no transactions in last 90 days)
features_df = features_df.withColumn(
    "churned",
    F.when(F.col("days_since_last") > 90, 1).otherwise(0)
)

print("Features created:")
features_df.show(10)

# Check class balance
features_df.groupBy("churned").count().show()
"""
)

# Save features (uses features_df from previous step)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
# Save to feature table
features_df.write \\
    .format("delta") \\
    .mode("overwrite") \\
    .saveAsTable("ml_dev.churn_prediction.customer_features")

print("Features saved to ml_dev.churn_prediction.customer_features")
"""
)

# Cleanup context
destroy_context(cluster_id="0123-456789-abc123", context_id=context_id)
```

## Phase 3: Model Training

### Step 4: Test Training Code

Use `databricks-testing` skill to validate training logic:

```python
databricks_command(
    cluster_id="0123-456789-abc123",
    language="python",
    code="""
# MAGIC %pip install mlflow scikit-learn

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load features
features_df = spark.table("ml_dev.churn_prediction.customer_features").toPandas()

# Prepare data
feature_cols = ["transaction_count", "total_spend", "avg_transaction", "days_since_last", "recent_transactions"]
X = features_df[feature_cols]
y = features_df["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train baseline model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Baseline Model Performance:")
print(f"  Accuracy: {accuracy:.4f}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall: {recall:.4f}")
print(f"  F1 Score: {f1:.4f}")
"""
)
```

## Phase 4: MLflow Experiment Tracking

### Complete Training Notebook with MLflow

**Template for ML training notebook:**

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Churn Prediction Model Training
# MAGIC
# MAGIC Trains Random Forest model with hyperparameter optimization and MLflow tracking

# COMMAND ----------
# MAGIC %pip install mlflow scikit-learn

# COMMAND ----------
# Widget parameterization
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "ml_dev"

try:
    schema = dbutils.widgets.get("schema")
except:
    schema = "churn_prediction"

try:
    experiment_name = dbutils.widgets.get("experiment_name")
except:
    experiment_name = f"/Users/{spark.sql('SELECT current_user()').collect()[0][0]}/experiments/churn_model"

print(f"Training with parameters:")
print(f"  Catalog: {catalog}")
print(f"  Schema: {schema}")
print(f"  Experiment: {experiment_name}")

# COMMAND ----------
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Set MLflow experiment
mlflow.set_experiment(experiment_name)

# COMMAND ----------
# Load features
features_df = spark.table(f"{catalog}.{schema}.customer_features").toPandas()

# Prepare data
feature_cols = ["transaction_count", "total_spend", "avg_transaction", "days_since_last", "recent_transactions"]
X = features_df[feature_cols]
y = features_df["churned"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")
print(f"Churn rate: {y.mean():.2%}")

# COMMAND ----------
# Hyperparameter tuning with MLflow
params_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [5, 10, 20, None],
    "min_samples_split": [2, 5, 10]
}

best_score = 0
best_run_id = None
best_params = None

for n_est in params_grid["n_estimators"]:
    for depth in params_grid["max_depth"]:
        for split in params_grid["min_samples_split"]:
            with mlflow.start_run(run_name=f"RF_n{n_est}_d{depth}_s{split}"):
                # Log parameters
                mlflow.log_param("n_estimators", n_est)
                mlflow.log_param("max_depth", depth if depth else "None")
                mlflow.log_param("min_samples_split", split)

                # Train model
                model = RandomForestClassifier(
                    n_estimators=n_est,
                    max_depth=depth,
                    min_samples_split=split,
                    random_state=42
                )

                # Cross-validation
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()

                # Log CV metrics
                mlflow.log_metric("cv_f1_mean", cv_mean)
                mlflow.log_metric("cv_f1_std", cv_std)

                # Train on full training set
                model.fit(X_train, y_train)

                # Test set evaluation
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                auc = roc_auc_score(y_test, y_pred_proba)

                # Log test metrics
                mlflow.log_metric("test_accuracy", accuracy)
                mlflow.log_metric("test_precision", precision)
                mlflow.log_metric("test_recall", recall)
                mlflow.log_metric("test_f1", f1)
                mlflow.log_metric("test_auc", auc)

                # Log model
                mlflow.sklearn.log_model(model, "model")

                # Track best model by F1 score
                if f1 > best_score:
                    best_score = f1
                    best_run_id = mlflow.active_run().info.run_id
                    best_params = {
                        "n_estimators": n_est,
                        "max_depth": depth,
                        "min_samples_split": split
                    }

print(f"\\nBest Model:")
print(f"  Run ID: {best_run_id}")
print(f"  F1 Score: {best_score:.4f}")
print(f"  Parameters: {best_params}")

# COMMAND ----------
# Register best model to Unity Catalog
model_name = f"{catalog}.{schema}.churn_prediction_model"

model_uri = f"runs:/{best_run_id}/model"
registered_model = mlflow.register_model(model_uri, model_name)

print(f"Model registered as: {model_name}")
print(f"Version: {registered_model.version}")

# COMMAND ----------
# Set model alias
from mlflow.tracking import MlflowClient

client = MlflowClient()
client.set_registered_model_alias(
    name=model_name,
    alias="Champion",
    version=registered_model.version
)

print(f"Model alias 'Champion' set to version {registered_model.version}")

# COMMAND ----------
# Add model description
client.update_model_version(
    name=model_name,
    version=registered_model.version,
    description=f"Random Forest churn prediction model. F1 score: {best_score:.4f}. Trained on {len(X_train)} samples. Parameters: {best_params}"
)

print("Model registration complete!")
```

## Phase 5: Deployment

### Step 5: Package as Databricks Asset Bundle

Use `databricks-bundle-deploy` skill to create production-ready bundle:

**Project structure:**
```
churn_prediction_pipeline/
├── databricks.yml
├── resources/
│   └── training_job.yml
└── src/
    └── churn_prediction/
        └── notebooks/
            ├── 01_data_prep.py
            ├── 02_feature_engineering.py
            └── 03_model_training.py
```

**databricks.yml:**
```yaml
bundle:
  name: churn_prediction_pipeline

variables:
  catalog:
    description: "Unity Catalog for ML assets"
    default: "ml_dev"

  schema:
    description: "Schema for churn prediction"
    default: "churn_prediction"

  experiment_name:
    description: "MLflow experiment path"

targets:
  dev:
    mode: development
    variables:
      catalog: "ml_dev"
      experiment_name: "/Users/${workspace.current_user.userName}/experiments/churn_dev"

  prod:
    mode: production
    variables:
      catalog: "ml_prod"
      experiment_name: "/Shared/experiments/churn_prod"

resources:
  jobs:
    churn_training_job:
      name: churn_training_${bundle.target}

      tasks:
        - task_key: data_preparation
          notebook_task:
            notebook_path: ../src/churn_prediction/notebooks/01_data_prep.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: feature_engineering
          depends_on:
            - task_key: data_preparation
          notebook_task:
            notebook_path: ../src/churn_prediction/notebooks/02_feature_engineering.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: model_training
          depends_on:
            - task_key: feature_engineering
          notebook_task:
            notebook_path: ../src/churn_prediction/notebooks/03_model_training.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}
              experiment_name: ${var.experiment_name}

      schedule:
        quartz_cron_expression: "0 0 2 * * ?"  # Daily at 2am UTC
        timezone_id: "UTC"

      email_notifications:
        on_failure:
          - ${workspace.current_user.userName}
```

**Validate and deploy (AUTOMATIC):**
```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
```

**Ask before running:**
```
"Do you want to run the training job now?"

# If yes:
databricks bundle run churn_training_job -t dev
```

## ML Best Practices

### 1. Always Use MLflow

- Set experiment at notebook start
- Log all hyperparameters
- Log all metrics (training and test)
- Log the model artifact
- Use run names for clarity

### 2. Register to Unity Catalog

**Use Unity Catalog model registry (not classic workspace):**

```python
# Good - Unity Catalog
model_name = f"{catalog}.{schema}.my_model"
mlflow.register_model(model_uri, model_name)

# Bad - Classic workspace
model_name = "my_model"  # Don't use!
```

### 3. Use Model Aliases

Set aliases for model lifecycle management:

```python
# Champion - current production model
client.set_registered_model_alias(name=model_name, alias="Champion", version=5)

# Challenger - candidate for production
client.set_registered_model_alias(name=model_name, alias="Challenger", version=6)

# Staging - in testing
client.set_registered_model_alias(name=model_name, alias="Staging", version=7)
```

### 4. Cross-Validation

Always use cross-validation for hyperparameter tuning:

```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
mlflow.log_metric("cv_f1_mean", cv_scores.mean())
mlflow.log_metric("cv_f1_std", cv_scores.std())
```

### 5. Add Model Metadata

Document models with descriptions and tags:

```python
client.update_model_version(
    name=model_name,
    version=version,
    description=f"RF model. F1: {f1:.4f}. Trained on {train_size} samples."
)

client.set_model_version_tag(
    name=model_name,
    version=version,
    key="validation_status",
    value="approved"
)
```

## Integration with Other Skills

### Uses
- `databricks-unity-catalog` - Creates schemas, verifies tables
- `databricks-testing` - Tests data loading, feature engineering, training
- `databricks-bundle-deploy` - Packages and deploys ML pipeline

### Workflow Summary

1. UC skill → Create ML schemas
2. Testing skill → Test feature engineering
3. Testing skill → Test training code
4. Testing skill → MLflow tracking
5. Bundle skill → Package as DAB
6. Bundle skill → Deploy to environments

## Common ML Patterns

### Classification with Imbalanced Data

```python
from sklearn.utils.class_weight import compute_class_weight

# Compute class weights
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

# Train with class weights
model = RandomForestClassifier(class_weight=class_weight_dict)
```

### Feature Importance Analysis

```python
# Log feature importance
import pandas as pd

feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)

# Log as artifact
feature_importance.to_csv("/tmp/feature_importance.csv", index=False)
mlflow.log_artifact("/tmp/feature_importance.csv")
```

### Batch Prediction Pipeline

```python
# Load model by alias
model_uri = f"models:/{catalog}.{schema}.churn_model@Champion"
model = mlflow.sklearn.load_model(model_uri)

# Score new data
new_customers = spark.table(f"{catalog}.{schema}.new_customer_features").toPandas()
predictions = model.predict_proba(new_customers[feature_cols])[:, 1]

# Save predictions
new_customers['churn_score'] = predictions
spark.createDataFrame(new_customers).write.saveAsTable(f"{catalog}.{schema}.churn_scores")
```

## Troubleshooting

### Issue: Model Not Registered to Unity Catalog

**Symptom:** Model appears in classic workspace registry

**Cause:** Used model name without catalog.schema prefix

**Fix:**
```python
# Include catalog and schema
model_name = f"{catalog}.{schema}.my_model"
mlflow.register_model(model_uri, model_name)
```

### Issue: MLflow Experiment Not Found

**Symptom:** "Experiment '/Users/...' does not exist"

**Cause:** Experiment path doesn't exist

**Fix:**
```python
# Create experiment if doesn't exist
try:
    mlflow.set_experiment(experiment_name)
except:
    mlflow.create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)
```

## Summary

This skill builds complete ML pipelines:
- **Setup**: Unity Catalog schemas for ML assets
- **Exploration**: Interactive data profiling on cluster
- **Features**: Test feature engineering logic
- **Training**: Hyperparameter tuning with MLflow
- **Registration**: Unity Catalog model registry
- **Deployment**: DAB packaging and scheduling

Use this skill to go from raw data to production ML pipeline in one workflow.
