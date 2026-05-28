import os
import sys
import json
import httpx
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# ============================================================================
# Configuration & Constants
# ============================================================================

ROBYNN_API_BASE_URL = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai/api/cli")
ENV_FILE_NAME = ".env"

# ============================================================================
# Robynn Client Utility
# ============================================================================

class RobynnClient:
    """Client for interacting with the Robynn platform API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ROBYNN_API_KEY")
        self.base_url = ROBYNN_API_BASE_URL
        
    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            return {"Content-Type": "application/json"}
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def validate_key(self, key: str) -> bool:
        """Validate an API key by fetching context."""
        try:
            with httpx.Client(headers={"Authorization": f"Bearer {key}"}) as client:
                response = client.get(f"{self.base_url}/context")
                return response.status_code == 200
        except Exception as e:
            print(f"Error validating key: {e}")
            return False

    def fetch_context(self) -> Optional[Dict[str, Any]]:
        """Fetch brand context from the platform."""
        if not self.api_key:
            return None
        try:
            with httpx.Client(headers=self._get_headers()) as client:
                response = client.get(f"{self.base_url}/context")
                response.raise_for_status()
                return response.json().get("data")
        except Exception as e:
            print(f"Error fetching brand context: {e}")
            return None

    def fetch_usage(self) -> Optional[Dict[str, Any]]:
        """Fetch CMO usage details."""
        if not self.api_key:
            return None
        try:
            with httpx.Client(headers=self._get_headers()) as client:
                response = client.get(f"{self.base_url}/usage")
                response.raise_for_status()
                return response.json().get("data")
        except Exception as e:
            print(f"Error fetching usage details: {e}")
            return None

# ============================================================================
# CLI Commands
# ============================================================================

def print_welcome():
    """Print the Rory welcome box."""
    welcome = """
┌─────────────────────────────────────────────┐
│                                             │
│   Hey, I'm Rory — your CMO in the terminal. │
│                                             │
│   I'm connected to your Brand Hub in        │
│   Robynn, so I already know your voice,     │
│   positioning, and competitors.             │
│                                             │
│   Try:                                      │
│   • rory research "Company Name"            │
│   • rory write linkedin-post                │
│   • rory competitors                        │
│                                             │
│   Let's make some noise.                    │
│                                             │
└─────────────────────────────────────────────┘
"""
    print(welcome)

def init_command(api_key: str):
    """Initialize the Robynn connection with an API key."""
    print(f"⠋ Rory is verifying your API key with Robynn AI...")
    client = RobynnClient(api_key)
    
    if not client.validate_key(api_key):
        print("\n❌ Invalid API key.")
        print("1. Sign up/Login at https://robynn.ai")
        print("2. Go to Settings > API Keys")
        print("3. Copy your key and try again: rory config <key>")
        sys.exit(1)
    
    # Save to .env file
    env_path = Path(ENV_FILE_NAME)
    lines = []
    key_exists = False
    
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("ROBYNN_API_KEY="):
                lines.append(f"ROBYNN_API_KEY={api_key}")
                key_exists = True
            else:
                lines.append(line)
    
    if not key_exists:
        lines.append(f"ROBYNN_API_KEY={api_key}")
    
    env_path.write_text("\n".join(lines) + "\n")
    print("\n✅ Successfully connected to Robynn AI Pro!")
    print("🚀 I now have full access to your Brand Hub context.")
    print("✨ Let's make some noise.")

def status_command(debug=False):
    """Check the connection status and brand details."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        print("\nStatus: ⚪ Not Connected (Anonymous Mode)")
        print("─" * 45)
        print("You are running in anonymous mode with generic marketing")
        print("context and limited tasks (5/day).\n")
        print("Quick setup (takes 2 minutes):")
        print("  1. Run: rory init")
        print("  2. Create your free account (20 free tasks/month)")
        print("  3. Paste your API key when prompted\n")
        print("Or if you already have a key, run:")
        print("  rory config <your_api_key>")
        print("\nGet your key at: https://robynn.ai/settings/api-keys")
        return

    print("\nStatus: 🟢 Connected (Pro Tier)")
    client = RobynnClient(api_key)
    context = client.fetch_context()
    
    if debug:
        print("\n[DEBUG] Raw API response:")
        print(json.dumps(context, indent=2, default=str))
        print()
    
    if context:
        # Extract data from the actual API structure
        org_id = context.get('organizationId', 'Unknown')
        
        # Company name can be at identity.companyName or top-level companyName
        identity = context.get('identity', {})
        company_name = identity.get('companyName') or context.get('companyName') or ''
        
        # Website might be in various places
        company_website = context.get('companyWebsite') or context.get('website') or ''
        
        # Voice is structured differently - check for voice.toneSpectrum or voice.coreAttributes
        voice = context.get('voice', {})
        voice_configured = bool(
            voice.get('coreAttributes') or 
            voice.get('toneSpectrum') or 
            context.get('voiceAndTone')
        )
        
        # Check if product knowledge exists
        product_knowledge = context.get('productKnowledge', {})
        features = product_knowledge.get('features', [])
        
        # Display results
        print(f"Organization: {org_id}")
        print(f"Company:      {company_name if company_name else 'Not Set'}")
        print(f"Website:      {company_website if company_website else 'Not Set'}")
        
        if voice_configured:
            print("Brand Voice:  ✅ Configured")
        else:
            print("Brand Voice:  ⚠️ Not configured in Brand Hub")
        
        if features:
            print(f"Features:     {len(features)} loaded")
        
        # Show helpful message if company name is not set
        if not company_name:
            print("\n💡 Tip: Add your company name in Brand Hub → Settings")
            print("   Visit: https://robynn.ai/dashboard → Brand Hub")
    else:
        print("⚠️  Connected, but I couldn't fetch your brand context. Check your settings on Robynn AI.")

def usage_command():
    """Check the current usage and limits."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        print("\nTier: ⚪ Anonymous")
        print("Limit: 5 tasks / day (Per IP)")
        print("\nSign up at https://robynn.ai to increase your limits to 20 tasks / month for free.")
        return

    client = RobynnClient(api_key)
    usage = client.fetch_usage()
    
    if usage:
        tier = usage.get("tier", "Unknown")
        remaining = usage.get("remaining", 0)
        total = usage.get("total", 0)
        reset_date = usage.get("resetDate")
        
        print(f"\nTier:      {tier}")
        print(f"Remaining: {remaining} of {total} tasks")
        if reset_date:
            print(f"Resets on: {reset_date}")
        
        if tier == "Free":
            print("\nUpgrade to Pro for 500 tasks / day and full Brand Hub access!")
    else:
        print("\n⚠️  I couldn't fetch your usage details right now. Please try again later.")

def sync_command(json_output=False):
    """Validate Brand Hub connection (no local storage needed)."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        if json_output:
            print(json.dumps({"success": False, "error": "Not connected"}))
        else:
            print("\n❌ You need to connect your Robynn account first.")
            print("Run: rory config <your_api_key>")
        return

    if not json_output:
        print("⠋ Rory is checking your Brand Hub connection...")

    client = RobynnClient(api_key)
    context = client.fetch_context()

    if context:
        company = context.get('companyName', 'Not Set')
        features = context.get('features', [])
        voice = context.get('voiceAndTone')

        if json_output:
            print(json.dumps({
                "success": True,
                "company": company,
                "features_count": len(features) if isinstance(features, list) else 0,
                "voice_configured": bool(voice)
            }))
        else:
            print(f"\n✅ Brand Hub connected")
            print(f"   Company: {company}")
            print(f"   Features: {len(features) if isinstance(features, list) else 0} loaded")
            print(f"   Voice: {'✅ Configured' if voice else '⚠️ Not configured'}")
            print(f"\n💡 Your brand context is fetched automatically on each request.")
            print(f"   No local files needed. Changes in Brand Hub reflect immediately.")
    else:
        if json_output:
            print(json.dumps({"success": False, "error": "Failed to fetch context"}))
        else:
            print("\n⚠️ Brand Hub not configured.")
            print("   Visit Settings → Brand Hub in Robynn to add your company info.")

def voice_command(json_output=False):
    """Preview brand voice settings."""
    api_key = os.environ.get("ROBYNN_API_KEY")
    if not api_key:
        if json_output:
            print(json.dumps({"success": False, "error": "Not connected"}))
        else:
            print("\nStatus: ⚪ Anonymous (Generic Voice)")
        return

    client = RobynnClient(api_key)
    context = client.fetch_context()
    
    if context and context.get('voiceAndTone'):
        if json_output:
            print(json.dumps({"success": True, "voice": context.get('voiceAndTone')}))
        else:
            print("\nVoice Settings:")
            print(f"Tone: {context.get('voiceAndTone')}")
            print("Status: ✅ Active")
    else:
        if json_output:
            print(json.dumps({"success": False, "error": "Voice settings not found"}))
        else:
            print("\nVoice settings not found in Brand Hub.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?")
    parser.add_argument("arg", nargs="?")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--debug", action="store_true", help="Show raw API responses")
    args = parser.parse_args()

    if not args.command:
        print_welcome()
        sys.exit(0)
        
    command = args.command
    json_output = args.json
    debug_mode = args.debug
    
    if command in ["init", "config"]:
        if not args.arg:
            print("Usage: rory config <key>")
            sys.exit(1)
        init_command(args.arg)
    elif command == "status":
        status_command(debug=debug_mode)
    elif command == "usage":
        usage_command()
    elif command == "sync":
        sync_command(json_output)
    elif command == "voice":
        voice_command(json_output)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
