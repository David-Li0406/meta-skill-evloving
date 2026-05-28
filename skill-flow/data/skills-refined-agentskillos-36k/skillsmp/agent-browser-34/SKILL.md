---
name: agent-browser
description: "Browser automation using Vercel's agent-browser CLI. Use for web interaction, form filling, screenshots, scraping, and UI/backend verification. Supports ref-based selection, parallel sessions, and headed debugging. Includes verification workflows with confidence assessment. Triggers on: browse website, fill form, click button, take screenshot, scrape page, web automation, UI verification."
---

# agent-browser: CLI Browser Automation

Vercel's headless browser automation CLI designed for AI agents. Uses ref-based selection (@e1, @e2) from accessibility snapshots.

## Setup Check

```bash
# Check installation
command -v agent-browser >/dev/null 2>&1 && echo "Installed" || echo "NOT INSTALLED - run: npm install -g agent-browser && agent-browser install"
```

### Install if Needed

```bash
npm install -g agent-browser
agent-browser install  # Downloads Chromium
```

## Core Workflow

**The snapshot + ref pattern is optimal for LLMs:**

1. **Navigate** to URL
2. **Snapshot** to get interactive elements with refs
3. **Interact** using refs (@e1, @e2, etc.)
4. **Re-snapshot** after navigation or DOM changes

```bash
# Step 1: Open URL
agent-browser open https://example.com

# Step 2: Get interactive elements with refs
agent-browser snapshot -i

# Step 3: Interact using refs
agent-browser click @e1
agent-browser fill @e2 "search query"

# Step 4: Re-snapshot after changes
agent-browser snapshot -i
```

## Verification Capabilities

### What You CAN Verify (High Confidence)

- Element existence (by test ID, role, or text)
- Text content of elements
- Page titles and headings
- Form field presence and labels
- Button clicks triggering navigation
- Form submission behavior
- Error message display
- Console errors

### What You CANNOT Verify (Flag for Human)

- Layout and spacing
- Element positioning ("is button centered?")
- Visual alignment ("do these items line up?")
- Responsive behavior at breakpoints
- Color and styling
- Overall aesthetics
- "Does this look right?"

**ALWAYS** flag these for human review when UI is involved.

## Command Reference

### Navigation

```bash
agent-browser open <url>       # Navigate to URL
agent-browser back             # Go back
agent-browser forward          # Go forward
agent-browser reload           # Reload page
agent-browser close            # Close browser
```

### Snapshots (Essential for AI)

```bash
agent-browser snapshot              # Full accessibility tree
agent-browser snapshot -i           # Interactive elements only (recommended)
agent-browser snapshot -i --json    # JSON output for parsing
agent-browser snapshot -c           # Compact (remove empty elements)
agent-browser snapshot -d 3         # Limit depth
```

### Interactions

```bash
agent-browser click @e1                    # Click element
agent-browser dblclick @e1                 # Double-click
agent-browser fill @e1 "text"              # Clear and fill input
agent-browser type @e1 "text"              # Type without clearing
agent-browser press Enter                  # Press key
agent-browser hover @e1                    # Hover element
agent-browser check @e1                    # Check checkbox
agent-browser uncheck @e1                  # Uncheck checkbox
agent-browser select @e1 "option"          # Select dropdown option
agent-browser scroll down 500              # Scroll (up/down/left/right)
agent-browser scrollintoview @e1           # Scroll element into view
```

### Get Information

```bash
agent-browser get text @e1          # Get element text
agent-browser get html @e1          # Get element HTML
agent-browser get value @e1         # Get input value
agent-browser get attr href @e1     # Get attribute
agent-browser get title             # Get page title
agent-browser get url               # Get current URL
agent-browser get count "button"    # Count matching elements
```

### Screenshots & PDFs

```bash
agent-browser screenshot                      # Viewport screenshot
agent-browser screenshot --full               # Full page
agent-browser screenshot output.png           # Save to file
agent-browser screenshot --full output.png    # Full page to file
agent-browser pdf output.pdf                  # Save as PDF
```

### Wait

```bash
agent-browser wait @e1              # Wait for element
agent-browser wait 2000             # Wait milliseconds
agent-browser wait "text"           # Wait for text to appear
agent-browser wait --url "**/path"  # Wait for URL pattern
```

### Execute JavaScript

```bash
agent-browser execute "localStorage.setItem('key', 'value')"
agent-browser execute "document.querySelector('.btn').click()"
```

### Console Errors

```bash
agent-browser errors                # Get console errors
```

## Semantic Locators (Alternative to Refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign up" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find placeholder "Search..." fill "query"
```

## Sessions (Parallel Browsers)

```bash
# Run multiple independent browser sessions
agent-browser --session browser1 open https://site1.com
agent-browser --session browser2 open https://site2.com

# List active sessions
agent-browser session list
```

## Debug Mode

```bash
# Run with visible browser window
agent-browser --headed open https://example.com
agent-browser --headed snapshot -i
agent-browser --headed click @e1
```

Use headed mode when:
- Debugging automation issues
- Testing apps with popups
- User needs to see what's happening

## JSON Output

Add `--json` for structured output:

```bash
agent-browser snapshot -i --json
```

Returns:
```json
{
  "success": true,
  "data": {
    "refs": {
      "e1": {"name": "Submit", "role": "button"},
      "e2": {"name": "Email", "role": "textbox"}
    },
    "snapshot": "- button \"Submit\" [ref=e1]\n- textbox \"Email\" [ref=e2]"
  }
}
```

## Verification Workflow

### 1. Navigate to Page

```bash
agent-browser open {url}
```

### 2. Capture Initial Snapshot

```bash
agent-browser snapshot -i
```

Parse the refs for elements to verify.

### 3. Verify Element Existence

For each expected element:
```bash
agent-browser is visible @{ref}
```

### 4. Verify Text Content

```bash
agent-browser get text @{ref}
```

Compare against expected content.

### 5. Test Interactions

```bash
# Click buttons
agent-browser click @{ref}

# Fill forms
agent-browser fill @{ref} "{value}"

# Wait for navigation
agent-browser wait --url "{pattern}"
```

### 6. Capture Screenshots

```bash
agent-browser screenshot .unitwork/verify/{name}.png
```

Save to `.unitwork/verify/` for human review.

### 7. Check for Errors

```bash
agent-browser errors
```

Report any console errors.

## Backend Testing Setup

When verifying backend changes (API endpoints, services, etc.):

### 1. Determine Target App URL

The app URL depends on the repository being tested:

| Repository | App URL |
|------------|---------|
| `relevance-app` (Vue frontend) | `https://app-development.relevanceai.com` |
| `relevance-chat-app` (React Native) | `https://chat-development.relevanceai.com` |
| Other/Unknown | Ask user for URL |

Check the current repo name from git remote or package.json to determine which URL to use.

### 2. Determine Backend Port

The backend port is NOT always 8000. Determine the correct port by:
1. **If running the backend server yourself** - Use the port your server is running on
2. **If user specified a port** - Use the user-specified port
3. **Default fallback** - Port 8000

### 3. Confirm Backend Server is Running

Before browser testing, inform the user and wait for confirmation if needed:

> "I'll verify the backend changes through the browser. Please ensure your local backend server is running. Once ready, I'll configure the browser to use your local backend at http://localhost:{PORT}."

### 4. Configure localStorage for Local Backend

After opening the browser, set the API URL to point to local backend:

```bash
# Open the target app
agent-browser open https://app-development.relevanceai.com

# Execute JavaScript to set localStorage
agent-browser execute "localStorage.setItem('api-url', 'http://localhost:{PORT}')"

# Reload to apply the setting
agent-browser reload

# Now proceed with verification
agent-browser snapshot -i
```

## Authentication Handling

### Detecting Login Required

After navigating to app:
```bash
agent-browser snapshot -i
# Look for: login form, sign-in button, auth-related elements
```

### Strategy Selection

| Scenario | Strategy |
|----------|----------|
| Login form detected, no credentials | Pause for user login |
| Login form detected, .unitwork/.env exists | Attempt automated login |
| OAuth/SSO redirect | Open headed mode, pause for user |
| 2FA required | Pause for user |

### Option 1: Pause for Manual Login

If login is required and the agent cannot authenticate:

> "I've opened the app but it requires authentication. Please log in manually in the browser window. Let me know when you're logged in and I'll continue with verification."

Wait for user confirmation before proceeding.

### Option 2: Automated Login with .unitwork/.env

If the user wants automated login:

#### Environment Setup Workflow

1. **Create credentials file:**
```bash
# Create .unitwork/.env file if not exists
mkdir -p .unitwork
touch .unitwork/.env

# Ensure .unitwork is gitignored
grep -q "^\.unitwork" .gitignore 2>/dev/null || echo ".unitwork/" >> .gitignore
```

2. **Open for user to fill:**
```bash
# Open in default text editor (macOS)
open -e .unitwork/.env

# Or use VS Code if available
code .unitwork/.env 2>/dev/null || open -e .unitwork/.env
```

3. **Prompt user:**
> "I've opened `.unitwork/.env` in your text editor. Please add your login credentials:
> ```
> TEST_EMAIL=your-email@example.com
> TEST_PASSWORD=your-password
> ```
> Let me know when ready."

4. **Read and use:**
```bash
# Source credentials
source .unitwork/.env

# Use in automation
agent-browser fill @email "$TEST_EMAIL"
agent-browser fill @password "$TEST_PASSWORD"
agent-browser click @login-button
```

### Authentication Workflow Summary

1. Navigate to app URL
2. Check if login page is displayed (look for login form elements)
3. If login required:
   - Check if `.unitwork/.env` file exists with credentials -> attempt automated login
   - If no credentials -> pause and ask user to login manually
4. Wait for successful authentication (check for dashboard/home page elements)
5. Continue with verification

## Popup Handling

Modern web apps often use popups for OAuth, payment, or confirmations.

### Configure Browser for Popups

For apps with known popups, use headed mode:

```bash
agent-browser --headed open https://app.example.com
```

This lets the user see and interact with popups while the agent handles the main window.

### When Popup Appears

**OAuth/Social login popup:**
- Pause and ask user: "A login popup appeared. Please complete authentication in the popup window."
- Wait for popup to close
- Re-snapshot main window

**Payment popup (Stripe, PayPal):**
- Do NOT attempt to automate - security risk
- Pause: "Payment popup detected. Please complete manually."

**Confirmation modals:**
- These are usually in-page, not true popups
- Snapshot should detect modal elements
- Interact normally with refs

### Detection Pattern

```bash
# After click that might trigger popup
agent-browser click @oauth-button

# Wait briefly
agent-browser wait 1000

# Check if we're on a new page/popup
agent-browser get url
# If URL changed to OAuth provider -> pause for user
```

## Output Format

```markdown
## UI Verification Results

### Page: {page_name}

**Screenshots:**
- {screenshot_1.png}
- {screenshot_2.png}

**Verified (high confidence):**
- Login form exists with correct test ID
- Page title is "Sign In"
- Email and password fields accept input
- Form submits and redirects to /dashboard
- No console errors

**Cannot Verify (needs human review):**
- Form field spacing and alignment
- Button positioning relative to form
- Overall visual balance of page
- Responsive behavior at mobile breakpoints

**Observations (with uncertainty):**
Login button appears in the lower portion of the form area.
Text reads "Sign In". Background appears to be a light color.

**Human verification needed for:**
- Layout positioning matches design
- Visual hierarchy is correct
- Spacing/padding feels right
- Mobile responsiveness
```

## Confidence Assessment

**UI verification confidence ceiling: 70-80%**

Because:
- Cannot verify spatial relationships
- Cannot judge aesthetics
- Cannot confirm responsive behavior
- Screenshots help but require human eyes

**ALWAYS set confidence below 95% for UI work and flag for human review.**

Start at 100%, subtract:
- -5% for each untested edge case
- -20% if UI layout changes
- -10% if complex state management
- -15% if external API integration

## Important Rules

1. **ALWAYS** capture screenshots
2. **NEVER** claim confidence above 80% for UI
3. **ALWAYS** list what needs human review
4. **DOCUMENT** element refs used
5. **REPORT** console errors prominently
6. **TIMEOUT** gracefully after 60 seconds
7. **NEVER** use Playwright MCP - use agent-browser CLI

## Examples

### Login Flow

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
# Output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Sign in" [ref=e3]
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait 2000
agent-browser screenshot .unitwork/verify/after-login.png
agent-browser snapshot -i  # Verify logged in
```

### Backend Verification

```bash
# Configure for local backend
agent-browser open https://app-development.relevanceai.com
agent-browser execute "localStorage.setItem('api-url', 'http://localhost:8000')"
agent-browser reload

# Login and test
agent-browser snapshot -i
agent-browser fill @email "test@example.com"
agent-browser fill @password "testpass"
agent-browser click @login
agent-browser wait --url "**/dashboard"

# Verify backend response reflected in UI
agent-browser snapshot -i
agent-browser get text @user-name  # Should show user from local backend
agent-browser screenshot .unitwork/verify/backend-test.png
```

### Form Filling with Verification

```bash
agent-browser open https://forms.example.com
agent-browser snapshot -i
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser select @e3 "United States"
agent-browser check @e4  # Agree to terms
agent-browser screenshot .unitwork/verify/form-filled.png
agent-browser click @e5  # Submit button
agent-browser wait 2000
agent-browser snapshot -i  # Check for success message
agent-browser screenshot .unitwork/verify/form-submitted.png
agent-browser errors  # Check for console errors
```

## vs Playwright MCP

| Feature | agent-browser (CLI) | Playwright MCP |
|---------|---------------------|----------------|
| Interface | Bash commands | MCP tools |
| Selection | Refs (@e1) | Refs (e1) |
| Output | Text/JSON | Tool responses |
| Parallel | Sessions | Tabs |
| Best for | Quick automation | Tool integration |

**Use agent-browser when:**
- You prefer Bash-based workflows
- You want simpler CLI commands
- You need quick one-off automation

**Use Playwright MCP when:**
- You need deep MCP tool integration
- You want tool-based responses
- You're building complex automation
