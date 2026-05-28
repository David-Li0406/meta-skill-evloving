# Experimental Design - Validations

## One-Factor-At-A-Time Pattern

### **Id**
ofat-pattern
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*in.*values:\s*\n.*test.*single
  - vary.*one.*at.*time
### **Message**
Consider factorial design instead of OFAT for interaction effects.
### **Applies To**
  - **/*.py

## Missing Run Order Randomization

### **Id**
no-randomization
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*treatment.*in.*order(?![\s\S]{0,200}shuffle|random)
### **Message**
Randomize run order to prevent time-based confounds.
### **Fix Action**
np.random.shuffle(run_order)
### **Applies To**
  - **/*.py

## Design Without Power Analysis

### **Id**
no-power-analysis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - n.*=.*[1-9]\d?(?!\d).*experiment
### **Message**
Calculate required sample size with power analysis before running.
### **Applies To**
  - **/*.py

## Factorial Without Replication

### **Id**
no-replication
### **Severity**
info
### **Type**
regex
### **Pattern**
  - factorial.*n_rep.*=.*1|fullfact(?![\s\S]{0,200}replicate)
### **Message**
Include replicates to estimate pure error.
### **Applies To**
  - **/*.py

## Potential Nuisance Variable Not Blocked

### **Id**
missing-blocking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - day|batch|operator(?![\s\S]{0,300}block)
### **Message**
Consider blocking on known nuisance variables (day, batch, etc.).
### **Applies To**
  - **/*.py