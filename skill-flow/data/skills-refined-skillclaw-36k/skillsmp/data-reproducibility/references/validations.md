# Data Reproducibility - Validations

## Random Operations Without Seed

### **Id**
no-seed-before-random
### **Severity**
error
### **Type**
regex
### **Pattern**
  - np\.random\.(rand|randn|choice)(?![\s\S]{0,200}seed)
  - random\.(shuffle|choice)(?![\s\S]{0,200}seed)
### **Message**
Set random seed before any random operations for reproducibility.
### **Fix Action**
np.random.seed(42) or random.seed(42)
### **Applies To**
  - **/*.py

## Hardcoded Absolute Paths

### **Id**
hardcoded-absolute-path
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - read_csv\(['"]C:|read_csv\(['"]D:
  - read_csv\(['"]Users/|read_csv\(['"]/home/
### **Message**
Hardcoded paths break reproducibility on other systems.
### **Fix Action**
Use relative paths or environment variables
### **Applies To**
  - **/*.py

## Unpinned Package Versions

### **Id**
unpinned-dependencies
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^[a-z][a-z0-9-]*$
  - pip install (?!.*==)
### **Message**
Pin exact versions for reproducibility: package==1.2.3
### **Applies To**
  - **/requirements*.txt
  - **/*.sh

## CUDA Without Deterministic Mode

### **Id**
no-deterministic-cuda
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - torch\.cuda(?![\s\S]{0,300}deterministic)
### **Message**
Set torch.backends.cudnn.deterministic = True for reproducibility.
### **Applies To**
  - **/*.py

## Missing Experiment Manifest

### **Id**
no-experiment-manifest
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def.*experiment(?![\s\S]{0,500}manifest|provenance|version)
### **Message**
Log environment, seeds, and versions for reproducibility.
### **Applies To**
  - **/*.py

## Current Datetime in Feature Engineering

### **Id**
datetime-now-in-features
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - datetime\.now\(\).*feature|feature.*datetime\.now
### **Message**
Using current time in features breaks reproducibility.
### **Fix Action**
Use a fixed reference date instead
### **Applies To**
  - **/*.py