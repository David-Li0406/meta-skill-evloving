#!/usr/bin/env python3
"""
Diagram generation using Nano Banana Pro.

Generate any technical diagram by describing it in natural language.
Nano Banana Pro handles everything automatically with smart iterative refinement.

Smart iteration: Only regenerates if quality is below threshold for your document type.
Quality review: Uses Gemini 3 Pro for professional evaluation.

Usage:
    # Generate for architecture docs (high quality threshold)
    python generate_diagram.py "Microservices architecture" -o architecture.png --doc-type architecture

    # Generate for presentation (lower threshold, faster)
    python generate_diagram.py "User flow diagram" -o flow.png --doc-type presentation

    # Generate for README
    python generate_diagram.py "System overview" -o system.png --doc-type readme
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate diagrams using Nano Banana Pro with smart iterative refinement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
How it works:
  Simply describe your diagram in natural language
  Nano Banana Pro generates it automatically with:
  - Smart iteration (only regenerates if quality is below threshold)
  - Quality review by Gemini 3 Pro
  - Document-type aware quality thresholds
  - Publication-ready output

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

Examples:
  # Generate architecture diagram
  python generate_diagram.py "Microservices with API gateway" -o arch.png --doc-type architecture

  # Generate for slides (faster)
  python generate_diagram.py "Data pipeline flow" -o pipeline.png --doc-type presentation

  # Verbose output
  python generate_diagram.py "ERD diagram" -o erd.png -v

Environment Variables:
  OPENROUTER_API_KEY    Required for AI generation
        """
    )

    parser.add_argument("prompt",
                       help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True,
                       help="Output file path")
    parser.add_argument("--doc-type", default="default",
                       choices=["specification", "architecture", "proposal", "sprint",
                               "journal", "conference", "poster", "presentation",
                               "report", "grant", "thesis", "preprint", "readme", "default"],
                       help="Document type for quality threshold (default: default)")
    parser.add_argument("--iterations", type=int, default=2,
                       help="Maximum refinement iterations (default: 2, max: 2)")
    parser.add_argument("--api-key",
                       help="OpenRouter API key (or use OPENROUTER_API_KEY env var)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")

    args = parser.parse_args()

    # Check for API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("\nFor AI generation, you need an OpenRouter API key.")
        print("Get one at: https://openrouter.ai/keys")
        print("\nSet it with:")
        print("  export OPENROUTER_API_KEY='your_api_key'")
        print("\nOr use --api-key flag")
        sys.exit(1)

    # Find AI generation script
    script_dir = Path(__file__).parent
    ai_script = script_dir / "generate_diagram_ai.py"

    if not ai_script.exists():
        print(f"Error: AI generation script not found: {ai_script}")
        sys.exit(1)

    # Build command
    cmd = [sys.executable, str(ai_script), args.prompt, "-o", args.output]

    if args.doc_type != "default":
        cmd.extend(["--doc-type", args.doc_type])

    # Enforce max 2 iterations
    iterations = min(args.iterations, 2)
    if iterations != 2:
        cmd.extend(["--iterations", str(iterations)])

    if api_key:
        cmd.extend(["--api-key", api_key])

    if args.verbose:
        cmd.append("-v")

    # Execute
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing AI generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
