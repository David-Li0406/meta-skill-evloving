# Iteration Reward Patterns

Concrete examples of iteration rewards with green and red flags for common experiment types.

## Table of Contents
1. [MI Estimation Experiment](#mi-estimation-experiment)
2. [CoT Faithfulness Experiment](#cot-faithfulness-experiment)
3. [Model Comparison Experiment](#model-comparison-experiment)
4. [Data Analysis Experiment](#data-analysis-experiment)

---

## MI Estimation Experiment

```markdown
## Iteration Rewards for: Logistic Regression MI Estimator

**After 1 min**: Data loads, features extract without error
**After 5 min**: Loss decreases on first 100 samples
**After 15 min**: Accuracy on validation set > random chance
**After 30 min**: MI estimate in reasonable range (0.1-3.0 bits)

**Progress signals to log**:
- Training loss per batch
- Validation accuracy per epoch

**Green flags (REQUIRED before done)**:
- [ ] MI estimate computed for all model/rep combinations
- [ ] Results match expected schema and saved to CSV
- [ ] Random baseline shows ~0 MI (sanity check)
- [ ] Cross-validation completed with confidence intervals

**Red flags (abandon immediately)**:
- Loss increases or stays flat after 1000 steps
- All predictions collapse to single class
```

---

## CoT Faithfulness Experiment

```markdown
## Iteration Rewards for: CoT Perturbation Study

**After 1 min**: Model produces any CoT output
**After 5 min**: Can parse and tokenize 5 CoT samples
**After 15 min**: Perturbation function changes token counts
**After 30 min**: Perturbation → accuracy delta on 50 samples

**Progress signals to log**:
- Parse success rate
- Token count before/after perturbation

**Green flags (REQUIRED before done)**:
- [ ] N=100+ samples processed successfully
- [ ] Perturbation effect size computed with p-value
- [ ] Control condition (no perturbation) matches original accuracy
- [ ] Results written to standardized output format

**Red flags (abandon immediately)**:
- >50% parse failures
- Perturbation doesn't change output at all
```

---

## Model Comparison Experiment

```markdown
## Iteration Rewards for: Code vs NL Representation Comparison

**After 1 min**: Both code and NL outputs generated for 1 sample
**After 5 min**: Parse success on 10 samples for both representations
**After 15 min**: Accuracy computed for both on 50 samples
**After 30 min**: Preliminary delta between code/NL visible

**Progress signals to log**:
- Per-model accuracy
- Parse success rate by representation type

**Green flags (REQUIRED before done)**:
- [ ] All target models tested (>3 models)
- [ ] Statistical test run (paired t-test or bootstrap)
- [ ] Effect size (Cohen's d) computed
- [ ] Visualization generated (boxplot or bar chart)
- [ ] Results saved with metadata (model, seed, timestamp)

**Red flags (abandon immediately)**:
- API rate limits blocking progress
- >30% of model outputs unparseable
- Baseline accuracy < 10% (task too hard)
```

---

## Data Analysis Experiment

```markdown
## Iteration Rewards for: Dataset Characterization

**After 1 min**: Data file loads without error
**After 5 min**: Basic statistics computed (count, mean, std)
**After 15 min**: Distribution plots generated
**After 30 min**: Key patterns identified and documented

**Progress signals to log**:
- Row/column counts
- Missing value percentages
- Distribution shapes

**Green flags (REQUIRED before done)**:
- [ ] All columns documented (type, range, meaning)
- [ ] Missing data strategy defined
- [ ] Outliers identified and decision made (keep/remove/cap)
- [ ] Summary statistics table saved
- [ ] At least 3 visualizations created

**Red flags (abandon immediately)**:
- >50% missing data in key columns
- Data format incompatible with analysis tools
- File corruption or encoding issues
```

---

## Creating Your Own Patterns

When designing iteration rewards for a new experiment:

1. **Start with smoke test**: What's the absolute minimum to verify setup works?
2. **Define quick metric**: What can you measure in <5 min on a tiny sample?
3. **Set pivot point**: At 30 min, what result means "this won't work"?
4. **List green flags**: What must be true before you can call this done?
5. **Identify red flags**: What signals should trigger immediate abandonment?

### Green Flag Categories

| Category | Example |
|----------|---------|
| **Completeness** | "All models tested" |
| **Statistical rigor** | "p-value < 0.05" |
| **Reproducibility** | "Can re-run from scratch" |
| **Output format** | "Results saved to expected location" |
| **Sanity check** | "Baseline matches expected value" |

### Red Flag Categories

| Category | Example |
|----------|---------|
| **Infrastructure** | "API unreachable" |
| **Data quality** | ">50% parse failures" |
| **Algorithm failure** | "Loss not decreasing" |
| **Fundamental issue** | "Approach can't work in principle" |
