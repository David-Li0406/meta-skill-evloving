---
id: video-generation
name: "Video Generation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Video Generation

## Overview

AI video generation creates video content from text prompts, images, or other videos. Modern models like Sora, Runway Gen-3, and Pika can generate realistic videos with complex motion, physics, and scene understanding.

## When to Use

- Marketing and advertising content
- Social media content creation
- Product demonstrations
- Educational content
- Film and animation prototyping
- Video editing and enhancement
- Creative exploration

## Key Concepts

### Video Generation Services

| Service | Quality | Duration | Resolution | Access |
|---------|---------|----------|------------|--------|
| OpenAI Sora | Highest | 60s | 1080p | Limited |
| Runway Gen-3 | Very High | 10s | 1080p | API |
| Pika | High | 4s | 1080p | API |
| Stable Video | Good | 4s | 1024x576 | Open |
| Luma Dream Machine | High | 5s | 720p | API |
| Kling | Very High | 5s | 1080p | API |

### Generation Types

| Type | Input | Output |
|------|-------|--------|
| Text-to-Video | Text prompt | Video |
| Image-to-Video | Image + prompt | Video animating image |
| Video-to-Video | Video + prompt | Modified video |
| Interpolation | Frames | Smooth video |

## Implementation

### Runway Gen-3 Integration

```python
import runwayml
from typing import Optional
import time

class RunwayVideoGenerator:
    """Generate videos using Runway Gen-3."""

    def __init__(self):
        self.client = runwayml.RunwayML()

    def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,  # seconds
        aspect_ratio: str = "16:9",
        seed: Optional[int] = None
    ) -> dict:
        """Generate video from text prompt."""
        task = self.client.image_to_video.create(
            model="gen3a_turbo",
            prompt_text=prompt,
            duration=duration,
            ratio=aspect_ratio,
            seed=seed
        )

        return self._wait_for_completion(task.id)

    def generate_from_image(
        self,
        image_url: str,
        prompt: str,
        duration: int = 5,
        motion_intensity: float = 0.5
    ) -> dict:
        """Generate video from image + prompt."""
        task = self.client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=image_url,
            prompt_text=prompt,
            duration=duration
        )

        return self._wait_for_completion(task.id)

    def _wait_for_completion(
        self,
        task_id: str,
        timeout: int = 300
    ) -> dict:
        """Poll for task completion."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            task = self.client.tasks.retrieve(task_id)

            if task.status == "SUCCEEDED":
                return {
                    "status": "success",
                    "video_url": task.output[0],
                    "task_id": task_id
                }
            elif task.status == "FAILED":
                return {
                    "status": "failed",
                    "error": task.failure,
                    "task_id": task_id
                }

            time.sleep(5)

        return {
            "status": "timeout",
            "task_id": task_id
        }
```

### Replicate Video Models

```python
import replicate
from typing import List, Optional

class ReplicateVideoGenerator:
    """Generate videos using Replicate models."""

    def generate_stable_video(
        self,
        image_path: str,
        motion_bucket_id: int = 127,
        fps: int = 7,
        num_frames: int = 25
    ) -> str:
        """Generate video from image using Stable Video Diffusion."""
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            input={
                "input_image": open(image_path, "rb"),
                "motion_bucket_id": motion_bucket_id,
                "fps": fps,
                "num_frames": num_frames
            }
        )
        return output

    def generate_with_animatediff(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_frames: int = 16,
        guidance_scale: float = 7.5
    ) -> str:
        """Generate video using AnimateDiff."""
        output = replicate.run(
            "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48c9f",
            input={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale
            }
        )
        return output

    def generate_with_zeroscope(
        self,
        prompt: str,
        num_frames: int = 24,
        fps: int = 8,
        width: int = 576,
        height: int = 320
    ) -> str:
        """Generate video using Zeroscope."""
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
            input={
                "prompt": prompt,
                "num_frames": num_frames,
                "fps": fps,
                "width": width,
                "height": height
            }
        )
        return output
```

### Luma Dream Machine

```python
import requests
from typing import Optional
import time

class LumaVideoGenerator:
    """Generate videos using Luma AI Dream Machine."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        loop: bool = False
    ) -> dict:
        """Generate video from text prompt."""
        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "loop": loop
            }
        )

        generation = response.json()
        return self._wait_for_completion(generation["id"])

    def generate_from_image(
        self,
        prompt: str,
        image_url: str,
        keyframes: dict = None
    ) -> dict:
        """Generate video from image."""
        payload = {
            "prompt": prompt,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": image_url
                }
            }
        }

        if keyframes:
            payload["keyframes"].update(keyframes)

        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )

        return self._wait_for_completion(response.json()["id"])

    def extend_video(
        self,
        video_id: str,
        prompt: str
    ) -> dict:
        """Extend existing video."""
        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "keyframes": {
                    "frame0": {
                        "type": "generation",
                        "id": video_id
                    }
                }
            }
        )

        return self._wait_for_completion(response.json()["id"])

    def _wait_for_completion(self, generation_id: str) -> dict:
        """Wait for video generation to complete."""
        while True:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            generation = response.json()

            if generation["state"] == "completed":
                return {
                    "status": "success",
                    "video_url": generation["assets"]["video"],
                    "id": generation_id
                }
            elif generation["state"] == "failed":
                return {
                    "status": "failed",
                    "error": generation.get("failure_reason"),
                    "id": generation_id
                }

            time.sleep(5)
```

### Video Prompt Engineering

```python
class VideoPromptBuilder:
    """Build effective prompts for video generation."""

    def __init__(self):
        self.components = {
            "subject": "",
            "action": "",
            "setting": "",
            "camera": "",
            "style": "",
            "lighting": "",
            "details": []
        }

    def set_subject(self, subject: str):
        """Set main subject."""
        self.components["subject"] = subject
        return self

    def set_action(self, action: str):
        """Set the action/motion."""
        self.components["action"] = action
        return self

    def set_setting(self, setting: str):
        """Set the environment/background."""
        self.components["setting"] = setting
        return self

    def set_camera(self, camera: str):
        """Set camera movement/angle."""
        # Camera options
        camera_movements = {
            "static": "static camera, locked shot",
            "pan_left": "smooth pan left",
            "pan_right": "smooth pan right",
            "dolly_in": "dolly in, moving closer",
            "dolly_out": "dolly out, pulling back",
            "tracking": "tracking shot, following subject",
            "crane": "crane shot, rising up",
            "handheld": "handheld camera, slight shake",
            "drone": "aerial drone shot",
            "orbit": "orbiting around subject"
        }
        self.components["camera"] = camera_movements.get(camera, camera)
        return self

    def set_style(self, style: str):
        """Set visual style."""
        styles = {
            "cinematic": "cinematic, film quality, 35mm",
            "documentary": "documentary style, natural",
            "commercial": "commercial quality, polished",
            "artistic": "artistic, stylized",
            "anime": "anime style, animation",
            "realistic": "photorealistic, lifelike"
        }
        self.components["style"] = styles.get(style, style)
        return self

    def set_lighting(self, lighting: str):
        """Set lighting conditions."""
        self.components["lighting"] = lighting
        return self

    def add_detail(self, detail: str):
        """Add specific detail."""
        self.components["details"].append(detail)
        return self

    def build(self) -> str:
        """Build final prompt."""
        parts = []

        if self.components["subject"]:
            parts.append(self.components["subject"])

        if self.components["action"]:
            parts.append(self.components["action"])

        if self.components["setting"]:
            parts.append(f"in {self.components['setting']}")

        if self.components["camera"]:
            parts.append(self.components["camera"])

        if self.components["style"]:
            parts.append(self.components["style"])

        if self.components["lighting"]:
            parts.append(self.components["lighting"])

        parts.extend(self.components["details"])

        return ", ".join(parts)

# Usage
prompt = (
    VideoPromptBuilder()
    .set_subject("a golden retriever")
    .set_action("running through a field of sunflowers")
    .set_setting("sunny countryside")
    .set_camera("tracking")
    .set_style("cinematic")
    .set_lighting("golden hour lighting")
    .add_detail("slow motion")
    .add_detail("4K quality")
    .build()
)
```

### Video Processing Utilities

```python
import subprocess
from pathlib import Path
from typing import List, Optional

class VideoProcessor:
    """Utilities for video processing."""

    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """Get video metadata using ffprobe."""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        import json
        return json.loads(result.stdout)

    @staticmethod
    def extract_frames(
        video_path: str,
        output_dir: str,
        fps: int = 1
    ) -> List[str]:
        """Extract frames from video."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps}",
            f"{output_dir}/frame_%04d.png"
        ]

        subprocess.run(cmd, check=True)

        return sorted(Path(output_dir).glob("frame_*.png"))

    @staticmethod
    def create_video_from_frames(
        frame_pattern: str,
        output_path: str,
        fps: int = 24
    ):
        """Create video from image sequence."""
        cmd = [
            "ffmpeg",
            "-framerate", str(fps),
            "-i", frame_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def concatenate_videos(
        video_paths: List[str],
        output_path: str
    ):
        """Concatenate multiple videos."""
        # Create file list
        list_path = "/tmp/video_list.txt"
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)
        Path(list_path).unlink()

    @staticmethod
    def add_audio(
        video_path: str,
        audio_path: str,
        output_path: str
    ):
        """Add audio track to video."""
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def resize_video(
        video_path: str,
        output_path: str,
        width: int,
        height: int
    ):
        """Resize video to specific dimensions."""
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"scale={width}:{height}",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def loop_video(
        video_path: str,
        output_path: str,
        loop_count: int = 3
    ):
        """Loop video multiple times."""
        cmd = [
            "ffmpeg",
            "-stream_loop", str(loop_count - 1),
            "-i", video_path,
            "-c", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)
```

### Production Video Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging
import asyncio

class VideoProvider(Enum):
    RUNWAY = "runway"
    LUMA = "luma"
    REPLICATE = "replicate"

@dataclass
class VideoGenerationConfig:
    provider: VideoProvider = VideoProvider.REPLICATE
    default_duration: int = 5
    default_aspect_ratio: str = "16:9"
    max_retries: int = 3
    timeout: int = 600
    output_dir: str = "./generated_videos"

class VideoGenerationService:
    """Production video generation service."""

    def __init__(self, config: Optional[VideoGenerationConfig] = None):
        self.config = config or VideoGenerationConfig()
        self.logger = logging.getLogger(__name__)
        Path(self.config.output_dir).mkdir(exist_ok=True)

    async def generate(
        self,
        prompt: str,
        provider: Optional[VideoProvider] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from prompt."""
        provider = provider or self.config.provider

        for attempt in range(self.config.max_retries):
            try:
                if provider == VideoProvider.RUNWAY:
                    result = await self._generate_runway(prompt, **kwargs)
                elif provider == VideoProvider.LUMA:
                    result = await self._generate_luma(prompt, **kwargs)
                else:
                    result = await self._generate_replicate(prompt, **kwargs)

                if result["status"] == "success":
                    # Download video
                    output_path = await self._download_video(
                        result["video_url"],
                        prompt[:50]
                    )
                    result["local_path"] = output_path

                return result

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    return {"status": "failed", "error": str(e)}

        return {"status": "failed", "error": "Max retries exceeded"}

    async def generate_from_image(
        self,
        image_path: str,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from image."""
        # Upload image and get URL
        image_url = await self._upload_image(image_path)

        # Generate with image
        return await self.generate(
            prompt,
            image_url=image_url,
            **kwargs
        )

    async def _generate_runway(self, prompt: str, **kwargs) -> Dict:
        """Generate using Runway."""
        generator = RunwayVideoGenerator()
        return generator.generate_from_text(
            prompt,
            duration=kwargs.get("duration", self.config.default_duration),
            aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio)
        )

    async def _generate_luma(self, prompt: str, **kwargs) -> Dict:
        """Generate using Luma."""
        import os
        generator = LumaVideoGenerator(os.environ.get("LUMA_API_KEY"))
        return generator.generate(
            prompt,
            aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio)
        )

    async def _generate_replicate(self, prompt: str, **kwargs) -> Dict:
        """Generate using Replicate."""
        generator = ReplicateVideoGenerator()
        video_url = generator.generate_with_zeroscope(prompt)
        return {"status": "success", "video_url": video_url}

    async def _download_video(self, url: str, name: str) -> str:
        """Download video from URL."""
        import httpx
        import re

        # Clean filename
        clean_name = re.sub(r'[^\w\s-]', '', name).strip()[:50]
        output_path = Path(self.config.output_dir) / f"{clean_name}.mp4"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            with open(output_path, "wb") as f:
                f.write(response.content)

        return str(output_path)

    async def _upload_image(self, image_path: str) -> str:
        """Upload image and get URL."""
        # Implementation depends on storage service
        # Could use S3, Cloudinary, etc.
        pass

    async def extend_video(
        self,
        video_path: str,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Extend existing video."""
        # Extract last frame
        processor = VideoProcessor()
        frames_dir = "/tmp/extend_frames"
        frames = processor.extract_frames(video_path, frames_dir, fps=1)

        if not frames:
            return {"status": "failed", "error": "Could not extract frames"}

        last_frame = str(frames[-1])

        # Generate continuation
        result = await self.generate_from_image(last_frame, prompt, **kwargs)

        if result["status"] == "success":
            # Concatenate videos
            output_path = str(Path(video_path).with_suffix(".extended.mp4"))
            processor.concatenate_videos(
                [video_path, result["local_path"]],
                output_path
            )
            result["extended_path"] = output_path

        return result
```

## Best Practices

1. **Prompt Quality**
   - Describe motion explicitly
   - Specify camera movements
   - Include style and lighting
   - Keep prompts focused

2. **Generation Settings**
   - Start with short durations
   - Use appropriate aspect ratios
   - Test different seeds

3. **Iteration**
   - Generate multiple versions
   - Refine prompts based on results
   - Use image-to-video for control

4. **Post-Processing**
   - Add music/sound effects
   - Color grade if needed
   - Trim/edit generated content

5. **Cost Management**
   - Start with cheaper models
   - Cache successful generations
   - Use appropriate quality levels

## Common Pitfalls

1. **Vague Motion** - Not specifying how things move
2. **Wrong Duration** - Videos too short/long
3. **No Camera Specified** - Random camera movements
4. **Conflicting Elements** - Too many things happening
5. **Ignoring Physics** - Unrealistic expectations
6. **No Style Guidance** - Inconsistent aesthetics

## References

- [Runway ML](https://runwayml.com/)
- [Luma AI](https://lumalabs.ai/)
- [Stable Video Diffusion](https://stability.ai/stable-video)
- [Pika](https://pika.art/)
