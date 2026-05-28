# Bioinformatics Workflows - Sharp Edges

## Pipeline Not Resumable After Failure

### **Id**
non-resumable-pipeline
### **Severity**
critical
### **Summary**
Restart from beginning after crash wastes hours/days of compute
### **Symptoms**
  - Cluster job times out, entire pipeline restarts
  - One sample fails, all samples re-run
  - Intermediate files deleted before completion
### **Why**
  Genomics pipelines can run for days. Without checkpointing/caching:
  - A network blip at hour 47 means starting over
  - Cluster preemption restarts everything
  - Debugging requires full re-runs
  
  Most workflow managers have resume capability, but it must be configured.
  
### **Gotcha**
  # Snakemake: Deletes temp files by default
  temp("results/aligned/{sample}.unsorted.bam")
  # If job fails after this, can't resume without re-running
  
  # Nextflow: cache disabled
  process.cache = false
  # Every run starts from scratch
  
### **Solution**
  # Nextflow: Enable resume (default)
  nextflow run main.nf -resume
  
  # Snakemake: Use --keep-incomplete
  snakemake --keep-incomplete ...
  
  # Keep intermediate files until pipeline completes
  # Don't mark as temp() until you're sure
  
  # Use work directory on fast storage
  workDir = '/scratch/nextflow_work'
  

## Non-Deterministic File Processing Order

### **Id**
unstable-sort-order
### **Severity**
high
### **Summary**
Glob patterns produce different order on different runs
### **Symptoms**
  - Same inputs, different checksum on outputs
  - Merged VCFs have samples in random order
  - Hard to compare runs
### **Why**
  file() and glob patterns don't guarantee order.
  Different filesystems return files in different orders.
  This causes non-reproducible outputs even with same inputs.
  
### **Gotcha**
  # Nextflow - order not guaranteed
  Channel.fromFilePairs("*.{1,2}.fq.gz")
  
  # Snakemake - expand() order varies
  expand("data/{sample}.bam", sample=samples)
  
### **Solution**
  // Nextflow: Sort the channel
  Channel
      .fromFilePairs("*.{1,2}.fq.gz")
      .toSortedList { it[0] }  // Sort by sample name
      .flatMap()
      .set { sorted_reads }
  
  # Snakemake: Sort in rule
  sorted_samples = sorted(samples)
  expand("data/{sample}.bam", sample=sorted_samples)
  
  # Always sort before merging
  bcftools merge $(ls *.vcf.gz | sort) > merged.vcf.gz
  

## Symlinks Not Followed in Containers

### **Id**
symlink-container-failure
### **Severity**
high
### **Summary**
Files exist but container process can't read them
### **Symptoms**
  - File not found errors in container
  - Works outside container, fails inside
  - Absolute path works, relative doesn't
### **Why**
  Containers mount specific directories.
  Symlinks pointing outside mounted directories are broken.
  This is especially common with shared storage and staged inputs.
  
### **Gotcha**
  # Host filesystem:
  /data/project/sample.bam -> /shared/raw_data/sample.bam
  
  # Container only mounts /data/project
  # Symlink target /shared/raw_data is not available
  
### **Solution**
  // Nextflow: Use stageInMode 'copy' for problem files
  process ALIGN {
      stageInMode 'copy'  // or 'link' with full path mounts
      ...
  }
  
  // Mount all required directories
  docker.runOptions = '-v /data:/data -v /shared:/shared'
  singularity.runOptions = '-B /data:/data -B /shared:/shared'
  
  # Snakemake: Use shadow rules
  rule align:
      shadow: "minimal"  # Copies inputs to temp dir
      ...
  

## Memory Requests Don't Match Actual Usage

### **Id**
memory-estimation-wrong
### **Severity**
high
### **Summary**
Jobs OOM killed or waste cluster resources
### **Symptoms**
  - Jobs killed with OOM (out of memory)
  - Jobs pending because requesting too much memory
  - Cluster efficiency < 50%
### **Why**
  Genomics tools have variable memory usage:
  - BWA: ~5GB per thread for human genome
  - STAR: 30-40GB for genome loading
  - GATK: Varies wildly by step
  
  Static memory requests don't account for sample size variation.
  
### **Gotcha**
  # Requesting flat 8GB for all samples
  process {
      memory = '8 GB'
  }
  # Small sample: wastes 6GB
  # Large sample: OOM killed
  
### **Solution**
  // Nextflow: Dynamic memory based on input
  process ALIGN {
      memory { 6.GB * task.cpus }
  
      // Or with retry
      memory { 8.GB * task.attempt }
      errorStrategy { task.exitStatus in 137..140 ? 'retry' : 'terminate' }
      maxRetries 3
  }
  
  # Snakemake: Use resources based on input
  rule align:
      resources:
          mem_mb=lambda wildcards, input: max(8000, input.size_mb * 10)
      ...
  
  # Profile tools to understand memory patterns
  # Use /usr/bin/time -v to get max RSS
  

## Ignoring Non-Zero Exit Codes

### **Id**
missing-exit-codes
### **Severity**
high
### **Summary**
Pipeline continues after tool failure, producing garbage
### **Symptoms**
  - Empty output files
  - Truncated BAMs/VCFs
  - Downstream tools fail with cryptic errors
### **Why**
  Some tools return non-zero exit codes for warnings.
  Others return 0 even on failure.
  Shell pipelines mask exit codes by default.
  
### **Gotcha**
  # Shell pipeline hides BWA failure
  bwa mem ref.fa reads.fq | samtools sort -o out.bam
  # Exit code is from samtools, not bwa
  
  # Tool returns 0 but wrote nothing
  some_tool input.fa > output.fa  # Empty file, exit 0
  
### **Solution**
  # Use pipefail in shell
  set -euo pipefail
  bwa mem ref.fa reads.fq | samtools sort -o out.bam
  
  # Nextflow: Always set in shell
  process ALIGN {
      shell:
      '''
      set -euo pipefail
      bwa mem !{ref} !{reads} | samtools sort -o !{output}
      '''
  }
  
  # Validate outputs
  if [[ ! -s output.fa ]]; then
      echo "Error: output file is empty" >&2
      exit 1
  fi
  
  # Check expected output patterns
  samtools quickcheck aligned.bam || exit 1
  

## Multiple Jobs Writing to Same Output

### **Id**
race-condition-outputs
### **Severity**
critical
### **Summary**
Parallel jobs overwrite each other's results
### **Symptoms**
  - Random missing samples in merged output
  - Different results each run
  - File corruption errors
### **Why**
  When parallelizing, multiple jobs may try to write to the same file.
  This causes race conditions and data loss.
  
### **Gotcha**
  # Multiple parallel jobs appending to same file
  parallel 'process {} >> combined_results.txt' ::: samples/*
  # Order is random, may have interleaved lines
  
  # GATK GenomicsDBImport with multiple writers
  gatk GenomicsDBImport ... --batch-size 50
  # Can fail with too many concurrent writers
  
### **Solution**
  # Write to separate files, merge at end
  parallel 'process {} > results/{/.}.txt' ::: samples/*
  cat results/*.txt > combined_results.txt
  
  # Use atomic writes
  process {} > temp_$$.txt && mv temp_$$.txt final.txt
  
  # Let workflow manager handle parallelism
  # Don't manually parallelize within rules/processes
  

## Using 'latest' Container Tags

### **Id**
version-drift-containers
### **Severity**
high
### **Summary**
Pipeline behavior changes without code changes
### **Symptoms**
  - Pipeline worked yesterday, fails today
  - Different results on different machines
  - Can't reproduce old analysis
### **Why**
  'latest' tags get updated. Your pipeline pulls a new version
  with different behavior, bugs, or broken dependencies.
  
### **Gotcha**
  container = 'biocontainers/bwa:latest'
  # Today: bwa 0.7.17
  # Next week: bwa 0.7.18 with different defaults
  
### **Solution**
  # Always use specific version tags
  container = 'biocontainers/bwa:0.7.17--h5bf99c6_8'
  
  # Use SHA256 digest for maximum reproducibility
  container = 'biocontainers/bwa@sha256:abc123...'
  
  # Lock all tool versions in environment
  # Export conda-lock or requirements.txt
  