---
name: drata-api
description: Drata compliance automation API integration for managing controls, evidence, personnel, assets, risks, vendors, and devices. Use when interacting with Drata's public API for compliance automation tasks including uploading evidence, managing personnel security training, querying controls, handling background checks, device compliance, vendor management, or any GRC (Governance, Risk, Compliance) automation workflows.
---

# Drata API Skill

## Base URLs

| Region        | URL                                 |
| ------------- | ----------------------------------- |
| North America | `https://public-api.drata.com`      |
| Europe        | `https://public-api.eu.drata.com`   |
| Asia-Pacific  | `https://public-api.apac.drata.com` |

## Authentication

The API key is stored in environment variable `DRATA_API_KEY`.

**Important:** Always use `bash -c '...'` wrapper when making API calls - environment variables may not inherit properly in direct commands:

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" "https://public-api.drata.com/public/controls"'
```

API keys created in Drata Settings > API Keys. Scope read/write per endpoint.

## Rate Limits

500 requests/minute per IP.

## API Versions

Drata has two API versions with different behaviors:

| Version | Path           | Pagination                      | Status                                               |
| ------- | -------------- | ------------------------------- | ---------------------------------------------------- |
| v1      | `/public/*`    | Page-based (`?limit=50&page=1`) | Recommended for controls, personnel, vendors, assets |
| v2      | `/public/v2/*` | Cursor-based (`?cursor=...`)    | Use for personnel, devices, vendors                  |

### v1 Pagination (Page-based)

```bash
# Fetch all pages
for p in 1 2 3 4 5; do
  bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
    "https://public-api.drata.com/public/controls?limit=50&page='$p'"'
done
```

### v2 Pagination (Cursor-based)

```javascript
async function fetchAll(endpoint) {
  let cursor;
  const results = [];
  do {
    const params = cursor ? `?cursor=${cursor}` : "";
    const resp = await fetch(
      `https://public-api.drata.com/public/v2/${endpoint}${params}`,
      {
        headers: { Authorization: `Bearer ${API_KEY}` },
      },
    );
    const data = await resp.json();
    results.push(...data.data);
    cursor = data?.pagination?.cursor;
  } while (cursor);
  return results;
}
```

## Endpoints

See `references/endpoints.md` for complete endpoint documentation.

## Common Queries

### Get ISO 27001 Control Status

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/controls?limit=50" | \
  jq "[.data[] | select(.frameworkTags | index(\"ISO 27001:2022\"))]"'
```

### Get Non-Ready Controls

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/controls?limit=100" | \
  jq "[.data[] | select(.isReady == false) | {name, code}]"'
```

### Get Personnel Compliance Summary

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/personnel" | \
  jq "{
    total: .data | length,
    compliant: [.data[] | select(.complianceChecks[] |
      select(.type == \"FULL_COMPLIANCE\" and .status == \"PASS\"))] | length
  }"'
```

### Get Devices with Compliance Issues

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/v2/devices" | \
  jq "[.data[] | select(.firewallEnabled == false or .encryptionEnabled == false)]"'
```

### Get High Risk Vendors

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/vendors" | \
  jq "[.data[] | select(.risk == \"HIGH\")]"'
```

## Filtering by Framework

Controls are tagged with frameworks. Common tags:

- "SOC 2"
- "ISO 27001:2022"
- "HIPAA"
- "GDPR"
- "PCI DSS"

Filter with jq:

```bash
jq '[.data[] | select(.frameworkTags | index("ISO 27001:2022"))]'
```

## Control Status Fields

| Field         | Type      | Description                      |
| ------------- | --------- | -------------------------------- |
| isReady       | boolean   | Control meets all requirements   |
| isMonitored   | boolean   | Automated monitoring enabled     |
| hasEvidence   | boolean   | Evidence uploaded                |
| hasOwner      | boolean   | Owner assigned                   |
| archivedAt    | timestamp | Null if active                   |
| frameworkTags | string[]  | Associated compliance frameworks |

## Personnel Compliance Check Types

| Type              | Description                      |
| ----------------- | -------------------------------- |
| FULL_COMPLIANCE   | Overall compliance status        |
| ACCEPTED_POLICIES | Policy acknowledgment            |
| IDENTITY_MFA      | MFA enabled on identity provider |
| BG_CHECK          | Background check completed       |
| AGENT_INSTALLED   | Drata agent on device            |
| PASSWORD_MANAGER  | Password manager detected        |
| HDD_ENCRYPTION    | FileVault/BitLocker enabled      |
| ANTIVIRUS         | Antivirus software detected      |
| AUTO_UPDATES      | Automatic updates enabled        |
| LOCK_SCREEN       | Screen lock configured           |
| SECURITY_TRAINING | Security training completed      |
| HIPAA_TRAINING    | HIPAA training (if applicable)   |
| OFFBOARDING       | Offboarding status               |

## Common Workflows

### Upload Evidence for Personnel

```javascript
// 1. Find personnel by email
const resp = await fetch(
  `https://public-api.drata.com/public/personnel?q=user@company.com`,
  {
    headers: { Authorization: `Bearer ${API_KEY}` },
  },
);
const userId = (await resp.json()).data[0].user.id;

// 2. Upload evidence
const form = new FormData();
form.append("type", "SEC_TRAINING"); // or HIPAA_TRAINING, BACKGROUND_CHECK, etc.
form.append("file", fs.createReadStream("evidence.pdf"));

await fetch(`https://public-api.drata.com/public/users/${userId}/documents`, {
  method: "POST",
  headers: { Authorization: `Bearer ${API_KEY}` },
  body: form,
});
```

### Evidence Types

| Type                    | Description                  |
| ----------------------- | ---------------------------- |
| `SEC_TRAINING`          | Security training completion |
| `HIPAA_TRAINING`        | HIPAA training completion    |
| `BACKGROUND_CHECK`      | Background check results     |
| `MFA_IDP`               | MFA on identity provider     |
| `PASSWORD_MANAGER`      | Password manager evidence    |
| `HARD_DRIVE_ENCRYPTION` | Device encryption            |
| `ANTI_VIRUS`            | Antivirus software           |
| `AUTO_UPDATES`          | Auto-updates enabled         |
| `SCREENSAVER_LOCK`      | Screensaver lock enabled     |

### Upload Control Evidence

```javascript
const form = new FormData();
form.append("file", fs.createReadStream("evidence.pdf"));

await fetch(
  `https://public-api.drata.com/public/controls/${controlId}/external-evidence`,
  {
    method: "POST",
    headers: { Authorization: `Bearer ${API_KEY}` },
    body: form,
  },
);
```

## Full Compliance Report Script

```bash
#!/bin/bash
# Generate compliance summary report

echo "=== DRATA COMPLIANCE REPORT ==="
echo ""

# Controls summary
echo "CONTROLS:"
for p in 1 2 3 4 5 6; do
  curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
    "https://public-api.drata.com/public/controls?limit=50&page=$p"
done | jq -s '[.[].data[]] | {
  total: length,
  ready: [.[] | select(.isReady)] | length,
  with_owner: [.[] | select(.hasOwner)] | length,
  with_evidence: [.[] | select(.hasEvidence)] | length,
  monitored: [.[] | select(.isMonitored)] | length
}'

echo ""
echo "PERSONNEL:"
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/personnel" | jq '{
  total: .data | length,
  compliant: [.data[] | select(.complianceChecks[] |
    select(.type == "FULL_COMPLIANCE" and .status == "PASS"))] | length
}'

echo ""
echo "VENDORS:"
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/vendors" | jq '{
  total: .data | length,
  high_risk: [.data[] | select(.risk == "HIGH")] | length,
  with_pii: [.data[] | select(.hasPii == true)] | length
}'
```

## Error Handling

| Code | Meaning                            |
| ---- | ---------------------------------- |
| 400  | Malformed data / validation errors |
| 401  | Invalid authorization              |
| 402  | Plan upgrade required              |
| 403  | Action not permitted               |
| 404  | Not found                          |
| 451  | Must accept Drata terms            |
| 500  | Internal server error              |

## Python Example

```python
import requests
import os

API_KEY = os.environ.get("DRATA_API_KEY")
BASE_URL = "https://public-api.drata.com/public"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_all_v1(endpoint, limit=50):
    """Fetch all pages from v1 endpoint (page-based)"""
    results, page = [], 1
    while True:
        resp = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS,
                          params={"limit": limit, "page": page})
        data = resp.json()
        if not data.get("data"):
            break
        results.extend(data["data"])
        page += 1
    return results

def get_all_v2(endpoint):
    """Fetch all pages from v2 endpoint (cursor-based)"""
    results, cursor = [], None
    while True:
        params = {"cursor": cursor} if cursor else {}
        resp = requests.get(f"{BASE_URL}/v2/{endpoint}", headers=HEADERS, params=params)
        data = resp.json()
        results.extend(data.get("data", []))
        cursor = data.get("pagination", {}).get("cursor")
        if not cursor:
            break
    return results

# Get all controls (v1)
controls = get_all_v1("controls")

# Get all personnel (v1 recommended)
personnel = get_all_v1("personnel")

# Get all devices (v2)
devices = get_all_v2("devices")
```
