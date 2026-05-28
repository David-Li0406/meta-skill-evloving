---
name: firebase-remote-config
description: |
  Provides atomic operations for managing Firebase Remote Config templates
  (including client and server namespaces) using REST API, CLI, or scripts.
  Supports fetch, list keys, create/update parameters & conditions, merge,
  validate, publish, rollback, import/export JSON, percent rollouts, deletion,
  diff, and recommended condition generation.
license: Apache-2.0
compatibility: Designed for Claude Code and compatible agents
metadata:
  author: staytuned
  version: "1.0"
  category: development
---

# Firebase Remote Config Skill

This skill exposes **atomic operations** for Firebase Remote Config templates
based on the official API. Use an access token with appropriate IAM role
(cloudconfig.admin) to make changes.

---

## Inputs

| Input | Description |
|-------|-------------|
| `project_id` | Firebase project ID |
| `namespace` | Template namespace (`firebase` for client, `firebase-server` for server) |
| `access_token` | OAuth2 Bearer token with remoteconfig scope (use `gcloud auth application-default print-access-token`) |
| `template_file` | Local path for export/import |
| `parameter_key` | Feature flag/parameter identifier |
| `parameter_values` | JSON of default + conditional values |
| `condition_name` | Name of a condition |
| `condition_expr` | Expression logic for condition |
| `version_number` | Template version number to rollback |
| `percent` | Rollout percentage |
| `base_template` | Local path (diff base) |
| `new_template` | Local path (diff new) |
| `etag` | Latest ETag from fetch for safe publish |

---

## OPERATIONS

### Fetch Current Template

Retrieve the active Remote Config template for a namespace.

**Shell (curl)**

```bash
bash scripts/fetch-template.sh \
  "{access_token}" "{project_id}" "{namespace}" "{output_file}"
```

---

### List Parameters & Conditions

List keys in template.json:

**Shell**

```bash
bash scripts/list-keys.sh template.json
```

---

### Create / Update Parameters

Modify template JSON locally using jq, then merge.

---

### Create / Update Conditions

Modify template JSON locally using jq, then merge.

---

### Merge Template JSON

Use Node script to merge changes safely.

```bash
node scripts/merge-template.js \
  --base="{base_template}" \
  --updates="{updates_file}" \
  --out="{output_file}"
```

---

### Validate Template

Validation is implicit on publish; external orchestrator should ensure JSON correctness.

**Validate JSON before publishing:**

```bash
jq '.' template.json > /dev/null && echo "Valid" || echo "Invalid"
```

---

### Publish Template

Replace the template using PUT.

**Important:** Remove `version` field before publishing (Firebase auto-generates it).

```bash
# Prepare template (remove version)
jq 'del(.version)' template.json > template-publish.json

# Publish using script (etag="*" for force update)
bash scripts/publish-template.sh \
  "{access_token}" "{project_id}" "{namespace}" "*" "template-publish.json"
```

**Note:** Using `etag="*"` forces an update. Firebase Remote Config API doesn't return ETag in headers, so force update is the standard approach.

---

### Rollback Template

Rollback to a previous version.

```bash
bash scripts/rollback-template.sh \
  "{access_token}" "{project_id}" "{namespace}" "{version_number}"
```

---

### Import / Export JSON

Export: fetch template to file
Import: publish from file

---

### Generate Percentage Rollout Condition

Create a conditional expression with percentage logic.

```bash
bash scripts/generate-percent-condition.sh "{condition_name}" "{percent}"
```

---

### Delete Parameter

Remove parameter from template JSON then publish.

```bash
bash scripts/delete-parameter.sh "{template_file}" "{parameter_key}" "{output_file}"
```

---

### Diff Templates

Show diff between two template files.

```bash
bash scripts/diff-templates.sh "{base_template}" "{new_template}"
```

---

### Generate Recommended Conditions

Given a feature metadata object, produce a set of environment conditions.

---

## Notes

- Namespace parameter added for REST calls so client/server templates can be managed separately.
- All operations are *stateless* and accept full inputs for each call.
- No built-in workflow sequencing — external planner must orchestrate calls.
- Scripts provided for shell/curl and Node merge logic.
- Progressive disclosure: agents can load scripts or reference docs only when needed.

## Supporting References

- [API-reference-summary.md](references/API-reference-summary.md) - REST API endpoints and schemas
- [example-feature-metadata-schema.json](references/example-feature-metadata-schema.json) - Example feature metadata
- Remote Config Conditional Expression Reference - Canonical syntax for condition expressions. <https://firebase.google.com/docs/remote-config/condition-reference>
- RemoteConfig REST API - Template schema and fields. <https://firebase.google.com/docs/reference/remote-config/rest/v1/RemoteConfig>
