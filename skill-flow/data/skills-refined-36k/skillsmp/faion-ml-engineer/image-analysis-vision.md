---
id: image-analysis-vision
name: "Image Analysis (Vision)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Image Analysis (Vision)

## Overview

Vision capabilities enable LLMs to understand, analyze, and describe images. This includes object detection, OCR, visual reasoning, image comparison, and multimodal applications combining text and images.

## When to Use

- Document and image analysis
- Visual question answering
- OCR and text extraction
- Content moderation
- Product image analysis
- Accessibility (image descriptions)
- Medical/scientific image analysis

## Key Concepts

### Vision Model Comparison

| Model | Max Images | Image Size | Capabilities |
|-------|------------|------------|--------------|
| GPT-4o | 20 | 20MB | Comprehensive understanding |
| GPT-4o-mini | 20 | 20MB | Faster, cost-effective |
| Claude 3.5 Sonnet | 20 | 20MB | Detailed analysis |
| Gemini 1.5 Pro | 3600 | 20MB | Large context, video |

### Image Input Methods

| Method | Use Case |
|--------|----------|
| URL | Public images |
| Base64 | Local files, private images |
| File upload | API-specific handling |

## Implementation

### Basic Image Analysis

```python
from openai import OpenAI
import base64
from pathlib import Path

client = OpenAI()

def analyze_image_url(
    image_url: str,
    prompt: str = "Describe this image in detail."
) -> str:
    """Analyze image from URL."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

def analyze_local_image(
    image_path: str,
    prompt: str = "Describe this image in detail."
) -> str:
    """Analyze local image file."""
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    # Determine media type
    suffix = Path(image_path).suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    media_type = media_types.get(suffix, "image/jpeg")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content
```

### Multiple Image Analysis

```python
def compare_images(
    image_paths: list[str],
    prompt: str = "Compare these images and describe their differences."
) -> str:
    """Analyze and compare multiple images."""
    content = [{"type": "text", "text": prompt}]

    for path in image_paths:
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content

def analyze_image_sequence(
    image_paths: list[str],
    prompt: str = "Describe what's happening in this sequence of images."
) -> str:
    """Analyze a sequence of images (e.g., storyboard)."""
    content = [{"type": "text", "text": prompt}]

    for i, path in enumerate(image_paths):
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        content.append({
            "type": "text",
            "text": f"Image {i + 1}:"
        })
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content
```

### Structured Image Analysis

```python
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class DetectedObject(BaseModel):
    name: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    description: str

class ImageAnalysis(BaseModel):
    description: str
    objects: List[DetectedObject]
    colors: List[str]
    mood: str
    text_content: Optional[str] = None
    tags: List[str]

def structured_analysis(image_path: str) -> ImageAnalysis:
    """Get structured analysis of an image."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    prompt = """Analyze this image and return structured JSON with:
- description: Overall description
- objects: List of detected objects with name, confidence (0-1), description
- colors: Dominant colors
- mood: Overall mood/atmosphere
- text_content: Any text visible in the image (or null)
- tags: Relevant tags for categorization

Return valid JSON matching this structure."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return ImageAnalysis(**data)
```

### OCR and Document Analysis

```python
class DocumentAnalyzer:
    """Analyze documents and extract text."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def extract_text(self, image_path: str) -> str:
        """Extract all text from image."""
        return self._analyze(
            image_path,
            "Extract all text visible in this image. Maintain formatting where possible."
        )

    def extract_structured_data(
        self,
        image_path: str,
        fields: List[str]
    ) -> dict:
        """Extract specific fields from document."""
        fields_str = ", ".join(fields)
        prompt = f"""Extract these fields from the document: {fields_str}

Return JSON with the field names as keys. Use null for missing fields."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def analyze_receipt(self, image_path: str) -> dict:
        """Analyze receipt and extract items."""
        prompt = """Analyze this receipt and extract:
- store_name
- date
- items: list of {name, quantity, price}
- subtotal
- tax
- total
- payment_method (if visible)

Return as JSON."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def analyze_form(self, image_path: str) -> dict:
        """Analyze filled form."""
        prompt = """Analyze this form and extract all filled fields.
Return JSON with field names/labels as keys and filled values as values.
For checkboxes, use true/false.
For empty fields, use null."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def _analyze(
        self,
        image_path: str,
        prompt: str,
        json_mode: bool = False
    ) -> str:
        """Internal analysis method."""
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ]
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
```

### Visual QA System

```python
class VisualQA:
    """Visual question answering system."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model
        self.conversation_history = []
        self.current_image = None

    def set_image(self, image_path: str):
        """Set the image for Q&A."""
        with open(image_path, "rb") as f:
            self.current_image = base64.standard_b64encode(f.read()).decode()
        self.conversation_history = []

    def ask(self, question: str) -> str:
        """Ask a question about the current image."""
        if not self.current_image:
            raise ValueError("No image set. Call set_image() first.")

        # Build messages
        messages = []

        # First message includes image
        if not self.conversation_history:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{self.current_image}"
                        }
                    }
                ]
            })
        else:
            # Include history and new question
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        answer = response.choices[0].message.content

        # Update history
        if not self.conversation_history:
            self.conversation_history.append(messages[0])
        else:
            self.conversation_history.append({"role": "user", "content": question})

        self.conversation_history.append({"role": "assistant", "content": answer})

        return answer

# Usage
vqa = VisualQA()
vqa.set_image("photo.jpg")
print(vqa.ask("What objects are in this image?"))
print(vqa.ask("What colors do you see?"))
print(vqa.ask("What is the mood of this image?"))
```

### Image Classification

```python
from typing import List, Dict

class ImageClassifier:
    """Classify images into categories."""

    def __init__(
        self,
        categories: List[str],
        model: str = "gpt-4o"
    ):
        self.categories = categories
        self.client = OpenAI()
        self.model = model

    def classify(
        self,
        image_path: str,
        return_confidence: bool = True
    ) -> Dict:
        """Classify image into predefined categories."""
        categories_str = ", ".join(self.categories)

        prompt = f"""Classify this image into one of these categories: {categories_str}

Return JSON with:
- category: the best matching category
- confidence: confidence score (0-1)
- reasoning: brief explanation"""

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def classify_batch(
        self,
        image_paths: List[str]
    ) -> List[Dict]:
        """Classify multiple images."""
        return [self.classify(path) for path in image_paths]

# Usage
classifier = ImageClassifier(
    categories=["landscape", "portrait", "product", "document", "screenshot"]
)
result = classifier.classify("image.jpg")
print(f"Category: {result['category']}, Confidence: {result['confidence']}")
```

### Content Moderation

```python
class ContentModerator:
    """Moderate image content for safety."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def moderate(self, image_path: str) -> Dict:
        """Check image for inappropriate content."""
        prompt = """Analyze this image for content moderation.

Check for:
- Violence or gore
- Adult/sexual content
- Hate symbols or imagery
- Dangerous activities
- Illegal content

Return JSON:
{
    "is_safe": true/false,
    "flags": [list of issues found],
    "severity": "none" | "low" | "medium" | "high",
    "details": "explanation"
}"""

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### Production Vision Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import logging
from pathlib import Path
import httpx

class ImageSource(Enum):
    URL = "url"
    FILE = "file"
    BASE64 = "base64"

@dataclass
class VisionConfig:
    model: str = "gpt-4o"
    max_image_size_mb: int = 20
    detail: str = "auto"  # "low", "high", "auto"
    max_retries: int = 3
    timeout: int = 60

class VisionService:
    """Production vision analysis service."""

    def __init__(self, config: Optional[VisionConfig] = None):
        self.config = config or VisionConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def analyze(
        self,
        image: Union[str, Path],
        prompt: str,
        source_type: ImageSource = ImageSource.FILE,
        structured_output: bool = False
    ) -> Dict[str, Any]:
        """Analyze image with error handling."""
        try:
            # Prepare image content
            image_content = self._prepare_image(image, source_type)

            # Build request
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_content,
                                "detail": self.config.detail
                            }
                        }
                    ]
                }
            ]

            kwargs = {
                "model": self.config.model,
                "messages": messages,
                "timeout": self.config.timeout
            }

            if structured_output:
                kwargs["response_format"] = {"type": "json_object"}

            # Make request with retry
            for attempt in range(self.config.max_retries):
                try:
                    response = self.client.chat.completions.create(**kwargs)
                    content = response.choices[0].message.content

                    return {
                        "success": True,
                        "content": json.loads(content) if structured_output else content,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens
                        }
                    }
                except Exception as e:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == self.config.max_retries - 1:
                        raise

        except Exception as e:
            self.logger.error(f"Vision analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _prepare_image(
        self,
        image: Union[str, Path],
        source_type: ImageSource
    ) -> str:
        """Prepare image for API."""
        if source_type == ImageSource.URL:
            return str(image)

        elif source_type == ImageSource.BASE64:
            return f"data:image/jpeg;base64,{image}"

        else:  # FILE
            path = Path(image)
            if not path.exists():
                raise FileNotFoundError(f"Image not found: {path}")

            # Check size
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > self.config.max_image_size_mb:
                raise ValueError(f"Image too large: {size_mb:.1f}MB")

            # Read and encode
            with open(path, "rb") as f:
                data = base64.standard_b64encode(f.read()).decode()

            # Determine media type
            suffix = path.suffix.lower()
            media_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }
            media_type = media_types.get(suffix, "image/jpeg")

            return f"data:{media_type};base64,{data}"

    def batch_analyze(
        self,
        images: List[Union[str, Path]],
        prompt: str,
        source_type: ImageSource = ImageSource.FILE
    ) -> List[Dict]:
        """Analyze multiple images."""
        results = []
        for image in images:
            result = self.analyze(image, prompt, source_type)
            results.append(result)
        return results
```

## Best Practices

1. **Image Quality**
   - Use appropriate resolution
   - Ensure good lighting/contrast
   - Crop to relevant content

2. **Prompting**
   - Be specific about what to analyze
   - Use structured output for consistency
   - Include context when relevant

3. **Performance**
   - Use "low" detail for simple tasks
   - Resize large images before sending
   - Batch similar analyses

4. **Error Handling**
   - Validate image formats
   - Handle API limits
   - Provide fallbacks

5. **Privacy**
   - Consider data sensitivity
   - Blur/mask personal information
   - Follow data retention policies

## Common Pitfalls

1. **Large Images** - Exceeding size limits
2. **Wrong Format** - Unsupported image types
3. **No Detail Control** - Wasting tokens on high-detail mode
4. **Vague Prompts** - Getting generic descriptions
5. **No Structured Output** - Difficult to parse results
6. **Missing Context** - Not providing enough background

## References

- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Claude Vision](https://docs.anthropic.com/en/docs/vision)
- [Gemini Vision](https://ai.google.dev/tutorials/python_quickstart#vision)
