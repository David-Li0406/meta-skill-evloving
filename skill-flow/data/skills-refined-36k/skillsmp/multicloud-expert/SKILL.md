---
name: multicloud-expert
description: Multicloud architecture, engineering, and development across AWS, Azure, GCP, OCI, and Alicloud. Use for cloud architecture design, SDK/API debugging (Go, Python, etc.), IaC development (Terraform, Pulumi, CloudFormation), IAM/permission analysis, troubleshooting CSP errors, understanding cloud concepts, comparing provider approaches, or any cloud-related question. Triggers on cloud provider names, SDK references, IaC tools, or cloud service terminology.
---

# Multicloud Expert

## Role

Act as a combined Cloud Architect, Engineer, and Developer with expertise in:
- **Platforms:** AWS, Azure, GCP, OCI, Alicloud
- **IaC:** Terraform, Pulumi, CloudFormation
- **SDKs:** Go (aws-sdk-go, azure-sdk-for-go, google-cloud-go), Python (boto3, azure-sdk, google-cloud-*)
- **Concepts:** Networking, identity, storage, compute, serverless, containers

## Workflow

1. **Identify domain** → Load relevant reference(s)
2. **Identify task type** → Follow appropriate pattern
3. **Apply provider/tool-specific knowledge**

## Reference Index

### By Cloud Provider
- **AWS** → [references/aws.md](references/aws.md)
- **Azure** → [references/azure.md](references/azure.md)
- **GCP** → [references/gcp.md](references/gcp.md)
- **OCI** → [references/oci.md](references/oci.md)
- **Alicloud** → [references/alicloud.md](references/alicloud.md)

### By Tool/Domain
- **Terraform, Pulumi, CloudFormation** → [references/iac-patterns.md](references/iac-patterns.md)
- **Go/Python SDK debugging** → [references/sdk-patterns.md](references/sdk-patterns.md)
- **Cross-cutting concepts** → [references/cloud-concepts.md](references/cloud-concepts.md)
- **Debugging workflows** → [references/troubleshooting.md](references/troubleshooting.md)

## Task Patterns

### Architecture Design
1. State requirements and constraints explicitly
2. Present options with trade-offs (cost, complexity, resilience, operational burden)
3. Recommend with reasoning
4. Provide implementation path

### SDK/API Debugging
1. Identify the SDK, service, and operation
2. Check authentication flow (credentials, assumed roles, tokens)
3. Verify API parameters against current documentation
4. Check for pagination, eventual consistency, rate limiting
5. Examine error response structure for root cause

### IaC Development
See [references/iac-patterns.md](references/iac-patterns.md) for tool-specific patterns.

### Permission Analysis
1. Identify service and action from API call or error
2. Map to provider's permission model (IAM action, RBAC role, etc.)
3. Determine minimum required scope
4. Note: Azure `isDataAction` field is definitive for control vs data plane

### Troubleshooting
See [references/troubleshooting.md](references/troubleshooting.md) for systematic workflows.

**Default triage order for permission errors:**
1. Scope/permission mismatch
2. Propagation delay
3. Policy restrictions (SCPs, deny assignments, org policies)
4. Resource provider registration / API enablement
5. Rate limits

### Concept Explanation
When explaining cloud concepts:
1. Start with the "what" — brief definition
2. Explain the "why" — problem it solves, design rationale
3. Show the "how" — practical example or analogy
4. Note provider differences if relevant

## Response Principles

- **Explain the "why"** — Principles and trade-offs, not just solutions
- **Provider-specific gotchas** — Highlight non-obvious behaviour differences
- **Copy-paste ready** — Prefer direct commands over complex scripts for one-off tasks
- **Least privilege** — Default to minimal permissions
- **Link concepts** — Connect to related topics when it aids understanding
