# Google Sheets Service Account Setup

**Time required**: ~10 minutes
**Cost**: $0 (completely free)

---

## Overview

A **Service Account** is a special Google account for automated access (not human users). Think of it as a "robot user" that can read/write your Google Sheets without browser login.

---

## Quick Reference

| Step | Time | Action |
|------|------|--------|
| 1 | 2 min | Create Google Cloud Project |
| 2 | 1 min | Enable Google Sheets API |
| 3 | 2 min | Create Service Account |
| 4 | 1 min | Download credentials.json |
| 5 | 2 min | Share Sheet with Service Account |
| 6 | 1 min | Test connection |

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with any Google account
3. Click project dropdown (top left) → **NEW PROJECT**
4. Name: `sheets-automation` (or any name)
5. Click **CREATE**
6. Wait ~30 seconds, then select the new project

---

## Step 2: Enable Google Sheets API

1. Go to [API Library](https://console.cloud.google.com/apis/library)
2. Search: "Google Sheets API"
3. Click result → Click **ENABLE**
4. (Optional) Also enable "Google Drive API" for full access

---

## Step 3: Create Service Account

1. Go to [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **+ CREATE SERVICE ACCOUNT**
3. Fill in:
   - Name: `sheets-writer`
   - Description: `Writes data to Google Sheets`
4. Click **CREATE AND CONTINUE**
5. Skip roles (leave empty) → Click **CONTINUE**
6. Skip user access → Click **DONE**

---

## Step 4: Download Credentials Key

1. Click on your service account (from the list)
2. Go to **KEYS** tab
3. Click **ADD KEY** → **Create new key**
4. Select **JSON** → Click **CREATE**
5. File downloads automatically
6. Move to project: `mv ~/Downloads/*.json ./credentials.json`
7. Secure it: `chmod 600 credentials.json`

---

## Step 5: Share Sheet with Service Account

1. Find your service account email (looks like: `sheets-writer@project-id.iam.gserviceaccount.com`)
2. Open your Google Sheet
3. Click **Share** (top right)
4. Paste service account email
5. Set permission: **Editor**
6. Uncheck "Notify people"
7. Click **Share**

---

## Step 6: Test Connection

```python
# test_connection.py
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

# Replace with your sheet name
sheet = client.open("Your Sheet Name").sheet1
print(f"Connected! Sheet has {len(sheet.get_all_values())} rows")
```

```bash
python test_connection.py
# Expected: "Connected! Sheet has X rows"
```

---

## Security Checklist

```bash
# 1. Verify gitignored
grep -q "credentials.json" .gitignore && echo "✅ Gitignored" || echo "❌ Add to .gitignore!"

# 2. Verify permissions
ls -la credentials.json
# Should show: -rw------- (600)

# 3. Verify not in git
git status | grep credentials.json && echo "❌ In git!" || echo "✅ Not tracked"
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `FileNotFoundError: credentials.json` | Download key from GCP (Step 4) |
| `SpreadsheetNotFound` | Share sheet with service account email (Step 5) |
| `PERMISSION_DENIED` | Grant "Editor" permission (not Viewer) |
| `Invalid JSON` | Re-download credentials file |

---

## Service Account Email Format

```
{account-name}@{project-id}.iam.gserviceaccount.com
```

Example: `sheets-writer@my-project-123456.iam.gserviceaccount.com`

You can find this in:
- GCP Console → IAM → Service Accounts → Email column
- Inside `credentials.json` → `client_email` field

---

## Key Rotation (Every 90 Days)

1. Go to Service Accounts in GCP
2. Click your service account → **KEYS** tab
3. **ADD KEY** → **Create new key** → **JSON**
4. Replace old `credentials.json` with new one
5. Test connection
6. Delete old key (click ⋮ → Delete)

---

## Cost

Everything is **$0**:
- Google Cloud project: Free
- Google Sheets API: Free (60 requests/minute)
- Service Account: Free
- Key creation: Free

**Quota limits** (free tier):
- Read: 300 requests per 60 seconds
- Write: 300 requests per 60 seconds

Typical usage (~10 API calls/day) = well within free tier.

---

## References

- [Service Accounts Overview](https://cloud.google.com/iam/docs/service-accounts)
- [Google Sheets API Quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [gspread Authentication](https://docs.gspread.org/en/latest/oauth2.html#service-account)
