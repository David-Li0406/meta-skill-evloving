---
name: create-job
description: >-
  Creates a Siril job file for a target by scanning the data folder structure,
  reading FITS headers for temperature, and finding matching calibration files.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Write
---
# Create Astro Job File

## Instructions

Given a target name (e.g., M45), create a job JSON file by scanning the data folders.

### Step 1: Get Base Path

Read `settings.json` in the project root to get `base_path`.

### Step 2: Scan Target Folders

List date folders for the target:
```bash
ls "{base_path}/{target}"
```

For each date folder, list filter/exposure subfolders:
```bash
ls "{base_path}/{target}/{date}"
```

Filter folders are named `{filter}{exposure}` (e.g., `L180`, `R300`, `Ha180`, `S180`).

### Step 3: Read FITS Temperature

Read the sensor temperature from a FITS file header. Pick any `.fit` or `.fits` file from a light folder:

```bash
ls "{base_path}/{target}/{date}/{filter_folder}"
```

Then read the temperature:
```bash
uv run python -c "from astropy.io import fits; h=fits.getheader(r'{path_to_fit_file}'); print(h.get('CCD-TEMP') or h.get('SET-TEMP'))"
```

Round to nearest integer (e.g., -9.8 -> -10).

### Step 4: Find Calibration Files

List available calibration dates:
```bash
ls "{base_path}/calibration/raw/biases"
ls "{base_path}/calibration/raw/darks"
ls "{base_path}/calibration/raw/flats"
```

Dark folders include temperature in the name: `{YYYY_MM_DD}_{temp}C` (e.g., `2025_01_23_-10C`).

Calibration matching:
- Bias: use most recent date
- Darks: find folders matching the light temperature, use most recent
- Flats: use most recent date

If no darks exist at the target temperature, use the closest available and set `dark_temp_override` in options. Otherwise, do not set `dark_temp_override`.

### Step 5: Determine Job Type

Based on filters found:
- Has L (with or without R,G,B, Ha, etc.) -> `LRGB`
- R, G, B only (no L) -> `RGB`
- S, H, O (narrowband only) -> `SHO`
- H, O only -> `HOO`

### Step 6: Generate Job Name

Format: `{target}_{season}{year}`

Determine season from the most recent light date:
- Dec, Jan, Feb -> Winter
- Mar, Apr, May -> Spring
- Jun, Jul, Aug -> Summer
- Sep, Oct, Nov -> Fall

Use the year of the most recent session.

### Step 7: Write Job File

Write to `jobs/{target}.json`.

## Template

```json
{
  "name": "{target}_{season}{year}",
  "type": "LRGB",
  "calibration": {
    "bias": "2024_08_05",
    "darks": "2025_01_23",
    "flats": "2025_01_19"
  },
  "lights": {
    "L": [
      "{target}/{date1}/L180",
      "{target}/{date2}/L180"
    ],
    "R": [
      "{target}/{date1}/R180",
      "{target}/{date2}/R180"
    ],
    "G": [
      "{target}/{date1}/G180",
      "{target}/{date2}/G180"
    ],
    "B": [
      "{target}/{date1}/B180",
      "{target}/{date2}/B180"
    ]
  },
  "output": "{target}/processed",
  "options": {}
}
```

## Examples

LRGB job (M31):
- Filters: L, R, G, B across multiple nights
- Type: `LRGB`

Narrowband job (IC443):
- Filters: S, H, O
- Type: `SHO`
- Options include `"palette": "SHO"`

LRGB + Ha:
- Filters: L, R, G, B, Ha
- Type: `LRGB`
- Include `Ha` key in lights alongside L, R, G, B

## Step 8: Run Job and Monitor

Run the job:
```bash
uv run python run_job.py jobs/{target}.json
```

Other run options:
```bash
uv run python run_job.py jobs/{target}.json --validate  # Validate only
uv run python run_job.py jobs/{target}.json --dry-run   # Dry run
uv run python run_job.py jobs/{target}.json --stage preprocess  # Run specific stage
```

Monitor the log file in `logs/{target}_{timestamp}.log` for:
- Calibration file matching issues
- Frame rejection (FWHM filtering)
- Stacking errors
- Any warnings or failures

After the job completes, review the log output and report any issues to the user.
