---
name: neurokit2
description: Use this skill when processing and analyzing physiological signals such as ECG, EEG, EDA, RSP, PPG, EMG, and EOG for applications in psychophysiology, clinical research, and human-computer interaction.
---

# Skill body

## Overview

NeuroKit2 is a comprehensive Python toolkit designed for processing and analyzing various physiological signals (biosignals). It is applicable in psychophysiology research, clinical applications, and human-computer interaction studies.

## When to Use This Skill

Apply this skill when working with:
- **Cardiac signals**: ECG, PPG, heart rate variability (HRV), pulse analysis
- **Brain signals**: EEG frequency bands, microstates, complexity, source localization
- **Autonomic signals**: Electrodermal activity (EDA/GSR), skin conductance responses (SCR)
- **Respiratory signals**: Breathing rate, respiratory variability (RRV), volume per time
- **Muscular signals**: EMG amplitude, muscle activation detection
- **Eye tracking**: EOG, blink detection and analysis
- **Multi-modal integration**: Processing multiple physiological signals simultaneously
- **Complexity analysis**: Entropy measures, fractal dimensions, nonlinear dynamics

## Core Capabilities

### 1. Cardiac Signal Processing (ECG/PPG)

Process electrocardiogram and photoplethysmography signals for cardiovascular analysis. 

**Primary workflows:**
- ECG processing pipeline: cleaning → R-peak detection → delineation → quality assessment
- HRV analysis across time, frequency, and nonlinear domains
- PPG pulse analysis and quality assessment
- ECG-derived respiration extraction

**Key functions:**
```python
import neurokit2 as nk

# Complete ECG processing pipeline
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Analyze ECG data (event-related or interval-related)
analysis = nk.ecg_analyze(signals, sampling_rate=1000)

# Comprehensive HRV analysis
hrv = nk.hrv(peaks, sampling_rate=1000)  # Time, frequency, nonlinear domains
```

### 2. Heart Rate Variability Analysis

Compute comprehensive HRV metrics from cardiac signals.