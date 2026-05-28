---
name: deploy-guardrail
description: Enforces a pre-flight check to prevent configuration drift between local defaults and Cloud Run environments.
---

# Deploy Guardrail Skill

Use this skill **BEFORE** any deployment to a Cloud Run environment (Dev or Prod). It ensures that all secrets required by the codebase are actually present in the target environment's configuration.

## Workflow

### 1. Identify Required Secrets
Scan the codebase for `ConfigSchema`, `process.env`, or `firebase functions` definitions to list required environment variables.
*   **Source Truths**:
    *   `server/src/appConfig/schema.ts` (Zod schema)
    *   `functions/src/config/schema.ts`
    *   `firebase.json` (secret versions)

### 2. Fetch Live Configuration
Execute the following command to get the current environment variables from Cloud Run:
```powershell
gcloud run services describe [SERVICE_NAME] --region us-west1 --format="json(spec.template.spec.containers[0].env)"
```

### 3. Compare & Assert
*   **Compare**: potential `process.env` usages vs. the JSON output from `gcloud`.
*   **Critical Assertion**: If a variable is marked as 'Required' in schema but missing in Cloud Run, **STOP THE DEPLOYMENT**.

### 4. Remediation (If Failed)
If drift is detected:
1.  **Do NOT** assume a default value.
2.  **Check** Secret Manager for the missing key.
3.  **If Missing**: Ask the user to generate/provide a secure value (do not generate one silently).
4.  **Update**: Use `gcloud run services update` to inject the missing variable.

## Example Command Chain
```powershell
# 1. Get Config
gcloud run services describe olybars-backend --region us-west1 --format="json" > current_config.json

# 2. Analyze (Manual or via grep)
Get-Content current_config.json | Select-String "INTERNAL_HEALTH_TOKEN"
```
