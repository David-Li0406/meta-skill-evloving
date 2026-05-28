---
name: neuropixels-analysis
description: Use this skill when analyzing Neuropixels neural recordings, including preprocessing, spike sorting, and quality metrics.
---

# Neuropixels Data Analysis

## Overview

Comprehensive toolkit for analyzing Neuropixels high-density neural recordings using best practices from SpikeInterface, Allen Institute, and International Brain Laboratory (IBL). Supports the full workflow from raw data to publication-ready curated units.

## When to Use This Skill

This skill should be used when:
- Working with Neuropixels recordings (.ap.bin, .lf.bin, .meta files)
- Loading data from SpikeGLX, Open Ephys, or NWB formats
- Preprocessing neural recordings (filtering, common average referencing, bad channel detection)
- Detecting and correcting motion/drift in recordings
- Running spike sorting (Kilosort4, SpykingCircus2, Mountainsort5)
- Computing quality metrics (SNR, ISI violations, presence ratio)
- Curating units using Allen/IBL criteria
- Creating visualizations of neural data
- Exporting results to Phy or NWB

## Supported Hardware & Formats

| Probe                     | Electrodes | Channels | Notes                           |
|---------------------------|------------|----------|---------------------------------|
| Neuropixels 1.0           | 960        | 384      | Requires phase_shift correction  |
| Neuropixels 2.0 (single)  | 1280       | 384      | Denser geometry                  |
| Neuropixels 2.0 (4-shank) | 5120       | 384      | Multi-region recording           |

| Format     | Extension                     | Reader                |
|------------|-------------------------------|-----------------------|
| SpikeGLX   | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()`  |
| Open Ephys | `.continuous`, `.oebin`       | `si.read_openephys()` |
| NWB        | `.nwb`                        | `si.read_nwb()`       |

## Quick Start

### Basic Import and Setup

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# Configure parallel processing
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### Loading Data

```python
# SpikeGLX (most common)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys (common for many labs)
recording = si.read_openephys('/path/to/Record_Node_101/')

# Check available streams
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']
```