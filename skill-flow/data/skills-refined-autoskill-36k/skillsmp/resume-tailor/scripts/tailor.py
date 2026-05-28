#!/usr/bin/env python3
"""
Tailor Resume Content

Usage:
    python3 tailor.py <resume_json> <job_description> [--model <model>]

Dependencies:
    pip install requests
"""

import sys
import argparse
import requests

SYSTEM_PROMPT = """You are an expert resume writer. tailored the resume bullets to match the job description.
RULES:
1. DO NOT fabricate skills or experience.
2. Only highlight existing experience that is relevant to the job.
3. Use keywords from the job description if they strictly match the candidate's actual experience.
4. Output JSON with the same structure as the input resume, but with modified 'decision' and 'tailored_content' fields if applicable.
"""


def tailor_resume(
    resume_json, job_desc, model="llama3.2", base_url="http://127.0.0.1:11434"
):
    url = f"{base_url}/api/generate"

    prompt = (
        f"Job Description:\n{job_desc}\n\nResume JSON:\n{resume_json}\n\nTailored JSON:"
    )

    payload = {
        "model": model,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response")
    except Exception as e:
        print(f"Error calling Ollama: {e}", file=sys.stderr)
        return "{}"


def main():
    parser = argparse.ArgumentParser(description="Tailor resume content")
    parser.add_argument("resume_file", help="Path to resume JSON file")
    parser.add_argument("job_file", help="Path to job description file")
    parser.add_argument("--model", default="llama3.2", help="Ollama model name")
    parser.add_argument(
        "--url", default="http://127.0.0.1:11434", help="Ollama base URL"
    )

    args = parser.parse_args()

    # Read resume
    try:
        with open(args.resume_file, "r") as f:
            resume_content = f.read()
    except Exception as e:
        print(f"Error reading resume: {e}", file=sys.stderr)
        sys.exit(1)

    # Read job desc
    try:
        with open(args.job_file, "r") as f:
            job_content = f.read()
    except Exception as e:
        print(f"Error reading job description: {e}", file=sys.stderr)
        sys.exit(1)

    result = tailor_resume(resume_content, job_content, args.model, args.url)
    print(result)


if __name__ == "__main__":
    main()
