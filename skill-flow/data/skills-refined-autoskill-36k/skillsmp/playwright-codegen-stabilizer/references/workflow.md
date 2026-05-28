# Workflow: From Recording to Production Automation

Use this checklist to convert a raw codegen recording into something that stays stable even when the page shifts slightly.

## Step 0: Confirm the “contract” of the flow

Write the flow as a list of steps:
- Step name (verb + object)
- Entry condition (what must be true before)
- Exit condition (what must be true after)

Example exit conditions:
- URL matches a pattern
- A specific heading/section is visible
- A form field value equals what you set
- A key request completes (if you can observe it)

## Step 1: Refactor into step functions

Replace the long linear script with:
- `run()` or `main()`
- a small number of step functions (5–15)
- a shared `ctx`/`config` object passed into steps

Keep each step:
- short (ideally < 50 lines)
- single-purpose
- independently debuggable

## Step 2: Add a small set of primitives

Create reusable primitives so fixes are made once:
- `click(locator, *, expect_after=None)`
- `fill(locator, value, *, expect_value=None)`
- `select(locator, option, *, expect_value=None)`
- `ensure_visible(locator)`
- `ensure_value(selector/locator, expected)`

Each primitive should:
- wait for actionability/visibility
- retry on transient errors
- produce useful logs

## Step 3: Replace sleeps with explicit waits

Replace:
- `wait_for_timeout(...)`, `time.sleep(...)`

With:
- `expect(locator).to_be_visible()`
- `expect(locator).to_have_text(...)`
- `page.wait_for_url(...)`
- `popup.wait_for_load_state("domcontentloaded")`

## Step 4: Make “duplicates” unambiguous

Any of these should trigger a refactor:
- `.nth(i)`
- `has_text="다음"` without scoping
- click by text on the whole document

Fix by scoping:
- locate the section/container first
- then locate within that container
- then assert the container identity (heading text, unique label, etc.)

## Step 5: Put volatility in config

Move to config:
- selectors and fallback selectors
- text tokens
- retry counts and timeouts
- headless/slowmo/storage state paths

Goal: when a selector changes, edits happen in config, not in code.
