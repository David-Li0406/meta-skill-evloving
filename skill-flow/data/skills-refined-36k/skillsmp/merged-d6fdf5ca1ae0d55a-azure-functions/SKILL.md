---
name: azure-functions
description: Use this skill when developing Azure Functions, including patterns for isolated worker models, Durable Functions orchestration, and cold start optimization across .NET, Python, and Node.js.
---

# Azure Functions

## Patterns

### Isolated Worker Model (.NET)
Modern .NET execution model with process isolation.

### Node.js Programming Model
Modern code-centric approach for TypeScript/JavaScript.

### Python Programming Model
Decorator-based approach for Python functions.

## Anti-Patterns

### ❌ Blocking Async Calls
Avoid blocking asynchronous calls to ensure optimal performance.

### ❌ New HttpClient Per Request
Do not create a new HttpClient instance for each request.

### ❌ In-Process Model for New Projects
Refrain from using the in-process model for new projects.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| High | Use async pattern with Durable Functions |
| High | Use IHttpClientFactory (Recommended) |
| High | Always use async/await |
| Medium | Configure maximum timeout (Consumption) |
| High | Use isolated worker for new projects |
| Medium | Configure Application Insights properly |
| Medium | Check extension bundle (most common) |
| Medium | Add warmup trigger to initialize your code |

## Reference System Usage

Always consult the provided reference files for guidance:
- **For Creation:** Refer to **`references/patterns.md`** for building patterns.
- **For Diagnosis:** Use **`references/sharp_edges.md`** to understand critical failures.
- **For Review:** Check **`references/validations.md`** for strict rules and constraints.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.