#!/usr/bin/env python3
"""
Parse Resume to JSON using Ollama

Usage:
    python3 parse_resume.py <resume_text_file> [--model <model>]

Dependencies:
    pip install requests
"""

import sys
import argparse
import requests

SYSTEM_PROMPT = """You are a resume parsing assistant. Extract the following fields from the resume text into a standard JSON format:
- full_name (string)
- email (string)
- phone (string)
- skills (list of strings)
- experience (list of objects with company, title, start_date, end_date, description)
- education (list of objects with school, degree, graduation_date)

Output ONLY valid JSON. Do not include any explanation."""


def parse_resume(text, model="llama3.2", base_url="http://127.0.0.1:11434"):
    url = f"{base_url}/api/generate"

    prompt = f"Resume Text:\n{text}\n\nJSON Output:"

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
    parser = argparse.ArgumentParser(description="Parse resume using LLM")
    parser.add_argument("resume_file", help="Path to text resume file")
    parser.add_argument("--model", default="llama3.2", help="Ollama model name")
    parser.add_argument(
        "--url", default="http://127.0.0.1:11434", help="Ollama base URL"
    )

    args = parser.parse_args()

    try:
        with open(args.resume_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    result = parse_resume(text, args.model, args.url)
    print(result)


if __name__ == "__main__":
    main()
