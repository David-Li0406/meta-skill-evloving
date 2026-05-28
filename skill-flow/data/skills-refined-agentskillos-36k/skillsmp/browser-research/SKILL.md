---
name: browser-research
description: Research web pages using agent-browser and summarize documentation or articles. Use when investigating URLs, checking page content, or summarizing documents.
allowed-tools: Bash(agent-browser:*), Read, Write
---

# Browser Research Skill

Research web pages using agent-browser CLI and summarize content.

## Usage

```
/browser-research <URL> [research topic or question]
```

## Workflow

### 1. Open the page

```bash
agent-browser open "<URL>"
```

### 2. Get page structure

```bash
agent-browser snapshot --compact
```

Use `--compact` to remove empty structural elements for cleaner output.

### 3. Get detailed content if needed

Get text from specific element:
```bash
agent-browser get text "@ref"
```

Get full page text:
```bash
agent-browser eval "document.body.innerText"
```

### 4. Handle long pages

Scroll to load more content:
```bash
agent-browser scroll down 500
agent-browser snapshot --compact
```

### 5. Navigate to linked pages

Click a link:
```bash
agent-browser click "@ref"
agent-browser snapshot --compact
```

Go back:
```bash
agent-browser back
```

### 6. Close when done

```bash
agent-browser close
```

## Output Format

Always respond in Japanese. Summarize findings in the following format:

1. **概要 (Overview)**: Main topic and purpose of the page
2. **主要ポイント (Key Points)**: Important information as bullet points
3. **詳細 (Details)**: Detailed explanations as needed
4. **関連リンク (Related Links)**: Additional resources to reference

## Notes

- Close existing session with `agent-browser close` before opening a new page
- For JavaScript-heavy pages, wait before snapshot: `agent-browser wait 2000`
- Cannot access pages requiring authentication
