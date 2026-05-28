---
name: Agent Browser Integration
description: >-
  Use Vercel's agent-browser CLI for automated browser testing and UI
  verification. Use when: (1) browser-based quality gates are required,
  (2) verifying UI behavior in the browser, (3) gathering screenshots or DOM
  evidence during Ralph execution. This replaces Playwriter MCP usage.
---

# Agent Browser Integration

Use the Vercel agent-browser CLI to drive browser interactions and collect evidence for UI validation. Ralph should rely on this skill for browser testing instead of Playwriter.

## Prerequisites

- Agent Browser CLI installed and available in PATH
- Browser available for automation (Chrome or Chromium)
- Task context that specifies browser validation requirements

## Setup Checklist

1. Confirm `agent-browser` is available in the shell environment.
2. Ensure the browser instance is running and accessible to the CLI.
3. Capture the target URL(s), expected UI state, and any required credentials.

## Smart Defaults & Triggers

**When to Run Browser Tests:**
1. **Explicit Requirement:** Task description demands UI verification.
2. **Frontend Changes:** You modified `.tsx`, `.jsx`, `.css`, `.html`, or `tailwind` config.
3. **UI Logic:** You changed client-side state management or routing.

## Execution Flow

1. **Open target context:** Use agent-browser CLI to open the required URL (localhost or preview).
2. **Perform UI steps:** Execute interactions (clicks, form entry).
3. **DOM Assertions (REQUIRED):** Use `agent-browser` to assert that specific elements exist or contain text. Do NOT rely solely on visual inspection.
4. **Capture Evidence:**
   - **Failure:** IF an assertion fails, capture a screenshot immediately to document the state.
   - **Success:** Capture a screenshot ONLY if the task involves visual design changes that need human review.
5. **Report:** Summarize results in task comments.

## Shell compatibility (zsh + bun)

- Quote paths and arguments to avoid zsh word-splitting surprises.
- When invoking through Bun, use `--cwd=<dir>` (Bun requires the equals form).

**Example (zsh-safe, Bun + agent-browser):**

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
OUT_DIR="$REPO_ROOT/.devagent/workspace/tests/ralph-e2e/runs/YYYY-MM-DD_<epic-id>/screenshots/qa"

args=(--output-dir "$OUT_DIR" --url "http://127.0.0.1:5173/arcade?seed=demo")
bun --cwd="$REPO_ROOT" x agent-browser "${args[@]}"
```

## Evidence Guidelines

- **DOM Verification:** Primary method. Assert on IDs, text content, or accessibility labels.
- **Failure Screenshots (Mandatory):** Must be captured when a test fails.
- **Success Screenshots (Optional):** Only for visual features.

## Screenshot Management

**Core policy:**
- Screenshots must be saved to repo-visible, project-accessible locations (never `/tmp/`).
- Screenshot storage follows a **routing rule**:
  - If the work is part of the `ralph-e2e` resettable loop, store screenshots in the `ralph-e2e` run hub.
  - Otherwise, store screenshots in the initiating task hub.

**Directory routing rule:**

- **If this is a `ralph-e2e` run** (plan lives under `.devagent/workspace/tests/ralph-e2e/`):
  - Per-run hub: `.devagent/workspace/tests/ralph-e2e/runs/YYYY-MM-DD_<epic-id>/`
  - Save screenshots to: `.devagent/workspace/tests/ralph-e2e/runs/YYYY-MM-DD_<epic-id>/screenshots/`
- **Otherwise (normal work)**:
  - Task hub pattern: `.devagent/workspace/tasks/active/YYYY-MM-DD_task-slug/`
  - Save screenshots to: `.devagent/workspace/tasks/active/YYYY-MM-DD_task-slug/screenshots/`
- **Fallback (last resort)** if you cannot determine the correct hub:
  - `.devagent/workspace/reviews/[epic-id]/screenshots/`

Create screenshot directories if they don't exist.

**Naming Convention:**
- Format: `[task-id]-[description]-[timestamp].png`
- Example: `devagent-6979.1-initial-load-20260118T1530.png`
- Include timestamps for sequence tracking when multiple screenshots are captured.

**Integration with Task Comments:**
- When screenshots are captured, include the repo path(s) in the task comment, and state what each screenshot shows.

## QA evidence format (recommended)

Keep evidence lightweight (Constitution C6), but always include enough to reproduce the decision:

### PASS comment template

- **Result**: PASS
- **Checks**:
  - [ ] <what you verified via DOM assertions>
  - [ ] <what you verified via interaction>
- **Evidence**:
  - DOM assertions: <brief list>
  - Screenshots (optional): `<repo-relative-paths>`
- **References**: <relevant framework/library docs>

### FAIL comment template

- **Result**: FAIL
- **Fail reason**: <one sentence>
- **Expected vs actual**:
  - Expected: <...>
  - Actual: <...>
- **Evidence**:
  - Screenshots (required): `<repo-relative-paths>`
  - DOM assertions: <what failed / what was missing>
- **References**: <relevant framework/library docs>
- **Next action**: set the Beads task back to `open` (see `beads-integration` skill for commands)

**Agent-Browser Configuration:**
- Configure agent-browser to use project-relative paths instead of `/tmp/`.
- Use `--output-dir` or equivalent flag to specify the screenshot directory.
- Ensure screenshots are accessible for review after execution.

## Error Handling

- If the CLI is unavailable, log an issue and pause browser testing.
- If UI actions fail, attempt a single retry before logging a blocker.
- If credentials are missing, request them explicitly rather than guessing.

## References

- Agent Browser repo: `https://github.com/vercel-labs/agent-browser`
