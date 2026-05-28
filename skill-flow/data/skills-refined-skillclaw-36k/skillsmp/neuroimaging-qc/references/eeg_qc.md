# EEG/MEG QC Reference

Comprehensive guide for QC of EEG and MEG data, primarily using MNE-Python.

## Table of Contents
1. [Channel-Level QC](#channel-level-qc)
2. [Epoch-Level QC](#epoch-level-qc)
3. [Artifact Detection](#artifact-detection)
4. [Subject-Level Exclusion](#subject-level-exclusion)
5. [Population Considerations](#population-considerations)
6. [Python Examples](#python-examples)

## Channel-Level QC

### Bad Channel Detection

**Indicators of bad channels:**
- Flat/dead channels (no signal variance)
- Noisy channels (excessive high-frequency activity)
- Channels with persistent artifacts
- Disconnected/bridged electrodes

**Detection strategies:**

1. **Amplitude-based**: Channels with abnormal variance
2. **Correlation-based**: Channels poorly correlated with neighbors
3. **Spectral-based**: Abnormal power spectrum shape
4. **Visual inspection**: Always recommended as final check

**MNE-Python thresholds (peak-to-peak):**

| Channel Type | Reject (Max PTP) | Flat (Min PTP) | Notes |
|--------------|-----------------|----------------|-------|
| EEG | 100-200 µV | 1 µV | Hardware-dependent |
| EOG | 200-250 µV | — | Blink detection |
| ECG | 5 mV | — | Heartbeat detection |
| MEG (magnetometer) | 3000-4000 fT | 1 fT | |
| MEG (gradiometer) | 3000-4000 fT/cm | 1 fT/cm | |

### Interpolation Guidelines

- **Maximum interpolatable channels**: 10% of total (e.g., ≤6 for 64-channel system)
- **Avoid interpolating**: Reference electrode neighbors, critical ROI channels
- **Method**: Spherical spline interpolation (MNE default)
- **Document**: Always report number and location of interpolated channels

## Epoch-Level QC

### Rejection Thresholds

**Standard EEG thresholds:**
```python
reject = dict(
    eeg=100e-6,    # 100 µV - conservative
    # eeg=150e-6,  # 150 µV - standard
    # eeg=200e-6,  # 200 µV - lenient
    eog=200e-6     # 200 µV for EOG
)

flat = dict(
    eeg=1e-6       # 1 µV minimum
)
```

**MEG thresholds:**
```python
reject = dict(
    mag=4000e-15,  # 4000 fT
    grad=4000e-13, # 4000 fT/cm
    eog=200e-6
)

flat = dict(
    mag=1e-15,     # 1 fT
    grad=1e-13     # 1 fT/cm
)
```

### Acceptable Epoch Loss

| Context | Acceptable Loss | Concern Level |
|---------|-----------------|---------------|
| High-trial designs (>200 per condition) | <30% | >40% |
| Standard designs (50-100 per condition) | <20% | >30% |
| Low-trial designs (<50 per condition) | <10% | >20% |

**Minimum trials for reliable ERPs:**
- Simple components (P1, N1): ~30-40 trials
- Later components (P300, N400): ~20-30 trials
- Complex conditions: varies by effect size

## Artifact Detection

### EOG (Eye Movement) Artifacts

**Types:**
- Blinks: Large amplitude, frontal distribution
- Saccades: Horizontal eye movements

**Detection (MNE):**
```python
# Find EOG events
eog_events = mne.preprocessing.find_eog_events(raw)

# Create EOG epochs for inspection/ICA
eog_epochs = mne.preprocessing.create_eog_epochs(raw)
```

**Handling strategies:**
1. **Rejection**: Remove contaminated epochs (simple, loses data)
2. **ICA**: Remove EOG components (preserves more data)
3. **Regression**: Regress out EOG signal (SSP projections)

### ECG (Cardiac) Artifacts

**More prominent in MEG than EEG.**

```python
ecg_events = mne.preprocessing.find_ecg_events(raw)
ecg_epochs = mne.preprocessing.create_ecg_epochs(raw)
```

### Muscle Artifacts

**Characteristics:**
- High frequency (>20 Hz)
- Often temporal/neck electrodes
- Common during jaw clenching, swallowing

**Detection:**
- High-frequency power increase
- ICA component inspection

### Line Noise (50/60 Hz)

**Handling:**
```python
# Notch filter
raw_filtered = raw.notch_filter(freqs=[60, 120, 180])  # 60 Hz and harmonics

# Or use spectral interpolation for narrow-band removal
```

## Subject-Level Exclusion

### Exclusion Criteria

**Quantitative:**
- >50% epochs rejected
- >10% channels interpolated
- Insufficient trials per condition (<minimum for analysis)
- Technical failures (disconnected electrodes, recording errors)

**Qualitative (requires visual inspection):**
- Persistent artifacts not removable by ICA
- Unusual waveform morphology suggesting hardware issues
- Excessive drowsiness/sleep (for wake studies)

### QC Checklist

```
□ Raw data visual inspection (scrolling)
□ Power spectrum check (line noise, muscle)
□ Bad channel identification and interpolation
□ Artifact detection (EOG, ECG)
□ ICA component inspection (if used)
□ Epoch rejection summary
□ Final epoch count per condition
□ ERP/ERF waveform check
```

## Population Considerations

### Infants

**Unique challenges:**
- More movement artifacts
- Different reference electrode considerations
- Shorter attention spans → fewer trials
- Different frequency characteristics

**Adjusted thresholds:**
```python
# More lenient for infant EEG
reject_infant = dict(
    eeg=200e-6,  # 200 µV (vs 100-150 for adults)
)
```

**Minimum trials (infant ERPs):**
- May need only 10-20 good trials for robust components
- Consider trial-by-trial analysis approaches

### Clinical Populations

**Considerations:**
- Pathological activity may look like artifacts
- Medication effects on EEG
- May have reduced compliance / more movement
- Adjust thresholds based on population characteristics

### High-Density EEG (64+ channels)

- Can be more aggressive with channel interpolation
- ICA more effective with more channels
- Consider spatial filtering approaches

## Python Examples

### Complete QC Pipeline

```python
import mne
import numpy as np

def run_eeg_qc(raw_path, events_path=None, event_id=None):
    """
    Complete EEG QC pipeline.
    
    Returns dict with QC metrics and processed data.
    """
    # Load data
    raw = mne.io.read_raw_fif(raw_path, preload=True)
    
    # 1. Filter
    raw.filter(l_freq=0.1, h_freq=40)
    raw.notch_filter(freqs=[60])
    
    # 2. Find bad channels by variance
    data = raw.get_data(picks='eeg')
    variance = np.var(data, axis=1)
    z_var = (variance - np.mean(variance)) / np.std(variance)
    bad_by_var = np.where(np.abs(z_var) > 3)[0]
    
    # 3. Mark bad channels
    eeg_names = raw.ch_names
    bad_channels = [eeg_names[i] for i in bad_by_var if eeg_names[i].startswith('EEG')]
    raw.info['bads'].extend(bad_channels)
    
    # 4. Interpolate bad channels
    if len(raw.info['bads']) > 0:
        raw.interpolate_bads(reset_bads=True)
    
    # 5. Re-reference (average reference)
    raw.set_eeg_reference('average')
    
    # 6. Create epochs (if events provided)
    qc_results = {
        'n_bad_channels': len(bad_channels),
        'bad_channels': bad_channels,
        'n_total_channels': len([ch for ch in raw.ch_names if ch.startswith('EEG')]),
    }
    
    if events_path and event_id:
        events = mne.read_events(events_path)
        
        reject = dict(eeg=150e-6)
        flat = dict(eeg=1e-6)
        
        epochs = mne.Epochs(
            raw, events, event_id,
            tmin=-0.2, tmax=0.8,
            reject=reject, flat=flat,
            preload=True
        )
        
        # Calculate epoch stats
        n_total = len(events)
        n_dropped = n_total - len(epochs)
        
        qc_results.update({
            'n_epochs_total': n_total,
            'n_epochs_dropped': n_dropped,
            'epoch_rejection_rate': 100 * n_dropped / n_total,
            'epochs_per_condition': {k: len(epochs[k]) for k in event_id.keys()},
        })
        
        return qc_results, raw, epochs
    
    return qc_results, raw, None


def check_subject_inclusion(qc_results, 
                           max_bad_channels_pct=10,
                           max_epoch_rejection_pct=30,
                           min_epochs_per_cond=30):
    """
    Check if subject meets inclusion criteria.
    """
    include = True
    reasons = []
    
    # Check bad channels
    bad_pct = 100 * qc_results['n_bad_channels'] / qc_results['n_total_channels']
    if bad_pct > max_bad_channels_pct:
        include = False
        reasons.append(f"Bad channels: {bad_pct:.1f}% > {max_bad_channels_pct}%")
    
    # Check epoch rejection
    if 'epoch_rejection_rate' in qc_results:
        if qc_results['epoch_rejection_rate'] > max_epoch_rejection_pct:
            include = False
            reasons.append(f"Epoch rejection: {qc_results['epoch_rejection_rate']:.1f}% > {max_epoch_rejection_pct}%")
        
        # Check epochs per condition
        for cond, n in qc_results['epochs_per_condition'].items():
            if n < min_epochs_per_cond:
                include = False
                reasons.append(f"Insufficient epochs for {cond}: {n} < {min_epochs_per_cond}")
    
    return include, reasons
```

### ICA-Based Artifact Removal

```python
def run_ica_artifact_removal(raw, n_components=15):
    """
    ICA-based artifact removal for EOG and ECG.
    """
    from mne.preprocessing import ICA
    
    # Fit ICA
    ica = ICA(n_components=n_components, random_state=42)
    ica.fit(raw)
    
    # Find EOG-related components
    eog_indices, eog_scores = ica.find_bads_eog(raw)
    
    # Find ECG-related components (if ECG channel available)
    try:
        ecg_indices, ecg_scores = ica.find_bads_ecg(raw)
    except:
        ecg_indices = []
    
    # Mark components for exclusion
    ica.exclude = list(set(eog_indices + ecg_indices))
    
    # Apply ICA
    raw_clean = ica.apply(raw.copy())
    
    return raw_clean, ica, {
        'n_eog_components': len(eog_indices),
        'n_ecg_components': len(ecg_indices),
        'eog_indices': eog_indices,
        'ecg_indices': ecg_indices,
    }
```

### Generate QC Report

```python
def generate_eeg_qc_report(qc_results, output_path):
    """Generate text QC report."""
    
    report = f"""
EEG Quality Control Report
==========================

Channel Quality
---------------
Total EEG channels: {qc_results['n_total_channels']}
Bad channels identified: {qc_results['n_bad_channels']}
Bad channel rate: {100 * qc_results['n_bad_channels'] / qc_results['n_total_channels']:.1f}%
Bad channel names: {', '.join(qc_results['bad_channels']) if qc_results['bad_channels'] else 'None'}
"""
    
    if 'n_epochs_total' in qc_results:
        report += f"""
Epoch Quality
-------------
Total epochs: {qc_results['n_epochs_total']}
Rejected epochs: {qc_results['n_epochs_dropped']}
Rejection rate: {qc_results['epoch_rejection_rate']:.1f}%

Epochs per condition:
"""
        for cond, n in qc_results['epochs_per_condition'].items():
            report += f"  {cond}: {n}\n"
    
    if 'n_eog_components' in qc_results:
        report += f"""
ICA Artifact Removal
--------------------
EOG components removed: {qc_results['n_eog_components']}
ECG components removed: {qc_results['n_ecg_components']}
"""
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    return report
```

## Key References

- Jas M et al. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. NeuroImage 159:417-429.
- Gramfort A et al. (2013). MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267.
- Delorme A & Makeig S. (2004). EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics. Journal of Neuroscience Methods 134(1):9-21.
- Luck SJ. (2014). An Introduction to the Event-Related Potential Technique. MIT Press.
