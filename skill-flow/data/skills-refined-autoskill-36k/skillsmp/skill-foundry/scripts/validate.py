#!/usr/bin/env python3
"""
Validates SKILL.md files for Agent Skills standard compliance and portability.

Usage:
    python validate.py path/to/SKILL.md
    python validate.py .claude/skills/*/SKILL.md  # Validate all skills

Exit codes:
    0 - Valid and portable
    1 - Errors found (invalid skill)
    2 - Warnings only (valid but has portability concerns)
"""

import sys
import re
import argparse
from pathlib import Path

def extract_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """Extract YAML frontmatter from markdown content."""
    # Check for frontmatter delimiters
    if not content.startswith('---'):
        return None, "File must start with '---' (YAML frontmatter delimiter)"
    
    # Find closing delimiter
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return None, "Missing closing '---' for frontmatter"
    
    yaml_content = content[4:end_match.start() + 3]
    
    # Simple YAML parsing (avoid external dependency)
    frontmatter = {}
    current_key = None
    current_value = []
    indent_level = 0
    
    for line in yaml_content.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
            
        # Check for key: value pattern
        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)$', stripped)
        if match:
            # Save previous key if exists
            if current_key:
                frontmatter[current_key] = '\n'.join(current_value).strip() if current_value else ''
            
            current_key = match.group(1)
            value = match.group(2).strip()
            
            # Handle quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            current_value = [value] if value else []
        elif current_key and line.startswith('  '):
            # Multi-line value continuation
            current_value.append(stripped)
    
    # Save last key
    if current_key:
        frontmatter[current_key] = '\n'.join(current_value).strip() if current_value else ''
    
    return frontmatter, None


def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    """
    Validate a SKILL.md file.
    
    Returns:
        (errors, warnings) - Lists of error and warning messages
    """
    errors = []
    warnings = []
    
    # Check file exists
    if not path.exists():
        return [f"File not found: {path}"], []
    
    if not path.is_file():
        return [f"Not a file: {path}"], []
    
    content = path.read_text(encoding='utf-8')
    
    # Extract frontmatter
    frontmatter, parse_error = extract_frontmatter(content)
    if parse_error:
        return [parse_error], []
    
    if not frontmatter:
        return ["No frontmatter found"], []
    
    # === Required Fields ===
    
    # name
    if 'name' not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = frontmatter['name']
        if not name:
            errors.append("Field 'name' cannot be empty")
        elif not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
            errors.append(f"Invalid name '{name}': must be lowercase letters, numbers, and hyphens; cannot start/end with hyphen")
        elif len(name) > 64:
            errors.append(f"Name too long ({len(name)} chars): maximum 64 characters")
    
    # description
    if 'description' not in frontmatter:
        errors.append("Missing required field: description")
    else:
        desc = frontmatter['description']
        if not desc:
            errors.append("Field 'description' cannot be empty")
        elif len(desc) > 1024:
            errors.append(f"Description too long ({len(desc)} chars): maximum 1024 characters")
        elif len(desc) < 20:
            warnings.append(f"Description is very short ({len(desc)} chars): consider adding more detail about when to use this skill")
    
    # === Optional Standard Fields ===
    
    # license (optional)
    if 'license' in frontmatter:
        license_val = frontmatter['license']
        if len(license_val) > 200:
            warnings.append("License field is unusually long; consider using just the license name")
    
    # requirements (optional)
    if 'requirements' in frontmatter:
        req = frontmatter['requirements']
        if len(req) > 500:
            errors.append(f"Requirements too long ({len(req)} chars): maximum 500 characters")
    
    # === Non-Portable Fields (Warnings) ===
    
    non_portable_fields = {
        'allowed-tools': 'Claude Code only - move to metadata.claude-code.allowed-tools',
        'model': 'Claude Code only - move to metadata.claude-code.model',
        'hooks': 'Claude Code only - not portable',
        'context': 'Claude Code only - not portable',
        'argument-hint': 'Slash commands only - not applicable to skills',
        'disable-model-invocation': 'Claude Code only - not applicable to portable skills',
        'agent': 'VS Code prompts only - not applicable to skills',
        'tools': 'VS Code prompts only - not applicable to skills',
    }
    
    for field, reason in non_portable_fields.items():
        if field in frontmatter:
            warnings.append(f"Non-portable field '{field}' at root level: {reason}")
    
    # === Deprecated/Invalid Fields ===
    
    # 'compatibility' is not in the spec; 'requirements' is the correct field
    if 'compatibility' in frontmatter:
        warnings.append("Field 'compatibility' is not in the Agent Skills spec; use 'requirements' instead")
    
    # === Body Analysis ===
    
    # Extract body (after frontmatter)
    body_match = re.search(r'^---\n.*?\n---\n(.*)$', content, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        
        # Check body length
        lines = body.strip().split('\n')
        if len(lines) > 500:
            warnings.append(f"SKILL.md body is {len(lines)} lines; consider moving content to references/")
        
        # Rough token estimate (words / 0.75)
        words = len(body.split())
        est_tokens = int(words / 0.75)
        if est_tokens > 5000:
            warnings.append(f"Estimated {est_tokens} tokens in body; recommended maximum is 5000")
    
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description='Validate SKILL.md files for Agent Skills standard compliance'
    )
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='SKILL.md file(s) to validate'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only output on errors/warnings'
    )
    
    args = parser.parse_args()
    
    exit_code = 0
    
    for filepath in args.files:
        errors, warnings = validate_skill(filepath)
        
        if errors:
            print(f"❌ {filepath}")
            for e in errors:
                print(f"   ERROR: {e}")
            exit_code = 1
        elif warnings:
            if args.strict:
                print(f"❌ {filepath}")
                exit_code = 1
            else:
                print(f"⚠️  {filepath}")
                if exit_code == 0:
                    exit_code = 2
            for w in warnings:
                print(f"   WARNING: {w}")
        elif not args.quiet:
            print(f"✅ {filepath}")
    
    if exit_code == 0 and not args.quiet:
        print(f"\nAll {len(args.files)} file(s) valid and portable.")
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
