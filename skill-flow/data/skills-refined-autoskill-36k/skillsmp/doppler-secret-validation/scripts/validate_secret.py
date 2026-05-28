#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Validate secret storage and retrieval from Doppler.

Usage:
    uv run validate_secret.py --project PROJECT --config CONFIG --secret SECRET_NAME

Example:
    uv run validate_secret.py --project claude-config --config prd --secret PYPI_TOKEN
"""
import argparse
import subprocess
import sys


def get_secret_from_doppler(project: str, config: str, secret_name: str) -> tuple[bool, str]:
    """
    Retrieve secret from Doppler.

    Returns:
        (success: bool, value: str or error_message: str)
    """
    try:
        result = subprocess.run(
            ['doppler', 'secrets', 'get', secret_name,
             '--project', project, '--config', config, '--plain'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return (True, result.stdout.strip())
    except subprocess.CalledProcessError as e:
        return (False, f"Failed to retrieve secret: {e.stderr}")
    except subprocess.TimeoutExpired:
        return (False, "Doppler command timed out after 10 seconds")
    except FileNotFoundError:
        return (False, "Doppler CLI not found. Install via: brew install dopplerhq/cli/doppler")


def verify_secret_exists(project: str, config: str, secret_name: str) -> bool:
    """Check if secret exists in Doppler config."""
    try:
        result = subprocess.run(
            ['doppler', 'secrets', '--project', project, '--config', config, '--only-names'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return secret_name in result.stdout.split('\n')
    except subprocess.CalledProcessError as e:
        print(f"[doppler-secret-validation] Failed to list secrets: {e.stderr or e}", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("[doppler-secret-validation] Doppler command timed out", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("[doppler-secret-validation] Doppler CLI not found", file=sys.stderr)
        return False


def test_env_injection(project: str, config: str, secret_name: str) -> bool:
    """Test that Doppler injects secret into environment."""
    try:
        result = subprocess.run(
            ['doppler', 'run', '--project', project, '--config', config, '--',
             'python3', '-c', f'import os; v = os.getenv("{secret_name}"); print("OK" if v else "MISSING")'],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return 'OK' in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[doppler-secret-validation] Environment injection failed: {e.stderr or e}", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("[doppler-secret-validation] Environment injection timed out", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("[doppler-secret-validation] Doppler CLI not found", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate secret storage and retrieval from Doppler'
    )
    parser.add_argument('--project', required=True, help='Doppler project name')
    parser.add_argument('--config', required=True, help='Doppler config name (e.g., dev, prd)')
    parser.add_argument('--secret', required=True, help='Secret name to validate')
    parser.add_argument('--show-value', action='store_true',
                       help='Show secret value (security risk, use only for debugging)')

    args = parser.parse_args()

    print(f"=== Validating Secret: {args.secret} ===")
    print(f"Project: {args.project}")
    print(f"Config: {args.config}\n")

    # Test 1: Check existence
    print("1. Checking if secret exists...")
    exists = verify_secret_exists(args.project, args.config, args.secret)
    if exists:
        print(f"   ✓ Secret '{args.secret}' exists in {args.project}/{args.config}\n")
    else:
        print(f"   ✗ Secret '{args.secret}' NOT found in {args.project}/{args.config}\n")
        sys.exit(1)

    # Test 2: Retrieve secret
    print("2. Retrieving secret value...")
    success, value = get_secret_from_doppler(args.project, args.config, args.secret)
    if success:
        if args.show_value:
            print(f"   ✓ Retrieved: {value}\n")
        else:
            print(f"   ✓ Retrieved: {value[:20]}...{value[-10:] if len(value) > 30 else ''}")
            print(f"   ✓ Length: {len(value)} characters\n")
    else:
        print(f"   ✗ {value}\n")
        sys.exit(1)

    # Test 3: Environment injection
    print("3. Testing environment injection...")
    injected = test_env_injection(args.project, args.config, args.secret)
    if injected:
        print("   ✓ Environment injection working\n")
    else:
        print("   ✗ Environment injection failed\n")
        sys.exit(1)

    # Summary
    print("=== Validation Summary ===")
    print("✓ Secret exists in Doppler")
    print("✓ Secret retrieval working")
    print("✓ Environment injection working")
    print(f"\n🎉 Secret '{args.secret}' is fully operational!")
    print("\nUsage:")
    print(f"  doppler run --project {args.project} --config {args.config} -- <command>")


if __name__ == '__main__':
    main()
