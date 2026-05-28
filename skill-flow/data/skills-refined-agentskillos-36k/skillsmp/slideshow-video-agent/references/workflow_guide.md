# Workflow Guide

This guide covers the complete workflow for generating video presentations.

## Prerequisites

### 1. FAL_KEY API Key

Get your API key from [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)

Add to `.env` file in project root:
```
FAL_KEY=your-actual-api-key-here
```

### 2. FFmpeg Installation (Windows)

FFmpeg is required for video assembly.

**Option A: Manual Download (Recommended)**
1. Go to https://github.com/BtbN/FFmpeg-Builds/releases
2. Download `ffmpeg-master-latest-win64-gpl.zip`
3. Extract to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to your system PATH:
   - Open System Properties > Advanced > Environment Variables
   - Edit PATH and add `C:\ffmpeg\bin`
5. Restart your terminal

**Option B: Using winget**
```powershell
winget install ffmpeg
```

**Option C: Using Chocolatey**
```powershell
choco install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Python Dependencies

```bash
pip install fal-client requests python-dotenv
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

## Workflow Overview

```
User Input (topic, slides, references)
         |
         v
+------------------+
| 1. Generate      |  Nano Banana Pro
|    Slide Images  |  (fal-ai/nano-banana-pro/edit)
+------------------+
         |
         v
+------------------+
| 2. Generate      |  Eleven Labs v3
|    Voiceovers    |  (fal-ai/elevenlabs/tts/eleven-v3)
+------------------+
         |
         v
+------------------+
| 3. Generate      |  Kling 2.6 Pro
|    Transitions   |  (fal-ai/kling-video/v2.6/pro/image-to-video)
+------------------+
         |
         v
+------------------+
| 4. Assemble      |  FFmpeg
|    Final Video   |  (concat, encode)
+------------------+
         |
         v
    Final MP4 Video
```

## Step-by-Step Process

### Step 1: Define Slides

Each slide needs:
- **title**: Text shown on slide
- **visual_description**: What the slide should look like
- **narration**: Script for voiceover

```python
slides = [
    Slide(
        title="Welcome to Our Company",
        visual_description="Modern title slide with company logo, clean design, corporate blue colors",
        narration="Welcome to our quarterly business update. Today we'll cover our achievements and future plans."
    ),
    Slide(
        title="Q4 Highlights",
        visual_description="Infographic showing growth metrics, charts, upward arrows, green accents",
        narration="Our fourth quarter exceeded expectations with record revenue growth."
    ),
]
```

### Step 2: Configure Presentation

```python
config = PresentationConfig(
    slides=slides,
    voice="George",               # See voice_options.md
    transition_style="cinematic", # See transition_styles.md
    reference_images=[
        "Reference Images/Abonmarche Primary Logo Full Color Transparent BG.png"
    ],
    output_path="./output/presentation.mp4"
)
```

### Step 3: Generate

```python
from scripts import create_slideshow_video
result = create_slideshow_video(config)
```

## Output Structure

```
output/
  presentation.mp4      # Final video
  slides/
    slide_01.png        # Generated slide images
    slide_02.png
    ...
  audio/
    narration_01.mp3    # Generated voiceover files
    narration_02.mp3
    ...
  transitions/
    transition_01.mp4   # Generated transition videos
    transition_02.mp4
    ...
```

## Cost Estimation

| Item | Cost per Unit | Example (5 slides) |
|------|---------------|-------------------|
| Slides | $0.15/image | $0.75 |
| Voiceovers | ~$0.30/1000 chars | ~$0.50 |
| Transitions | $0.35/video | $1.40 |
| **Total** | | **~$2.65** |

Use the cost estimator:
```python
from scripts import estimate_cost
cost = estimate_cost(num_slides=5, avg_narration_chars=200)
print(cost)
```

## Troubleshooting

### FAL_KEY not found
- Ensure `.env` file exists in project root
- Check that FAL_KEY is set correctly (not the placeholder)
- Restart your terminal after creating .env

### FFmpeg not found
- Verify FFmpeg is in PATH: `ffmpeg -version`
- Restart terminal after installation
- On Windows, ensure you added `C:\ffmpeg\bin` to PATH

### API Errors
- The system retries failed API calls up to 3 times
- If persistent, check your fal.ai account for rate limits
- Ensure you have sufficient credits

### Reference Images Not Working
- Use absolute paths or paths relative to project root
- Verify images exist: `list_reference_images()`
- Supported formats: PNG, JPG, JPEG, WebP

### Video Assembly Fails
- Check disk space
- Ensure all slide/audio files were generated
- Check temp folder for partial outputs
