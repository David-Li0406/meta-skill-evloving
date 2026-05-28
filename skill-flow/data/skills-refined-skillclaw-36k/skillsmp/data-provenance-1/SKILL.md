---
name: data-provenance
description: Track data lineage, ensure reproducibility, and maintain audit trails. Trigger when processing data, creating outputs, or needing to document analysis provenance. Ensures all analyses are reproducible and traceable.
---

# Data Provenance

Track data lineage, ensure reproducibility, and maintain audit trails for all analyses.

## Core Principles

1. **Input validation**: Verify inputs before processing
2. **Checksum tracking**: Record file checksums at each stage
3. **Parameter logging**: Document all analysis parameters
4. **Version control**: Track software and reference versions
5. **Output verification**: Validate outputs after processing

## Input Validation

### File Checksums

```python
import hashlib
from pathlib import Path
from datetime import datetime

def calculate_checksum(filepath: str, algorithm: str = "md5") -> str:
    """
    Calculate file checksum.

    Args:
        filepath: Path to file
        algorithm: Hash algorithm (md5, sha256)

    Returns:
        Hexadecimal checksum string
    """
    if algorithm == "md5":
        hasher = hashlib.md5()
    elif algorithm == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def validate_input_file(filepath: str, expected_checksum: str = None) -> dict:
    """
    Validate input file and record metadata.

    Returns:
        Dict with validation results and file metadata
    """
    path = Path(filepath)

    if not path.exists():
        return {
            "valid": False,
            "error": f"File not found: {filepath}",
        }

    # Calculate checksums
    md5 = calculate_checksum(filepath, "md5")

    result = {
        "valid": True,
        "filepath": str(path.absolute()),
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        "md5": md5,
        "validated_at": datetime.now().isoformat(),
    }

    # Verify against expected checksum
    if expected_checksum:
        if md5 != expected_checksum:
            result["valid"] = False
            result["error"] = f"Checksum mismatch: expected {expected_checksum}, got {md5}"

    return result
```

### Input Manifest

```python
import json

def create_input_manifest(input_files: list, output_path: str) -> dict:
    """
    Create manifest of all input files with checksums.

    Args:
        input_files: List of input file paths
        output_path: Path to write manifest

    Returns:
        Manifest dict
    """
    manifest = {
        "created": datetime.now().isoformat(),
        "files": [],
    }

    for filepath in input_files:
        file_info = validate_input_file(filepath)
        manifest["files"].append(file_info)

    # Check all valid
    manifest["all_valid"] = all(f["valid"] for f in manifest["files"])

    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest
```

## Analysis Provenance Record

### Provenance Template

```python
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any
import platform
import sys

@dataclass
class ProvenanceRecord:
    """Complete provenance record for an analysis."""

    # Analysis identification
    analysis_id: str
    analysis_type: str
    started: str = field(default_factory=lambda: datetime.now().isoformat())
    completed: str = None

    # Inputs
    input_files: List[Dict] = field(default_factory=list)

    # Parameters
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Software versions
    software_versions: Dict[str, str] = field(default_factory=dict)

    # Outputs
    output_files: List[Dict] = field(default_factory=list)

    # Environment
    environment: Dict[str, str] = field(default_factory=dict)

    # Status
    status: str = "running"
    error: str = None

    def __post_init__(self):
        """Capture environment on creation."""
        self.environment = {
            "platform": platform.platform(),
            "python_version": sys.version,
            "hostname": platform.node(),
            "user": os.environ.get("USER", "unknown"),
        }

    def add_input(self, filepath: str, expected_checksum: str = None):
        """Add and validate input file."""
        validation = validate_input_file(filepath, expected_checksum)
        self.input_files.append(validation)

    def add_output(self, filepath: str):
        """Add output file with checksum."""
        if Path(filepath).exists():
            output_info = validate_input_file(filepath)  # Same validation
            output_info["created_at"] = datetime.now().isoformat()
            self.output_files.append(output_info)

    def set_software_version(self, name: str, version: str):
        """Record software version."""
        self.software_versions[name] = version

    def complete(self, status: str = "success", error: str = None):
        """Mark analysis as complete."""
        self.completed = datetime.now().isoformat()
        self.status = status
        self.error = error

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def save(self, filepath: str):
        """Save provenance record to JSON."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "ProvenanceRecord":
        """Load provenance record from JSON."""
        with open(filepath) as f:
            data = json.load(f)
        return cls(**data)
```

### Usage Example

```python
import biometal
import os

def run_analysis_with_provenance(
    input_path: str,
    output_path: str,
    parameters: dict,
) -> ProvenanceRecord:
    """
    Run analysis with full provenance tracking.
    """
    # Create provenance record
    provenance = ProvenanceRecord(
        analysis_id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        analysis_type="fastq_qc",
        parameters=parameters,
    )

    # Record software versions
    provenance.set_software_version("biometal", biometal.__version__)
    provenance.set_software_version("python", sys.version.split()[0])

    # Validate input
    provenance.add_input(input_path)

    if not all(f["valid"] for f in provenance.input_files):
        provenance.complete("failed", "Input validation failed")
        return provenance

    try:
        # Run analysis
        stats = run_fastq_qc(input_path, output_path, **parameters)

        # Record output
        provenance.add_output(output_path)

        # Success
        provenance.complete("success")

    except Exception as e:
        provenance.complete("failed", str(e))

    return provenance
```

## Reproducibility Tracking

### Analysis Manifest

```python
def create_analysis_manifest(
    analysis_dir: str,
    description: str,
) -> dict:
    """
    Create manifest for complete analysis directory.

    Includes all files with checksums for reproducibility.
    """
    analysis_path = Path(analysis_dir)
    manifest = {
        "description": description,
        "created": datetime.now().isoformat(),
        "root_directory": str(analysis_path.absolute()),
        "files": [],
    }

    # Recursively catalog all files
    for filepath in analysis_path.rglob("*"):
        if filepath.is_file():
            rel_path = filepath.relative_to(analysis_path)
            file_info = {
                "path": str(rel_path),
                "size_bytes": filepath.stat().st_size,
                "md5": calculate_checksum(str(filepath)),
            }
            manifest["files"].append(file_info)

    manifest["total_files"] = len(manifest["files"])
    manifest["total_size_bytes"] = sum(f["size_bytes"] for f in manifest["files"])

    return manifest
```

### Reproducibility Verification

```python
def verify_reproducibility(
    manifest_path: str,
    analysis_dir: str,
) -> dict:
    """
    Verify analysis directory matches manifest.

    Returns:
        Dict with verification results
    """
    with open(manifest_path) as f:
        manifest = json.load(f)

    analysis_path = Path(analysis_dir)
    results = {
        "verified": True,
        "manifest_files": len(manifest["files"]),
        "missing_files": [],
        "modified_files": [],
        "extra_files": [],
    }

    manifest_files = {f["path"]: f for f in manifest["files"]}

    # Check each file in manifest
    for rel_path, expected in manifest_files.items():
        filepath = analysis_path / rel_path

        if not filepath.exists():
            results["missing_files"].append(rel_path)
            results["verified"] = False
        else:
            actual_md5 = calculate_checksum(str(filepath))
            if actual_md5 != expected["md5"]:
                results["modified_files"].append({
                    "path": rel_path,
                    "expected_md5": expected["md5"],
                    "actual_md5": actual_md5,
                })
                results["verified"] = False

    # Check for extra files
    current_files = set(
        str(p.relative_to(analysis_path))
        for p in analysis_path.rglob("*")
        if p.is_file()
    )
    expected_files = set(manifest_files.keys())
    results["extra_files"] = list(current_files - expected_files)

    return results
```

## Audit Trail

### Audit Log

```python
import logging

class AuditLogger:
    """Audit logger for tracking all analysis operations."""

    def __init__(self, log_path: str):
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s\t%(levelname)s\t%(message)s"
        ))
        self.logger.addHandler(handler)

    def log_input(self, filepath: str, checksum: str):
        """Log input file access."""
        self.logger.info(f"INPUT\t{filepath}\t{checksum}")

    def log_output(self, filepath: str, checksum: str):
        """Log output file creation."""
        self.logger.info(f"OUTPUT\t{filepath}\t{checksum}")

    def log_parameter(self, name: str, value: Any):
        """Log analysis parameter."""
        self.logger.info(f"PARAM\t{name}\t{value}")

    def log_event(self, event: str, details: str = ""):
        """Log analysis event."""
        self.logger.info(f"EVENT\t{event}\t{details}")

    def log_error(self, error: str):
        """Log error."""
        self.logger.error(f"ERROR\t{error}")
```

## Best Practices

1. **Always validate inputs** before processing
2. **Record checksums** for all inputs and outputs
3. **Log all parameters** used in analysis
4. **Track software versions** including dependencies
5. **Save provenance records** alongside outputs
6. **Create manifests** for complete analyses
7. **Verify reproducibility** periodically

## Integration with Pipelines

```python
def pipeline_with_provenance(
    sample_id: str,
    input_path: str,
    output_dir: str,
) -> ProvenanceRecord:
    """
    Complete pipeline with provenance tracking.
    """
    # Initialize
    provenance = ProvenanceRecord(
        analysis_id=f"{sample_id}_{datetime.now().strftime('%Y%m%d')}",
        analysis_type="full_pipeline",
    )
    audit = AuditLogger(f"{output_dir}/{sample_id}_audit.log")

    # Track input
    provenance.add_input(input_path)
    audit.log_input(input_path, provenance.input_files[-1]["md5"])

    # Run pipeline steps...
    # (Each step logs to audit trail)

    # Save provenance
    provenance_path = f"{output_dir}/{sample_id}_provenance.json"
    provenance.save(provenance_path)

    return provenance
```
