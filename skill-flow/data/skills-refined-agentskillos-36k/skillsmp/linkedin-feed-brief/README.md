# linkedin-feed-brief

This skill collects and summarizes LinkedIn home feed posts using **Playwright MCP** in **Extension Mode** (browser-based). Extension Mode lets the agent operate inside a real, signed-in Chrome profile (useful for sites like LinkedIn).

Reference: `https://github.com/microsoft/playwright-mcp/blob/main/extension/README.md`

## When this skill should run

Use `linkedin-feed-brief` when the user wants to:

- Open `https://www.linkedin.com/feed/`
- Collect **N** home-feed posts while scrolling
- Exclude ads/“Promoted” posts and non-post modules (jobs, in-app promotions)
- Produce a grouped brief with keywords + per-post title/insight + a source link (prefer permalink; fallback to URN-based `/feed/update/{URN}/`)

## Install this skill

### Codex

```bash
$skill-installer install https://github.com/ZiminPark/agent-zym/tree/main/plugins/linkedin-feed-brief/skills/linkedin-feed-brief
```

Restart Codex to pick up new skills.

### Claude Code

```bash
/plugins marketplace add ZiminPark/agent-zym
/plugins install linkedin-feed-brief
```

## Minimal setup (Playwright MCP Extension Mode)

1) Install **Google Chrome**.

2) Install the **Playwright MCP** Chrome extension:
   - Download the extension build as described in the reference README.
   - In Chrome, go to `chrome://extensions`, enable **Developer mode**, then **Load unpacked**.

3) Start the MCP server in Extension Mode:
   ```bash
   npx @playwright/mcp@latest --extension
   ```

4) In your MCP client, connect to the Playwright MCP server. Once connected, the agent can drive the same Chrome session (including your LinkedIn login) to scroll `/feed/` and extract posts.
