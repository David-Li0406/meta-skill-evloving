---
name: bio-epitranscriptomics-m6a-analysis
description: Use this skill for comprehensive analysis of m6A methylation from MeRIP-seq data, including peak calling, differential methylation analysis, and visualization.
---

# Skill body

## Overview

This skill provides a complete workflow for analyzing m6A methylation from MeRIP-seq data, including quality control, alignment, peak calling, differential analysis, and visualization.

## Step 1: Quality Control

```bash
fastp -i IP_R1.fq.gz -I IP_R2.fq.gz \
    -o IP_R1_trimmed.fq.gz -O IP_R2_trimmed.fq.gz \
    --json IP_fastp.json --html IP_fastp.html

fastp -i Input_R1.fq.gz -I Input_R2.fq.gz \
    -o Input_R1_trimmed.fq.gz -O Input_R2_trimmed.fq.gz \
    --json Input_fastp.json --html Input_fastp.html
```

## Step 2: Alignment

```bash
STAR --genomeDir star_index \
    --readFilesIn IP_R1_trimmed.fq.gz IP_R2_trimmed.fq.gz \
    --readFilesCommand zcat \
    --outSAMtype BAM SortedByCoordinate \
    --outFileNamePrefix IP_

STAR --genomeDir star_index \
    --readFilesIn Input_R1_trimmed.fq.gz Input_R2_trimmed.fq.gz \
    --readFilesCommand zcat \
    --outSAMtype BAM SortedByCoordinate \
    --outFileNamePrefix Input_

samtools index IP_Aligned.sortedByCoord.out.bam
samtools index Input_Aligned.sortedByCoord.out.bam
```

## Step 3: Peak Calling with exomePeak2

```r
library(exomePeak2)

result <- exomePeak2(
    bam_ip = c('IP_rep1.bam', 'IP_rep2.bam'),
    bam_input = c('Input_rep1.bam', 'Input_rep2.bam'),
    gff = 'genes.gtf',
    genome = 'hg38'
)

peaks <- exomePeaks(result)
exportResults(result, format = 'BED', file = 'm6a_peaks.bed')
```

## Step 4: Differential Methylation Analysis

```r
# Define sample design
design <- data.frame(
    condition = factor(c('ctrl', 'ctrl', 'treat', 'treat'))
)

# Differential peak calling
result <- exomePeak2(
    bam_ip = c('ctrl_IP1.bam', 'ctrl_IP2.bam', 'treat_IP1.bam', 'treat_IP2.bam'),
    bam_input = c('ctrl_Input1.bam', 'ctrl_Input2.bam', 'treat_Input1.bam', 'treat_Input2.bam'),
    gff = 'genes.gtf',
    genome = 'hg38',
    experiment_design = design
)

# Get differential sites
diff_sites <- results(result, contrast = c('condition', 'treat', 'ctrl'))
```

## Step 5: Visualization

```r
library(ggplot2)

# Volcano plot
ggplot(diff_sites, aes(x = log2FoldChange, y = -log10(padj))) +
    geom_point(aes(color = padj < 0.05 & abs(log2FoldChange) > 1)) +
    geom_hline(yintercept = -log10(0.05), linetype = 'dashed') +
    geom_vline(xintercept = c(-1, 1), linetype = 'dashed')
```

## Related Skills

- **m6a-peak-calling** - Identify peaks first
- **differential-expression** - Similar statistical concepts
- **modification-visualization** - Plot differential sites