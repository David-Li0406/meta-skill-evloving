#!/usr/bin/env python3
"""
Stop hook: Witty narration of what just happened.
Reads transcript, sends to small model, speaks result.

Enable per-project: touch ~/.narrator-<projectname>
"""

import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import llm_generate

PROMPT = """You are a witty narrator for a coding session. In ONE SHORT sentence (max 15 words),
comment on what the assistant just did. Be brief, clever, slightly sarcastic. No quotes.

What happened: {summary}

Your narration:"""


def should_narrate(project: str) -> bool:
    """Check if narration enabled for this project."""
    if not project:
        return False
    flag = Path.home() / f".narrator-{project.lower()}"
    return flag.exists()


def speak(text: str, rate: int = 185):
    """TTS using macOS say."""
    subprocess.Popen(["say", "-v", "Daniel", "-r", str(rate), text])


def summarize_exchange(assistant_msg: str) -> str:
    """Extract key action from assistant's response."""
    # Take first 200 chars or first paragraph
    lines = assistant_msg.strip().split('\n')
    summary = lines[0][:200] if lines else ""
    return summary


def load_transcript_messages(transcript_path: str) -> list:
    """Load messages from JSONL transcript file."""
    messages = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    # Assistant messages have type="assistant" and message.content
                    if entry.get("type") == "assistant":
                        msg = entry.get("message", {})
                        if msg.get("role") == "assistant":
                            messages.append({
                                "role": "assistant",
                                "content": msg.get("content", "")
                            })
                    # User messages have type="user"
                    elif entry.get("type") == "user":
                        msg = entry.get("message", {})
                        messages.append({
                            "role": "user",
                            "content": msg.get("content", "")
                        })
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass
    return messages


def main():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        sys.exit(0)

    # Get project from cwd
    cwd = data.get("cwd", "")
    project = cwd.split("/")[-1]

    if not should_narrate(project):
        sys.exit(0)

    # Load messages from transcript file (Stop hook provides transcript_path, not messages)
    transcript_path = data.get("transcript_path", "")
    if transcript_path:
        messages = load_transcript_messages(transcript_path)
    else:
        messages = data.get("messages", [])

    # Get last assistant message
    assistant_msg = ""
    for msg in reversed(messages):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if isinstance(content, list):
                # Extract text from content blocks, skip thinking blocks
                texts = []
                for c in content:
                    if isinstance(c, dict):
                        if c.get("type") == "text":
                            texts.append(c.get("text", ""))
                        elif c.get("type") == "tool_use":
                            texts.append(f"[using {c.get('name', 'tool')}]")
                assistant_msg = " ".join(texts)
            else:
                assistant_msg = str(content)
            break

    if not assistant_msg:
        sys.exit(0)

    # Generate narration
    summary = summarize_exchange(assistant_msg)
    prompt = PROMPT.format(summary=summary)

    try:
        narration, _ = llm_generate(prompt, timeout=5)
    except Exception:
        sys.exit(0)

    if narration:
        narration = narration.strip().strip('"').split('\n')[0]
        speak(narration)


if __name__ == "__main__":
    main()
