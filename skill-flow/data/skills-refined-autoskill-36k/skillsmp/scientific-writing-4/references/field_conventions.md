# Field-Specific Conventions Reference

## Contents
1. [Biomedical/Clinical](#biomedicalclinical)
2. [Molecular Biology](#molecular-biology)
3. [Chemistry](#chemistry)
4. [Neuroscience](#neuroscience)
5. [Ecology](#ecology)
6. [Physics/Engineering](#physicsengineering)
7. [Social/Behavioral Sciences](#socialbehavioral-sciences)
8. [Machine Learning/CS](#machine-learningcs)

---

## Biomedical/Clinical

### Terminology
- Use precise anatomical/clinical terms ("myocardial infarction" not "heart attack")
- Follow ICD, DSM, SNOMED-CT nomenclature
- Generic drug names first: "metformin (Glucophage)"
- "Patients" for clinical studies, "participants" for community research

### Genetic Variants
Follow HGVS nomenclature:
- DNA: c.76A>T (coding), g.12345A>T (genomic)
- Protein: p.Arg25Cys or p.R25C
- Reference sequence required: NM_000123.4:c.76A>T

### Units
- SI units for most international journals
- Report lab values with reference ranges
- Blood pressure: mmHg
- Temperature: °C

### Statistics
- Report absolute numbers with percentages: "32 (64%)"
- Include 95% CI for main outcomes
- NNT/NNH for clinical significance

---

## Molecular Biology

### Gene/Protein Nomenclature
| Species | Gene | Protein |
|---------|------|---------|
| Human | *BRCA1* (italic, uppercase) | BRCA1 (regular, uppercase) |
| Mouse | *Brca1* (italic, sentence case) | Brca1 (regular, sentence case) |
| General | *gene* (italic) | Protein (regular) |

### Species Names
- Full at first mention: *Escherichia coli*
- Abbreviated after: *E. coli*
- Italicize genus and species

### Techniques
- "quantitative PCR" or "qPCR" (not "real-time PCR")
- "Western blot" (capitalized)
- "CRISPR-Cas9" (specific system)

### Sequence Data
- Accession numbers required for deposited sequences
- Report GenBank/EMBL/DDBJ numbers

---

## Chemistry

### Nomenclature
- IUPAC names for novel compounds
- Common names acceptable for well-known substances
- CAS numbers for unambiguous identification

### Structure Notation
- SMILES for machine-readable
- InChI for databases
- Chemical drawings following IUPAC conventions

### Concentrations
| Unit | Use Case |
|------|----------|
| M, mM, μM, nM | Solution concentration |
| % w/v | Weight per volume |
| % v/v | Volume per volume |
| ppm, ppb | Trace amounts |

### Reactions
- Use standard arrow notation (→, ⇌)
- Report yields as percentage
- Specify conditions (temperature, solvent, catalyst)

---

## Neuroscience

### Brain Regions
- Use standardized nomenclature (Allen Brain Atlas, Paxinos)
- Specify coordinates: "AP: -3.2, ML: ±2.0, DV: -4.5 from bregma"
- Abbreviations after first use: "prefrontal cortex (PFC)"

### Neural Activity
| Term | Measurement |
|------|-------------|
| "neural activity" | General |
| "neuronal firing" | Single-unit recording |
| "brain activation" | fMRI BOLD signal |
| "oscillations" | LFP/EEG rhythms |

### Techniques
- Specify fully: "whole-cell patch clamp recording"
- Include sampling rates for electrophysiology
- Report signal processing parameters

### Behavioral Measures
- Use validated test names exactly
- Cite original validation papers
- Report inter-rater reliability if applicable

---

## Ecology

### Taxonomic Names
- Binomial: *Homo sapiens*
- Authority at first mention if relevant: *Quercus robur* L.
- Common names lowercase unless proper nouns

### Ecological Metrics
- "species richness" (count)
- "Shannon diversity index" (H')
- "Simpson's diversity index" (D)
- Report with units and methods

### Sampling Methods
- Standardized terms: "transect," "quadrat," "mark-recapture"
- Report effort: "100 trap-nights"
- Include GPS coordinates when appropriate

### Habitat Classification
- Use standardized systems (IUCN, CORINE)
- Define custom classifications clearly

---

## Physics/Engineering

### Units
- SI units unless field conventions differ
- Specify: "5.2 ± 0.3 nm" (value ± uncertainty)
- Use scientific notation consistently: 3.2 × 10⁸ m/s

### Mathematical Notation
- Scalars: italic (*m*, *v*)
- Vectors: bold (**v**) or arrow (v⃗)
- Matrices: bold uppercase (**A**)
- ℏ for reduced Planck constant

### Physical Quantities
- Define symbols at first use
- Use established notation for field
- Consistent notation throughout

### Equipment
- Model numbers and manufacturers
- Calibration information
- Operating parameters

---

## Social/Behavioral Sciences

### Language Guidelines
- Person-first: "people with schizophrenia" not "schizophrenics"
- Avoid stigmatizing language
- Follow APA bias-free language guidelines
- "Participants" not "subjects" for humans

### Constructs
- Use established psychological construct names
- Cite validated assessment tools
- Report Cronbach's α for scales

### Demographics
- Report: age (M, SD, range), gender/sex, race/ethnicity, SES
- Use participant-preferred terminology
- Follow journal guidelines for demographic reporting

### Theoretical Frameworks
- Name theories explicitly
- Cite seminal sources
- Define key constructs operationally

---

## Machine Learning/CS

### Model Description
- Architecture: "3-layer MLP with 256, 128, 64 units"
- Activation functions: "ReLU," "softmax"
- Regularization: "dropout (p=0.5)," "L2 (λ=0.01)"

### Training Details
- Optimizer: "Adam (lr=0.001, β₁=0.9, β₂=0.999)"
- Batch size, epochs
- Hardware: "NVIDIA A100, 40GB"
- Training time

### Evaluation
- Standard metrics with definitions
- Report mean ± std over multiple runs
- Include confidence intervals
- Specify test set (held-out, cross-validation)

### Reproducibility
- Random seeds
- Dataset splits
- Code availability
- Environment specifications (PyTorch version, CUDA)

### Terminology
| Term | Use |
|------|-----|
| "model" | The learned function |
| "architecture" | Network structure |
| "hyperparameters" | User-set values |
| "parameters" | Learned weights |

---

## General Principles

### Consistency
- Same term for same concept throughout
- One abbreviation system
- Consistent notation

### Audience Matching
- Specialist journal: technical terms freely
- Broad journal: define more terms
- Interdisciplinary: balance precision and accessibility

### Verification
- Check recent papers in target journal
- Consult field-specific style guides
- Use domain databases (MeSH, Gene Ontology)
