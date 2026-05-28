# Genomics Pipelines

## Patterns

### **Workflow Management**
  #### **Name**
Workflow Manager Selection
  #### **Description**
Choose appropriate workflow manager for genomics
  #### **When**
Building multi-step genomics pipeline
  #### **Pattern**
    # Nextflow (Recommended for most genomics)
    # - DSL2 with modules
    # - Excellent container support
    # - nf-core community pipelines
    
    nextflow.config:
    ```groovy
    // nextflow.config
    params {
        reads = "data/*_{1,2}.fastq.gz"
        genome = "GRCh38"
        outdir = "results"
    }
    
    profiles {
        docker {
            docker.enabled = true
        }
        singularity {
            singularity.enabled = true
            singularity.autoMounts = true
        }
        conda {
            conda.enabled = true
        }
    }
    
    // Resource management - CRITICAL for genomics
    process {
        withLabel: 'high_memory' {
            memory = '64.GB'
            cpus = 16
        }
        withLabel: 'low_memory' {
            memory = '4.GB'
            cpus = 2
        }
    }
    
    // Enable execution reports
    timeline.enabled = true
    report.enabled = true
    trace.enabled = true
    ```
    
    main.nf:
    ```groovy
    #!/usr/bin/env nextflow
    nextflow.enable.dsl = 2
    
    include { FASTQC } from './modules/fastqc'
    include { TRIM_GALORE } from './modules/trim_galore'
    include { BWA_MEM } from './modules/bwa_mem'
    
    workflow {
        // Input channels
        reads_ch = Channel
            .fromFilePairs(params.reads, checkIfExists: true)
    
        // Pipeline steps
        FASTQC(reads_ch)
        TRIM_GALORE(reads_ch)
        BWA_MEM(TRIM_GALORE.out.reads, params.genome)
    }
    ```
    
  #### **Why**
Nextflow handles complex dependencies and scales from laptop to HPC/cloud
### **Fastq Processing**
  #### **Name**
FASTQ Quality Control
  #### **Description**
Validate and preprocess raw sequencing reads
  #### **Pattern**
    import subprocess
    from pathlib import Path
    from dataclasses import dataclass
    from typing import Tuple, Optional
    
    @dataclass
    class FastQCResult:
        total_sequences: int
        sequence_length: str
        gc_content: float
        per_base_quality: str  # PASS/WARN/FAIL
        adapter_content: str
    
    def validate_fastq_pair(
        read1: Path,
        read2: Path
    ) -> Tuple[bool, list[str]]:
        """
        Validate paired FASTQ files before processing.
    
        CRITICAL CHECKS:
        - Same number of reads in both files
        - Read names match (except /1 /2 suffix)
        - No truncated records
        """
        errors = []
    
        # Check files exist and are gzipped
        for f in [read1, read2]:
            if not f.exists():
                errors.append(f"File not found: {f}")
            if not f.suffix == '.gz':
                errors.append(f"FASTQ should be gzipped: {f}")
    
        # Count reads (fast method)
        def count_reads(fastq_gz: Path) -> int:
            result = subprocess.run(
                f"zcat {fastq_gz} | wc -l",
                shell=True, capture_output=True, text=True
            )
            return int(result.stdout.strip()) // 4
    
        r1_count = count_reads(read1)
        r2_count = count_reads(read2)
    
        if r1_count != r2_count:
            errors.append(
                f"Read count mismatch: R1={r1_count}, R2={r2_count}"
            )
    
        return len(errors) == 0, errors
    
    def run_fastqc(
        fastq: Path,
        outdir: Path,
        threads: int = 4
    ) -> FastQCResult:
        """Run FastQC and parse results."""
        subprocess.run([
            "fastqc",
            "--threads", str(threads),
            "--outdir", str(outdir),
            str(fastq)
        ], check=True)
    
        # Parse FastQC output
        # ... parse fastqc_data.txt
        return FastQCResult(...)
    
    def trim_adapters(
        read1: Path,
        read2: Path,
        outdir: Path,
        min_length: int = 20,
        quality_cutoff: int = 20
    ) -> Tuple[Path, Path]:
        """
        Trim adapters and low-quality bases.
    
        Uses Trim Galore (wrapper around Cutadapt + FastQC).
        """
        subprocess.run([
            "trim_galore",
            "--paired",
            "--quality", str(quality_cutoff),
            "--length", str(min_length),
            "--fastqc",
            "--output_dir", str(outdir),
            str(read1), str(read2)
        ], check=True)
    
        # Return trimmed file paths
        r1_trimmed = outdir / f"{read1.stem}_val_1.fq.gz"
        r2_trimmed = outdir / f"{read2.stem}_val_2.fq.gz"
        return r1_trimmed, r2_trimmed
    
  #### **Why**
Quality control prevents garbage-in-garbage-out in downstream analysis
### **Alignment Pipeline**
  #### **Name**
Read Alignment Best Practices
  #### **Description**
Align reads to reference genome correctly
  #### **Pattern**
    from pathlib import Path
    import subprocess
    from typing import Optional
    
    def align_dna_reads(
        read1: Path,
        read2: Path,
        reference: Path,
        output_bam: Path,
        sample_name: str,
        read_group: Optional[str] = None,
        threads: int = 8
    ) -> Path:
        """
        Align DNA reads with BWA-MEM2.
    
        CRITICAL: Include read groups for downstream tools.
        """
        if read_group is None:
            # Construct proper read group
            read_group = (
                f"@RG\\tID:{sample_name}\\t"
                f"SM:{sample_name}\\t"
                f"PL:ILLUMINA\\t"
                f"LB:{sample_name}"
            )
    
        # BWA-MEM2 alignment + sort + index
        cmd = f"""
        bwa-mem2 mem \\
            -t {threads} \\
            -R '{read_group}' \\
            {reference} \\
            {read1} {read2} \\
        | samtools sort \\
            -@ {threads} \\
            -o {output_bam} \\
            -
    
        samtools index {output_bam}
        """
        subprocess.run(cmd, shell=True, check=True)
        return output_bam
    
    def align_rna_reads(
        read1: Path,
        read2: Path,
        genome_dir: Path,
        output_prefix: Path,
        threads: int = 8
    ) -> Path:
        """
        Align RNA-seq reads with STAR.
    
        CRITICAL: Use splice-aware aligner for RNA-seq!
        Never use BWA/Bowtie for RNA-seq.
        """
        subprocess.run([
            "STAR",
            "--runThreadN", str(threads),
            "--genomeDir", str(genome_dir),
            "--readFilesIn", str(read1), str(read2),
            "--readFilesCommand", "zcat",  # For gzipped files
            "--outFileNamePrefix", str(output_prefix),
            "--outSAMtype", "BAM", "SortedByCoordinate",
            "--outSAMattributes", "NH", "HI", "AS", "nM", "MD",
            "--quantMode", "GeneCounts",  # Also count genes
        ], check=True)
    
        return Path(f"{output_prefix}Aligned.sortedByCoord.out.bam")
    
    def mark_duplicates(
        input_bam: Path,
        output_bam: Path,
        metrics_file: Path
    ) -> Path:
        """
        Mark PCR duplicates.
    
        CRITICAL for DNA-seq (variant calling).
        OPTIONAL for RNA-seq (depends on analysis).
        """
        subprocess.run([
            "picard", "MarkDuplicates",
            f"I={input_bam}",
            f"O={output_bam}",
            f"M={metrics_file}",
            "CREATE_INDEX=true",
            "VALIDATION_STRINGENCY=LENIENT"
        ], check=True)
        return output_bam
    
  #### **Why**
Correct alignment is foundation for all downstream analyses
### **Variant Calling**
  #### **Name**
Variant Calling Pipeline
  #### **Description**
Call SNPs and indels from aligned reads
  #### **Pattern**
    from pathlib import Path
    import subprocess
    from dataclasses import dataclass
    
    @dataclass
    class VariantCallingConfig:
        reference: Path
        known_sites: list[Path]  # Known variants for BQSR
        intervals: Optional[Path] = None  # Target regions
        min_base_quality: int = 20
        min_mapping_quality: int = 20
    
    def gatk_variant_calling_pipeline(
        input_bam: Path,
        config: VariantCallingConfig,
        output_vcf: Path,
        sample_name: str
    ) -> Path:
        """
        GATK Best Practices variant calling.
    
        Steps:
        1. Base Quality Score Recalibration (BQSR)
        2. HaplotypeCaller
        3. Variant filtering (CNN or hard filters)
        """
        # Step 1: BQSR - Recalibrate base quality scores
        recal_table = output_vcf.with_suffix('.recal_data.table')
    
        known_sites_args = []
        for ks in config.known_sites:
            known_sites_args.extend(["--known-sites", str(ks)])
    
        subprocess.run([
            "gatk", "BaseRecalibrator",
            "-I", str(input_bam),
            "-R", str(config.reference),
            *known_sites_args,
            "-O", str(recal_table)
        ], check=True)
    
        # Apply BQSR
        recal_bam = input_bam.with_suffix('.recal.bam')
        subprocess.run([
            "gatk", "ApplyBQSR",
            "-I", str(input_bam),
            "-R", str(config.reference),
            "--bqsr-recal-file", str(recal_table),
            "-O", str(recal_bam)
        ], check=True)
    
        # Step 2: Call variants with HaplotypeCaller
        raw_vcf = output_vcf.with_suffix('.raw.vcf.gz')
        subprocess.run([
            "gatk", "HaplotypeCaller",
            "-I", str(recal_bam),
            "-R", str(config.reference),
            "-O", str(raw_vcf),
            "--emit-ref-confidence", "GVCF",  # For joint calling
        ], check=True)
    
        # Step 3: Filter variants
        subprocess.run([
            "gatk", "CNNScoreVariants",
            "-V", str(raw_vcf),
            "-R", str(config.reference),
            "-O", str(output_vcf)
        ], check=True)
    
        return output_vcf
    
    def deepvariant_calling(
        input_bam: Path,
        reference: Path,
        output_vcf: Path,
        model_type: str = "WGS"  # WGS, WES, or PACBIO
    ) -> Path:
        """
        DeepVariant - Deep learning variant caller.
    
        Often more accurate than GATK for certain data types.
        """
        subprocess.run([
            "run_deepvariant",
            f"--model_type={model_type}",
            f"--ref={reference}",
            f"--reads={input_bam}",
            f"--output_vcf={output_vcf}",
            "--num_shards=8"
        ], check=True)
        return output_vcf
    
  #### **Why**
GATK Best Practices and DeepVariant are gold standards for variant calling
### **Rnaseq Analysis**
  #### **Name**
RNA-seq Analysis Pipeline
  #### **Description**
Differential expression and transcript quantification
  #### **Pattern**
    from pathlib import Path
    import pandas as pd
    import subprocess
    
    def quantify_transcripts_salmon(
        read1: Path,
        read2: Path,
        index_dir: Path,
        output_dir: Path,
        threads: int = 8
    ) -> Path:
        """
        Salmon pseudo-alignment for transcript quantification.
    
        Faster than alignment-based methods, accurate for DE analysis.
        """
        subprocess.run([
            "salmon", "quant",
            "-i", str(index_dir),
            "-l", "A",  # Automatic library type detection
            "-1", str(read1),
            "-2", str(read2),
            "-p", str(threads),
            "--validateMappings",
            "--gcBias",  # GC bias correction
            "--seqBias",  # Sequence-specific bias correction
            "-o", str(output_dir)
        ], check=True)
    
        return output_dir / "quant.sf"
    
    def run_deseq2_analysis(
        count_matrix: pd.DataFrame,
        sample_info: pd.DataFrame,
        design_formula: str = "~ condition",
        alpha: float = 0.05
    ) -> pd.DataFrame:
        """
        DESeq2 differential expression analysis.
    
        Uses rpy2 to call R. Returns results as pandas DataFrame.
        """
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.packages import importr
    
        pandas2ri.activate()
    
        deseq2 = importr('DESeq2')
    
        # Convert to R objects
        r_counts = pandas2ri.py2rpy(count_matrix)
        r_coldata = pandas2ri.py2rpy(sample_info)
    
        # Create DESeqDataSet
        dds = deseq2.DESeqDataSetFromMatrix(
            countData=r_counts,
            colData=r_coldata,
            design=ro.Formula(design_formula)
        )
    
        # Run DESeq2
        dds = deseq2.DESeq(dds)
    
        # Get results
        res = deseq2.results(dds, alpha=alpha)
        results_df = pandas2ri.rpy2py(ro.r['as.data.frame'](res))
    
        return results_df
    
    # CRITICAL: Proper sample size for RNA-seq
    SAMPLE_SIZE_GUIDANCE = """
    RNA-seq Sample Size Guidelines:
    - Minimum: 3 biological replicates per condition
    - Recommended: 6+ for detecting subtle differences
    - Power analysis: Use RNASeqPower R package
    
    Technical replicates are NOT substitutes for biological replicates!
    """
    
  #### **Why**
RNA-seq requires careful experimental design and appropriate statistical methods

## Anti-Patterns

### **Dna Aligner For Rna**
  #### **Name**
Using DNA Aligner for RNA-seq
  #### **Problem**
    # Using BWA or Bowtie2 for RNA-seq
    bwa mem reference.fa rna_reads.fq > aligned.sam
    
  #### **Solution**
    # Use splice-aware aligner (STAR, HISAT2)
    STAR --genomeDir star_index --readFilesIn reads.fq
    
### **Ignoring Read Groups**
  #### **Name**
Missing Read Groups in BAM
  #### **Problem**
BAM files without @RG tags fail in GATK
  #### **Solution**
Always include -R '@RG\tID:...' in alignment
### **Hardcoded Paths**
  #### **Name**
Hardcoded Paths in Pipeline
  #### **Problem**
Pipeline only works on one machine
  #### **Solution**
Use config files and container paths