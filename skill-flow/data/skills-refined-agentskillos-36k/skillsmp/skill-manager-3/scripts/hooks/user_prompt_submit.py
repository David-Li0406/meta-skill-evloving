#!/usr/bin/env python3
"""
user_prompt_submit.py - Analyzes user prompts for domain markers.
Runs when user submits a prompt.

Also backs up Claude credentials on each prompt to ensure they persist.

Hook type: UserPromptSubmit
"""

import json
import sys
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# Determine skills directory based on environment
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))


def backup_credentials():
    """Backup Claude credentials and config to bind-mounted folders.

    Primary backup: ~/projects/ (direct bind mount, most reliable)
    Legacy backup: ~/.claude/skills/.skill-system/ (nested mount, kept for compatibility)
    """
    try:
        creds_file = Path.home() / ".claude" / ".credentials.json"
        config_file = Path.home() / ".claude.json"
        # PRIMARY: Direct bind mount (./home/) - most reliable
        creds_backup = Path.home() / "projects" / ".claude-credentials-backup.json"
        config_backup = Path.home() / "projects" / ".claude-config-backup.json"
        # LEGACY: Nested bind mount (./skills/) - kept for compatibility
        legacy_backup = SKILLS_DIR / ".skill-system" / ".credentials-backup.json"

        # Backup credentials
        if creds_file.exists() and creds_file.stat().st_size > 0:
            # Primary backup first
            if creds_backup.parent.exists():
                shutil.copy2(creds_file, creds_backup)
                creds_backup.chmod(0o600)

            # Legacy backup for compatibility
            legacy_backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(creds_file, legacy_backup)
            legacy_backup.chmod(0o600)

        # Backup .claude.json (user settings, workspace trust)
        if config_file.exists() and config_file.stat().st_size > 0:
            if config_backup.parent.exists():
                shutil.copy2(config_file, config_backup)
                config_backup.chmod(0o600)
    except Exception:
        pass  # Fail silently - don't interrupt the hook


PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
DOMAIN_FILE = PATTERNS_DIR / "prompt-patterns.jsonl"
CONFIG_FILE = SKILLS_DIR / ".skill-system" / "config.json"

# Default domain markers (loaded from config if available)
DEFAULT_DOMAIN_MARKERS = {
    "devops": r"\b(docker|kubernetes|k8s|deploy|ci\/cd|pipeline|terraform|ansible|helm|jenkins|container|pod|service)\b",
    "security": r"\b(vulnerability|cve|audit|pentest|owasp|encryption|auth|token|ssl|tls|certificate|secret|credential)\b",
    "data_science": r"\b(pandas|numpy|model|train|dataset|jupyter|sklearn|tensorflow|pytorch|ml|machine learning|dataframe)\b",
    "frontend": r"\b(react|vue|angular|css|component|webpack|vite|tailwind|nextjs|svelte|dom|browser|html)\b",
    "backend": r"\b(api|rest|graphql|database|sql|orm|endpoint|middleware|express|fastapi|django|flask|server)\b",
    "git": r"\b(merge|rebase|branch|pr|pull request|commit|cherry-pick|stash|checkout|fetch|push|clone|diff)\b",
}


def load_domain_markers():
    """Load domain markers from config, fall back to defaults."""
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            markers = config.get("domains", {}).get("markers", {})
            if markers:
                # Convert list format to regex pattern
                result = {}
                for domain, keywords in markers.items():
                    if isinstance(keywords, list):
                        pattern = r"\b(" + "|".join(re.escape(k) for k in keywords) + r")\b"
                        result[domain] = pattern
                    else:
                        result[domain] = keywords
                return result
    except Exception:
        pass
    return DEFAULT_DOMAIN_MARKERS


def get_session_id():
    """Get or generate a session ID."""
    session_id = os.environ.get('CLAUDE_SESSION_ID')
    if not session_id:
        session_id = datetime.utcnow().strftime("%Y%m%d-%H")
    return session_id


def extract_intent_signals(prompt):
    """Extract intent signals from the prompt."""
    signals = []

    # Action verbs indicating implementation
    if re.search(r"\b(create|implement|build|add|make|write|develop)\b", prompt, re.I):
        signals.append("implement")

    # Action verbs indicating fixing
    if re.search(r"\b(fix|debug|solve|repair|resolve|troubleshoot)\b", prompt, re.I):
        signals.append("fix")

    # Action verbs indicating exploration
    if re.search(r"\b(find|search|look|explore|understand|explain|how)\b", prompt, re.I):
        signals.append("explore")

    # Action verbs indicating refactoring
    if re.search(r"\b(refactor|clean|optimize|improve|restructure)\b", prompt, re.I):
        signals.append("refactor")

    # Action verbs indicating testing
    if re.search(r"\b(test|verify|check|validate|assert)\b", prompt, re.I):
        signals.append("test")

    # Action verbs indicating deployment
    if re.search(r"\b(deploy|release|ship|publish|push to)\b", prompt, re.I):
        signals.append("deploy")

    return signals


def main():
    # Backup credentials on every prompt (ensures OAuth persists immediately)
    backup_credentials()

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)

    prompt = input_data.get("prompt", "")
    if not prompt:
        sys.exit(0)

    prompt_lower = prompt.lower()
    domain_markers = load_domain_markers()

    # Detect domains
    detected_domains = []
    domain_matches = {}

    for domain, pattern in domain_markers.items():
        matches = re.findall(pattern, prompt_lower, re.IGNORECASE)
        if matches:
            detected_domains.append(domain)
            domain_matches[domain] = len(matches)

    # Extract intent signals
    intent_signals = extract_intent_signals(prompt_lower)

    # Only record if we detected something interesting
    if detected_domains or intent_signals:
        record = {
            "session_id": get_session_id(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "domains": detected_domains,
            "domain_strength": domain_matches,
            "intent_signals": intent_signals,
            "prompt_length": len(prompt),
            "prompt_words": len(prompt.split()),
        }

        try:
            PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
            with open(DOMAIN_FILE, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

    sys.exit(0)


if __name__ == "__main__":
    main()
