# Causal Scientist - Validations

## DoWhy Proceeding When Unidentifiable

### **Id**
dowhy-proceed-unidentifiable
### **Severity**
error
### **Type**
regex
### **Pattern**
  - proceed_when_unidentifiable.*=.*True
  - proceed_when_unidentifiable=True
### **Message**
DoWhy proceeding when effect is unidentifiable. Estimate is meaningless.
### **Fix Action**
Set proceed_when_unidentifiable=False and handle unidentifiable cases
### **Applies To**
  - **/causal/**/*.py
  - **/*causal*.py

## Causal Estimate Without Refutation

### **Id**
causal-no-refutation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - estimate_effect\\([^)]*\\)(?!.*refute)
  - model\\.estimate(?!.*refut)
### **Message**
Causal estimate without refutation tests. Effect may not be robust.
### **Fix Action**
Add refutation tests: random_common_cause, placebo, data_subset
### **Applies To**
  - **/causal/**/*.py

## Using Only Single Causal Estimator

### **Id**
causal-single-estimator
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - method_name.*=.*["']backdoor\.
  - estimate_effect.*method.*=(?!.*multiple|.*robust)
### **Message**
Using single causal estimator. Use multiple for robustness.
### **Fix Action**
Try multiple estimators and check agreement
### **Applies To**
  - **/causal/**/*.py

## Causal Graph Without Cycle Check

### **Id**
causal-graph-no-validation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - DiGraph\\(\\)(?!.*is_directed_acyclic|.*simple_cycles)
  - add_edge(?!.*validate|.*acyclic)
### **Message**
Building causal graph without validating DAG properties.
### **Fix Action**
Validate graph is acyclic with nx.is_directed_acyclic_graph()
### **Applies To**
  - **/causal/**/*.py
  - **/graph/**/*.py

## Causal Discovery Without Sample Size Check

### **Id**
causal-discovery-no-sample-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pc\\((?!.*len.*>|.*sample)
  - fci\\((?!.*size|.*sample)
### **Message**
Causal discovery without checking sample size. May lack power.
### **Fix Action**
Verify sufficient samples per variable (~50-100)
### **Applies To**
  - **/causal/**/*.py

## Counterfactual Without Uncertainty

### **Id**
counterfactual-no-uncertainty
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - counterfactual.*\\.mean\\(\\)(?!.*std|.*percentile)
  - counterfactual(?!.*confidence|.*interval|.*std)
### **Message**
Counterfactual without uncertainty quantification.
### **Fix Action**
Report confidence intervals for counterfactual estimates
### **Applies To**
  - **/causal/**/*.py

## Causal Model Without Confounders

### **Id**
causal-no-confounders
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CausalModel\\([^)]*treatment[^)]*outcome[^)]*\\)(?!.*common_causes)
  - common_causes.*=.*\\[\\]
  - common_causes.*=.*None
### **Message**
Causal model without confounders specified. Effect likely biased.
### **Fix Action**
Identify and specify common causes (confounders)
### **Applies To**
  - **/causal/**/*.py

## Causal Claim From Correlation

### **Id**
causal-correlation-claim
### **Severity**
error
### **Type**
regex
### **Pattern**
  - corr.*caus|caus.*corr
  - \\.corr\\(\\).*effect
  - correlation.*implies.*causation
### **Message**
Correlation used to claim causation. Need proper causal inference.
### **Fix Action**
Use DoWhy or similar for proper causal effect estimation
### **Applies To**
  - **/*.py

## Causal Effect Without Confidence Interval

### **Id**
causal-effect-no-ci
### **Severity**
info
### **Type**
regex
### **Pattern**
  - estimate\\.value(?!.*confidence|.*interval)
  - effect.*=.*estimate(?!.*ci|.*interval)
### **Message**
Causal effect reported without confidence interval.
### **Fix Action**
Use estimate.get_confidence_intervals()
### **Applies To**
  - **/causal/**/*.py

## Causal Graph Without Temporal Ordering

### **Id**
causal-temporal-order-ignored
### **Severity**
info
### **Type**
regex
### **Pattern**
  - add_edge(?!.*temporal|.*time|.*order)
  - CausalModel(?!.*temporal)
### **Message**
Causal graph built without temporal ordering constraints.
### **Fix Action**
Apply temporal ordering: causes must precede effects
### **Applies To**
  - **/causal/**/*.py

## Intervention Outside Observed Range

### **Id**
intervention-extrapolation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - intervention.*=(?!.*min|.*max|.*range)
  - do\\((?!.*bounds|.*range)
### **Message**
Intervention may be outside observed data range.
### **Fix Action**
Check if intervention value is within training data range
### **Applies To**
  - **/causal/**/*.py

## Using ATE for Individual Predictions

### **Id**
ate-not-individual
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - average.*treatment.*effect.*individual
  - ate.*predict.*user
### **Message**
Average treatment effect used for individual predictions.
### **Fix Action**
Consider CATE (Conditional Average Treatment Effect) for heterogeneous effects
### **Applies To**
  - **/causal/**/*.py