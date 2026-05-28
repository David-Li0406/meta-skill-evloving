#!/usr/bin/env python3
"""
Check Azure authentication status and prompt for az login if needed.
Uses AzureDefaultCredential to verify authentication.
"""

import subprocess
import sys
from typing import Tuple


def check_azure_cli_installed() -> bool:
    """Check if Azure CLI is installed."""
    try:
        result = subprocess.run(
            ["az", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_azure_cli_logged_in() -> Tuple[bool, str | None]:
    """Check if user is logged in via Azure CLI."""
    try:
        result = subprocess.run(
            ["az", "account", "show", "--output", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            import json
            account = json.loads(result.stdout)
            user = account.get("user", {}).get("name", "unknown")
            return True, user
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return False, None


def check_default_credential() -> Tuple[bool, str | None]:
    """Check if AzureDefaultCredential can obtain a token."""
    try:
        from azure.identity import DefaultAzureCredential
        from azure.core.exceptions import ClientAuthenticationError
        
        credential = DefaultAzureCredential()
        # Try to get a token for Azure management scope
        token = credential.get_token("https://management.azure.com/.default")
        return True, "Token obtained successfully"
    except ClientAuthenticationError as e:
        return False, str(e)
    except ImportError:
        return False, "azure-identity not installed. Run: pip install azure-identity"
    except Exception as e:
        return False, f"Unexpected error: {type(e).__name__}: {e}"


def run_az_login() -> bool:
    """Run az login interactively."""
    print("\nStarting Azure login...")
    print("A browser window will open for authentication.\n")
    
    try:
        result = subprocess.run(
            ["az", "login"],
            timeout=300  # 5 minute timeout for interactive login
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("ERROR: Login timed out after 5 minutes.")
        return False
    except FileNotFoundError:
        print("ERROR: Azure CLI not found.")
        return False


def main() -> int:
    """Main entry point."""
    print("Checking Azure authentication status...\n")
    
    # Check if Azure CLI is installed
    if not check_azure_cli_installed():
        print("WARNING: Azure CLI is not installed.")
        print("Install it from: https://docs.microsoft.com/cli/azure/install-azure-cli")
        print("\nAttempting to use AzureDefaultCredential anyway...\n")
    
    # Check AzureDefaultCredential
    auth_ok, message = check_default_credential()
    
    if auth_ok:
        # Also show who is logged in via CLI if available
        cli_ok, user = check_azure_cli_logged_in()
        if cli_ok:
            print(f"✓ Authenticated as: {user}")
        else:
            print("✓ Authentication successful via AzureDefaultCredential")
        print("✓ Ready to call Foundry agents")
        return 0
    
    print(f"✗ Authentication failed: {message}")
    
    # Offer to run az login
    if check_azure_cli_installed():
        print("\nWould you like to run 'az login' to authenticate?")
        response = input("Enter 'y' to login, any other key to exit: ").strip().lower()
        
        if response == 'y':
            if run_az_login():
                # Verify login worked
                auth_ok, _ = check_default_credential()
                if auth_ok:
                    print("\n✓ Login successful! Ready to call Foundry agents.")
                    return 0
                else:
                    print("\n✗ Login completed but authentication still failing.")
                    return 1
            else:
                print("\n✗ Login failed.")
                return 1
    else:
        print("\nTo authenticate, install Azure CLI and run: az login")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
