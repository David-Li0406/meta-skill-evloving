---
name: data-analysis
description: Analyze simulation data and compute properties. Use when asked to parse LAMMPS/QE output, calculate diffusion coefficients, RDF, MSD, energies, or generate plots and visualizations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Simulation Data Analysis

You are analyzing computational materials science simulation data.

## ML Environment

For Python-based analysis, use the blackwell-ml conda environment:

```bash
conda run -n blackwell-ml python script.py
# Or interactively:
conda activate blackwell-ml
```

Available packages: numpy, scipy, pandas, matplotlib, pytorch, cupy

## LAMMPS Output Analysis

### Log File Parsing

LAMMPS log files contain thermodynamic data in tabular format:

```python
import numpy as np
import pandas as pd

def parse_lammps_log(logfile):
    """Parse LAMMPS log file for thermodynamic data."""
    data = []
    in_run = False
    headers = None

    with open(logfile, 'r') as f:
        for line in f:
            if line.startswith('Step'):
                headers = line.split()
                in_run = True
                continue
            if in_run:
                if line.startswith('Loop'):
                    in_run = False
                    continue
                try:
                    values = [float(x) for x in line.split()]
                    if len(values) == len(headers):
                        data.append(values)
                except ValueError:
                    in_run = False

    return pd.DataFrame(data, columns=headers)

# Usage
df = parse_lammps_log('log.lammps')
print(df[['Step', 'Temp', 'PotEng', 'TotEng']].describe())
```

### Trajectory Analysis

For LAMMPS dump files (.lammpstrj):

```python
def read_lammpstrj(filename):
    """Read LAMMPS trajectory file."""
    frames = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if 'ITEM: TIMESTEP' in line:
                timestep = int(f.readline())
                f.readline()  # ITEM: NUMBER OF ATOMS
                natoms = int(f.readline())
                f.readline()  # ITEM: BOX BOUNDS
                box = []
                for _ in range(3):
                    box.append([float(x) for x in f.readline().split()])
                f.readline()  # ITEM: ATOMS
                atoms = []
                for _ in range(natoms):
                    atoms.append(f.readline().split())
                frames.append({
                    'timestep': timestep,
                    'natoms': natoms,
                    'box': box,
                    'atoms': atoms
                })
    return frames
```

### Mean Square Displacement (MSD)

```python
def compute_msd(positions, timesteps):
    """Compute MSD from trajectory positions."""
    n_frames = len(positions)
    n_atoms = len(positions[0])

    msd = np.zeros(n_frames)
    for t in range(n_frames):
        disp = positions[t] - positions[0]
        msd[t] = np.mean(np.sum(disp**2, axis=1))

    return timesteps, msd

# Diffusion coefficient from MSD slope
# D = slope / (2 * dimensions)
# For 3D: D = slope / 6
```

### Radial Distribution Function (RDF)

```python
def compute_rdf(positions, box, n_bins=100, r_max=None):
    """Compute radial distribution function."""
    if r_max is None:
        r_max = min(box) / 2

    dr = r_max / n_bins
    hist = np.zeros(n_bins)
    n_atoms = len(positions)

    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            r_vec = positions[j] - positions[i]
            # Apply minimum image convention
            r_vec = r_vec - box * np.round(r_vec / box)
            r = np.linalg.norm(r_vec)
            if r < r_max:
                bin_idx = int(r / dr)
                hist[bin_idx] += 2

    # Normalize
    r = np.linspace(dr/2, r_max - dr/2, n_bins)
    volume = np.prod(box)
    rho = n_atoms / volume

    for i in range(n_bins):
        shell_volume = 4/3 * np.pi * ((r[i]+dr/2)**3 - (r[i]-dr/2)**3)
        hist[i] /= (n_atoms * shell_volume * rho)

    return r, hist
```

## Quantum ESPRESSO Output Analysis

### Energy Extraction

```bash
# Total energy
grep "!" output.out | tail -1

# Forces
grep -A 100 "Forces acting on atoms" output.out | head -20

# Stress tensor
grep -A 10 "total   stress" output.out
```

### Band Structure Analysis

```python
def parse_bands(bands_file):
    """Parse QE bands.dat file."""
    with open(bands_file, 'r') as f:
        header = f.readline()  # nbnd, nks
        nbnd, nks = map(int, header.split()[:2])

        kpoints = []
        bands = np.zeros((nks, nbnd))

        for ik in range(nks):
            kline = f.readline()
            kpoints.append([float(x) for x in kline.split()])

            energies = []
            while len(energies) < nbnd:
                line = f.readline()
                energies.extend([float(x) for x in line.split()])
            bands[ik, :] = energies

    return np.array(kpoints), bands
```

### DOS Analysis

```python
def parse_dos(dos_file):
    """Parse QE DOS output."""
    data = np.loadtxt(dos_file, skiprows=1)
    energy = data[:, 0]
    dos = data[:, 1]
    integrated_dos = data[:, 2] if data.shape[1] > 2 else None
    return energy, dos, integrated_dos
```

## Visualization

### Basic Plotting

```python
import matplotlib.pyplot as plt

def plot_energy_time(df):
    """Plot energy vs time from LAMMPS log."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Step'], df['TotEng'], label='Total Energy')
    ax.plot(df['Step'], df['PotEng'], label='Potential Energy')
    ax.set_xlabel('Timestep')
    ax.set_ylabel('Energy (kcal/mol)')
    ax.legend()
    plt.savefig('energy_vs_time.png', dpi=150)
    return fig

def plot_rdf(r, g_r):
    """Plot radial distribution function."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(r, g_r)
    ax.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax.set_xlabel('r (Angstrom)')
    ax.set_ylabel('g(r)')
    ax.set_title('Radial Distribution Function')
    plt.savefig('rdf.png', dpi=150)
    return fig
```

### Band Structure Plot

```python
def plot_bands(kpoints, bands, fermi_energy=0):
    """Plot electronic band structure."""
    fig, ax = plt.subplots(figsize=(8, 10))

    k_dist = [0]
    for i in range(1, len(kpoints)):
        dk = np.linalg.norm(kpoints[i][:3] - kpoints[i-1][:3])
        k_dist.append(k_dist[-1] + dk)

    for band in range(bands.shape[1]):
        ax.plot(k_dist, bands[:, band] - fermi_energy, 'b-', lw=0.5)

    ax.axhline(y=0, color='k', linestyle='--')
    ax.set_xlabel('k')
    ax.set_ylabel('E - E_F (eV)')
    ax.set_title('Electronic Band Structure')
    plt.savefig('bands.png', dpi=150)
    return fig
```

## Property Calculations

### Diffusion Coefficient

```python
def diffusion_from_msd(time, msd, fit_start=0.2, fit_end=0.8):
    """Calculate diffusion coefficient from MSD."""
    n = len(time)
    i_start = int(n * fit_start)
    i_end = int(n * fit_end)

    # Linear fit in the diffusive regime
    coeffs = np.polyfit(time[i_start:i_end], msd[i_start:i_end], 1)
    slope = coeffs[0]

    # D = slope / (2 * d) where d is dimensionality
    D = slope / 6  # 3D

    return D
```

### Thermal Conductivity (Green-Kubo)

```python
def thermal_conductivity_gk(heat_flux, volume, temperature, dt, max_lag=None):
    """Compute thermal conductivity via Green-Kubo."""
    kb = 1.380649e-23  # J/K

    if max_lag is None:
        max_lag = len(heat_flux) // 2

    # Autocorrelation function
    acf = np.correlate(heat_flux, heat_flux, mode='full')
    acf = acf[len(acf)//2:len(acf)//2 + max_lag]
    acf /= np.arange(len(heat_flux), len(heat_flux) - max_lag, -1)

    # Integrate
    kappa = volume / (kb * temperature**2) * np.trapz(acf, dx=dt)

    return kappa
```

## Output Organization

Save analysis results to:
```
workspaces/project-name/analysis/
├── scripts/
│   └── analyze_trajectory.py
├── data/
│   ├── energy_data.csv
│   ├── rdf_data.csv
│   └── msd_data.csv
├── figures/
│   ├── energy_vs_time.png
│   ├── rdf.png
│   └── msd.png
└── results.md  # Summary of findings
```

## Common Analysis Tasks

1. **Equilibration Check**
   - Plot energy vs time
   - Check for drift/instability
   - Verify temperature/pressure stability

2. **Structural Analysis**
   - RDF for local structure
   - Coordination numbers
   - Density profiles

3. **Dynamic Properties**
   - MSD for diffusion
   - Velocity autocorrelation
   - Vibrational spectra

4. **Electronic Structure**
   - Band gaps
   - DOS features
   - Charge density analysis

## Analysis Methodology

### Before Implementing Analysis

1. **Know what you're measuring** - What property? What units? What's the expected range?
2. **Research the method if unfamiliar** - Search "[property] calculation python" or check library docs (MDAnalysis, pymatgen have tutorials)
3. **Understand the physics** - Why does this method work? What assumptions does it make?

### Validation

Before trusting your results:
- **Test on known systems** - Does your MSD analysis give correct D for a well-characterized liquid?
- **Check literature values** - Is your result within the expected range?
- **Verify convergence** - Enough data points? Proper equilibration excluded?

### When Results Seem Wrong

If your analysis gives unexpected values:
1. **Check your implementation** - Units? Array indexing? Time conversion?
2. **Check the input data** - Was the simulation equilibrated? Correct format?
3. **Research alternative methods** - Maybe a different approach is more appropriate
4. **Iterate** - Fix and re-run until results match physical expectations

**Do not accept results you know are wrong.** A diffusion coefficient 100x off from literature means your analysis is flawed, not that you've discovered new physics. See CLAUDE.md "When Something Seems Wrong" for full guidance.
