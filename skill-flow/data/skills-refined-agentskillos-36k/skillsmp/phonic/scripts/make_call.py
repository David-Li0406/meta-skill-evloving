#!/usr/bin/env python3
"""
Outbound phone call using Phonic AI telephone agent.

Usage:
    uv run make_call.py "+1234567890" --system-prompt "You are a friendly assistant..."
    uv run make_call.py "+1234567890" --system-prompt "..." --voice virginia
    uv run make_call.py "+1234567890" --system-prompt "..." --max-wait 900 --json
    uv run make_call.py "+1234567890" --system-prompt "..." --output-dir ./recordings

Environment:
    PHONIC_API_KEY must be set
"""

import argparse
import gzip
import json
import os
import shutil
import sys
import time
import urllib.request
import zipfile
from pathlib import Path
from phonic import Phonic


def download_audio(audio_url: str, conversation_id: str, output_dir: str) -> str | None:
    """
    Download audio file from URL. If zipped, extract and delete the zip.

    Returns the path to the audio file, or None if download failed.
    """
    if not audio_url:
        return None

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Determine filename from URL or use conversation_id
    url_path = audio_url.split("?")[0]  # Remove query params
    extension = Path(url_path).suffix or ".wav"

    download_filename = f"{conversation_id}{extension}"
    download_path = output_path / download_filename

    print(f"Downloading audio to {download_path}...", file=sys.stderr)

    try:
        urllib.request.urlretrieve(audio_url, download_path)
    except Exception as e:
        print(f"Failed to download audio: {e}", file=sys.stderr)
        return None

    # If it's a gzip file, extract and delete the gz
    if extension.lower() == ".gz":
        print(f"Extracting gzip file...", file=sys.stderr)
        try:
            # Determine output filename (remove .gz extension, add .wav if no extension)
            extracted_name = download_path.stem
            if not Path(extracted_name).suffix:
                extracted_name += ".wav"
            extracted_path = output_path / extracted_name

            with gzip.open(download_path, 'rb') as f_in:
                with open(extracted_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Delete the gzip file
            os.remove(download_path)
            print(f"Deleted gzip file: {download_path}", file=sys.stderr)
            print(f"Audio saved to: {extracted_path}", file=sys.stderr)
            return str(extracted_path)

        except Exception as e:
            print(f"Failed to extract gzip: {e}", file=sys.stderr)
            return str(download_path)

    # If it's a zip file, extract and delete the zip
    if extension.lower() == ".zip" or zipfile.is_zipfile(download_path):
        print(f"Extracting zip file...", file=sys.stderr)
        try:
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(output_path)
                extracted_files = zip_ref.namelist()

            # Delete the zip file
            os.remove(download_path)
            print(f"Deleted zip file: {download_path}", file=sys.stderr)

            # Return path to the first extracted audio file
            audio_extensions = {'.wav', '.mp3', '.ogg', '.m4a', '.flac', '.webm'}
            for extracted in extracted_files:
                if Path(extracted).suffix.lower() in audio_extensions:
                    final_path = output_path / extracted
                    print(f"Audio saved to: {final_path}", file=sys.stderr)
                    return str(final_path)

            # If no audio file found, return first extracted file
            if extracted_files:
                final_path = output_path / extracted_files[0]
                print(f"Extracted file saved to: {final_path}", file=sys.stderr)
                return str(final_path)

        except Exception as e:
            print(f"Failed to extract zip: {e}", file=sys.stderr)
            return str(download_path)

    print(f"Audio saved to: {download_path}", file=sys.stderr)
    return str(download_path)


def make_call(
    phone_number: str,
    system_prompt: str,
    voice_id: str = "virginia",
    welcome_message: str | None = None,
    template_variables: dict[str, str] | None = None,
    languages: list[str] | None = None,
    boosted_keywords: list[str] | None = None,
    tools: list[str] | None = None,
    max_wait_seconds: int = 600,
    poll_interval_seconds: int = 5,
    output_dir: str | None = None,
) -> dict:
    """
    Make an outbound call and wait for completion.

    Args:
        phone_number: Phone number to call (E.164 format, e.g., +1234567890)
        system_prompt: Instructions for the AI agent
        voice_id: Voice selection (default: "virginia")
        welcome_message: Custom opening line (optional)
        template_variables: Variables for {{placeholder}} substitution
        languages: ISO 639-1 language codes for recognition ("en" always included)
        boosted_keywords: Words/phrases for better recognition
        tools: Tool names to enable ("keypad_input" always included)
        max_wait_seconds: Maximum time to wait for call completion
        poll_interval_seconds: Interval between status checks
        output_dir: Directory to save audio recording (optional)

    Returns:
        dict with conversation_id, transcript, ended_by, duration_ms, audio_file, etc.
    """
    client = Phonic()

    # Build config
    config = {
        "system_prompt": system_prompt,
        "voice_id": voice_id,
    }

    if welcome_message:
        config["welcome_message"] = welcome_message
    if template_variables:
        config["template_variables"] = template_variables

    # Languages: always include "en"
    config_languages = ["en"]
    if languages:
        config_languages = list(dict.fromkeys(["en"] + languages))  # dedupe, en first
    config["languages"] = config_languages

    if boosted_keywords:
        config["boosted_keywords"] = boosted_keywords

    # Tools: always include "keypad_input"
    config_tools = ["keypad_input"]
    if tools:
        config_tools = list(dict.fromkeys(["keypad_input"] + tools))  # dedupe
    config["tools"] = config_tools

    # Initiate call
    print(f"Initiating call to {phone_number}...", file=sys.stderr)
    result = client.conversations.outbound_call(
        to_phone_number=phone_number,
        config=config,
    )
    conversation_id = result.conversation_id
    print(f"Call started: {conversation_id}", file=sys.stderr)

    # Poll for completion with progress output
    start_time = time.time()
    while True:
        elapsed = int(time.time() - start_time)

        if elapsed > max_wait_seconds:
            raise TimeoutError(f"Call did not complete within {max_wait_seconds} seconds")

        response = client.conversations.get(conversation_id)
        conversation = response.conversation

        if conversation.ended_at is not None:
            print(f"Call completed after {elapsed}s", file=sys.stderr)
            break

        print(f"Waiting for call completion... {elapsed}s elapsed", file=sys.stderr)
        time.sleep(poll_interval_seconds)

    # Extract transcript (prefer post-call for accuracy)
    transcript = get_transcript(conversation)

    # Download audio if output_dir specified and audio_url available
    audio_file = None
    if output_dir and conversation.audio_url:
        audio_file = download_audio(conversation.audio_url, conversation_id, output_dir)

    # Build result
    return {
        "conversation_id": conversation_id,
        "ended_by": conversation.ended_by,
        "ended_at": str(conversation.ended_at) if conversation.ended_at else None,
        "duration_ms": conversation.duration_ms,
        "transcript": transcript,
        "audio_file": audio_file,
        "items": [
            {
                "role": item.role,
                "text": item.post_call_transcript or item.live_transcript,
                "duration_ms": item.duration_ms,
            }
            for item in conversation.items
        ],
    }


def get_transcript(conversation) -> str:
    """Extract transcript text from conversation, preferring post-call version."""
    # First try the full post-call transcript
    if conversation.post_call_transcript:
        return conversation.post_call_transcript

    # Fall back to live transcript
    if conversation.live_transcript:
        return conversation.live_transcript

    # Build from items if no full transcript available
    lines = []
    for item in conversation.items:
        speaker = "Agent" if item.role == "assistant" else "User"
        text = item.post_call_transcript or item.live_transcript
        if text:
            lines.append(f"{speaker}: {text}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Make outbound call using Phonic AI telephone agent"
    )
    parser.add_argument(
        "phone_number",
        help="Phone number to call (E.164 format, e.g., +1234567890)",
    )
    parser.add_argument(
        "--system-prompt",
        "-s",
        required=True,
        help="Instructions for the AI agent",
    )
    parser.add_argument(
        "--voice",
        "-v",
        default="virginia",
        help="Voice ID (default: virginia)",
    )
    parser.add_argument(
        "--welcome-message",
        "-w",
        help="Custom opening line (optional - agent generates greeting from system_prompt if not specified)",
    )
    parser.add_argument(
        "--languages",
        "-l",
        nargs="+",
        help="ISO 639-1 language codes (e.g., en es)",
    )
    parser.add_argument(
        "--boosted-keywords",
        "-k",
        nargs="+",
        help="Words/phrases for better recognition",
    )
    parser.add_argument(
        "--tools",
        "-t",
        nargs="+",
        help="Tool names to enable (keypad_input always included)",
    )
    parser.add_argument(
        "--max-wait",
        type=int,
        default=600,
        help="Maximum seconds to wait for call completion (default: 600)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=5,
        help="Seconds between status checks (default: 5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Directory to save audio recording",
    )

    args = parser.parse_args()

    try:
        result = make_call(
            phone_number=args.phone_number,
            system_prompt=args.system_prompt,
            voice_id=args.voice,
            welcome_message=args.welcome_message,
            languages=args.languages,
            boosted_keywords=args.boosted_keywords,
            tools=args.tools,
            max_wait_seconds=args.max_wait,
            poll_interval_seconds=args.poll_interval,
            output_dir=args.output_dir,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n=== Call Summary ===")
            print(f"Conversation ID: {result['conversation_id']}")
            print(f"Ended by: {result['ended_by']}")
            print(f"Duration: {result['duration_ms'] / 1000:.1f}s")
            if result.get("audio_file"):
                print(f"Audio: {result['audio_file']}")
            print(f"\n=== Transcript ===")
            print(result["transcript"])

    except TimeoutError as e:
        print(f"Timeout: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
