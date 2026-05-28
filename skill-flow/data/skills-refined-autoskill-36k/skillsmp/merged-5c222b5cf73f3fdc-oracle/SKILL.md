---
name: oracle
description: Use the @steipete/oracle CLI to bundle a prompt plus the right files and get a second-model review (API or browser) for debugging, refactors, design checks, or cross-validation.
---

# Oracle (CLI) — best use

Oracle bundles your prompt and selected files into a single “one-shot” request so another model can provide insights with real repository context (API or browser automation). Treat outputs as advisory: always verify against the codebase and tests.

## When to use
- You need a second-model review with real repo context.
- You want a multi-model comparison for risk/uncertainty.
- You require browser automation runs against ChatGPT/Gemini.

## Philosophy
- Prefer minimal, high-signal context over bulk file dumps.
- Validate outputs against source and tests; never treat them as ground truth.
- Default to API runs for reliability; use browser mode when necessary.

## Anti-patterns
- Do not attach secrets or `.env` files.
- Do not re-run after a timeout; reattach to the session.
- Avoid using browser automation for API-only requirements when API is available.

## Current defaults
- Node requirement: 22+.
- Engine auto-picks API when `OPENAI_API_KEY` is set; otherwise, it defaults to browser.
- Default API model: `gpt-5.1-pro` (alias for GPT‑5.2 Pro).
- Browser model selection: use `--browser-model-strategy current` to keep the active ChatGPT model.

## Golden path (fast + reliable)
1. Pick a tight file set (fewest files that still contain the truth).
2. Preview what you’re about to send using `--dry-run summary` and `--files-report` if needed.
3. Prefer API runs for reliability; use browser runs when necessary.
4. If a run detaches or times out, reattach to the stored session instead of re-running.

## Procedure
1. Clarify the question, target files, and engine choice.
2. Run a dry-run preview to confirm scope.
3. Execute Oracle with the selected engine and model strategy.
4. Review results and verify against code/tests.
5. Reattach instead of re-running if the session detaches.

## Commands (preferred)
- Help (once/session):
  - `npx -y @steipete/oracle --help`

- Preview (no tokens):
  - `npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `npx -y @steipete/oracle --dry-run full -p "<task>" --file "src/**"`

- Token/cost sanity:
  - `npx -y @steipete/oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- API run (default when `OPENAI_API_KEY` is set):
  - `npx -y @steipete/oracle -p "<task>" --file "src/**"`
  - Add `--wait` to stay attached for GPT‑5 Pro background runs.

- Browser run (experimental):
  - `npx -y @steipete/oracle --engine browser --browser-model-strategy current -p "<task>" --file "src/**"`

- Manual paste fallback (assemble bundle, copy to clipboard):
  - `npx -y @steipete/oracle --render --copy -p "<task>" --file "src/**"`

## Files + size limits
- Default ignored directories: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`.
- Honors `.gitignore` when expanding globs.
- Does not follow symlinks.
- Dotfiles are filtered unless explicitly included.
- Hard cap: files > 1 MB are rejected.

## Sessions + reattach
- Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`).
- Runs may detach; reattach via `oracle status --hours 72` and `oracle session <id> --render`.
- Use `--slug "<3-5 words>"` to keep session IDs readable.

## Prompt template (high signal)
Oracle starts with zero project knowledge. Include:
- Project briefing (stack + build/test commands + platform constraints).
- “Where things live” (key directories, entrypoints, config files).
- Exact question + what you tried + error text (verbatim).
- Constraints (“don’t change X”, “must keep public API”, “perf budget”).
- Desired output (“return patch plan + tests”, “list risky assumptions”).

## Safety
- Don’t attach secrets by default (`.env`, key files, tokens). Redact aggressively.
- Prefer “just enough context”: fewer files + better prompt beats whole-repo dumps.
- API runs incur usage costs; get explicit approval before launching them.

## Validation
- Use `--dry-run` and `--files-report` before paid runs.
- Fail fast: stop at the first failed check and fix before continuing.

## Examples
- "Run Oracle in API mode on `src/**` to review a refactor plan."
- "Use browser mode with `--browser-model-strategy current` for UI checks."