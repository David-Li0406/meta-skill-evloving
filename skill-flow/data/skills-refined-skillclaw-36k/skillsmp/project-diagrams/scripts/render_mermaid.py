#!/usr/bin/env python3
"""
Mermaid Diagram Renderer with Multi-Tier Fallback

Converts Mermaid markdown files to PNG images using:
1. Local mermaid-cli (mmdc) - Best quality, offline
2. Kroki.io API - Free online renderer, no install needed
3. Nano Banana AI - Generate from Mermaid description
4. Keep markdown only - Last resort

Usage:
    python render_mermaid.py input.md -o output.png
    python render_mermaid.py input.md --method kroki
    python render_mermaid.py diagrams/ --batch  # Render all .md/.mmd files
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import zlib
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# Kroki.io endpoint for Mermaid rendering
KROKI_ENDPOINT = "https://kroki.io/mermaid/png"

# Nano Banana models via OpenRouter
NANO_BANANA_MODEL = "google/gemini-3-pro-image-preview"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def check_mmdc_available() -> bool:
    """Check if mermaid-cli (mmdc) is installed."""
    return shutil.which("mmdc") is not None


def extract_mermaid_from_markdown(file_path: Path) -> Optional[str]:
    """Extract Mermaid code block from a markdown file."""
    content = file_path.read_text(encoding="utf-8")

    # Match ```mermaid ... ``` code blocks
    pattern = r"```mermaid\s*\n(.*?)```"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    # If no code block, check if entire file is Mermaid syntax
    # (starts with graph, flowchart, sequenceDiagram, etc.)
    mermaid_keywords = [
        "graph ", "flowchart ", "sequenceDiagram", "classDiagram",
        "stateDiagram", "erDiagram", "gantt", "pie ", "journey",
        "gitGraph", "C4Context", "C4Container", "C4Component", "mindmap"
    ]

    for keyword in mermaid_keywords:
        if content.strip().startswith(keyword):
            return content.strip()

    return None


def render_with_mmdc(
    mermaid_code: str,
    output_path: Path,
    theme: str = "neutral",
    width: int = 2000,
    background: str = "white"
) -> tuple[bool, str]:
    """Render Mermaid diagram using local mermaid-cli."""
    if not check_mmdc_available():
        return False, "mmdc not installed"

    # Write Mermaid code to temp file
    temp_input = output_path.parent / f".temp_{output_path.stem}.mmd"
    try:
        temp_input.write_text(mermaid_code, encoding="utf-8")

        cmd = [
            "mmdc",
            "-i", str(temp_input),
            "-o", str(output_path),
            "-t", theme,
            "-w", str(width),
            "-b", background
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0 and output_path.exists():
            return True, "Rendered with local mmdc"
        else:
            return False, f"mmdc error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "mmdc timed out"
    except Exception as e:
        return False, f"mmdc exception: {e}"
    finally:
        if temp_input.exists():
            temp_input.unlink()


def render_with_kroki(mermaid_code: str, output_path: Path) -> tuple[bool, str]:
    """Render Mermaid diagram using Kroki.io API (free, no auth)."""
    try:
        # Kroki expects base64-encoded, zlib-compressed diagram
        compressed = zlib.compress(mermaid_code.encode("utf-8"), level=9)
        encoded = base64.urlsafe_b64encode(compressed).decode("ascii")

        url = f"{KROKI_ENDPOINT}/{encoded}"

        request = Request(url)
        request.add_header("Accept", "image/png")

        with urlopen(request, timeout=30) as response:
            png_data = response.read()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(png_data)

        if output_path.exists() and output_path.stat().st_size > 0:
            return True, "Rendered with Kroki.io API"
        else:
            return False, "Kroki returned empty response"

    except HTTPError as e:
        return False, f"Kroki HTTP error: {e.code} - {e.reason}"
    except URLError as e:
        return False, f"Kroki network error: {e.reason}"
    except Exception as e:
        return False, f"Kroki exception: {e}"


def render_with_nano_banana(
    mermaid_code: str,
    output_path: Path,
    context: str = ""
) -> tuple[bool, str]:
    """
    Generate diagram image using Nano Banana AI.
    Falls back to AI when Mermaid rendering not available.
    Requires OPENROUTER_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return False, "OPENROUTER_API_KEY not set"

    # Parse Mermaid to create description for AI
    diagram_description = _mermaid_to_description(mermaid_code)

    prompt = f"""Generate a professional technical diagram based on this Mermaid diagram specification:

{mermaid_code}

Key elements to include: {diagram_description}
{f'Context: {context}' if context else ''}

Create a clean, professional diagram with:
- Clear labeled boxes and connections
- Professional color scheme (blues, grays)
- High contrast for readability
- Technical documentation style
- No decorative elements, pure information visualization"""

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/flight505/claude-project-planner",
            "X-Title": "Claude Project Planner"
        }

        data = json.dumps({
            "model": NANO_BANANA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096
        }).encode("utf-8")

        request = Request(OPENROUTER_API_URL, data=data, headers=headers)

        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        # Extract image from response
        message = result.get("choices", [{}])[0].get("message", {})

        # Check for images array (Nano Banana format)
        images = message.get("images", [])
        if images:
            image_data = base64.b64decode(images[0])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_data)
            return True, "Generated with Nano Banana AI"

        # Check content array for image blocks
        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "image":
                    image_data = base64.b64decode(item.get("data", ""))
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(image_data)
                    return True, "Generated with Nano Banana AI"

        return False, "Nano Banana returned no image"

    except Exception as e:
        return False, f"Nano Banana exception: {e}"


def _mermaid_to_description(mermaid_code: str) -> str:
    """Convert Mermaid code to a natural language description for AI."""
    lines = mermaid_code.strip().split("\n")
    description_parts = []

    # Detect diagram type
    first_line = lines[0].lower()
    if "graph" in first_line or "flowchart" in first_line:
        description_parts.append("Flowchart diagram")
    elif "sequencediagram" in first_line:
        description_parts.append("Sequence diagram showing interactions")
    elif "classdiagram" in first_line:
        description_parts.append("Class diagram with relationships")
    elif "erdiagram" in first_line:
        description_parts.append("Entity-relationship diagram")
    elif "gantt" in first_line:
        description_parts.append("Gantt chart timeline")
    elif "c4" in first_line.lower():
        description_parts.append("C4 architecture diagram")
    elif "mindmap" in first_line:
        description_parts.append("Mind map visualization")

    # Extract node/entity names
    nodes = set()
    for line in lines:
        # Match node definitions: A[Label] or A(Label) or A{Label}
        matches = re.findall(r'(\w+)\s*[\[\(\{]([^\]\)\}]+)[\]\)\}]', line)
        for _, label in matches:
            nodes.add(label.strip())

        # Match participant names in sequence diagrams
        if "participant" in line.lower():
            match = re.search(r'participant\s+(\w+)', line, re.IGNORECASE)
            if match:
                nodes.add(match.group(1))

    if nodes:
        description_parts.append(f"Elements: {', '.join(list(nodes)[:10])}")

    return ". ".join(description_parts)


def render_mermaid(
    input_path: Path,
    output_path: Optional[Path] = None,
    method: str = "auto",
    theme: str = "neutral",
    width: int = 2000,
    context: str = ""
) -> tuple[bool, str, str]:
    """
    Render a Mermaid file to PNG with fallback methods.

    Args:
        input_path: Path to .md or .mmd file containing Mermaid
        output_path: Output PNG path (default: same name as input with .png)
        method: "auto", "mmdc", "kroki", or "nano-banana"
        theme: Mermaid theme for mmdc (neutral, default, dark, forest)
        width: Output width in pixels
        context: Additional context for AI generation

    Returns:
        Tuple of (success, method_used, message)
    """
    if not input_path.exists():
        return False, "none", f"Input file not found: {input_path}"

    # Extract Mermaid code
    mermaid_code = extract_mermaid_from_markdown(input_path)
    if not mermaid_code:
        return False, "none", f"No Mermaid code found in {input_path}"

    # Determine output path
    if output_path is None:
        output_path = input_path.with_suffix(".png")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Define fallback order
    if method == "auto":
        methods = ["mmdc", "kroki", "nano-banana"]
    else:
        methods = [method]

    errors = []

    for m in methods:
        if m == "mmdc":
            success, msg = render_with_mmdc(mermaid_code, output_path, theme, width)
            if success:
                return True, "mmdc", msg
            errors.append(f"mmdc: {msg}")

        elif m == "kroki":
            success, msg = render_with_kroki(mermaid_code, output_path)
            if success:
                return True, "kroki", msg
            errors.append(f"kroki: {msg}")

        elif m == "nano-banana":
            success, msg = render_with_nano_banana(mermaid_code, output_path, context)
            if success:
                return True, "nano-banana", msg
            errors.append(f"nano-banana: {msg}")

    return False, "none", f"All methods failed: {'; '.join(errors)}"


def batch_render(
    directory: Path,
    recursive: bool = True,
    method: str = "auto"
) -> dict:
    """Render all Mermaid files in a directory."""
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }

    patterns = ["*.md", "*.mmd"]
    files = []

    for pattern in patterns:
        if recursive:
            files.extend(directory.rglob(pattern))
        else:
            files.extend(directory.glob(pattern))

    for file_path in files:
        # Skip if PNG already exists and is newer
        png_path = file_path.with_suffix(".png")
        if png_path.exists():
            if png_path.stat().st_mtime >= file_path.stat().st_mtime:
                results["skipped"].append({
                    "file": str(file_path),
                    "reason": "PNG already up to date"
                })
                continue

        # Check if file contains Mermaid
        mermaid_code = extract_mermaid_from_markdown(file_path)
        if not mermaid_code:
            continue  # Not a Mermaid file, silently skip

        success, method_used, message = render_mermaid(
            file_path,
            png_path,
            method=method
        )

        if success:
            results["success"].append({
                "file": str(file_path),
                "output": str(png_path),
                "method": method_used,
                "message": message
            })
        else:
            results["failed"].append({
                "file": str(file_path),
                "error": message
            })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Render Mermaid diagrams to PNG with fallback methods"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input .md/.mmd file or directory (with --batch)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PNG path (default: same as input with .png)"
    )
    parser.add_argument(
        "--method",
        choices=["auto", "mmdc", "kroki", "nano-banana"],
        default="auto",
        help="Rendering method (default: auto with fallback)"
    )
    parser.add_argument(
        "--theme",
        choices=["neutral", "default", "dark", "forest"],
        default="neutral",
        help="Mermaid theme for mmdc (default: neutral)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=2000,
        help="Output width in pixels (default: 2000)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch render all Mermaid files in directory"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't search subdirectories in batch mode"
    )
    parser.add_argument(
        "--check-mmdc",
        action="store_true",
        help="Check if mmdc is available and exit"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Check mmdc mode
    if args.check_mmdc:
        available = check_mmdc_available()
        if args.json:
            print(json.dumps({"mmdc_available": available}))
        else:
            if available:
                print("mmdc is available")
            else:
                print("mmdc is NOT installed")
                print("Install with: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(0 if available else 1)

    # Batch mode
    if args.batch:
        if not args.input.is_dir():
            print(f"Error: {args.input} is not a directory", file=sys.stderr)
            sys.exit(1)

        results = batch_render(
            args.input,
            recursive=not args.no_recursive,
            method=args.method
        )

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Rendered: {len(results['success'])} files")
            print(f"Failed: {len(results['failed'])} files")
            print(f"Skipped: {len(results['skipped'])} files")

            if results["failed"]:
                print("\nFailed files:")
                for item in results["failed"]:
                    print(f"  - {item['file']}: {item['error']}")

        sys.exit(0 if not results["failed"] else 1)

    # Single file mode
    success, method_used, message = render_mermaid(
        args.input,
        args.output,
        method=args.method,
        theme=args.theme,
        width=args.width
    )

    if args.json:
        print(json.dumps({
            "success": success,
            "method": method_used,
            "message": message,
            "input": str(args.input),
            "output": str(args.output or args.input.with_suffix(".png"))
        }))
    else:
        if success:
            print(f"Success: {message}")
            print(f"Output: {args.output or args.input.with_suffix('.png')}")
        else:
            print(f"Error: {message}", file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
