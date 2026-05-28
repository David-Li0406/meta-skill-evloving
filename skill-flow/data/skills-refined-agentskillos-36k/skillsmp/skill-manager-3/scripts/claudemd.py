#!/usr/bin/env python3
"""
claudemd.py - Maintains the global CLAUDE.md file.

Scans skills directory for SKILL.md files, extracts name and description
from YAML frontmatter, and merges missing skills into CLAUDE.md.

Content outside the auto-generated markers is preserved, allowing agents
and users to add their own notes over time.
"""

import os
import re
import json
import argparse
from pathlib import Path

# Configuration - use /home/agent for container environment
AGENT_HOME = Path("/home/agent")
CLAUDE_DIR = Path(os.environ.get('CLAUDE_DIR', AGENT_HOME / ".claude"))
SKILLS_DIR = CLAUDE_DIR / "skills"
CLAUDE_MD_PATH = CLAUDE_DIR / "CLAUDE.md"

# Markers to identify auto-generated section
SKILLS_SECTION_START = "<!-- AUTO-GENERATED SKILLS START -->"
SKILLS_SECTION_END = "<!-- AUTO-GENERATED SKILLS END -->"

# User preferences (persistent across rebuilds)
USER_PREFS_FILE = SKILLS_DIR / ".skill-system" / "patterns" / "user-preferences.json"
USER_PREFS_START = "<!-- USER PREFERENCES START -->"
USER_PREFS_END = "<!-- USER PREFERENCES END -->"

# Manual directives from repo (version controlled)
MANUAL_DIRECTIVES_FILE = SKILLS_DIR / "CLAUDE.local.md"
MANUAL_DIRECTIVES_START = "<!-- MANUAL DIRECTIVES START -->"
MANUAL_DIRECTIVES_END = "<!-- MANUAL DIRECTIVES END -->"


def parse_yaml_frontmatter(filepath):
    """
    Parse YAML frontmatter from a SKILL.md file using regex.
    Returns dict with 'name' and 'description' or None if parsing fails.
    """
    try:
        content = filepath.read_text()

        # Check for YAML frontmatter delimiters
        if not content.startswith("---"):
            return None

        # Find the closing ---
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return None

        yaml_content = content[3:end_idx]

        # Extract key-value pairs using regex
        result = {}

        # Match name: value (simple key-value)
        name_match = re.search(r'^name:\s*(.+)$', yaml_content, re.MULTILINE)
        if name_match:
            value = name_match.group(1).strip()
            # Remove surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            result['name'] = value

        # Match description: value (can contain quotes and special chars)
        desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)
        if desc_match:
            value = desc_match.group(1).strip()
            # Remove surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            result['description'] = value

        return result if result.get('name') else None

    except Exception as e:
        return None


def discover_skills(verbose=False):
    """
    Discover all skills with SKILL.md files recursively.
    Returns list of dicts with 'name', 'description', 'dir'.
    """
    skills = []

    if not SKILLS_DIR.exists():
        return skills

    # Use rglob to find all SKILL.md files recursively
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        # Skip hidden directories and system directories starting with .
        if any(part.startswith(".") for part in skill_md.relative_to(SKILLS_DIR).parts):
            continue
            
        # Skip the _skill-manager itself if it's considered a skill (optional)
        # if "_skill-manager" in skill_md.parts:
        #     continue

        frontmatter = parse_yaml_frontmatter(skill_md)
        if frontmatter and frontmatter.get("name"):
            # Use the directory containing SKILL.md as the skill dir name
            skill_dir_name = skill_md.parent.name
            
            # If it's very deep, we might want to include more context in the name
            # but for now, the parent directory name is usually sufficient.
            
            skills.append({
                "name": frontmatter.get("name"),
                "description": frontmatter.get("description", "No description available"),
                "dir": skill_dir_name,
            })
            if verbose:
                print(f"  Found: {frontmatter.get('name')} in {skill_dir_name}")
        elif verbose:
            print(f"  Skipping {skill_md}: no valid frontmatter")

    return skills


def get_initial_template():
    """Return the initial CLAUDE.md template."""
    return f'''# Agent Mobile

Global configuration for Claude Code in the agent-mobile container.

## Available Skills

{SKILLS_SECTION_START}
<!-- Skills will be auto-inserted here -->
{SKILLS_SECTION_END}

## Environment Capabilities

### GitHub Access

A `GITHUB_TOKEN` personal access token is available in the environment. Use it for:
- GitHub API operations via `gh` CLI (already authenticated)
- Cloning/pushing to private repositories (git credentials configured)
- Direct API requests: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/...`

### Tailscale Network

This container runs on a Tailscale network with MagicDNS enabled:
- **MagicDNS hostname**: `agent-mobile` (preferred, easier to remember)
- **Get IP**: `tailscale ip -4`

When deploying local services (web servers, APIs, etc.), tell the user to connect via:
- `http://agent-mobile:<port>` (MagicDNS)
- `http://<tailscale-ip>:<port>` (IP fallback)

Example: If you start a server on port 3000, the user accesses it at `http://agent-mobile:3000`

### Package Installation

This container has **passwordless sudo** configured. You can install missing packages without prompts:

```bash
sudo apt-get update && sudo apt-get install -y <package-name>
```

Common packages you might need:
- Build tools: `build-essential`, `cmake`, `pkg-config`
- Python: `python3-pip`, `python3-venv`, `python3-dev`
- Languages: `golang-go`, `rustc`, `cargo`
- Databases: `postgresql-client`, `redis-tools`, `sqlite3`
- Networking: `netcat`, `nmap`, `dnsutils`

Use this proactively when a tool or dependency is missing rather than asking the user to install it.

### Docker

This container has access to the host's Docker daemon via socket mount. You can manage containers directly:

```bash
# Run containers
docker run -d --name redis -p 6379:6379 redis:latest

# List running containers
docker ps

# Stop and remove
docker stop <container>
docker rm <container>

# View logs
docker logs <container>

# Execute commands in container
docker exec -it <container> sh
```

**Common use cases:**
- Spin up Redis, PostgreSQL, or other services for development
- Run one-off containers for testing
- Manage supporting services for projects in `~/projects`

**Network note:** Containers started here share the host network context. Access them via `localhost:<port>` from within the agent, or via `agent-mobile:<port>` from other Tailscale devices.

## Documentation

**Always update documentation** when completing features, changes, or tasks:

- Update `README.md` when adding/changing features, commands, or configuration
- Update relevant `.md` files in the project when behavior changes
- Keep docs concise and accurate - remove outdated information
- Add new features to appropriate sections (Features list, usage examples, etc.)

Do this automatically as part of completing work, not as a separate step.

## Git Safety

**Never push to protected branches without explicit user confirmation:**

- `main`, `master`, `production`, `release/*` are sensitive branches
- Always ask before: `git push origin main`, `git push origin master`
- Force pushes (`--force`, `-f`) require explicit user approval
- When in doubt, push to a feature branch and create a PR instead

Safe by default:
- Pushing to feature branches: OK
- Creating commits: OK
- Creating PRs: OK

## Skill System Awareness

**Learn user preferences from usage patterns.** Run periodically:
```bash
# Scan transcripts for patterns
python3 ~/.claude/skills/_skill-manager/scripts/manage.py scan

# Learn user preferences (workflows, style, shortcuts)
python3 ~/.claude/skills/_skill-manager/scripts/manage.py preferences --force
```

This learns actionable rules like:
- "After commit, push" → auto-push when user says commit
- "Before commit, update docs" → update docs first
- Response style preferences from feedback

**Run after sessions** where user gives feedback or repeats similar commands.

## Project Domains

Default domains: devops, security, data_science, frontend, backend, git

For niche areas, add custom domain markers in:
`~/.claude/skills/.skill-system/config.json`

## Manual Directives

{MANUAL_DIRECTIVES_START}
<!-- Loaded from skills/CLAUDE.local.md -->
{MANUAL_DIRECTIVES_END}

## Notes

Add your own notes below this line. They will be preserved across updates.

---

'''


def generate_skills_section(skills):
    """Generate the skills documentation section."""
    if not skills:
        return "No skills installed yet.\n"

    lines = []
    for skill in sorted(skills, key=lambda s: s["name"]):
        lines.append(f"### {skill['name']}")
        lines.append(f"{skill['description']}")
        lines.append("")

    return "\n".join(lines)


def load_user_preferences():
    """Load user preferences from JSON file."""
    if not USER_PREFS_FILE.exists():
        return {}
    try:
        with open(USER_PREFS_FILE) as f:
            return json.load(f)
    except:
        return {}


def load_manual_directives():
    """Load manual directives from CLAUDE.local.md in skills folder."""
    if not MANUAL_DIRECTIVES_FILE.exists():
        return ""
    try:
        content = MANUAL_DIRECTIVES_FILE.read_text().strip()
        # Skip the title line if present
        lines = content.split('\n')
        if lines and lines[0].startswith('# '):
            lines = lines[1:]
        return '\n'.join(lines).strip()
    except:
        return ""


def generate_user_prefs_section(prefs):
    """Generate markdown section from user preferences."""
    if not prefs:
        return ""

    sections = []

    # Workflow rules
    workflows = prefs.get("rules", {}).get("workflows", [])
    if workflows:
        sections.append("## Workflow Rules")
        sections.append("Do these automatically without asking:")
        for r in workflows:
            sections.append(f"- {r['rule'].capitalize()}")
        sections.append("")

    # Style preferences
    style = prefs.get("rules", {}).get("style", [])
    if style:
        sections.append("## Response Style")
        for s in style:
            sections.append(f"- {s['rule'].capitalize()}")
        sections.append("")

    # Skip preferences
    skips = prefs.get("rules", {}).get("skip", [])
    if skips:
        sections.append("## Skip Unless Asked")
        for s in skips:
            sections.append(f"- {s['rule'].capitalize()}")
        sections.append("")

    # Project context
    context = prefs.get("context", [])
    if context:
        sections.append("## Current Project")
        for c in context:
            if c['type'] == 'tech':
                sections.append(f"- Uses: {c['value']}")
            elif c['type'] == 'url':
                sections.append(f"- URL: {c['value']}")
            elif c['type'] == 'project_name':
                sections.append(f"- Project: {c['value']}")
        sections.append("")

    return "\n".join(sections)


def update_claude_md(verbose=True):
    """
    Main function to update CLAUDE.md.
    Discovers skills and merges them into the auto-generated section.
    Preserves all content outside the markers.
    """
    # Discover all skills
    if verbose:
        print("Scanning for skills...")
    skills = discover_skills(verbose=verbose)
    if verbose:
        print(f"Found {len(skills)} skill(s) with SKILL.md files")

    # Check if CLAUDE.md exists
    if not CLAUDE_MD_PATH.exists():
        if verbose:
            print("Creating new CLAUDE.md from template...")
        content = get_initial_template()
    else:
        content = CLAUDE_MD_PATH.read_text()

    # Find skills section markers
    start_idx = content.find(SKILLS_SECTION_START)
    end_idx = content.find(SKILLS_SECTION_END)

    # Generate new skills content
    new_skills_content = generate_skills_section(skills)

    if start_idx == -1 or end_idx == -1:
        # No markers found - add the skills section
        if verbose:
            print("Skills section markers not found, adding them...")

        # Try to insert after "## Available Skills" if it exists
        avail_skills_idx = content.find("## Available Skills")
        if avail_skills_idx != -1:
            # Find end of that line
            newline_idx = content.find("\n", avail_skills_idx)
            if newline_idx != -1:
                insert_pos = newline_idx + 1
                skills_block = f"\n{SKILLS_SECTION_START}\n{new_skills_content}{SKILLS_SECTION_END}\n"
                content = content[:insert_pos] + skills_block + content[insert_pos:]
        else:
            # Insert after first heading or at start
            first_heading = content.find("\n## ")
            if first_heading != -1:
                insert_pos = first_heading + 1
            else:
                insert_pos = 0

            skills_block = f"\n## Available Skills\n\n{SKILLS_SECTION_START}\n{new_skills_content}{SKILLS_SECTION_END}\n\n"
            content = content[:insert_pos] + skills_block + content[insert_pos:]
    else:
        # Replace content between markers
        content = (
            content[:start_idx + len(SKILLS_SECTION_START)]
            + "\n"
            + new_skills_content
            + content[end_idx:]
        )

    # Also restore user preferences if they exist
    user_prefs = load_user_preferences()
    if user_prefs:
        if verbose:
            print("Restoring user preferences...")
        prefs_content = generate_user_prefs_section(user_prefs)
        if prefs_content:
            prefs_section = f"\n{USER_PREFS_START}\n{prefs_content}{USER_PREFS_END}\n"

            # Check if preferences section exists
            prefs_start_idx = content.find(USER_PREFS_START)
            prefs_end_idx = content.find(USER_PREFS_END)

            if prefs_start_idx != -1 and prefs_end_idx != -1:
                # Replace existing
                content = (
                    content[:prefs_start_idx]
                    + prefs_section.strip()
                    + content[prefs_end_idx + len(USER_PREFS_END):]
                )
            else:
                # Append at end
                content = content.rstrip() + "\n" + prefs_section

    # Load and merge manual directives from CLAUDE.local.md
    manual_directives = load_manual_directives()
    if manual_directives:
        if verbose:
            print("Loading manual directives from CLAUDE.local.md...")
        directives_section = f"{MANUAL_DIRECTIVES_START}\n{manual_directives}\n{MANUAL_DIRECTIVES_END}"

        # Check if manual directives section exists
        dir_start_idx = content.find(MANUAL_DIRECTIVES_START)
        dir_end_idx = content.find(MANUAL_DIRECTIVES_END)

        if dir_start_idx != -1 and dir_end_idx != -1:
            # Replace existing
            content = (
                content[:dir_start_idx]
                + directives_section
                + content[dir_end_idx + len(MANUAL_DIRECTIVES_END):]
            )
        else:
            # Insert before ## Notes if it exists, otherwise append
            notes_idx = content.find("## Notes")
            if notes_idx != -1:
                content = content[:notes_idx] + f"## Manual Directives\n\n{directives_section}\n\n" + content[notes_idx:]
            else:
                content = content.rstrip() + f"\n\n## Manual Directives\n\n{directives_section}\n"

    # Write back
    CLAUDE_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLAUDE_MD_PATH.write_text(content)

    if verbose:
        print(f"Updated {CLAUDE_MD_PATH}")
        for skill in sorted(skills, key=lambda s: s["name"]):
            desc_preview = skill['description'][:50] + "..." if len(skill['description']) > 50 else skill['description']
            print(f"  - {skill['name']}: {desc_preview}")
        if user_prefs:
            rules = user_prefs.get("rules", {})
            total_rules = len(rules.get("workflows", [])) + len(rules.get("style", [])) + len(rules.get("skip", []))
            print(f"  + {total_rules} user preference rules restored")
        if manual_directives:
            print(f"  + Manual directives loaded from CLAUDE.local.md")


def main():
    parser = argparse.ArgumentParser(description="Maintain global CLAUDE.md with skill documentation")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    parser.add_argument("--check", action="store_true", help="Check skills without updating")
    args = parser.parse_args()

    if args.check:
        skills = discover_skills(verbose=True)
        print(f"\nTotal skills found: {len(skills)}")
        for s in skills:
            print(f"  {s['name']}: {s['description'][:60]}...")
    else:
        update_claude_md(verbose=not args.quiet)


if __name__ == "__main__":
    main()
