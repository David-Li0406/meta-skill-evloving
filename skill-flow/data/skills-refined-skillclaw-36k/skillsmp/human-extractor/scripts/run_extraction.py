#!/usr/bin/env python3
"""
Human Extractor Skill - Main Entry Point
Wrapper script for basic human detection and cropping pipeline
"""
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

# Path to Human_Detection project
PROJECT_ROOT = Path(r"G:\My Drive\PROJECTS\APPS\Human_Detection")
CLI_PATH = PROJECT_ROOT / "src" / "cli"

def validate_config(config: Dict[str, Any]) -> tuple[bool, str]:
    """Validate configuration parameters"""

    # Check required fields
    if "roots" not in config:
        return False, "Missing required field: 'roots'"

    if not isinstance(config["roots"], list) or len(config["roots"]) == 0:
        return False, "'roots' must be a non-empty list"

    # Validate paths exist
    for root in config["roots"]:
        if not Path(root).exists():
            return False, f"Path does not exist: {root}"

    return True, "OK"


def build_command(config: Dict[str, Any]) -> list[str]:
    """Build command line arguments for the basic human cropping CLI script"""

    cmd = [
        sys.executable,
        "-m", "src.cli.run_human_cropping",
        "--root", config["roots"][0],  # Primary root
        "--out", config.get("output_dir", "parsed"),
    ]

    # Optional: Delete original videos after processing
    if config.get("delete_original", False):
        cmd.append("--delete-original")

    return cmd


def run_extraction(config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the basic human extraction pipeline"""

    # Validate configuration
    valid, msg = validate_config(config)
    if not valid:
        return {
            "status": "error",
            "error": f"Configuration validation failed: {msg}"
        }

    # Build command
    cmd = build_command(config)

    # Change to project directory
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(PROJECT_ROOT)

        # Execute
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=18000  # 5 hour timeout
        )

        if result.returncode == 0:
            # Parse output to find where files were saved
            output_dir = config.get("output_dir", "parsed")

            return {
                "status": "ok",
                "summary": {
                    "message": "Human extraction completed successfully",
                    "stdout": result.stdout,
                },
                "artifacts": {
                    "output_dir": output_dir,
                    "index_csv": str(Path(output_dir) / "INDEX.csv"),
                    "note": "Human crops saved in {Camera}/{Date}/humans_summary/ subdirectories"
                }
            }
        else:
            return {
                "status": "error",
                "error": f"Process failed with code {result.returncode}",
                "stderr": result.stderr,
                "stdout": result.stdout
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "Process timeout (>5 hours)"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    # Read config from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    # Run extraction
    result = run_extraction(config)

    # Output result
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "ok" else 1)
