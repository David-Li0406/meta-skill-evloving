#!/usr/bin/env python3
"""
JSON extraction from unstructured text using Claude API.

Usage:
    uv run extract_json.py "John Smith, CTO at Acme Corp, email: john@acme.com"
    uv run extract_json.py "Extract data from this text" --schema '{"name": "string", "email": "string"}'
    uv run extract_json.py "Contract text here..." --schema-file schema.json

Environment:
    ANTHROPIC_API_KEY must be set
"""

import argparse
import json
import sys
from pathlib import Path
from anthropic import Anthropic, APIError, RateLimitError


def extract_json(
    text: str,
    schema: dict | str | None = None,
    model: str = "claude-sonnet-4-5-20250929",
    examples: list[dict] | None = None,
) -> dict:
    """
    Extract structured JSON from unstructured text.

    Args:
        text: The unstructured text to extract data from
        schema: JSON schema describing expected output structure
        model: Model identifier
        examples: Optional list of example input/output pairs

    Returns:
        Extracted data as a dictionary
    """
    client = Anthropic()

    # Build system prompt
    system_parts = [
        "You are a data extraction assistant. Extract structured information from the provided text.",
        "Return ONLY valid JSON. No markdown code blocks, no explanation, no additional text.",
    ]

    if schema:
        if isinstance(schema, dict):
            schema_str = json.dumps(schema, indent=2)
        else:
            schema_str = schema
        system_parts.append(f"Output must match this schema:\n{schema_str}")

    if examples:
        system_parts.append("\nExamples:")
        for i, example in enumerate(examples, 1):
            system_parts.append(f"\nExample {i}:")
            system_parts.append(f"Input: {example.get('input', '')}")
            system_parts.append(f"Output: {json.dumps(example.get('output', {}))}")

    system = "\n".join(system_parts)

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0,  # Deterministic for extraction
        system=system,
        messages=[{"role": "user", "content": text}],
    )

    response_text = message.content[0].text.strip()

    # Clean up common formatting issues
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    return json.loads(response_text)


def main():
    parser = argparse.ArgumentParser(
        description="Extract JSON from unstructured text using Claude API"
    )
    parser.add_argument("text", help="The text to extract data from")
    parser.add_argument(
        "--schema",
        "-s",
        help="JSON schema as a string",
    )
    parser.add_argument(
        "--schema-file",
        "-f",
        type=Path,
        help="Path to JSON schema file",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="claude-sonnet-4-5-20250929",
        help="Model to use (default: claude-sonnet-4-5-20250929)",
    )
    parser.add_argument(
        "--pretty",
        "-p",
        action="store_true",
        help="Pretty print the output",
    )

    args = parser.parse_args()

    # Load schema
    schema = None
    if args.schema_file:
        schema = json.loads(args.schema_file.read_text())
    elif args.schema:
        schema = json.loads(args.schema)

    try:
        result = extract_json(
            text=args.text,
            schema=schema,
            model=args.model,
        )

        if args.pretty:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}", file=sys.stderr)
        sys.exit(1)
    except RateLimitError:
        print("Rate limit exceeded. Please wait and try again.", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
