#!/usr/bin/env python3
"""
Authentication manager for Gemini Image Generator
Handles Google account authentication with persistent browser profiles
Based on NotebookLM skill patterns with improvements

Usage:
    python scripts/run.py auth_manager.py setup    # Initial authentication
    python scripts/run.py auth_manager.py status   # Check authentication status
    python scripts/run.py auth_manager.py clear    # Clear authentication
"""

import sys
import json
import argparse
import re
import time
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DATA_DIR,
    BROWSER_PROFILE_DIR,
    STATE_FILE,
    AUTH_INFO_FILE,
    AUTH_TIMEOUT
)
from browser_utils import BrowserFactory


def ensure_data_dir():
    """Create data directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def check_status():
    """
    Check if authenticated and show status.

    Primary check is STATE_FILE (state.json) with actual cookies.
    AUTH_INFO_FILE is secondary metadata only.
    """
    # Primary check: state.json must exist with cookies
    if not STATE_FILE.exists():
        print("❌ Not authenticated")
        print("   Run: python scripts/run.py auth_manager.py setup")
        return False

    authenticated = False
    info = {}

    # Check state file for valid cookies
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)

        if 'cookies' not in state or len(state['cookies']) == 0:
            print("❌ Not authenticated (no cookies in state file)")
            print("   Run: python scripts/run.py auth_manager.py setup")
            return False

        # Check for Google auth cookies specifically
        google_auth_cookie_names = [
            'SID', 'HSID', 'SSID', 'APISID', 'SAPISID',
            '__Secure-1PSID', '__Secure-3PSID',
            '__Secure-1PAPISID', '__Secure-3PAPISID'
        ]
        google_auth_cookies = [c for c in state['cookies']
                               if c['name'] in google_auth_cookie_names]

        if len(google_auth_cookies) < 3:
            print("⚠️  Missing Google auth cookies!")
            print(f"   Found only {len(google_auth_cookies)} auth cookies (need at least 3)")
            print("   You may need to re-authenticate:")
            print("   Run: python scripts/run.py auth_manager.py setup")
            return False

        authenticated = True
        info['cookie_count'] = len(state['cookies'])
        info['auth_cookie_count'] = len(google_auth_cookies)

        age_hours = (time.time() - STATE_FILE.stat().st_mtime) / 3600
        info['state_age_hours'] = age_hours

        if age_hours > 168:  # 7 days
            print(f"⚠️  Browser state is {age_hours/24:.1f} days old")
            print("   You may need to re-authenticate soon")

    except Exception as e:
        print(f"❌ Error reading state file: {e}")
        print("   Run: python scripts/run.py auth_manager.py setup")
        return False

    # Check auth info file (secondary metadata)
    if AUTH_INFO_FILE.exists():
        try:
            with open(AUTH_INFO_FILE, 'r') as f:
                saved_info = json.load(f)
                info.update(saved_info)
        except:
            pass

    if authenticated:
        print("✓ Authenticated")
        if 'email' in info:
            print(f"  User: {info['email']}")
        if 'auth_date' in info:
            print(f"  Date: {info['auth_date']}")
        if 'state_age_hours' in info:
            print(f"  Session age: {info['state_age_hours']:.1f} hours")
        if 'cookie_count' in info:
            print(f"  Total cookies: {info['cookie_count']}")
        if 'auth_cookie_count' in info:
            print(f"  Google auth cookies: {info['auth_cookie_count']}")
        return True
    else:
        print("❌ Not authenticated")
        print("   Run: python scripts/run.py auth_manager.py setup")
        return False


def setup_auth(timeout_minutes: int = 10):
    """
    Perform interactive authentication setup.

    This uses a persistent browser context which:
    - Maintains profile between sessions
    - Automatically saves cookies and localStorage
    - Waits for URL change instead of user input

    Args:
        timeout_minutes: Maximum time to wait for login (default: 10)

    Returns:
        bool: True if authentication successful
    """
    ensure_data_dir()

    print("🔐 Starting authentication setup...")
    print(f"   Timeout: {timeout_minutes} minutes")
    print()

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()

        # Launch persistent context (key improvement!)
        print("🌐 Opening browser...")
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=False  # Must be visible for manual login
        )

        # Navigate to Google accounts first to ensure proper login flow
        print("   → Navigating to Google accounts...")
        page = context.pages[0] if context.pages else context.new_page()

        # First, go to accounts.google.com to trigger full login
        page.goto("https://accounts.google.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # Check if already logged in to Google
        current_google_url = page.url
        if "myaccount.google.com" in current_google_url or "accounts.google.com/SignOutOptions" in current_google_url:
            # Already logged in, get cookies from Google domain
            print("   → Already logged into Google")
        else:
            # Need to login at accounts.google.com first
            print()
            print("  👤 Please log in to your Google account...")
            print(f"  ⏱️  Waiting up to {timeout_minutes} minutes for Google login...")
            print()

            # Wait for redirect to myaccount.google.com (indicates successful login)
            try:
                timeout_ms = int(timeout_minutes * 60 * 1000)
                page.wait_for_url(
                    re.compile(r"^https://myaccount\.google\.com/"),
                    timeout=timeout_ms
                )
                print("  ✅ Google login successful!")
                page.wait_for_timeout(2000)  # Let cookies settle
            except Exception as e:
                print(f"  ⏱️  Timeout waiting for Google login")
                context.close()
                playwright.stop()
                return False

        # Now navigate to Gemini
        print("   → Navigating to Gemini...")
        page.goto("https://gemini.google.com/", wait_until="domcontentloaded")

        # Check if already authenticated
        current_url = page.url
        if "gemini.google.com" in current_url and "accounts.google.com" not in current_url:
            # Wait for page to fully load
            try:
                page.wait_for_load_state("networkidle", timeout=60000)
            except:
                pass
            page.wait_for_timeout(3000)

            # Check if we have Google auth cookies (not just analytics)
            # Google auth cookies include: SID, HSID, SSID, __Secure-1PSID, etc.
            cookies = context.cookies()
            google_auth_cookies = [c for c in cookies if c['name'] in [
                'SID', 'HSID', 'SSID', 'APISID', 'SAPISID',
                '__Secure-1PSID', '__Secure-3PSID',
                '__Secure-1PAPISID', '__Secure-3PAPISID'
            ]]

            if len(google_auth_cookies) >= 3:
                # We have proper Google auth cookies
                print()
                print("  ✅ Already authenticated with Google!")
                print(f"     Found {len(google_auth_cookies)} auth cookies")
                _save_auth_state(context, page)
                context.close()
                playwright.stop()
                return True
            else:
                # Page loads but no auth cookies - need manual login
                print()
                print("  ⚠️  Page accessible but missing Google auth cookies")
                print("     This may be using system Chrome login, not persistent profile")
                print("     Please log in manually to establish persistent session...")
                print()

        # Wait for manual login
        print()
        print("  👤 Please log in to your Google account in the browser...")
        print(f"  ⏱️  Waiting up to {timeout_minutes} minutes for login...")
        print()

        try:
            # Wait for URL to change to Gemini (automatic detection!)
            # This is the key improvement - no input() needed
            timeout_ms = int(timeout_minutes * 60 * 1000)
            page.wait_for_url(
                re.compile(r"^https://gemini\.google\.com/(?!accounts)"),
                timeout=timeout_ms
            )

            print("  ✅ Login successful!")
            print()

            # Wait for page to fully load and cookies to be set
            try:
                page.wait_for_load_state("networkidle", timeout=60000)
            except:
                pass  # Timeout is OK, page may have continuous network activity
            page.wait_for_timeout(3000)  # Extra wait for cookies

            # Verify we got Google auth cookies
            cookies = context.cookies()
            google_auth_cookies = [c for c in cookies if c['name'] in [
                'SID', 'HSID', 'SSID', 'APISID', 'SAPISID',
                '__Secure-1PSID', '__Secure-3PSID',
                '__Secure-1PAPISID', '__Secure-3PAPISID'
            ]]
            print(f"     Found {len(google_auth_cookies)} Google auth cookies")
            print(f"     Total cookies: {len(cookies)}")

            # Save authentication state
            _save_auth_state(context, page)

            context.close()
            playwright.stop()
            return True

        except Exception as timeout_error:
            print()
            print(f"  ⏱️  Timeout after {timeout_minutes} minutes")
            print("  ❌ Login not completed in time")
            print()
            print("  Please try again and complete login faster,")
            print("  or increase timeout with: --timeout 15")

            if context:
                context.close()
            if playwright:
                playwright.stop()
            return False

    except KeyboardInterrupt:
        print()
        print("  ⚠️  Authentication cancelled by user")
        if context:
            context.close()
        if playwright:
            playwright.stop()
        return False

    except Exception as e:
        print()
        print(f"  ❌ Authentication failed: {e}")
        print()
        print("  Troubleshooting:")
        print("  - Check your internet connection")
        print("  - Try clearing data: python scripts/run.py auth_manager.py clear")
        print("  - Try again with visible browser to see what's happening")

        if context:
            context.close()
        if playwright:
            playwright.stop()
        return False


def _save_auth_state(context, page):
    """Save authentication state and info."""
    try:
        # Save browser state (cookies, localStorage, etc.)
        context.storage_state(path=str(STATE_FILE))
        print("  → Session saved")

        # Try to extract user email (best effort)
        user_email = "Unknown"
        try:
            # Look for user profile button or email display
            # This selector may vary, just best effort
            email_selectors = [
                '[data-identifier-type="EMAIL"]',
                'div[aria-label*="Account"]',
                'button[aria-label*="Google Account"]'
            ]

            for selector in email_selectors:
                if page.locator(selector).count() > 0:
                    text = page.locator(selector).first.text_content()
                    if '@' in text:
                        user_email = text
                        break
        except:
            pass

        # Save auth info
        auth_data = {
            "authenticated": True,
            "email": user_email,
            "auth_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "profile_dir": str(BROWSER_PROFILE_DIR)
        }

        with open(AUTH_INFO_FILE, 'w') as f:
            json.dump(auth_data, f, indent=2)

        print("  → Authentication info saved")

    except Exception as e:
        print(f"  ⚠️  Could not save state: {e}")


def clear_auth():
    """Clear all authentication data."""
    try:
        removed_items = []

        if AUTH_INFO_FILE.exists():
            AUTH_INFO_FILE.unlink()
            removed_items.append("auth_info.json")

        if STATE_FILE.exists():
            STATE_FILE.unlink()
            removed_items.append("state.json")

        if BROWSER_PROFILE_DIR.exists():
            import shutil
            shutil.rmtree(BROWSER_PROFILE_DIR)
            BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
            removed_items.append("browser profile")

        if removed_items:
            print("✓ Cleared:")
            for item in removed_items:
                print(f"  - {item}")
        else:
            print("  No authentication data found")

        return True

    except Exception as e:
        print(f"❌ Error clearing auth: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Manage Gemini authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run.py auth_manager.py setup              # Authenticate
  python scripts/run.py auth_manager.py setup --timeout 15 # With longer timeout
  python scripts/run.py auth_manager.py status             # Check status
  python scripts/run.py auth_manager.py clear              # Clear and logout
        """
    )

    parser.add_argument(
        "action",
        choices=["setup", "status", "clear"],
        help="Action to perform"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in minutes for authentication (default: 10)"
    )

    args = parser.parse_args()

    if args.action == "setup":
        success = setup_auth(timeout_minutes=args.timeout)
        return 0 if success else 1

    elif args.action == "status":
        success = check_status()
        return 0 if success else 1

    elif args.action == "clear":
        success = clear_auth()
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
