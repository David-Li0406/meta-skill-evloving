# Data Reproducibility - Sharp Edges

## Floating Point Non-determinism Across Hardware

### **Id**
floating-point-nondeterminism
### **Severity**
critical
### **Summary**
Same code, same seed, different results on different GPUs
### **Symptoms**
  - Results differ between local and cloud
  - CI produces different numbers than laptop
  - Model checkpoints don't reproduce exactly
### **Why**
  GPU operations often use non-deterministic algorithms for speed.
  Different hardware has different floating point precision.
  Order of operations affects floating point results.
  
### **Gotcha**
  # Set seed everywhere
  torch.manual_seed(42)
  # But still get different results!
  
  # GPU operations are non-deterministic by default
  # cudnn autotuning picks fastest (not reproducible) algorithm
  
### **Solution**
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  torch.use_deterministic_algorithms(True)
  # Note: Some ops don't have deterministic implementations
  

## Implicit System Dependencies

### **Id**
implicit-dependencies
### **Severity**
critical
### **Summary**
pip freeze misses system libraries your code depends on
### **Symptoms**
  - Works on your machine, fails on fresh install
  - Cryptic import errors about missing .so files
  - Different numerical results on different systems
### **Why**
  Python packages often wrap system libraries (BLAS, LAPACK, OpenSSL).
  pip/conda can't capture system-level dependencies.
  Different systems have different versions installed.
  
### **Solution**
  1. Use Docker for complete isolation
  2. Document system requirements in README
  3. Use conda for scientific packages (bundles system libs)
  4. Test in clean environment before publishing
  

## Data Changed But Nobody Noticed

### **Id**
data-drift-unnoticed
### **Severity**
high
### **Summary**
Upstream data source changed, breaking reproducibility
### **Symptoms**
  - Model performance suddenly drops
  - Can't reproduce old results with current data
  - Results from paper don't match current code
### **Solution**
  1. Version data with DVC or similar
  2. Hash all input data in manifests
  3. Archive exact dataset used for publications
  4. Never depend on mutable data sources for research
  

## Timestamps Introduce Hidden Randomness

### **Id**
timestamp-randomness
### **Severity**
high
### **Summary**
datetime.now() in features breaks reproducibility
### **Symptoms**
  - Different results when run at different times
  - Time-based features change between runs
### **Solution**
  # Bad
  df['age'] = (datetime.now() - df['birth_date']).days / 365
  
  # Good: Use fixed reference date
  REFERENCE_DATE = datetime(2024, 1, 1)
  df['age'] = (REFERENCE_DATE - df['birth_date']).days / 365
  

## Python Dict/Set Ordering Was Random Before 3.7

### **Id**
order-dependent-hashing
### **Severity**
medium
### **Summary**
Hash randomization affects iteration order
### **Symptoms**
  - Different feature order in older Python
  - PYTHONHASHSEED not set
### **Solution**
  os.environ['PYTHONHASHSEED'] = '0'
  # Or use Python 3.7+ where dicts maintain insertion order
  