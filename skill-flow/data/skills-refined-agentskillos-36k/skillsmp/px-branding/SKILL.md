---
name: px-branding
description: "Trigger: 'criar apresentação PX', 'apresentação PX', 'deck PX', 'pptx PX'. Aplica identidade visual PX Center em apresentações PowerPoint (.pptx) com formato 16:9 widescreen. Cores da marca, logo, tipografia Nunito/Poppins. Geração de imagens AI via Gemini API (requer aprovação do usuário antes de cada uso devido ao custo ~R$0.90/imagem)."
---

# PX Center Branding Skill

Apply PX Center brand identity to all Office documents, with intelligent visual asset generation.

## Execution Method (Windows)

Run Python scripts directly via PowerShell or cmd. Scripts are located in `.claude/skills/px-branding/scripts/`.

```powershell
python "%TEMP%\px-branding\script.py" args
```

## Presentation Workflow

### Phase 1: Content Planning

Before any visual generation, create a structured plan:

```markdown
## Visual Assets Plan

| Slide | Asset Type | Approach | Rationale |
|-------|------------|----------|-----------|
| 1 | Title background | AI Image | Abstract branded scene, hard to code |
| 3 | Bar chart | React | Structured data, precise rendering |
| 5 | Process flow | React | 4-step linear flow, boxes and arrows |
| 7 | Market illustration | AI Image | Complex conceptual scene |
```

### Phase 2: User Confirmation (REQUIRED)

*Always present this choice before generating visuals:*

```
Visual Assets Required: [N] items

REACT/CODE (Free, instant):
- Charts: bar, line, pie, area, scatter
- Diagrams: flowcharts, org charts, timelines
- Data tables with styling
- Simple icons and shapes

AI IMAGE GENERATION (~$0.15/image, ~R$0.90):
- Complex illustrations and scenes
- Abstract branded backgrounds
- Conceptual imagery
- Photo-realistic visuals

PLACEHOLDER (Free, manual):
- Empty containers with prompt text
- You generate manually in AI Studio

Recommended approach:
[List each asset with recommendation]

Which approach for each? Or reply:
- "all react" - Code everything possible
- "all placeholder" - I'll generate manually
- "proceed" - Use recommendations above
```

### Phase 3: Environment Setup (once per session)

```powershell
# Create working directory
New-Item -ItemType Directory -Force -Path "$env:TEMP\px-branding"

# Copy scripts from skill directory
Copy-Item -Path ".\.claude\skills\px-branding\scripts\*" -Destination "$env:TEMP\px-branding\" -Recurse -Force

# Check/install dependencies
python -c "import requests, pptx" 2>$null
if ($LASTEXITCODE -ne 0) { pip install requests python-pptx }
```

*CRITICAL: Copy all scripts to temp directory before use:*
- logo.py (contains embedded logo as base64)
- generate_image.py (AI image generation)
- px_branding.py (presentation builder with brand constants)

### Phase 4: Generate Assets

#### React/Code Assets (Default for structured data)

Create as HTML artifacts or SVG files. For PPTX embedding, export React as PNG or use SVG directly.

#### AI Image Generation (Complex visuals only)

```powershell
# Cost estimate first
python "$env:TEMP\px-branding\generate_image.py" "prompt" "$env:TEMP\out.png" --dry-run

# Generate if approved
python "$env:TEMP\px-branding\generate_image.py" "prompt" "$env:TEMP\out.png"
```

#### Placeholder Containers

For manual generation, create text boxes in PPTX with the prompt inside.

### Phase 5: Assemble & Deliver

```powershell
# Copy to Desktop
Copy-Item "$env:TEMP\output.pptx" "$env:USERPROFILE\Desktop\Presentation.pptx"

# Show API usage summary
python "$env:TEMP\px-branding\generate_image.py" --summary

# Open in PowerPoint
Start-Process "$env:USERPROFILE\Desktop\Presentation.pptx"
```

## Visual Asset Decision Matrix

| Asset Type | Default Approach | When to use AI Image |
|------------|------------------|---------------------|
| Bar/Line/Pie charts | *React* | Never |
| Data tables | *React* | Never |
| Flowcharts (<8 nodes) | *React* | Never |
| Org charts | *React* | Never |
| Timelines | *React* | Never |
| Simple icons | *React/SVG* | Never |
| Process diagrams | React | >10 nodes, complex branching |
| Infographics | React | Heavy illustration component |
| Conceptual scenes | AI Image | Always |
| Abstract backgrounds | AI Image | Always |
| Photo-realistic | AI Image | Always |
| Complex illustrations | AI Image | Always |

*Rule of thumb*: If it's data or can be described as boxes/arrows/lines, use React. If it requires artistic interpretation, use AI.

## Brand Assets

### Logo (Embedded Base64)

The logo is embedded directly in scripts/logo.py as base64 to avoid file transfer issues.

*Usage in python-pptx:*

```python
import sys
sys.path.insert(0, os.path.join(os.environ['TEMP'], 'px-branding'))
from logo import get_logo_stream
from pptx.util import Inches

# Add logo to slide
slide.shapes.add_picture(get_logo_stream(), Inches(0.5), Inches(0.3), width=Inches(1.5))
```

*Alternative: Write logo file once per session*

```python
from logo import write_logo_file
logo_path = write_logo_file()  # Returns temp path to logo.png
slide.shapes.add_picture(logo_path, Inches(0.5), Inches(0.3), width=Inches(1.5))
```

## Color Palette

| Name | HEX | RGB | Usage |
|------|-----|-----|-------|
| blue-100 | #D5E4F5 | 213, 228, 245 | Light backgrounds |
| blue-500 | #3399FF | 51, 153, 255 | Primary, headers |
| blue-700 | #0F3D66 | 15, 61, 102 | Dark accents |

## Typography

Sans-serif: *Nunito*, *Poppins*, or *Arial* (fallback)

## python-pptx Reference

*Correct imports for v1.0.2:*

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor  # NOT pptx.shared or pptx.util
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
```

*PX Colors:*

```python
BLUE_100 = RGBColor(0xD5, 0xE4, 0xF5)
BLUE_500 = RGBColor(0x33, 0x99, 0xFF)
BLUE_700 = RGBColor(0x0F, 0x3D, 0x66)
```

*16:9 Slide Setup:*

```python
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

## AI Image Generation

### Pricing Reference (Gemini 3 Pro Image Preview)

| Component | Cost |
|-----------|------|
| Input | $2.00 / 1M tokens |
| Output (image) | $120.00 / 1M tokens |
| Per image (1K-2K) | ~$0.134 (~R$0.80) |
| Per image (4K) | ~$0.24 (~R$1.44) |

### Script Features

- *Cost estimation*: --dry-run flag shows cost before generating
- *Request logging*: All API calls logged to %TEMP%\px-branding\api_log.jsonl
- *Usage summary*: --summary flag shows total spend
- *IMAGE-only output*: No text tokens wasted

### Usage

```powershell
# Cost estimate only
python "$env:TEMP\px-branding\generate_image.py" "Abstract network" "$env:TEMP\bg.png" --dry-run

# Generate 16:9 (default)
python "$env:TEMP\px-branding\generate_image.py" "Process flow diagram" "$env:TEMP\flow.png"

# View usage summary
python "$env:TEMP\px-branding\generate_image.py" --summary
```

## Analyst Mode

### Spreadsheets: Assumption-Driven Models

Never hardcode. Break into editable assumptions.

### Documents: Insight Comments

Add thought bubbles with analyst notes.

### Presentations: Hidden Appendix

After main slides, add appendix with raw data and sources.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scripts not found | Copy scripts to %TEMP%\px-branding\ first |
| No module named 'requests' | pip install requests |
| No module named 'pptx' | pip install python-pptx |
| cannot import RGBColor | Use from pptx.dml.color import RGBColor |
| High API costs | Check --summary, reduce AI images |
| Logo shows as WebP/wrong format | Use logo.py with embedded base64 (fixed) |

## Cost Control Checklist

Before generating any presentation:

1. [ ] Count required visuals
2. [ ] Categorize each (React vs AI vs Placeholder)
3. [ ] Show user the plan with cost estimate
4. [ ] Get explicit approval for AI generation
5. [ ] Run --dry-run before each AI call
6. [ ] Check --summary after completion
