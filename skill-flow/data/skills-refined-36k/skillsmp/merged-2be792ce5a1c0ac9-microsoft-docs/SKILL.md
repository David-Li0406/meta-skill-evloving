---
name: microsoft-docs
description: Use this skill to query official Microsoft documentation for understanding concepts, finding tutorials, and learning about services across Azure, .NET, Microsoft 365, Windows, Power Platform, and other Microsoft technologies.
---

# Microsoft Docs

## Tools

| Tool                    | Use For                                                       |
| ----------------------- | ------------------------------------------------------------- |
| `microsoft_docs_search` | Find documentation—concepts, guides, tutorials, configuration |
| `microsoft_docs_fetch`  | Get full page content (when search excerpts aren't enough)    |

## When to Use

- **Understanding concepts** — e.g., "How does Cosmos DB partitioning work?"
- **Learning a service** — e.g., "Azure Functions overview", "Container Apps architecture"
- **Finding tutorials** — e.g., "quickstart", "getting started", "step-by-step"
- **Configuration options** — e.g., "App Service configuration settings"
- **Limits & quotas** — e.g., "Azure OpenAI rate limits", "Service Bus quotas"
- **Best practices** — e.g., "Azure security best practices"

## Query Effectiveness

Good queries are specific:

```
# ❌ Too broad
"Azure Functions"

# ✅ Specific
"Azure Functions Python v2 programming model"
"Cosmos DB partition key design best practices"
"Container Apps scaling rules KEDA"
```

Include context:

- **Version** when relevant (e.g., `.NET 8`, `EF Core 8`)
- **Task intent** (e.g., `quickstart`, `tutorial`, `overview`, `limits`)
- **Platform** for multi-platform docs (e.g., `Linux`, `Windows`)

## When to Fetch Full Page

Fetch after search when:

- **Tutorials** — need complete step-by-step instructions
- **Configuration guides** — need all options listed
- **Deep dives** — user wants comprehensive coverage
- **Search excerpt is cut off** — full context needed

## Why Use This

- **Accuracy** — live docs, not training data that may be outdated
- **Completeness** — tutorials have all steps, not fragments
- **Authority** — official Microsoft documentation