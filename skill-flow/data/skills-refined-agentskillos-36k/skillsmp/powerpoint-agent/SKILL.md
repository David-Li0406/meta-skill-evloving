---
name: powerpoint-agent
description: Creates editable PowerPoint presentations (.pptx) with AI-generated full-slide images. Auto-trigger when users ask to create PowerPoint presentations, PPTX files, editable slide decks, or presentations they can edit later. Supports brand consistency via reference images (logos, colors) and rolling style references to maintain visual consistency across slides. Uses fal.ai Nano Banana Pro for slide generation.
---

# PowerPoint Agent

Creates professional PowerPoint presentations with:
- **Full-slide AI images** - Each slide is an AI-generated image that fills the entire slide
- **16:9 widescreen format** - Standard presentation dimensions (10" x 5.625")
- **Brand consistency** - Reference images (logos, colors) applied to all slides
- **Rolling style references** - Previous slides used as references for consistent styling
- **Editable output** - Standard .pptx file that can be opened in PowerPoint, Google Slides, etc.

## Output Format

```
slide_01.png --> Full-slide image in PowerPoint
slide_02.png --> Full-slide image in PowerPoint
...
```

Final output: .pptx file with slide titles in speaker notes

## Prerequisites

Before generating, verify:

1. **FAL_KEY** in `.env` file (get from https://fal.ai/dashboard/keys)
2. **python-pptx** installed: `pip install python-pptx`
3. **ANTHROPIC_API_KEY** in `.env` (optional, for validation)

Check prerequisites:
```python
from scripts import print_prerequisites_status
print_prerequisites_status()
```

## Available Reference Images

Located in `Reference Images/` folder:
- Abonmarche Primary Logo Full Color Transparent BG.png
- Abonmarche A Transparent BG.png
- COP Logo.png

## Workflow

### Step 1: Gather Information

Ask the user for:
1. **Topic/subject** of the presentation
2. **Number of slides** (default: 5)
3. **Reference images** - which images from Reference Images folder to use for branding
4. **Rolling references** - use previous slides to maintain style (default: yes)

### Step 2: Generate Slide Content

For each slide, define:
- **title**: Heading text displayed on slide
- **bullet_points**: 3-4 brief points (3-6 words each)
- **visual_description**: Description of the icon/graphic

Example for 3 slides:
```python
slides = [
    SlideContent(
        title="Welcome to Abonmarche",
        bullet_points=["Engineering Excellence", "Innovation in Design", "Trusted Partner"],
        visual_description="Professional title slide with Abonmarche logo prominently displayed",
        is_title_slide=True,
    ),
    SlideContent(
        title="Our Services",
        bullet_points=["Civil Engineering", "Land Surveying", "Environmental Consulting"],
        visual_description="Simple line-art icons representing engineering services",
    ),
    SlideContent(
        title="Contact Us",
        bullet_points=["Visit abonmarche.com", "Call for consultation", "Partner with us"],
        visual_description="Contact information with simple phone/web icons",
    ),
]
```

### Step 3: Create Configuration

```python
from scripts import PPTXConfig, SlideContent

config = PPTXConfig(
    slides=slides,
    reference_images=[
        "Reference Images/Abonmarche Primary Logo Full Color Transparent BG.png"
    ],
    use_rolling_references=True,
    rolling_reference_count=1,
    validate_slides=True,
    output_path="./output/presentation.pptx",
    presentation_title="Abonmarche Overview",
)
```

### Step 4: Generate PowerPoint

```python
from scripts import create_powerpoint

result = create_powerpoint(config)
print(f"PowerPoint saved: {result}")
```

## Style Reference Feature

The skill supports two types of reference images:

### Static References
- Logos, brand colors, style examples
- Applied to ALL slides
- Uploaded once to fal.ai

### Rolling References
- Previously generated slides used as reference
- Slide 1: Uses static references only
- Slide 2+: Uses static references + previous slide(s)
- Helps maintain consistent styling across the deck

Configuration:
```python
config = PPTXConfig(
    slides=slides,
    reference_images=["logo.png"],      # Static refs
    use_rolling_references=True,         # Enable rolling refs
    rolling_reference_count=1,           # Include last 1 slide
)
```

## Cost Estimate

| Item | Cost |
|------|------|
| Slides | $0.15/image (Nano Banana Pro) |
| Validation | ~$0.001/slide (Claude Haiku 4.5, optional) |

5-slide presentation: ~$0.75-0.80 (much cheaper than video!)

```python
from scripts import estimate_cost
print(estimate_cost(num_slides=5))
```

## Example Prompts That Trigger This Skill

- "Create a PowerPoint about renewable energy"
- "Make me an editable presentation for our team meeting"
- "Generate a PPTX file about civil engineering"
- "Build a slide deck I can edit later"
- "Create a presentation about workplace safety that I can modify"
- "Make a 5-slide PowerPoint on our company services"

## JSON Configuration

Alternatively, use JSON config file:

```json
{
    "title": "Company Overview",
    "author": "John Smith",
    "reference_images": [
        "Reference Images/Abonmarche Primary Logo Full Color Transparent BG.png"
    ],
    "output_path": "./output/presentation.pptx",
    "validate_slides": true,
    "use_rolling_references": true,
    "rolling_reference_count": 1,
    "slides": [
        {
            "title": "Welcome",
            "bullet_points": ["Point 1", "Point 2", "Point 3"],
            "visual_description": "Title slide with logo",
            "is_title_slide": true
        },
        {
            "title": "Our Services",
            "bullet_points": ["Service A", "Service B", "Service C"],
            "visual_description": "Service icons"
        }
    ]
}
```

Run with:
```python
from scripts import run_from_json
result = run_from_json("presentation_config.json")
```

## Output Structure

```
output/
  <presentation_name>/
    slides/
      slide_01.png
      slide_02.png
      ...
    presentation.pptx
```

## Editing Existing PowerPoints

The skill can edit existing presentations by regenerating specific slides and replacing them.

### Replacing a Single Slide

When a user asks to "fix slide X" or "regenerate slide X":

1. **Generate a new slide image** using an adjacent slide as reference (for style consistency)
   - If fixing slide 1, use slide 2 as the style reference
   - If fixing slide N, use slide N-1 or N+1 as the style reference
2. **Replace the slide** in the existing PowerPoint

```python
from scripts import generate_slide, replace_slide_image, upload_reference_images

# Step 1: Upload the adjacent slide as style reference
ref_urls = upload_reference_images(["output/presentation/slides/slide_02.png"])

# Step 2: Generate new slide image
new_image = generate_slide(
    title="What is RAG?",
    bullet_points=["Retrieval Augmented Generation", "AI searches your docs", "Answers with YOUR data"],
    visual_description="Corporate memphis style intro slide with AI/search icon",
    slide_number=1,
    output_dir="./output/presentation/slides",
    reference_urls=ref_urls,
    is_title_slide=True,
)

# Step 3: Replace in existing PowerPoint
replace_slide_image(
    pptx_path="./output/presentation/presentation.pptx",
    slide_number=1,
    new_image_path=new_image,
    new_title="What is RAG?",
)
```

### Replacing Multiple Slides

```python
from scripts import replace_multiple_slides

replace_multiple_slides(
    pptx_path="./output/presentation.pptx",
    replacements=[
        {"slide_number": 1, "image_path": "new_slide_01.png", "title": "New Title 1"},
        {"slide_number": 3, "image_path": "new_slide_03.png", "title": "New Title 3"},
    ],
    output_path="./output/presentation_updated.pptx",  # Optional: save to new file
)
```

### Key Principle: Style Reference from Adjacent Slides

When regenerating a slide, use an adjacent slide (not the original reference image) to maintain consistency with the rest of the deck:

- **Slide 1**: Use slide 2 as reference
- **Slide N (middle)**: Use slide N-1 as reference (previous slide)
- **Last slide**: Use second-to-last slide as reference

This ensures the regenerated slide matches the style already established in the presentation.

### Example: Fix Slide That Copied Reference Too Literally

If a slide looks too much like the reference image (copied graphics instead of creating new ones):

1. Use an adjacent slide that has the correct style
2. Give detailed visual_description for what NEW graphic to create
3. Regenerate and replace

## Comparison: PowerPoint vs Video Agent

| Feature | PowerPoint Agent | Video Agent |
|---------|-----------------|-------------|
| Output | .pptx (editable) | .mp4 (video) |
| Cost/5 slides | ~$0.75 | ~$2.65 |
| Voiceover | No | Yes |
| Transitions | No | Yes (animated) |
| Editable | Yes | No |
| Use case | Edit/customize | Share/present |
