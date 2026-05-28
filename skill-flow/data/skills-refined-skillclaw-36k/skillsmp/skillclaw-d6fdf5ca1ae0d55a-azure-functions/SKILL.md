---
name: azure-functions
description: Use this skill when developing Azure Functions to implement best practices, avoid common pitfalls, and optimize performance across .NET, Python, and Node.js.
---

# Azure Functions

## Patterns

### Isolated Worker Model (.NET)
Modern .NET execution model with process isolation.

### Node.js v4 Programming Model
Modern code-centric approach for TypeScript/JavaScript.

### Python v2 Programming Model
Decorator-based approach for Python functions.

## Anti-Patterns

### ❌ Blocking Async Calls
Avoid blocking calls in asynchronous functions.

### ❌ New HttpClient Per Request
Refrain from creating a new HttpClient instance for each request.

### ❌ In-Process Model for New Projects
Do not use the in-process model for new Azure Functions projects.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| High | Use async pattern with Durable Functions. |
| High | Use IHttpClientFactory (Recommended). |
| High | Always use async/await. |
| Medium | Configure maximum timeout (Consumption). |
| High | Use isolated worker for new projects. |
| Medium | Configure Application Insights properly. |
| Medium | Check extension bundle (most common). |
| Medium | Add warmup trigger to initialize your code. |