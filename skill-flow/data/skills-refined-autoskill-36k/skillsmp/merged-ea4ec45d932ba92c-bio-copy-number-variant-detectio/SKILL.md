---
name: bio-copy-number-variant-detection
description: Use this skill for detecting copy number variants (CNVs) from targeted or exome sequencing data using CNVkit, supporting various analysis types including tumor-normal pairs and germline calling.
---

# CNV Detection Workflow

This skill provides a comprehensive workflow for detecting copy number variants (CNVs) from sequencing data, utilizing CNVkit for analysis, visualization, and annotation.

## Workflow Overview

```
BAM files (tumor/normal or germline)
    |
    v
[1. Target Preparation] --> Create/access target BED
    |
    v
[2. Coverage Calculation] --> Read depth per target
    |
    v
[3. Reference Creation] --> Pool of normals or flat reference
    |
    v
[4. CNV Calling] --------> Log2 ratios, segmentation
    |
    v
[5. Visualization] ------> Scatter plots, heatmaps
    |
    v
[6. Annotation] ---------> Gene-level CNVs
    |
    v
CNV calls with gene annotations
```

## Primary Tool: CNVkit

### Step 1: Prepare Target Regions

```bash
# Generate target and antitarget regions
cnvkit.py target <targets.bed> --annotate <refFlat.txt> --split -o <output_targets.bed>
cnvkit.py access <genome.fa> -o <output_access.bed>
cnvkit.py antitarget <output_targets.bed> --access <output_access.bed> -o <output_antitargets.bed>
```

### Step 2: Calculate Coverage

```bash
# For each sample
for bam in *.bam; do
    sample=$(basename $bam .bam)

    # Target coverage
    cnvkit.py coverage $bam <output_targets.bed> -o coverage/${sample}.targetcoverage.cnn

    # Antitarget coverage
    cnvkit.py coverage $bam <output_antitargets.bed> -o coverage/${sample}.antitargetcoverage.cnn
done
```

### Step 3: Create Reference

```bash
# From normal samples
cnvkit.py reference coverage/normal*.targetcoverage.cnn coverage/normal*.antitargetcoverage.cnn --fasta <genome.fa> -o <output_reference.cnn>

# Or flat reference (no normals available)
cnvkit.py reference --fasta <genome.fa> --targets <output_targets.bed> --antitargets <output_antitargets.bed> -o <output_flat_reference.cnn>
```

### Step 4: Call CNVs

```bash
for bam in tumor*.bam; do
    sample=$(basename $bam .bam)

    # Fix and segment
    cnvkit.py fix coverage/${sample}.targetcoverage.cnn coverage/${sample}.antitargetcoverage.cnn <output_reference.cnn> -o cnv/${sample}.cnr
    cnvkit.py segment cnv/${sample}.cnr -o cnv/${sample}.cns
    cnvkit.py call cnv/${sample}.cns -o cnv/${sample}.call.cns
done
```

### Step 5: Visualization

```bash
# Scatter plot for single sample
cnvkit.py scatter cnv/<sample>.cnr -s cnv/<sample>.cns -o plots/<sample>_scatter.pdf

# Heatmap for multiple samples
cnvkit.py heatmap cnv/*.cns -o plots/cohort_heatmap.pdf
```

### Step 6: Export and Annotation

```bash
# Export to various formats
cnvkit.py export seg cnv/*.cns -o cnv/cohort.seg
cnvkit.py export vcf cnv/<sample>.call.cns -o cnv/<sample>.vcf
cnvkit.py genemetrics cnv/<sample>.cnr -s cnv/<sample>.cns --threshold 0.2 -o cnv/<sample>_genes.tsv
```

## Batch Processing Script

```bash
#!/bin/bash
set -e

OUTDIR="cnv_results"
mkdir -p ${OUTDIR}/{coverage,cnv,plots,annotation}

# Process all tumor samples
for bam in tumor*.bam; do
    sample=$(basename $bam .bam)
    echo "Processing ${sample}..."

    # Coverage
    cnvkit.py coverage $bam <output_targets.bed> -o ${OUTDIR}/coverage/${sample}.targetcoverage.cnn
    cnvkit.py coverage $bam <output_antitargets.bed> -o ${OUTDIR}/coverage/${sample}.antitargetcoverage.cnn

    # Fix
    cnvkit.py fix ${OUTDIR}/coverage/${sample}.targetcoverage.cnn ${OUTDIR}/coverage/${sample}.antitargetcoverage.cnn <output_reference.cnn> -o ${OUTDIR}/cnv/${sample}.cnr

    # Segment
    cnvkit.py segment ${OUTDIR}/cnv/${sample}.cnr -o ${OUTDIR}/cnv/${sample}.cns

    # Call
    cnvkit.py call ${OUTDIR}/cnv/${sample}.cns -o ${OUTDIR}/cnv/${sample}.call.cns

    # Plot
    cnvkit.py scatter ${OUTDIR}/cnv/${sample}.cnr -s ${OUTDIR}/cnv/${sample}.cns -o ${OUTDIR}/plots/${sample}.pdf
done

echo "Pipeline complete. Results in ${OUTDIR}/"
```

## Quality Control and Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Noisy signal | Low coverage | Increase sequencing depth |
| No CNVs | Flat reference, normal sample | Check reference creation |
| Many small CNVs | Over-segmentation | Increase segment min size |
| Batch effects | Different capture kits | Match samples to correct reference |

## Related Skills

- **copy-number/cnv-visualization** - Advanced plotting options
- **copy-number/cnv-annotation** - Gene-level annotation
- **alignment-files/alignment-statistics** - QC of input BAMs
- **long-read-sequencing/structural-variants** - Complementary SV calling