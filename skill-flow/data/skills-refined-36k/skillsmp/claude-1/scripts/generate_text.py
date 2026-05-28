#!/usr/bin/env python3
"""
Text generation using Claude API.

Usage:
    uv run generate_text.py "Your prompt here"
    uv run generate_text.py "Your prompt" --model claude-3-5-haiku-20241022
    uv run generate_text.py "Your prompt" --system "You are a helpful assistant"
    uv run generate_text.py "Your prompt" --temperature 0.7 --max-tokens 2048

Environment:
    ANTHROPIC_API_KEY must be set
"""

import argparse
import sys
from anthropic import Anthropic, APIError, RateLimitError


def generate_text(
    prompt: str,
    model: str = "claude-sonnet-4-5-20250929",
    system: str | None = None,
    max_tokens: int = 1024,
    temperature: float | None = None,
    stream: bool = False,
) -> str:
    """
    Generate text using Claude API.

    Args:
        prompt: The user prompt/message
        model: Model identifier (haiku, sonnet, or opus)
        system: Optional system prompt for context
        max_tokens: Maximum tokens to generate
        temperature: Randomness (0.0-1.0, None for default)
        stream: Whether to stream the response

    Returns:
        Generated text response
    """
    client = Anthropic()

    # Build request parameters
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    if system:
        params["system"] = system

    if temperature is not None:
        params["temperature"] = temperature

    if stream:
        output = []
        with client.messages.stream(**params) as response:
            for text in response.text_stream:
                print(text, end="", flush=True)
                output.append(text)
        print()  # Newline after streaming
        return "".join(output)
    else:
        message = client.messages.create(**params)
        return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Generate text using Claude API")
    parser.add_argument("prompt", help="The prompt to send to Claude")
    parser.add_argument(
        "--model",
        "-m",
        default="claude-sonnet-4-5-20250929",
        help="Model to use (default: claude-sonnet-4-5-20250929)",
    )
    parser.add_argument(
        "--system",
        "-s",
        help="System prompt for context/instructions",
    )
    parser.add_argument(
        "--max-tokens",
        "-t",
        type=int,
        default=1024,
        help="Maximum tokens to generate (default: 1024)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Temperature for randomness (0.0-1.0)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream the response",
    )

    args = parser.parse_args()

    try:
        result = generate_text(
            prompt=args.prompt,
            model=args.model,
            system=args.system,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            stream=args.stream,
        )
        if not args.stream:
            print(result)
    except RateLimitError:
        print("Rate limit exceeded. Please wait and try again.", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
