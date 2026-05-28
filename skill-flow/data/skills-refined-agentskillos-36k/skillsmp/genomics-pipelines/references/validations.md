# Genomics Pipelines - Validations

## DNA Aligner Used for RNA-seq

### **Id**
dna-aligner-for-rna
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - bwa\s+(mem|aln).*rna|rna.*bwa\s+(mem|aln)
  - bowtie2?.*rna|rna.*bowtie2?
  - RNA.*bwa_mem|bwa_mem.*RNA
### **Message**
Use splice-aware aligner (STAR, HISAT2) for RNA-seq, not BWA/Bowtie.
### **Fix Action**
Replace with: STAR --genomeDir index --readFilesIn reads.fq
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf
  - **/*.smk

## Alignment Without Read Groups

### **Id**
missing-read-groups
### **Severity**
high
### **Type**
regex
### **Pattern**
  - bwa\s+mem(?![\s\S]{0,100}-R\s+['"]@RG)
  - bwa-mem2\s+mem(?![\s\S]{0,100}-R\s+['"]@RG)
### **Message**
Include read groups (-R '@RG\tID:...') for GATK compatibility.
### **Fix Action**
Add: -R '@RG\tID:sample\tSM:sample\tPL:ILLUMINA'
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf

## Duplicate Marking on RNA-seq

### **Id**
duplicate-marking-rnaseq
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - MarkDuplicates.*rna|rna.*MarkDuplicates
  - mark.*dup.*RNA|RNA.*mark.*dup
### **Message**
Consider skipping duplicate marking for RNA-seq unless using UMIs.
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf

## Hardcoded Genome Reference Path

### **Id**
hardcoded-genome-path
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - /home/[a-z]+/.*\.fa[sta]?
  - /data/genomes/.*\.fa[sta]?
  - C:\\.*\.fa[sta]?
### **Message**
Use config parameter for reference genome path, not hardcoded path.
### **Fix Action**
Move to params.reference or config variable
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf
  - **/*.smk

## Using Index Without Existence Check

### **Id**
missing-index-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - samtools\s+view(?![\s\S]{0,200}index|bai)
  - \$bam(?![\s\S]{0,50}\.bai)
### **Message**
Ensure BAM index exists before operations that require it.
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf

## Defaulting to Unstranded for RNA-seq

### **Id**
unstranded-rnaseq-default
### **Severity**
info
### **Type**
regex
### **Pattern**
  - featureCounts.*-s\s*0
  - --library-type\s+unstranded
  - strandedness.*=.*'?none'?
### **Message**
Most RNA-seq is stranded. Verify library type before defaulting to unstranded.
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf

## Pipeline Without Quality Report

### **Id**
no-multiqc-report
### **Severity**
info
### **Type**
regex
### **Pattern**
  - workflow\s*\{[^}]*(?!multiqc)[^}]*\}
### **Message**
Consider adding MultiQC for unified quality reporting.
### **Applies To**
  - **/*.nf
  - **/*.smk

## Processing FASTQ Without QC

### **Id**
missing-fastqc
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (trim_galore|cutadapt|fastp)(?![\s\S]{0,500}fastqc)
### **Message**
Run FastQC before and after trimming to verify quality.
### **Applies To**
  - **/*.py
  - **/*.sh
  - **/*.nf

## Nextflow Process Without Container

### **Id**
no-container-specification
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process\s+\w+\s*\{[^}]*(?!container)[^}]*\}
### **Message**
Specify container/conda for reproducibility.
### **Applies To**
  - **/*.nf

## Using Shell Glob Instead of Channel fromFilePairs

### **Id**
shell-glob-in-channel
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Channel\.from\(.*\*.*\)
  - Channel\.fromPath\(.*_\{1,2\}.*\)
### **Message**
Use Channel.fromFilePairs() for paired-end reads.
### **Fix Action**
Channel.fromFilePairs('*_{1,2}.fastq.gz')
### **Applies To**
  - **/*.nf