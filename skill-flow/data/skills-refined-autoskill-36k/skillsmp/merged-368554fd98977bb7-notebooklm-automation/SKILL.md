---
name: notebooklm-automation
description: Use this skill to automate Google NotebookLM for creating notebooks, adding sources, generating various artifacts, and downloading results, including handling anti-crawler content extraction.
---

# NotebookLM Automation

Automate Google NotebookLM: create notebooks, add sources, chat with content, generate artifacts (podcasts, videos, quizzes), and download results. This skill also supports browser-based content extraction for anti-crawler platforms (Twitter/X, LinkedIn, etc.).

## Prerequisites

**IMPORTANT:** Before using any command, you MUST authenticate:

```bash
notebooklm login          # Opens browser for Google OAuth
notebooklm list           # Verify authentication works
```

If commands fail with authentication errors, re-run `notebooklm login`.

### CI/CD, Multiple Accounts, and Parallel Agents

For automated environments, multiple accounts, or parallel agent workflows:

| Variable | Purpose |
|----------|---------|
| `NOTEBOOKLM_HOME` | Custom config directory (default: `~/.notebooklm`) |
| `NOTEBOOKLM_AUTH_JSON` | Inline auth JSON - no file writes needed |

**CI/CD setup:** Set `NOTEBOOKLM_AUTH_JSON` from a secret containing your `storage_state.json` contents.

**Multiple accounts:** Use different `NOTEBOOKLM_HOME` directories per account.

**Parallel agents:** The CLI stores notebook context in a shared file (`~/.notebooklm/context.json`). Multiple concurrent agents using `notebooklm use` can overwrite each other's context.

**Solutions for parallel workflows:**
1. **Always use explicit notebook ID** (recommended): Pass `-n <notebook_id>` (for `wait`/`download` commands) or `--notebook <notebook_id>` (for others) instead of relying on `use`.
2. **Per-agent isolation:** Set unique `NOTEBOOKLM_HOME` per agent: `export NOTEBOOKLM_HOME=/tmp/agent-$ID`.
3. **Use full UUIDs:** Avoid partial IDs in automation (they can become ambiguous).

## Agent Setup Verification

Before starting workflows, verify the CLI is ready:

1. `notebooklm status` → Should show "Authenticated as: email@..."
2. `notebooklm list --json` → Should return valid JSON (even if empty notebooks list)
3. If either fails → Run `notebooklm login`

## When This Skill Activates

**Explicit:** User says "/notebooklm", "use notebooklm", or mentions the tool by name.

**Intent detection:** Recognize requests like:
- "Create a podcast about [topic]"
- "Summarize these URLs/documents"
- "Generate a quiz from my research"
- "Turn this into an audio overview"
- "Add these sources to NotebookLM"
- "Create a notebook from [Twitter/X link]"
- "Extract content from this [social media post]"

## Autonomy Rules

**Run automatically (no confirmation):**
- `notebooklm status` - check context
- `notebooklm list` - list notebooks
- `notebooklm source list` - list sources
- `notebooklm artifact list` - list artifacts
- `notebooklm artifact wait` - wait for artifact completion (in subagent context)
- `notebooklm source wait` - wait for source processing (in subagent context)
- `notebooklm research status` - check research status
- `notebooklm research wait` - wait for research (in subagent context)
- `notebooklm use <id>` - set context (⚠️ SINGLE-AGENT ONLY - use `-n` flag in parallel workflows)
- `notebooklm create` - create notebook
- `notebooklm ask "..."` - chat queries
- `notebooklm source add` - add sources

**Ask before running:**
- `notebooklm delete` - destructive
- `notebooklm generate *` - long-running, may fail
- `notebooklm download *` - writes to filesystem
- `notebooklm artifact wait` - long-running (when in main conversation)
- `notebooklm source wait` - long-running (when in main conversation)
- `notebooklm research wait` - long-running (when in main conversation)

## Quick Reference

| Task | Command |
|------|---------|
| Authenticate | `notebooklm login` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Set context | `notebooklm use <notebook_id>` |
| Show context | `notebooklm status` |
| Add URL source | `notebooklm source add "https://..."` |
| Add file | `notebooklm source add ./file.pdf` |
| Add YouTube | `notebooklm source add "https://youtube.com/..."` |
| Extract Twitter/X via browser | Use Playwright skill → Save → `notebooklm source add ./file.md` |
| Extract anti-crawler content | Use browser automation → Save → Add to notebook |
| List sources | `notebooklm source list` |
| Wait for source processing | `notebooklm source wait <source_id>` |
| Web research (fast) | `notebooklm source add-research "query"` |
| Web research (deep) | `notebooklm source add-research "query" --mode deep --no-wait` |
| Check research status | `notebooklm research status` |
| Wait for research | `notebooklm research wait --import-all` |
| Chat | `notebooklm ask "question"` |
| Chat (new conversation) | `notebooklm ask "question" --new` |
| Chat (specific sources) | `notebooklm ask "question" -s src_id1 -s src_id2` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate podcast (specific sources) | `notebooklm generate audio -s src_id1 -s src_id2` |
| Generate video | `notebooklm generate video "instructions"` |
| Generate quiz | `notebooklm generate quiz` |
| Check artifact status | `notebooklm artifact list` |
| Wait for completion | `notebooklm artifact wait <artifact_id>` |
| Download audio | `notebooklm download audio ./output.mp3` |
| Download video | `notebooklm download video ./output.mp4` |
| Delete notebook | `notebooklm notebook delete <id>` |

## Command Output Formats

Commands with `--json` return structured data for parsing:

**Create notebook:**
```
$ notebooklm create "Research" --json
{"id": "abc123de-...", "title": "Research"}
```

**Add source:**
```
$ notebooklm source add "https://example.com" --json
{"source_id": "def456...", "title": "Example", "status": "PROCESSING"}
```

**Generate artifact:**
```
$ notebooklm generate audio "Focus on key points" --json
{"artifact_id": "xyz789...", "status": "PENDING", "type": "AUDIO_OVERVIEW"}
```

**Extract IDs:** Parse the `id`, `source_id`, or `artifact_id` field from JSON output.

## Generation Types

All generate commands support `-s, --source` to use specific source(s) instead of all sources.

| Type | Command | Downloadable |
|------|---------|--------------|
| Podcast | `generate audio` | Yes (.mp3) |
| Video | `generate video` | Yes (.mp4) |
| Slides | `generate slide-deck` | Yes (.pdf) |
| Infographic | `generate infographic` | Yes (.png) |
| Quiz | `generate quiz` | No (view in UI) |
| Flashcards | `generate flashcards` | No (view in UI) |
| Mind Map | `generate mind-map` | No (view in UI) |
| Data Table | `generate data-table` | No (export to Sheets) |
| Report | `generate report` | No (export to Docs) |

## Common Workflows

### Smart Extraction Workflow (Scene-Based)

**Scenario 1: Twitter/X (Anti-Crawler)**
```bash
# Direct path: Skip regular method, use browser extraction immediately
extract_twitter_content() {
  local url="$1"
  
  # Navigate
  skill_mcp playwright browser_navigate --arguments "{\"url\": \"$url\"}"
  
  # Wait and extract with multi-selector strategy
  skill_mcp playwright browser_run_code --arguments '{
    "code": "async (page) => {
      await page.waitForTimeout(6000);
      
      // Multi-selector priority
      const selectors = [
        '\''article [data-testid=\"tweetText\"]\'',  // Primary: tweet text
        '\''div[data-testid=\"tweet\"] span\'',          // Fallback 1
        '\''[role=\"article\"]\''                   // Fallback 2
      ];
      
      let content = null;
      for (const selector of selectors) {
        try {
          const element = await page.locator(selector).first();
          if (await element.count() > 0) {
            content = await element.textContent();
            if (content && content.trim().length > 0) {
              console.log(`Found with selector: ${selector}`);
              break;
            }
          }
        } catch (e) {
          // Try next selector
        }
      }
      
      // Ultimate fallback
      if (!content) {
        content = await page.evaluate(() => {
          const articles = document.querySelectorAll("article");
          return Array.from(articles).map(a => a.innerText).join("\\n---\\n");
        });
      }
      
      return {
        url: page.url(),
        title: await page.title(),
        content: content?.trim()
      };
    }"
  }'
  
  # Save to file and add to NotebookLM
  local filename="/tmp/twitter_extract_$(date +%s).md"
  echo "$EXTRACTED_CONTENT" > "$filename"
  notebooklm source add "$filename" --notebook "$NOTEBOOK_ID"
  
  echo "⚠️ Browser extraction used (anti-crawler protection)"
}

# Usage
extract_twitter_content "https://x.com/user/status/123"
```

**Scenario 2: Open Web (Regular Method First)**
```bash
# Try regular method first
try_regular_add() {
  local url="$1"
  local result=$(notebooklm source add "$url" --notebook "$NOTEBOOK_ID" --json)
  
  local status=$(echo "$result" | jq -r '.source.status // empty')
  
  case "$status" in
    READY|PROCESSING)
      echo "✓ Regular method succeeded"
      return 0
      ;;
    FAILED|AUTH_REQUIRED)
      echo "⚠️ Failed - trying browser extraction"
      # Fall back to browser extraction
      extract_content_via_browser "$url"
      ;;
    *)
      echo "❓ Unknown status, trying browser"
      extract_content_via_browser "$url"
      ;;
  esac
}
```

### Research to Podcast (Interactive)
**Time:** 5-10 minutes total

1. `notebooklm create "Research: [topic]"` — *if fails: check auth with `notebooklm login`*
2. `notebooklm source add` for each URL/document — *if one fails: log warning, continue with others*
3. Wait for sources: `notebooklm source list --json` until all status=READY — *required before generation*
4. `notebooklm generate audio "Focus on [specific angle]"` (confirm when asked) — *if rate limited: wait 5 min, retry once*
5. Note the artifact ID returned
6. Check `notebooklm artifact list` later for status
7. `notebooklm download audio ./podcast.mp3` when complete (confirm when asked)

### Research to Podcast (Automated with Subagent)
**Time:** 5-10 minutes, but continues in background

When user wants full automation (generate and download when ready):

1. Create notebook and add sources as usual
2. Wait for sources to be ready (use `source wait` or check `source list --json`)
3. Run `notebooklm generate audio "..." --json` → parse `artifact_id` from output
4. **Spawn a background agent** using Task tool:
   ```
   Task(
     prompt="Wait for artifact {artifact_id} in notebook {notebook_id} to complete, then download.
             Use: notebooklm artifact wait {artifact_id} -n {notebook_id} --timeout 600
             Then: notebooklm download audio ./podcast.mp3 -a {artifact_id} -n {notebook_id}",
     subagent_type="general-purpose"
   )
   ```
5. Main conversation continues while agent waits

**Error handling in subagent:**
- If `artifact wait` returns exit code 2 (timeout): Report timeout, suggest checking `artifact list`
- If download fails: Check if artifact status is COMPLETED first

**Benefits:** Non-blocking, user can do other work, automatic download on completion

### Document Analysis
**Time:** 1-2 minutes

1. `notebooklm create "Analysis: [project]"`
2. `notebooklm source add ./doc.pdf` (or URLs)
3. `notebooklm ask "Summarize the key points"`
4. `notebooklm ask "What are the main arguments?"`
5. Continue chatting as needed

### Bulk Import with Progressive Fallback
**Time:** Varies by source count

1. `notebooklm create "Collection: [name]"`
2. Add multiple sources (progressive fallback applied automatically):
   ```bash
    # Always try direct addition first
    notebooklm source add "https://open-site.com/article" --notebook <id> --json
    # Monitor status: if FAILED, then use browser extraction

    # For anti-crawler URLs (fallback applied only if direct fails):
    # Twitter/X example
    notebooklm source add "https://x.com/user/status/123" --notebook <id> --json
    # If returns FAILED:
    skill_mcp playwright browser_navigate --arguments '{"url": "https://x.com/user/status/123"}'
    skill_mcp playwright browser_run_code --arguments '{...extract code...}'
    echo "# Extracted content" > /tmp/twitter_content.md
    notebooklm source add /tmp/twitter_content.md --notebook <id>
    ```
3. `notebooklm source list` to verify all sources status

**Source limits:** Max 50 sources per notebook
**Supported types:** PDFs, YouTube URLs, web URLs, Google Docs, text files

### Deep Web Research (Subagent Pattern)
**Time:** 2-5 minutes, runs in background

1. Create notebook: `notebooklm create "Research: [topic]"`
2. Start deep research (non-blocking):
   ```bash
   notebooklm source add-research "topic query" --mode deep --no-wait
   ```
3. **Spawn a background agent** to wait and import:
   ```
   Task(
     prompt="Wait for research in notebook {notebook_id} to complete and import sources.
             Use: notebooklm research wait -n {notebook_id} --import-all --timeout 300
             Report how many sources were imported.",
     subagent_type="general-purpose"
   )
   ```
4. Main conversation continues while agent waits
5. When agent completes, sources are imported automatically

**Alternative (blocking):** For simple cases, omit `--no-wait`:
```bash
notebooklm source add-research "topic" --mode deep --import-all
# Blocks for up to 5 minutes
```

**When to use each mode:**
- `--mode fast`: Specific topic, quick overview needed (5-10 sources, seconds)
- `--mode deep`: Broad topic, comprehensive analysis needed (20+ sources, 2-5 min)

**Research sources:**
- `--from web`: Search the web (default)
- `--from drive`: Search Google Drive

## Output Style

**Progress updates:** Brief status for each step
- "Creating notebook 'Research: AI'..."
- "Adding source: https://example.com..."
- "Starting audio generation... (task ID: abc123)"

**Fire-and-forget for long operations:**
- Start generation, return artifact ID immediately
- Do NOT poll or wait in main conversation - generation