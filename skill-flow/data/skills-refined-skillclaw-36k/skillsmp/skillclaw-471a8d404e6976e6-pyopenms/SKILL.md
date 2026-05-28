---
name: pyopenms
description: Use this skill when you need to perform mass spectrometry analysis for proteomics and metabolomics, including feature detection, peptide identification, and protein quantification.
---

# PyOpenMS

## Overview

PyOpenMS provides Python bindings to the OpenMS library for computational mass spectrometry, enabling analysis of proteomics and metabolomics data. Use it for handling mass spectrometry file formats, processing spectral data, detecting features, identifying peptides/proteins, and performing quantitative analysis.

## Installation

Install using uv:

```bash
uv uv pip install pyopenms
```

Verify installation:

```python
import pyopenms
print(pyopenms.__version__)
```

## Core Capabilities

PyOpenMS organizes functionality into these domains:

### 1. File I/O and Data Formats

Handle mass spectrometry file formats and convert between representations.

**Supported formats**: mzML, mzXML, TraML, mzTab, FASTA, pepXML, protXML, mzIdentML, featureXML, consensusXML, idXML

Basic file reading:

```python
import pyopenms as ms

# Read mzML file
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Access spectra
for spectrum in exp:
    mz, intensity = spectrum.get_peaks()
    print(f"Spectrum: {len(mz)} peaks")
```

### 2. Signal Processing

Process raw spectral data with smoothing, filtering, centroiding, and normalization.

Basic spectrum processing:

```python
# Smooth spectrum with Gaussian filter
gaussian = ms.GaussFilter()
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.1)
gaussian.setParameters(params)
gaussian.filterExperiment(exp)
```

### 3. Feature Detection

Detect and link features across spectra and samples for quantitative analysis.

```python
# Detect features
ff = ms.FeatureFinder()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

### 4. Peptide and Protein Identification

Integrate with search engines and process identification results.

**Supported engines**: Comet, Mascot, MSGFPlus, XTandem, OMSSA, Myrimatch

Basic identification workflow:

```python
# Example code for peptide identification
```