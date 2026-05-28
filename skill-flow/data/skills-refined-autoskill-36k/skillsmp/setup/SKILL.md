---
name: setup
description: Interactive setup guide for Grant Tracker. Walks through GCP project creation, OAuth configuration, Google Sheets setup, and dev environment. Use when setting up Grant Tracker for the first time or configuring Google Cloud.
---

# Setup Skill

Interactive setup guide for Grant Tracker. Walks through the complete setup process from clone to running application.

## Instructions

When this skill is invoked, guide the user through the Grant Tracker setup process interactively. Check the current state before each step and skip steps that are already complete.

### Phase 1: Prerequisites Check

1. **Check Docker is running:**
   ```bash
   docker info > /dev/null 2>&1
   ```
   If this fails, tell the user to start Docker Desktop and wait for it to be ready.

2. **Check gcp-config.env exists:**
   ```bash
   test -f scripts/gcp-config.env
   ```
   If missing, tell the user:
   - Copy the template: `cp scripts/gcp-config.env.example scripts/gcp-config.env`
   - Edit it with their values (explain each field)
   - Wait for them to confirm before continuing

### Phase 2: Container Setup

3. **Check if container image exists:**
   ```bash
   docker images grant-tracker-dev --format "{{.Repository}}"
   ```
   If empty, run `./gt build` and show progress.

4. **Verify container works:**
   ```bash
   ./gt run echo "Container OK"
   ```

### Phase 3: GCP Authentication

5. **Check if already authenticated:**
   ```bash
   ls .gcloud/credentials.db 2>/dev/null
   ```

   If the file doesn't exist, the user needs to authenticate.

   **Important:** The `./gt gcp auth` command requires an interactive terminal. Tell the user:

   > Please run this command in your terminal:
   > ```
   > ./gt gcp auth
   > ```
   > It will show a URL. Open it in your browser, sign in, and paste the verification code back.

   Wait for them to confirm they've completed authentication.

   Credentials are stored in the local `.gcloud/` directory (gitignored).

### Phase 4: GCP Project Setup

6. **Check if project exists:**
   First read the project ID from config:
   ```bash
   grep GCP_PROJECT_ID scripts/gcp-config.env | cut -d= -f2 | tr -d '"'
   ```
   Then run setup (it will skip if project exists):
   ```bash
   ./gt gcp setup
   ```

7. **Verify APIs are enabled:**
   The setup script enables Sheets, Drive, and Picker APIs. Check output for success messages.

### Phase 5: OAuth Configuration (Manual Steps)

8. **Guide through OAuth consent screen:**

   Get the project ID and construct the URL:
   ```
   https://console.cloud.google.com/apis/credentials/consent?project=PROJECT_ID
   ```

   Tell the user to:
   - Open the URL
   - Select External (or Internal for Workspace)
   - Set App name to "Grant Tracker"
   - Add their email for support and developer contact
   - Add scopes: `drive.file`, `userinfo.email`
   - Add themselves as a test user

   **Note on scopes:** We use `drive.file` instead of `spreadsheets` because it provides access only to files the app creates or that the user explicitly selects via Picker. This is more privacy-respecting.

   Ask them to confirm when done.

9. **Guide through OAuth client creation:**

   URL: `https://console.cloud.google.com/apis/credentials?project=PROJECT_ID`

   Tell the user to:
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Web application"
   - Name it "Grant Tracker"
   - Add authorized origin: `http://localhost:5173`
   - Click Create
   - Copy the Client ID

   Ask them to paste the Client ID so you can help create the env file.

### Phase 6: Environment Configuration

10. **Create web/.env.local:**

    Once you have the Client ID, create the file:
    ```bash
    echo "VITE_GOOGLE_CLIENT_ID=CLIENT_ID_HERE" > web/.env.local
    ```

    **Note:** No spreadsheet ID is needed. Users will select or create their spreadsheet through the app's UI using Google Picker. The spreadsheet ID is stored in localStorage per user/browser.

    Show the user what was created.

### Phase 7: Verification

11. **Start the dev server:**
    ```bash
    ./gt start
    ```

    Tell the user to open http://localhost:5173.

    To verify it's running, you can use:
    ```bash
    sleep 5 && curl -s http://localhost:5173 | head -10
    ```

12. **Verify everything works:**

    Ask the user to confirm:
    - Can they see the sign-in button?
    - Does Google OAuth flow work?
    - Does the app load without errors?

    If there are issues, help troubleshoot based on error messages.

### Completion

When all steps are done, summarize what was set up:
- GCP project: PROJECT_ID
- APIs enabled: Sheets, Drive, Picker
- OAuth client configured
- Dev server running

Mention next steps:
- On first use, the app will prompt to select or create a spreadsheet
- Review docs/DESIGN.md for the data model
- See mockups/ for UI direction
- For production deployment, see the "Production Deployment" section in docs/SETUP.md

## State Tracking

Track progress using the TodoWrite tool. Create todos for each phase and mark them complete as you go. This helps if the user needs to pause and resume later.

## Error Handling

Common issues and how to help:

**Docker not running:**
- macOS: "Open Docker Desktop and wait for it to start"
- Check with `docker info`

**gcloud auth requires interactive terminal:**
- The `./gt gcp auth` command cannot be run non-interactively
- Tell the user to run it directly in their terminal
- Credentials are stored in `.gcloud/` directory

**"Not logged in to gcloud" after auth:**
- Check that `.gcloud/credentials.db` exists
- If not, the user needs to run `./gt gcp auth` again
- Make sure they're copying the full auth code

**Project creation fails (already exists):**
- Either the project ID is taken globally, or they already created it
- The setup script will skip creation if project exists
- Suggest a different project ID if needed

**OAuth errors (redirect_uri_mismatch):**
- Verify localhost:5173 is in authorized origins
- Check for typos in the client ID
- Make sure they saved the OAuth client configuration

**Spreadsheet access:**
- Users select spreadsheets via Picker or create new ones
- The `drive.file` scope grants access to selected/created files
- No need to manually share spreadsheets if using Picker flow
