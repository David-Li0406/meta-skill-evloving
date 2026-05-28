# BABS Configuration Reference

Use the BABS script example (mriqc_babs_script1226.sh) as the reference template.

## Key Configuration Elements

### Input Datasets
- BIDS dataset with required files
- NIDM dataset for incremental building

### CLI Arguments  
- Standard BIDS args (--participant_label, --session_label)
- NIDM args (--nidm-input-dir)
- Analysis-specific args

### Output Configuration
Use bidsapp name as zip folder (e.g., mriqc_nidm)

### Resource Requirements
Adjust CPU, memory, time based on analysis tool
