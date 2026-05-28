#!/usr/bin/env python3
"""
Create Embeddings using Ollama

Usage:
    python3 embed.py <text> [--model <model_name>] [--url <base_url>]

Dependencies:
    pip install requests
"""

import sys
import argparse
import json
import requests


def get_embedding(text, model="nomic-embed-text", base_url="http://127.0.0.1:11434"):
    """
    Get vector embedding from Ollama API.

    Args:
        text (str): Text to embed.
        model (str): Model name (default: nomic-embed-text).
        base_url (str): Ollama API base URL.

    Returns:
        list: Vector embedding (list of floats).
    """
    url = f"{base_url}/api/embeddings"
    payload = {"model": model, "prompt": text}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("embedding")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Get embeddings from Ollama")
    parser.add_argument("text", help="Text to embed")
    parser.add_argument("--model", default="nomic-embed-text", help="Ollama model name")
    parser.add_argument(
        "--url", default="http://127.0.0.1:11434", help="Ollama base URL"
    )

    args = parser.parse_args()

    embedding = get_embedding(args.text, args.model, args.url)

    # Print as JSON for easy parsing by other tools
    print(json.dumps(embedding))


if __name__ == "__main__":
    main()
