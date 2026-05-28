---
name: fastmcp-quality-review
description: Review and score FastMCP MCP server quality. Use when creating/auditing MCP servers, before publishing to MCP directory, or to improve existing servers.
triggers:
  # English
  - is my MCP server good?
  - check my server quality
  - review my MCP
  - how can I improve my MCP server?
  - analyze the quality of this server
  - give me feedback on my MCP
  - how well-written is this server?
  # French
  - mon serveur MCP est-il bon ?
  - vérifie la qualité de mon serveur
  - analyse mon MCP
  - comment puis-je améliorer mon serveur MCP ?
  - donne-moi ton avis sur mon MCP
  - ce serveur est-il bien écrit ?
---

# FastMCP Quality Review

Automated quality review for FastMCP MCP servers based on Anthropic MCP Directory Policy.

## Quick Start

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "fastmcp-quality-review" activated
```

1. Locate the MCP server file (usually `mcp_server.py` or similar)
2. Run the review process below
3. Get a score out of 100 with actionable recommendations

## Review Process

### Step 1: Load Server Code

```python
# Read the MCP server file
from fastmcp import Client
# Import the server instance
```

### Step 2: Run Quality Checks

Execute each check from the [Quality Checklist](references/quality-checklist.md):

| Check | Weight | Pass Criteria |
|-------|--------|---------------|
| Tool Descriptions | 20% | Clear, <64 chars, matches functionality |
| Error Handling | 15% | Graceful errors with helpful messages |
| Annotations | 15% | readOnlyHint, destructiveHint present |
| Token Efficiency | 15% | Minimal response sizes |
| Test Coverage | 20% | pytest tests exist and pass |
| Documentation | 15% | Docstrings + 3 usage examples |

### Step 3: Generate Report

Output format:

```
## MCP Server Quality Report

**Server**: {server_name}
**Score**: {total}/100 ({grade})

### Results by Category

| Category | Score | Status | Issues |
|----------|-------|--------|--------|
| Tool Descriptions | X/20 | ✅/⚠️/❌ | ... |
| Error Handling | X/15 | ... | ... |
| ... | ... | ... | ... |

### Critical Issues (Must Fix)
1. ...

### Recommendations (Should Fix)
1. ...

### Nice to Have
1. ...
```

## Scoring Guide

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Production ready, MCP Directory eligible |
| B | 75-89 | Good quality, minor improvements needed |
| C | 60-74 | Acceptable, several issues to address |
| D | 40-59 | Needs work before deployment |
| F | 0-39 | Major redesign required |

## Review Script

```python
# In-memory review using FastMCP Client
import asyncio
from fastmcp import Client

async def review_mcp_server(mcp_server):
    """Review an MCP server and return quality score."""
    results = {
        "tool_descriptions": {"score": 0, "max": 20, "issues": []},
        "error_handling": {"score": 0, "max": 15, "issues": []},
        "annotations": {"score": 0, "max": 15, "issues": []},
        "token_efficiency": {"score": 0, "max": 15, "issues": []},
        "test_coverage": {"score": 0, "max": 20, "issues": []},
        "documentation": {"score": 0, "max": 15, "issues": []},
    }

    async with Client(transport=mcp_server) as client:
        tools = await client.list_tools()

        for tool in tools:
            # Check description length
            if len(tool.name) > 64:
                results["tool_descriptions"]["issues"].append(
                    f"Tool '{tool.name}' name exceeds 64 chars"
                )

            # Check description exists and is clear
            if not tool.description or len(tool.description) < 10:
                results["tool_descriptions"]["issues"].append(
                    f"Tool '{tool.name}' has missing/short description"
                )

            # Check for annotations (if available in schema)
            # ...

    return results
```

## What to Check Manually

Some checks require manual review:

1. **Functionality Match**: Do tools actually do what descriptions say?
2. **Security**: OAuth 2.0 for remote servers? No hardcoded secrets?
3. **Edge Cases**: Test with invalid inputs
4. **Token Bloat**: Are responses unnecessarily verbose?

See [references/manual-review-guide.md](references/manual-review-guide.md) for detailed manual checks.

## Skill Chaining

### Skills Required Before
- None (entry point for MCP review)

### Input Expected
- Path to MCP server file or module
- Optional: path to test directory

### Output Produced
- **Format**: Markdown quality report with score
- **Side effects**: None (read-only analysis)

### Compatible Skills After
- **skill-creator**: If major rewrite needed
- **commit**: After fixing issues

### Tools Used
- `Read` (read server source code)
- `Bash` (run pytest, import checks)
- `Grep` (find patterns in code)
