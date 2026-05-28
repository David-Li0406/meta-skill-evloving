# fMRI QC Reference

Comprehensive guide for QC of functional MRI data from fMRIPrep, MRIQC, and related pipelines.

## Table of Contents
1. [Motion Metrics](#motion-metrics)
2. [Signal Quality Metrics](#signal-quality-metrics)
3. [MRIQC IQMs](#mriqc-iqms)
4. [fMRIPrep Confounds](#fmriprep-confounds)
5. [Threshold Recommendations](#threshold-recommendations)
6. [Python Examples](#python-examples)

## Motion Metrics

### Framewise Displacement (FD)

**Definition**: Sum of absolute translations and rotations between consecutive volumes, with rotations converted to mm using 50mm sphere radius (Power et al., 2012).

```
FD_t = |Δd_x| + |Δd_y| + |Δd_z| + |Δα| + |Δβ| + |Δγ|
```

**Key metrics from pipelines:**
- `fd_mean`: Mean FD across all volumes
- `fd_max`: Maximum single-volume FD
- `fd_num`: Number of volumes exceeding threshold (MRIQC uses 0.2mm)
- `fd_perc`: Percentage of volumes exceeding threshold

**Threshold recommendations by population and paradigm:**

| Context | Conservative | Standard | Lenient | Reference |
|---------|-------------|----------|---------|-----------|
| Adult resting-state | 0.2 mm | 0.3 mm | 0.5 mm | Power et al., 2014 |
| Adult task | 0.5 mm | 0.9 mm | 1.0 mm | Siegel et al., 2014 |
| Pediatric (6-12y) | 0.25 mm | 0.3 mm | 0.4 mm | Satterthwaite et al., 2012 |
| Infant (sleep) | 0.2 mm | 0.5 mm | — | Smyser et al., 2010 |
| Infant (awake) | 0.3 mm | 0.5 mm | — | Ellis et al., 2020 |

**Subject exclusion criteria:**
- Mean FD > threshold (see table above)
- >20-50% of volumes exceed threshold (fd_perc)
- <5 minutes of usable data after scrubbing (resting-state)
- Insufficient trials remaining (task fMRI)

### DVARS (Derivative of Variance)

**Definition**: Root mean square of temporal derivative of BOLD signal across brain voxels. Indexes frame-to-frame signal intensity changes.

```
DVARS_t = sqrt(mean((S_t - S_{t-1})^2))
```

**Interpretation:**
- Spikes indicate rapid signal changes (often motion-related)
- Correlates with FD but captures signal-level artifacts
- Standardized DVARS (stdDVARS) normalized to baseline variance

**Thresholds:**
- Raw DVARS: Site/scanner dependent
- Standardized DVARS > 1.5: Potential artifact
- Used in conjunction with FD for volume censoring

## Signal Quality Metrics

### Temporal SNR (tSNR)

**Definition**: Mean BOLD signal divided by temporal standard deviation.

```
tSNR = mean(S_t) / std(S_t)
```

**Interpretation:**
- Higher is better
- Typical adult values: 40-100 (varies with sequence, field strength)
- Lower in infants/neonates
- Affected by motion, physiological noise, hardware

**Population norms (approximate, 3T):**
- Adults: 50-80 (cortex average)
- Children: 40-70
- Infants: 30-60

**No absolute cutoff** — compare within your sample, flag outliers >2 SD below mean.

### Global Signal Correlation

**Metrics:**
- `gsr_x`, `gsr_y`: Ghost-to-signal ratio along phase-encoding axes
- `gcor`: Global correlation (mean correlation of all voxels)

**Interpretation:**
- High gcor may indicate excessive global signal / physiological noise
- GSR artifacts indicate gradient/reconstruction issues

## MRIQC IQMs

### BOLD IQMs (Complete List)

| Metric | Description | Direction | Notes |
|--------|-------------|-----------|-------|
| `aor` | AFNI outlier ratio | Lower better | Fraction of outlier voxels |
| `aqi` | AFNI quality index | Lower better | Mean outlier ratio |
| `dvars_std` | Standardized DVARS mean | Lower better | ~1.0 is baseline |
| `dvars_vstd` | Voxelwise std DVARS | Lower better | Variability in DVARS |
| `dvars_nstd` | Non-standardized DVARS | Lower better | Raw DVARS mean |
| `efc` | Entropy focus criterion | Lower better | Image ghosting |
| `fber` | Foreground-background energy ratio | Higher better | Signal clarity |
| `fd_mean` | Mean framewise displacement | Lower better | Overall motion |
| `fd_num` | # volumes with FD > 0.2mm | Lower better | High-motion volumes |
| `fd_perc` | % volumes with FD > 0.2mm | Lower better | Motion proportion |
| `fwhm_avg` | Average smoothness (mm) | Context | Spatial smoothness |
| `gcor` | Global correlation | Lower better | Global signal |
| `gsr_x`, `gsr_y` | Ghost-to-signal ratio | Lower better | Nyquist ghosting |
| `size_t` | Number of volumes | Context | Scan length |
| `size_x/y/z` | Matrix dimensions | Context | Acquisition params |
| `snr` | Signal-to-noise ratio | Higher better | Image quality |
| `spacing_tr` | Repetition time | Context | Acquisition params |
| `summary_*_mean/std` | Tissue signal stats | Context | Per-tissue metrics |
| `tsnr` | Temporal SNR | Higher better | Key quality metric |

### Prioritized Metrics for Exclusion

**Primary (always check):**
1. `fd_mean` — motion summary
2. `fd_perc` — motion distribution
3. `tsnr` — signal quality

**Secondary (for outlier detection):**
4. `dvars_std` — signal stability
5. `aor` — outlier volumes
6. `efc` — ghosting artifacts

## fMRIPrep Confounds

### Key Confound Columns

From `*_desc-confounds_timeseries.tsv`:

**Motion parameters:**
- `trans_x`, `trans_y`, `trans_z`: Translation (mm)
- `rot_x`, `rot_y`, `rot_z`: Rotation (radians)
- `*_derivative1`: First derivatives
- `*_power2`: Squared terms

**Composite motion:**
- `framewise_displacement`: FD per volume
- `rmsd`: Root mean squared deviation from reference

**Signal regressors:**
- `dvars`: DVARS per volume
- `std_dvars`: Standardized DVARS
- `global_signal`: Whole-brain mean
- `csf`, `white_matter`: Tissue signals

**Outlier detection:**
- `motion_outlier_*`: Binary columns for censoring
- `non_steady_state_*`: Initial volumes to exclude

### Calculating Summary Statistics

```python
import pandas as pd
import numpy as np

def summarize_confounds(confounds_path, fd_thresh=0.5):
    """Summarize fMRIPrep confounds for QC."""
    df = pd.read_csv(confounds_path, sep='\t')
    
    fd = df['framewise_displacement'].values
    fd = fd[~np.isnan(fd)]  # First volume is NaN
    
    return {
        'fd_mean': np.mean(fd),
        'fd_max': np.max(fd),
        'fd_perc': 100 * np.sum(fd > fd_thresh) / len(fd),
        'n_volumes': len(df),
        'n_high_motion': np.sum(fd > fd_thresh),
        'dvars_mean': df['std_dvars'].mean(),
    }
```

## Threshold Recommendations

### Resting-State fMRI (Adults)

**Conservative (high-quality connectivity):**
- fd_mean < 0.2 mm
- fd_perc < 20%
- Minimum 5 min after scrubbing
- tsnr > sample mean - 2 SD

**Standard:**
- fd_mean < 0.3 mm
- fd_perc < 30%
- Minimum 4 min after scrubbing

**Lenient (preserve sample size):**
- fd_mean < 0.5 mm
- fd_perc < 50%

### Task fMRI (Adults)

**Standard:**
- fd_mean < 0.9 mm (Siegel et al., 2014)
- fd_max < 3-5 mm
- >80% of task trials usable

**Per-run exclusion:**
- Exclude run if >20% frames censored

### Developmental Populations

**Infants (0-12 months):**
- fd_mean < 0.5 mm (more lenient than adults)
- Accept shorter usable segments (2-3 min)
- Visual QC critical for registration

**Children (6-12 years):**
- fd_mean < 0.3-0.4 mm
- Consider age as covariate in group comparisons
- fd_perc < 30%

## Python Examples

### Parse MRIQC Group Output

```python
import pandas as pd
import numpy as np

def load_mriqc_bold(group_tsv_path):
    """Load MRIQC group BOLD TSV."""
    df = pd.read_csv(group_tsv_path, sep='\t')
    return df

def flag_subjects(df, fd_mean_thresh=0.3, fd_perc_thresh=30, tsnr_zscore=-2):
    """Flag subjects for exclusion based on QC metrics."""
    flags = pd.DataFrame(index=df.index)
    
    # Motion flags
    flags['high_fd_mean'] = df['fd_mean'] > fd_mean_thresh
    flags['high_fd_perc'] = df['fd_perc'] > fd_perc_thresh
    
    # tSNR flag (z-score based)
    tsnr_z = (df['tsnr'] - df['tsnr'].mean()) / df['tsnr'].std()
    flags['low_tsnr'] = tsnr_z < tsnr_zscore
    
    # Composite flag
    flags['exclude'] = flags.any(axis=1)
    
    # Merge with subject IDs
    result = df[['bids_name']].copy()
    result = pd.concat([result, flags], axis=1)
    
    return result

def generate_qc_report(df, flags):
    """Generate QC summary report."""
    n_total = len(df)
    n_exclude = flags['exclude'].sum()
    
    report = f"""
    QC Summary Report
    =================
    Total subjects: {n_total}
    Excluded: {n_exclude} ({100*n_exclude/n_total:.1f}%)
    
    Exclusion breakdown:
    - High mean FD: {flags['high_fd_mean'].sum()}
    - High FD percentage: {flags['high_fd_perc'].sum()}
    - Low tSNR: {flags['low_tsnr'].sum()}
    
    Included subjects: {n_total - n_exclude}
    """
    return report
```

### Visualize QC Distributions

```python
import matplotlib.pyplot as plt

def plot_qc_distributions(df, output_path=None):
    """Plot QC metric distributions with threshold lines."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # FD mean
    ax = axes[0, 0]
    ax.hist(df['fd_mean'], bins=30, edgecolor='black')
    ax.axvline(0.3, color='orange', linestyle='--', label='Standard (0.3mm)')
    ax.axvline(0.5, color='red', linestyle='--', label='Lenient (0.5mm)')
    ax.set_xlabel('Mean FD (mm)')
    ax.set_ylabel('Count')
    ax.set_title('Framewise Displacement')
    ax.legend()
    
    # FD percentage
    ax = axes[0, 1]
    ax.hist(df['fd_perc'], bins=30, edgecolor='black')
    ax.axvline(20, color='orange', linestyle='--', label='20%')
    ax.axvline(50, color='red', linestyle='--', label='50%')
    ax.set_xlabel('% Volumes > 0.2mm')
    ax.set_ylabel('Count')
    ax.set_title('High-Motion Volume Percentage')
    ax.legend()
    
    # tSNR
    ax = axes[1, 0]
    ax.hist(df['tsnr'], bins=30, edgecolor='black')
    mean_tsnr = df['tsnr'].mean()
    std_tsnr = df['tsnr'].std()
    ax.axvline(mean_tsnr - 2*std_tsnr, color='red', linestyle='--', 
               label=f'-2 SD ({mean_tsnr - 2*std_tsnr:.1f})')
    ax.set_xlabel('tSNR')
    ax.set_ylabel('Count')
    ax.set_title('Temporal SNR')
    ax.legend()
    
    # DVARS
    ax = axes[1, 1]
    ax.hist(df['dvars_std'], bins=30, edgecolor='black')
    ax.axvline(1.5, color='red', linestyle='--', label='1.5 (elevated)')
    ax.set_xlabel('Standardized DVARS')
    ax.set_ylabel('Count')
    ax.set_title('DVARS')
    ax.legend()
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig
```

## Key References

- Power JD et al. (2012). Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion. NeuroImage 59(3):2142-2154. doi:10.1016/j.neuroimage.2011.10.018
- Power JD et al. (2014). Methods to detect, characterize, and remove motion artifact in resting state fMRI. NeuroImage 84:320-341. doi:10.1016/j.neuroimage.2013.08.048
- Satterthwaite TD et al. (2012). Impact of in-scanner head motion on multiple measures of functional connectivity. NeuroImage 60(1):623-632.
- Siegel JS et al. (2014). Statistical improvements in functional magnetic resonance imaging analyses produced by censoring high-motion data points. Human Brain Mapping 35(5):1981-1996.
- Esteban O et al. (2017). MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites. PLOS ONE 12(9):e0184661.
