# fNIRS QC Reference

Comprehensive guide for QC of functional near-infrared spectroscopy (fNIRS) data.

## Table of Contents
1. [Signal Quality Metrics](#signal-quality-metrics)
2. [Channel-Level QC](#channel-level-qc)
3. [Motion Artifact Detection](#motion-artifact-detection)
4. [Subject-Level Exclusion](#subject-level-exclusion)
5. [Population Considerations](#population-considerations)
6. [Python Examples](#python-examples)

## Signal Quality Metrics

### Scalp Coupling Index (SCI)

**Definition**: Measure of optode-scalp coupling quality based on cardiac pulsation detection.

**Interpretation:**
- Range: 0-1 (higher = better coupling)
- Threshold: SCI > 0.7-0.8 typically acceptable
- Based on correlation between wavelengths at cardiac frequency

**Calculation principle:**
- Good coupling → visible cardiac pulsation in signal
- Poor coupling → no cardiac signal, likely hair/poor contact

### Peak Spectral Power (PSP)

**Definition**: Power at cardiac frequency relative to total power.

**Interpretation:**
- Higher values indicate clear cardiac signal (good coupling)
- Low PSP suggests poor signal quality

### Coefficient of Variation (CV)

**Definition**: Standard deviation / mean of raw signal intensity.

**Interpretation:**
- Low CV (<10%): Stable signal
- High CV (>10-15%): Variable signal, potential motion/coupling issues

### Signal-to-Noise Ratio (SNR)

**Calculation:**
```
SNR = mean(signal) / std(noise)
```

**Interpretation:**
- Higher is better
- Compare across channels within subject

## Channel-Level QC

### Bad Channel Indicators

1. **Saturated signal**: Intensity at detector limit
2. **Zero/flat signal**: No light detected
3. **Excessive noise**: High variance unrelated to task
4. **Poor SCI**: SCI < 0.7
5. **Negative values**: After optical density conversion (physically impossible)

### Channel Rejection Criteria

| Metric | Reject Threshold | Notes |
|--------|-----------------|-------|
| SCI | < 0.7 | Coupling quality |
| CV | > 15% | Signal stability |
| Heart rate detectability | Not detected | Coupling validation |
| Negative OD values | Any | Data integrity |
| SNR | < sample mean - 2 SD | Relative quality |

### Maximum Acceptable Channel Loss

**Guidelines:**
- <20% of channels: Acceptable for most analyses
- 20-40%: Consider with caution, limit spatial inferences
- >40%: May need to exclude subject or use reduced channel set

## Motion Artifact Detection

### Motion Artifact Characteristics

- **Spikes**: Rapid, large amplitude changes
- **Baseline shifts**: Step changes in signal level
- **Slow drifts**: Gradual changes from optode movement

### Detection Methods

**1. Threshold-based:**
- Detect samples exceeding amplitude threshold
- Flag abrupt changes (derivative threshold)

**2. Moving window:**
- Calculate local statistics
- Flag windows with anomalous values

**3. Wavelet-based:**
- Decompose signal into frequency bands
- Identify motion-related components

### Correction Strategies

**1. Rejection:**
- Remove contaminated time segments
- Simple but loses data

**2. Spline interpolation:**
- Interpolate over short artifacts
- Preserves data length

**3. Wavelet filtering:**
- Remove motion-related wavelet components
- Preserves more data

**4. Principal Component Analysis (PCA):**
- Remove motion-related components
- Global artifact removal

**5. Targeted PCA / tPCA:**
- More targeted motion artifact removal

### Homer3 Motion Correction Functions

| Function | Description | Use Case |
|----------|-------------|----------|
| `hmrR_MotionArtifact` | Detect motion artifacts | Initial detection |
| `hmrR_MotionCorrectSpline` | Spline interpolation | Short artifacts |
| `hmrR_MotionCorrectWavelet` | Wavelet filtering | Broader correction |
| `hmrR_MotionCorrectPCArecurse` | Recursive PCA | Persistent artifacts |

## Subject-Level Exclusion

### Exclusion Criteria

**Quantitative:**
- >40% channels rejected
- >50% of data contaminated by motion
- Insufficient task trials after artifact rejection
- Technical failures (optode disconnection, recording errors)

**Qualitative:**
- Unable to achieve adequate optode placement (thick/dark hair)
- Persistent artifacts not correctable
- Subject non-compliance

### QC Checklist

```
□ Raw signal inspection (all channels)
□ Scalp coupling index check
□ Motion artifact detection
□ Channel pruning (bad channels removed)
□ Motion correction applied
□ Final signal quality assessment
□ Task-related segments verified
□ Hemodynamic response plausibility check
```

## Population Considerations

### Infants

**Unique considerations:**
- Different optode configurations (smaller head)
- More motion expected
- Hair less of an issue (less/finer hair)
- Different hemodynamic response characteristics

**Adjusted criteria:**
- More lenient motion thresholds
- Shorter usable segments acceptable
- Visual inspection critical

### Clinical Populations

**Considerations:**
- Altered hemodynamics (stroke, vascular disease)
- Medication effects
- Potential structural abnormalities affecting light propagation
- May have compliance challenges

## Python Examples (MNE-NIRS)

### Basic Signal Quality Check

```python
import mne
import mne_nirs
import numpy as np

def check_fnirs_quality(raw):
    """
    Basic fNIRS signal quality assessment.
    """
    # Get data
    data = raw.get_data()
    
    qc_results = {
        'n_channels': len(raw.ch_names),
        'duration_sec': raw.times[-1],
        'sfreq': raw.info['sfreq'],
    }
    
    # Calculate per-channel statistics
    channel_stats = []
    for i, ch_name in enumerate(raw.ch_names):
        ch_data = data[i, :]
        stats = {
            'channel': ch_name,
            'mean': np.mean(ch_data),
            'std': np.std(ch_data),
            'cv': np.std(ch_data) / np.abs(np.mean(ch_data)) * 100,
            'min': np.min(ch_data),
            'max': np.max(ch_data),
        }
        channel_stats.append(stats)
    
    qc_results['channel_stats'] = channel_stats
    
    return qc_results


def calculate_sci(raw, cardiac_freq_range=(0.5, 2.5)):
    """
    Calculate Scalp Coupling Index for fNIRS channels.
    
    SCI based on correlation between wavelengths at cardiac frequency.
    """
    from scipy import signal
    
    # This is a simplified SCI calculation
    # Full implementation would pair wavelengths by source-detector
    
    sfreq = raw.info['sfreq']
    data = raw.get_data()
    
    sci_values = []
    
    # For each channel, calculate cardiac power ratio
    for i in range(data.shape[0]):
        ch_data = data[i, :]
        
        # Calculate PSD
        freqs, psd = signal.welch(ch_data, fs=sfreq, nperseg=int(4*sfreq))
        
        # Find cardiac band
        cardiac_mask = (freqs >= cardiac_freq_range[0]) & (freqs <= cardiac_freq_range[1])
        
        if np.any(cardiac_mask):
            cardiac_power = np.max(psd[cardiac_mask])
            total_power = np.sum(psd)
            psp = cardiac_power / total_power
        else:
            psp = 0
        
        # SCI approximation (would need paired wavelengths for true SCI)
        sci_values.append(psp)
    
    return np.array(sci_values)
```

### Motion Artifact Detection

```python
def detect_motion_artifacts(raw, threshold_std=3.0, window_sec=1.0):
    """
    Detect motion artifacts using threshold-based method.
    """
    data = raw.get_data()
    sfreq = raw.info['sfreq']
    n_samples = data.shape[1]
    window_samples = int(window_sec * sfreq)
    
    # Calculate global signal variance
    global_std = np.std(data)
    threshold = threshold_std * global_std
    
    # Detect artifacts (samples where derivative exceeds threshold)
    diff_data = np.diff(data, axis=1)
    artifacts = np.zeros(n_samples, dtype=bool)
    
    for i in range(data.shape[0]):
        ch_artifacts = np.abs(diff_data[i, :]) > threshold
        # Expand to include surrounding samples
        for j in np.where(ch_artifacts)[0]:
            start = max(0, j - window_samples)
            end = min(n_samples, j + window_samples)
            artifacts[start:end] = True
    
    artifact_pct = 100 * np.sum(artifacts) / n_samples
    
    return artifacts, artifact_pct


def prune_bad_channels(raw, sci_threshold=0.7, cv_threshold=15):
    """
    Identify and mark bad channels based on quality metrics.
    """
    qc = check_fnirs_quality(raw)
    sci = calculate_sci(raw)
    
    bad_channels = []
    
    for i, stats in enumerate(qc['channel_stats']):
        ch_name = stats['channel']
        
        # Check CV
        if stats['cv'] > cv_threshold:
            bad_channels.append(ch_name)
            continue
        
        # Check SCI
        if sci[i] < sci_threshold:
            bad_channels.append(ch_name)
            continue
        
        # Check for negative values (if optical density)
        if stats['min'] < 0:
            bad_channels.append(ch_name)
    
    return bad_channels
```

### Complete QC Pipeline

```python
def fnirs_qc_pipeline(raw_path, output_dir=None):
    """
    Complete fNIRS QC pipeline.
    """
    import os
    
    # Load data
    raw = mne.io.read_raw_snirf(raw_path, preload=True)
    
    # Basic quality check
    qc_results = check_fnirs_quality(raw)
    
    # Calculate SCI
    sci_values = calculate_sci(raw)
    qc_results['sci_mean'] = np.mean(sci_values)
    qc_results['sci_min'] = np.min(sci_values)
    qc_results['n_low_sci'] = np.sum(sci_values < 0.7)
    
    # Detect motion artifacts
    artifacts, artifact_pct = detect_motion_artifacts(raw)
    qc_results['artifact_pct'] = artifact_pct
    
    # Identify bad channels
    bad_channels = prune_bad_channels(raw)
    qc_results['n_bad_channels'] = len(bad_channels)
    qc_results['bad_channels'] = bad_channels
    qc_results['bad_channel_pct'] = 100 * len(bad_channels) / qc_results['n_channels']
    
    # Determine inclusion
    include = True
    reasons = []
    
    if qc_results['bad_channel_pct'] > 40:
        include = False
        reasons.append(f"Bad channels: {qc_results['bad_channel_pct']:.1f}% > 40%")
    
    if qc_results['artifact_pct'] > 50:
        include = False
        reasons.append(f"Motion artifacts: {qc_results['artifact_pct']:.1f}% > 50%")
    
    qc_results['include'] = include
    qc_results['exclusion_reasons'] = reasons
    
    return qc_results
```

### QC Report Generation

```python
def generate_fnirs_report(qc_results, output_path):
    """Generate fNIRS QC report."""
    
    report = f"""
fNIRS Quality Control Report
============================

Recording Information
---------------------
Channels: {qc_results['n_channels']}
Duration: {qc_results['duration_sec']:.1f} seconds
Sampling rate: {qc_results['sfreq']} Hz

Signal Quality
--------------
Mean SCI: {qc_results.get('sci_mean', 'N/A'):.3f}
Min SCI: {qc_results.get('sci_min', 'N/A'):.3f}
Channels with low SCI: {qc_results.get('n_low_sci', 'N/A')}

Channel Quality
---------------
Bad channels: {qc_results['n_bad_channels']} ({qc_results['bad_channel_pct']:.1f}%)
Bad channel names: {', '.join(qc_results['bad_channels']) if qc_results['bad_channels'] else 'None'}

Motion Artifacts
----------------
Data affected by motion: {qc_results['artifact_pct']:.1f}%

Inclusion Decision
------------------
Include: {'Yes' if qc_results['include'] else 'No'}
"""
    
    if not qc_results['include']:
        report += f"Exclusion reasons:\n"
        for reason in qc_results['exclusion_reasons']:
            report += f"  - {reason}\n"
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
    
    return report
```

## Key References

- Pollonini L et al. (2014). Auditory cortex activation to natural speech and simulated cochlear implant speech measured with functional near-infrared spectroscopy. Hearing Research 309:84-93. (SCI metric)
- Hocke LM et al. (2018). Automated Processing of fNIRS Data—A Visual Guide to the Pitfalls and Consequences. Algorithms 11(5):67.
- Brigadoi S et al. (2014). Motion artifacts in functional near-infrared spectroscopy: A comparison of motion correction techniques applied to real cognitive data. NeuroImage 85:181-191.
- Yücel MA et al. (2021). Best practices for fNIRS publications. Neurophotonics 8(1):012101.
- Santosa H et al. (2018). The NIRS Brain AnalyzIR Toolbox. Algorithms 11(5):73.
