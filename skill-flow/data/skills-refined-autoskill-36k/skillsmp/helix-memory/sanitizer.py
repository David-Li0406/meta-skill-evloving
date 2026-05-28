#!/usr/bin/env python3
"""
Sanitizer for public devlog generation.

Removes/anonymizes sensitive data:
- Production URLs → [domain]
- IP addresses → [server]
- Project names → Project A/B/C
- Credentials → stripped
"""

import re
from typing import Dict, List, Optional

# Safe domains that don't need anonymization
SAFE_DOMAINS = {
    'github.com', 'stackoverflow.com', 'npmjs.com', 'pypi.org',
    'developer.mozilla.org', 'docs.python.org', 'fastapi.tiangolo.com',
    'pico.css', 'data-star.dev', 'htmx.org', 'anthropic.com',
    'openrouter.ai', 'helix-db.com', 'docs.helix-db.com',
    'google.com', 'youtube.com', 'wikipedia.org'
}

# Patterns that indicate credentials (not the actual secrets)
CREDENTIAL_PATTERNS = [
    r'(wp-admin|admin):\s*\w+',   # WordPress admin usernames
    r'\b\w+@[\w.-]+\s*:\s*\S+',   # user@host:password format
    r'password[:\s=]+\S+',        # password mentions
    r'api[_-]?key[:\s=]+\S+',     # API keys
    r'sk-[a-zA-Z0-9]+',           # OpenAI/Anthropic style keys
    r'secret[:\s=]+\S+',          # secrets
    r'token[:\s=]+\S+',           # tokens
    r'Bearer\s+\S+',              # Bearer tokens
]


class Sanitizer:
    """Sanitizes text for public devlog."""

    def __init__(self):
        self.project_mapping: Dict[str, str] = {}
        self.project_counter = 0

    def _get_project_alias(self, project: str) -> str:
        """Get consistent alias for project name."""
        project_lower = project.lower().strip()
        if project_lower not in self.project_mapping:
            self.project_counter += 1
            self.project_mapping[project_lower] = f"Project {chr(64 + self.project_counter)}"
        return self.project_mapping[project_lower]

    def sanitize_urls(self, text: str) -> str:
        """Replace production URLs with [domain]."""
        # Pattern for full URLs
        url_pattern = r'https?://([a-zA-Z0-9][-a-zA-Z0-9]*\.)+[a-zA-Z]{2,}(?:[:/][^\s]*)?'

        def replace_url(match):
            url = match.group(0)
            domain_match = re.search(r'https?://([^/:]+)', url)
            if domain_match:
                domain = domain_match.group(1).lower()
                for safe in SAFE_DOMAINS:
                    if safe in domain:
                        return url
                if any(x in domain for x in ['localhost', '127.0.0.1', '.local', '.loc', '.test', '.dev']):
                    return '[local-dev-url]'
            return '[domain]'

        result = re.sub(url_pattern, replace_url, text)

        # Also catch bare domain names (word.tld pattern) that aren't safe
        bare_domain = r'\b([a-zA-Z0-9][-a-zA-Z0-9]*\.(?:com|org|net|io|dev|co\.[a-z]{2}|[a-z]{2,3}))\b'

        def replace_bare(match):
            domain = match.group(1).lower()
            for safe in SAFE_DOMAINS:
                if safe in domain or domain in safe:
                    return match.group(0)
            # Check if it's a dev domain
            if any(x in domain for x in ['.local', '.loc', '.test']):
                return '[local-domain]'
            return '[domain]'

        return re.sub(bare_domain, replace_bare, result)

    def sanitize_ips(self, text: str) -> str:
        """Replace IP addresses with [server]."""
        # IPv4 pattern (avoid matching version numbers like 1.0.0)
        ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

        def replace_ip(match):
            ip = match.group(0)
            # Keep localhost
            if ip.startswith('127.') or ip.startswith('0.'):
                return '[localhost]'
            # Keep private ranges but mark them
            if ip.startswith('192.168.') or ip.startswith('10.'):
                return '[local-network]'
            return '[server]'

        return re.sub(ip_pattern, replace_ip, text)

    def sanitize_credentials(self, text: str) -> str:
        """Remove credential patterns."""
        result = text
        for pattern in CREDENTIAL_PATTERNS:
            result = re.sub(pattern, '[credential-redacted]', result, flags=re.IGNORECASE)
        return result

    def sanitize_project_names(self, text: str, known_projects: Optional[List[str]] = None) -> str:
        """Replace project names with generic aliases."""
        if not known_projects:
            return text

        result = text
        # Sort by length (longest first) to avoid partial replacements
        for project in sorted(known_projects, key=len, reverse=True):
            if len(project) < 3:  # Skip very short names
                continue
            alias = self._get_project_alias(project)
            # Case insensitive replacement
            pattern = re.compile(re.escape(project), re.IGNORECASE)
            result = pattern.sub(alias, result)

        return result

    def sanitize_paths(self, text: str) -> str:
        """Sanitize file paths that might reveal project structure."""
        # Replace home directory
        home_pattern = r'/Users/[^/\s]+/'
        text = re.sub(home_pattern, '~/', text)

        # Replace wp-content paths with project info
        wp_pattern = r'/wp-content/(?:plugins|themes)/([^/\s]+)'
        def replace_wp(match):
            plugin_name = match.group(1)
            alias = self._get_project_alias(plugin_name)
            return f'/wp-content/plugins/{alias.lower().replace(" ", "-")}'
        text = re.sub(wp_pattern, replace_wp, text)

        return text

    def sanitize_hosting_details(self, text: str) -> str:
        """Generalize hosting provider mentions with project context."""
        hosting_patterns = [
            (r'DigitalOcean\s+VPS\s*\([^)]+\)', 'cloud VPS'),
            (r'AWS\s+\w+\s*\([^)]+\)', 'cloud infrastructure'),
            (r'Cloudways\s*\([^)]+\)', 'managed hosting'),
            (r'Cloudflare\s+\w+\s*\([^)]+\)', 'CDN/proxy'),
        ]
        result = text
        for pattern, replacement in hosting_patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    def sanitize(self, text: str, known_projects: Optional[List[str]] = None) -> str:
        """Full sanitization pipeline."""
        if not text:
            return text

        result = text
        result = self.sanitize_credentials(result)
        result = self.sanitize_urls(result)
        result = self.sanitize_ips(result)
        result = self.sanitize_paths(result)
        result = self.sanitize_hosting_details(result)
        if known_projects:
            result = self.sanitize_project_names(result, known_projects)

        return result


def sanitize_memory(memory: dict, sanitizer: Sanitizer, known_projects: Optional[List[str]] = None) -> dict:
    """Sanitize a single memory dict."""
    result = memory.copy()

    # Sanitize content
    if 'content' in result:
        result['content'] = sanitizer.sanitize(result['content'], known_projects)

    # Anonymize tags (project names)
    if 'tags' in result and result['tags']:
        new_tags = []
        for tag in result['tags'].split(','):
            tag = tag.strip()
            if tag and known_projects and tag.lower() in [p.lower() for p in known_projects]:
                new_tags.append(sanitizer._get_project_alias(tag))
            elif tag:
                new_tags.append(tag)
        result['tags'] = ', '.join(new_tags)

    return result


# CLI for testing
if __name__ == "__main__":
    import sys

    test_texts = [
        "Deployed to https://matchify-app.com on server 164.90.180.88",
        "Fixed bug in zbm.co.il WordPress plugin",
        "wp-admin: john_admin password: secret123",
        "API key: sk-abc123xyz, Bearer token123",
        "Working on /Users/username/Sites/my-project/wp-content/plugins/my-plugin",
        "DigitalOcean VPS (Project X) with Cloudflare proxy",
        "Check https://github.com/user/repo for docs",  # Should stay
    ]

    sanitizer = Sanitizer()
    known = ['matchify', 'zbm', 'level2-academy', 'my-plugin']

    print("=== Sanitizer Test ===\n")
    for text in test_texts:
        sanitized = sanitizer.sanitize(text, known)
        print(f"IN:  {text}")
        print(f"OUT: {sanitized}")
        print()
