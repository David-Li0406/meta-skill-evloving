---
id: image-generation
name: "Image Generation (DALL-E, Midjourney)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Image Generation (DALL-E, Midjourney)

## Overview

AI image generation creates visual content from text descriptions. Services like DALL-E 3, Midjourney, and Stable Diffusion enable automated creative workflows, content generation, and visual prototyping.

## When to Use

- Marketing and advertising content
- Product visualization
- UI/UX design prototyping
- Creative exploration
- Custom illustrations
- Social media content

## Key Concepts

### Image Generation Services

| Service | Quality | Style | API | Cost |
|---------|---------|-------|-----|------|
| DALL-E 3 | High | Versatile | OpenAI | $0.04-0.12/image |
| Midjourney | Very High | Artistic | Discord/API | $10-60/month |
| Stable Diffusion | Good | Customizable | Local/API | Free/Variable |
| Ideogram | High | Text in images | API | Credits |
| Flux | Very High | Photorealistic | Replicate | Pay-per-use |

### Generation Parameters

| Parameter | Effect |
|-----------|--------|
| Prompt | Content description |
| Size | Output dimensions |
| Quality | Detail level |
| Style | Artistic approach |
| Negative Prompt | What to avoid |

## Implementation

### DALL-E 3 Integration

```python
from openai import OpenAI
import base64
import requests
from pathlib import Path

client = OpenAI()

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid",
    n: int = 1
) -> dict:
    """
    Generate image with DALL-E 3.

    size: "1024x1024", "1792x1024", "1024x1792"
    quality: "standard", "hd"
    style: "vivid", "natural"
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=n
    )

    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt
    }

def generate_and_save(
    prompt: str,
    output_path: str,
    **kwargs
) -> str:
    """Generate image and save to file."""
    result = generate_image(prompt, **kwargs)

    # Download image
    response = requests.get(result["url"])
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path

def generate_variations(
    image_path: str,
    n: int = 3,
    size: str = "1024x1024"
) -> list:
    """Generate variations of an existing image (DALL-E 2 only)."""
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f,
            n=n,
            size=size,
            model="dall-e-2"
        )

    return [img.url for img in response.data]

def edit_image(
    image_path: str,
    mask_path: str,
    prompt: str,
    size: str = "1024x1024"
) -> str:
    """Edit image with mask (DALL-E 2 only)."""
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            image=img,
            mask=mask,
            prompt=prompt,
            n=1,
            size=size,
            model="dall-e-2"
        )

    return response.data[0].url
```

### Prompt Engineering for Images

```python
class ImagePromptBuilder:
    """Build effective image generation prompts."""

    def __init__(self):
        self.components = {
            "subject": "",
            "style": "",
            "lighting": "",
            "composition": "",
            "details": [],
            "mood": "",
            "technical": []
        }

    def set_subject(self, subject: str):
        """Set main subject."""
        self.components["subject"] = subject
        return self

    def set_style(self, style: str):
        """Set artistic style."""
        # Common styles
        styles = {
            "photorealistic": "photorealistic, highly detailed photograph",
            "digital_art": "digital art, vibrant colors",
            "oil_painting": "oil painting, textured brushstrokes",
            "watercolor": "watercolor painting, soft edges, fluid",
            "anime": "anime style, cel shading",
            "3d_render": "3D render, octane render, highly detailed",
            "sketch": "pencil sketch, hand-drawn",
            "minimalist": "minimalist, clean lines, simple"
        }
        self.components["style"] = styles.get(style, style)
        return self

    def set_lighting(self, lighting: str):
        """Set lighting conditions."""
        lighting_options = {
            "golden_hour": "golden hour lighting, warm tones",
            "studio": "professional studio lighting",
            "dramatic": "dramatic lighting, high contrast",
            "soft": "soft diffused lighting",
            "neon": "neon lighting, cyberpunk atmosphere",
            "natural": "natural daylight"
        }
        self.components["lighting"] = lighting_options.get(lighting, lighting)
        return self

    def set_composition(self, composition: str):
        """Set composition style."""
        self.components["composition"] = composition
        return self

    def add_detail(self, detail: str):
        """Add specific detail."""
        self.components["details"].append(detail)
        return self

    def set_mood(self, mood: str):
        """Set mood/atmosphere."""
        self.components["mood"] = mood
        return self

    def add_technical(self, spec: str):
        """Add technical specification."""
        # Common technical specs
        specs = {
            "4k": "4K resolution, ultra detailed",
            "8k": "8K resolution, extremely detailed",
            "depth_of_field": "shallow depth of field, bokeh",
            "wide_angle": "wide angle lens",
            "macro": "macro photography, extreme detail",
            "cinematic": "cinematic composition, film grain"
        }
        self.components["technical"].append(specs.get(spec, spec))
        return self

    def build(self) -> str:
        """Build the final prompt."""
        parts = []

        if self.components["subject"]:
            parts.append(self.components["subject"])

        if self.components["style"]:
            parts.append(self.components["style"])

        if self.components["lighting"]:
            parts.append(self.components["lighting"])

        if self.components["composition"]:
            parts.append(self.components["composition"])

        if self.components["mood"]:
            parts.append(f"{self.components['mood']} mood")

        parts.extend(self.components["details"])
        parts.extend(self.components["technical"])

        return ", ".join(parts)

# Usage
prompt = (
    ImagePromptBuilder()
    .set_subject("a futuristic city skyline at sunset")
    .set_style("digital_art")
    .set_lighting("golden_hour")
    .set_mood("hopeful")
    .add_detail("flying cars")
    .add_detail("glass buildings")
    .add_technical("8k")
    .add_technical("cinematic")
    .build()
)
# "a futuristic city skyline at sunset, digital art, vibrant colors, golden hour lighting, warm tones, hopeful mood, flying cars, glass buildings, 8K resolution, extremely detailed, cinematic composition, film grain"
```

### Stable Diffusion via Replicate

```python
import replicate

def generate_with_stable_diffusion(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5
) -> str:
    """Generate image with Stable Diffusion XL."""
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale
        }
    )
    return output[0]  # Returns URL

def generate_with_flux(
    prompt: str,
    aspect_ratio: str = "1:1",
    num_outputs: int = 1
) -> list:
    """Generate image with Flux (high quality)."""
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "num_outputs": num_outputs,
            "output_format": "webp",
            "output_quality": 90
        }
    )
    return output
```

### Batch Generation

```python
import asyncio
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

class BatchImageGenerator:
    """Generate multiple images efficiently."""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.client = OpenAI()

    def generate_batch(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[Dict]:
        """Generate images for multiple prompts."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = []

            for prompt in prompts:
                future = executor.submit(
                    self._generate_single,
                    prompt,
                    **kwargs
                )
                futures.append((prompt, future))

            for prompt, future in futures:
                try:
                    result = future.result()
                    results.append({
                        "prompt": prompt,
                        "success": True,
                        "url": result["url"],
                        "revised_prompt": result["revised_prompt"]
                    })
                except Exception as e:
                    results.append({
                        "prompt": prompt,
                        "success": False,
                        "error": str(e)
                    })

        return results

    def _generate_single(self, prompt: str, **kwargs) -> dict:
        """Generate single image."""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            **kwargs
        )
        return {
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt
        }

    def generate_grid(
        self,
        base_prompt: str,
        variations: List[str],
        **kwargs
    ) -> List[Dict]:
        """Generate grid of variations."""
        prompts = [
            f"{base_prompt}, {variation}"
            for variation in variations
        ]
        return self.generate_batch(prompts, **kwargs)
```

### Image-to-Image with Vision

```python
import base64
from pathlib import Path

def describe_image(image_path: str) -> str:
    """Describe image using GPT-4 Vision."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in detail for image generation."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

def reimagine_image(
    image_path: str,
    style_modifier: str = "",
    **kwargs
) -> dict:
    """Create new image inspired by existing one."""
    # Get description
    description = describe_image(image_path)

    # Modify prompt
    prompt = f"{description}. {style_modifier}" if style_modifier else description

    # Generate new image
    return generate_image(prompt, **kwargs)
```

### Production Image Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
import logging
import hashlib
import os

class ImageModel(Enum):
    DALLE3 = "dall-e-3"
    DALLE2 = "dall-e-2"
    SDXL = "stable-diffusion-xl"
    FLUX = "flux"

@dataclass
class ImageGenerationConfig:
    model: ImageModel = ImageModel.DALLE3
    default_size: str = "1024x1024"
    default_quality: str = "standard"
    max_retries: int = 3
    cache_enabled: bool = True
    cache_dir: str = "./image_cache"

class ImageGenerationService:
    """Production image generation service."""

    def __init__(self, config: Optional[ImageGenerationConfig] = None):
        self.config = config or ImageGenerationConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

        if self.config.cache_enabled:
            os.makedirs(self.config.cache_dir, exist_ok=True)

    def generate(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        style: str = "vivid",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Generate image with caching and retry."""
        size = size or self.config.default_size
        quality = quality or self.config.default_quality

        # Check cache
        if use_cache and self.config.cache_enabled:
            cached = self._get_cached(prompt, size, quality, style)
            if cached:
                self.logger.info("Cache hit")
                return cached

        # Generate with retry
        for attempt in range(self.config.max_retries):
            try:
                if self.config.model == ImageModel.DALLE3:
                    result = self._generate_dalle3(prompt, size, quality, style)
                elif self.config.model == ImageModel.SDXL:
                    result = self._generate_sdxl(prompt, size)
                else:
                    result = self._generate_dalle3(prompt, size, quality, style)

                # Cache result
                if self.config.cache_enabled:
                    self._cache_result(prompt, size, quality, style, result)

                return result

            except Exception as e:
                self.logger.error(f"Generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise

        return {"error": "Max retries exceeded"}

    def _generate_dalle3(
        self,
        prompt: str,
        size: str,
        quality: str,
        style: str
    ) -> Dict:
        """Generate with DALL-E 3."""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1
        )

        return {
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt,
            "model": "dall-e-3"
        }

    def _generate_sdxl(self, prompt: str, size: str) -> Dict:
        """Generate with Stable Diffusion XL."""
        import replicate

        width, height = map(int, size.split("x"))
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "width": width,
                "height": height
            }
        )

        return {
            "url": output[0],
            "model": "sdxl"
        }

    def _get_cache_key(self, prompt: str, size: str, quality: str, style: str) -> str:
        """Generate cache key."""
        content = f"{prompt}|{size}|{quality}|{style}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, prompt: str, size: str, quality: str, style: str) -> Optional[Dict]:
        """Get cached result."""
        key = self._get_cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"

        if cache_file.exists():
            import json
            with open(cache_file) as f:
                return json.load(f)
        return None

    def _cache_result(self, prompt: str, size: str, quality: str, style: str, result: Dict):
        """Cache result."""
        import json
        key = self._get_cache_key(prompt, size, quality, style)
        cache_file = Path(self.config.cache_dir) / f"{key}.json"

        with open(cache_file, "w") as f:
            json.dump(result, f)
```

## Best Practices

1. **Prompt Quality**
   - Be specific and detailed
   - Describe style, lighting, composition
   - Use reference art styles
   - Include technical specifications

2. **Cost Management**
   - Cache generated images
   - Use appropriate quality levels
   - Batch similar requests
   - Consider local alternatives

3. **Content Safety**
   - Review content policies
   - Implement content filtering
   - Handle rejected prompts gracefully

4. **Quality Control**
   - Review generated images
   - Iterate on prompts
   - Use variations for options

5. **Workflow Integration**
   - Automate common use cases
   - Build prompt templates
   - Version control prompts

## Common Pitfalls

1. **Vague Prompts** - Results don't match expectations
2. **Ignoring Revised Prompts** - Missing what DALL-E actually generated
3. **Wrong Aspect Ratio** - Not matching use case
4. **No Caching** - Regenerating same images
5. **Content Policy Violations** - Prompts getting rejected
6. **Overcomplication** - Too many conflicting details

## References

- [DALL-E 3 Documentation](https://platform.openai.com/docs/guides/images)
- [Midjourney Documentation](https://docs.midjourney.com/)
- [Stable Diffusion](https://stability.ai/)
- [Replicate API](https://replicate.com/docs)
