---
name: Gallery Agent Management
description: Protocols for managing the Google Service Account credentials and onboarding new photographers/galleries.
---

# Gallery Agent Management

This skill outlines the protocols for managing "The Gallery Agent" (the Google Service Account that powers the website) and how to onboard new photographers.

## 1. Current Architecture: "The Gallery Agent"

The website uses a **Single Service Account** architecture.
- **Identity**: `the-gallery-agent@the-lost-and-unf-1737406545588.iam.gserviceaccount.com`
- **Role**: This "robot user" acts as the bridge between your website and Google Drive.
- **Access**: It can *only* see folders that are explicitly shared with it.

### Credential Management

If you need to rotate keys or switch accounts in the future, use the provided scripts in the project root:

1.  **Switch/Update Credentials**:
    ```bash
    ./scripts/switch-google-account.sh
    ```
    *Use this if you have a new JSON key file and want to paste the key securely.*

2.  **Update from File (Automated)**:
    ```bash
    npx tsx scripts/update-google-creds-from-file.ts <path-to-json-file>
    ```
    *Use this if you have the JSON file downloaded and want to apply it instantly without copy-pasting.*

---

## 2. Protocol: Onboarding New Photographers

**Scenario**: You have a new photographer, "Alex", who wants to host a gallery.

### The "Service Account" Method (Current Standard)
Since we use a global agent, Alex does **not** need to give you their password or connect their account via OAuth.

**Protocol:**
1.  **Alex** creates a folder in their Google Drive (e.g., "Alex's Portfolio").
2.  **Alex** adds photos to that folder.
3.  **Alex** clicks "Share" on that folder and adds:
    `the-gallery-agent@the-lost-and-unf-1737406545588.iam.gserviceaccount.com`
    *Role: Viewer (or Editor)*.
4.  **You (Admin)** go to the **Admin Dashboard**.
5.  **You** create a new Gallery.
    *   **Name**: "Alex's Portfolio"
    *   **Folder ID**: (Get the ID from Alex's folder link).
6.  **You** click **"Test Connection"**.
    *   *Result*: The Agent sees the folder (because Alex shared it) and syncs the photos.

**Pros**: Secure, no code changes, no complex login flows for Alex.
**Cons**: Requires Alex to manually share the folder with a specific email address.

---

## 3. Future Roadmap: "Connect Google Drive" (OAuth)

**Scenario**: You want Alex to log in to your dashboard and click "Connect my Drive" to select folders seamlessly.

To implement this later, you would move from a **Service Account** to an **OAuth 2.0 App**.

### Implementation Overview
1.  **Google Cloud Console**:
    *   Create an OAuth Client ID.
    *   Submit app for "Verification" (required for access to sensitive scopes like `drive.readonly`).
2.  **Frontend**:
    *   Add a "Sign in with Google" button.
    *   Request `drive.readonly` scope.
3.  **Backend**:
    *   Store *Alex's* Access Token and Refresh Token in the database (encrypted).
    *   When syncing "Alex's Gallery", use *Alex's Token* instead of the Service Account Key.

**Why wait?**
*   Requires Google Security Assessment (can cost money/time).
*   Requires complex token management (refreshing tokens, handling revoked access).
*   The current Service Account method scales infinitely as long as people share their folders.
