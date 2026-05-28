---
name: web-to-markdown
description: Use this skill when the user explicitly requests to convert webpage URLs to clean Markdown using the `web2md` CLI.
---

# Skill body

## Hard trigger gate (must enforce)

This skill MUST NOT be used unless the user explicitly wrote **exactly** a phrase like:
- `use the skill web-to-markdown ...`
- `use a skill web-to-markdown ...`

If the user did not explicitly request this skill by name, stop and ask them to re-issue the request including: `use the skill web-to-markdown`.

## What this skill does

- Handles JS-rendered pages (Puppeteer → user Chrome).
- Works best with Chromium-family browsers (Chrome/Chromium/Brave/Edge) via `puppeteer-core`.
- Extracts main content (Readability).
- Converts to Markdown (Turndown) with cleaned links and optional YAML frontmatter.

## Non-goals

- Do not use Playwright or other browser automation stacks; the mechanism is `web2md`.

## Inputs you should collect (ask only if missing)

- `url` (or a list of URLs)
- Output preference:
  - Print to stdout (`--print`), OR
  - Save to a file (`--out ./file.md`), OR
  - Save to a directory (`--out ./some-dir/` to auto-name by page title)
- Optional rendering controls for tricky pages:
  - `--chrome-path <path>` (if Chrome auto-detection fails)
  - `--interactive` (show Chrome and pause so the user can complete human checks/login, then press Enter)
  - `--wait-until load|domcontentloaded|networkidle0|networkidle2`
  - `--wait-for '<css selector>'`
  - `--wait-ms <milliseconds>`
  - `--headful` (debug)
  - `--no-sandbox` (sometimes required in containers/CI)
  - `--user-data-dir <dir>` (login/session; use a dedicated profile directory)

## Workflow

1. Confirm the user explicitly invoked the skill (`use the skill web-to-markdown`).
2. Validate URL(s) start with `http://` or `https://`.
3. Ensure `web2md` is installed:
   - Run: `command -v web2md`
   - If missing, instruct the user to install it (assume the project exists at `~/workspace/softaworks/projects/web2md`):
     - If available via npm: `npm install -g web2md`
     - If from source: 
       - `cd ~/workspace/softaworks/projects/web2md && npm install && npm run build && npm link`
       - Or: `cd ~/workspace/softaworks/projects/web2md && npm install && npm run build && npm install -g .`
4. Convert:
   - Single URL → file:
     - `web2md '<url>' --out ./page.md`
   - Single URL → auto-named file in directory:
     - `mkdir -p ./out && web2md '<url>' --out ./out/`
   - List of URLs → files:
     - For each URL, run `web2md '<url>' --out ./out/$(basename '<url>').md`