---
name: matchms
description: Use this skill for spectral similarity and compound identification in metabolomics, particularly for comparing mass spectra, computing similarity scores, and identifying unknown compounds from spectral libraries.
---

# Matchms

## Overview

Matchms is an open-source Python library for mass spectrometry data processing and analysis. It allows users to import spectra from various formats, standardize metadata, filter peaks, calculate spectral similarities, and build reproducible analytical workflows.

## Core Capabilities

### 1. Importing and Exporting Mass Spectrometry Data

Load spectra from multiple file formats and export processed data:

```python
from matchms.importing import load_from_mgf, load_from_mzml, load_from_msp, load_from_json
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json

# Import spectra
spectra = list(load_from_mgf("spectra.mgf"))
spectra = list(load_from_mzml("data.mzML"))
spectra = list(load_from_msp("library.msp"))

# Export processed spectra
save_as_mgf(spectra, "output.mgf")
save_as_json(spectra, "output.json")
```

**Supported formats:**
- mzML and mzXML (raw mass spectrometry formats)
- MGF (Mascot Generic Format)
- MSP (spectral library format)
- JSON (GNPS-compatible)
- metabolomics-USI references
- Pickle (Python serialization)

### 2. Spectrum Filtering and Processing

Apply comprehensive filters to standardize metadata and refine peak data:

```python
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks

# Apply default metadata harmonization filters
spectrum = default_filters(spectrum)

# Normalize peak intensities
spectrum = normalize_intensities(spectrum)

# Filter peaks by relative intensity
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01, intensity_to=1.0)

# Require minimum peaks
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

**Filter categories:**
- **Metadata processing**: Harmonize compound names, derive chemical structures, standardize adducts, correct charges.
- **Peak filtering**: Normalize intensities, select by m/z or intensity, remove precursor ions.