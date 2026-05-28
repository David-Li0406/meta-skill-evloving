---
name: bio-epitranscriptomics-m6a-analysis
description: Use this skill for comprehensive analysis of m6A methylation from MeRIP-seq data, including peak calling, differential analysis, and visualization.
---

# m6A Analysis Workflow

## Overview

This workflow covers the end-to-end analysis of m6A methylation from MeRIP-seq data, including quality control, alignment, peak calling, differential analysis, and visualization.

## Step 1: Quality Control

```bash
fastp -i <IP_R1> -I <IP_R2> -o <IP_R1_trimmed> -O <IP_R2_trimmed> --json <IP_fastp.json> --html <IP_fastp.html>
fastp -i <Input_R1> -I <Input_R2> -o <Input_R1_trimmed> -O <Input_R2_trimmed> --json <Input_fastp.json> --html <Input_fastp.html>
```

## Step 2: Alignment

```bash
STAR --genomeDir <genome_index> --readFilesIn <IP_R1_trimmed> <IP_R2_trimmed> --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate --outFileNamePrefix <IP_prefix>
STAR --genomeDir <genome_index> --readFilesIn <Input_R1_trimmed> <Input_R2_trimmed> --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate --outFileNamePrefix <Input_prefix>

samtools index <IP_bam>
samtools index <Input_bam>
```

## Step 3: Peak Calling with exomePeak2

```r
library(exomePeak2)
library(TxDb.Hsapiens.UCSC.hg38.knownGene)

result <- exomePeak2(
    bam_ip = c('<IP_rep1.bam>', '<IP_rep2.bam>'),
    bam_input = c('<Input_rep1.bam>', '<Input_rep2.bam>'),
    txdb = TxDb.Hsapiens.UCSC.hg38.knownGene,
    genome = 'hg38'
)

peaks <- exomePeaks(result)
exportResults(result, format = 'BED', file = 'm6a_peaks.bed')
```

## Step 4: Differential Methylation Analysis

```r
library(exomePeak2)

design <- data.frame(
    condition = factor(c('ctrl', 'ctrl', 'treat', 'treat')),
    row.names = c('ctrl_1', 'ctrl_2', 'treat_1', 'treat_2')
)

diff_result <- exomePeak2(
    bam_ip = c('<ctrl_IP_1.bam>', '<ctrl_IP_2.bam>', '<treat_IP_1.bam>', '<treat_IP_2.bam>'),
    bam_input = c('<ctrl_Input_1.bam>', '<ctrl_Input_2.bam>', '<treat_Input_1.bam>', '<treat_Input_2.bam>'),
    txdb = TxDb.Hsapiens.UCSC.hg38.knownGene,
    experiment_design = design,
    test_method = 'DESeq2'
)

diff_peaks <- results(diff_result)
sig_peaks <- diff_peaks[diff_peaks$padj < 0.05, ]
```

## Step 5: Visualization

### Volcano Plot

```r
library(ggplot2)

ggplot(diff_peaks, aes(x = log2FoldChange, y = -log10(padj))) +
    geom_point(aes(color = padj < 0.05 & abs(log2FoldChange) > 1)) +
    geom_hline(yintercept = -log10(0.05), linetype = 'dashed') +
    geom_vline(xintercept = c(-1, 1), linetype = 'dashed')
```

### Peak Annotation

```r
library(ChIPseeker)

peaks_gr <- import('m6a_peaks.bed')
anno <- annotatePeak(peaks_gr, TxDb = TxDb.Hsapiens.UCSC.hg38.knownGene)
plotAnnoBar(anno)
plotDistToTSS(anno)
```

## Output Files

| File | Description |
|------|-------------|
| `m6a_peaks.bed` | Called m6A peak locations |
| `diff_m6a.csv` | Differential methylation results |
| `metagene.pdf` | Peak distribution across transcripts |

## Related Skills

- **m6a-peak-calling** - Identify peaks from MeRIP-seq data.
- **differential-expression** - Statistical methods for differential analysis.
- **modification-visualization** - Techniques for visualizing epitranscriptomic modifications.