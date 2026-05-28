# Bioinformatics Workflows - Validations

## Using Latest Container Tag

### **Id**
latest-container-tag
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - container.*['"].*:latest['"]
  - docker.*:latest
  - singularity.*:latest
### **Message**
Pin container version instead of 'latest' for reproducibility.
### **Fix Action**
Use specific version tag (e.g., :0.7.17--h5bf99c6_8)
### **Applies To**
  - **/*.nf
  - **/nextflow.config
  - **/*.smk
  - **/Snakefile

## Shell Without Pipefail

### **Id**
no-pipefail
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - shell:\s*['"]\s*[^'"]*\|[^'"]*['"](?![\s\S]{0,50}pipefail)
  - shell:\s*'''[^']*\|[^']*'''(?![\s\S]{0,50}pipefail)
### **Message**
Use 'set -euo pipefail' in shell blocks with pipes.
### **Applies To**
  - **/*.nf

## Hardcoded Thread Count

### **Id**
hardcoded-thread-count
### **Severity**
info
### **Type**
regex
### **Pattern**
  - -t\s+[0-9]+(?![\s\S]{0,20}\$\{?task\.cpus)
  - --threads\s+[0-9]+(?![\s\S]{0,20}\$\{?task\.cpus)
  - -p\s+[0-9]+(?![\s\S]{0,20}threads)
### **Message**
Use dynamic thread allocation (task.cpus or {threads}).
### **Applies To**
  - **/*.nf
  - **/*.smk

## Process Without Version Tracking

### **Id**
no-version-output
### **Severity**
info
### **Type**
regex
### **Pattern**
  - process\s+\w+\s*\{[^}]*output:[^}]*(?!versions)[^}]*\}
### **Message**
Include versions.yml output for tool version tracking.
### **Applies To**
  - **/*.nf

## Temp Files Without Backup Strategy

### **Id**
temp-without-protected
### **Severity**
info
### **Type**
regex
### **Pattern**
  - temp\([^)]+\.bam[^)]*\)
  - temp\([^)]+\.vcf[^)]*\)
### **Message**
Consider keeping intermediate BAM/VCF until pipeline completes.
### **Applies To**
  - **/*.smk

## Snakemake Rule Without Log

### **Id**
missing-log-directive
### **Severity**
info
### **Type**
regex
### **Pattern**
  - rule\s+\w+:[^}]*(?!log:)[^}]*shell:
### **Message**
Add log directive to capture stderr for debugging.
### **Applies To**
  - **/*.smk
  - **/Snakefile

## Process Without Resource Limits

### **Id**
no-resource-specification
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process\s+\w+\s*\{[^}]*(?!memory|cpus|label)[^}]*\}
### **Message**
Specify memory and CPU requirements for cluster execution.
### **Applies To**
  - **/*.nf

## Merging Files Without Sorting

### **Id**
unsorted-merge-input
### **Severity**
info
### **Type**
regex
### **Pattern**
  - collect\(\)(?![\s\S]{0,50}sort)
  - bcftools\s+merge(?![\s\S]{0,50}sort)
### **Message**
Sort input files before merging for reproducible order.
### **Applies To**
  - **/*.nf
  - **/*.smk

## Process Without Error Handling

### **Id**
no-error-strategy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - process\s+\w+\s*\{[^}]*(?!errorStrategy)[^}]*\}
### **Message**
Consider adding errorStrategy for retry on transient failures.
### **Applies To**
  - **/*.nf

## Absolute Path in Workflow Definition

### **Id**
absolute-path-in-workflow
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ['"]/home/[a-z]+/.*['"]
  - ['"]/data/.*['"]
  - ['"]C:\\.*['"]
### **Message**
Use relative paths or params for portability.
### **Applies To**
  - **/*.nf
  - **/*.smk
  - **/Snakefile