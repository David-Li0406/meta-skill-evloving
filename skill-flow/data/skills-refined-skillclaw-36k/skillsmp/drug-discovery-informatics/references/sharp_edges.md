# Drug Discovery Informatics - Sharp Edges

## Treating Docking Scores as Binding Affinities

### **Id**
docking-score-overconfidence
### **Severity**
critical
### **Summary**
Docking scores poorly correlate with experimental binding
### **Symptoms**
  - Ranking compounds purely by docking score
  - Reporting docking score as predicted Kd
  - Excluding compounds based on score cutoff alone
### **Why**
  Docking scores are RELATIVE rankings, not absolute affinities.
  Correlation with experimental Kd is typically R² = 0.2-0.4.
  
  Common issues:
  - Scoring functions trained on limited data
  - Solvation effects poorly modeled
  - Protein flexibility ignored
  - Entropic contributions missed
  
  A compound with docking score -10 isn't "better" than -8
  in any absolute sense.
  
### **Gotcha**
  # WRONG: Using score as activity prediction
  compounds_df = compounds_df[compounds_df['docking_score'] < -8]
  # Throws away potentially active compounds!
  
  # WRONG: Reporting score as Kd
  "Predicted binding affinity: -9.2 kcal/mol"
  # This is meaningless without validation
  
### **Solution**
  # Use docking for pose prediction, not affinity
  # Validate top hits experimentally
  
  # Use consensus scoring
  def consensus_rank(scores_dict):
      ranks = {}
      for program, scores in scores_dict.items():
          ranks[program] = scores.rank()
      return pd.DataFrame(ranks).mean(axis=1)
  
  # Report as relative ranking, not absolute
  "Compound ranked in top 1% by docking"
  
  # Validate with orthogonal methods
  # - FEP calculations for accurate affinity
  # - MD simulations for pose stability
  # - Experimental binding assays
  

## Not Filtering for Pan-Assay Interference Compounds

### **Id**
ignoring-pains
### **Severity**
high
### **Summary**
PAINS give false positives in biochemical assays
### **Symptoms**
  - Hit compound active against many unrelated targets
  - Activity doesn't translate to cellular assays
  - SAR is flat (all analogs equally active)
### **Why**
  Pan-Assay INterference compoundS (PAINS) are promiscuous hitters
  that interfere with assays through non-specific mechanisms:
  - Redox cycling
  - Aggregation
  - Fluorescence interference
  - Metal chelation
  - Covalent modification of assay proteins
  
  ~5% of commercial screening compounds are PAINS.
  They waste years of medicinal chemistry effort.
  
### **Gotcha**
  # Rhodanine - classic PAINS motif
  hit_smiles = "O=C1NC(=S)S/C1=C/c2ccccc2"
  # Will show activity in many assays, none real
  
  # Screening without PAINS filter
  hits = screen(library, target)
  # 20% of hits may be PAINS false positives
  
### **Solution**
  from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
  
  def filter_pains(smiles_list):
      params = FilterCatalogParams()
      params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
      catalog = FilterCatalog(params)
  
      clean_compounds = []
      for smiles in smiles_list:
          mol = Chem.MolFromSmiles(smiles)
          if not catalog.HasMatch(mol):
              clean_compounds.append(smiles)
  
      return clean_compounds
  
  # Also check Brenk filters for reactive compounds
  # Run orthogonal counter-screens
  

## Incorrect Binding Site Definition

### **Id**
poor-binding-site-definition
### **Severity**
high
### **Summary**
Wrong box size or center leads to missed poses
### **Symptoms**
  - Known binders get poor scores
  - Re-docking doesn't reproduce crystal pose
  - Best poses are at box edges
### **Why**
  Docking requires defining where ligands can bind.
  If the box is:
  - Too small: Misses valid binding modes
  - Too large: Searches irrelevant space, slower
  - Off-center: Best poses at edges (unreliable)
  
  Crystal structure ligand position is best guide.
  But for novel sites, use site prediction tools.
  
### **Gotcha**
  # Box too small - clips ligand poses
  config = DockingConfig(box_size=(10, 10, 10))  # Too small for most drugs
  
  # Center at random residue
  center = get_residue_center("ALA123")  # Not the binding site!
  
### **Solution**
  # Use known ligand to define site
  def define_box_from_ligand(complex_pdb, ligand_name, padding=5):
      ligand_atoms = get_ligand_atoms(complex_pdb, ligand_name)
      center = np.mean(ligand_atoms, axis=0)
      extent = np.ptp(ligand_atoms, axis=0) + 2 * padding
      return center, extent
  
  # For unknown sites, use cavity detection
  # fpocket, SiteMap, DoGSiteScorer
  
  # Validate by re-docking known ligand
  # RMSD < 2.0 Å from crystal pose = good
  

## Using Standard Docking for Covalent Inhibitors

### **Id**
covalent-docking-mistake
### **Severity**
critical
### **Summary**
Standard docking cannot model covalent bond formation
### **Symptoms**
  - Covalent inhibitors score poorly
  - Warhead not positioned near reactive residue
  - Known covalent drugs rank low
### **Why**
  Standard docking treats ligand and protein as non-bonded.
  Covalent inhibitors form bonds with specific residues
  (usually Cys, Ser, Lys). The docking program:
  - Doesn't know which atom is the warhead
  - Doesn't model bond formation energy
  - Places warhead randomly
  
  Results are essentially meaningless.
  
### **Gotcha**
  # Docking a covalent EGFR inhibitor (afatinib) with Vina
  vina_dock(receptor, afatinib)  # Standard docking
  # Result: Acrylamide warhead points away from Cys797
  
### **Solution**
  # Use covalent docking tools
  # - Schrödinger CovDock
  # - DOCKovalent
  # - GOLD covalent mode
  # - AutoDock-GPU covalent
  
  # Define reactive residue and warhead type
  covalent_config = CovalentDockingConfig(
      reactive_residue="CYS797",
      warhead_type="acrylamide",
      reaction_type="michael_addition"
  )
  
  # Gold covalent example
  gold_covalent_dock(receptor, ligand, covalent_config)
  

## Considering ADMET Only After Lead Selection

### **Id**
admet-afterthought
### **Severity**
critical
### **Summary**
Leads fail late due to properties known early
### **Symptoms**
  - Potent compounds fail in PK studies
  - Extensive optimization wasted on fundamentally flawed scaffolds
  - High attrition in preclinical development
### **Why**
  ~50% of clinical drug development failures are due to ADMET issues.
  Many ADMET properties are determined by the chemical scaffold.
  If you optimize a flawed scaffold for potency, you can't fix ADMET later.
  
  Common late-stage failures:
  - Poor oral bioavailability
  - Rapid metabolism (short half-life)
  - CYP inhibition (drug-drug interactions)
  - hERG liability (cardiac toxicity)
  
### **Gotcha**
  # Optimize potency, ignore ADMET
  lead = optimize_for_potency(hit)
  # Result: IC50 = 1 nM, but LogP = 7, MW = 650
  # Zero chance of oral drug
  
  # Check ADMET only at the end
  admet = predict_admet(lead)
  # "Hepatotoxicity: HIGH" - 2 years wasted
  
### **Solution**
  # Multi-parameter optimization from the start
  objectives = {
      'potency': 'maximize',
      'logp': ('target', 3.0),  # Keep in sweet spot
      'mw': ('max', 500),
      'tpsa': ('range', (40, 90)),
      'cyp_inhibition': 'minimize',
      'herg_liability': 'minimize'
  }
  
  # Filter by ADMET before optimization
  def admet_filter(compound):
      props = predict_admet(compound)
      return (
          props['logp'] < 5 and
          props['mw'] < 500 and
          props['herg_risk'] != 'high' and
          not props['ames_mutagenic']
      )
  
  # Track ADMET trajectory during optimization
  # Flag if properties trending wrong
  

## Overfitting QSAR Models to Training Data

### **Id**
overfitting-qsar
### **Severity**
high
### **Summary**
Models perform well on training, fail on new compounds
### **Symptoms**
  - Model R² = 0.99 on training, 0.3 on test
  - Predictions wrong for novel scaffolds
  - Activity cliffs not captured
### **Why**
  QSAR models often overfit when:
  - Too many descriptors vs. compounds
  - No proper train/test split
  - Same scaffold in train and test
  - Not validating on external set
  
  Overfitted models give false confidence.
  
### **Solution**
  # Proper validation
  from sklearn.model_selection import cross_val_score
  
  # Use scaffold-based split (not random!)
  train, test = scaffold_split(data, test_size=0.2)
  
  # Cross-validation
  scores = cross_val_score(model, X, y, cv=5)
  
  # External validation set (new scaffolds)
  external_set = compounds_from_different_project
  
  # Applicability domain
  # Don't predict outside training space
  