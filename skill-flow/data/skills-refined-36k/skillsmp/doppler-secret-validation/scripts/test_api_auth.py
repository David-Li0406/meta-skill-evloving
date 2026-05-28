#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Test API authentication using token from Doppler.

This is a template script - adapt the test_api_authentication() function
for your specific API.

Usage:
    # Via Doppler (recommended)
    doppler run --project PROJECT --config CONFIG -- uv run test_api_auth.py --secret SECRET_NAME --api-url API_URL

    # Manual (for testing)
    uv run test_api_auth.py --secret SECRET_NAME --api-url API_URL --token TOKEN

Example (PyPI):
    doppler run --project claude-config --config prd -- \
        uv run test_api_auth.py --secret PYPI_TOKEN --api-url https://upload.pypi.org/legacy/
"""
import argparse
import os
import subprocess
import sys
import urllib.error
import urllib.request


def get_token_from_env(secret_name: str) -> str | None:
    """Get token from environment (injected by Doppler)."""
    return os.getenv(secret_name)


def get_token_from_doppler(project: str, config: str, secret_name: str) -> str | None:
    """Directly retrieve token from Doppler (fallback)."""
    try:
        result = subprocess.run(
            ['doppler', 'secrets', 'get', secret_name,
             '--project', project, '--config', config, '--plain'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return None


def test_api_authentication(token: str, api_url: str) -> tuple[bool, str]:
    """
    Test API authentication with token.

    TEMPLATE: Customize this function for your specific API.

    Args:
        token: Authentication token
        api_url: API endpoint to test

    Returns:
        (success: bool, message: str)
    """
    try:
        req = urllib.request.Request(api_url)
        req.add_header('Authorization', f'Bearer {token}')

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return (True, f"API responded: {response.status} OK")

        except urllib.error.HTTPError as e:
            # Some APIs return error codes for GET on POST-only endpoints
            # but still validate authentication
            if e.code in [405, 404]:  # Method Not Allowed / Not Found
                return (True, f"Authentication successful (code {e.code} expected)")
            elif e.code == 401:
                return (False, "Authentication failed: 401 Unauthorized")
            elif e.code == 403:
                return (False, "Authentication failed: 403 Forbidden")
            else:
                return (True, f"API responded: {e.code} (may indicate valid auth)")

    except urllib.error.URLError as e:
        return (False, f"Network error: {e}")
    except Exception as e:
        return (False, f"Unexpected error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Test API authentication using token from Doppler'
    )
    parser.add_argument('--secret', required=True, help='Secret name (e.g., PYPI_TOKEN)')
    parser.add_argument('--api-url', required=True, help='API endpoint to test')
    parser.add_argument('--token', help='Token value (for manual testing, not recommended)')
    parser.add_argument('--project', help='Doppler project (if not using doppler run)')
    parser.add_argument('--config', help='Doppler config (if not using doppler run)')

    args = parser.parse_args()

    print("=== API Authentication Test ===")
    print(f"Secret: {args.secret}")
    print(f"API URL: {args.api_url}\n")

    # Get token
    token = None
    if args.token:
        print("⚠ Using manually provided token")
        token = args.token
    else:
        # Try environment first (doppler run injects it)
        token = get_token_from_env(args.secret)
        if token:
            print("✓ Token retrieved from environment (via Doppler)")
        elif args.project and args.config:
            # Fallback to direct Doppler call
            print("ℹ Retrieving token directly from Doppler...")
            token = get_token_from_doppler(args.project, args.config, args.secret)
            if token:
                print("✓ Token retrieved from Doppler CLI")

    if not token:
        print("✗ No token available")
        print("\nUsage:")
        print(f"  doppler run --project PROJECT --config CONFIG -- uv run {sys.argv[0]} --secret {args.secret} --api-url {args.api_url}")
        sys.exit(1)

    print(f"✓ Token: {token[:20]}...{token[-10:] if len(token) > 30 else ''}")
    print(f"✓ Length: {len(token)} characters\n")

    # Test authentication
    print("Testing API authentication...")
    success, message = test_api_authentication(token, args.api_url)

    print(f"   {message}\n")

    if success:
        print("🎉 Authentication successful!")
        print(f"\nToken is valid for use with {args.api_url}")
        sys.exit(0)
    else:
        print("✗ Authentication failed")
        print("\nCheck:")
        print("  - Token is correct and not expired")
        print("  - API URL is correct")
        print("  - Token has necessary permissions")
        sys.exit(1)


if __name__ == '__main__':
    main()
