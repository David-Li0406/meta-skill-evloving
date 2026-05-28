# A B Testing - Validations

## Missing Hypothesis Statement

### **Id**
abt-no-hypothesis
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(A/B test|experiment|variant)\b(?!.{0,200}\b(hypothesis|we believe|expect that|predict)\b)
### **Message**
A/B test proposed without clear hypothesis. Every experiment needs a testable hypothesis.
### **Fix Action**
Add hypothesis statement: 'We believe that [change] will cause [effect] because [reasoning]'
### **Applies To**
  - *.md
  - *.txt

## Missing Sample Size Calculation

### **Id**
abt-no-sample-size
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(A/B test|experiment|variant)\b(?!.{0,300}\b(sample size|statistical power|MDE|minimum detectable effect|power analysis)\b)
### **Message**
No sample size calculation mentioned. Running experiments without power analysis wastes time and resources.
### **Fix Action**
Calculate required sample size using power analysis (typically 80% power, 95% confidence, expected effect size)
### **Applies To**
  - *.md
  - *.txt

## Peeking at Results

### **Id**
abt-peeking
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(check results|peek at|look at data)\b.{0,50}\b(before|early|mid-experiment)
  - \b(stop|end|conclude)\b.{0,50}\b(experiment|test)\b.{0,50}\b(early|ahead of schedule)\b(?!.{0,100}\bsequential testing\b)
### **Message**
Peeking at results before reaching sample size inflates false positive rate. Use sequential testing methods if early stopping is needed.
### **Fix Action**
Wait until predetermined sample size is reached, or use proper sequential testing (e.g., always-valid inference)
### **Applies To**
  - *.md
  - *.py
  - *.js
  - *.tsx

## Missing Control Group

### **Id**
abt-no-control
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(variant|version) [AB]\b(?!.{0,200}\b(control|baseline|current version)\b)
  - \b(testing|experiment)\b.{0,100}\b(new feature|change)\b(?!.{0,200}\b(vs|versus|against|control)\b)
### **Message**
No control group mentioned. Every experiment needs a control to compare against.
### **Fix Action**
Ensure one variant is the control (current experience) with no changes
### **Applies To**
  - *.md
  - *.txt

## Multiple Changes in Single Test

### **Id**
abt-multiple-changes
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(and|plus|also)\b.{0,50}\b(change|modify|update|test)\b.{0,50}\b(and|plus|also)\b
  - \b(testing|experiment).{0,100}\b(multiple|several|various)\b.{0,50}\b(changes|features|variants)\b
### **Message**
Testing multiple changes simultaneously makes it impossible to identify which change caused the effect.
### **Fix Action**
Test one change at a time, or use multivariate testing with sufficient sample size
### **Applies To**
  - *.md
  - *.txt

## Missing Primary Success Metric

### **Id**
abt-no-success-metric
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(A/B test|experiment)\b(?!.{0,300}\b(primary metric|success metric|KPI|measure|conversion|revenue|retention)\b)
### **Message**
No primary success metric defined. Must have one clear metric to optimize for.
### **Fix Action**
Define single primary metric that aligns with business goal (e.g., conversion rate, revenue per user)
### **Applies To**
  - *.md
  - *.txt

## Missing Test Duration

### **Id**
abt-no-duration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(run|start|launch)\b.{0,50}\b(experiment|A/B test|test)\b(?!.{0,200}\b(duration|days|weeks|until|sample size reached)\b)
### **Message**
No test duration or stopping criteria specified.
### **Fix Action**
Specify duration based on sample size calculation and traffic, account for weekly seasonality
### **Applies To**
  - *.md
  - *.txt

## Missing Randomization Strategy

### **Id**
abt-no-randomization
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(assign|split|divide)\b.{0,50}\b(users|traffic|visitors)\b(?!.{0,200}\b(random|hash|shuffle)\b)
### **Message**
No randomization method specified. Non-random assignment introduces selection bias.
### **Fix Action**
Use proper randomization (user hash-based assignment) to ensure unbiased group allocation
### **Applies To**
  - *.md
  - *.py
  - *.js
  - *.tsx

## No Novelty Effect Consideration

### **Id**
abt-novelty-effect
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(significant|big|major)\b.{0,50}\b(UI change|redesign|new design)\b(?!.{0,300}\b(novelty effect|initial reaction|long-term)\b)
### **Message**
Major UI changes may show novelty or change aversion effects that fade over time.
### **Fix Action**
Run test for minimum 2 weeks to account for novelty effects, consider cohort analysis
### **Applies To**
  - *.md
  - *.txt

## Missing A/A Test Validation

### **Id**
abt-no-aa-test
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \b(new|first|initial)\b.{0,50}\b(experiment|A/B test|testing system)\b(?!.{0,300}\b(A/A test|validation test|sanity check)\b)
### **Message**
New testing systems should run A/A test to validate proper randomization and metric calculation.
### **Fix Action**
Run A/A test (identical variants) to verify false positive rate matches expected alpha level
### **Applies To**
  - *.md
  - *.txt

## Relying Only on P-Value

### **Id**
abt-p-value-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \bp\s*<\s*0\.05\b(?!.{0,200}\b(effect size|confidence interval|practical significance)\b)
  - \bstatistically significant\b(?!.{0,200}\b(but|however|effect size|magnitude)\b)
### **Message**
Statistical significance (p-value) doesn't indicate practical significance or effect size.
### **Fix Action**
Report effect size and confidence intervals, assess practical/business significance
### **Applies To**
  - *.md
  - *.py
  - *.js

## Missing Segmentation Analysis Plan

### **Id**
abt-no-segment-plan
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \b(experiment|A/B test)\b.{0,300}\b(results|analysis)\b(?!.{0,300}\b(segment|cohort|subgroup|breakdown)\b)
### **Message**
No plan for segment analysis. Pre-specify important segments to analyze to avoid data dredging.
### **Fix Action**
Pre-specify 2-3 key segments to analyze (e.g., new vs returning, mobile vs desktop)
### **Applies To**
  - *.md
  - *.txt