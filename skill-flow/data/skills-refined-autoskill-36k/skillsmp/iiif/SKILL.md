---
name: iiif
description: Work with IIIF manifests and the Wellcome Collection API. Use this skill to download manifests, extract metadata, or process canvases. Invoke with /iiif.
---

# IIIF Manifest Processing

This skill helps work with IIIF (International Image Interoperability Framework) manifests from the Wellcome Collection.

## Overview

The Wellcome Collection provides digitized works via IIIF Presentation API. Each work has a manifest containing:
- Metadata (title, contributors, subjects)
- Sequences of canvases (pages)
- Image URLs and dimensions
- Text renderings (OCR text URLs)

## CLI Commands

The `iiif_manifests.py` module provides Click-based CLI commands:

### Download Manifests
```bash
# Download first 1000 manifests
python -m wc_simd.iiif_manifests download-manifests --limit 1000

# Download all manifests
python -m wc_simd.iiif_manifests download-manifests
```

### Create Hive Tables
```bash
python -m wc_simd.iiif_manifests create-tables
```

### Process Specific Work
```bash
python -m wc_simd.iiif_manifests process-work --work-id abc123
```

## API Endpoints

### Works API
```
https://api.wellcomecollection.org/catalogue/v2/works
https://api.wellcomecollection.org/catalogue/v2/works/{id}
```

### IIIF Presentation API
```
https://iiif.wellcomecollection.org/presentation/v3/{id}
```

### Image API
```
https://iiif.wellcomecollection.org/image/{image_id}/full/max/0/default.jpg
```

## Python Usage

```python
from wc_simd.iiif_manifests import (
    fetch_manifest,
    extract_canvases,
    get_text_rendering_url
)

# Fetch a manifest
manifest = fetch_manifest("abc123")

# Extract canvas metadata
canvases = extract_canvases(manifest)

# Get OCR text URL
text_url = get_text_rendering_url(manifest)
```

## Content Advisory Authentication

Some images require authentication due to content advisory. Handle with session cookies:

```python
import requests

session = requests.Session()
# Accept content advisory
session.get("https://wellcomecollection.org/works/{id}?acceptContentAdvisory=true")
# Now fetch protected content
response = session.get(protected_url)
```

## Key Statistics

- **Total manifests**: ~340,000
- **Works with OCR text**: 226,145
- **Total pages**: ~42 million
- **Download failure rate**: 0.47%

## Hive Tables Created

| Table | Description |
|-------|-------------|
| `iiif_manifests` | Manifest metadata (id, label, attribution) |
| `iiif_canvases` | Canvas data (image URLs, dimensions, labels) |
| `alto_text` | OCR text extracted from text renderings |
