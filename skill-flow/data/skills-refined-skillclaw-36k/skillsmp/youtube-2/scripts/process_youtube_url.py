#!/usr/bin/env python3
"""
Process YouTube URL: fetch transcript and save to Bookmarks database.

This is the main entry point that Claude should call.
It handles everything in one step without polluting chat context.
"""

import sys
import json
import subprocess
from pathlib import Path


def main():
    """
    Main entry point.

    Input (stdin JSON):
    {
        "url": "https://youtube.com/watch?v=...",
        "lang": "en",  // Optional, defaults to "en"
        "force": false  // Optional, force re-fetch even if cached
    }

    Output (stdout JSON):
    {
        "success": true,
        "video_id": "abc123",
        "filepath": "Database/Bookmarks/youtube-abc123.md",
        "url": "https://youtu.be/abc123",
        "title": "Video Title",
        "cached": false
    }
    """
    try:
        # Read input
        input_data = json.load(sys.stdin)
        url = input_data.get("url")
        lang = input_data.get("lang", "en")
        force = input_data.get("force", False)

        if not url:
            print(json.dumps({
                "success": False,
                "error": "No URL provided"
            }))
            sys.exit(1)

        script_dir = Path(__file__).parent
        save_script = script_dir / "save_transcript.py"
        fetch_script = script_dir / "fetch_transcript.py"

        # Step 1: Check cache (unless force=True)
        if not force:
            check_input = {
                "url": url,
                "title": "",
                "transcript": [],
                "force": False
            }

            result = subprocess.run(
                ["python3", str(save_script)],
                input=json.dumps(check_input),
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                output = json.loads(result.stdout)
                if output.get("success") and output.get("cached"):
                    # Already cached, return immediately
                    print(result.stdout)
                    sys.exit(0)

        # Step 2: Fetch transcript
        fetch_input = {
            "url": url,
            "lang": lang
        }

        fetch_result = subprocess.run(
            ["python3", str(fetch_script)],
            input=json.dumps(fetch_input),
            capture_output=True,
            text=True,
            check=False
        )

        if fetch_result.returncode != 0:
            # Fetch failed, return error
            print(fetch_result.stdout)
            sys.exit(1)

        fetch_output = json.loads(fetch_result.stdout)
        if not fetch_output.get("success"):
            print(fetch_result.stdout)
            sys.exit(1)

        # Step 3: Save to bookmarks
        save_input = {
            "url": url,
            "title": fetch_output.get("metadata", {}).get("title", "Untitled Video"),
            "transcript": fetch_output.get("transcript", []),
            "force": force
        }

        save_result = subprocess.run(
            ["python3", str(save_script)],
            input=json.dumps(save_input),
            capture_output=True,
            text=True,
            check=False
        )

        print(save_result.stdout)
        sys.exit(save_result.returncode)

    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "Invalid JSON input"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
