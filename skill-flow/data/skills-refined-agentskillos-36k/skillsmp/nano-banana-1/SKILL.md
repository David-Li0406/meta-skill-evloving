---
name: Nano-Banana
description: Generate PPT slide images from JSON slide outlines using Gemini Image Generation API (gemini-3-pro-image-preview). Use when creating presentation slides from JSON, generating slide images in batch, or converting slide outlines to visual slides.
allowed-tools: Read, Bash, Glob
version: 4.0.0
updated: 2026-01-23
status: active
---

# Nano-Banana PPT Slide Image Generator

Generate high-quality PPT slide images from JSON slide outlines using the Gemini Image Generation API (Nano Banana Pro - gemini-3-pro-image-preview).

---

## Quick Reference (30 seconds)

**Purpose**: Generate PPT slide images from JSON outlines containing Nano-Banana optimized prompts.

**Execution Commands**:
```bash
# Generate empty template image (for consistent header/footer)
uv run python "{skill_scripts_dir}/Generate_Template.py" "{json_file}"

# Generate all slides (auto-detects template.png in JSON directory)
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}"

# Generate with explicit template image
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}" --template "{template_path}"

# Generate specific slides only (for recovery/retry)
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}" --slides 5
uv run python "{skill_scripts_dir}/Generate_Slides.py" "{json_file}" --output-dir "{output_dir}" --slides 5,7,9
```

**Script Location**:
`.claude/skills/Nano-Banana/Scripts/Generate_Slides.py`
`.claude/skills/Nano-Banana/Scripts/Generate_Template.py`

**Prerequisites**:
- Python dependencies: `google-genai`, `python-dotenv`, `pillow`
- API Key: `.claude/skills/Nano-Banana/Scripts/.env` with `GOOGLE_API_KEYS=key1,key2` or `GOOGLE_API_KEY=your_key`

**Output**: PNG images saved as `slide_001.png`, `slide_002.png`, etc.

---

## Implementation Guide (5 minutes)

### Basic Usage

**Step 1**: Ensure prerequisites are installed
```bash
pip install google-genai python-dotenv pillow
```

**Step 2**: Create `.env` file in skill Scripts directory
```bash
# Create at: .claude/skills/Nano-Banana/Scripts/.env
# Single key
GOOGLE_API_KEY=your_google_api_key_here
# Or multiple keys for rotation (recommended)
GOOGLE_API_KEYS=key1,key2,key3
```

**Step 3**: Generate template (optional, for consistent header/footer)
```bash
# Generate empty template image from design_system
uv run python "/path/to/Generate_Template.py" "slides.json"
uv run python "/path/to/Generate_Template.py" "slides.json" --output "./template.png"
```

**Step 4**: Execute slide generation
```bash
# Basic execution (output: {json_name}_images/)
# Auto-detects template.png in JSON directory if exists
uv run python "/path/to/Generate_Slides.py" "slides.json"

# With custom output directory
uv run python "/path/to/Generate_Slides.py" "slides.json" --output-dir "./output"

# With explicit template image
uv run python "/path/to/Generate_Slides.py" "slides.json" --template "./template.png"

# With custom .env file path
uv run python "/path/to/Generate_Slides.py" "slides.json" --env-file "/path/to/.env"

# Generate specific slides only (for recovery/retry)
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 5           # Single slide
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 5,7,9       # Multiple slides
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 1-5         # Range
uv run python "/path/to/Generate_Slides.py" "slides.json" --slides 1-3,5,7-9   # Mixed
```

### Input JSON Schema (v12.0)

The script expects a JSON file with the following structure. **Key Change**: nano_banana_prompt contains ONLY slide content. Design system is auto-prepended by the script.

```json
{
  "source_file": "/path/to/source.md",
  "created_at": "2024-12-05T14:30:22",
  "total_slides": 10,
  "theme": "economic_policy_critical",
  "target_audience": "general",
  "reference_images": ["/path/to/global_ref.png"],
  "style_guide": {
    "slide_prefix": "Create a professional presentation slide image",
    "layer4_specs": "16:9 aspect ratio, 1920x1080 resolution. All Korean text clearly readable.",
    "design_system": {
      "color_palette": {
        "background": "#1A1A1A dark charcoal with subtle grain",
        "text": "#FFFFFF white",
        "accent_primary": "#C41E3A crimson",
        "accent_secondary": "#4A90D9 steel blue",
        "sub": "#2D2D2D dark gray for cards"
      },
      "typography": {
        "headings": "Bold sans-serif, 30-40% slide width",
        "body": "Light sans-serif, high readability"
      },
      "layout": {
        "header": "Top 8% - left-aligned section title, sub color background, thin accent_primary line below",
        "content": "Middle 84%",
        "footer": "Bottom 8% - right-aligned page number, sub color background, thin accent_primary line above"
      },
      "mood": "Serious documentary with data-driven urgency",
      "illustration": "Visual metaphors, infographic elements"
    }
  },
  "slides": [
    {
      "page": 1,
      "title": "Slide Title",
      "key_message": "Reading Deck detailed explanation (2-4 sentences)",
      "nano_banana_prompt": "Header: '01. 서론'. Title: '제목'. Content area: [visual elements]. Footer: '발표제목 | 1/10'.",
      "reference_images": ["/path/to/slide_specific_ref.png"]
    }
  ]
}
```

**Top-Level Field Descriptions**:
- `source_file`: Original source file path
- `theme`: Dynamically generated descriptive theme name based on content analysis
- `reference_images`: (Optional) Global reference images applied to ALL slides
- `style_guide`: Design system for visual consistency. Contains:
  - `slide_prefix`: Opening phrase (auto-prepended to all prompts)
  - `layer4_specs`: Technical specifications (auto-prepended)
  - `design_system`: Visual design specification (auto-prepended as context)
    - `color_palette`: 5-color scheme (background, text, accent_primary, accent_secondary, sub)
    - `typography`: headings and body text styling
    - `layout`: header (8%), content (84%), footer (8%) zones
    - `mood`: overall visual atmosphere
    - `illustration`: guidance for visual elements

**Slide Field Descriptions**:
- `page`: Slide number (starts from 1)
- `title`: Slide title (Korean, max 10 words)
- `key_message`: Reading Deck detailed explanation (Korean, 2-4 sentences)
- `nano_banana_prompt`: **Content only** - title, text, visual elements (NO placeholders, NO style info)
- `reference_images`: (Optional) Slide-specific reference images (combined with global references)

### How Prompts Are Built (v12.0)

The script automatically prepends `style_guide` context to each `nano_banana_prompt`:

1. **slide_prefix** is prepended first
2. **design_system** (colors, typography, layout, mood, illustration) is added as context
3. **layer4_specs** (technical requirements) is added
4. **nano_banana_prompt** (slide content) follows

This means `nano_banana_prompt` should contain ONLY:
- Header text (section info)
- Title text
- Content area description (visual elements, data)
- Footer text (presentation title, page number)
- All Korean text in quotes for exact rendering

### Script Configuration

Configurable constants in `Generate_Slides.py`:

```python
MODEL = "gemini-3-pro-image-preview"  # Gemini model
ASPECT_RATIO = "16:9"                  # Image aspect ratio
IMAGE_SIZE = "2K"                      # Image resolution
MAX_RETRIES = 10                       # Maximum retry attempts per slide
RETRY_DELAY_SECONDS = 5                # Delay for quota/rate limit errors
EMPTY_RESPONSE_RETRIES = 5             # Max retries for empty responses
MAX_WORKERS = 20                       # Maximum parallel threads per batch
BATCH_SIZE = 20                        # Slides processed per batch
BATCH_DELAY_SECONDS = 30               # Wait between batches (API rate limit)
```

Configurable constants in `Generate_Template.py`:

```python
MODEL = "gemini-3-pro-image-preview"
ASPECT_RATIO = "16:9"
IMAGE_SIZE = "2K"
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 5
```

### Output Example

**Generate_Template.py Output:**
```
============================================================
Template Generation
============================================================
Input: Plan_example.json
Output: /path/to/template.png
Model: gemini-3-pro-image-preview

Design System:
  Background: #FFFFFF white
  Accent: #B8282E crimson
  Sub (bars): #F3F4F6 light gray

Layout:
  Header: Top 8% - left-aligned section title...
  Footer: Bottom 8% - right-aligned page number...
============================================================

Starting template generation...
  [Attempt 1/5] Generating template image...

============================================================
Template Generated Successfully!
============================================================
Saved to: /path/to/template.png
============================================================
```

**Generate_Slides.py Output:**
```
[Auto-detect] Found template image: /path/to/template.png
[API Keys] Loaded 2 API key(s) for rotation
[Thread-Safe] Using thread-local clients for parallel processing
[Style Guide] Using custom style_guide from JSON
[Template] Using template image: /path/to/template.png
[Global Reference] Found 1 global reference image(s)

============================================================
Starting BATCHED PARALLEL image generation
Total slides: 22
Batch size: 20
Total batches: 2
Batch delay: 30 seconds
Output directory: slides_images
Model: gemini-3-pro-image-preview
Max workers: 20
Max retries: 10
Retry delay: 5 seconds
============================================================

============================================================
BATCH 1/2: Processing 20 slides
============================================================

[Slide 01/22] Title Slide (refs: 1) - Starting...
  [Reference Image] Loaded: template.png
  [Attempt 1/10] Generating image with 1 reference(s)...
[Slide 01] Success - Saved to slide_001.png
...

[Batch 1] Completed in 45.2 seconds
[Batch 1] Success: 20, Failed: 0

[Wait] Pausing 30 seconds before next batch...

============================================================
Generation Complete!
============================================================
Total slides processed: 22
Successful: 22
Failed: 0
Total time: 95.4 seconds
Average time per slide: 4.3 seconds
============================================================
```

---

## Advanced Implementation (10+ minutes)

### Error Handling

The script implements sophisticated error handling:

**Rate Limit / Quota Errors**:
- Detection: Checks for "rate" or "quota" in error message
- Recovery: API key rotation (if multiple keys) or 5-second delay
- Maximum: 10 retry attempts per slide

**Empty Response Handling**:
- Detection: `response.parts is None`
- Recovery: Up to 5 retries with 3-second delay
- Provides detailed feedback (prompt_feedback, finish_reason, safety_ratings)

**Safety Filter Blocks**:
- Detection: Checks for "blocked" or "safety" in error message
- Recovery: Skip the slide, log the error with reason
- Impact: Slide will not be generated, recorded in FAILURES.json

**API Key Rotation**:
- Supports multiple API keys via `GOOGLE_API_KEYS` environment variable
- Automatically rotates to next key on quota errors
- Thread-safe rotation with per-thread client instances

**Other Errors**:
- Recovery: 5-second delay before retry
- Maximum: 10 retry attempts

### Performance Optimization

**Batched Parallel Execution**:
- Uses ThreadPoolExecutor with configurable max workers (default: 20)
- Processes slides in batches of 20 to respect API rate limits
- 30-second delay between batches (Gemini API: 20 RPM)
- Results are collected as tasks complete within each batch

**Average Performance Metrics**:
- Generation time per slide: 4-8 seconds (with template reference)
- Throughput: 8-15 slides per minute (with batched parallelization)
- Success rate: 95%+ (with retry logic and API key rotation)

### Reference Images

The script supports reference images to guide visual style and content generation.

**Use Cases**:
- Consistent header/footer styling (template images)
- Consistent character appearance across slides
- Brand asset integration (logos, icons)
- Style reference for visual consistency
- Photo-based slide generation

**Reference Image Types**:

1. **Template Image** (`--template` option or auto-detected `template.png`):
   - Generated by `Generate_Template.py` showing empty header/footer structure
   - Auto-detected: If `template.png` exists in JSON directory, used automatically
   - Prepended to global references (highest priority)
   - Use for: consistent header/footer bar size, position, and color

2. **Global Reference Images** (top-level `reference_images`):
   - Applied to ALL slides in the presentation
   - Use for: brand assets, consistent characters, style guides

3. **Slide-Specific Reference Images** (per-slide `reference_images`):
   - Applied only to that specific slide
   - Combined with global references (slide-specific first, then global)
   - Use for: slide-specific photos, diagrams, charts

**Example JSON with Reference Images**:
```json
{
  "source_file": "/path/to/source.md",
  "reference_images": ["/path/to/logo.png", "/path/to/style_guide.png"],
  "slides": [
    {
      "page": 1,
      "title": "Title Slide",
      "nano_banana_prompt": "Create a title slide incorporating the provided logo...",
      "reference_images": ["/path/to/hero_image.png"]
    },
    {
      "page": 2,
      "title": "Team Introduction",
      "nano_banana_prompt": "Create a team photo slide using the provided photos...",
      "reference_images": ["/path/to/person1.png", "/path/to/person2.png"]
    }
  ]
}
```

**Output with Reference Images**:
```
[Global Reference] Found 2 global reference image(s)
[Slide 01/10] Title Slide (refs: 3) - Starting...
  [Reference Image] Loaded: hero_image.png
  [Reference Image] Loaded: logo.png
  [Reference Image] Loaded: style_guide.png
  [Attempt 1/10] Generating image with 3 reference(s)...
[Slide 01] Success - Saved to slide_001.png
```

**Best Practices**:
- Keep reference images under 5 per slide for optimal performance
- Use high-quality images (minimum 512x512 pixels recommended)
- Ensure reference images are accessible (absolute paths recommended)
- Reference images are optional - omit the field if not needed

### Integration Workflow

The complete PPT generation workflow:

**Step 1**: Source Analysis (Planner-PPT Agent)
- Analyzes markdown or PDF source files
- Generates JSON slide outline with nano_banana_prompt

**Step 2**: Image Generation (Nano-Banana Script)
- Reads JSON slide outline
- Generates PNG images for each slide

**Step 3**: Assembly (Manual or Automation)
- Combine generated images into final presentation

### Programmatic Integration

```python
from pathlib import Path
import subprocess

def generate_slides(json_path: str, output_dir: str = None) -> int:
    """Generate slides from JSON using Nano-Banana script."""
    script_path = "/path/to/Generate_Slides.py"
    cmd = ["uv", "run", "python", script_path, json_path]

    if output_dir:
        cmd.extend(["--output-dir", output_dir])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode
```

---

## Related Resources

**Related Agent**:
- `Planner-PPT`: Generates JSON slide outlines from source files

**Related Command**:
- `/ppt`: Orchestrates the complete PPT generation workflow

**Model Information**:
- Model: gemini-3-pro-image-preview (Nano Banana Pro)
- Capabilities: Text rendering, high-quality 2K images, 16:9 aspect ratio

**API Documentation**:
- Google AI Studio: https://aistudio.google.com/
- Gemini API: https://ai.google.dev/

---

## Works Well With

- `Planner-PPT` - Generates JSON slide outlines from markdown/PDF
- `/ppt` command - Orchestrates complete source-to-slides workflow

---

## Troubleshooting

**API Key Not Found**:
- Ensure `.env` file exists at `.claude/skills/Nano-Banana/Scripts/.env`
- Verify `GOOGLE_API_KEYS` or `GOOGLE_API_KEY` is set correctly

**Quota Exceeded**:
- Use multiple API keys via `GOOGLE_API_KEYS=key1,key2,key3`
- Wait for quota reset or reduce BATCH_SIZE/MAX_WORKERS
- Check Google AI Studio for quota status

**Safety Filter Triggered**:
- Review prompt content for problematic terms
- Simplify or rephrase the nano_banana_prompt
- Check FAILURES.json for detailed error reasons
- Avoid controversial or explicit content

**Image Generation Failed**:
- Check network connectivity
- Verify API key is valid
- Review prompt structure follows design_system format

**Empty Response (Sensitive Content)**:
- Script retries up to 5 times automatically
- Check if content triggers safety filters
- Detailed feedback logged (prompt_feedback, finish_reason)

**Inconsistent Header/Footer**:
- Generate template first: `python Generate_Template.py slides.json`
- Ensure template.png is in same directory as JSON
- Use `--template` option to specify explicitly

**Partial Slide Recovery**:
- Use `--slides` parameter to regenerate only failed slides
- Example: `--slides 5,12,15` to regenerate slides 5, 12, and 15
- Supports single numbers, comma-separated lists, and ranges (e.g., `1-5`, `1-3,5,7-9`)
- Check FAILURES.json for list of failed slides
