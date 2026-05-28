#!/usr/bin/env python3
"""
AI-powered diagram generation using Nano Banana Pro.

This script uses a smart iterative refinement approach:
1. Generate initial diagram with Nano Banana Pro (Gemini 3 Pro Image)
2. AI quality review using Gemini 3 Pro for professional critique
3. Only regenerate if quality is below threshold for document type
4. Repeat until quality meets standards (max iterations)

Requirements:
    - OPENROUTER_API_KEY environment variable
    - Python 3.8+ (uses stdlib only, no external dependencies)

Usage:
    python generate_diagram_ai.py "Create a flowchart showing user authentication flow" -o flowchart.png
    python generate_diagram_ai.py "System architecture diagram for microservices" -o architecture.png --doc-type architecture
    python generate_diagram_ai.py "Simple block diagram" -o diagram.png --doc-type presentation
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import socket
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple


def _load_env_file():
    """Load .env file from current directory or parent directories.

    Returns True if a .env file was found and loaded, False otherwise.
    Note: This does NOT override existing environment variables.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return False

    # Try current working directory first
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        return True

    # Try parent directories (up to 5 levels)
    cwd = Path.cwd()
    for _ in range(5):
        env_path = cwd / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        cwd = cwd.parent
        if cwd == cwd.parent:
            break

    # Try the script's parent directory
    script_dir = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        script_dir = script_dir.parent
        if script_dir == script_dir.parent:
            break

    return False


class NanoBananaGenerator:
    """Generate diagrams using Nano Banana Pro with smart iterative refinement.

    Uses Gemini 3 Pro for quality review to determine if regeneration is needed.
    Multiple passes only occur if the generated diagram doesn't meet the
    quality threshold for the target document type.
    """

    # Quality thresholds by document type (score out of 10)
    QUALITY_THRESHOLDS = {
        # Technical/Project doc types
        "specification": 8.5,  # Technical specs, PRDs - highest standards
        "architecture": 8.0,   # Architecture documents - high standards
        "proposal": 8.0,       # Business proposals - must be compelling
        "sprint": 7.5,         # Sprint planning docs - professional
        "readme": 7.0,         # README files - good quality
        # Academic/Scientific doc types
        "journal": 8.5,        # Nature, Science, etc. - highest standards
        "conference": 8.0,     # Conference papers - high standards
        "poster": 7.0,         # Academic posters - good quality
        "presentation": 6.5,   # Slides/talks - clear but less formal
        "report": 7.5,         # Technical reports - professional
        "grant": 8.0,          # Grant proposals - must be compelling
        "thesis": 8.0,         # Dissertations - formal academic
        "preprint": 7.5,       # arXiv, etc. - good quality
        "default": 7.5,        # Default threshold
    }

    # Diagram generation guidelines
    DIAGRAM_GUIDELINES = """
Create a high-quality technical diagram with these requirements:

VISUAL QUALITY:
- Clean white or light background (no textures or gradients)
- High contrast for readability and printing
- Professional, publication-ready appearance
- Sharp, clear lines and text
- Adequate spacing between elements to prevent crowding

TYPOGRAPHY:
- Clear, readable sans-serif fonts (Arial, Helvetica style)
- Minimum 10pt font size for all labels
- Consistent font sizes throughout
- All text horizontal or clearly readable
- No overlapping text

TECHNICAL STANDARDS:
- Accurate representation of concepts
- Clear labels for all components
- Include legends where appropriate
- Use standard notation and symbols
- Logical grouping of related elements

ACCESSIBILITY:
- Colorblind-friendly color palette (use Okabe-Ito colors if using color)
- High contrast between elements
- Redundant encoding (shapes + colors, not just colors)
- Works well in grayscale

LAYOUT:
- Logical flow (left-to-right or top-to-bottom)
- Clear visual hierarchy
- Balanced composition
- Appropriate use of whitespace
- No clutter or unnecessary decorative elements
"""

    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize the generator.

        Args:
            api_key: OpenRouter API key (or use OPENROUTER_API_KEY env var)
            verbose: Print detailed progress information
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            _load_env_file()
            self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please either:\n"
                "  1. Set the OPENROUTER_API_KEY environment variable\n"
                "  2. Add OPENROUTER_API_KEY to your .env file\n"
                "  3. Pass api_key parameter to the constructor\n"
                "Get your API key from: https://openrouter.ai/keys"
            )

        self.verbose = verbose
        self._last_error = None
        self.base_url = "https://openrouter.ai/api/v1"
        # Nano Banana Pro - Google's Gemini 3 Pro image generation
        self.image_model = "google/gemini-3-pro-image-preview"
        # Gemini 3 Pro for quality review
        self.review_model = "google/gemini-3-pro"

    def _log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def _make_request(self, model: str, messages: List[Dict[str, Any]],
                     modalities: Optional[List[str]] = None) -> Dict[str, Any]:
        """Make a request to OpenRouter API using stdlib (zero external dependencies)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/flight505/nano-banana",
            "X-Title": "Nano Banana Diagram Generator"
        }

        payload = {
            "model": model,
            "messages": messages
        }

        if modalities:
            payload["modalities"] = modalities

        self._log(f"Making request to {model}...")

        url = f"{self.base_url}/chat/completions"
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                response_body = response.read().decode("utf-8")
                try:
                    return json.loads(response_body)
                except json.JSONDecodeError:
                    return {"raw_text": response_body[:500]}

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
                error_json = json.loads(error_body)
                error_detail = error_json.get("error", error_json)
            except (json.JSONDecodeError, Exception):
                error_detail = error_body or str(e)
            self._log(f"HTTP {e.code}: {error_detail}")
            raise RuntimeError(f"API request failed (HTTP {e.code}): {error_detail}")

        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                raise RuntimeError("API request timed out after 120 seconds")
            raise RuntimeError(f"API request failed: {e.reason}")

        except socket.timeout:
            raise RuntimeError("API request timed out after 120 seconds")

    def _extract_image_from_response(self, response: Dict[str, Any]) -> Optional[bytes]:
        """Extract base64-encoded image from API response."""
        try:
            choices = response.get("choices", [])
            if not choices:
                self._log("No choices in response")
                return None

            message = choices[0].get("message", {})

            # Nano Banana Pro returns images in the 'images' field
            images = message.get("images", [])
            if images and len(images) > 0:
                self._log(f"Found {len(images)} image(s) in 'images' field")

                first_image = images[0]
                if isinstance(first_image, dict):
                    if first_image.get("type") == "image_url":
                        url = first_image.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")

                        if url and url.startswith("data:image"):
                            if "," in url:
                                base64_str = url.split(",", 1)[1]
                                base64_str = base64_str.replace('\n', '').replace('\r', '').replace(' ', '')
                                self._log(f"Extracted base64 data (length: {len(base64_str)})")
                                return base64.b64decode(base64_str)

            # Fallback: check content field
            content = message.get("content", "")

            if isinstance(content, str) and "data:image" in content:
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\n\r]+)', content, re.DOTALL)
                if match:
                    base64_str = match.group(1).replace('\n', '').replace('\r', '').replace(' ', '')
                    self._log(f"Found image in content field (length: {len(base64_str)})")
                    return base64.b64decode(base64_str)

            if isinstance(content, list):
                for i, block in enumerate(content):
                    if isinstance(block, dict) and block.get("type") == "image_url":
                        url = block.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url and url.startswith("data:image") and "," in url:
                            base64_str = url.split(",", 1)[1].replace('\n', '').replace('\r', '').replace(' ', '')
                            self._log(f"Found image in content block {i}")
                            return base64.b64decode(base64_str)

            self._log("No image data found in response")
            return None

        except Exception as e:
            self._log(f"Error extracting image: {str(e)}")
            return None

    def _image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 data URL."""
        with open(image_path, "rb") as f:
            image_data = f.read()

        ext = Path(image_path).suffix.lower()
        mime_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }.get(ext, "image/png")

        base64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

    def generate_image(self, prompt: str) -> Optional[bytes]:
        """Generate an image using Nano Banana Pro."""
        self._last_error = None

        messages = [{"role": "user", "content": prompt}]

        try:
            response = self._make_request(
                model=self.image_model,
                messages=messages,
                modalities=["image", "text"]
            )

            if "error" in response:
                error_msg = response["error"]
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("message", str(error_msg))
                self._last_error = f"API Error: {error_msg}"
                print(f"✗ {self._last_error}")
                return None

            image_data = self._extract_image_from_response(response)
            if image_data:
                self._log(f"✓ Generated image ({len(image_data)} bytes)")
            else:
                self._last_error = "No image data in API response"
                self._log(f"✗ {self._last_error}")

            return image_data
        except RuntimeError as e:
            self._last_error = str(e)
            self._log(f"✗ Generation failed: {self._last_error}")
            return None
        except Exception as e:
            self._last_error = f"Unexpected error: {str(e)}"
            self._log(f"✗ Generation failed: {self._last_error}")
            return None

    def review_image(self, image_path: str, original_prompt: str,
                    iteration: int, doc_type: str = "default",
                    max_iterations: int = 2) -> Tuple[str, float, bool]:
        """Review generated image using Gemini 3 Pro for quality analysis."""
        image_data_url = self._image_to_base64(image_path)
        threshold = self.QUALITY_THRESHOLDS.get(doc_type.lower(),
                                                 self.QUALITY_THRESHOLDS["default"])

        review_prompt = f"""You are an expert reviewer evaluating a technical diagram for publication quality.

ORIGINAL REQUEST: {original_prompt}

DOCUMENT TYPE: {doc_type} (quality threshold: {threshold}/10)
ITERATION: {iteration}/{max_iterations}

Evaluate this diagram on these criteria:

1. **Technical Accuracy** (0-2 points) - Correct representation of concepts
2. **Clarity and Readability** (0-2 points) - Easy to understand at a glance
3. **Label Quality** (0-2 points) - All elements labeled, readable fonts
4. **Layout and Composition** (0-2 points) - Logical flow, balanced space
5. **Professional Appearance** (0-2 points) - Publication-ready quality

RESPOND IN THIS EXACT FORMAT:
SCORE: [total score 0-10]

STRENGTHS:
- [strength 1]
- [strength 2]

ISSUES:
- [issue 1 if any]
- [issue 2 if any]

VERDICT: [ACCEPTABLE or NEEDS_IMPROVEMENT]

If score >= {threshold}, the diagram is ACCEPTABLE for {doc_type}.
If score < {threshold}, mark as NEEDS_IMPROVEMENT with specific suggestions."""

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": review_prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]

        try:
            response = self._make_request(model=self.review_model, messages=messages)

            choices = response.get("choices", [])
            if not choices:
                return "Image generated successfully", 8.0, False

            message = choices[0].get("message", {})
            content = message.get("content", "")

            reasoning = message.get("reasoning", "")
            if reasoning and not content:
                content = reasoning

            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)

            # Extract score
            score = 7.5
            score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', content, re.IGNORECASE)
            if score_match:
                score = float(score_match.group(1))
            else:
                score_match = re.search(r'(?:score|rating|quality)[:\s]+(\d+(?:\.\d+)?)', content, re.IGNORECASE)
                if score_match:
                    score = float(score_match.group(1))

            needs_improvement = False
            if "NEEDS_IMPROVEMENT" in content.upper():
                needs_improvement = True
            elif score < threshold:
                needs_improvement = True

            self._log(f"✓ Review complete (Score: {score}/10, Threshold: {threshold}/10)")

            return (content if content else "Image generated successfully", score, needs_improvement)
        except Exception as e:
            self._log(f"Review skipped: {str(e)}")
            return "Image generated successfully (review skipped)", 7.5, False

    def improve_prompt(self, original_prompt: str, critique: str, iteration: int) -> str:
        """Improve the generation prompt based on critique."""
        return f"""{self.DIAGRAM_GUIDELINES}

USER REQUEST: {original_prompt}

ITERATION {iteration}: Based on previous feedback, address these specific improvements:
{critique}

Generate an improved version that addresses all the critique points while maintaining technical accuracy and professional quality."""

    def generate_iterative(self, user_prompt: str, output_path: str,
                          iterations: int = 2,
                          doc_type: str = "default") -> Dict[str, Any]:
        """Generate diagram with smart iterative refinement."""
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        base_name = output_path.stem
        extension = output_path.suffix or ".png"

        threshold = self.QUALITY_THRESHOLDS.get(doc_type.lower(),
                                                 self.QUALITY_THRESHOLDS["default"])

        results = {
            "user_prompt": user_prompt,
            "doc_type": doc_type,
            "quality_threshold": threshold,
            "iterations": [],
            "final_image": None,
            "final_score": 0.0,
            "success": False,
            "early_stop": False,
            "early_stop_reason": None
        }

        current_prompt = f"""{self.DIAGRAM_GUIDELINES}

USER REQUEST: {user_prompt}

Generate a publication-quality technical diagram that meets all the guidelines above."""

        print(f"\n{'='*60}")
        print(f"🍌 Nano Banana - Generating Diagram")
        print(f"{'='*60}")
        print(f"Description: {user_prompt}")
        print(f"Document Type: {doc_type}")
        print(f"Quality Threshold: {threshold}/10")
        print(f"Max Iterations: {iterations}")
        print(f"Output: {output_path}")
        print(f"{'='*60}\n")

        for i in range(1, iterations + 1):
            print(f"\n[Iteration {i}/{iterations}]")
            print("-" * 40)

            print(f"Generating diagram...")
            image_data = self.generate_image(current_prompt)

            if not image_data:
                error_msg = getattr(self, '_last_error', 'Image generation failed')
                print(f"✗ Generation failed: {error_msg}")
                results["iterations"].append({
                    "iteration": i,
                    "success": False,
                    "error": error_msg
                })
                continue

            iter_path = output_dir / f"{base_name}_v{i}{extension}"
            with open(iter_path, "wb") as f:
                f.write(image_data)
            print(f"✓ Saved: {iter_path}")

            print(f"Reviewing with Gemini 3 Pro...")
            critique, score, needs_improvement = self.review_image(
                str(iter_path), user_prompt, i, doc_type, iterations
            )
            print(f"✓ Score: {score}/10 (threshold: {threshold}/10)")

            iteration_result = {
                "iteration": i,
                "image_path": str(iter_path),
                "prompt": current_prompt,
                "critique": critique,
                "score": score,
                "needs_improvement": needs_improvement,
                "success": True
            }
            results["iterations"].append(iteration_result)

            if not needs_improvement:
                print(f"\n✓ Quality meets {doc_type} threshold ({score} >= {threshold})")
                print(f"  No further iterations needed!")
                results["final_image"] = str(iter_path)
                results["final_score"] = score
                results["success"] = True
                results["early_stop"] = True
                results["early_stop_reason"] = f"Quality score {score} meets threshold {threshold} for {doc_type}"
                break

            if i == iterations:
                print(f"\n⚠ Maximum iterations reached")
                results["final_image"] = str(iter_path)
                results["final_score"] = score
                results["success"] = True
                break

            print(f"\n⚠ Quality below threshold ({score} < {threshold})")
            print(f"Improving prompt based on feedback...")
            current_prompt = self.improve_prompt(user_prompt, critique, i + 1)

        # Copy final version to output path
        if results["success"] and results["final_image"]:
            final_iter_path = Path(results["final_image"])
            if final_iter_path != output_path:
                import shutil
                shutil.copy(final_iter_path, output_path)
                print(f"\n✓ Final image: {output_path}")

        # Save review log
        log_path = output_dir / f"{base_name}_review_log.json"
        with open(log_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✓ Review log: {log_path}")

        print(f"\n{'='*60}")
        print(f"🍌 Generation Complete!")
        print(f"Final Score: {results['final_score']}/10")
        if results["early_stop"]:
            print(f"Iterations Used: {len([r for r in results['iterations'] if r.get('success')])}/{iterations} (early stop)")
        print(f"{'='*60}\n")

        return results


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate diagrams using Nano Banana Pro with smart iterative refinement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate architecture diagram
  python generate_diagram_ai.py "Microservices architecture with API gateway" -o architecture.png --doc-type architecture

  # Generate flowchart for presentation (lower threshold, faster)
  python generate_diagram_ai.py "User authentication flow" -o auth_flow.png --doc-type presentation

  # Generate with verbose output
  python generate_diagram_ai.py "Database schema for e-commerce" -o schema.png -v

Document Types (quality thresholds):
  specification 8.5/10 - Technical specs, PRDs
  architecture  8.0/10 - Architecture documents
  proposal      8.0/10 - Business proposals
  journal       8.5/10 - Academic journals
  conference    8.0/10 - Conference papers
  thesis        8.0/10 - Dissertations
  grant         8.0/10 - Grant proposals
  sprint        7.5/10 - Sprint planning docs
  report        7.5/10 - Technical reports
  preprint      7.5/10 - Preprints
  readme        7.0/10 - README files
  poster        7.0/10 - Academic posters
  presentation  6.5/10 - Slides, talks
  default       7.5/10 - General purpose

Note: Multiple iterations only occur if quality is BELOW the threshold.
      If the first generation meets the threshold, no extra API calls are made.

Environment:
  OPENROUTER_API_KEY    OpenRouter API key (required)
        """
    )

    parser.add_argument("prompt", help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True,
                       help="Output image path (e.g., diagram.png)")
    parser.add_argument("--iterations", type=int, default=2,
                       help="Maximum refinement iterations (default: 2, max: 2)")
    parser.add_argument("--doc-type", default="default",
                       choices=list(NanoBananaGenerator.QUALITY_THRESHOLDS.keys()),
                       help="Document type for quality threshold (default: default)")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export OPENROUTER_API_KEY='your_api_key'")
        print("\nOr provide via --api-key flag")
        sys.exit(1)

    if args.iterations < 1 or args.iterations > 2:
        print("Error: Iterations must be between 1 and 2")
        sys.exit(1)

    try:
        generator = NanoBananaGenerator(api_key=api_key, verbose=args.verbose)
        results = generator.generate_iterative(
            user_prompt=args.prompt,
            output_path=args.output,
            iterations=args.iterations,
            doc_type=args.doc_type
        )

        if results["success"]:
            print(f"\n✓ Success! Image saved to: {args.output}")
            sys.exit(0)
        else:
            print(f"\n✗ Generation failed. Check review log for details.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
