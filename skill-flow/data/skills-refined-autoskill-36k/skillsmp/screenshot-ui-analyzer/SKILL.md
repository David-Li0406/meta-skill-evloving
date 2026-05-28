---
name: screenshot-ui-analyzer
description: Takes a screenshot, analyzes it using AI (Gemini Vision) to detect UI elements with bounding boxes, names, and descriptions, saves to JSON, and generates an annotated image. Use when you need to identify and label screen elements with advanced AI. Key commands: screenshot, analyze, annotate.
---

# Screenshot UI Analyzer

Takes a screenshot of the current screen, analyzes it using Google's Gemini Vision AI to detect UI elements (buttons, text fields, icons, menus, etc.), assigns bounding boxes, names, and descriptions, saves the data to a JSON file, and generates an annotated image with bounding boxes and labels.

## Usage

```bash
python ~/.copilot/skills/screenshot-ui-analyzer/script.py [--output-dir OUTPUT_DIR] [--model MODEL]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Directory to save the JSON and annotated image | Current directory |
| `--model` | Detection model ('gemini' for AI analysis, 'text' for OCR, 'hybrid' for Tesseract + LightOn refinement) | gemini |

## Output

JSON file with:
- `elements`: List of detected elements, each with `name`, `description`, `bbox` (x, y, width, height), `center` (x, y)

Annotated image file with bounding boxes drawn and names labeled.

## Requirements

- Set `GOOGLE_API_KEY` environment variable with your Google AI API key.
- Install dependencies: `pip install opencv-python pyautogui google-generativeai pillow`

## Examples

### Basic usage with Gemini AI
```bash
python ~/.copilot/skills/screenshot-ui-analyzer/script.py
```

### With custom output directory
```bash
python ~/.copilot/skills/screenshot-ui-analyzer/script.py --output-dir /path/to/output
```

### With hybrid model (Tesseract + LightOn)
```bash
python ~/.copilot/skills/screenshot-ui-analyzer/script.py --model hybrid
```