---
name: playwright-codegen-stabilizer
description: >
  Stabilize Playwright codegen recordings into reliable, maintainable automations.
  Use when a Playwright script recorded via codegen is flaky, fails when replayed, or requires frequent edits
  due to unstable locators, timing issues, popups/dialogs, multi-window flows, or dynamic DOM.
  Provides a repeatable workflow: convert recordings into intent-based locators, centralize selectors and tunables in
  config, add step contracts and diagnostics (trace/screenshot/HTML/a11y dumps), and use Playwright MCP (if available)
  to debug failures and validate fixes.
---

# Playwright Codegen Stabilizer

Convert codegen output into “production automation”: resilient locators, centralized configuration, deterministic waits, and failure artifacts that let an AI fix breakage quickly with minimal code churn.

## Core Principles

- Treat codegen output as a **recording**, not the final script.
- Prefer **intent-based locators** (`get_by_role`, `get_by_label`, `get_by_test_id`) over brittle CSS/XPath.
- Make changes **config-first**: move selectors, timeouts, URLs, and text tokens into a config file so most breakages become config edits.
- Eliminate `sleep`-style timing: replace with **contracts** (assertions / `expect(...)`) and event-based waits.
- When something breaks, always capture **artifacts** (trace + screenshot + HTML + accessibility snapshot) so fixes are data-driven.

## Workflow (Use This Every Time)

1) Reproduce the failure
- Run the script once as-is to identify the failing step.
- Record: failing action, expected state, actual state, URL, and whether a popup/new tab/dialog is involved.

2) Add diagnostics before fixing
- Enable Playwright tracing for the full run or around the failing step.
- On exception: save `trace.zip`, a full-page screenshot, `page.content()` HTML dump, and an accessibility snapshot JSON.
- Save artifacts with a timestamped prefix.
- See `references/diagnostics.md`.

3) Convert the recording into stable structure
- Extract a small set of reusable primitives (click/fill/select/wait-for) with built-in waits and retries.
- Break the script into **steps** (login, navigate, fill section A, open popup, select item, submit).
- Give each step a contract: “how do we know the step succeeded?” (URL, heading visible, field value updated, request finished).
- See `references/workflow.md`.

4) Fix locators the right way (not by piling on `nth()` or sleeps)
- Prefer: `get_by_test_id` > `get_by_role` > `get_by_label` > scoped `locator()` with stable attributes.
- Scope to containers to avoid duplicate text (e.g., `"다음"` exists in multiple sections).
- Avoid `.nth()` unless you can also assert container identity.
- Add fallback locators only when necessary, and keep them centralized in config.
- See `references/locator-strategy.md`.

5) Stabilize multi-window, dialogs, and popups
- Handle dialogs with `page.on("dialog", ...)`.
- For new windows: wrap the triggering action with `expect_popup()` and immediately assert the popup is on the expected origin/page.
- If the site spawns nuisance popups, close by URL/title patterns.
- See `references/popups-and-dialogs.md`.

6) Validate using Playwright MCP (when available)
- Use MCP to inspect the DOM at the failure point, confirm locator uniqueness, and verify the new locator works interactively.
- If MCP is unavailable, fall back to `page.pause()` + trace viewer.

7) Visual validation (required)
- After changes, run the flow and capture **result screenshots** at the defined verification checkpoints.
- Decide pass/fail **only by the actual web UI state** shown in the screenshots (or in the live browser when reproducing).
- Never declare success based on console output/log lines (e.g., “completed successfully”) alone.

8) Regression-proof
- Run the script multiple times (at least 2–3) to confirm flakiness is gone.
- If the flow is critical, add a narrow regression test for the fixed step (or a smoke test) with artifacts enabled.

## Configuration Pattern (Recommended)

Centralize “change often / break often” values:
- URLs and navigation targets
- Selectors and locator strategies (primary + fallbacks)
- Text tokens used for matching
- Timeouts and retry counts
- Environment-specific settings (headless, slowmo, storage_state path)

Use YAML/JSON/TOML—whatever the repo already prefers. Keep the script logic stable; move volatility into config.

## References

- `references/workflow.md` (step contracts + refactor template)
- `references/locator-strategy.md` (locator hierarchy + duplicate text strategy)
- `references/diagnostics.md` (trace/screenshot/html/a11y artifact pattern)
- `references/popups-and-dialogs.md` (popup, dialog, and overlay patterns)
- `references/visual-validation.md` (result screenshots + UI-only pass/fail rule)
