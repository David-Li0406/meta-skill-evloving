---
name: browser-automate
description: Automate web browser interactions using agent-browser for testing, research, and data extraction
allowed-tools:
  - Bash
  - WebFetch
  - Read
  - Write
  - Glob
  - Grep
---

<objective>
Automate web browser interactions using agent-browser CLI tool.

Enables AI agents to:
- Navigate and interact with web pages reliably
- Extract data from web applications
- Test web interfaces and workflows
- Research web-based products and competitors
- Automate form submissions and user flows
- Capture screenshots and documentation

Uses agent-browser's AI-friendly ref system for deterministic element selection.
</objective>

<execution_context>
@~/.claude/ag4one/skills/agent-browser.md
@~/.claude/ag4one/templates/browser-automation/
</execution_context>

<context>
@.planning/PROJECT.md (if exists)
Current working directory for file outputs
</context>

<process>

<step name="validate_setup">
```bash
# Check if agent-browser is installed
if ! command -v agent-browser &> /dev/null; then
    echo "ERROR: agent-browser not found. Install with: npm install -g agent-browser"
    exit 1
fi

# Create output directory if needed
mkdir -p .automation/browser
mkdir -p .automation/screenshots
mkdir -p .automation/data

echo "agent-browser version: $(agent-browser --version 2>/dev/null || echo 'unknown')"
```
</step>

<step name="get_user_intent">
Use AskUserQuestion:
- header: "Browser automation goal"
- question: "What do you want to accomplish with browser automation?"
- options:
  - "Test web application" — Automated testing of web interfaces
  - "Research competitor" — Analyze competitor websites and features  
  - "Extract data" — Scrape data from web pages
  - "Automate workflow" — Automate repetitive web tasks
  - "Documentation" — Capture screenshots and documentation
  - "Custom" — Specify your own automation goal

Based on selection, ask follow-up questions about:
- Target URL(s)
- Specific actions to perform
- Data to extract
- Output format preferences
</step>

<step name="setup_session">
```bash
# Initialize browser session
BROWSER_SESSION="automation_$(date +%s)"
echo "Session: $BROWSER_SESSION" > .automation/browser/session.txt

# Start browser in appropriate mode
if [[ "$AUTOMATION_MODE" == "debug" ]]; then
    agent-browser open "$TARGET_URL" --headed
else
    agent-browser open "$TARGET_URL"
fi

echo "Browser opened for: $TARGET_URL"
```
</step>

<step name="initial_snapshot">
```bash
# Get initial page state
agent-browser snapshot -i --json > .automation/browser/initial_snapshot.json
agent-browser screenshot .automation/screenshots/initial.png

echo "Initial snapshot captured"
echo "Page title: $(agent-browser get title --json)"
echo "Current URL: $(agent-browser get url --json)"
```
</step>

<step name="execute_automation">
Based on user intent, execute appropriate automation pattern:

**For Testing:**
```bash
# Navigate through test flow
agent-browser snapshot -i --json > .automation/browser/step1_snapshot.json
# Parse snapshot to identify refs for interaction
agent-browser click @e2  # Example: click login button
agent-browser wait --text "Welcome"
agent-browser fill @e5 "test@example.com"
agent-browser fill @e6 "password123"
agent-browser click @e7  # Example: submit form
```

**For Research:**
```bash
# Capture page structure and content
agent-browser snapshot -i --json > .automation/browser/research_snapshot.json
agent-browser get text "body" --json > .automation/data/page_content.json
agent-browser screenshot .automation/screenshots/full_page.png --full
```

**For Data Extraction:**
```bash
# Extract specific data elements
agent-browser get text "[data-product]" --json > .automation/browser/products.json
agent-browser get attr "href" "[data-link]" --json > .automation/browser/links.json
```

**For Workflow Automation:**
```bash
# Execute multi-step process
agent-browser fill @e3 "$USERNAME"
agent-browser fill @e4 "$PASSWORD"
agent-browser click @e5
agent-browser wait --url "**/dashboard"
agent-browser click @e10  # Navigate to target section
```
</step>

<step name="capture_results">
```bash
# Final state capture
agent-browser snapshot -i --json > .automation/browser/final_snapshot.json
agent-browser screenshot .automation/screenshots/final.png

# Compile automation results
cat > .automation/browser/results.md << EOF
# Browser Automation Results

## Session
- Session ID: $BROWSER_SESSION
- Target URL: $TARGET_URL
- Timestamp: $(date)

## Actions Performed
$(cat .automation/browser/session.log 2>/dev/null || echo "No action log found")

## Screenshots
- Initial: .automation/screenshots/initial.png
- Final: .automation/screenshots/final.png

## Data Captured
- Initial snapshot: .automation/browser/initial_snapshot.json
- Final snapshot: .automation/browser/final_snapshot.json
- Extracted data: .automation/data/

## Next Steps
- Review screenshots and data
- Integrate findings into project documentation
- Schedule regular automation if needed
EOF

echo "Automation results saved to .automation/browser/results.md"
```
</step>

<step name="cleanup">
```bash
# Close browser session
agent-browser close

# Organize results
echo "Session completed: $BROWSER_SESSION"
echo "Results available in .automation/ directory"
```
</step>

<step name="done">
```
Browser automation complete:

- Screenshots: .automation/screenshots/
- Snapshots: .automation/browser/
- Data: .automation/data/
- Summary: .automation/browser/results.md

---

## ▶ Next Up

**Research phase** — Use automation data for project research

`/ag4:research-phase`

<sub>`/clear` first → fresh context window</sub>

**Flow:** browser-automate → research-phase → define-requirements

---
```
</step>

</process>

<when_to_use>
**Use browser-automate for:**
- Testing web applications and user interfaces
- Researching competitor websites and features
- Extracting structured data from web pages
- Automating repetitive web workflows
- Creating documentation with screenshots
- Validating web-based integrations

**Skip browser-automate for:**
- API testing (use API tools instead)
- Local application testing (use appropriate tools)
- Simple HTTP requests (use curl/fetch)
</when_to_use>

<success_criteria>
- [ ] agent-browser installed and validated
- [ ] User intent captured and confirmed
- [ ] Browser session started successfully
- [ ] Initial snapshot captured
- [ ] Automation pattern executed based on intent
- [ ] Results captured and saved
- [ ] Screenshots and data organized
- [ ] Browser session closed cleanly
- [ ] User understands next steps
</success_criteria>