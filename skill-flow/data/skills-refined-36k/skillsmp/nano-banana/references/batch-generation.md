# Batch Generation Reference

Complete workflow and reference for generating 5+ slides efficiently with minimal context consumption.

---

## Overview

### When to Use

**Automatic activation:** 5+ slides detected
- **Benefits:** 80% context reduction (1,800 → 390 tokens for 10 slides)
- **Trade-off:** Less immediate feedback (progress shown periodically)
- **Best for:** Large slide decks, long presentations

**Use direct execution for 1-4 slides:**
- Immediate feedback per slide
- Simpler workflow
- Better for small sets

---

## Complete Workflow

### Step 1: Create Configuration File

Create a JSON configuration file with all slide specifications:

```python
import json
from pathlib import Path

# Example: 10-slide CI/CD presentation
config = {
    "slides": [
        {"number": 1, "prompt": "CI/CD pipeline overview diagram", "style": "professional"},
        {"number": 2, "prompt": "Version control and branching strategy", "style": "data-viz"},
        {"number": 3, "prompt": "Build automation workflow", "style": "professional"},
        {"number": 4, "prompt": "Testing pyramid with unit, integration, e2e", "style": "data-viz"},
        {"number": 5, "prompt": "Containerization with Docker", "style": "professional"},
        {"number": 6, "prompt": "Kubernetes deployment architecture", "style": "data-viz"},
        {"number": 7, "prompt": "Monitoring and observability stack", "style": "professional"},
        {"number": 8, "prompt": "Security scanning and compliance", "style": "data-viz"},
        {"number": 9, "prompt": "Performance metrics dashboard", "style": "data-viz"},
        {"number": 10, "prompt": "Best practices and next steps", "style": "professional"}
    ],
    "output_dir": "/home/user/presentations/001-cicd-deck/",
    # NOTE: Don't specify "model" here - let the script use NANO_BANANA_MODEL env var
    # This matches nano-banana's standard pattern
    "format": "webp",
    "quality": 90
}

# Write config to temp file (cross-platform)
import tempfile
config_path = Path(tempfile.gettempdir()) / "nano-banana-config.json"
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"Configuration saved to: {config_path}")
```

**Configuration Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slides` | Array | Yes | Array of slide objects |
| `slides[].number` | Integer | Yes | Slide number (for naming) |
| `slides[].prompt` | String | Yes | Image generation prompt |
| `slides[].style` | String | No | Style preset: `professional`, `data-viz`, `infographic` |
| `output_dir` | String | Yes | Directory path for generated slides |
| `model` | String | No | Model name (default: `gemini-3-pro-image-preview`) |
| `format` | String | No | Output format: `webp`, `png`, `jpeg` (default: `webp`) |
| `quality` | Integer | No | Image quality 1-100 (default: 90) |

---

### Step 2: Start Background Task

Use `Bash` tool with `run_in_background=True` to start batch generation:

```python
# CRITICAL: Must use 'uv run' not plain 'python'
# The script dependencies are managed by uv via PEP 723 inline metadata
# {base_dir} is the skill base directory provided by Claude Code

task_result = Bash(
    command="uv run {base_dir}/generate_images.py --config {config_path}",
    run_in_background=True,
    description="Generate 10 slides in batch mode"
)

# Notify user
print("🚀 Started batch generation for 10 slides...")
print("Progress updates will appear every 10-15 seconds.")
```

**IMPORTANT - Common Mistakes:**

❌ **WRONG - Will fail with import errors:**

```python
Bash(
    command="python generate_images.py --config {config_path}",
    run_in_background=True
)
```

❌ **WRONG - Missing full path:**

```python
Bash(
    command="uv run generate_images.py --config {config_path}",
    run_in_background=True
)
```

❌ **WRONG - Changes directory (breaks relative paths in config):**

```python
Bash(
    command="cd {base_dir} && uv run generate_images.py --config {config_path}",
    run_in_background=True
)
```

This makes `Path.cwd()` return the plugin cache directory, causing `./001-slides/` to resolve to the wrong location.

✅ **CORRECT:**

```python
Bash(
    command="uv run {base_dir}/generate_images.py --config {config_path}",
    run_in_background=True
)
```

**Key Points:**
- `{base_dir}` is the skill base directory provided by Claude Code when loading the skill
- Use absolute path to script WITHOUT `cd` command
- This keeps execution cwd in user's project directory, so relative paths in config work correctly

---

### Step 3: Poll Progress File

Poll progress file in system temp directory every 10-15 seconds to show user progress:

```python
import time
import json
from pathlib import Path

progress_file = Path(tempfile.gettempdir()) / "nano-banana-progress.json"

# Poll loop (Claude handles this automatically)
while True:
    time.sleep(12)  # Poll every 10-15 seconds

    try:
        if not progress_file.exists():
            # Task just started, progress file not created yet
            continue

        with open(progress_file, 'r') as f:
            progress = json.load(f)

        current = progress['current']
        total = progress['total']
        percentage = int((current / total) * 100)

        # Update user
        print(f"Progress: {current}/{total} slides completed ({percentage}%)")

        # Check if complete
        if current >= total:
            print("✓ All slides generated!")
            break

    except Exception as e:
        # Handle transient read errors (file being written)
        continue
```

**Progress File Schema:**

```json
{
  "current": 3,
  "total": 10,
  "status": "generating slide 3...",
  "completed": [
    "/home/user/presentations/001-cicd-deck/slide-01.webp",
    "/home/user/presentations/001-cicd-deck/slide-02.webp",
    "/home/user/presentations/001-cicd-deck/slide-03.webp"
  ],
  "failed": [],
  "started_at": "2026-01-16T10:30:00Z",
  "updated_at": "2026-01-16T10:30:45Z"
}
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `current` | Integer | Number of slides processed so far |
| `total` | Integer | Total slides to generate |
| `status` | String | Current status message |
| `completed` | Array | Paths to successfully generated slides |
| `failed` | Array | Slide numbers that failed |
| `started_at` | String | ISO timestamp when batch started |
| `updated_at` | String | ISO timestamp of last update |

---

### Step 4: Read Results File

When complete (`current == total`), read results file in system temp directory:

```python
import json
from pathlib import Path

results_file = Path(tempfile.gettempdir()) / "nano-banana-results.json"

with open(results_file, 'r') as f:
    results = json.load(f)

# Report to user
completed = results['completed']
failed = results['failed']
total = results['total']
duration = results['duration_seconds']

print(f"\n{'='*60}")
print(f"Batch generation completed in {duration}s")
print(f"{'='*60}")
print(f"✓ Completed: {completed}/{total} slides")

if failed > 0:
    print(f"⚠ Failed: {failed}/{total} slides")
    print("\nErrors:")
    for err in results['errors']:
        print(f"  Slide {err['slide']}: {err['error']}")

print(f"\nOutput directory: {results['outputs'][0]['path'].rsplit('/', 1)[0]}/")
print("\nGenerated slides:")
for output in results['outputs']:
    size = output['size_kb']
    print(f"  slide-{output['slide']:02d}.webp ({size} KB)")
```

**Results File Schema:**

```json
{
  "completed": 8,
  "failed": 2,
  "total": 10,
  "outputs": [
    {"slide": 1, "path": "/path/slide-01.webp", "size_kb": 245},
    {"slide": 2, "path": "/path/slide-02.webp", "size_kb": 312},
    {"slide": 4, "path": "/path/slide-04.webp", "size_kb": 289},
    {"slide": 5, "path": "/path/slide-05.webp", "size_kb": 301}
  ],
  "errors": [
    {
      "slide": 3,
      "error": "API rate limit exceeded",
      "timestamp": "2026-01-16T10:31:15Z"
    },
    {
      "slide": 7,
      "error": "Invalid prompt format",
      "timestamp": "2026-01-16T10:32:03Z"
    }
  ],
  "started_at": "2026-01-16T10:30:00Z",
  "completed_at": "2026-01-16T10:32:30Z",
  "duration_seconds": 150
}
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `completed` | Integer | Number of successfully generated slides |
| `failed` | Integer | Number of failed slides |
| `total` | Integer | Total slides attempted |
| `outputs` | Array | Array of output info objects |
| `outputs[].slide` | Integer | Slide number |
| `outputs[].path` | String | Full path to generated file |
| `outputs[].size_kb` | Integer | File size in kilobytes |
| `errors` | Array | Array of error info objects |
| `errors[].slide` | Integer | Failed slide number |
| `errors[].error` | String | Error message |
| `errors[].timestamp` | String | ISO timestamp of failure |
| `started_at` | String | ISO timestamp when batch started |
| `completed_at` | String | ISO timestamp when batch finished |
| `duration_seconds` | Integer | Total duration in seconds |

---

## Error Handling

### Continue on Failure

The batch script continues processing remaining slides when individual slides fail:

**Scenario: Slide 3 fails with API error**
- Slides 1-2: ✓ Completed
- Slide 3: ✗ Failed (logged in errors array)
- Slides 4-10: ✓ Continue processing

### Exit Codes

| Exit Code | Meaning | Results |
|-----------|---------|---------|
| 0 | Success | At least some slides completed |
| 1 | Total failure | All slides failed or fatal error |

### Common Errors

**1. API Rate Limit**

```json
{
  "error": "API rate limit exceeded",
  "slide": 5
}
```

**Solution:** Wait for rate limit reset, retry failed slides

**2. Invalid Configuration**

```json
{
  "error": "Config must contain 'slides' array"
}
```

**Solution:** Fix configuration JSON format, retry entire batch

**3. File I/O Error**

```json
{
  "error": "Cannot create output directory: Permission denied"
}
```

**Solution:** Check directory permissions, use writable path

**4. Missing API Key**

```
Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set
```

**Solution:** Set `GEMINI_API_KEY` environment variable

---

## Style Presets

The `style` field in slide configuration applies prompt enhancements:

### professional

```json
{"number": 1, "prompt": "CI/CD pipeline overview", "style": "professional"}
```

- Enhanced prompt: "Professional presentation slide: CI/CD pipeline overview. Clean, minimal design with clear typography."
- Uses lossless WebP (for crisp text)

### data-viz

```json
{"number": 2, "prompt": "Testing pyramid metrics", "style": "data-viz"}
```

- Enhanced prompt: "Data visualization slide: Testing pyramid metrics. Clear charts and graphs, professional color scheme."
- Uses lossless WebP (for sharp diagrams)

### infographic

```json
{"number": 3, "prompt": "DevOps workflow", "style": "infographic"}
```

- Enhanced prompt: "Infographic style: DevOps workflow. Visual storytelling with icons and illustrations."
- Uses lossless WebP (for detailed graphics)

### No style (default)

```json
{"number": 4, "prompt": "Kubernetes architecture"}
```

- Prompt used as-is
- Uses lossy WebP (smaller file size)

---

## Performance Characteristics

### Context Consumption

| Slides | Direct Execution | Batch Mode | Savings |
|--------|------------------|------------|---------|
| 5 slides | ~900 tokens | ~320 tokens | 64% |
| 10 slides | ~1,800 tokens | ~390 tokens | 78% |
| 20 slides | ~3,600 tokens | ~520 tokens | 86% |

**Batch mode breakdown (10 slides):**
- Config creation: ~50 tokens
- Start background task: ~20 tokens
- Progress polls (3-6x): ~120-240 tokens
- Final results: ~250 tokens
- **Total: ~390 tokens**

### Generation Time

- Sequential generation: ~10-15s per slide
- 10 slides: ~100-150s total duration
- Progress updates: Every 10-15s during generation

---

## Troubleshooting

### Problem: Progress file not updating

**Symptoms:**
- Progress file created but not changing
- `current` value stuck

**Possible causes:**
1. Script crashed (check background task)
2. API errors (check results file)
3. Long generation time (wait longer)

**Solution:**

```python
# Check if background task is still running
# If task finished, read results file for errors
```

### Problem: "Module not found" error

**Symptoms:**

```
ModuleNotFoundError: No module named 'google.genai'
```

**Cause:** Used `python` instead of `uv run`

**Solution:** Always use `uv run generate_images.py`

### Problem: Permission denied on progress/results file

**Symptoms:**

```
PermissionError: [Errno 13] Permission denied: '<temp_dir>/nano-banana-progress.json'
```

**Solution:** Check system temp directory permissions (should be writable). On Linux/macOS: `/tmp/`, on Windows: `%TEMP%`

---

## Complete Example: 5-Slide Generation

Full working example generating 5 slides:

```python
import json
from pathlib import Path

# Step 1: Create configuration
config = {
    "slides": [
        {"number": 1, "prompt": "Docker containerization basics", "style": "professional"},
        {"number": 2, "prompt": "Container layers and image building", "style": "data-viz"},
        {"number": 3, "prompt": "Docker Compose multi-container setup", "style": "professional"},
        {"number": 4, "prompt": "Container orchestration comparison", "style": "data-viz"},
        {"number": 5, "prompt": "Best practices for production", "style": "professional"}
    ],
    "output_dir": "./002-docker-basics/",
    "format": "webp",
    "quality": 90
}

# Use cross-platform temp directory
import tempfile
config_path = Path(tempfile.gettempdir()) / "nano-banana-config.json"
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

# Step 2: Start background task
print("🚀 Starting batch generation for 5 slides...")
# Use Bash tool with run_in_background=True
# Command: uv run /path/to/generate_images.py --config {config_path}

# Step 3: Poll progress (Claude handles automatically)
# Read progress file from temp directory every 10-15s

# Step 4: Read results when complete
# Read results file from temp directory
# Report completion status to user
```

**Expected output:**

```
🚀 Starting batch generation for 5 slides...
Progress: 2/5 slides completed (40%)
Progress: 4/5 slides completed (80%)
✓ All slides generated!

============================================================
Batch generation completed in 65s
============================================================
✓ Completed: 5/5 slides

Output directory: ./002-docker-basics/

Generated slides:
  slide-01.webp (287 KB)
  slide-02.webp (312 KB)
  slide-03.webp (294 KB)
  slide-04.webp (305 KB)
  slide-05.webp (289 KB)
```

---

## Related Documentation

- **SKILL.md**: Quick reference and mode selection rules
- **gemini-api.md**: Gemini API details for direct generation
- **imagen-api.md**: Imagen API details for direct generation
- **slide-deck-styles.md**: Style specifications and design guidelines
