#!/usr/bin/env python3
"""
OpenRouter API Client for Claude Code.

Usage:
    uv run --with requests openrouter_client.py chat MODEL "Your prompt here" [OPTIONS]
    uv run --with requests openrouter_client.py image MODEL "Image description" [OPTIONS]
    uv run --with requests openrouter_client.py models [CAPABILITY]
    uv run --with requests openrouter_client.py find "search term"

Environment:
    SKILL_OPENROUTER_API_KEY - Required API key from https://openrouter.ai/keys

Examples:
    uv run --with requests openrouter_client.py chat anthropic/claude-sonnet-4.5 "Explain recursion"
    uv run --with requests openrouter_client.py chat openai/gpt-5.2 "Write a haiku" --max-tokens 100
    uv run --with requests openrouter_client.py image google/gemini-3-pro-image-preview "A sunset" --output sunset.png
    uv run --with requests openrouter_client.py image openai/gpt-5-image "A star icon" --output star.png --background transparent
    uv run --with requests openrouter_client.py models vision
    uv run --with requests openrouter_client.py find "claude"
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library required. Run with: uv run --with requests scripts/openrouter_client.py ...", file=sys.stderr)
    sys.exit(1)


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://claude.ai/claude-code",
            "X-Title": "Claude Code"
        }

    def _request(self, method: str, endpoint: str, payload: dict = None, max_retries: int = 3):
        """Make API request with retry logic."""
        # Support both relative endpoints and full URLs
        url = endpoint if endpoint.startswith("http") else f"{self.BASE_URL}/{endpoint}"

        for attempt in range(max_retries):
            try:
                if method == "GET":
                    response = requests.get(url, headers=self.headers, timeout=120)
                else:
                    response = requests.post(url, headers=self.headers, json=payload, timeout=120)

                if response.status_code == 200:
                    return response.json()

                error = response.json().get("error", {})
                code = error.get("code", response.status_code)
                message = error.get("message", response.text)

                # Retryable errors
                if code in [408, 429, 502, 503] and attempt < max_retries - 1:
                    wait = min(2 ** attempt * 2, 30)
                    print(f"Retrying in {wait}s (attempt {attempt + 1}/{max_retries})...", file=sys.stderr)
                    time.sleep(wait)
                    continue

                # Non-retryable errors
                error_messages = {
                    400: "Bad request - check parameters",
                    401: "Invalid API key - check SKILL_OPENROUTER_API_KEY",
                    402: "Insufficient credits - add funds at openrouter.ai",
                    403: "Content flagged by moderation",
                    429: "Rate limited - wait before retrying"
                }
                msg = error_messages.get(code, message)
                raise Exception(f"OpenRouter error {code}: {msg}")

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    continue
                raise Exception("Request timed out after retries")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Network error: {e}")

        raise Exception("Max retries exceeded")

    def chat(self, model: str, messages: list, **kwargs) -> dict:
        """Send chat completion request."""
        payload = {"model": model, "messages": messages}
        payload.update(kwargs)
        return self._request("POST", "chat/completions", payload)

    def chat_simple(self, model: str, prompt: str, system: str = None, **kwargs) -> str:
        """Simple chat - returns just the response text."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        result = self.chat(model, messages, **kwargs)
        return result["choices"][0]["message"]["content"]

    def generate_image(self, model: str, prompt: str, output_path: str = None,
                       aspect_ratio: str = "1:1", size: str = "1K", background: str = None,
                       quality: str = None, output_format: str = None) -> list:
        """Generate image using chat completions endpoint.

        Args:
            background: Optional background setting (e.g., "transparent").
                       Support depends on model capabilities.
            quality: Optional quality setting (e.g., "high", "medium", "low").
                    Required for best transparency results.
            output_format: Optional output format (e.g., "png", "webp", "jpeg").
                          Required for transparency (use "png" or "webp").
        """
        image_config = {"aspect_ratio": aspect_ratio, "image_size": size}

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "image_config": image_config,
            "n": 1
        }

        # Add top-level parameters (for OpenAI GPT Image models)
        if background:
            payload["background"] = background
        if quality:
            payload["quality"] = quality
        if output_format:
            payload["output_format"] = output_format

        result = self._request("POST", "chat/completions", payload)
        images = result["choices"][0]["message"].get("images", [])

        if output_path and images:
            output = Path(output_path).resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            for idx, img in enumerate(images):
                data_url = img["image_url"]["url"]
                base64_data = data_url.split(",")[1]
                if len(images) == 1:
                    path = output
                else:
                    path = output.parent / f"{output.stem}_{idx}{output.suffix}"
                with open(path, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                print(f"Saved: {path}", file=sys.stderr)

        return images

    def list_models(self, capability: str = None) -> list:
        """List available models, optionally filtered by capability.

        Uses the frontend/models endpoint which includes all models (600+)
        including image generation models like Flux that are not in /api/v1/models.
        """
        result = self._request("GET", "https://openrouter.ai/api/frontend/models")
        models = result.get("data", [])

        if capability:
            if capability == "vision":
                models = [m for m in models if "image" in m.get("input_modalities", [])]
            elif capability == "image_gen":
                models = [m for m in models if "image" in m.get("output_modalities", [])]
            elif capability == "tools":
                models = [m for m in models if "tools" in m.get("supported_parameters", [])]
            elif capability == "long_context":
                models = [m for m in models if m.get("context_length", 0) >= 100000]

        return models

    def find_model(self, search_term: str) -> list:
        """Find models matching search term."""
        models = self.list_models()
        search_lower = search_term.lower()
        return [m for m in models if search_lower in m["slug"].lower() or search_lower in m["name"].lower()]


def main():
    parser = argparse.ArgumentParser(description="OpenRouter API Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Send chat completion")
    chat_parser.add_argument("model", help="Model ID (e.g., anthropic/claude-sonnet-4.5)")
    chat_parser.add_argument("prompt", help="User prompt")
    chat_parser.add_argument("--system", "-s", help="System prompt")
    chat_parser.add_argument("--max-tokens", "-m", type=int, help="Max tokens")
    chat_parser.add_argument("--temperature", "-t", type=float, help="Temperature (0-2)")
    chat_parser.add_argument("--json", "-j", action="store_true", help="Request JSON output")

    # Image command
    image_parser = subparsers.add_parser("image", help="Generate image")
    image_parser.add_argument("model", help="Image model (e.g., google/gemini-3-pro-image-preview)")
    image_parser.add_argument("prompt", help="Image description")
    image_parser.add_argument("--output", "-o", default="output.png", help="Output filename")
    image_parser.add_argument("--aspect", "-a", default="1:1", help="Aspect ratio (1:1, 16:9, etc)")
    image_parser.add_argument("--size", "-z", default="1K", help="Size (1K, 2K, 4K)")
    image_parser.add_argument("--background", "-b", help="Background setting (e.g., 'transparent')")
    image_parser.add_argument("--quality", "-q", help="Quality setting (e.g., 'high', 'medium', 'low')")
    image_parser.add_argument("--output-format", "-f", help="Output format (e.g., 'png', 'webp', 'jpeg')")

    # Models command
    models_parser = subparsers.add_parser("models", help="List available models")
    models_parser.add_argument("capability", nargs="?", choices=["vision", "image_gen", "tools", "long_context"],
                               help="Filter by capability")

    # Find command
    find_parser = subparsers.add_parser("find", help="Find model by name")
    find_parser.add_argument("search", help="Search term")

    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("SKILL_OPENROUTER_API_KEY")
    if not api_key:
        print("Error: SKILL_OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        print("Get your key at: https://openrouter.ai/keys", file=sys.stderr)
        sys.exit(1)

    client = OpenRouterClient(api_key)

    try:
        if args.command == "chat":
            kwargs = {}
            if args.max_tokens:
                kwargs["max_tokens"] = args.max_tokens
            if args.temperature is not None:
                kwargs["temperature"] = args.temperature
            if args.json:
                kwargs["response_format"] = {"type": "json_object"}

            response = client.chat_simple(args.model, args.prompt, system=args.system, **kwargs)
            print(response)

        elif args.command == "image":
            images = client.generate_image(
                args.model, args.prompt, args.output, args.aspect, args.size,
                background=args.background, quality=args.quality, output_format=args.output_format
            )
            if images:
                print(f"Generated {len(images)} image(s)")
            else:
                print("No images generated", file=sys.stderr)
                sys.exit(1)

        elif args.command == "models":
            models = client.list_models(args.capability)
            for m in models:
                pricing = m.get("pricing", {})
                ctx = m.get("context_length", "?")
                prompt_price = float(pricing.get("prompt", 0)) * 1_000_000
                print(f"{m['slug']:50} ctx:{ctx:>7}  ${prompt_price:.2f}/M")

        elif args.command == "find":
            matches = client.find_model(args.search)
            if matches:
                for m in matches[:10]:
                    ctx = m.get("context_length", "?")
                    print(f"{m['slug']:50} ctx:{ctx:>7}")
            else:
                print(f"No models found matching '{args.search}'", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
