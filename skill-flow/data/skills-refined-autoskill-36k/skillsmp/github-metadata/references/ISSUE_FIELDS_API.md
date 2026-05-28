# Issue Fields API

Reference for interacting with GitHub Issue Fields via the Early Access REST API.

> [!NOTE]
> These endpoints are currently "Early Access".
> **Base URL**: `https://api.github.com`
> **Required Header**: `Accept: application/vnd.github+json` (and `X-GitHub-Api-Version: 2022-11-28`)
> **Authentication**: Requires a token with `repo`, `organization`, or specific fine-grained permissions.

## 1. Discovery (List Fields)

Get defined custom fields for an organization.

**Endpoint**: `GET /orgs/{ORG}/issue-fields`

**Example**:

```bash
gh api /orgs/my-org/issue-fields
```

**Response**:

```json
[
  {
    "id": 123,
    "name": "Priority",
    "data_type": "single_select",
    "options": [
      { "id": 1, "name": "High" },
      { "id": 2, "name": "Low" }
    ]
  }
]
```

## 2. Reading Values (List Field Values)

Get the values set on a specific issue.

**Endpoint**: `GET /repos/{OWNER}/{REPO}/issues/{ISSUE_NUMBER}/issue-field-values`

**Example**:

```bash
gh api /repos/my-org/my-repo/issues/42/issue-field-values
```

## 3. Writing Values (Set Field Values)

Update/Set custom field values for an issue.

**Endpoint**: `PUT /repositories/{REPOSITORY_ID}/issues/{ISSUE_NUMBER}/issue-field-values`
*Note: This uses the numeric `REPOSITORY_ID`, not the `owner/repo` path.*

**Payload**:

```json
{
  "issue_field_values": [
    { "field_id": 123, "value": "Critical" },
    { "field_id": 456, "value": 5 },
    { "field_id": 789, "value": "2025-12-31" }
  ]
}
```

**How to get `REPOSITORY_ID`**:

```bash
gh repo view my-org/my-repo --json id -q .id
```

## 4. Workflow: Discovering Field IDs

To set a field value, you need the numeric `field_id`. Here's how to find it:

1. List all fields for the organization:

   ```bash
   gh api /orgs/my-org/issue-fields
   ```

2. Parse the JSON response to find the field by name:

   ```bash
   gh api /orgs/my-org/issue-fields | jq '.[] | select(.name == "Priority") | .id'
   ```

3. Use the returned ID in your PUT request.

## 5. Updates (Modify Field Definitions)

Change the definition of a field (e.g., rename "Priority" to "Severity").

**Endpoint**: `PATCH /orgs/{ORG}/issue-fields/{FIELD_ID}`
