# Drug Discovery Informatics - Validations

## Screening Without PAINS Filter

### **Id**
no-pains-filter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - screen.*compound(?![\s\S]{0,500}pains|filter)
  - virtual.*screen(?![\s\S]{0,500}pains|filter_catalog)
### **Message**
Filter PAINS (pan-assay interference compounds) before screening.
### **Fix Action**
Add FilterCatalog with PAINS filters
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Treating Docking Score as Binding Affinity

### **Id**
docking-score-as-kd
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - docking.*score.*\bKd\b|\bKi\b
  - affinity.*=.*docking_score
  - predicted.*binding.*kcal
### **Message**
Docking scores are relative rankings, not absolute affinities.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Docking Box Too Small

### **Id**
small-docking-box
### **Severity**
info
### **Type**
regex
### **Pattern**
  - box_size.*=.*\(\s*[0-9]\s*,
  - size_[xyz].*=.*[0-9](?![0-9])
### **Message**
Docking box may be too small. Typical size is 15-25 Angstroms per dimension.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Lead Optimization Without ADMET Tracking

### **Id**
no-admet-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - optimize.*potency(?![\s\S]{0,500}admet|lipinski|druglike)
  - lead.*optimization(?![\s\S]{0,500}properties)
### **Message**
Include ADMET property monitoring during lead optimization.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Single Docking Program Only

### **Id**
no-consensus-scoring
### **Severity**
info
### **Type**
regex
### **Pattern**
  - vina\.dock(?![\s\S]{0,500}glide|gold|gnina)
  - run_docking(?![\s\S]{0,300}consensus)
### **Message**
Consider consensus scoring from multiple docking programs.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Random Split for QSAR (Not Scaffold-Based)

### **Id**
random-train-test-split
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - train_test_split.*smiles|compound
  - random.*split.*activity
### **Message**
Use scaffold-based split for QSAR to avoid data leakage.
### **Fix Action**
Use GroupShuffleSplit with molecule scaffolds
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Compounds Without Drug-Likeness Filter

### **Id**
no-lipinski-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - generate.*molecule(?![\s\S]{0,500}lipinski|druglike|ro5)
  - library.*compound(?![\s\S]{0,500}filter)
### **Message**
Apply Lipinski's Rule of Five or similar drug-likeness filter.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Hardcoded Binding Site Coordinates

### **Id**
hardcoded-binding-site
### **Severity**
info
### **Type**
regex
### **Pattern**
  - center_[xyz].*=.*[0-9]+\.[0-9]+
  - binding_site.*=.*\[.*[0-9]+\.[0-9]+
### **Message**
Define binding site from structure or ligand, not hardcoded values.
### **Applies To**
  - **/*.py
  - **/*.ipynb