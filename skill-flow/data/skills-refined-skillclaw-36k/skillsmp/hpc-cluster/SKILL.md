---
name: hpc-cluster
description: Run jobs on CU Boulder CURC HPC cluster (Alpine). Use when simulations need more compute than the local workstation, for large-scale parallel jobs, or when GPU resources are needed beyond local availability. You have full SSH access - work like a researcher.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# CURC HPC Cluster Access (CU Boulder Alpine)

You have full SSH access to CU Boulder's Alpine HPC cluster. You can do everything a human researcher can do: submit jobs, debug failures, load modules, transfer files, and work autonomously.

## Quick Reference

| Item | Value |
|------|-------|
| **Login** | `ssh $CURC_USER@login.rc.colorado.edu` |
| **Filesystem** | `/scratch/alpine/$CURC_USER/` (10TB, fast I/O) |
| **Agent Workspace** | `/scratch/alpine/$CURC_USER/Agent_Runs/` |
| **Job Scheduler** | SLURM |
| **Default Partition** | `amilan` (CPU), `aa100` (GPU) |
| **Authentication** | SSH key (pre-configured) |
| **HPC Client** | `.claude/skills/hpc-cluster/hpc_client.py` |

---

## Two Ways to Work

You have two approaches available:

### 1. Python HPC Client (Recommended for common operations)

A lightweight client that handles connection management and common patterns:

```python
import sys
import os
# Add the skill directory to path (relative to project root)
skill_dir = os.path.join(os.environ.get('PROJECT_ROOT', '.'), '.claude/skills/hpc-cluster')
sys.path.insert(0, skill_dir)
from hpc_client import HPCClient

hpc = HPCClient()
hpc.connect()

# Create workspace, upload files, submit job, wait for completion
run_dir = hpc.create_run("argon-diffusion")
hpc.upload("input.lmp", f"{run_dir}/input.lmp")
hpc.upload("job.slurm", f"{run_dir}/job.slurm")
job_id = hpc.submit(f"{run_dir}/job.slurm")
status = hpc.wait_for_job(job_id, timeout=3600)

if status.is_success:
    hpc.download(f"{run_dir}/output.dat", "./results/")
else:
    # Debug: read error output
    print(hpc.read_file(f"{run_dir}/my_job_{job_id}.err"))

hpc.disconnect()
```

### 2. Direct SSH (For full control)

When you need to do something the client doesn't support, use raw SSH:

```bash
# Run any command
ssh $CURC_USER@login.rc.colorado.edu "your command here"

# Interactive debugging
ssh $CURC_USER@login.rc.colorado.edu
```

**Use the client for**: workspace setup, file transfer, job submission, job monitoring
**Use raw SSH for**: debugging, exploring, unusual operations, anything not covered

---

## Connection

### SSH Access

SSH is pre-configured with key-based authentication and connection multiplexing via `~/.ssh/config`. Use the `cu_alpine` alias for simplicity:

```bash
# Connect to CURC login node (uses ~/.ssh/config)
ssh cu_alpine

# Run a single command
ssh cu_alpine "squeue -u $CURC_USER"

# Or use full address
ssh $CURC_USER@login.rc.colorado.edu "squeue -u $CURC_USER"

# Transfer files TO HPC
scp local_file.txt $CURC_USER@login.rc.colorado.edu:/scratch/alpine/$CURC_USER/

# Transfer files FROM HPC
scp $CURC_USER@login.rc.colorado.edu:/scratch/alpine/$CURC_USER/results.dat ./
```

**Connection multiplexing**: The SSH config uses ControlMaster to reuse connections - the first connection is slower, but subsequent ones are instant.

**Important**: The login node is for submitting jobs and light tasks. Never run compute-intensive work directly on login nodes.

---

## Workspace Structure

All agent work on HPC goes in the existing `Agent_Runs` directory:

```
/scratch/alpine/$CURC_USER/Agent_Runs/
├── argon-diffusion-20260118/
│   ├── inputs/
│   ├── outputs/
│   ├── job.slurm
│   └── README.md
├── water-tip4p-20260119/
├── shared/
│   ├── potentials/          # Downloaded force fields
│   ├── pseudopotentials/    # Downloaded pseudopotentials
│   └── scripts/             # Reusable analysis scripts
└── ...
```

### Creating a New Run

```bash
# Create run directory with timestamp
RUN_NAME="project-name-$(date +%Y%m%d-%H%M%S)"
RUN_DIR="/scratch/alpine/$CURC_USER/Agent_Runs/$RUN_NAME"
ssh cu_alpine "mkdir -p $RUN_DIR/{inputs,outputs}"
```

---

## SLURM Job Submission

### Job Script Template

```bash
#!/bin/bash
#SBATCH --job-name=my_simulation
#SBATCH --partition=amilan          # CPU partition (or aa100 for GPU)
#SBATCH --nodes=1
#SBATCH --ntasks=32                 # Number of MPI tasks
#SBATCH --time=04:00:00             # Max runtime (HH:MM:SS)
#SBATCH --output=%x_%j.out          # stdout file
#SBATCH --error=%x_%j.err           # stderr file
#SBATCH --mail-type=END,FAIL        # Email notifications
#SBATCH --mail-user=your@email.com

# Load required modules
module purge
module load gcc/13.1.0
module load openmpi/4.1.6

# Change to run directory
cd $SLURM_SUBMIT_DIR

# Run your simulation
mpirun -np $SLURM_NTASKS ./your_program input.in
```

### Key SLURM Commands

| Command | Purpose |
|---------|---------|
| `sbatch job.slurm` | Submit batch job |
| `squeue -u $USER` | Check your job status |
| `squeue -j <jobid>` | Check specific job |
| `scancel <jobid>` | Cancel a job |
| `sinfo -p amilan` | Check partition status |
| `sacct -j <jobid>` | Job accounting info |
| `scontrol show job <jobid>` | Detailed job info |

### Job Status Codes

| Code | Meaning |
|------|---------|
| `PD` | Pending (waiting for resources) |
| `R` | Running |
| `CG` | Completing |
| `CD` | Completed |
| `F` | Failed |
| `TO` | Timeout |
| `CA` | Cancelled |

---

## Available Partitions

### Partition Selection Strategy

**CRITICAL: Always validate on testing partition first before production runs!**

```
Workflow:
1. atesting / atesting_a100  →  Validate job script works (1 hour max)
2. amilan / aa100            →  Production runs (24 hour max)
3. amilan + qos=long         →  Extended runs (7 day max, lower priority)
```

### Testing Partitions (Use First!)

| Partition | Limits | Max Time | Purpose |
|-----------|--------|----------|---------|
| `atesting` | 2 nodes, 16 cores max | 1h | **Validate CPU jobs work before production** |
| `atesting_a100` | 1 GPU, 10 cores max | 1h | **Validate GPU jobs work before production** |
| `atesting_mi100` | 1 GPU, 10 cores max | 1h | Validate AMD GPU jobs |

**Always run a short test on atesting first** to catch:
- Module loading issues
- Path errors
- Input file problems
- Memory requirements

### Production CPU Partitions

| Partition | Nodes | Cores/Node | RAM/Node | Max Time | Use For |
|-----------|-------|------------|----------|----------|---------|
| `amilan` | 387 | 32-64 | 256 GB (3.75 GB/core) | 24h | **Default for production CPU jobs** |
| `amilan128c` | 16 | 128 | 256 GB (2 GB/core) | 24h | **High core count on single node** (see below) |
| `amem` | 24 | 48-128 | up to 2 TB | 24h | Memory-intensive (requires `--qos=mem`, must request 256GB+) |

#### When to Use amilan128c vs amilan

**Use `amilan128c` when:**
- Your job benefits from **128 cores on ONE node** (vs spreading across multiple nodes)
- Running **OpenMP/shared-memory** parallel codes
- High **inter-process communication** (MPI with frequent small messages)
- **Tightly-coupled simulations** where network latency hurts performance
- Large LAMMPS/QE jobs that scale well but suffer from inter-node communication

**Use regular `amilan` when:**
- Your job needs **fewer than 64 cores**
- You need **multiple nodes** (amilan has 387 nodes vs only 16 for 128c)
- Memory per core matters more (3.75 GB/core vs 2 GB/core on 128c)
- Queue wait time is a concern (more nodes = shorter queue)

**Example: 128-core single-node LAMMPS job**
```bash
#SBATCH --partition=amilan128c
#SBATCH --nodes=1
#SBATCH --ntasks=128           # Use all 128 cores
#SBATCH --time=12:00:00
```

### Production GPU Partitions

| Partition | Nodes | GPUs/Node | GPU Type | Max Time | Use For |
|-----------|-------|-----------|----------|----------|---------|
| `aa100` | 11 | 3 | NVIDIA A100 (40GB) | 24h | **Best for CUDA, ML/DL, GPU-accelerated MD** |
| `ami100` | 7 | 3 | AMD MI100 | 24h | ROCm/HIP workloads |
| `al40` | 3 | 3 | NVIDIA L40 | 24h | Newer architecture, visualization |

### Special Partitions

| Partition | Max Time | Purpose |
|-----------|----------|---------|
| `acompile` | 12h | Compiling software only (use via `acompile` command) |
| `csu` | 24h | Colorado State contributed nodes |
| `amc` | 24h | CU Anschutz contributed nodes |

### QoS (Quality of Service)

| QoS | Max Time | Priority | When to Use |
|-----|----------|----------|-------------|
| `normal` | 24h | Normal | **Default - use for most jobs** |
| `long` | 7 days | Lower | Extended simulations (will wait longer in queue) |
| `mem` | 24h | Normal | Required for `amem` partition (high-memory jobs) |

### Partition Selection Examples

```bash
# 1. TESTING: Always start here to validate your job works
#SBATCH --partition=atesting
#SBATCH --time=00:30:00
#SBATCH --ntasks=4

# 2. PRODUCTION CPU: After testing passes
#SBATCH --partition=amilan
#SBATCH --time=04:00:00
#SBATCH --ntasks=32

# 3. PRODUCTION GPU: For GPU-accelerated codes
#SBATCH --partition=aa100
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00

# 4. LONG RUNS: When 24h isn't enough (lower priority)
#SBATCH --partition=amilan
#SBATCH --qos=long
#SBATCH --time=168:00:00   # 7 days

# 5. HIGH MEMORY: For memory-intensive jobs (256GB+ required)
#SBATCH --partition=amem
#SBATCH --qos=mem
#SBATCH --mem=512G
#SBATCH --time=12:00:00
```

---

## Module System

Software is managed through environment modules. **Always work from a compute node or compile node, not login.**

### Essential Commands

```bash
# List available modules
module avail

# Search for specific software
module spider lammps
module spider python

# Load modules
module load gcc/13.1.0
module load openmpi/4.1.6
module load lammps/20230802

# See what's loaded
module list

# Unload all modules
module purge

# Save/restore module sets
module save my_env
module restore my_env
```

### Finding and Loading Software

Software on CURC is installed in `/curc/sw/install/`. To find what's available:

```bash
# List all installed software
ls /curc/sw/install/

# Check specific software versions
ls /curc/sw/install/lammps/    # LAMMPS versions (22July25, 2Sept25, etc.)
ls /curc/sw/install/QE/        # Quantum ESPRESSO (7.0, 7.2)
ls /curc/sw/install/gromacs/   # GROMACS versions
```

**LAMMPS example** (check exact paths for current versions):
```bash
# Find the binary
ls /curc/sw/install/lammps/22July25/gcc/12.2.0/openmpi/4.1.5/bin/

# In job script
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/lammps/22July25/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"
mpirun -np $SLURM_NTASKS lmp -in input.lmp
```

**Quantum ESPRESSO example**:
```bash
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/QE/7.2/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"
mpirun -np $SLURM_NTASKS pw.x < input.in > output.out
```

**Note**: Module dependencies matter. Load compiler first, then MPI. Check exact version paths as they may change.

---

## Storage Filesystem

### Paths and Quotas

| Path | Quota | Purge | Use For |
|------|-------|-------|---------|
| `/home/$USER` | 2 GB | Never | Scripts, small configs |
| `/projects/$USER` | 250 GB | Never | Code, small datasets |
| `/scratch/alpine/$USER` | 10 TB | 90 days | **Job I/O, large files** |
| `$SLURM_SCRATCH` | ~300 GB | Job end | Node-local temp storage |

### Performance Rules

**DO:**
- Run all job I/O on `/scratch/alpine/`
- Use `$SLURM_SCRATCH` for intensive temporary files
- Copy results back after job completes

**DON'T:**
- Run I/O-intensive jobs on `/home` or `/projects` (will be killed)
- Store important data only on `/scratch` (it's purged!)
- Leave large files on login nodes

---

## Example Workflows

### Recommended Workflow: Test First, Then Production

**Step 1: Create a testing job script (job_test.slurm)**
```bash
#!/bin/bash
#SBATCH --job-name=argon_test
#SBATCH --partition=atesting        # <-- TEST PARTITION FIRST
#SBATCH --nodes=1
#SBATCH --ntasks=4                  # Small scale for testing
#SBATCH --time=00:30:00             # 30 min is plenty for testing
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

echo "=== Testing job script ==="
echo "Started at: $(date)"
echo "Running on: $(hostname)"

module purge
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/lammps/22July25/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"

cd $SLURM_SUBMIT_DIR
echo "Working directory: $(pwd)"
echo "Input files: $(ls -la)"

# Run short test (reduce timesteps in input for testing)
mpirun -np $SLURM_NTASKS lmp -in input.lmp

echo "Finished at: $(date)"
```

**Step 2: If test passes, create production job (job_prod.slurm)**
```bash
#!/bin/bash
#SBATCH --job-name=argon_prod
#SBATCH --partition=amilan          # <-- PRODUCTION PARTITION
#SBATCH --nodes=1
#SBATCH --ntasks=32                 # Full scale
#SBATCH --time=04:00:00             # Appropriate for full run
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

module purge
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/lammps/22July25/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"

cd $SLURM_SUBMIT_DIR
mpirun -np $SLURM_NTASKS lmp -in input.lmp
```

### LAMMPS MD Simulation (Full Example)

```bash
#!/bin/bash
#SBATCH --job-name=argon_md
#SBATCH --partition=amilan
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=02:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

module purge
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/lammps/22July25/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"

cd $SLURM_SUBMIT_DIR
mpirun -np $SLURM_NTASKS lmp -in input.lmp
```

### Quantum ESPRESSO DFT

```bash
#!/bin/bash
#SBATCH --job-name=si_scf
#SBATCH --partition=amilan
#SBATCH --nodes=2
#SBATCH --ntasks=64
#SBATCH --time=04:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

module purge
module load gcc/12.2.0 openmpi/4.1.5
export PATH="/curc/sw/install/QE/7.2/gcc/12.2.0/openmpi/4.1.5/bin:$PATH"

cd $SLURM_SUBMIT_DIR
mpirun -np $SLURM_NTASKS pw.x < si_scf.in > si_scf.out
```

### GPU Job (Testing First)

**Test on atesting_a100:**
```bash
#!/bin/bash
#SBATCH --job-name=md_gpu_test
#SBATCH --partition=atesting_a100   # <-- GPU TESTING
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=%x_%j.out

module purge
module load gcc/12.2.0 cuda/12.1.1
# Add LAMMPS GPU path here

cd $SLURM_SUBMIT_DIR
lmp -k on g 1 -sf kk -pk kokkos gpu/aware off -in input.lmp
```

**Then production on aa100:**
```bash
#!/bin/bash
#SBATCH --job-name=md_gpu_prod
#SBATCH --partition=aa100           # <-- GPU PRODUCTION
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:3                # Can use up to 3 GPUs per node
#SBATCH --time=04:00:00
#SBATCH --output=%x_%j.out

module purge
module load gcc/12.2.0 cuda/12.1.1

cd $SLURM_SUBMIT_DIR
lmp -k on g 3 -sf kk -pk kokkos gpu/aware off -in input.lmp
```

---

## Debugging Failed Jobs

When a job fails, investigate systematically:

### 1. Check Job Status

```bash
# See why it failed
sacct -j <jobid> --format=JobID,State,ExitCode,Reason

# Get detailed info
scontrol show job <jobid>
```

### 2. Read Output Files

```bash
# Check stdout
cat my_job_12345.out

# Check stderr (often has the real error)
cat my_job_12345.err

# Check application logs
cat log.lammps
```

### 3. Common Failure Reasons

| Issue | Symptom | Solution |
|-------|---------|----------|
| Timeout | State=TIMEOUT | Increase `--time` or optimize |
| Memory | State=OUT_OF_MEMORY | Increase nodes or use `amem` |
| Module not found | "command not found" | Check `module load` order |
| Bad path | "file not found" | Use absolute paths |
| Wrong partition | Job pending forever | Check partition resources |

### 4. Interactive Debugging

```bash
# Get interactive session for debugging
sinteractive --partition=atesting --time=01:00:00 --ntasks=4

# Then run commands interactively to debug
module load lammps
lmp -in input.lmp  # See errors in real-time
```

---

## File Transfer

### Between Local and HPC

```bash
# Upload input files
scp -r ./inputs/ $CURC_USER@login.rc.colorado.edu:/scratch/alpine/$CURC_USER/agent-workspace/runs/my-run/

# Download results
scp $CURC_USER@login.rc.colorado.edu:/scratch/alpine/$CURC_USER/agent-workspace/runs/my-run/output.dat ./

# Sync directories (rsync is more efficient for updates)
rsync -avz ./project/ $CURC_USER@login.rc.colorado.edu:/scratch/alpine/$CURC_USER/project/
```

### Large File Transfers

For very large files, use Globus (web-based) or DTN nodes:

```bash
# Use data transfer node for large transfers
scp large_file.tar $CURC_USER@dtn.rc.colorado.edu:/scratch/alpine/$CURC_USER/
```

---

## Queue Times and Async Job Management

### Understanding Queue Wait Times

**CRITICAL**: HPC jobs don't start immediately. Queue times vary dramatically:

| Partition | Typical Wait | Why |
|-----------|-------------|-----|
| `atesting` | Minutes | Testing partition, low demand |
| `amilan` | Minutes to hours | Many nodes (387), high throughput |
| `amilan128c` | **Hours to DAYS** | Only 16 nodes, high demand |
| `aa100` | Hours to days | Only 11 nodes, GPU scarcity |

**Before submitting, check the queue:**
```bash
# See pending jobs and estimated start times
ssh cu_alpine "squeue -p amilan128c --start"

# Quick queue depth check
ssh cu_alpine "squeue -p amilan128c --state=PENDING | wc -l"
```

### Async Workflow (For Long Queue Times)

**DON'T** block waiting for jobs with multi-day queues. Instead:

```python
from hpc_client import HPCClient

hpc = HPCClient()
hpc.connect()

# 1. Check queue before choosing partition
status = hpc.get_queue_status('amilan128c')
print(f"Estimated wait: {status['estimated_wait']}")
print(f"Pending jobs: {status['pending_jobs']}")

# 2. Compare partitions to choose wisely
for part in hpc.compare_partitions(['amilan', 'amilan128c', 'aa100']):
    print(f"{part['partition']}: {part['estimated_wait']}, {part['pending_jobs']} pending")

# 3. Submit async (returns immediately, saves tracking file)
tracking = hpc.submit_async(f"{run_dir}/job.slurm")
print(f"Job {tracking['job_id']} submitted")
print(f"Estimated start: {tracking['estimated_start']}")
# Returns immediately - don't wait!

# 4. Later: Check on all submitted jobs
jobs = hpc.check_async_jobs()
for job in jobs:
    print(f"Job {job['job_id']}: {job['current_status']}")
    if job['is_finished']:
        print(f"  Completed! Success: {job['is_success']}")
```

### Workflow Strategy for Long-Running Studies

For multi-day queue scenarios:

```
Day 1: Submit jobs
├── Check queue status
├── Submit with submit_async()
├── Note estimated start times
└── Move on to other work

Day 2+: Check periodically
├── hpc.check_async_jobs()
├── If still PENDING: wait
├── If RUNNING: monitor progress
└── If COMPLETED: download results and analyze
```

### SLURM Email Notifications (Recommended)

Add to your job scripts for automatic notifications:

```bash
#SBATCH --mail-type=BEGIN,END,FAIL    # When to email
#SBATCH --mail-user=your@email.com    # Your email

# Options: NONE, BEGIN, END, FAIL, REQUEUE, ALL
# BEGIN = job started (left queue)
# END = job finished
# FAIL = job failed
```

### Smart Partition Selection

**Decision tree:**

```
Need GPU?
├── YES → Check aa100 queue
│         └── Long wait? Consider if job can run on CPU instead
└── NO → How many cores?
         ├── ≤64 cores → amilan (shorter queue, more nodes)
         └── >64 cores or tightly-coupled →
             └── Check amilan128c queue
                 └── Wait >24h? Consider splitting across amilan nodes
```

### Check Job Progress

```bash
# One-time status check with start time estimates
ssh cu_alpine "squeue -u $CURC_USER --start"

# See job details
ssh cu_alpine "scontrol show job <jobid>"

# Check why job is pending
ssh cu_alpine "squeue -j <jobid> --format='%r'"  # Shows REASON
```

### Wait for Job Completion (Short Jobs Only)

Only use blocking wait for jobs expected to complete within minutes:

```bash
# Poll until job completes (ONLY for short jobs!)
JOB_ID=12345
while ssh cu_alpine "squeue -j $JOB_ID 2>/dev/null | grep -q $JOB_ID"; do
    echo "Job $JOB_ID still running..."
    sleep 60
done
echo "Job $JOB_ID completed"

# Check final status
ssh cu_alpine "sacct -j $JOB_ID --format=JobID,State,ExitCode"
```

---

## Key Principles

### You Are a Researcher

You have the same access a human researcher has. You can:
- Create any job script you need
- Load any available module
- Debug failures by reading logs
- Adapt to different software versions
- Figure out problems through investigation

### Don't Just Execute - Verify

After running on HPC:
1. Check job completed successfully (not just submitted)
2. Verify output files exist and have content
3. Check for error messages in stderr
4. Validate results are physically reasonable

### Document Your Work

Leave breadcrumbs for yourself:
```bash
# In job script
echo "Job started at $(date)"
echo "Running on $(hostname)"
echo "Loaded modules: $(module list 2>&1)"
```

---

## Reference Links

- [CURC Documentation](https://curc.readthedocs.io/en/latest/)
- [Alpine Hardware](https://curc.readthedocs.io/en/latest/clusters/alpine/alpine-hardware.html)
- [SLURM Guide](https://curc.readthedocs.io/en/latest/running-jobs/running-apps-with-jobs.html)
- [Module System](https://curc.readthedocs.io/en/latest/compute/modules.html)
- [Filesystems](https://curc.readthedocs.io/en/latest/compute/filesystems.html)
