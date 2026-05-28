---
name: slurm-workflow-integration
description: "Integrating SLURM job submission with kintsugi init for HPC clusters. Trigger: adding SLURM support to projects, auto-detecting HPC settings, CLI batch submission"
author: Claude Code
date: 2026-01-22
---

# SLURM Workflow Integration with kintsugi init

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-22 |
| **Goal** | Reduce friction for HPC users by integrating SLURM setup with project initialization |
| **Environment** | HiperGator HPC, SLURM scheduler, Python 3.10+, Click CLI |
| **Status** | Success |

## Context

Before this integration, users had to:
1. Run `kintsugi init` to create a project
2. Manually discover that SLURM scripts exist in the main repo
3. Run `submit.sh --project <dir>` which creates a config
4. Edit the config with HPC-specific settings (account, partition, GPU type)
5. Re-run submission

This created undiscoverable functionality and friction for HPC users.

## Verified Workflow

### Option 1: Create Project with SLURM Support
```bash
kintsugi init /path/to/project --name "My Project" --slurm
```

Creates:
```
project/
└── slurm/
    ├── config.sh      # Pre-populated with auto-detected settings
    ├── jobs/          # Symlink to KINTSUGI job scripts
    └── README.md      # Quick-start guide
```

### Option 2: Add SLURM to Existing Project
```bash
kintsugi slurm init /path/to/project
```

### Option 3: Submit Jobs via CLI
```bash
kintsugi slurm submit .                    # All steps
kintsugi slurm submit . --steps decon,edf  # Specific steps
kintsugi slurm submit . --cycles 1-5       # Specific cycles
kintsugi slurm submit . --dry-run          # Preview commands
```

### Auto-Detection Implementation

The `hpc.py` module detects settings from the environment:

```python
def detect_hpc_settings() -> dict:
    settings = {}

    # SLURM account
    for env_var in ["SLURM_ACCOUNT", "SBATCH_ACCOUNT", "SLURM_JOB_ACCOUNT"]:
        if env_var in os.environ:
            settings["account"] = os.environ[env_var]
            break

    # GPU type from nvidia-smi
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        settings["gpu_type"] = normalize_gpu_type(result.stdout.strip())

    # Conda environment
    if "CONDA_DEFAULT_ENV" in os.environ:
        settings["conda_env"] = os.environ["CONDA_DEFAULT_ENV"]

    return settings
```

On HiperGator, this auto-detected:
- `account=maigan`
- `gpu_type=b200`
- `conda_env=KINTSUGI`

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using sed substitution on template | Complex quoting, hard to maintain | Generate config from scratch in Python |
| Copying job scripts to project | Updates don't propagate | Use symlinks to main repo |
| Requiring all settings upfront | Users don't know partition/QOS | Auto-detect with sensible defaults |
| Single monolithic command | Too many options on init | Separate `init --slurm` flag + `slurm init` for existing |

## Architecture

### Files Created

| File | Purpose |
|------|---------|
| `src/kintsugi/hpc.py` | HPC detection utilities, config generation |
| `src/kintsugi/cli.py` | Added `--slurm` flag to `init`, new `slurm` command group |
| `src/kintsugi/project.py` | Added `setup_slurm()` method to `KintsugiProject` |

### CLI Structure
```
kintsugi
├── init --slurm           # Create project with SLURM
├── slurm
│   ├── init              # Add SLURM to existing project
│   ├── submit            # Submit jobs (wrapper around submit.sh)
│   └── status            # Check job status
```

## Key Insights

- **Symlinks over copies**: Job scripts symlinked to main repo so updates propagate automatically
- **Auto-detection with overrides**: Detect what we can, allow explicit options for edge cases
- **Wrapper not replacement**: `slurm submit` wraps existing `submit.sh`, doesn't duplicate functionality
- **README as documentation**: Each project gets a README.md with quick-start guide
- **Generated not templated**: Config generated from Python (easier to maintain than sed/envsubst)

## Final Parameters

Default SLURM settings (in `hpc.py`):
```python
{
    "partition": "gpu",
    "gpu_type": "a100",
    "gpus_per_node": 2,
    "mem_correction": 64,
    "mem_stitch": 128,
    "mem_decon": 192,
    "mem_edf": 64,
    "time_correction": "04:00:00",
    "time_stitch": "06:00:00",
    "time_decon": "08:00:00",
    "time_edf": "02:00:00",
}
```

## References

- KINTSUGI CLAUDE.md - Updated with SLURM documentation
- `slurm/submit.sh` - Original submission script
- `slurm/config_template.sh` - Template for manual configuration
- HiperGator SLURM documentation: https://help.rc.ufl.edu/doc/SLURM_Commands
