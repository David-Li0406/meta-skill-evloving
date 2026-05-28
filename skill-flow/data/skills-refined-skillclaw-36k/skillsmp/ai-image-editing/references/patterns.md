# AI Image Editing

## Patterns


---
  #### **Id**
replicate-inpainting
  #### **Name**
Inpainting with Replicate API
  #### **Description**
    Use Replicate's Flux Fill model for professional inpainting.
    Mask white areas to be filled, black to preserve.
    
    Model options:
    - flux-fill-pro: Best quality, seamless blending
    - flux-dev-inpainting: Good balance of speed/quality
    - sdxl-inpainting: SDXL-based, lower cost
    
  #### **Code Example**
    # Install: pip install replicate
    
    import replicate
    import base64
    from pathlib import Path
    
    # Initialize client
    client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
    
    # Load image and mask
    def encode_image(path: str) -> str:
        """Encode image to base64 data URI."""
        data = Path(path).read_bytes()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    
    # Run Flux Fill Pro (best quality)
    output = client.run(
        "black-forest-labs/flux-fill-pro",
        input={
            "image": encode_image("input.png"),
            "mask": encode_image("mask.png"),  # White = edit, Black = keep
            "prompt": "a red sports car parked on the street",
            "output_format": "png",
        }
    )
    
    # Save result
    with open("output.png", "wb") as f:
        f.write(output.read())
    
    # Alternative: Flux Dev Inpainting (faster, cheaper)
    output = client.run(
        "zsxkib/flux-dev-inpainting",
        input={
            "image": encode_image("input.png"),
            "mask": encode_image("mask.png"),
            "prompt": "modern office furniture",
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "strength": 0.85,  # 0.5-0.85 recommended
        }
    )
    
    # Async for long-running tasks
    prediction = client.predictions.create(
        model="black-forest-labs/flux-fill-pro",
        input={
            "image": encode_image("input.png"),
            "mask": encode_image("mask.png"),
            "prompt": "vintage furniture in cozy room",
        }
    )
    
    # Poll for completion
    prediction = client.predictions.wait(prediction)
    print(f"Status: {prediction.status}")
    print(f"Output: {prediction.output}")
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Mask with inverted colors
      ###### **Why**
White should be edit area, black should be preserve
      ###### **Fix**
Invert mask before sending to API
    
---
      ###### **Pattern**
Very high strength for subtle edits
      ###### **Why**
Strength 0.9+ completely replaces content
      ###### **Fix**
Use 0.5-0.75 for balanced edits
  #### **References**
    - https://replicate.com/black-forest-labs/flux-fill-pro
    - https://replicate.com/collections/image-editing

---
  #### **Id**
stability-search-replace
  #### **Name**
Stability AI Search and Replace
  #### **Description**
    Replace objects without creating masks manually.
    Describe what to find and what to replace it with.
    
    Available on AWS Bedrock and direct API.
    No mask required - AI automatically segments.
    
  #### **Code Example**
    import requests
    import base64
    from pathlib import Path
    
    STABILITY_API_KEY = os.environ["STABILITY_API_KEY"]
    
    def search_and_replace(
        image_path: str,
        search_prompt: str,
        replace_prompt: str,
        output_path: str = "output.png"
    ):
        """Replace objects in image by description."""
    
        with open(image_path, "rb") as f:
            image_data = f.read()
    
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*",
            },
            files={
                "image": image_data,
            },
            data={
                "search_prompt": search_prompt,
                "prompt": replace_prompt,
                "output_format": "png",
            },
        )
    
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    # Usage
    search_and_replace(
        image_path="room.png",
        search_prompt="old wooden chair",
        replace_prompt="modern ergonomic office chair",
        output_path="room_updated.png"
    )
    
    # Erase object (replace with background)
    def erase_object(image_path: str, mask_path: str, output_path: str):
        """Remove object and fill with background."""
    
        with open(image_path, "rb") as img_f:
            image_data = img_f.read()
        with open(mask_path, "rb") as mask_f:
            mask_data = mask_f.read()
    
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/edit/erase",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*",
            },
            files={
                "image": image_data,
                "mask": mask_data,  # White = area to erase
            },
            data={
                "output_format": "png",
            },
        )
    
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
    
    # Remove background
    def remove_background(image_path: str, output_path: str):
        """Remove background, return transparent PNG."""
    
        with open(image_path, "rb") as f:
            image_data = f.read()
    
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/edit/remove-background",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*",
            },
            files={"image": image_data},
            data={"output_format": "png"},
        )
    
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Vague search prompts
      ###### **Why**
AI may match wrong objects
      ###### **Fix**
Be specific: 'red leather sofa' not 'furniture'
    
---
      ###### **Pattern**
Not handling rate limits
      ###### **Why**
API has usage limits
      ###### **Fix**
Add retry logic with exponential backoff
  #### **References**
    - https://platform.stability.ai/docs/api-reference
    - https://aws.amazon.com/bedrock/stability-ai/

---
  #### **Id**
outpainting-extend
  #### **Name**
Outpainting and Image Extension
  #### **Description**
    Extend images beyond original boundaries.
    AI generates seamless content matching style.
    
    Key concepts:
    - Extend in any direction (left, right, up, down)
    - Maintain color/style consistency
    - Handle aspect ratio changes
    
  #### **Code Example**
    import replicate
    import requests
    from PIL import Image
    import io
    
    # Method 1: Replicate Flux Fill Pro for outpainting
    def outpaint_replicate(
        image_path: str,
        direction: str = "right",  # left, right, up, down
        extend_pixels: int = 512,
        prompt: str = ""
    ) -> bytes:
        """Extend image in specified direction."""
    
        # Load and prepare image
        img = Image.open(image_path)
        orig_w, orig_h = img.size
    
        # Calculate new canvas size
        if direction == "right":
            new_w, new_h = orig_w + extend_pixels, orig_h
            paste_pos = (0, 0)
        elif direction == "left":
            new_w, new_h = orig_w + extend_pixels, orig_h
            paste_pos = (extend_pixels, 0)
        elif direction == "down":
            new_w, new_h = orig_w, orig_h + extend_pixels
            paste_pos = (0, 0)
        elif direction == "up":
            new_w, new_h = orig_w, orig_h + extend_pixels
            paste_pos = (0, extend_pixels)
    
        # Create expanded canvas with original image
        canvas = Image.new("RGB", (new_w, new_h), (128, 128, 128))
        canvas.paste(img, paste_pos)
    
        # Create mask (white = generate, black = keep)
        mask = Image.new("L", (new_w, new_h), 255)  # All white
        mask_region = Image.new("L", img.size, 0)   # Black for original
        mask.paste(mask_region, paste_pos)
    
        # Convert to bytes
        def to_bytes(pil_img, format="PNG"):
            buf = io.BytesIO()
            pil_img.save(buf, format=format)
            return buf.getvalue()
    
        # Call API
        client = replicate.Client()
        output = client.run(
            "black-forest-labs/flux-fill-pro",
            input={
                "image": to_bytes(canvas),
                "mask": to_bytes(mask),
                "prompt": prompt or "seamless extension of the scene",
            }
        )
    
        return output.read()
    
    # Method 2: Stability AI Outpaint
    def outpaint_stability(
        image_path: str,
        left: int = 0,
        right: int = 512,
        up: int = 0,
        down: int = 0,
        prompt: str = "",
    ):
        """Extend image using Stability AI."""
    
        with open(image_path, "rb") as f:
            image_data = f.read()
    
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/edit/outpaint",
            headers={
                "Authorization": f"Bearer {os.environ['STABILITY_API_KEY']}",
                "Accept": "image/*",
            },
            files={"image": image_data},
            data={
                "left": left,
                "right": right,
                "up": up,
                "down": down,
                "prompt": prompt,
                "output_format": "png",
            },
        )
    
        if response.status_code == 200:
            return response.content
        raise Exception(f"Outpaint failed: {response.text}")
    
    # Usage: Extend for different aspect ratios
    # Portrait to landscape
    result = outpaint_stability(
        "portrait.png",
        left=256,
        right=256,
        prompt="continue the scenic landscape naturally"
    )
    
    # Square to 16:9
    result = outpaint_stability(
        "square.png",
        left=128,
        right=128,
        prompt="extend the environment seamlessly"
    )
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Extending without prompt context
      ###### **Why**
AI may generate inconsistent content
      ###### **Fix**
Provide descriptive prompt matching original style
    
---
      ###### **Pattern**
Very large extensions at once
      ###### **Why**
Quality degrades with massive extensions
      ###### **Fix**
Chain smaller extensions (256-512px each)
  #### **References**
    - https://myaiforce.com/flux-fill-model-inpainting-workflow/
    - https://aws.amazon.com/about-aws/whats-new/2025/10/stability-ai-image-updates-amazon-bedrock/

---
  #### **Id**
controlnet-guidance
  #### **Name**
ControlNet Structure Control
  #### **Description**
    Control image generation with structural guidance.
    
    Control types:
    - Canny: Edge detection, sharp boundaries
    - Depth: 3D spatial relationships
    - Pose: Human body positioning
    - HED/Soft Edge: Organic, softer boundaries
    
    Combine multiple controls for precise results.
    
  #### **Code Example**
    import replicate
    from PIL import Image
    import cv2
    import numpy as np
    
    # Generate Canny edge map
    def create_canny_map(image_path: str, low: int = 100, high: int = 200):
        """Create Canny edge detection map."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(img, low, high)
        return Image.fromarray(edges)
    
    # Use ControlNet on Replicate
    def generate_with_controlnet(
        control_image_path: str,
        prompt: str,
        control_type: str = "canny",  # canny, depth, pose
        control_strength: float = 0.8,
    ):
        """Generate image with ControlNet guidance."""
    
        client = replicate.Client()
    
        # For Flux ControlNet
        if control_type == "canny":
            model = "black-forest-labs/flux-canny-pro"
        elif control_type == "depth":
            model = "black-forest-labs/flux-depth-pro"
        else:
            # Use InstantX Union for flexibility
            model = "xlabs-ai/flux-controlnet"
    
        output = client.run(
            model,
            input={
                "control_image": open(control_image_path, "rb"),
                "prompt": prompt,
                "control_strength": control_strength,
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
            }
        )
    
        return output
    
    # Combining multiple ControlNets
    def multi_controlnet(
        pose_image: str,
        depth_image: str,
        prompt: str,
        pose_strength: float = 0.5,
        depth_strength: float = 0.4,
    ):
        """Combine pose and depth control."""
    
        # Note: Multi-ControlNet requires compatible model
        # Total strength should be ~0.8-1.0 when combined
    
        client = replicate.Client()
    
        output = client.run(
            "xlabs-ai/flux-controlnet",
            input={
                "control_image": open(pose_image, "rb"),
                "control_image_2": open(depth_image, "rb"),
                "control_type": "pose",
                "control_type_2": "depth",
                "control_strength": pose_strength,
                "control_strength_2": depth_strength,
                "prompt": prompt,
            }
        )
    
        return output
    
    # Generate depth map from image
    def create_depth_map(image_path: str):
        """Generate depth map using MiDaS."""
    
        client = replicate.Client()
    
        output = client.run(
            "cjwbw/midas:a6ba5798f04f80d3b314de0f0a62277f21ab3c8a6eb7f3bb0bb9d7e6b62c3c0d",
            input={
                "image": open(image_path, "rb"),
                "model_type": "DPT_Large",
            }
        )
    
        return output
    
    # Practical example: Transform sketch to artwork
    def sketch_to_art(sketch_path: str, style_prompt: str):
        """Convert rough sketch to polished artwork."""
    
        # Create Canny edges from sketch
        canny_map = create_canny_map(sketch_path, low=50, high=150)
        canny_map.save("temp_canny.png")
    
        # Generate with style
        client = replicate.Client()
        output = client.run(
            "black-forest-labs/flux-canny-pro",
            input={
                "control_image": open("temp_canny.png", "rb"),
                "prompt": f"{style_prompt}, high detail, professional",
                "control_strength": 0.75,
            }
        )
    
        return output
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Control strength 1.0 with multiple controls
      ###### **Why**
Combined strength exceeds 1.0, over-constrains generation
      ###### **Fix**
Use 0.4-0.5 per control when combining
    
---
      ###### **Pattern**
Using Canny for organic subjects like faces
      ###### **Why**
Hard edges don't capture facial nuances
      ###### **Fix**
Use depth or soft edge for organic subjects
    
---
      ###### **Pattern**
Wrong resolution control images
      ###### **Why**
Control images must match output resolution
      ###### **Fix**
Resize control image to target dimensions
  #### **References**
    - https://stable-diffusion-art.com/controlnet/
    - https://blog.segmind.com/flux-1-controlnets-what-are-they-all-you-need-to-know/

---
  #### **Id**
image-to-image
  #### **Name**
Image-to-Image Transformation
  #### **Description**
    Transform existing images with style/content changes.
    Control transformation strength to balance original vs new.
    
    Use cases:
    - Style transfer (photo to art)
    - Retexturing (change materials/surfaces)
    - Color grading
    - Detail enhancement
    
  #### **Code Example**
    import replicate
    import fal_client
    
    # Replicate Image-to-Image
    def transform_image_replicate(
        image_path: str,
        prompt: str,
        strength: float = 0.75,  # 0.0 = keep original, 1.0 = ignore original
        model: str = "flux"
    ):
        """Transform image with prompt guidance."""
    
        client = replicate.Client()
    
        if model == "flux":
            output = client.run(
                "black-forest-labs/flux-dev",
                input={
                    "image": open(image_path, "rb"),
                    "prompt": prompt,
                    "prompt_strength": strength,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                }
            )
        else:  # SDXL
            output = client.run(
                "stability-ai/sdxl",
                input={
                    "image": open(image_path, "rb"),
                    "prompt": prompt,
                    "prompt_strength": strength,
                    "num_inference_steps": 25,
                }
            )
    
        return output
    
    # Fal.ai Image-to-Image (fast)
    def transform_image_fal(
        image_url: str,
        prompt: str,
        strength: float = 0.75,
    ):
        """Transform using Fal.ai's fast inference."""
    
        result = fal_client.submit(
            "fal-ai/flux/dev/image-to-image",
            arguments={
                "image_url": image_url,
                "prompt": prompt,
                "strength": strength,
                "num_inference_steps": 28,
            }
        )
    
        return result.get()
    
    # Strength guide:
    # 0.3-0.5: Subtle changes (color grading, minor style)
    # 0.5-0.75: Balanced transformation (recommended)
    # 0.75-0.9: Major changes while keeping composition
    # 0.9-1.0: Nearly complete regeneration
    
    # Style transfer example
    def apply_art_style(photo_path: str, style: str):
        """Convert photo to artistic style."""
    
        style_prompts = {
            "watercolor": "watercolor painting, soft brushstrokes, flowing colors",
            "oil_painting": "oil painting, rich textures, dramatic lighting",
            "anime": "anime style, vibrant colors, clean lines, studio ghibli",
            "pencil_sketch": "detailed pencil sketch, cross-hatching, artistic",
            "cyberpunk": "cyberpunk aesthetic, neon lights, futuristic",
        }
    
        prompt = style_prompts.get(style, style)
    
        return transform_image_replicate(
            photo_path,
            prompt=prompt,
            strength=0.65,  # Preserve composition
        )
    
    # Batch processing
    async def batch_transform(
        images: list[str],
        prompt: str,
        strength: float = 0.75,
    ):
        """Process multiple images concurrently."""
        import asyncio
    
        client = replicate.Client()
    
        async def process_one(image_path: str):
            prediction = client.predictions.create(
                model="black-forest-labs/flux-dev",
                input={
                    "image": open(image_path, "rb"),
                    "prompt": prompt,
                    "prompt_strength": strength,
                }
            )
            return await asyncio.to_thread(
                client.predictions.wait,
                prediction
            )
    
        tasks = [process_one(img) for img in images]
        return await asyncio.gather(*tasks)
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Strength 0.9+ for style transfer
      ###### **Why**
Loses original composition and content
      ###### **Fix**
Use 0.5-0.75 to preserve structure
    
---
      ###### **Pattern**
No negative prompt for quality
      ###### **Why**
May generate artifacts
      ###### **Fix**
Add negative: 'blurry, distorted, low quality'
  #### **References**
    - https://replicate.com/blog/run-sdxl-with-an-api
    - https://www.aifreeapi.com/en/posts/free-image-to-image-api

---
  #### **Id**
multi-step-editing
  #### **Name**
Multi-Step Iterative Editing
  #### **Description**
    Chain multiple editing operations for complex results.
    Each step builds on the previous, enabling sophisticated edits.
    
    Strategy:
    1. Use lower denoise per step
    2. Expand masks gradually
    3. Verify intermediate results
    
  #### **Code Example**
    from PIL import Image
    import replicate
    from typing import Callable
    import io
    
    class ImageEditPipeline:
        """Chain multiple AI editing operations."""
    
        def __init__(self, image_path: str):
            self.image = Image.open(image_path)
            self.history = [self.image.copy()]
            self.client = replicate.Client()
    
        def _image_to_bytes(self, img: Image.Image) -> bytes:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()
    
        def inpaint(
            self,
            mask: Image.Image,
            prompt: str,
            strength: float = 0.75
        ) -> "ImageEditPipeline":
            """Inpaint masked area."""
    
            output = self.client.run(
                "black-forest-labs/flux-fill-pro",
                input={
                    "image": self._image_to_bytes(self.image),
                    "mask": self._image_to_bytes(mask),
                    "prompt": prompt,
                    "strength": strength,
                }
            )
    
            self.image = Image.open(io.BytesIO(output.read()))
            self.history.append(self.image.copy())
            return self
    
        def transform(self, prompt: str, strength: float = 0.5) -> "ImageEditPipeline":
            """Apply image-to-image transformation."""
    
            output = self.client.run(
                "black-forest-labs/flux-dev",
                input={
                    "image": self._image_to_bytes(self.image),
                    "prompt": prompt,
                    "prompt_strength": strength,
                }
            )
    
            self.image = Image.open(io.BytesIO(output.read()))
            self.history.append(self.image.copy())
            return self
    
        def upscale(self, scale: int = 2) -> "ImageEditPipeline":
            """Upscale image resolution."""
    
            output = self.client.run(
                "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
                input={
                    "image": self._image_to_bytes(self.image),
                    "scale": scale,
                }
            )
    
            self.image = Image.open(io.BytesIO(output.read()))
            self.history.append(self.image.copy())
            return self
    
        def undo(self) -> "ImageEditPipeline":
            """Revert to previous state."""
            if len(self.history) > 1:
                self.history.pop()
                self.image = self.history[-1].copy()
            return self
    
        def save(self, path: str):
            """Save current result."""
            self.image.save(path)
            return self
    
    # Usage: Complex product photo editing
    def edit_product_photo(image_path: str):
        """Multi-step product photo enhancement."""
    
        pipeline = ImageEditPipeline(image_path)
    
        # Step 1: Clean up background
        bg_mask = create_background_mask(image_path)
        pipeline.inpaint(
            mask=bg_mask,
            prompt="clean white studio background, professional product photography",
            strength=0.6
        )
    
        # Step 2: Enhance product lighting
        pipeline.transform(
            prompt="professional product photography, soft studio lighting, high-end commercial",
            strength=0.3  # Subtle enhancement
        )
    
        # Step 3: Upscale for high resolution
        pipeline.upscale(scale=2)
    
        # Save result
        pipeline.save("product_enhanced.png")
    
        return pipeline
    
    # Iterative inpainting with mask expansion
    def iterative_inpaint(
        image_path: str,
        base_mask: Image.Image,
        prompt: str,
        iterations: int = 3,
    ):
        """Inpaint with gradually expanding mask."""
    
        from scipy.ndimage import binary_dilation
        import numpy as np
    
        pipeline = ImageEditPipeline(image_path)
        current_mask = np.array(base_mask)
    
        # Decreasing strength per iteration
        strengths = [0.7, 0.5, 0.3]
    
        for i in range(iterations):
            # Expand mask slightly each iteration
            if i > 0:
                current_mask = binary_dilation(current_mask, iterations=10)
    
            mask_img = Image.fromarray(current_mask.astype(np.uint8) * 255)
    
            pipeline.inpaint(
                mask=mask_img,
                prompt=prompt,
                strength=strengths[min(i, len(strengths)-1)]
            )
    
        return pipeline
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
Single high-denoise pass for complex edits
      ###### **Why**
Hard to control, may produce artifacts
      ###### **Fix**
Use multiple passes with decreasing strength
    
---
      ###### **Pattern**
No history/undo capability
      ###### **Why**
Can't recover from bad edits
      ###### **Fix**
Maintain edit history for rollback
  #### **References**
    - https://docs.comfy.org/tutorials/basic/inpaint
    - https://medium.com/@techlatest.net/inpainting-and-outpainting-techniques-in-comfyui-d708d3ea690d

---
  #### **Id**
content-moderation
  #### **Name**
Content Moderation for Generated Images
  #### **Description**
    Ensure generated images comply with content policies.
    Check both inputs and outputs for safety.
    
    Key concerns:
    - NSFW/explicit content
    - Violence/gore
    - Hate symbols
    - Deepfakes/impersonation
    
  #### **Code Example**
    import requests
    import openai
    from typing import Tuple
    from enum import Enum
    
    class ContentRating(Enum):
        SAFE = "safe"
        WARNING = "warning"
        BLOCKED = "blocked"
    
    # OpenAI Moderation API (free)
    def check_prompt_safety(prompt: str) -> Tuple[bool, dict]:
        """Check if prompt is safe for image generation."""
    
        client = openai.OpenAI()
    
        response = client.moderations.create(input=prompt)
        result = response.results[0]
    
        # Check relevant categories
        flags = {
            "sexual": result.categories.sexual,
            "violence": result.categories.violence,
            "hate": result.categories.hate,
            "self_harm": result.categories.self_harm,
        }
    
        is_safe = not any(flags.values())
        return is_safe, flags
    
    # Image moderation with dedicated API
    def moderate_image(image_url: str) -> ContentRating:
        """Check generated image for policy violations."""
    
        # Using SightEngine API
        response = requests.get(
            "https://api.sightengine.com/1.0/check.json",
            params={
                "url": image_url,
                "models": "nudity-2.1,offensive,gore",
                "api_user": os.environ["SIGHTENGINE_USER"],
                "api_secret": os.environ["SIGHTENGINE_SECRET"],
            }
        )
    
        result = response.json()
    
        # Check nudity
        nudity = result.get("nudity", {})
        if nudity.get("sexual_activity", 0) > 0.5:
            return ContentRating.BLOCKED
        if nudity.get("sexual_display", 0) > 0.5:
            return ContentRating.BLOCKED
    
        # Check violence
        if result.get("gore", {}).get("prob", 0) > 0.5:
            return ContentRating.BLOCKED
    
        # Check offensive content
        if result.get("offensive", {}).get("prob", 0) > 0.7:
            return ContentRating.WARNING
    
        return ContentRating.SAFE
    
    # Safe generation wrapper
    class SafeImageGenerator:
        """Generate images with content safety checks."""
    
        def __init__(self, replicate_client):
            self.client = replicate_client
    
        def generate(
            self,
            prompt: str,
            **kwargs
        ) -> dict:
            """Generate image with safety checks."""
    
            # Pre-check prompt
            is_safe, flags = check_prompt_safety(prompt)
            if not is_safe:
                return {
                    "success": False,
                    "error": "Prompt blocked by content policy",
                    "flags": flags,
                }
    
            # Generate image
            try:
                output = self.client.run(
                    "black-forest-labs/flux-schnell",
                    input={
                        "prompt": prompt,
                        "safety_checker": True,  # Enable model's safety
                        **kwargs
                    }
                )
    
                image_url = output[0] if isinstance(output, list) else str(output)
    
                # Post-check generated image
                rating = moderate_image(image_url)
    
                if rating == ContentRating.BLOCKED:
                    return {
                        "success": False,
                        "error": "Generated image blocked by content policy",
                    }
    
                return {
                    "success": True,
                    "image_url": image_url,
                    "content_rating": rating.value,
                }
    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                }
    
    # Usage
    generator = SafeImageGenerator(replicate.Client())
    result = generator.generate(
        prompt="professional headshot of a business person",
        num_outputs=1
    )
    
    if result["success"]:
        print(f"Image: {result['image_url']}")
    else:
        print(f"Blocked: {result['error']}")
    
  #### **Anti Patterns**
    
---
      ###### **Pattern**
No content moderation in production
      ###### **Why**
Users may generate harmful content
      ###### **Fix**
Always check prompts and outputs
    
---
      ###### **Pattern**
Only checking prompts, not outputs
      ###### **Why**
Safe prompts can still produce unsafe images
      ###### **Fix**
Check both input prompts and output images
  #### **References**
    - https://www.edenai.co/post/best-image-moderation-apis
    - https://medium.com/@API4AI/automated-nsfw-detection-the-2025-content-safety-playbook-7ac82fd2f351