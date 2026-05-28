#!/usr/bin/env python3
"""
Get Dify plugin debugging credentials.

Usage:
    # First time: will prompt for credentials and save to .credential
    python get_debug_key.py

    # With explicit credentials (also saves to .credential)
    python get_debug_key.py --host https://your-dify.com --email user@example.com --password yourpassword

    # Output as .env format
    python get_debug_key.py --output-env > .env

This script will:
1. Read credentials from .credential file (or prompt if not exists)
2. Login to Dify console API
3. Fetch the plugin debugging key
4. Output the key for use in .env file
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import httpx

# Default credential file location (project root)
CREDENTIAL_FILE = ".credential"


def login(host: str, email: str, password: str) -> tuple[str, dict, str]:
    """Login to Dify and get access token from cookies."""
    url = f"{host.rstrip('/')}/console/api/login"

    # Password needs to be base64 encoded
    encoded_password = base64.b64encode(password.encode()).decode()

    response = httpx.post(
        url,
        json={
            "email": email,
            "password": encoded_password,
            "remember_me": True,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")

    # Access token is in cookies, not response body
    # Cookie names may have __Host- prefix for secure cookies
    cookies = dict(response.cookies)
    access_token = cookies.get("access_token") or cookies.get("__Host-access_token")
    csrf_token = cookies.get("csrf_token") or cookies.get("__Host-csrf_token")

    if not access_token:
        raise Exception(f"No access_token in cookies. Cookies: {list(cookies.keys())}")

    return access_token, cookies, csrf_token


def get_debugging_key(host: str, cookies: dict, csrf_token: str) -> str:
    """Get plugin debugging key from Dify."""
    url = f"{host.rstrip('/')}/console/api/workspaces/current/plugin/debugging-key"

    response = httpx.get(
        url,
        cookies=cookies,
        headers={
            "X-CSRF-Token": csrf_token,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get debugging key: {response.status_code} - {response.text}")

    data = response.json()
    if "key" not in data:
        raise Exception(f"Unexpected response: {data}")

    return data["key"]


def find_credential_file() -> Path | None:
    """Find .credential file in current directory or parent directories."""
    current = Path.cwd()
    while current != current.parent:
        cred_path = current / CREDENTIAL_FILE
        if cred_path.exists():
            return cred_path
        current = current.parent
    # Check current directory as fallback
    cred_path = Path.cwd() / CREDENTIAL_FILE
    return cred_path if cred_path.exists() else None


def load_credentials(credential_file: Path | None = None) -> dict | None:
    """Load credentials from .credential file."""
    if credential_file is None:
        credential_file = find_credential_file()
    if credential_file is None or not credential_file.exists():
        return None

    try:
        with open(credential_file) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to read {credential_file}: {e}", file=sys.stderr)
        return None


def save_credentials(host: str, email: str, password: str, credential_file: Path | None = None) -> Path:
    """Save credentials to .credential file in project root."""
    if credential_file is None:
        # Save to current working directory
        credential_file = Path.cwd() / CREDENTIAL_FILE

    credentials = {
        "host": host,
        "email": email,
        "password": password,
    }

    with open(credential_file, "w") as f:
        json.dump(credentials, f, indent=2)

    # Set restrictive permissions (owner read/write only)
    os.chmod(credential_file, 0o600)

    print(f"Credentials saved to {credential_file}", file=sys.stderr)
    return credential_file


def prompt_for_credentials() -> tuple[str, str, str]:
    """Prompt user for credentials interactively."""
    import getpass

    print("No credentials found. Please enter Dify credentials:", file=sys.stderr)
    print("(These will be saved to .credential for future use)", file=sys.stderr)
    print(file=sys.stderr)

    host = input("Dify host URL (e.g., https://your-dify.com): ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")

    return host, email, password


def main():
    parser = argparse.ArgumentParser(
        description="Get Dify plugin debugging credentials"
    )
    parser.add_argument(
        "--host",
        help="Dify host URL (e.g., https://your-dify.com)",
    )
    parser.add_argument(
        "--email",
        help="Dify account email",
    )
    parser.add_argument(
        "--password",
        help="Dify account password",
    )
    parser.add_argument(
        "--output-env",
        action="store_true",
        help="Output as .env format",
    )
    parser.add_argument(
        "--credential-file",
        type=Path,
        help=f"Path to credential file (default: ./{CREDENTIAL_FILE})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save credentials to file",
    )

    args = parser.parse_args()

    try:
        host = args.host
        email = args.email
        password = args.password
        credential_file = args.credential_file

        # Try to load from credential file if not all args provided
        if not all([host, email, password]):
            saved_creds = load_credentials(credential_file)
            if saved_creds:
                host = host or saved_creds.get("host")
                email = email or saved_creds.get("email")
                password = password or saved_creds.get("password")
                print(f"Loaded credentials from {find_credential_file() or CREDENTIAL_FILE}", file=sys.stderr)

        # If still missing, prompt interactively
        if not all([host, email, password]):
            host, email, password = prompt_for_credentials()

        # Save credentials if not disabled
        if not args.no_save:
            save_credentials(host, email, password, credential_file)

        # Step 1: Login
        print(f"Logging in to {host}...", file=sys.stderr)
        access_token, cookies, csrf_token = login(host, email, password)
        print("Login successful.", file=sys.stderr)

        # Step 2: Get debugging key
        print("Fetching debugging key...", file=sys.stderr)
        debug_key = get_debugging_key(host, cookies, csrf_token)

        # Output
        if args.output_env:
            print(f"INSTALL_METHOD=remote")
            print(f"REMOTE_INSTALL_HOST={host}")
            print(f"REMOTE_INSTALL_PORT=5003")
            print(f"REMOTE_INSTALL_KEY={debug_key}")
        else:
            print(f"\nDebugging Key: {debug_key}")
            print(f"\nAdd to your plugin's .env file:")
            print(f"  INSTALL_METHOD=remote")
            print(f"  REMOTE_INSTALL_HOST={host}")
            print(f"  REMOTE_INSTALL_PORT=5003")
            print(f"  REMOTE_INSTALL_KEY={debug_key}")

    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
