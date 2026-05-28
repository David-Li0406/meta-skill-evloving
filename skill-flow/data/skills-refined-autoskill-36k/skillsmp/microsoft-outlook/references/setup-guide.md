# Microsoft Entra App Registration Guide

Complete guide for setting up Microsoft API credentials required for the microsoft-outlook skill.

## Step 1: Access Microsoft Entra Admin Center

1. Go to [Microsoft Entra admin center](https://entra.microsoft.com/)
2. Sign in with your Microsoft account (personal or work/school)
3. Navigate to **Identity** > **Applications** > **App registrations**

## Step 2: Register a New Application

1. Click **New registration**
2. Configure the application:
   - **Name**: `microsoft-skill-cli` (or any descriptive name)
   - **Supported account types**: Select **"Accounts in any organizational directory and personal Microsoft accounts"** (Multitenant + Personal)
   - **Redirect URI**:
     - Platform: **Web**
     - URI: `http://localhost:3000/callback`
3. Click **Register**

## Step 3: Copy Application ID

After registration, you'll see the **Overview** page:

1. Copy the **Application (client) ID** - this is your `client_id`
2. Save it securely (you'll need it for setup)

## Step 4: Create Client Secret

1. In the left sidebar, click **Certificates & secrets**
2. Under **Client secrets**, click **New client secret**
3. Configure:
   - **Description**: `CLI access` (or any description)
   - **Expires**: Choose appropriate duration (24 months recommended)
4. Click **Add**
5. **IMPORTANT**: Copy the **Value** immediately - this is your `client_secret`
   - This value is only shown once!
   - Store it securely

## Step 5: Configure API Permissions

1. In the left sidebar, click **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add these permissions:
   - `User.Read` - Read user profile
   - `Mail.Read` - Read user mail
   - `offline_access` - Maintain access (for refresh tokens)
6. Click **Add permissions**

### Admin Consent (Optional)

For personal Microsoft accounts, users consent during login. For organizational accounts:
- Click **Grant admin consent for [organization]** if you have admin privileges
- Otherwise, users will be prompted to consent on first login

## Step 6: Run Setup

With your credentials ready:

```bash
pnpm tsx skills/microsoft-outlook/scripts/microsoft.ts setup
```

Choose your storage method:
- **1Password** (recommended): Store credentials in 1Password at:
  - `op://Personal/Microsoft Client ID/notesPlain`
  - `op://Personal/Microsoft Client Secret/notesPlain`
- **Manual**: Enter credentials directly, stored at `~/.config/microsoft-skill/credentials.json`

## Credential Storage Locations

### 1Password References

If using 1Password CLI (`op`), create two items in your vault:
- **Microsoft Client ID** - Store client_id in Notes field
- **Microsoft Client Secret** - Store client_secret in Notes field

The skill reads from:
```
op://Personal/Microsoft Client ID/notesPlain
op://Personal/Microsoft Client Secret/notesPlain
```

### Local File Storage

Credentials stored at:
```
~/.config/microsoft-skill/credentials.json
```

Format:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

## Token Storage

After authentication, tokens are stored:

- **Per-project** (default): `.claude/microsoft-skill.local.json`
- **Global** (with `--global`): `~/.config/microsoft-skill/tokens.json`

The `.claude/*.local.*` pattern should be in `.gitignore` to prevent committing tokens.

## Troubleshooting

### "AADSTS65001: User has not consented"

The user needs to grant permissions. This happens automatically on first login for personal accounts.

### "AADSTS700016: Application not found"

Check that:
- Client ID is correct
- App registration exists in the correct tenant
- "Multitenant + Personal" is selected for account types

### "AADSTS7000218: Invalid client secret"

The client secret may have:
- Expired
- Been deleted
- Been copied incorrectly (use the Value, not the Secret ID)

Generate a new secret in Entra admin center.

### "Redirect URI mismatch"

Ensure the redirect URI in Entra matches exactly:
```
http://localhost:3000/callback
```

Platform must be **Web** (not SPA or Mobile).

## Security Best Practices

1. **Never commit credentials** - Use 1Password or ensure credentials file is outside repo
2. **Use per-project tokens** - Allows different accounts per project
3. **Rotate secrets periodically** - Create new secrets before expiration
4. **Use minimal permissions** - Only request Mail.Read, not Mail.ReadWrite
5. **Add `.claude/*.local.*` to `.gitignore`** - Prevents token commits
