# Synthetic Data - Validations

## Synthetic Data Without Quality Check

### **Id**
no-quality-check
### **Severity**
error
### **Description**
Always validate synthetic data quality before use
### **Pattern**
  generateSynthetic|syntheticData(?!.*validate|quality|check|verify)
  
### **Message**
Synthetic data must be validated for quality before training.
### **Autofix**


## No Distribution Comparison

### **Id**
no-distribution-check
### **Severity**
warning
### **Description**
Compare synthetic distribution to real data
### **Pattern**
  synthetic.*push(?!.*distribution|compare|audit)
  
### **Message**
Compare synthetic data distribution to real data.
### **Autofix**


## No Uniqueness Verification

### **Id**
missing-uniqueness-check
### **Severity**
warning
### **Description**
Check for duplicate or near-duplicate examples
### **Pattern**
  synthetic.*length|syntheticData\.length(?!.*unique|duplicate|Set)
  
### **Message**
Check synthetic data for duplicates before use.
### **Autofix**


## No Privacy Validation

### **Id**
no-privacy-check
### **Severity**
error
### **Description**
Synthetic data needs privacy validation
### **Pattern**
  generateSynthetic.*privacy(?!.*check|validate|dp|epsilon)
  
### **Message**
Validate synthetic data doesn't leak real data information.
### **Autofix**


## No PII Filtering

### **Id**
no-pii-filter
### **Severity**
error
### **Description**
Filter PII from synthetic outputs
### **Pattern**
  llm.*generate.*data(?!.*pii|filter|sanitize|redact)
  
### **Message**
LLM-generated data may contain memorized PII. Filter outputs.
### **Autofix**


## No Memorization Check

### **Id**
no-memorization-check
### **Severity**
warning
### **Description**
Check if synthetic data matches real data exactly
### **Pattern**
  synthetic.*real(?!.*overlap|match|memoriz)
  
### **Message**
Check for exact matches between synthetic and real data.
### **Autofix**


## No Schema Validation

### **Id**
no-schema-validation
### **Severity**
error
### **Description**
Validate synthetic data against schema
### **Pattern**
  generateSynthetic|syntheticData(?!.*schema|parse|validate|zod)
  
### **Message**
Validate synthetic data against expected schema.
### **Autofix**


## No Domain Constraint Check

### **Id**
no-constraint-check
### **Severity**
warning
### **Description**
Validate domain-specific constraints
### **Pattern**
  synthetic.*domain(?!.*constraint|rule|validate)
  
### **Message**
Validate domain-specific constraints (e.g., date ranges, zip codes).
### **Autofix**


## No Cost Estimation

### **Id**
no-cost-estimate
### **Severity**
info
### **Description**
Estimate costs before large generation runs
### **Pattern**
  generate.*count.*\d{3,}(?!.*cost|estimate|budget)
  
### **Message**
Estimate costs before generating large datasets.
### **Autofix**


## Using Expensive Model for Bulk Generation

### **Id**
using-expensive-model
### **Severity**
info
### **Description**
Use cheaper models for high-volume generation
### **Pattern**
  generate.*count.*\d{4,}.*gpt-4o[^-]|claude-sonnet
  
### **Message**
Consider gpt-4o-mini or haiku for bulk generation.
### **Autofix**


## Low Temperature for Synthetic Data

### **Id**
low-temperature-generation
### **Severity**
warning
### **Description**
Low temperature reduces diversity
### **Pattern**
  temperature.*0\.[0-3].*synthetic|synthetic.*temperature.*0\.[0-3]
  
### **Message**
Low temperature reduces diversity. Use 0.7-1.0 for synthetic data.
### **Autofix**


## No Diversity Metrics

### **Id**
no-diversity-check
### **Severity**
warning
### **Description**
Monitor diversity during generation
### **Pattern**
  synthetic.*batch(?!.*diversity|entropy|coverage)
  
### **Message**
Monitor diversity metrics during synthetic generation.
### **Autofix**


## Training Only on Synthetic Data

### **Id**
synthetic-only-training
### **Severity**
error
### **Description**
Include real data in validation set
### **Pattern**
  train.*synthetic(?!.*real.*valid|holdout)
  
### **Message**
Always validate on real data, even when training on synthetic.
### **Autofix**


## No Synthetic Data Flag

### **Id**
no-synthetic-flag
### **Severity**
info
### **Description**
Mark synthetic examples for tracking
### **Pattern**
  syntheticData\.push(?!.*synthetic.*true|source.*synthetic)
  
### **Message**
Mark synthetic examples with a flag for analysis.
### **Autofix**
