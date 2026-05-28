# Protein Structure - Validations

## Analysis on Low-Confidence Regions

### **Id**
using-low-plddt-regions
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - binding_site.*residue.*pLDDT.*<\s*50
  - dock.*region.*confidence.*low
  - interpret.*loop.*disordered
### **Message**
Avoid structural interpretation of regions with pLDDT < 50 (likely disordered).
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Structure Analysis Without Confidence Check

### **Id**
no-plddt-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - load.*alphafold.*pdb(?![\s\S]{0,300}plddt|bfactor|confidence)
  - PDBParser.*alphafold(?![\s\S]{0,300}bfactor)
### **Message**
Check pLDDT (B-factor column) before interpreting AlphaFold structures.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Complex Analysis Without PAE Check

### **Id**
no-pae-for-complex
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - multimer|complex.*predict(?![\s\S]{0,500}pae|predicted_aligned_error)
  - interface.*analysis(?![\s\S]{0,300}pae)
### **Message**
Check PAE matrix for domain/interface confidence in complexes.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Using Only Top-Ranked Model

### **Id**
single-model-only
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ranked_0\.pdb(?![\s\S]{0,200}ranked_[1-4])
  - model_0(?![\s\S]{0,200}model_[1-4])
### **Message**
Consider comparing multiple ranked models for conformational diversity.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Using Unrelaxed Model for Downstream

### **Id**
no-relaxation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - unrelaxed.*\.pdb.*dock
  - predict(?![\s\S]{0,200}relax|amber).*structure
### **Message**
Consider AMBER relaxation before docking or molecular dynamics.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Glycoprotein Without Glycan Note

### **Id**
missing-glycan-consideration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - antibody.*epitope.*predict
  - surface.*accessibility.*glycoprotein
### **Message**
Consider glycan shielding effects for glycoprotein analysis.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Trusting Predicted Interface Without Validation

### **Id**
trusting-af-interface
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - interface.*residue.*alphafold.*interact
  - complex.*predict.*binding_site
### **Message**
Validate predicted interfaces experimentally; ipTM > 0.8 for high confidence.
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Using Old AlphaFold DB Version

### **Id**
outdated-alphafold-db
### **Severity**
info
### **Type**
regex
### **Pattern**
  - alphafold.*v[12](?!v4)
  - AF-.*-F1-model_v[12]
### **Message**
Consider using AlphaFold DB v4 for latest predictions.
### **Applies To**
  - **/*.py
  - **/*.sh