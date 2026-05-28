# GitHub Secrets Setup for Play Store Deployment

## Overview

GitHub Actions requires several secrets to deploy your app to the Play Store. This guide explains how to set up each secret.

## Prerequisites

- Admin access to GitHub repository
- Service account JSON file from android-playstore-setup
- Production keystore from android-release-build-setup

## Required Secrets

Navigate to: **Your Repository → Settings → Secrets and variables → Actions → New repository secret**

---

### 1. SERVICE_ACCOUNT_JSON_PLAINTEXT

**What it is:** Complete plaintext contents of the Google Cloud service account JSON file (not base64 encoded)

**How to get the value:**

1. Locate the JSON file downloaded during android-playstore-setup
   - Filename: `service-account.json` (or similar)
   - Location: Where you saved it securely

2. Open the file in a text editor

3. Copy the **ENTIRE** contents
   - From the first `{` to the last `}`
   - Include all whitespace and newlines
   - Should be ~2,400 characters

4. In GitHub:
   - Name: `SERVICE_ACCOUNT_JSON_PLAINTEXT`
   - Value: Paste the copied JSON (plaintext, not base64 encoded)

**Example format (DO NOT use this, use your actual file):**
```json
{
  "type": "service_account",
  "project_id": "your-gcp-project",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "playstore-deploy@your-project.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

**Verification:**
- ✅ Starts with `{` and ends with `}`
- ✅ Contains `"type": "service_account"`
- ✅ Contains `"client_email"` with @...iam.gserviceaccount.com
- ✅ Contains `"private_key"` section with BEGIN/END markers
- ✅ Valid JSON (no syntax errors)

---

### 2. SIGNING_KEY_STORE_BASE64

**What it is:** Your production keystore file encoded as base64

**How to get the value:**

**On Linux/macOS:**
```bash
base64 -w 0 keystores/production-release.jks
```

**On macOS (alternative):**
```bash
base64 -i keystores/production-release.jks | tr -d '\n'
```

**On Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('keystores\production-release.jks'))
```

**On Windows (Git Bash):**
```bash
base64 -w 0 keystores/production-release.jks
```

**Steps:**
1. Navigate to your project directory
2. Run the appropriate command above
3. Copy the output (one long string, no line breaks)
4. In GitHub:
   - Name: `SIGNING_KEY_STORE_BASE64`
   - Value: Paste the base64 string

**Verification:**
- ✅ String is very long (~5,000+ characters)
- ✅ Contains only alphanumeric characters, +, /, and = (padding)
- ✅ No line breaks or spaces

**Common mistakes:**
- ❌ Including `-----BEGIN CERTIFICATE-----` headers (wrong encoding method)
- ❌ Line breaks in the base64 string
- ❌ Encoding the wrong file (debug.keystore instead of production)

---

### 3. SIGNING_KEY_ALIAS

**What it is:** The alias used when creating your production keystore

**How to get the value:**

From `keystores/KEYSTORE_INFO.txt`:
```
Alias: upload
```

Or list keystore contents:
```bash
keytool -list -v -keystore keystores/production-release.jks
# Look for "Alias name:"
```

**Typical values:**
- `upload` (recommended by Google Play)
- `release`
- `production`
- `key0` (default for some tools)

**Steps:**
1. Check your keystore info file
2. In GitHub:
   - Name: `SIGNING_KEY_ALIAS`
   - Value: The alias (e.g., `upload`)

**Verification:**
- ✅ Matches the alias in your keystore
- ✅ Case-sensitive (use exact match)

---

### 4. SIGNING_STORE_PASSWORD

**What it is:** Password for the keystore file itself

**How to get the value:**

From `keystores/KEYSTORE_INFO.txt`:
```
Store Password: your-store-password
```

**Steps:**
1. Get password from secure location (password manager, keystore info file)
2. In GitHub:
   - Name: `SIGNING_STORE_PASSWORD`
   - Value: The password (case-sensitive)

**Security notes:**
- 🔒 Never commit this password to git
- 🔒 Store in password manager
- 🔒 Use strong password (16+ characters)

---

### 5. SIGNING_KEY_PASSWORD

**What it is:** Password for the specific key within the keystore

**How to get the value:**

From `keystores/KEYSTORE_INFO.txt`:
```
Key Password: your-key-password
```

**Note:** Key password and store password are often the same, but can be different.

**Steps:**
1. Get password from secure location
2. In GitHub:
   - Name: `SIGNING_KEY_PASSWORD`
   - Value: The password (case-sensitive)

---

## Verification Checklist

After adding all secrets:

- [ ] All 5 secrets are listed in repository settings
- [ ] No typos in secret names (they're case-sensitive!)
- [ ] SERVICE_ACCOUNT_JSON_PLAINTEXT is valid JSON
- [ ] SIGNING_KEY_STORE_BASE64 has no line breaks
- [ ] Aliases and passwords match your keystore
- [ ] Test deployment workflow to verify

## Testing Secrets

To verify secrets are correct without deploying:

1. Create a test GitHub Actions workflow:

```yaml
name: Test Secrets

on: workflow_dispatch

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Test SERVICE_ACCOUNT_JSON_PLAINTEXT
        run: |
          echo "${{ secrets.SERVICE_ACCOUNT_JSON_PLAINTEXT }}" | jq -r '.client_email'
          # Should output: playstore-deploy@your-project.iam.gserviceaccount.com
      
      - name: Test Keystore Decode
        run: |
          echo "${{ secrets.SIGNING_KEY_STORE_BASE64 }}" | base64 --decode > test.jks
          keytool -list -v -keystore test.jks \
            -storepass "${{ secrets.SIGNING_STORE_PASSWORD }}" \
            -alias "${{ secrets.SIGNING_KEY_ALIAS }}"
          # Should show keystore details
      
      - name: Cleanup
        if: always()
        run: rm -f test.jks
```

2. Run workflow manually
3. Check logs for verification
4. Delete test workflow after verification

## Common Issues

### "Invalid service account JSON (SERVICE_ACCOUNT_JSON_PLAINTEXT)"

**Symptom:** Deployment fails with authentication error

**Causes:**
- JSON is truncated (didn't copy all of it)
- JSON has syntax errors
- Wrong service account file

**Fix:**
1. Re-copy the entire JSON file
2. Validate JSON: https://jsonlint.com/
3. Ensure file is from Google Cloud (has "type": "service_account")

---

### "Failed to decode keystore"

**Symptom:** Build fails when decoding keystore

**Causes:**
- Base64 string has line breaks
- Wrong file was encoded
- Encoding method was incorrect

**Fix:**
1. Re-encode using commands above
2. Ensure output is single line
3. Verify keystore file is correct one

---

### "Keystore password incorrect"

**Symptom:** Signing fails with password error

**Causes:**
- Typo in password
- Using wrong password (debug instead of release)
- Password has special characters causing shell issues

**Fix:**
1. Verify password from KEYSTORE_INFO.txt
2. Test locally first: `keytool -list -keystore production-release.jks`
3. If password has special characters, escape them

---

### "Alias not found"

**Symptom:** Cannot find key with specified alias

**Causes:**
- Alias name typo
- Wrong keystore file
- Case sensitivity

**Fix:**
1. List keystore contents: `keytool -list -v -keystore production-release.jks`
2. Copy exact alias name (case-sensitive)
3. Update GitHub secret with correct alias

---

## Security Best Practices

### 1. Least Privilege
- Only grant secret access to necessary workflows
- Use environment-specific secrets if needed
- Regular audit of who has access

### 2. Rotation
- Rotate service account keys annually
- Update GitHub Secrets after rotation
- Test deployment after rotation
- Document rotation date

### 3. Monitoring
- Enable GitHub Actions audit log
- Monitor for unauthorized secret access
- Review workflow run history
- Check for failed authentication attempts

### 4. Backup
- Keep service account JSON in password manager
- Store keystore and passwords in company vault
- Document secret values in secure location (not git!)
- Have disaster recovery plan

### 5. Separation
- Use different service accounts for dev/staging/prod
- Consider separate repositories for different environments
- Never share production secrets with development

---

## Updating Secrets

When you need to update a secret:

1. Navigate to: Repository → Settings → Secrets → Actions
2. Find the secret to update
3. Click "Update"
4. Paste new value
5. Click "Update secret"
6. Test deployment to verify

**Note:** Updating a secret does NOT automatically re-run workflows. You need to trigger a new workflow run.

---

## Deleting Secrets

If you need to rotate or remove a secret:

1. **Before deleting:**
   - Ensure new secret is ready (if rotating)
   - Update workflows if secret name changes
   - Test with new secret

2. **Delete:**
   - Repository → Settings → Secrets → Actions
   - Click secret to delete
   - Click "Remove secret"
   - Confirm deletion

3. **After deleting:**
   - Add new secret immediately
   - Test deployment
   - Update documentation

---

## References

- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)
- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [keytool Documentation](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html)
