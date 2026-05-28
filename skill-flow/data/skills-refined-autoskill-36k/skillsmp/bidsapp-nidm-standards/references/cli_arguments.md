# CLI Arguments Reference

## Standard BIDS App Arguments

### Positional Arguments (Required)
```python
parser.add_argument('bids_dir', help='BIDS dataset directory')
parser.add_argument('output_dir', help='Output directory')
parser.add_argument('analysis_level', choices=['participant'], help='Analysis level')
```

### Standard Optional Arguments

```python
parser.add_argument('--participant-label', nargs='+',
                   help='Subject ID(s) without "sub-" prefix')
parser.add_argument('--session-label', nargs='+',
                   help='Session ID(s) without "ses-" prefix')
```

## NIDM Arguments (Required for all BIDSapps)

```python
parser.add_argument('--nidm-input-dir', required=True,
                   help='Directory containing existing NIDM files')
parser.add_argument('--skip-nidm', action='store_true',
                   help='Skip NIDM conversion step')
parser.add_argument('--skip-<analysis>', action='store_true',
                   help='Skip <analysis> execution (use existing outputs)')
```

## Analysis-Specific Arguments

Add as needed for each tool. Examples:

### FreeSurfer
```python
parser.add_argument('--fs-license', help='Path to FreeSurfer license file')
parser.add_argument('--fs-options', help='Additional options for recon-all')
```

### MRIQC
```python
parser.add_argument('--nprocs', type=int, default=1, help='Number of processors')
parser.add_argument('--mem', help='Memory limit (e.g., "16G")')
parser.add_argument('--omp-nthreads', type=int, help='OpenMP threads')
```

### ANTs
```python
parser.add_argument('--num-threads', type=int, default=1, help='Number of threads')
parser.add_argument('--prob-threshold', type=float, default=0.5,
                   help='Probability threshold for segmentation')
```

## Argument Validation

Always validate inputs:

```python
def validate_args(args):
    """Validate CLI arguments."""
    # Check BIDS directory exists
    if not Path(args.bids_dir).exists():
        raise ValueError(f"BIDS directory not found: {args.bids_dir}")
    
    # Check NIDM input directory exists
    if not Path(args.nidm_input_dir).exists():
        raise ValueError(f"NIDM input directory not found: {args.nidm_input_dir}")
    
    # Validate participant labels format
    if args.participant_label:
        for label in args.participant_label:
            if label.startswith('sub-'):
                raise ValueError(f"Remove 'sub-' prefix from participant label: {label}")
```
