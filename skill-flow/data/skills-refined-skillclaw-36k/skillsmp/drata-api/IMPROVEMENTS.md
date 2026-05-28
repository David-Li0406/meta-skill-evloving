# Drata API Skill Improvements

Learnings from ISO 27001 readiness assessment on 2026-01-06.

## API Endpoint Issues

### 1. v1 vs v2 API Inconsistency

The skill documentation references v2 endpoints that don't exist or behave differently:

```
# These v2 endpoints returned 404:
/public/v2/controls
/public/v2/risks
/public/v2/monitoring-tests

# Working alternatives (v1):
/public/controls (works, paginated with page/limit)
/public/personnel (works, returns detailed compliance data)
/public/assets (works)
/public/vendors (works)
```

**Recommendation:** Update `references/endpoints.md` to clarify which endpoints are v1 vs v2, and which actually exist.

### 2. Personnel Expand Parameter

The documented expand values are wrong:

```
# Documented:
?expand=user,devices

# Actual valid values (from error message):
?expand=customFields,complianceChecks,reasonProvider,user
```

**Recommendation:** Update personnel endpoint documentation with correct expand values.

### 3. Pagination Differences

v1 endpoints use `page` and `limit`:

```
/public/controls?limit=50&page=2
```

v2 endpoints use cursor-based pagination:

```
/public/v2/personnel (has pagination.cursor)
```

**Recommendation:** Document pagination differences between v1 and v2.

---

## Missing Useful Endpoints

Add documentation for these working endpoints:

### Controls (v1)

```bash
GET /public/controls?limit=50&page=1

Response includes:
- frameworkTags: ["SOC 2", "ISO 27001:2022"]
- isReady: boolean
- isMonitored: boolean
- hasEvidence: boolean
- hasOwner: boolean
- archivedAt: timestamp or null
```

### Assets (v1)

```bash
GET /public/assets

Response includes device compliance checks and owner info.
```

---

## Suggested Skill Enhancements

### 1. Add Common Queries Section

````markdown
## Common Queries

### Get ISO 27001 Control Status

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/controls?limit=50" | \
  jq '[.data[] | select(.frameworkTags | index("ISO 27001:2022"))]'
```
````

### Get Non-Ready Controls

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/controls?limit=100" | \
  jq '[.data[] | select(.isReady == false) | {name, code}]'
```

### Get Personnel Compliance Summary

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/personnel" | \
  jq '{
    total: .data | length,
    compliant: [.data[] | select(.complianceChecks[] |
      select(.type == "FULL_COMPLIANCE" and .status == "PASS"))] | length
  }'
```

### Get Devices with Compliance Issues

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/v2/devices" | \
  jq '[.data[] | select(.firewallEnabled == false or .encryptionEnabled == false)]'
```

### Get High Risk Vendors

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" \
  "https://public-api.drata.com/public/vendors" | \
  jq '[.data[] | select(.risk == "HIGH")]'
```

````

### 2. Add Framework Filter Examples

```markdown
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
````

````

### 3. Add Compliance Check Types Reference

```markdown
## Personnel Compliance Check Types

| Type | Description |
|------|-------------|
| FULL_COMPLIANCE | Overall compliance status |
| ACCEPTED_POLICIES | Policy acknowledgment |
| IDENTITY_MFA | MFA enabled on identity provider |
| BG_CHECK | Background check completed |
| AGENT_INSTALLED | Drata agent on device |
| PASSWORD_MANAGER | Password manager detected |
| HDD_ENCRYPTION | FileVault/BitLocker enabled |
| ANTIVIRUS | Antivirus software detected |
| AUTO_UPDATES | Automatic updates enabled |
| LOCK_SCREEN | Screen lock configured |
| SECURITY_TRAINING | Security training completed |
| HIPAA_TRAINING | HIPAA training (if applicable) |
| OFFBOARDING | Offboarding status |
````

### 4. Add Control Status Fields Reference

```markdown
## Control Status Fields

| Field         | Type      | Description                      |
| ------------- | --------- | -------------------------------- |
| isReady       | boolean   | Control meets all requirements   |
| isMonitored   | boolean   | Automated monitoring enabled     |
| hasEvidence   | boolean   | Evidence uploaded                |
| hasOwner      | boolean   | Owner assigned                   |
| archivedAt    | timestamp | Null if active                   |
| frameworkTags | string[]  | Associated compliance frameworks |
```

### 5. Add Aggregation Script

````markdown
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
````

````

---

## Updated endpoints.md Structure

Suggest reorganizing to:

```markdown
# Drata API Endpoints

## API Versions
- v1: `/public/*` - Original API, page-based pagination
- v2: `/public/v2/*` - Newer API, cursor-based pagination

## v1 Endpoints (Recommended)

### Controls
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/controls` | List controls (paginated: ?limit=50&page=1) |
| GET | `/public/controls/{id}` | Get control by ID |

### Personnel
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/personnel` | List personnel with compliance data |

### Vendors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/vendors` | List vendors |

### Assets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/assets` | List assets with device info |

## v2 Endpoints

### Company
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/v2/company` | Get company settings |

### Personnel
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/v2/personnel` | List personnel (cursor pagination) |

### Devices
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/v2/devices` | List devices |

### Vendors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/v2/vendors` | List vendors |
````

---

## Shell Environment Note

**Important:** When using `bash -c '...'` wrapper, environment variables inherit correctly from the parent shell. Direct commands in Claude Code may not have access to env vars like `$DRATA_API_KEY`.

Always use:

```bash
bash -c 'curl -s -H "Authorization: Bearer $DRATA_API_KEY" "https://..."'
```

Instead of:

```bash
curl -s -H "Authorization: Bearer $DRATA_API_KEY" "https://..."
```
