# Neural Architecture Search - Validations

## NAS Without Compute Budget

### **Id**
no-compute-budget
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - optimize\(.*n_trials\s*=\s*None
  - study\.optimize(?!.*n_trials|.*timeout)
### **Message**
Set compute budget for NAS to prevent runaway resource usage.
### **Fix Action**
Add: n_trials=100 or timeout=3600
### **Applies To**
  - **/*.py

## NAS Without Seed Setting

### **Id**
no-seed-setting
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - optuna\.create_study(?!.*seed)
  - random\.choice(?!.*seed|.*random\.seed)
### **Message**
Set random seeds for reproducible NAS results.
### **Fix Action**
Add: sampler=optuna.samplers.TPESampler(seed=42)
### **Applies To**
  - **/*search*.py
  - **/*nas*.py

## NAS Without Early Stopping/Pruning

### **Id**
no-pruning
### **Severity**
info
### **Type**
regex
### **Pattern**
  - create_study(?!.*pruner)
### **Message**
Enable pruning to stop unpromising trials early.
### **Fix Action**
Add: pruner=optuna.pruners.MedianPruner()
### **Applies To**
  - **/*optuna*.py

## NAS Without Experiment Tracking

### **Id**
no-experiment-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - create_study(?!.*storage|.*study_name)
### **Message**
Use persistent storage for NAS experiment tracking.
### **Fix Action**
Add: storage='sqlite:///optuna.db', study_name='experiment'
### **Applies To**
  - **/*optuna*.py

## Unbounded Search Space Parameters

### **Id**
unbounded-search-space
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - suggest_int.*1,\s*1000
  - suggest_float.*1e-10,\s*1e10
  - suggest_int.*0,\s*\d{4,}
### **Message**
Very large search ranges may be intractable. Consider constraining.
### **Fix Action**
Narrow range based on domain knowledge or prior results.
### **Applies To**
  - **/*.py

## NAS Without Full Task Validation

### **Id**
no-validation-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - best_trial\.value(?!.*validate|.*full)
### **Message**
Validate best NAS result on full task, not just proxy.
### **Fix Action**
Retrain best architecture on full dataset and evaluate.
### **Applies To**
  - **/*nas*.py
  - **/*search*.py