---
name: vibe
description: 'Talos-class comprehensive code validation. Use for "validate code", "run vibe", "check quality", "security review", "architecture review", "accessibility audit", "complexity check", or any validation need. One skill to validate them all.'
---

# Vibe - Talos Comprehensive Validation

**One skill to validate them all.**

Vibe is a Talos-class validator that combines fast static analysis with deep
semantic verification across all quality dimensions: code quality, security,
architecture, accessibility, complexity, and more.

## Role in the Brownian Ratchet

> **Vibe is THE filter.**

In the Brownian Ratchet pipeline (chaos + filter + ratchet = progress), vibe serves as
the primary validation gate that determines what can proceed:

| Severity | Gate Decision | Ratchet Status |
|----------|---------------|----------------|
| 0 CRITICAL | **PASS** | Can ratchet forward (merge allowed) |
| 1+ CRITICAL | **BLOCK** | Must fix before proceeding |
| HIGH findings | **WARN** | Creates follow-up issues, can proceed |

**Gate Mode** (CI/automation):
```bash
/vibe recent --gate      # Exit non-zero on CRITICAL findings
```

Without the filter, chaos produces garbage. Vibe ensures only valid work ratchets.

## Philosophy

> **Mono over Micro**: Instead of chaining small skills, Vibe provides comprehensive
> validation in one invocation. Trade-off: larger context, but simpler mental model
> and guaranteed coverage.

> **Evidence over Scores**: All claims must be verifiable with specific evidence.
> Use letter grades + findings for quality assessments. Never use numeric scores
> (X/100) for subjective qualities. No "100%" claims without specific context.

## Quick Start

```bash
/vibe                     # Auto-detect target (recent changes or staged files)
/vibe recent              # Full validation of recent changes
/vibe services/           # Validate a directory
/vibe --fast recent       # Prescan only (no LLM, CI-friendly)
/vibe --security recent   # Security-focused deep dive
/vibe --all-aspects all   # Nuclear option: everything on everything
```

## Argument Inference

When invoked without an explicit target, infer from context:

### Priority 1: Conversational Context

If the user mentions a topic, file, or directory in the same message (e.g., "/vibe the auth changes"),
use that as the target:

```bash
# User said "/vibe the auth changes" -> validate auth-related files
git diff --name-only | grep -i auth
# Or search for auth directory
find . -type d -name "*auth*" | head -1
```

**Extract keywords** from the user's message and match against changed files or directories.

### Priority 2: Git State Discovery

```bash
# 1. Check for staged changes
STAGED=$(git diff --cached --name-only 2>/dev/null | head -20)
if [[ -n "$STAGED" ]]; then
    TARGET="staged"
    echo "[VIBE] Auto-selected target: staged changes"
    echo "$STAGED" | head -5
    exit 0
fi

# 2. Check for unstaged changes
UNSTAGED=$(git diff --name-only 2>/dev/null | head -20)
if [[ -n "$UNSTAGED" ]]; then
    TARGET="recent"
    echo "[VIBE] Auto-selected target: recent changes (unstaged)"
    echo "$UNSTAGED" | head -5
    exit 0
fi

# 3. Check for recent commits (last 24h)
RECENT_COMMITS=$(git log --since="24 hours ago" --oneline 2>/dev/null | head -5)
if [[ -n "$RECENT_COMMITS" ]]; then
    TARGET="recent"
    echo "[VIBE] Auto-selected target: recent commits"
    echo "$RECENT_COMMITS"
    exit 0
fi

# 4. No changes found - ask user
echo "[VIBE] No recent changes detected. Please specify a target:"
echo "  /vibe services/        # Validate a directory"
echo "  /vibe path/to/file.py  # Validate specific file"
echo "  /vibe all              # Validate entire codebase"
```

**Key**: Conversational keywords > staged > unstaged > recent commits > ask user.
