---
name: run-job
description: >-
  Runs a Siril job file for astrophotography processing. Handles calibration,
  stacking, registration, and composition of LRGB/SHO/HOO images.
allowed-tools:
  - Bash
  - Read
---
# Run Siril Job

## Instructions

Run a Siril job file to process astrophotography data.

### Arguments

The skill accepts a job file path as an argument:
- `/run-job M31` - runs `jobs/M31.json`
- `/run-job jobs/IC1396.json` - runs the specified path

### Run Command

```bash
uv run python run_job.py {job_file}
```

### Common Options

```bash
# Standard run (uses cached stacks if available)
uv run python run_job.py jobs/{target}.json

# Force reprocessing (ignores cache)
uv run python run_job.py jobs/{target}.json --force

# Validate only (check calibration files exist)
uv run python run_job.py jobs/{target}.json --validate

# Dry run (show what would happen)
uv run python run_job.py jobs/{target}.json --dry-run

# Run specific stage
uv run python run_job.py jobs/{target}.json --stage preprocess
uv run python run_job.py jobs/{target}.json --stage stack
uv run python run_job.py jobs/{target}.json --stage compose
```

### Execution

1. Parse the argument to determine the job file path
2. If argument is just a target name (e.g., `M31`), use `jobs/{target}.json`
3. Run the job in the background to allow monitoring
4. Report the output paths when complete

### Output Monitoring

The job will output progress including:
- Frame counts and dates
- Calibration status
- Registration statistics
- FWHM filtering decisions
- Stack creation
- Composition steps
- Final output paths

### After Completion

Report to the user:
- Job success/failure
- Output file paths (JPG, TIF, FIT)
- Any warnings or issues from the log
