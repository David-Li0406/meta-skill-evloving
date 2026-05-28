#!/usr/bin/env python3
"""
Smart connect for Push integration (Doctor Mode).

This script is a comprehensive health check and connect tool:
- Version check: Compare local vs remote plugin version
- API validation: Verify API key is still valid
- Project registration: Register current project with keywords
- Authentication: Handle initial auth or re-auth when needed

Usage:
    python connect.py                      # Full doctor flow
    python connect.py --check-version      # Check for updates only
    python connect.py --update             # Update to latest version
    python connect.py --validate-key       # Validate API key only
    python connect.py --client claude-code # Explicit client type
    python connect.py --reauth             # Force re-authentication

See: /docs/20260114_cli_action_auto_creation_implementation_plan.md
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import webbrowser
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# Configuration
API_BASE = "https://jxuzqcbqhiaxmfitzxlo.supabase.co/functions/v1"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4dXpxY2JxaGlheG1maXR6eGxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU2OTY5MzQsImV4cCI6MjA1MTI3MjkzNH0.4Nm5_ABkgJCrrFc-bVzbx8qAp-SQo92HKziH7TBgspo"
CONFIG_DIR = os.path.expanduser("~/.config/push")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

# Plugin version checking
REMOTE_PLUGIN_JSON_URL = "https://raw.githubusercontent.com/MasslessAI/push-todo-cli/main/plugins/push-todo/.claude-plugin/plugin.json"
INSTALL_SCRIPT_URL = "https://raw.githubusercontent.com/MasslessAI/push-todo-cli/main/install.sh"
CODEX_INSTALL_SCRIPT_URL = "https://raw.githubusercontent.com/MasslessAI/push-todo-cli/main/codex/install-codex.sh"


class SlowDownError(Exception):
    """Raised when polling too frequently."""
    def __init__(self, new_interval: int):
        self.new_interval = new_interval


# ============================================================================
# CONFIG FILE HELPERS
# ============================================================================

def get_existing_key() -> Optional[str]:
    """Get existing API key from config."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                for line in f:
                    if line.startswith("export PUSH_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"\'')
                        return key if key else None
        except Exception:
            pass
    return None


def get_existing_email() -> Optional[str]:
    """Get existing email from config."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                for line in f:
                    if line.startswith("export PUSH_EMAIL="):
                        email = line.split("=", 1)[1].strip().strip('"\'')
                        return email if email else None
        except Exception:
            pass
    return None


def save_config(api_key: str, email: str):
    """Save API key and email to config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        f.write(f'export PUSH_API_KEY="{api_key}"\n')
        f.write(f'export PUSH_EMAIL="{email}"\n')

    # Set restrictive permissions
    os.chmod(CONFIG_FILE, 0o600)


def clear_config():
    """Clear the config file (for re-auth)."""
    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
        except Exception:
            pass


# ============================================================================
# VERSION CHECKING & UPDATE
# ============================================================================

def get_local_version() -> Optional[str]:
    """Get the local plugin version from plugin.json."""
    plugin_dir = Path(__file__).parent.parent
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

    if not plugin_json.exists():
        return None

    try:
        with open(plugin_json) as f:
            data = json.load(f)
            return data.get("version")
    except Exception:
        return None


def get_remote_version() -> Optional[str]:
    """Fetch the remote plugin version from GitHub."""
    try:
        req = urllib.request.Request(
            REMOTE_PLUGIN_JSON_URL,
            headers={"User-Agent": "push-cli/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("version")
    except Exception:
        return None


def parse_version(version_str: str) -> tuple:
    """Parse version string into comparable tuple."""
    try:
        parts = version_str.split(".")
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_version() -> dict:
    """
    Check if an update is available.

    Returns dict with:
        - status: "up_to_date", "update_available", "unknown"
        - local_version: Current local version
        - remote_version: Latest remote version
        - message: Human-readable message
    """
    local = get_local_version()
    remote = get_remote_version()

    if not local:
        return {
            "status": "unknown",
            "local_version": None,
            "remote_version": remote,
            "message": "Could not determine local version"
        }

    if not remote:
        return {
            "status": "unknown",
            "local_version": local,
            "remote_version": None,
            "message": "Could not fetch remote version (network error)"
        }

    local_tuple = parse_version(local)
    remote_tuple = parse_version(remote)

    if remote_tuple > local_tuple:
        return {
            "status": "update_available",
            "local_version": local,
            "remote_version": remote,
            "message": f"Update available: {local} → {remote}"
        }

    return {
        "status": "up_to_date",
        "local_version": local,
        "remote_version": remote,
        "message": f"Plugin is up to date (v{local})"
    }


def do_update() -> dict:
    """
    Update the plugin by re-running the install script.

    Returns dict with:
        - status: "success", "failed", "skipped", "manual_required"
        - message: Human-readable message
        - command: (optional) Command for user to run manually
    """
    method = get_installation_method()

    if method == "marketplace":
        # Claude Code marketplace - check if auto-update is enabled
        auto_update = is_marketplace_auto_update_enabled()

        if auto_update is True:
            # Auto-update is ON - Claude Code handles updates automatically
            return {
                "status": "skipped",
                "message": "Marketplace auto-update is enabled - Claude Code handles updates automatically",
                "auto_update_enabled": True
            }
        else:
            # Auto-update is OFF or unknown (defaults to OFF for third-party)
            # User must run update command themselves
            return {
                "status": "manual_required",
                "message": "Marketplace auto-update is disabled - run update command in Claude Code",
                "command": "claude plugin update push-todo@push-todo-cli",
                "auto_update_enabled": False,
                "hint": "To enable auto-updates: /plugin → Marketplaces → push-todo-cli → Enable auto-update"
            }

    if method == "codex":
        # Codex installation - re-run the Codex install script
        try:
            result = subprocess.run(
                ["bash", "-c", f"curl -fsSL {CODEX_INSTALL_SCRIPT_URL} | bash"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return {
                    "status": "success",
                    "message": "Codex skill updated successfully"
                }
            else:
                return {
                    "status": "failed",
                    "message": f"Update failed: {result.stderr or 'Unknown error'}"
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "message": "Update timed out"
            }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Update failed: {e}"
            }

    if method == "development":
        return {
            "status": "skipped",
            "message": "Development installation - use git pull instead"
        }

    # Legacy installation - run curl installer
    try:
        result = subprocess.run(
            ["bash", "-c", f"curl -fsSL {INSTALL_SCRIPT_URL} | bash"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Plugin updated successfully"
            }
        else:
            return {
                "status": "failed",
                "message": f"Update failed: {result.stderr or 'Unknown error'}"
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "message": "Update timed out"
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": f"Update failed: {e}"
        }


# ============================================================================
# API KEY VALIDATION
# ============================================================================

def validate_api_key(api_key: str) -> dict:
    """
    Validate an API key with the backend.

    This makes a lightweight request to check if the key is still valid.

    Returns dict with:
        - status: "valid", "invalid", "revoked", "error"
        - message: Human-readable message
        - email: User's email (if valid)
    """
    # Use synced-todos endpoint with a minimal request to validate key
    # This is a read-only endpoint that returns quickly
    req = urllib.request.Request(
        f"{API_BASE}/synced-todos?limit=0",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            # If we get here, the key is valid
            return {
                "status": "valid",
                "message": "API key is valid",
                "email": get_existing_email()
            }
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return {
                "status": "invalid",
                "message": "API key is invalid or revoked"
            }
        elif e.code == 403:
            return {
                "status": "revoked",
                "message": "API key has been revoked"
            }
        else:
            return {
                "status": "error",
                "message": f"Server error: {e.code}"
            }
    except urllib.error.URLError as e:
        return {
            "status": "error",
            "message": f"Network error: {e.reason}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Validation failed: {e}"
        }


# ============================================================================
# CONTEXT COLLECTION
# ============================================================================

def get_device_name() -> str:
    """Get the computer's hostname for device identification."""
    try:
        return platform.node() or "Unknown Device"
    except Exception:
        return "Unknown Device"


def get_project_path() -> str:
    """Get the current working directory."""
    try:
        return os.getcwd()
    except Exception:
        return ""


def get_git_remote() -> Optional[str]:
    """Get the git remote URL (origin) if in a git repo.

    Returns the origin remote URL, or None if not a git repo or no origin.
    This is used for git-first project identification.
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip() or None
        return None
    except Exception:
        return None


# ============================================================================
# LIGHTWEIGHT PROJECT REGISTRATION (FAST PATH)
# ============================================================================

def register_project(
    api_key: str,
    client_type: str = "claude-code",
    keywords: str = "",
    description: str = ""
) -> dict:
    """
    Register current project using existing API key.

    This is the "fast path" - no browser needed, instant registration.

    Args:
        api_key: The user's Push API key
        client_type: "claude-code" or "openai-codex"
        keywords: Comma-separated keywords for AI matching (from agent)
        description: Short description of the project (from agent)

    Returns dict with:
        - status: "success", "unauthorized", or "error"
        - action_name: Name of the action (if success)
        - created: True if new, False if existing (if success)
        - message: Human-readable message
    """
    client_names = {
        "claude-code": "Claude Code",
        "openai-codex": "OpenAI Codex"
    }

    # Build request payload
    payload = {
        "client_type": client_type,
        "client_name": client_names.get(client_type, "Claude Code"),
        "device_name": get_device_name(),
        "project_path": get_project_path(),
        "git_remote": get_git_remote(),
    }

    # Add agent-generated keywords and description if provided
    if keywords:
        payload["keywords"] = keywords
    if description:
        payload["description"] = description

    req = urllib.request.Request(
        f"{API_BASE}/register-project",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {api_key}",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get("success"):
                return {
                    "status": "success",
                    "action_name": data.get("action_name", "Unknown"),
                    "created": data.get("created", True),
                    "message": data.get("message", ""),
                }
            return {"status": "error", "message": "Unknown error"}
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return {"status": "unauthorized", "message": "API key invalid or revoked"}
        try:
            body = json.loads(e.read().decode())
            return {"status": "error", "message": body.get("error_description", str(e))}
        except Exception:
            return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# FULL DEVICE AUTH FLOW (SLOW PATH)
# ============================================================================

def initiate_device_flow(client_type: str = "claude-code") -> dict:
    """Request a new device code from the server.

    Sends git_remote (if available) for git-first project identification.
    Falls back to project_path when not in a git repo.
    """
    client_names = {
        "claude-code": "Claude Code",
        "openai-codex": "OpenAI Codex"
    }
    client_name = client_names.get(client_type, "Claude Code")

    req = urllib.request.Request(
        f"{API_BASE}/device-auth/init",
        data=json.dumps({
            "client_name": client_name,
            "client_type": client_type,
            "client_version": "1.0.0",
            "device_name": get_device_name(),
            "project_path": get_project_path(),
            "git_remote": get_git_remote(),
        }).encode(),
        headers={
            "Content-Type": "application/json",
            "apikey": ANON_KEY,
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())


def poll_status(device_code: str) -> dict:
    """Poll for authorization status."""
    req = urllib.request.Request(
        f"{API_BASE}/device-auth/poll",
        data=json.dumps({"device_code": device_code}).encode(),
        headers={
            "Content-Type": "application/json",
            "apikey": ANON_KEY,
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode())
        if body.get("error") == "slow_down":
            raise SlowDownError(body.get("interval", 10))
        raise


def do_full_device_auth(client_type: str = "claude-code") -> dict:
    """
    Full device auth flow with browser sign-in.

    Returns dict with:
        - api_key: The new API key
        - email: User's email from Apple Sign-In
        - action_name: Name of the created action
    """
    client_names = {
        "claude-code": "Claude Code",
        "openai-codex": "OpenAI Codex"
    }
    client_name = client_names.get(client_type, "Claude Code")

    # Initiate device code flow
    print("  Initializing...")
    try:
        device_data = initiate_device_flow(client_type)
    except Exception as e:
        print(f"  Error: Failed to initiate connection: {e}")
        sys.exit(1)

    device_code = device_data["device_code"]
    expires_in = device_data["expires_in"]
    interval = device_data.get("interval", 5)

    # Get the web OAuth URL
    auth_url = device_data.get("verification_uri_complete",
                               f"https://pushto.do/auth/cli?code={device_code}")

    # Open browser for OAuth
    print()
    print("  Opening browser for Sign in with Apple...")
    print()

    browser_opened = webbrowser.open(auth_url)

    if browser_opened:
        print("  If the browser didn't open, visit:")
    else:
        print("  Open this URL in your browser:")
    print(f"  {auth_url}")
    print()
    print(f"  Waiting for authorization ({expires_in // 60} min timeout)...")
    print("  Press Ctrl+C to cancel")
    print()

    # Poll for authorization
    start_time = time.time()
    poll_interval = interval

    while True:
        elapsed = time.time() - start_time
        if elapsed > expires_in:
            print()
            print("  Error: Authorization timed out. Please run connect again.")
            print()
            sys.exit(1)

        try:
            result = poll_status(device_code)

            if result["status"] == "authorized":
                api_key = result.get("api_key")
                email = result.get("email", "Unknown")
                action_name = result.get("action_name", client_name)

                if api_key:
                    return {
                        "api_key": api_key,
                        "email": email,
                        "action_name": action_name,
                    }
                else:
                    print()
                    print("  Error: Authorization succeeded but no API key received.")
                    print()
                    sys.exit(1)

            elif result["status"] == "denied":
                print()
                print("  Authorization denied.")
                print()
                sys.exit(1)

            elif result["status"] == "expired":
                print()
                print("  Error: Authorization expired. Please run connect again.")
                print()
                sys.exit(1)

            # Still pending, continue polling
            remaining = expires_in - int(elapsed)
            mins, secs = divmod(remaining, 60)
            sys.stdout.write(f"\r  Waiting... ({mins}:{secs:02d} remaining)   ")
            sys.stdout.flush()

        except SlowDownError as e:
            poll_interval = e.new_interval
        except urllib.error.URLError:
            sys.stdout.write(f"\r  Network error, retrying...              ")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(f"\r  Error: {e}. Retrying...                 ")
            sys.stdout.flush()

        time.sleep(poll_interval)


# ============================================================================
# STATUS DISPLAY
# ============================================================================

def show_status():
    """Show current connection status."""
    print()
    print("  Push Connection Status")
    print("  " + "=" * 40)
    print()

    existing_key = get_existing_key()
    existing_email = get_existing_email()

    if existing_key and existing_email:
        print(f"  ✓ Connected as {existing_email}")
        print(f"  ✓ API key: {existing_key[:16]}...")
        print()
        print("  Current project:")
        git_remote = get_git_remote()
        if git_remote:
            print(f"    Git remote: {git_remote}")
        else:
            print(f"    Path: {get_project_path()}")
        print()
        print("  Run 'connect' to register this project.")
        print("  Run 'connect --reauth' to re-authenticate.")
    elif existing_key:
        print(f"  ⚠ Partial config (missing email)")
        print(f"    API key: {existing_key[:16]}...")
        print()
        print("  Run 'connect --reauth' to fix.")
    else:
        print("  ✗ Not connected")
        print()
        print("  Run 'connect' to connect your Push account.")

    print()


# ============================================================================
# INSTALLATION METHOD DETECTION
# ============================================================================

def get_installation_method() -> str:
    """
    Detect how the plugin was installed.

    Returns:
        "marketplace" - Installed via Claude Code marketplace (in ~/.claude/plugins/)
        "codex" - Installed via Codex curl installer (in ~/.codex/skills/)
        "development" - Symlinked for development (INTERNAL USE ONLY - not a user scenario)
        "legacy" - Installed via curl (files in ~/.claude/skills/, no symlink/git)

    Note: Real users install via marketplace, codex, or legacy curl. The "development"
    detection is purely for plugin maintainers who use symlinks for convenience.
    """
    plugin_dir = Path(__file__).parent.parent

    # Check if this is a marketplace installation
    # Marketplace installs are in ~/.claude/plugins/, not ~/.claude/skills/
    if ".claude/plugins" in str(plugin_dir):
        return "marketplace"

    # Check if this is a Codex installation
    # Codex installs are in ~/.codex/skills/
    if ".codex/skills" in str(plugin_dir):
        return "codex"

    # Check if it's a symlink (development setup)
    skills_path = Path.home() / ".claude" / "skills" / "push-todo"
    if skills_path.is_symlink():
        return "development"

    # Check if there's a .git directory (cloned, not curl)
    git_dir = plugin_dir / ".git"
    if git_dir.exists():
        return "development"

    # Otherwise it's a legacy curl installation
    return "legacy"


def is_marketplace_auto_update_enabled() -> Optional[bool]:
    """
    Check if auto-update is enabled for our marketplace in Claude Code.

    Reads ~/.claude/plugins/known_marketplaces.json to check the autoUpdate field.

    Returns:
        True - Auto-update is explicitly enabled
        False - Auto-update is explicitly disabled
        None - Cannot determine (file missing, marketplace not found, or field absent)

    Note: For official marketplaces, autoUpdate defaults to True.
          For third-party marketplaces, autoUpdate defaults to False.
    """
    known_marketplaces_file = Path.home() / ".claude" / "plugins" / "known_marketplaces.json"

    if not known_marketplaces_file.exists():
        return None

    try:
        with open(known_marketplaces_file) as f:
            data = json.load(f)

        # Our marketplace ID
        marketplace_id = "push-todo-cli"

        if marketplace_id not in data:
            return None

        marketplace_info = data[marketplace_id]

        # autoUpdate field may or may not be present
        if "autoUpdate" in marketplace_info:
            return marketplace_info["autoUpdate"]

        # Field not present - return None (caller decides based on defaults)
        return None

    except Exception:
        return None


def show_migration_hint():
    """Show migration hint for legacy installations."""
    method = get_installation_method()

    # Don't show migration hints for Codex users (they're already on the right install method)
    if method == "codex":
        return

    if method == "legacy":
        print()
        print("  " + "-" * 50)
        print("  TIP: You're using a legacy installation.")
        print("  For auto-updates, migrate to the marketplace:")
        print()
        print("  Step 1: Remove old installation")
        print("    rm -rf ~/.claude/skills/push-todo")
        print()
        print("  Step 2: Add marketplace")
        print("    /plugin marketplace add MasslessAI/push-todo-cli")
        print()
        print("  Step 3: Install plugin")
        print("    /plugin install push-todo@push-todo-cli")
        print()
        print("  Step 4: Enable auto-updates")
        print("    /plugin -> Marketplaces -> Enable auto-update")
        print()
        print("  Your config (~/.config/push/) will be preserved.")
        print("  " + "-" * 50)


# ============================================================================
# MAIN
# ============================================================================

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Connect to Push (Doctor Mode)")
    parser.add_argument(
        "--client",
        choices=["claude-code", "openai-codex"],
        default="claude-code",
        help="Client type (default: claude-code)"
    )
    parser.add_argument(
        "--reauth",
        action="store_true",
        help="Force re-authentication (get new API key)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current connection status without registering"
    )
    parser.add_argument(
        "--check-version",
        action="store_true",
        help="Check for plugin updates (JSON output)"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update plugin to latest version"
    )
    parser.add_argument(
        "--validate-key",
        action="store_true",
        help="Validate API key with backend (JSON output)"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default="",
        help="Comma-separated keywords for AI matching (generated by agent)"
    )
    parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Short description of the project (generated by agent)"
    )
    args = parser.parse_args()

    # Handle --check-version flag (JSON output for agent parsing)
    if args.check_version:
        result = check_version()
        print(json.dumps(result, indent=2))
        return

    # Handle --update flag
    if args.update:
        result = do_update()
        print(json.dumps(result, indent=2))
        return

    # Handle --validate-key flag (JSON output for agent parsing)
    if args.validate_key:
        existing_key = get_existing_key()
        if not existing_key:
            print(json.dumps({
                "status": "missing",
                "message": "No API key configured"
            }, indent=2))
            return
        result = validate_api_key(existing_key)
        print(json.dumps(result, indent=2))
        return

    # Handle --status flag (show status and exit)
    if args.status:
        show_status()
        return

    client_type = args.client
    client_names = {
        "claude-code": "Claude Code",
        "openai-codex": "OpenAI Codex"
    }
    client_name = client_names.get(client_type, "Claude Code")

    print()
    print(f"  Push Voice Tasks Connect")
    print("  " + "=" * 40)
    print()

    # Check for --reauth flag
    if args.reauth:
        print("  Forcing re-authentication...")
        clear_config()

    existing_key = get_existing_key()
    existing_email = get_existing_email()

    if existing_key and existing_email and not args.reauth:
        # ─────────────────────────────────────────────────────────────────
        # FAST PATH: Already authenticated, just register project
        # ─────────────────────────────────────────────────────────────────
        print(f"  Connected as {existing_email}")
        print("  Registering project...")

        result = register_project(
            existing_key,
            client_type,
            keywords=args.keywords,
            description=args.description
        )

        if result["status"] == "success":
            print()
            print("  " + "=" * 40)
            if result["created"]:
                print(f'  Created action: "{result["action_name"]}"')
            else:
                print(f'  Found existing action: "{result["action_name"]}"')
            print("  " + "=" * 40)
            print()
            if result["created"]:
                print("  Your iOS app will sync this automatically.")
            else:
                print("  This project is already configured.")

            # Show migration hint for legacy installations
            show_migration_hint()
            print()
            return

        elif result["status"] == "unauthorized":
            print()
            print("  Session expired, re-authenticating...")
            print()
            clear_config()
            # Fall through to full auth

        else:
            print()
            print(f"  Registration failed: {result.get('message', 'Unknown error')}")
            print("  Trying full connection...")
            print()
            # Fall through to full auth

    # ─────────────────────────────────────────────────────────────────────
    # SLOW PATH: First time or re-auth needed
    # ─────────────────────────────────────────────────────────────────────
    is_reauth = existing_key is not None

    result = do_full_device_auth(client_type)

    # Save credentials
    save_config(result["api_key"], result["email"])

    # Show success
    print()
    print("  " + "=" * 40)
    if is_reauth:
        print(f'  Re-connected as {result["email"]}')
    else:
        print(f'  Connected as {result["email"]}')
    print(f'  Created action: "{result["action_name"]}"')
    print("  " + "=" * 40)
    print()
    print("  Your iOS app will sync this automatically.")

    # Show migration hint for legacy installations
    show_migration_hint()
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("  Connection cancelled.")
        print()
        sys.exit(1)
