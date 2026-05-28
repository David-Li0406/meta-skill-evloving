---
name: thehub
description: Access GitHub's internal Hub documentation from thehub.github.com URLs. Automatically converts Hub URLs to github/thehub repository paths and retrieves content using GitHub MCP tools. Use when users reference thehub.github.com URLs or request Hub documentation.
---

# TheHub Documentation Reader

Access GitHub's internal Hub documentation (thehub.github.com) by converting URLs to the `github/thehub` repository paths.

## When to Use This Skill

Trigger this skill when:
- User provides a thehub.github.com URL
- User asks about Hub documentation or internal GitHub documentation
- User references "TheHub" or "The Hub"
- You need to access content from thehub.github.com

## How TheHub URLs Work

Hub URLs require 2FA login, but all content is available in the `github/thehub` repository:

**URL Pattern:**
- Hub URL: `https://thehub.github.com/<path>/`
- Repository path: `docs/<path>/` in `github/thehub` repo

**Examples:**
- `https://thehub.github.com/security/security-operations/tailscale/`
  → `docs/security/security-operations/tailscale/`
- `https://thehub.github.com/engineering/teams/copilot/`
  → `docs/engineering/teams/copilot/`

## Workflow

### 1. Convert URL to Repository Path

When you receive a Hub URL:

1. Strip the domain: `https://thehub.github.com/`
2. Take the remaining path
3. Prepend `docs/` to create the repository path
4. Remove trailing slashes

**Example:**
```
Input:  https://thehub.github.com/security/security-operations/tailscale/
Output: docs/security/security-operations/tailscale
```

### 2. Access Content Using GitHub MCP Tools

Use `github-mcp-server-get_file_contents` to fetch content:

**To list directory contents:**
```
owner: github
repo: thehub
path: docs/<converted-path>
```

**To fetch specific files:**
Most Hub pages use `index.md` as the main content file:
```
owner: github
repo: thehub
path: docs/<converted-path>/index.md
```

**Example calls:**
```javascript
// List directory contents
github-mcp-server-get_file_contents(
  owner: "github",
  repo: "thehub",
  path: "docs/security/security-operations/tailscale"
)

// Fetch main page content
github-mcp-server-get_file_contents(
  owner: "github",
  repo: "thehub",
  path: "docs/security/security-operations/tailscale/index.md"
)
```

### 3. Present Content to User

After retrieving the content:

1. **Summarize** the main points relevant to the user's question
2. **Provide context** about what section of TheHub this came from
3. **Include the Hub URL** in your response so users know where the information originated
4. **Extract key information** rather than dumping entire markdown files

## Common Hub Sections

Frequently accessed Hub areas:
- `/engineering/` - Engineering practices, teams, systems
- `/security/` - Security operations, policies, tools
- `/product/` - Product documentation and processes
- `/people/` - HR, benefits, team information
- `/handbook/` - Company handbook and policies

## Important Notes

- **Always use the `github/thehub` repository** - don't try to access thehub.github.com directly
- **Path conversion is critical** - must prepend `docs/` to the URL path
- **Most pages use `index.md`** - try this first for main content
- **Directory listings** - call without filename to see available files
- **Be concise** - summarize content rather than showing everything

## Example Usage

**User request:**
> "What does thehub.github.com/security/security-operations/tailscale/ say about VPN access?"

**Your workflow:**
1. Convert URL: `docs/security/security-operations/tailscale`
2. Fetch directory listing to see files
3. Fetch `docs/security/security-operations/tailscale/index.md`
4. Extract VPN-related information
5. Summarize findings with reference to the Hub URL

**Response format:**
> According to [TheHub Security Operations - Tailscale](https://thehub.github.com/security/security-operations/tailscale/), VPN access is configured by...
> 
> [Key points extracted from the documentation]

## Error Handling

If content is not found:
1. Try listing the parent directory to see available paths
2. Check for alternative file names (README.md, main.md, etc.)
3. Inform user the path may not exist or may have moved
4. Suggest searching the repository if needed
