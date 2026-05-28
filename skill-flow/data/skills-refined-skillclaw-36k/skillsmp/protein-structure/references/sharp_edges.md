# Protein Structure - Sharp Edges

## Treating Low-Confidence Regions as Structured

### **Id**
low-plddt-as-structure
### **Severity**
critical
### **Summary**
Interpreting pLDDT < 50 regions as real structures, not disorder
### **Symptoms**
  - Publishing figures showing loops with pLDDT < 50
  - Docking ligands to low-confidence binding sites
  - Making functional claims about disordered regions
### **Why**
  AlphaFold2 predicts EVERYTHING as some structure, even intrinsically
  disordered regions. pLDDT < 50 indicates the model has no confidence
  in the structure - it's essentially random.
  
  These regions are likely:
  - Intrinsically disordered (no stable structure exists)
  - Flexible linkers between domains
  - Regions that only fold upon binding
  
  Treating them as structured leads to wrong conclusions and
  wasted experimental effort.
  
### **Gotcha**
  # Paper shows "novel loop structure" at residues 120-150
  # But pLDDT for this region is 35-45
  # There IS no structure - it's just what the model guessed
  
  # Docking to predicted "binding pocket"
  docking_site = residues_120_150  # pLDDT < 50
  # These residues probably don't maintain this conformation!
  
### **Solution**
  # Always check pLDDT before interpreting structure
  def is_structured_region(plddt_scores, start, end, threshold=70):
      region_plddt = plddt_scores[start:end]
      return np.mean(region_plddt) >= threshold
  
  # Visualize by confidence
  # Blue (>90): Trust it
  # Light blue (70-90): Probably correct
  # Yellow (50-70): Uncertain
  # Red (<50): Likely disordered - DON'T INTERPRET
  
  # For disordered regions, report them as such:
  "Residues 120-150 are predicted to be disordered (mean pLDDT = 42)"
  

## Trusting Relative Domain Orientation Without Checking PAE

### **Id**
domain-orientation-trust
### **Severity**
critical
### **Summary**
Multi-domain predictions often have correct domains but wrong orientation
### **Symptoms**
  - Using predicted inter-domain contacts for experimental design
  - Claiming domain-domain interactions from prediction
  - Docking based on predicted domain arrangement
### **Why**
  AlphaFold2 can predict individual domains accurately while completely
  failing at their relative orientation. Each domain might have pLDDT > 90,
  but the angle between them could be arbitrary.
  
  The PAE (Predicted Aligned Error) matrix reveals this:
  - Blue on diagonal = confident domains
  - Red between domains = uncertain orientation
  
  This is especially problematic for:
  - Multi-domain proteins with flexible linkers
  - Protein complexes
  - Proteins with domain rearrangements
  
### **Gotcha**
  # Protein has two domains, both with pLDDT > 85
  # But PAE between domains is > 20 Angstrom
  # The relative orientation is essentially random!
  
  # Wrong conclusion:
  "Domain A contacts domain B at interface X"
  
  # Reality:
  "Domain A and B structures are reliable, but their
   relative orientation is unknown"
  
### **Solution**
  # Always check PAE matrix for multi-domain proteins
  def check_domain_confidence(pae_matrix, domain1_range, domain2_range):
      inter_domain_pae = pae_matrix[
          domain1_range[0]:domain1_range[1],
          domain2_range[0]:domain2_range[1]
      ]
      mean_pae = np.mean(inter_domain_pae)
  
      if mean_pae > 15:
          return "UNRELIABLE: Domain orientation uncertain"
      elif mean_pae > 10:
          return "CAUTION: Some uncertainty in orientation"
      else:
          return "CONFIDENT: Domain orientation likely correct"
  
  # For uncertain orientations:
  # 1. Analyze domains separately
  # 2. Use experimental data (SAXS, crosslinking) to constrain
  # 3. Sample multiple conformations
  

## Over-Trusting Protein Complex Predictions

### **Id**
complex-prediction-overconfidence
### **Severity**
high
### **Summary**
Complex predictions are less reliable than monomer predictions
### **Symptoms**
  - Using AF-Multimer for novel interaction discovery
  - Trusting interface residues without experimental validation
  - Missing false positive interactions
### **Why**
  AF-Multimer can predict complexes, but:
  - Training was mostly on known complexes
  - False positives: Predicts complexes that don't exist
  - Interface accuracy varies widely
  - Stoichiometry must be known in advance
  
  The ipTM score helps but isn't definitive.
  Experimental validation is essential.
  
### **Gotcha**
  # AF-Multimer predicts A-B complex with ipTM = 0.6
  # Conclusion: "A and B interact"
  # But 0.6 ipTM doesn't guarantee real interaction!
  
  # Wrong stoichiometry input:
  predict_complex(["A", "B"])  # Assumes 1:1
  # Reality might be 2:1 or transient
  
### **Solution**
  # Complex prediction best practices:
  # 1. Only predict complexes with experimental evidence of interaction
  # 2. ipTM > 0.8 for high confidence
  # 3. Check interface makes biological sense
  # 4. Validate key residues experimentally
  
  def assess_complex_confidence(iptm, interface_pae):
      if iptm >= 0.8 and interface_pae < 10:
          return "HIGH - likely accurate"
      elif iptm >= 0.6:
          return "MEDIUM - validate interface"
      else:
          return "LOW - don't trust without validation"
  

## Membrane Protein Predictions Without Context

### **Id**
membrane-protein-issues
### **Severity**
high
### **Summary**
AlphaFold doesn't model membrane environment
### **Symptoms**
  - Transmembrane helices in wrong orientation
  - Lipid-facing residues shown as solvent-exposed
  - Missing membrane-induced conformational effects
### **Why**
  AlphaFold2 predicts membrane proteins as if in water.
  This means:
  - Membrane orientation may be inverted
  - Lipid-exposed surfaces are treated like water-exposed
  - Conformational changes requiring membrane are missed
  
  The structure may be "correct" but unusable for
  membrane-related questions.
  
### **Solution**
  # Post-processing for membrane proteins:
  # 1. Predict topology with TOPCONS or DeepTMHMM
  # 2. Orient structure in membrane with PPM server
  # 3. Consider membrane effects on dynamics
  
  # Use specialized membrane predictors when available
  # Or integrate with experimental membrane data
  

## Glycoprotein Predictions Missing Glycosylation

### **Id**
glycoprotein-missing-glycans
### **Severity**
medium
### **Summary**
AlphaFold doesn't predict glycans attached to proteins
### **Symptoms**
  - Using unglycosylated model for antibody epitope prediction
  - Missing glycan shield effects
  - Surface accessibility calculations wrong
### **Why**
  AlphaFold2 predicts the protein chain only.
  Glycans can:
  - Block antibody access (glycan shield)
  - Stabilize protein structure
  - Be essential for function
  
  The "bare" model may be misleading for glycoproteins.
  
### **Solution**
  # Check glycosylation sites
  # N-glycosylation: N-X-S/T motif
  # O-glycosylation: No clear motif
  
  # Add glycans computationally:
  # - GlyProt server
  # - CHARMM-GUI Glycan Reader
  
  # Report glycan sites:
  "Note: N120 is a known glycosylation site; glycan not modeled"
  

## Assuming Single Conformation Represents All States

### **Id**
single-conformation-assumption
### **Severity**
high
### **Summary**
Proteins exist in conformational ensembles, not single structures
### **Symptoms**
  - Claiming active site is 'closed' based on prediction
  - Missing allosteric conformational changes
  - Failing to sample alternative states
### **Why**
  AlphaFold2 typically predicts the most stable/common conformation.
  Proteins often have:
  - Open/closed states
  - Ligand-induced changes
  - Allosteric conformations
  - Breathing motions
  
  A single model doesn't capture this dynamics.
  
### **Solution**
  # Sample multiple conformations
  config = PredictionConfig(
      num_models=5,
      num_recycles=[1, 3, 6, 12],  # Different depths
      dropout=True  # Enable for diversity
  )
  
  # Compare models for conformational diversity
  # Use molecular dynamics for ensemble generation
  # Integrate with experimental ensemble data
  