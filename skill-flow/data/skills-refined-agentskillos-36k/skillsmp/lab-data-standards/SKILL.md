---
name: lab-data-standards
description: Lab-specific data standards and naming conventions. Trigger when creating new files, organizing data, or naming samples/outputs. Enforces consistent naming schemes, directory structures, and metadata requirements. CUSTOMIZE THIS SKILL for your lab's specific conventions.
---

# Lab Data Standards

**TEMPLATE SKILL**: Customize this for your lab's specific conventions.

This skill enforces consistent data organization across all analyses.

## Sample ID Format

All sample identifiers MUST follow this pattern:

```
{PROJECT}_{SAMPLE}_{LANE}_{DATE}

Examples:
- HMP2_S001_L001_20260126
- MGEN_P042_L002_20260115
- VIRAL_CTL01_L001_20260120
```

### Validation

```python
import re

SAMPLE_ID_PATTERN = re.compile(
    r"^[A-Z0-9]+_[A-Z0-9]+_L\d{3}_\d{8}$"
)

def validate_sample_id(sample_id: str) -> bool:
    """Check if sample ID matches lab convention."""
    return bool(SAMPLE_ID_PATTERN.match(sample_id))

def parse_sample_id(sample_id: str) -> dict:
    """Parse sample ID into components."""
    if not validate_sample_id(sample_id):
        raise ValueError(f"Invalid sample ID format: {sample_id}")

    parts = sample_id.split("_")
    return {
        "project": parts[0],
        "sample": parts[1],
        "lane": parts[2],
        "date": parts[3],
    }
```

## Directory Structure

Standard project layout:

```
project_name/
├── raw_data/              # Original sequencing files (NEVER modify)
│   ├── fastq/
│   └── checksums.md5
├── processed/             # Filtered/trimmed data
│   ├── filtered/
│   └── qc_reports/
├── analysis/              # Analysis outputs
│   ├── alignment/
│   ├── variants/
│   ├── diversity/
│   └── figures/
├── metadata/              # Sample information
│   ├── sample_manifest.tsv
│   └── sequencing_info.tsv
├── scripts/               # Analysis code
│   ├── 01_qc.py
│   ├── 02_align.py
│   └── ...
├── results/               # Final deliverables
│   └── YYYY-MM-DD_report/
└── README.md              # Project description
```

### Path Generation

```python
from pathlib import Path

def get_project_paths(project_root: str, sample_id: str) -> dict:
    """Generate standard paths for a sample."""
    root = Path(project_root)
    parsed = parse_sample_id(sample_id)

    return {
        "raw_fastq": root / "raw_data" / "fastq" / f"{sample_id}.fq.gz",
        "filtered_fastq": root / "processed" / "filtered" / f"{sample_id}.filtered.fq.gz",
        "qc_report": root / "processed" / "qc_reports" / f"{sample_id}_qc.json",
        "alignment": root / "analysis" / "alignment" / f"{sample_id}.bam",
        "variants": root / "analysis" / "variants" / f"{sample_id}.vcf.gz",
    }
```

## File Naming Conventions

### Input Files

| Type | Pattern | Example |
|------|---------|---------|
| Raw FASTQ | `{SAMPLE_ID}.fq.gz` | `HMP2_S001_L001_20260126.fq.gz` |
| Raw FASTQ R1/R2 | `{SAMPLE_ID}_R1.fq.gz` | `HMP2_S001_L001_20260126_R1.fq.gz` |
| Reference | `{GENOME}_{VERSION}.fa` | `hg38_GRCh38.fa` |

### Output Files

| Type | Pattern | Example |
|------|---------|---------|
| Filtered FASTQ | `{SAMPLE_ID}.filtered.fq.gz` | `HMP2_S001_L001_20260126.filtered.fq.gz` |
| BAM | `{SAMPLE_ID}.{ALIGNER}.bam` | `HMP2_S001_L001_20260126.bwa.bam` |
| VCF | `{SAMPLE_ID}.{CALLER}.vcf.gz` | `HMP2_S001_L001_20260126.gatk.vcf.gz` |
| QC JSON | `{SAMPLE_ID}_qc.json` | `HMP2_S001_L001_20260126_qc.json` |
| Report | `{DATE}_{PROJECT}_report.html` | `20260126_HMP2_report.html` |

## Metadata Requirements

### Sample Manifest (required columns)

```
sample_id       # Unique identifier (must match naming convention)
fastq_path      # Path to raw FASTQ file
group           # Experimental group (control/treatment/etc.)
subject_id      # Subject/patient identifier
timepoint       # Collection timepoint
```

### Optional Metadata

```
sequencing_date     # Date of sequencing
instrument          # Sequencing platform
library_prep        # Library preparation method
read_length         # Expected read length
notes               # Additional notes
```

### Validation

```python
REQUIRED_METADATA_COLUMNS = [
    "sample_id",
    "fastq_path",
    "group",
    "subject_id",
    "timepoint",
]

def validate_manifest(manifest_path: str) -> list:
    """Validate sample manifest format and content."""
    import csv

    errors = []

    with open(manifest_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        columns = reader.fieldnames or []

        # Check required columns
        for col in REQUIRED_METADATA_COLUMNS:
            if col not in columns:
                errors.append(f"Missing required column: {col}")

        # Check each row
        for i, row in enumerate(reader, start=2):
            # Validate sample ID
            if not validate_sample_id(row.get("sample_id", "")):
                errors.append(f"Row {i}: Invalid sample_id format")

            # Check file exists
            fastq_path = row.get("fastq_path", "")
            if fastq_path and not Path(fastq_path).exists():
                errors.append(f"Row {i}: FASTQ file not found: {fastq_path}")

    return errors
```

## Checksum Requirements

All raw data must have MD5 checksums:

```python
import hashlib

def calculate_md5(filepath: str, chunk_size: int = 8192) -> str:
    """Calculate MD5 checksum for file."""
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()

def verify_checksums(checksum_file: str) -> list:
    """Verify all files against checksums."""
    errors = []

    with open(checksum_file) as f:
        for line in f:
            expected_md5, filepath = line.strip().split("  ")
            actual_md5 = calculate_md5(filepath)

            if actual_md5 != expected_md5:
                errors.append(f"Checksum mismatch: {filepath}")

    return errors
```

## Customization

**TO CUSTOMIZE FOR YOUR LAB:**

1. Update `SAMPLE_ID_PATTERN` regex for your naming convention
2. Modify `REQUIRED_METADATA_COLUMNS` for your needs
3. Adjust directory structure for your workflow
4. Add any lab-specific validation rules

This skill ensures consistency across all lab members and projects.
