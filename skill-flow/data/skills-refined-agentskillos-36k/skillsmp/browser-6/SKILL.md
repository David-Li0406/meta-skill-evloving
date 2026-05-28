---
name: browser
description: Automate Chrome via Puppeteer to browse, navigate, scrape, and capture web pages across platforms.
version: 1.0.0
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# Browser Skill

## Overview

The browser skill allows AI agents to interact with web pages through a locally installed Chrome browser using the
[`puppeteer-core`](https://pptr.dev/) library.  It supports launching Chrome, navigating to pages, executing JavaScript,
taking screenshots and interactively picking DOM elements.  This version improves on the original design by adding
cross‑platform support, richer options and more robust error handling.

### When to use

Use this skill whenever you need to:

* Browse or scrape websites.
* Automate form submissions or clicks.
* Extract data from web pages via DOM queries.
* Capture screenshots of pages.
* Select elements visually for follow‑up actions.

### Features

* **Cross‑platform Chrome detection** – automatically locates the Chrome binary on macOS, Linux and Windows, or you can
  override the path with the `CHROME_PATH` environment variable.
* **Optional profile sync** – copy your existing Chrome profile (cookies, logins) into a temporary user data directory via `--profile`.
* **Customisable launch** – configure the remote debugging port (`--port`), headless mode (`--headless`), and user data
  directory (`--user-data-dir`).
* **Flexible navigation** – open pages in the current tab or a new tab (`--new`), and specify the wait condition for
  navigation (`--wait load|domcontentloaded|networkidle0|networkidle2`).
* **Multi‑line JavaScript evaluation** – execute arbitrary expressions or multi‑statement scripts and optionally read code
  from a file (`--file <path>`).
* **Configurable screenshots** – capture either the viewport or the full page, choose the output path and file format.
* **Interactive element picker** – pick elements visually with support for multi‑selection, returning rich information
  about each selected element.

## Setup

1. Ensure [Node.js](https://nodejs.org/) version 18 or higher is installed.
2. Install the dependencies in the skill directory:

   ```bash
   npm install --prefix skills/browser
   ```

3. Make sure Google Chrome is installed on your machine.  If Chrome is not installed in a standard location you can
   specify its path via the `CHROME_PATH` environment variable or the `--chrome-path` flag when launching the browser.

## Tools

This skill exposes several scripts in the `scripts/` folder.  They should be run with Node and are designed to be called
by an AI agent.  Each script prints human‑readable messages or simple data to `stdout`.

### start.js – launch Chrome

Launches a Chrome instance under the control of Puppeteer.  Available options:

* `--profile` – copy your default Chrome profile (cookies, logins) into the temporary user data directory.
* `--user-data-dir <dir>` – specify a custom directory for Chrome’s user data.
* `--chrome-path <path>` – override the detected path to the Chrome executable.
* `--port <number>` – specify the remote debugging port (default `9222`).
* `--headless` – run Chrome in headless mode.

Example:

```bash
node scripts/start.js --profile --port 9223
```

### nav.js – navigate to a URL

Opens the given URL in the current tab or a new tab and waits for the page to load.  Options:

* `--new` – open the URL in a new tab instead of the current tab.
* `--wait <event>` – specify when navigation is considered complete; accepted values are `load`,
  `domcontentloaded`, `networkidle0`, and `networkidle2` (default `domcontentloaded`).

Example:

```bash
node scripts/nav.js https://example.com --new --wait networkidle2
```

### eval.js – execute JavaScript on the page

Evaluates JavaScript in the context of the active page.  Accepts either a single expression or a multi‑statement
immediately invoked function expression (IIFE).  Options:

* `--file <path>` – read the JavaScript to evaluate from a file.  This is useful for longer scripts.

Example:

```bash
node scripts/eval.js "document.title"
node scripts/eval.js --file scripts/sample.js
```

### screenshot.js – capture a screenshot

Captures the current page.  Options:

* `--file <path>` – specify the output file path.  If omitted, a timestamped filename in the system temporary directory is used.
* `--fullpage` – capture the entire page rather than just the visible viewport.
* `--format <png|jpeg>` – choose the image format (`png` by default).

Example:

```bash
node scripts/screenshot.js --file ~/Desktop/page.png --fullpage
```

### pick.js – interactively pick DOM elements

Displays an overlay in the current page and lets you click elements to inspect them.  When finished, it returns an array
of objects describing each selected element:

* `tag` – the element’s tag name.
* `id` – the element’s ID (if any).
* `class` – the element’s class attribute (if any).
* `text` – up to 200 characters of text content.
* `html` – up to 500 characters of the element’s outer HTML.
* `parents` – a “breadcrumb” of the element’s parent chain.

Use Cmd/Ctrl+click to select multiple elements, Enter to finish, or Esc to cancel.

## Workflow

1. Run `start.js` once per session to launch Chrome.  Use `--profile` if you need to retain cookies or logged‑in state.
2. Use `nav.js` to open the target page.  The `--new` flag can be used to avoid overwriting the current tab.
3. Use `eval.js` to run JavaScript for scraping or automation tasks.
4. Call `screenshot.js` to capture evidence or debug pages as needed.
5. Use `pick.js` to visually select elements when CSS selectors are not known in advance.

## References

See `references/design.md` for additional design notes, and refer to the script source files in `scripts/` for
implementation details.
