#!/usr/bin/env python3
"""
Commentary mode - Use remote GPU to narrate Claude's actions.
Faster 8b model for real-time commentary.

Test: python3 commentary.py "Claude just searched for files in the codebase"
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import OLLAMA_URL, OLLAMA_LLM_MODEL, OLLAMA_SOURCE, llm_generate

def speak(text: str, rate: int = 185):
    """TTS using macOS say command."""
    subprocess.run(["say", "-v", "Daniel", "-r", str(rate), text], check=False)

def commentary(action: str) -> str:
    """Generate brief commentary for an action using remote 8b model."""
    prompt = f"""You are a witty narrator for a coding session. In ONE SHORT sentence (max 15 words), comment on this action. Be brief, clever, slightly sarcastic.

Action: {action}

Response (one sentence only):"""

    output, provider = llm_generate(prompt, timeout=5)
    if output:
        # Clean up response
        return output.strip().strip('"').split('\n')[0]
    return ""

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <action to comment on>")
        print(f"Using: {OLLAMA_SOURCE} ({OLLAMA_URL}) with {OLLAMA_LLM_MODEL}")
        sys.exit(1)

    action = " ".join(sys.argv[1:])
    print(f"[{OLLAMA_SOURCE}] Generating commentary for: {action[:50]}...")

    comment = commentary(action)
    if comment:
        print(f"Commentary: {comment}")
        speak(comment)
    else:
        print("No commentary generated")

if __name__ == "__main__":
    main()
