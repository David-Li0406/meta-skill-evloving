---
name: neuroimaging-qc
description: Evidence-based QC decision-making for neuroimaging data. Interpret QC metrics from any pipeline (fMRIPrep, MRIQC, FreeSurfer, MNE-Python, Homer3, custom outputs) to make justified inclusion/exclusion decisions. Covers fMRI, EEG, fNIRS, and structural MRI across populations (adults, infants, adolescents, clinical) and paradigms (resting-state, task, naturalistic, sleep). Use when filtering subjects based on QC outputs, setting exclusion thresholds, justifying QC criteria for methods sections, or parsing QC files programmatically with Python.
---

# Neuroimaging QC Decision-Making

Evidence-based guidance for interpreting QC metrics and making principled inclusion/exclusion decisions.

## Core Principles

### 1. No Universal Thresholds
QC thresholds are study-specific. Factors affecting appropriate cutoffs:
- **Population**: Infants tolerate higher motion than adults
- **Paradigm**: Task fMRI has different constraints than resting-state
- **Analysis**: Connectivity analyses are more motion-sensitive than activation
- **Sample size**: Stricter thresholds with larger N; lenient with small N

### 2. Distribution-Based Decisions
Always examine your sample's QC distribution before applying thresholds:
1. Plot histograms of key metrics
2. Identify natural breakpoints/outliers (>2-3 SD from mean)
3. Apply literature-based thresholds as starting points, adjust based on distribution
4. Report both threshold AND resulting exclusion rate

### 3. Multi-Metric Assessment
Never exclude based on single metric. Combine:
- Motion metrics (FD, DVARS)
- Signal quality metrics (tSNR, SNR)
- Artifact indicators (outlier volumes, registration quality)
- Visual inspection for edge cases

## Decision Workflow

```
1. IDENTIFY your QC source
   ├── Known pipeline (fMRIPrep, MRIQC, etc.) → See modality references
   └── Custom/unknown output → Parse available metrics, map to known categories

2. CHARACTERIZE your study
   ├── Population: adult / pediatric / infant / clinical
   ├── Paradigm: rest / task / naturalistic / sleep
   └── Analysis: activation / connectivity / other

3. ESTABLISH thresholds
   ├── Start with literature recommendations (see references)
   ├── Examine your sample distribution
   └── Adjust based on trade-off: data quality vs. statistical power

4. APPLY and DOCUMENT
   ├── Generate exclusion summary
   ├── Report thresholds with citations
   └── Conduct sensitivity analysis with stricter/lenient thresholds
```

## Quick Reference: Common Thresholds

### fMRI Motion (FD)

| Population | Conservative | Standard | Lenient | Citation |
|------------|-------------|----------|---------|----------|
| Adults (rest) | 0.2 mm | 0.3 mm | 0.5 mm | Power et al., 2012, 2014 |
| Adults (task) | 0.5 mm | 0.9 mm | 1.0 mm | Siegel et al., 2014 |
| Children (6-12y) | 0.3 mm | 0.4 mm | 0.5 mm | Fair et al., 2012 |
| Infants | 0.3 mm | 0.5 mm | — | Population-dependent |
| Neonates | 0.2 mm | 0.5 mm | — | Smyser et al., 2010 |

**Additional motion criteria:**
- fd_perc (% volumes > threshold): typically exclude if >20-50%
- Maximum FD spike: consider >3-5 mm as problematic
- Minimum usable data: ≥5 min for resting-state, task-dependent for task fMRI

### EEG Amplitude (Peak-to-Peak)

| Channel Type | Reject Threshold | Flat Threshold | Notes |
|--------------|-----------------|----------------|-------|
| EEG | 100-200 µV | 1 µV | Hardware-dependent |
| EOG | 200-250 µV | — | Blink detection |
| MEG (mag) | 3000-4000 fT | 1 fT | Magnetometers |
| MEG (grad) | 3000-4000 fT/cm | 1 fT/cm | Gradiometers |

**Additional EEG criteria:**
- Channel rejection: >20-30% bad epochs → mark as bad channel
- Epoch rejection: typically accept 10-30% epoch loss; >50% problematic
- Interpolation limit: ≤10% of channels can be interpolated

### Structural MRI

| Metric | Direction | Concern Level | Notes |
|--------|-----------|---------------|-------|
| CNR (GM/WM) | Higher better | <2.5 | Tissue contrast |
| SNR | Higher better | Site-dependent | Compare within-site |
| QI1 | Lower better | >0.1 | Artifact detection |
| EFC | Lower better | Outlier in distribution | Ghosting indicator |

## Modality-Specific References

For detailed metrics, thresholds, and Python code:

- **fMRI (fMRIPrep/MRIQC)**: See [references/fmri_qc.md](references/fmri_qc.md)
- **EEG/MEG (MNE-Python)**: See [references/eeg_qc.md](references/eeg_qc.md)
- **fNIRS (Homer3/MNE-NIRS)**: See [references/fnirs_qc.md](references/fnirs_qc.md)
- **Structural MRI**: See [references/structural_qc.md](references/structural_qc.md)

## Python Utilities

Scripts for parsing QC outputs and applying thresholds:

- `scripts/parse_mriqc.py`: Parse MRIQC group TSV, flag subjects
- `scripts/parse_fmriprep_confounds.py`: Summarize fMRIPrep confounds
- `scripts/qc_report.py`: Generate QC summary reports

## Methods Section Templates

### fMRI QC Methods
```
Quality control was performed using [MRIQC/fMRIPrep] outputs. Subjects were 
excluded based on the following criteria: (1) mean framewise displacement 
(FD) > X mm [cite Power et al., 2012], (2) >Y% of volumes exceeding FD 
threshold of Z mm, or (3) visual inspection revealing [registration 
failures/artifacts]. This resulted in N subjects excluded (X% of sample), 
yielding a final sample of M participants.
```

### EEG QC Methods
```
Continuous EEG data underwent artifact rejection using MNE-Python. Epochs 
containing peak-to-peak amplitudes exceeding X µV were rejected. Channels 
with >Y% rejected epochs were marked as bad and interpolated using spherical 
spline interpolation. Participants with >Z% rejected epochs or >N bad 
channels were excluded from analysis.
```

## Handling Unknown QC Outputs

When encountering unfamiliar QC metrics:

1. **Identify metric category**:
   - Motion/movement: Look for displacement, rotation, translation terms
   - Signal quality: SNR, tSNR, CNR, variance-related
   - Artifacts: Outlier counts, spike detection, artifact indices

2. **Determine directionality**:
   - Higher-is-better: SNR, tSNR, CNR
   - Lower-is-better: FD, DVARS, artifact indices, outlier counts

3. **Establish thresholds**:
   - Plot distribution, identify outliers
   - If metric has known analog, use those thresholds
   - Otherwise: use ±2-3 SD from mean as starting point

4. **Validate**:
   - Cross-reference with visual inspection
   - Check correlation with known metrics
   - Verify excluded subjects are actually problematic

## Population-Specific Considerations

### Infants (0-24 months)
- Higher baseline motion expected; adjust FD thresholds upward
- Shorter usable data segments acceptable
- Age-appropriate templates critical for registration QC
- Sleep state affects data quality (deep sleep preferred)

### Pediatric (3-12 years)
- Motion decreases with age; consider age as covariate
- Task compliance affects data quality
- Mock scanner training reduces motion
- Consider breaks during long protocols

### Adolescents
- Motion intermediate between children and adults
- Developmental stage affects hemodynamics
- Consider puberty stage as potential confound

### Clinical Populations
- Disease-specific considerations (lesions, atrophy)
- Medication effects on signal
- May need population-specific templates
- Balance data quality vs. already-reduced sample sizes

## Paradigm-Specific Considerations

### Resting-State
- Scrubbing viable (can remove timepoints)
- Need minimum continuous/total duration (≥5 min recommended)
- Strict motion thresholds (FD < 0.2-0.3 mm)

### Task fMRI
- Cannot arbitrarily remove timepoints
- Consider motion relative to task timing
- More lenient thresholds acceptable (FD < 0.5-0.9 mm)
- Ensure sufficient trials survive exclusion

### Naturalistic (movies, stories)
- Long durations increase motion likelihood
- Consider segment-wise QC
- Drift artifacts more relevant

### Sleep Studies
- State-dependent QC (arousal events)
- EEG quality for sleep staging
- Movement during state transitions
