# Browser Skill Design Notes

This document accompanies the **browser** skill.  It explains some of the key design decisions and improvements made in
this version compared to earlier implementations.

## Cross‑Platform Chrome Detection

Many users work on different operating systems, so the `start.js` script attempts to locate the Chrome binary on macOS,
Linux and Windows.  It checks a list of common installation paths and allows overriding via the `CHROME_PATH`
environment variable or the `--chrome-path` flag.  If Chrome cannot be found the script prints a clear error message
and exits.

## Profile Copying

The `--profile` flag copies the user’s default Chrome profile into the temporary user data directory.  This makes
cookies and login sessions available to Puppeteer.  On macOS, the default profile is under
`~/Library/Application Support/Google/Chrome`, on Windows under `%LOCALAPPDATA%\Google\Chrome\User Data`, and on Linux
under `~/.config/google-chrome` or `~/.config/chromium`.  Copying is best‑effort and ignores errors.

## Port and Headless Options

You can change the remote debugging port using `--port`, which is useful when running multiple sessions in parallel.
Headless mode can be enabled with `--headless`.  When headless is enabled, Chrome is launched with the newer
`--headless=new` flag when supported.

## Navigation Wait Conditions

The `nav.js` script lets you specify how long to wait for a page load.  Choices include:

- `load` – the `load` event fires after the page and all dependent resources have finished loading.
- `domcontentloaded` (default) – the `DOMContentLoaded` event fires when the document has been parsed.
- `networkidle0` – consider navigation complete when there are zero network connections for at least 500 ms.
- `networkidle2` – similar to `networkidle0` but waits for two or fewer connections.

Different wait conditions suit different scraping and automation tasks.

## Multi‑Line Evaluation

The `eval.js` script supports evaluating multi‑statement code by passing an Immediately Invoked Function Expression
(IIFE) or by reading code from a file with `--file`.  It prints arrays and objects in an easy‑to‑read format.

## Screenshots

Screenshots can be saved in PNG or JPEG format and optionally capture the entire page (`--fullpage`).  You can specify
an output filename or let the script generate one based on a timestamp in the system temporary directory.

## Interactive Picker

`pick.js` injects a `pick()` helper into the page if it does not already exist.  The helper displays a banner with
instructions and highlights elements as you hover.  Elements can be selected singly or in groups.  The returned
information includes a trimmed text snippet and the full outer HTML truncated at 500 characters.  Selected elements
receive a green outline, and the banner updates the selection count.

## Environment Variables

All scripts respect the `BROWSER_PORT` environment variable.  If set, it overrides the default port used to connect to
the Chrome instance.  This allows integration with other tools or running multiple browser sessions concurrently.
