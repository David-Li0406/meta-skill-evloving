# Structural MRI QC Reference

Comprehensive guide for QC of structural MRI data (T1w, T2w) from MRIQC, FreeSurfer, and related pipelines.

## Table of Contents
1. [MRIQC Anatomical IQMs](#mriqc-anatomical-iqms)
2. [FreeSurfer QC](#freesurfer-qc)
3. [Registration QC](#registration-qc)
4. [Segmentation QC](#segmentation-qc)
5. [Population Considerations](#population-considerations)
6. [Python Examples](#python-examples)

## MRIQC Anatomical IQMs

### Complete T1w/T2w IQM List

| Metric | Description | Direction | Typical Range |
|--------|-------------|-----------|---------------|
| **Noise Metrics** ||||
| `snr_csf` | SNR in CSF | Higher better | 5-15 |
| `snr_gm` | SNR in gray matter | Higher better | 8-20 |
| `snr_wm` | SNR in white matter | Higher better | 10-25 |
| `snr_total` | Total SNR | Higher better | Varies |
| `cnr` | Contrast-to-noise ratio (GM/WM) | Higher better | >2.5 |
| **Information Metrics** ||||
| `cjv` | Coefficient of joint variation | Lower better | <0.5 |
| `efc` | Entropy focus criterion | Lower better | <0.6 |
| `fber` | Foreground-background energy ratio | Higher better | >100 |
| **Artifact Metrics** ||||
| `qi_1` | Artifact detection (Mortamet) | Lower better | <0.05 |
| `qi_2` | Artifact detection (extended) | Lower better | <0.05 |
| `inu_med` | INU bias median | ~1.0 | 0.9-1.1 |
| `inu_range` | INU bias range | Lower better | <0.3 |
| `wm2max` | WM to max intensity ratio | ~0.5-0.8 | Site-dependent |
| **Resolution/Size** ||||
| `fwhm_avg` | Average smoothness (mm) | Context | 2-4mm |
| `fwhm_x/y/z` | Directional smoothness | Context | |
| `size_x/y/z` | Matrix dimensions | Context | |
| `spacing_x/y/z` | Voxel dimensions | Context | |
| **Tissue Stats** ||||
| `summary_*_mean` | Mean intensity per tissue | Context | |
| `summary_*_stdv` | Stdv intensity per tissue | Context | |
| `summary_*_p05/p95` | 5th/95th percentiles | Context | |
| `tpm_overlap_*` | TPM overlap per tissue | Higher better | >0.7 |
| `icvs_*` | Intracranial volume fractions | Context | |

### Key Metrics for Exclusion Decisions

**Primary (always check):**
1. `qi_1` — artifact detection
2. `cnr` — tissue contrast quality
3. `snr_gm` / `snr_wm` — signal quality
4. `cjv` — GM/WM separability

**Secondary:**
5. `efc` — ghosting/ringing
6. `inu_range` — bias field severity
7. `fwhm_avg` — effective resolution

### Threshold Recommendations

**Note**: Absolute thresholds don't generalize well across sites/scanners. Use distribution-based outlier detection.

**General guidelines:**
- `qi_1` > 0.1: Potential artifacts
- `cnr` < 2.5: Poor tissue contrast
- `cjv` > 0.5: Poor GM/WM separation
- `efc` > 0.6: Possible ghosting

**Recommended approach:**
```python
# Flag outliers beyond 2-3 SD from sample mean
for metric in ['qi_1', 'cnr', 'cjv', 'efc']:
    z_score = (value - sample_mean) / sample_std
    if abs(z_score) > 3:
        flag_for_review(subject)
```

## FreeSurfer QC

### Automated QC Metrics

**Euler number:**
- Topological measure of surface quality
- More negative = more holes/handles (worse)
- Threshold: Euler < -200 flagged for review (Rosen et al., 2018)

**Surface holes:**
- Count of topological defects
- Threshold: >100 holes concerning

**Estimated total intracranial volume (eTIV):**
- Should be within expected range for population
- Flag outliers (>2 SD from mean)

### Visual QC Checkpoints

**1. Skull stripping:**
```
□ Brain fully included
□ No skull/dura remaining
□ No brain tissue removed
```

**2. White matter segmentation:**
```
□ WM follows gyral pattern
□ No WM in ventricles
□ No holes in WM
```

**3. Pial surface:**
```
□ Follows gray matter boundary
□ No extension into skull/dura
□ No cuts into brain tissue
```

**4. Subcortical segmentation:**
```
□ Symmetric structures similar size
□ No obvious mislabeling
□ Hippocampus properly delineated
```

### Common FreeSurfer Issues

| Issue | Visual Sign | Potential Cause |
|-------|-------------|-----------------|
| Skull stripping failure | Brain cut off or skull included | Low contrast, unusual anatomy |
| WM segmentation error | WM extends into GM | Motion blur, bias field |
| Pial surface error | Surface extends into skull | Dura enhancement, blood vessels |
| Subcortical mislabel | Asymmetric volumes | Poor contrast, pathology |

### FreeSurfer QC Tools

```bash
# View segmentation overlaid on T1
freeview -v $SUBJECTS_DIR/$subj/mri/T1.mgz \
         -v $SUBJECTS_DIR/$subj/mri/aseg.mgz:colormap=lut

# View surfaces
freeview -v $SUBJECTS_DIR/$subj/mri/T1.mgz \
         -f $SUBJECTS_DIR/$subj/surf/lh.white:edgecolor=yellow \
         -f $SUBJECTS_DIR/$subj/surf/lh.pial:edgecolor=red
```

## Registration QC

### Checking Normalization Quality

**Metrics:**
- Cost function value (mutual information, correlation ratio)
- Overlap with template (Dice, Jaccard)
- Landmark alignment

**Visual checks:**
```
□ Major structures aligned (ventricles, sulci)
□ No gross misalignment
□ Edges match template
□ Subcortical structures properly positioned
```

### Common Registration Failures

1. **Local minima**: Registration stuck in wrong position
2. **Scaling errors**: Brain too large/small
3. **Rotation errors**: Tilted relative to template
4. **Shearing**: Non-rigid distortion

### Template Considerations

**Adults:**
- MNI152 (most common)
- Colin27
- fsaverage (surface)

**Pediatric:**
- Pediatric templates (e.g., NIH Pediatric MRI Database)
- Age-specific templates

**Infants:**
- UNC infant templates
- MCRIB
- dHCP templates (Developing Human Connectome Project)

## Segmentation QC

### Tissue Segmentation Checks

**CSF:**
- Present in ventricles and sulci
- Not extending into parenchyma

**Gray matter:**
- Follows cortical ribbon
- Proper thickness (~2-4mm in adults)

**White matter:**
- Connected through centrum semiovale
- Follows expected pattern

### Volume Plausibility

**Adult brain volumes (approximate):**
| Structure | Typical Volume | Flag if... |
|-----------|---------------|------------|
| Total brain | 1200-1500 cm³ | <1000 or >1700 |
| Cerebral WM | 400-600 cm³ | Outlier |
| Cortical GM | 550-750 cm³ | Outlier |
| Hippocampus (each) | 3-4 cm³ | <2 or >5 |
| Lateral ventricle (each) | 7-20 cm³ | >40 (unless elderly) |

**Note**: Volumes vary with age, sex, and pathology.

## Population Considerations

### Infants

**Challenges:**
- Inverted T1 contrast (myelination incomplete)
- Rapidly changing brain size
- Different templates needed

**QC considerations:**
- Use age-appropriate templates
- Expect different metric distributions
- Visual QC more critical

### Elderly

**Considerations:**
- Atrophy affects volumes and segmentation
- WM hyperintensities affect contrast
- Enlarged ventricles normal

**Adjusted criteria:**
- Larger acceptable ventricle volumes
- Lower GM volumes expected
- Check for WMH handling

### Clinical Populations

**Considerations:**
- Lesions may affect segmentation
- Atrophy patterns disease-specific
- May need lesion masking

## Python Examples

### Parse MRIQC Anatomical Output

```python
import pandas as pd
import numpy as np

def load_mriqc_anat(group_tsv_path):
    """Load MRIQC T1w group TSV."""
    df = pd.read_csv(group_tsv_path, sep='\t')
    return df


def flag_anat_outliers(df, zscore_threshold=3):
    """
    Flag subjects with outlier anatomical IQMs.
    """
    metrics_to_check = ['qi_1', 'cnr', 'cjv', 'efc', 'snr_gm', 'snr_wm']
    
    # Direction: higher is worse for these
    higher_worse = ['qi_1', 'cjv', 'efc']
    # Direction: lower is worse for these
    lower_worse = ['cnr', 'snr_gm', 'snr_wm']
    
    flags = pd.DataFrame(index=df.index)
    
    for metric in metrics_to_check:
        if metric not in df.columns:
            continue
        
        z = (df[metric] - df[metric].mean()) / df[metric].std()
        
        if metric in higher_worse:
            flags[f'outlier_{metric}'] = z > zscore_threshold
        else:  # lower_worse
            flags[f'outlier_{metric}'] = z < -zscore_threshold
    
    flags['any_outlier'] = flags.any(axis=1)
    
    return flags


def anat_qc_report(df, flags):
    """Generate anatomical QC summary."""
    n_total = len(df)
    n_outliers = flags['any_outlier'].sum()
    
    report = f"""
Anatomical MRI QC Summary
=========================

Total subjects: {n_total}
Outliers detected: {n_outliers} ({100*n_outliers/n_total:.1f}%)

Metric distributions:
"""
    
    for col in ['qi_1', 'cnr', 'cjv', 'snr_gm']:
        if col in df.columns:
            report += f"\n{col}:\n"
            report += f"  Mean: {df[col].mean():.3f}\n"
            report += f"  Std:  {df[col].std():.3f}\n"
            report += f"  Range: [{df[col].min():.3f}, {df[col].max():.3f}]\n"
    
    return report
```

### FreeSurfer QC Extraction

```python
import os
import subprocess

def get_euler_number(subjects_dir, subject):
    """Extract Euler number from FreeSurfer output."""
    euler_lh = None
    euler_rh = None
    
    # Read from log file or compute
    log_file = os.path.join(subjects_dir, subject, 'scripts', 'recon-all.log')
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                if 'euler' in line.lower():
                    # Parse euler number from log
                    pass
    
    # Alternative: compute directly
    for hemi in ['lh', 'rh']:
        surf_path = os.path.join(subjects_dir, subject, 'surf', f'{hemi}.orig')
        if os.path.exists(surf_path):
            result = subprocess.run(
                ['mris_euler_number', surf_path],
                capture_output=True, text=True
            )
            # Parse output
    
    return euler_lh, euler_rh


def get_fs_volumes(subjects_dir, subject):
    """Extract key volumes from FreeSurfer stats."""
    stats_file = os.path.join(subjects_dir, subject, 'stats', 'aseg.stats')
    
    volumes = {}
    
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.strip().split()
                if len(parts) >= 4:
                    struct_name = parts[4] if len(parts) > 4 else parts[0]
                    volume = float(parts[3])
                    volumes[struct_name] = volume
    
    return volumes


def check_fs_qc(subjects_dir, subject):
    """Comprehensive FreeSurfer QC check."""
    qc_results = {
        'subject': subject,
        'passed': True,
        'issues': []
    }
    
    # Check if recon-all completed
    done_file = os.path.join(subjects_dir, subject, 'scripts', 'recon-all.done')
    if not os.path.exists(done_file):
        qc_results['passed'] = False
        qc_results['issues'].append('recon-all did not complete')
        return qc_results
    
    # Check Euler numbers
    euler_lh, euler_rh = get_euler_number(subjects_dir, subject)
    if euler_lh is not None and euler_lh < -200:
        qc_results['issues'].append(f'Low Euler LH: {euler_lh}')
    if euler_rh is not None and euler_rh < -200:
        qc_results['issues'].append(f'Low Euler RH: {euler_rh}')
    
    # Check volumes
    volumes = get_fs_volumes(subjects_dir, subject)
    
    # Example: check for extreme hippocampal volumes
    for hemi in ['Left', 'Right']:
        hipp_key = f'{hemi}-Hippocampus'
        if hipp_key in volumes:
            vol = volumes[hipp_key]
            if vol < 2000 or vol > 5500:  # in mm³
                qc_results['issues'].append(f'Unusual {hemi} hippocampus: {vol:.0f} mm³')
    
    if qc_results['issues']:
        qc_results['passed'] = False
    
    return qc_results
```

### Visual QC Screenshot Generation

```python
def generate_qc_screenshots(subjects_dir, subject, output_dir):
    """Generate QC screenshots using FreeSurfer tools."""
    import subprocess
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Axial slices with segmentation overlay
    for slice_num in [80, 100, 120, 140]:
        output_file = os.path.join(output_dir, f'{subject}_axial_{slice_num}.png')
        cmd = [
            'freeview',
            '-v', f'{subjects_dir}/{subject}/mri/T1.mgz',
            '-v', f'{subjects_dir}/{subject}/mri/aseg.mgz:colormap=lut:opacity=0.3',
            '-slice', '0', '0', str(slice_num),
            '-viewport', 'axial',
            '-ss', output_file,
            '-quit'
        ]
        subprocess.run(cmd)
    
    # Surface views
    for hemi in ['lh', 'rh']:
        for view in ['lateral', 'medial']:
            output_file = os.path.join(output_dir, f'{subject}_{hemi}_{view}.png')
            cmd = [
                'freeview',
                '-f', f'{subjects_dir}/{subject}/surf/{hemi}.pial:overlay={subjects_dir}/{subject}/surf/{hemi}.thickness',
                '-viewport', '3d',
                '-cam', 'azimuth', '0' if view == 'lateral' else '180',
                '-ss', output_file,
                '-quit'
            ]
            subprocess.run(cmd)
```

## Key References

- Esteban O et al. (2017). MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites. PLOS ONE 12(9):e0184661.
- Rosen AFG et al. (2018). Quantitative assessment of structural image quality. NeuroImage 169:407-418.
- Fischl B. (2012). FreeSurfer. NeuroImage 62(2):774-781.
- Klapwijk ET et al. (2019). Qoala-T: A supervised-learning tool for quality control of FreeSurfer segmented MRI data. NeuroImage 189:116-129.
