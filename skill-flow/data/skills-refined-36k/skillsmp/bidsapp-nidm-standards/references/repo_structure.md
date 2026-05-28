# Repository Structure Reference

## Standard Directory Layout

```
<bidsapp_name>/                    # e.g., freesurfer_bidsapp, mriqc-nidm_bidsapp
├── src/                           # Source code
│   ├── <analysis_name>/          # Main analysis package
│   │   ├── __init__.py
│   │   ├── run.py                # CLI entry point
│   │   ├── <analysis>_runner.py  # Core analysis execution
│   │   ├── utils.py              # Utility functions
│   │   └── validators.py         # Input validation
│   └── nidm/                      # NIDM conversion package
│       ├── __init__.py
│       ├── nidm_converter.py     # Main NIDM conversion logic
│       ├── nidm_utils.py         # NIDM utilities
│       └── data/                  # NIDM reference data
│           ├── ontology_mappings.json
│           └── software_metadata.csv
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_<analysis>.py        # Analysis tests
│   ├── test_nidm.py              # NIDM conversion tests
│   ├── test_integration.py       # End-to-end tests
│   └── fixtures/                  # Test data
│       ├── bids_data/
│       └── nidm_data/
├── examples/                      # Usage examples
│   ├── example_usage.sh          # Basic usage script
│   └── babs_integration.sh       # BABS workflow example
├── Dockerfile                     # Docker container definition
├── Singularity                    # Singularity/Apptainer definition
├── setup.py                       # Package setup and metadata
├── setup.cfg                      # Setup configuration
├── requirements.txt               # Python dependencies
├── VERSION                        # Version number (e.g., 0.1.0)
├── LICENSE                        # MIT license
├── README.md                      # Usage documentation
├── .gitignore                     # Git ignore patterns
└── .github/                       # GitHub workflows (optional)
    └── workflows/
        └── test.yml              # CI/CD tests
```

## File Responsibilities

### src/<analysis_name>/run.py
- CLI argument parsing using argparse
- Input validation
- Orchestrate analysis and NIDM workflows
- Error handling and logging

### src/<analysis_name>/<analysis>_runner.py
- Execute the actual analysis tool
- Handle tool-specific configurations
- Manage intermediate outputs
- Extract metrics for NIDM

### src/nidm/nidm_converter.py
- Copy input NIDM file to output directory
- Extract relevant metrics from analysis outputs
- Integrate metrics into NIDM file (overwrite)
- Validate NIDM output

### Dockerfile
- Define container image
- Install analysis tool dependencies
- Install Python package
- Set entry point to run.py

### Singularity
- Define Apptainer/Singularity container
- Use existing base images where possible
- Install analysis tool and Python package
- Configure for HPC execution

### setup.py
- Package metadata (name, version, author)
- Define entry points for CLI commands
- Specify dependencies
- Include package data files

## Key Naming Conventions

- **Repository name**: `<tool>_bidsapp` or `<tool>-nidm_bidsapp`
  - Examples: `freesurfer_bidsapp`, `mriqc-nidm_bidsapp`, `ants_bidsapp`

- **Package name**: `<tool>_nidm` (in setup.py)
  - Examples: `freesurfer_nidm`, `mriqc_nidm`, `ants_nidm`

- **Output directory**: `<tool>_nidm` or `<tool>-nidm`
  - Must match package name for consistency

- **Container name**: `<tool>-nidm-bidsapp-<version>`
  - Example: `mriqc-nidm-bidsapp-0-1-0`

## Modularity Requirements

The NIDM conversion component must be:
- **Self-contained**: All NIDM logic in `src/nidm/` directory
- **Reusable**: Can be imported and used independently
- **Analysis-specific**: Tailored to the specific analysis tool's outputs
- **Consistent API**: Standard function signatures across all BIDSapps

Example NIDM module API:

```python
# In src/nidm/nidm_converter.py
def copy_nidm_input(input_dir, output_dir, subject_id, session_id):
    """Copy existing NIDM file to output directory."""
    pass

def extract_metrics(analysis_output_dir, subject_id, session_id):
    """Extract relevant metrics from analysis outputs."""
    pass

def integrate_to_nidm(nidm_file, metrics):
    """Integrate extracted metrics into NIDM file."""
    pass
```
