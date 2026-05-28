---
name: tooling
description: Tooling and verification. Apply when encountering unfamiliar third-party libraries, framework updates, uncertain parameter types, verifying best practices, or uncertain API parameters.
---

# Tooling & Verification

## Core Principle

"RTFM (Read The Fing Manual)."
Don't guess API signatures. Don't assume library behavior. Before writing code, ensure you have evidence.

## Official Documentation Verification

When encountering unfamiliar third-party libraries, framework updates, or uncertain parameter types:

1. **Locate library ID**: Use `resolve-library-id` to convert library name (e.g., "shadcn/ui", "stripe-js") to accurate system ID
2. **Get documentation**: Use `get-library-docs` to fetch latest official documentation snippets
3. **Cite authority**: Reference official documentation as basis for implementation in code comments or explanations

**Applicable scenarios**:
- "How do I use React 19's useActionState?"
- "What are the payment intent parameters for Stripe API?"

## Real Code Search

Documentation tells you **theoretically** how to use it; GitHub tells you **actually** how to use it. When documentation is unclear or you need to reference best practices:

1. **Search use cases**: Use `searchGitHub` to search specific function or pattern implementations in real codebases
2. **Pitfall guide**: Observe if other developers have discussed related bugs in Issues
3. **Pattern imitation**: Look for implementation patterns in high-star projects as reference

**Applicable scenarios**:
- "Is this configuration option actually used in production?"
- "I want to see the actual implementation code for this complex pattern"

## Execution Strategy

- **Verify first, write second**: Unless it's the most basic function in standard library, if there's any uncertainty, call tools
- **No hallucination**: If tools can't find it, clearly tell user "documentation not found" instead of fabricating a plausible API
