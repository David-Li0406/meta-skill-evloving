<div align="center">
  <h1>Moodle Mirror Skill</h1>
  <p><a href="README.md">English</a> | <a href="README.zh-CN.md">中文</a></p>
</div>

This repository contains a reusable skill package to mirror authenticated Moodle course/module pages to a local folder (e.g., an Obsidian vault), preserving structure and enabling offline search.

### What it does

- Mirrors Moodle pages to `MD` + `TXT` + `meta.json` (URL-to-path mapping, stable on re-runs).
- Downloads common attachments (PDF/DOCX/PPTX/ZIP, etc.) into `_attachments/`.
- Handles common Moodle friction points:
  - SSO redirects (Microsoft login)
  - Cloudflare verification pages (manual completion with bounded waiting)
  - Moodle `mod/resource` downloads (browser-download fallback)
  - Moodle `mod/url` external redirects (mirrors wrapper page via `forceview=1`)

### Important note about MCP

This skill **does not require** any MCP server (e.g., Playwright MCP or Chrome DevTools MCP).
It uses:

- **Python Playwright** for crawling + file writing
- **Chrome CDP** (Chrome DevTools Protocol) optionally, to reuse a real logged-in Chrome session

If you already use browser MCP servers, they can help with interactive login/debugging, but they are not a dependency for the mirroring workflow.

### Prerequisites

- Python 3.x
- Google Chrome
- Playwright for Python + browsers:

```powershell
pip install playwright
python -m playwright install
```

Optional (recommended): start a dedicated Chrome profile with CDP enabled:

```powershell
.\scripts\start_chrome_cdp.ps1
```

Run a quick self-check:

```powershell
python .\scripts\check_prereqs.py
```

### Usage

CDP mode (recommended for bot-detection/SSO-heavy sites):

```powershell
python .\scripts\moodle_mirror.py `
  --cdp-url http://127.0.0.1:9222 `
  --start-url "https://moodle.example.edu/course/view.php?id=123" `
  --out-dir "D:\Obsidian\My Course\Moodle Mirror" `
  --format md --rewrite-links `
  --allow-prefix https://moodle.example.edu/course/ `
  --allow-prefix https://moodle.example.edu/mod/ `
  --allow-prefix https://moodle.example.edu/pluginfile.php/ `
  --max-pages 200 --max-downloads 300 `
  --block-wait-seconds 180
```

Persistent profile mode (use when downloads are flaky in CDP):

```powershell
python .\scripts\moodle_mirror.py `
  --persistent --headful --channel chrome `
  --start-url "https://moodle.example.edu/course/view.php?id=123" `
  --out-dir "D:\Obsidian\My Course\Moodle Mirror" `
  --format md --rewrite-links `
  --allow-prefix https://moodle.example.edu/course/ `
  --allow-prefix https://moodle.example.edu/mod/ `
  --allow-prefix https://moodle.example.edu/pluginfile.php/ `
  --max-pages 200 --max-downloads 300 `
  --block-wait-seconds 180
```

Generate a status report:

```powershell
python .\scripts\mirror_status.py `
  --index "D:\Obsidian\My Course\Moodle Mirror\_index.jsonl" `
  --out   "D:\Obsidian\My Course\Moodle Mirror\_status.md"
```

### Auto-click account selection (SSO helper)

If Microsoft login shows an account chooser (saved account tiles), you can enable best-effort auto-click:

```powershell
python .\scripts\moodle_mirror.py --auto-login --auto-login-account "your.name@ucl.ac.uk" ...
```

This **does not** bypass MFA or enter passwords. MFA prompts still require manual confirmation.

### Notes on overwriting

Re-running the crawler will overwrite local page files for the same URL *when that URL is re-saved*. This is intentional to avoid duplicates when re-running to fix gaps/errors.

For a more incremental workflow:

- Use `--resume` to skip URLs that are already saved.
- Use `--update-on-change` so that when a previously-saved page is revisited (typically start URLs), it is only re-saved if content changed.
- For Moodle, `--polite-delay-ms 0` and `--networkidle-wait-ms 0` are usually fine and noticeably faster.

If you want historical snapshots, use a different output folder per run (e.g., append a date).

### Install as a Codex skill (optional)

Copy this folder into your Codex skills directory (or use your existing skill installer workflow):

- Windows: `C:\Users\<you>\.codex\skills\moodle-mirror`

The skill metadata is in `SKILL.md`.

