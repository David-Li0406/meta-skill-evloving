import os
import shutil
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any

# Handle imports for both direct execution and package imports
try:
    from tools.robynn import RobynnClient
    from tools.base import extract_domain
except ImportError:
    from robynn import RobynnClient
    from base import extract_domain

ENV_FILE_NAME = ".env"

def display_welcome_message():
    """Display a friendly welcome message for the onboarding process."""
    welcome = """
┌─────────────────────────────────────────────┐
│                                             │
│   Welcome to Rory! Let's get you set up.    │
│                                             │
│   I'm your AI-powered CMO in the terminal.  │
│   To work my magic, I need to connect to    │
│   your Robynn Brand Hub.                    │
│                                             │
└─────────────────────────────────────────────┘
"""
    print(welcome)

def open_signup_in_browser(domain: Optional[str] = None):
    """Open the Robynn signup page in the default browser."""
    url = "https://robynn.ai/signup?ref=cli"
    if domain:
        # Extract domain if a full URL was provided
        clean_domain = extract_domain(domain)
        url += f"&domain={clean_domain}"
    
    print(f"→ Opening your browser to: {url}")
    webbrowser.open(url)

def prompt_for_api_key() -> Optional[str]:
    """Prompt the user to paste their API key."""
    print("\nOnce you've signed up and generated a key in Settings > API Keys,")
    print("paste it below to connect your account.")
    
    try:
        api_key = input("\nAPI Key: ").strip()
        if not api_key:
            return None
        return api_key
    except KeyboardInterrupt:
        print("\n\nOnboarding cancelled.")
        return None

def verify_connection(api_key: str) -> bool:
    """Verify the API key and fetch initial context."""
    client = RobynnClient(api_key)
    print(f"⠋ Rory is verifying your API key with Robynn AI...")
    if client.validate_key(api_key):
        return True
    return False

def save_api_key_to_env(api_key: str) -> bool:
    """Save the API key to the .env file, creating it if necessary."""
    env_path = Path(ENV_FILE_NAME)
    lines = []
    key_exists = False
    
    # Read existing lines if file exists
    if env_path.exists():
        try:
            content = env_path.read_text()
            for line in content.splitlines():
                if line.startswith("ROBYNN_API_KEY="):
                    lines.append(f"ROBYNN_API_KEY={api_key}")
                    key_exists = True
                else:
                    lines.append(line)
        except Exception as e:
            print(f"Warning: Could not read existing .env file: {e}")
    
    # Add key if it wasn't there
    if not key_exists:
        lines.append(f"ROBYNN_API_KEY={api_key}")
    
    # Write back to .env
    try:
        env_path.write_text("\n".join(lines) + "\n")
        # Ensure the env var is updated in the current process too
        os.environ["ROBYNN_API_KEY"] = api_key
        return True
    except Exception as e:
        print(f"Error: Could not save to .env file: {e}")
        return False

def interactive_init(domain_or_key: Optional[str] = None) -> bool:
    """
    Run the onboarding wizard.
    
    If domain_or_key looks like an API key (starts with 'rb_'), it's used directly.
    Otherwise, it's treated as a domain for the signup URL.
    """
    import sys
    
    # Check if we're in a non-interactive environment (no tty)
    is_interactive = sys.stdin.isatty() if hasattr(sys.stdin, 'isatty') else False
    
    # Check if the argument is an API key (starts with rb_ or is long alphanumeric)
    api_key = None
    domain = None
    
    if domain_or_key:
        # If it looks like an API key, use it directly
        if domain_or_key.startswith('rb_') or (len(domain_or_key) > 30 and domain_or_key.isalnum()):
            api_key = domain_or_key
        else:
            domain = domain_or_key
    
    # If API key was provided as argument, skip interactive flow
    if api_key:
        print("⠋ Rory is verifying your API key...")
        if verify_connection(api_key):
            if save_api_key_to_env(api_key):
                print("\n✅ Successfully connected to Robynn AI!")
                print("🚀 I now have full access to your Brand Hub context.")
                print("\nTry: rory status")
                return True
        else:
            print("\n❌ Invalid API key.")
            print("Get your key at: https://robynn.ai/settings/api-keys")
            return False
    
    # Non-interactive mode: just open browser and show instructions
    if not is_interactive:
        display_welcome_message()
        print("To complete setup, you have two options:\n")
        print("Option 1: Manual Configuration (Quick)")
        print("If you have your Robynn API key, create the .env file directly:")
        print('echo "ROBYNN_API_KEY=your-api-key-here" > ~/.claude/skills/rory/.env')
        print("\nThen verify with:")
        print("rory status\n")
        print("Option 2: Get an API Key")
        print("1. Go to https://robynn.ai/signup?ref=cli")
        print("2. Sign up or log in")
        print("3. Navigate to Settings → API Keys")
        print("4. Generate a new key")
        print("5. Run the command above with your key")
        print("\n---")
        print("Do you have a Robynn API key I can configure for you? Just paste it here and I'll set everything up.")
        return False
    
    # Interactive mode: full wizard
    display_welcome_message()
    
    # Check if they already have a key
    has_key = input("Do you already have a Robynn API key? [y/N]: ").lower().strip()
    
    if has_key != 'y':
        open_signup_in_browser(domain)
        print("\nWaiting for you to sign up...")
    
    api_key = prompt_for_api_key()
    if not api_key:
        return False
    
    if verify_connection(api_key):
        if save_api_key_to_env(api_key):
            print("\n✅ Successfully connected to Robynn AI!")
            print("🚀 I now have full access to your Brand Hub context.")
            print("\nTry some commands to get started:")
            print("• rory status")
            print("• rory research \"your domain\"")
            print("• rory write linkedin-post")
            print("\nLet's make some noise.")
            return True
    else:
        print("\n❌ Invalid API key. Please check your key at https://robynn.ai/settings/api-keys and try again.")
        print("Tip: Run 'rory init' to try the setup wizard again.")
        return False
    
    return False

def logout() -> bool:
    """Remove the API key from the .env file."""
    env_path = Path(ENV_FILE_NAME)
    if not env_path.exists():
        print("You are not currently logged in.")
        return False
    
    lines = []
    found = False
    
    try:
        content = env_path.read_text()
        for line in content.splitlines():
            if line.startswith("ROBYNN_API_KEY="):
                found = True
                continue
            lines.append(line)
        
        if found:
            env_path.write_text("\n".join(lines) + "\n")
            # Remove from current environment too
            if "ROBYNN_API_KEY" in os.environ:
                del os.environ["ROBYNN_API_KEY"]
            print("✅ Successfully logged out. API key removed.")
            return True
        else:
            print("No API key found in your .env file.")
            return False
            
    except Exception as e:
        print(f"Error during logout: {e}")
        return False

def uninstall(plugin_dir: Optional[str] = None) -> bool:
    """Uninstall Rory by removing the plugin directory."""
    target_dir = Path(plugin_dir) if plugin_dir else Path(__file__).resolve().parent.parent

    if not target_dir.exists():
        print("Rory does not appear to be installed here.")
        return False

    if not (target_dir / "rory.py").exists() or not (target_dir / "tools").is_dir():
        print("Safety check failed: target directory does not look like Rory.")
        return False

    confirmation = input(
        f"This will remove Rory from {target_dir}. Continue? [y/N]: "
    ).strip().lower()
    if confirmation != "y":
        print("Uninstall cancelled.")
        return False

    try:
        os.chdir(Path.home())
        shutil.rmtree(target_dir)
        print("✅ Rory uninstalled. You can reinstall anytime via install.sh.")
        return True
    except Exception as e:
        print(f"Error during uninstall: {e}")
        return False
