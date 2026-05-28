---
name: github-metadata
description: manage custom issue fields, metadata schemas, and early-access REST API features
metadata:
  category: github
---

# GitHub Metadata

## What is it?

The **Metadata Skill** handles advanced and "hidden" GitHub features, specifically focusing on Issue Custom Fields and attributes accessible via the Issue Fields REST API.

## Success Criteria

- Custom field values are accurately read or updated.
- Numeric IDs for fields and repositories are resolved BEFORE API calls.
- API calls use the correct `Accept` headers and JSON payloads.
- No assumptions are made about existing field values.

## Why use it?

- **Advanced customization**: Access GitHub's early-access custom fields API
- **Flexible metadata**: Manage custom properties beyond standard issue fields
- **Dynamic resolution**: Handles complex ID lookups for fields and repositories
- **Future-proof**: Leverages cutting-edge GitHub features before MCP support
- **Precise control**: Direct REST API access for fine-grained metadata operations

## When to use this skill

- "Get the value of the 'Priority' custom field for issue #10."
- "Set the 'Target Date' field on this issue."
- "What are the available custom fields in this organization?"

## What this skill can do

- **Discovery**: List available issue fields in an organization (`GET /orgs/{org}/issue-fields`).
- **Read**: Fetch values of specific custom fields on an issue.
- **Write**: Update custom field values using raw REST calls.

## What this skill will NOT do

- Manage standard metadata (assignees) - use `github-issues`.
- Create fields (admin task, though supported by API).

## How to use this skill

1. **Resolve IDs**: Use `gh repo view` and field discovery to get numeric IDs. Writing values REQUIRES these IDs.
2. **Check MCP**: Ensure `issue_read` doesn't already return the field.
3. **Construct API Call**: Use `gh api` with the endpoints defined in `ISSUE_FIELDS_API.md`.
4. **Authentication**: Ensure the token has `repo` and `organization` scopes.

## Tool usage rules

- **Statelessness**: Always resolve IDs dynamically; do not hardcode field or repository IDs.
- **REST Essential**: This skill relies heavily on the `run_command` tool to execute `gh api` using the REST endpoints. _Note: MCP tools do not currently support the Issue Fields Early Access API._
- **Header**: `Accept: application/vnd.github+json` is mandatory for these endpoints.
- **IDs**: Writing values REQUIRES the numeric `field_id` (from Discovery) and `repository_id`.

## Examples

See [field-payload-examples.json](assets/field-payload-examples.json) for concrete payloads and expected outcomes.

### Listing Fields

```bash
# Get all defined fields for the org
gh api /orgs/my-org/issue-fields
```

### Setting a Field Value

```bash
# 1. Get Repo ID
REPO_ID=$(gh repo view my-org/my-repo --json id -q .id)

# 2. Set Value (Field ID 123 = Priority, Value = "High")
gh api --method PUT /repositories/$REPO_ID/issues/42/issue-field-values \
  -f issue_field_values='[{"field_id": 123, "value": "High"}]'
```

## Limitations

- Requires numeric IDs for fields and repositories.
- Early Access API is subject to change.
