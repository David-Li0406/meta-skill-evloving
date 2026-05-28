---
name: repo-explore
description: Use this skill when you want to clone and explore external GitHub repositories to understand how libraries, frameworks, or dependencies work.
---

# Skill body

Explore external GitHub repositories by cloning them locally and using the Explore agent for comprehensive codebase analysis.

## Cache Location

```
~/.cache/claude/repos/<owner>/<repo>/
```

## Workflow

### 1. Parse Repository URL

Extract owner and repo from various formats:
- `https://github.com/owner/repo`
- `git@github.com:owner/repo.git`
- `owner/repo` (shorthand)
- `github.com/owner/repo`

### 2. Check Cache

```bash
ls ~/.cache/claude/repos/<owner>/<repo>/
```

- **If not cached**: Proceed to clone (step 3).
- **If cached and user specified a version/tag**: Proceed to version detection (step 4).
- **If cached and no version specified**: Update to the latest default branch before exploring:
  ```bash
  cd ~/.cache/claude/repos/<owner>/<repo>
  git fetch --all --tags
  DEFAULT_BRANCH=$(git rev-parse --abbrev-ref origin/HEAD | sed 's|origin/||')
  git checkout "$DEFAULT_BRANCH" && git pull origin "$DEFAULT_BRANCH"
  ```

### 3. Clone Repository

```bash
mkdir -p ~/.cache/claude/repos/<owner>
git clone https://github.com/<owner>/<repo>.git ~/.cache/claude/repos/<owner>/<repo>
```

### 4. Version Detection (CRITICAL)

**Before exploring, check if this repo is a dependency in the current working directory.**

Consult `version-detection.md` for:
- Which dependency files to check
- How to extract versions from each format
- How to map versions to git tags

If a matching version is found:
```bash
cd ~/.cache/claude/repos/<owner>/<repo>
git fetch --all --tags
git checkout <tag>
```

Common tag formats to try:
- `v1.2.3`
- `1.2.3`
- `release-1.2.3`
- `release/1.2.3`

### 5. Explore with Explore Agent

**ALWAYS use the Task tool with `subagent_type=Explore` for answering questions about the repository.**

Do NOT manually browse files when the Explore agent can do it. The Explore agent is optimized for:
- Finding files by patterns
- Searching code for keywords
- Understanding codebase architecture
- Answering questions about how code works

Example:
```
Task(
  subagent_type="Explore",
  prompt="""In ~/.cache/claude/repos/owner/repo/, find how authentication is implemented.

Requirements for your response:
- Include code snippets with file paths and line numbers
- Show key functions and their usage
"""
)
```