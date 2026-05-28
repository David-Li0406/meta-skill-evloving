---
name: pydicom
description: Use this skill when working with DICOM (Digital Imaging and Communications in Medicine) files for reading, writing, or modifying medical imaging data, extracting pixel data, anonymizing files, and handling metadata.
---

# Pydicom

## Overview

Pydicom is a pure Python package for working with DICOM files, the standard format for medical imaging data. This skill provides guidance on reading, writing, and manipulating DICOM files, including working with pixel data, metadata, and various compression formats.

## When to Use This Skill

Use this skill when working with:
- Medical imaging files (CT, MRI, X-ray, ultrasound, PET, etc.)
- DICOM datasets requiring metadata extraction or modification
- Pixel data extraction and image processing from medical scans
- DICOM anonymization for research or data sharing
- Converting DICOM files to standard image formats
- Compressed DICOM data requiring decompression
- DICOM sequences and structured reports
- Multi-slice volume reconstruction
- PACS (Picture Archiving and Communication System) integration

## Installation

Install pydicom and common dependencies:

```bash
pip install pydicom
pip install pillow  # For image format conversion
pip install numpy   # For pixel array manipulation
pip install matplotlib  # For visualization
```

For handling compressed DICOM files, additional packages may be needed:

```bash
pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg  # JPEG compression
pip install python-gdcm  # Alternative compression handler
```

## Core Workflows

### Reading DICOM Files

Read a DICOM file using `pydicom.dcmread()`:

```python
import pydicom

# Read a DICOM file
ds = pydicom.dcmread('path/to/file.dcm')

# Access metadata
print(f"Patient Name: {ds.PatientName}")
print(f"Study Date: {ds.StudyDate}")
print(f"Modality: {ds.Modality}")

# Display all elements
print(ds)
```

**Key points:**
- `dcmread()` returns a `Dataset` object.
- Access data elements using attribute notation (e.g., `ds.PatientName`) or tag notation (e.g., `ds[0x0010, 0x0010]`).
- Use `ds.file_meta` to access file metadata like Transfer Syntax UID.