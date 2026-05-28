#!/usr/bin/env python3
"""
MyAgentive Configuration Validator

Validates the MyAgentive configuration file and reports issues.

Usage:
    python check_config.py
    python check_config.py --verbose
"""

import os
import sys
from pathlib import Path

# Configuration
CONFIG_PATH = Path.home() / ".myagentive" / "config"
DATA_PATH = Path.home() / ".myagentive" / "data"
MEDIA_PATH = Path.home() / ".myagentive" / "media"

REQUIRED_KEYS = [
    ("TELEGRAM_BOT_TOKEN", "Telegram bot authentication"),
    ("TELEGRAM_USER_ID", "Your Telegram user ID"),
    ("WEB_PASSWORD", "Web interface password"),
    ("API_KEY", "REST API authentication key"),
]

OPTIONAL_API_KEYS = [
    ("DEEPGRAM_API_KEY", "Audio/video transcription", "https://deepgram.com", "$200 free credit"),
    ("GEMINI_API_KEY", "Image generation", "https://ai.google.dev", "Limited free tier"),
    ("ELEVENLABS_API_KEY", "Voice synthesis", "https://elevenlabs.io", "10k chars/month free"),
    ("ANTHROPIC_API_KEY", "Anthropic API (optional)", "https://console.anthropic.com", "Pay-per-use"),
    ("OPENAI_API_KEY", "OpenAI API (optional)", "https://platform.openai.com", "Pay-per-use"),
]

SOCIAL_MEDIA_KEYS = [
    ("LINKEDIN_CLIENT_ID", "LinkedIn API"),
    ("LINKEDIN_CLIENT_SECRET", "LinkedIn API"),
    ("LINKEDIN_ACCESS_TOKEN", "LinkedIn API"),
    ("TWITTER_API_KEY", "Twitter/X API"),
    ("TWITTER_API_SECRET", "Twitter/X API"),
    ("TWITTER_ACCESS_TOKEN", "Twitter/X API"),
    ("TWITTER_ACCESS_TOKEN_SECRET", "Twitter/X API"),
    ("TWITTER_BEARER_TOKEN", "Twitter/X API"),
]


def load_config():
    """Load configuration file as dictionary."""
    if not CONFIG_PATH.exists():
        return None

    config = {}
    with open(CONFIG_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def check_required(config, verbose=False):
    """Check required configuration keys."""
    issues = []

    for key, description in REQUIRED_KEYS:
        value = config.get(key, '')
        if not value:
            issues.append(f"Missing: {key} ({description})")
        elif verbose:
            # Mask sensitive values
            masked = value[:4] + '...' + value[-4:] if len(value) > 10 else '***'
            print(f"  [OK] {key}: {masked}")

    return issues


def validate_telegram_token(config):
    """Validate Telegram bot token format."""
    token = config.get('TELEGRAM_BOT_TOKEN', '')
    if token and ':' not in token:
        return "TELEGRAM_BOT_TOKEN appears invalid (should contain ':')"
    return None


def validate_telegram_user_id(config):
    """Validate Telegram user ID is numeric."""
    user_id = config.get('TELEGRAM_USER_ID', '')
    if user_id:
        try:
            int(user_id)
        except ValueError:
            return "TELEGRAM_USER_ID must be numeric (not @username)"
    return None


def check_optional_keys(config, verbose=False):
    """Check optional API keys."""
    configured = []
    missing = []

    for item in OPTIONAL_API_KEYS:
        key, description, url, free_tier = item
        if config.get(key):
            configured.append(key)
            if verbose:
                print(f"  [OK] {key}")
        else:
            missing.append((key, description, url, free_tier))

    return configured, missing


def check_social_media(config, verbose=False):
    """Check social media API keys."""
    linkedin_keys = [k for k, _ in SOCIAL_MEDIA_KEYS if 'LINKEDIN' in k]
    twitter_keys = [k for k, _ in SOCIAL_MEDIA_KEYS if 'TWITTER' in k]

    linkedin_configured = all(config.get(k) for k in linkedin_keys)
    twitter_configured = all(config.get(k) for k in twitter_keys)

    return linkedin_configured, twitter_configured


def check_directories():
    """Check required directories exist."""
    issues = []

    if not DATA_PATH.exists():
        issues.append(f"Data directory missing: {DATA_PATH}")

    if not MEDIA_PATH.exists():
        issues.append(f"Media directory missing: {MEDIA_PATH}")
    else:
        # Check subdirectories
        for subdir in ['audio', 'voice', 'videos', 'photos', 'documents']:
            path = MEDIA_PATH / subdir
            if not path.exists():
                issues.append(f"Media subdirectory missing: {path}")

    return issues


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("=" * 60)
    print("MyAgentive Configuration Validator")
    print("=" * 60)
    print()

    # Check config file exists
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Configuration file not found: {CONFIG_PATH}")
        print()
        print("To create configuration, run MyAgentive:")
        print("  bun run dev")
        print("  # or")
        print("  myagentive")
        print()
        print("The setup wizard will guide you through configuration.")
        sys.exit(1)

    print(f"[OK] Config file found: {CONFIG_PATH}")
    print()

    # Load config
    config = load_config()
    if config is None:
        print("[ERROR] Failed to load configuration")
        sys.exit(1)

    # Check required keys
    print("Required Configuration:")
    print("-" * 40)
    issues = check_required(config, verbose)

    if issues:
        for issue in issues:
            print(f"  [MISSING] {issue}")
    elif not verbose:
        print("  All required keys present")
    print()

    # Validate formats
    print("Validation:")
    print("-" * 40)

    token_issue = validate_telegram_token(config)
    if token_issue:
        print(f"  [WARNING] {token_issue}")
        issues.append(token_issue)
    else:
        print("  [OK] Telegram bot token format valid")

    user_id_issue = validate_telegram_user_id(config)
    if user_id_issue:
        print(f"  [WARNING] {user_id_issue}")
        issues.append(user_id_issue)
    else:
        print("  [OK] Telegram user ID format valid")
    print()

    # Check optional API keys
    print("Optional API Keys:")
    print("-" * 40)
    configured, missing = check_optional_keys(config, verbose)

    if configured:
        print(f"  Configured: {', '.join(configured)}")
    else:
        print("  No optional API keys configured")

    if missing and verbose:
        print()
        print("  Available integrations:")
        for key, desc, url, free_tier in missing:
            print(f"    - {desc}: {url} ({free_tier})")
    print()

    # Check social media
    print("Social Media Integration:")
    print("-" * 40)
    linkedin, twitter = check_social_media(config, verbose)
    print(f"  LinkedIn: {'Configured' if linkedin else 'Not configured'}")
    print(f"  Twitter/X: {'Configured' if twitter else 'Not configured'}")
    print()

    # Check directories
    print("Directories:")
    print("-" * 40)
    dir_issues = check_directories()

    if dir_issues:
        for issue in dir_issues:
            print(f"  [WARNING] {issue}")
    else:
        print("  [OK] All directories present")
    print()

    # Summary
    print("=" * 60)
    all_issues = issues + dir_issues
    if all_issues:
        print(f"Status: {len(all_issues)} issue(s) found")
        print()
        print("To fix issues:")
        print("  1. Edit config: nano ~/.myagentive/config")
        print("  2. Or reset: rm ~/.myagentive/config && bun run dev")
        sys.exit(1)
    else:
        print("Status: Configuration valid")
        if missing:
            print()
            print(f"Tip: {len(missing)} optional integrations available.")
            print("Run with --verbose to see details.")
    print("=" * 60)


if __name__ == "__main__":
    main()
