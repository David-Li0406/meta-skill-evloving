---
name: lab-reporting
description: Standard reporting formats and output generation for the lab. Trigger when creating reports, generating summaries, or formatting analysis outputs. Ensures consistent, professional deliverables. CUSTOMIZE THIS SKILL with your lab's report templates.
---

# Lab Reporting

**TEMPLATE SKILL**: Customize with your lab's standard report formats.

This skill provides templates for consistent analysis reports.

## Report Types

### 1. QC Summary Report

Standard format for QC results:

```python
from datetime import datetime
from pathlib import Path
import json

def generate_qc_summary_report(
    sample_results: dict,
    output_path: str,
    report_title: str = "Quality Control Summary",
) -> None:
    """
    Generate QC summary report.

    Args:
        sample_results: Dict of {sample_id: qc_results}
        output_path: Output file path (.tsv or .json)
    """
    # Calculate summary statistics
    n_samples = len(sample_results)
    n_passed = sum(1 for r in sample_results.values()
                   if r.get("qc_decision", {}).get("passed", False))
    pass_rate = n_passed / n_samples if n_samples > 0 else 0

    report = {
        "title": report_title,
        "generated": datetime.now().isoformat(),
        "summary": {
            "total_samples": n_samples,
            "passed_qc": n_passed,
            "failed_qc": n_samples - n_passed,
            "pass_rate": f"{pass_rate:.1%}",
        },
        "samples": {},
    }

    # Per-sample details
    for sample_id, results in sample_results.items():
        decision = results.get("qc_decision", {})
        report["samples"][sample_id] = {
            "status": "PASS" if decision.get("passed", False) else "FAIL",
            "reasons": decision.get("reasons", []),
            "warnings": decision.get("warnings", []),
            "metrics": {
                "total_reads": results.get("total_reads", "N/A"),
                "pass_rate": f"{results.get('pass_rate', 0):.1%}",
                "mean_quality": f"{results.get('mean_quality', 0):.1f}",
            },
        }

    # Write report
    output_path = Path(output_path)
    if output_path.suffix == ".json":
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
    else:
        write_tsv_report(report, output_path)
```

### 2. Analysis Summary TSV

Standard tabular output:

```python
def write_analysis_summary_tsv(
    results: dict,
    output_path: str,
    columns: list = None,
) -> None:
    """
    Write analysis results as TSV.

    Standard columns:
    - sample_id
    - qc_status
    - total_reads
    - mapped_reads
    - mapping_rate
    - mean_quality
    - mean_coverage
    - notes
    """
    if columns is None:
        columns = [
            "sample_id", "qc_status", "total_reads", "mapped_reads",
            "mapping_rate", "mean_quality", "mean_coverage", "notes"
        ]

    with open(output_path, "w") as f:
        # Header
        f.write("\t".join(columns) + "\n")

        # Data rows
        for sample_id, data in results.items():
            row = []
            for col in columns:
                if col == "sample_id":
                    row.append(sample_id)
                elif col == "qc_status":
                    row.append("PASS" if data.get("qc_passed", False) else "FAIL")
                elif col == "mapping_rate":
                    rate = data.get("mapping_rate", 0)
                    row.append(f"{rate:.1%}")
                elif col in data:
                    value = data[col]
                    if isinstance(value, float):
                        row.append(f"{value:.2f}")
                    else:
                        row.append(str(value))
                else:
                    row.append("N/A")

            f.write("\t".join(row) + "\n")
```

### 3. Executive Summary

High-level summary for stakeholders:

```python
def generate_executive_summary(
    project_name: str,
    sample_results: dict,
    output_path: str,
) -> None:
    """
    Generate executive summary for project.

    Includes:
    - Project overview
    - Key findings
    - QC summary
    - Recommendations
    """
    n_samples = len(sample_results)
    n_passed = sum(1 for r in sample_results.values()
                   if r.get("qc_passed", False))

    # Aggregate metrics
    all_reads = [r.get("total_reads", 0) for r in sample_results.values()]
    all_quality = [r.get("mean_quality", 0) for r in sample_results.values()]

    summary = f"""# {project_name} - Executive Summary

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Overview

- **Total Samples**: {n_samples}
- **Passed QC**: {n_passed} ({100*n_passed/n_samples:.1f}%)
- **Failed QC**: {n_samples - n_passed}

## Key Metrics

| Metric | Min | Mean | Max |
|--------|-----|------|-----|
| Total Reads | {min(all_reads):,} | {sum(all_reads)/len(all_reads):,.0f} | {max(all_reads):,} |
| Mean Quality | {min(all_quality):.1f} | {sum(all_quality)/len(all_quality):.1f} | {max(all_quality):.1f} |

## Recommendations

"""

    # Add recommendations based on results
    if n_passed < n_samples:
        failed = [s for s, r in sample_results.items() if not r.get("qc_passed", False)]
        summary += f"- **{len(failed)} samples failed QC**: {', '.join(failed[:5])}"
        if len(failed) > 5:
            summary += f" (and {len(failed)-5} more)"
        summary += "\n"
        summary += "- Consider re-sequencing failed samples or adjusting analysis parameters\n"

    if sum(all_quality)/len(all_quality) < 25:
        summary += "- **Quality below typical threshold**: Consider more stringent filtering\n"

    if not summary.endswith("\n\n"):
        summary += "\n## Next Steps\n\n"
        summary += "1. Review failed samples\n"
        summary += "2. Proceed with downstream analysis on passed samples\n"
        summary += "3. Archive raw data\n"

    with open(output_path, "w") as f:
        f.write(summary)
```

## Standard Output Columns

### FASTQ QC Report

```python
FASTQ_QC_COLUMNS = [
    ("sample_id", "Sample ID"),
    ("total_reads", "Total Reads"),
    ("total_bases", "Total Bases (bp)"),
    ("mean_length", "Mean Length (bp)"),
    ("mean_quality", "Mean Quality (Phred)"),
    ("mean_gc", "Mean GC (%)"),
    ("q20_rate", "Q20 Rate (%)"),
    ("qc_status", "QC Status"),
]
```

### Alignment Report

```python
ALIGNMENT_COLUMNS = [
    ("sample_id", "Sample ID"),
    ("total_reads", "Total Reads"),
    ("mapped_reads", "Mapped Reads"),
    ("mapping_rate", "Mapping Rate (%)"),
    ("mean_mapq", "Mean MAPQ"),
    ("duplicate_rate", "Duplicate Rate (%)"),
    ("mean_coverage", "Mean Coverage (x)"),
    ("qc_status", "QC Status"),
]
```

### Variant Summary

```python
VARIANT_COLUMNS = [
    ("sample_id", "Sample ID"),
    ("total_variants", "Total Variants"),
    ("snps", "SNPs"),
    ("indels", "Indels"),
    ("ts_tv_ratio", "Ts/Tv Ratio"),
    ("pass_rate", "PASS Rate (%)"),
    ("qc_status", "QC Status"),
]
```

## Report Generation Utilities

### Timestamp Formatting

```python
def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for reports."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_date(dt: datetime = None) -> str:
    """Format date for filenames."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y%m%d")
```

### Number Formatting

```python
def format_number(value, decimals: int = 2) -> str:
    """Format number with appropriate precision."""
    if value is None:
        return "N/A"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        if value < 0.01:
            return f"{value:.2e}"
        return f"{value:,.{decimals}f}"
    return str(value)

def format_percentage(value, decimals: int = 1) -> str:
    """Format as percentage."""
    if value is None:
        return "N/A"
    return f"{100*value:.{decimals}f}%"
```

### Report Naming

```python
def generate_report_filename(
    project: str,
    report_type: str,
    extension: str = "tsv",
) -> str:
    """Generate standardized report filename."""
    date = format_date()
    return f"{date}_{project}_{report_type}.{extension}"

# Examples:
# 20260126_HMP2_qc_summary.tsv
# 20260126_HMP2_alignment_report.json
# 20260126_HMP2_executive_summary.md
```

## Complete Report Pipeline

```python
def generate_all_reports(
    project_name: str,
    sample_results: dict,
    output_dir: str,
) -> dict:
    """
    Generate all standard reports for a project.

    Returns dict of report paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    date = format_date()

    reports = {}

    # TSV summary
    tsv_path = output_dir / f"{date}_{project_name}_summary.tsv"
    write_analysis_summary_tsv(sample_results, str(tsv_path))
    reports["tsv_summary"] = str(tsv_path)

    # JSON report
    json_path = output_dir / f"{date}_{project_name}_report.json"
    generate_qc_summary_report(sample_results, str(json_path))
    reports["json_report"] = str(json_path)

    # Executive summary
    exec_path = output_dir / f"{date}_{project_name}_executive_summary.md"
    generate_executive_summary(project_name, sample_results, str(exec_path))
    reports["executive_summary"] = str(exec_path)

    print(f"Generated {len(reports)} reports in {output_dir}")
    return reports
```

## Customization

1. **Add logo/branding**: Modify HTML/PDF templates
2. **Custom columns**: Adjust column lists per report type
3. **New report types**: Add functions following existing patterns
4. **Output formats**: Add PDF, HTML, or other formats as needed
