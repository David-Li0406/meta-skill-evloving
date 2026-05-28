---
name: skill-install
description: Use this skill when you want to install Claude skills from GitHub repositories with automated security scanning to ensure safety against malicious code.
---

# Skill Install

## Overview

Install Claude skills from GitHub repositories with built-in security scanning to protect against malicious code, backdoors, and vulnerabilities.

## When to Use

Trigger this skill when the user:
- Provides a GitHub repository URL and wants to install skills
- Asks to "install skills from GitHub"
- Wants to browse and select skills from a repository
- Needs to add new skills to their Claude environment

## Workflow

### Step 1: Parse GitHub URL

Accept a GitHub repository URL from the user. The URL should point to a repository containing a `skills/` directory.

Supported URL formats:
- `https://github.com/user/repo`
- `https://github.com/user/repo/tree/main/skills`
- `https://github.com/user/repo/tree/branch-name/skills`

Extract:
- Repository owner
- Repository name
- Branch (default to `main` if not specified)

### Step 2: Fetch Skills List

Use the WebFetch tool to retrieve the skills directory listing from GitHub.

GitHub API endpoint pattern:
```
https://api.github.com/repos/{owner}/{repo}/contents/skills?ref={branch}
```

Parse the response to extract:
- Skill directory names
- Each skill should be a subdirectory containing a SKILL.md file

### Step 3: Present Skills to User

Use the AskUserQuestion tool to let the user select which skills to install.

Set `multiSelect: true` to allow multiple selections.

Present each skill with:
- Skill name (directory name)
- Brief description (if available from SKILL.md frontmatter)

### Step 4: Fetch Skill Content

For each selected skill, fetch all files in the skill directory:

1. Get the file tree for the skill directory
2. Download all files (SKILL.md, scripts/, references/, assets/)
3. Store the complete skill content for security analysis

Use WebFetch with GitHub API:
```
https://api.github.com/repos/{owner}/{repo}/contents/skills/{skill_name}?ref={branch}
```

For each file, fetch the raw content:
```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/skills/{skill_name}/{file_path}
```

### Step 5: Security Scan

**CRITICAL:** Before installation, perform a thorough security analysis of each skill.

Read the security scan prompt template from `references/security_scan_prompt`.