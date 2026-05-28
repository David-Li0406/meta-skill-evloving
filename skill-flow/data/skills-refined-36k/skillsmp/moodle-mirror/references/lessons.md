# Lessons and SOP (Moodle Mirror)

## Purpose

Mirror authenticated Moodle courses into a local folder with stable offline search.

## SOP (High-Level)

1) Preflight:
   - Confirm Chrome CDP endpoint is available (`http://127.0.0.1:9222/json/version`).
   - Confirm output directory exists in the Obsidian vault.
   - If CDP is not running, start Chrome with:
     `chrome.exe --remote-debugging-port=9222 --user-data-dir=%USERPROFILE%\.codex\state\moodle_profile_cdp`
2) Login:
   - Prefer CDP mode (reuse real Chrome session).
   - Use `--auto-login` to click saved account tiles.
3) Crawl:
   - Scope to Moodle paths only (`/course/`, `/mod/`, `/pluginfile.php/`).
   - Use bounded `--max-pages` and `--max-downloads`.
   - For `mod/url` pages, mirror with `forceview=1` to avoid external 502s.
4) Validate:
   - Generate `_status.md` via `mirror_status.py`.
5) Remediate:
   - Handle `mod/url` with `forceview=1`.
   - Use persistent headful mode if downloads fail in CDP.

## Overwrite Rationale

- The crawler maps each URL to a fixed file path.
- Re-running the crawl for the same URL will overwrite those files.
- This is intentional to prevent duplicate files when fixing gaps or errors.
- If you need history, use a new output folder per run (e.g., append a date).

## Prerequisites

??????????`python .\scripts\check_prereqs.py`?

- Python + Playwright installed
- Chrome installed
- For CDP: start Chrome with `--remote-debugging-port=9222`

## MCP????

- MCP ???????????? `Python Playwright` ?????
- MCP ?????????????/??????????????

## Tool Choices (What Worked vs. Not)

- Works best:
  - Playwright + CDP (reuses logged-in Chrome, fewer bot checks).
  - Playwright persistent profile (`--persistent --channel chrome`) when downloads are flaky.
- Not viable:
  - `curl`/`Invoke-WebRequest` without auth (HTTP 403).
  - Browser-to-localhost receiver (blocked by Private Network Access / Local Network Access).
  - Fully headless for Cloudflare/SSO-heavy flows.

## Common Problems and Fixes

1) HTTP 502 on `mod/url/view.php`:
   - Root cause: Moodle URL module redirects to external site with Cloudflare 502.
   - Fix: Use `forceview=1` and mirror the internal Moodle page.

2) “Download is starting” errors:
   - Root cause: Moodle resource triggers a file download, not a page.
   - Fix: Treat `/mod/resource/view.php` as a download and use browser download fallback.

3) Cloudflare “Verify you are human”:
   - Root cause: Anti-bot check.
   - Fix: Keep browser headful, wait with `--block-wait-seconds`, complete manually if needed.

4) Re-login on every run:
   - Root cause: no persistent session.
   - Fix: Use CDP or persistent profile; store auth under `%USERPROFILE%\.codex\state`.

5) Script hang:
   - Root cause: blocked SSO or network stall.
   - Fix: use timeouts, stop stuck `python`, re-run with smaller scope.

## Constraints

- Cannot bypass MFA or password prompts; auto-login only clicks saved account tiles.
- External sites behind Cloudflare can still fail; mirror the Moodle “wrapper” page instead.
- By default, re-runs overwrite page files for the same URL. Use a new output folder per run to keep historical snapshots.
