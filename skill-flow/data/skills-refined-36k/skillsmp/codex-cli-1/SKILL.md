---
name: codex-cli
description: Use Codex CLI for web search, code review, and writing review. Triggers on (1) web search requests, (2) code review of git changes, (3) writing/file review. Use for "search the web for...", "review this code", "review my changes", "review this file".
---

# Codex CLI

OpenAI's Codex CLI for web search and reviews. All commands are non-interactive.

## Web Search

ChatGPT-tuned agentic search. Default: `gpt-5.2` with medium reasoning.

```bash
codex exec "your question" -c 'tools.web_search=true' -m gpt-5.2 -c model_reasoning_effort="medium" \
  --output-last-message /tmp/codex-result.txt >/dev/null 2>&1 && cat /tmp/codex-result.txt
```

## Code Review (Git Changes)

Default: `gpt-5.2-codex` with high reasoning.

```bash
# Review uncommitted changes (staged + unstaged + untracked)
codex review --uncommitted -c model="gpt-5.2-codex" -c model_reasoning_effort="high"

# Review against a base branch
codex review --base main -c model="gpt-5.2-codex" -c model_reasoning_effort="high"

# Review a specific commit
codex review --commit <sha> -c model="gpt-5.2-codex" -c model_reasoning_effort="high"

# Custom review instructions
codex review --uncommitted "Focus on security issues" -c model="gpt-5.2-codex" -c model_reasoning_effort="high"
```

## Writing/File Review

Review a file for clarity, density, and fluff removal.

```bash
codex exec "Review the writing at <filepath>. Provide an improved version in full, then explain each change. Prioritize: removing fluff, increasing information density, improving clarity. No stylistic preferences." \
  --skip-git-repo-check --output-last-message /tmp/codex-result.txt >/dev/null 2>&1 && cat /tmp/codex-result.txt
```

Use your judgment to incorporate high-value changes directly. Briefly summarize what you changed and why.

## Reasoning Effort

Override with `-c model_reasoning_effort="low|medium|high"`. Higher = deeper analysis, slower.
