#!/usr/bin/env python3
"""
Make phone calls with natural AI voices using ElevenLabs and Twilio.

Usage:
    ./voice_call.py --to "+61431431907" --message "Hello, this is a test call"
    ./voice_call.py --to "+61431431907" --message "Hello" --voice sarah --from-us
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse

# Default configuration
DEFAULT_VOICE = "charlie"
DEFAULT_MODEL = "eleven_v3"
DEFAULT_FROM_AU = "+61348279516"
DEFAULT_FROM_US = "+19788785597"

# Available voices
VOICES = {
    "charlie": {"id": "IKne3meq5aSn9XLyUdCD", "accent": "Australian"},
    "george": {"id": "JBFqnCBsd6RMkjVDRZzb", "accent": "British"},
    "alice": {"id": "Xb7hH8MSUJpSbSDYk0k2", "accent": "British"},
    "sarah": {"id": "EXAVITQu4vr4xnSDxMaL", "accent": "American"},
    "roger": {"id": "CwhRBWXzGAHq8TQ4Fs17", "accent": "American"},
    "laura": {"id": "FGY2WhTYpPnrIDTdsKH5", "accent": "American"},
    "matilda": {"id": "XrExE9yKIg1WjnnlVkGX", "accent": "American"},
}


def get_api_key():
    """Get ElevenLabs API key from environment or .env file."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if api_key:
        return api_key

    # Try loading from .env file
    env_paths = [
        os.path.join(os.getcwd(), ".env"),
        os.path.expanduser("~/.env"),
    ]

    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("ELEVENLABS_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def normalise_phone_number(phone: str) -> str:
    """Convert phone number to E.164 format."""
    # Remove spaces and dashes
    phone = re.sub(r"[\s\-()]", "", phone)

    # Australian mobile starting with 04
    if phone.startswith("04") and len(phone) == 10:
        return "+61" + phone[1:]

    # Australian landline starting with 0
    if phone.startswith("0") and len(phone) == 10:
        return "+61" + phone[1:]

    # Already has country code
    if phone.startswith("+"):
        return phone

    # Assume Australian if no country code
    return "+61" + phone


def generate_audio(text: str, voice_id: str, api_key: str, output_path: str) -> bool:
    """Generate audio using ElevenLabs API."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"

    data = json.dumps({
        "text": text,
        "model_id": DEFAULT_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return True
    except urllib.error.HTTPError as e:
        print(f"Error generating audio: {e.code} - {e.read().decode()}", file=sys.stderr)
        return False


def upload_audio(file_path: str) -> str:
    """Upload audio file to tmpfiles.org and return direct URL."""
    # Use curl for multipart upload (simpler than urllib)
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "-F", f"file=@{file_path}", "https://tmpfiles.org/api/v1/upload"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error uploading file: {result.stderr}", file=sys.stderr)
        return None

    try:
        response = json.loads(result.stdout)
        url = response["data"]["url"]
        # Convert to direct download URL
        # http://tmpfiles.org/XXXXXX/file.mp3 -> https://tmpfiles.org/dl/XXXXXX/file.mp3
        direct_url = url.replace("http://tmpfiles.org/", "https://tmpfiles.org/dl/")
        return direct_url
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing upload response: {e}", file=sys.stderr)
        return None


def make_call(from_number: str, to_number: str, audio_url: str) -> dict:
    """Make a phone call using Twilio CLI."""
    twiml = f"<Response><Play>{audio_url}</Play></Response>"

    result = subprocess.run(
        [
            "twilio", "api:core:calls:create",
            "--from", from_number,
            "--to", to_number,
            "--twiml", twiml,
            "-o", "json"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error making call: {result.stderr}", file=sys.stderr)
        return None

    try:
        # Twilio CLI returns array
        calls = json.loads(result.stdout)
        return calls[0] if calls else None
    except json.JSONDecodeError:
        # Try parsing as plain output
        return {"output": result.stdout}


def send_sms(from_number: str, to_number: str, message: str) -> dict:
    """Send SMS using Twilio CLI."""
    result = subprocess.run(
        [
            "twilio", "api:core:messages:create",
            "--from", from_number,
            "--to", to_number,
            "--body", message,
            "-o", "json"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error sending SMS: {result.stderr}", file=sys.stderr)
        return None

    try:
        messages = json.loads(result.stdout)
        return messages[0] if messages else None
    except json.JSONDecodeError:
        return {"output": result.stdout}


def main():
    parser = argparse.ArgumentParser(
        description="Make phone calls with natural AI voices using ElevenLabs and Twilio"
    )
    parser.add_argument("--to", help="Phone number to call (E.164 or Australian format)")
    parser.add_argument("--message", help="Message to speak")
    parser.add_argument("--voice", default=DEFAULT_VOICE, choices=list(VOICES.keys()),
                        help=f"Voice to use (default: {DEFAULT_VOICE})")
    parser.add_argument("--from-us", action="store_true", help="Use US number instead of Australian")
    parser.add_argument("--from-number", help="Custom from number (overrides --from-us)")
    parser.add_argument("--sms", action="store_true", help="Send SMS instead of making a call")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")

    args = parser.parse_args()

    if args.list_voices:
        print("Available voices:")
        for name, info in VOICES.items():
            print(f"  {name}: {info['accent']} ({info['id']})")
        return 0

    # Validate required args for call/sms
    if not args.to or not args.message:
        parser.error("--to and --message are required for calls and SMS")
        return 1

    # Determine from number
    if args.from_number:
        from_number = args.from_number
    elif args.from_us:
        from_number = DEFAULT_FROM_US
    else:
        from_number = DEFAULT_FROM_AU

    # Normalise to number
    to_number = normalise_phone_number(args.to)

    # SMS mode
    if args.sms:
        print(f"Sending SMS to {to_number}...")
        result = send_sms(from_number, to_number, args.message)
        if result:
            print(f"SMS sent! SID: {result.get('sid', 'unknown')}")
            return 0
        return 1

    # Voice call mode
    api_key = get_api_key()
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment or .env file", file=sys.stderr)
        return 1

    voice_info = VOICES[args.voice]
    print(f"Generating audio with {args.voice} ({voice_info['accent']}) voice...")

    # Generate audio
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        audio_path = f.name

    if not generate_audio(args.message, voice_info["id"], api_key, audio_path):
        return 1

    print(f"Audio generated: {audio_path}")

    # Upload audio
    print("Uploading audio...")
    audio_url = upload_audio(audio_path)
    if not audio_url:
        return 1

    print(f"Audio URL: {audio_url}")

    # Make call
    print(f"Calling {to_number} from {from_number}...")
    result = make_call(from_number, to_number, audio_url)

    if result:
        sid = result.get("sid", "unknown")
        status = result.get("status", "unknown")
        print(f"Call initiated! SID: {sid}, Status: {status}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
