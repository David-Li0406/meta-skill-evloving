---
name: context7-usage
description: Guidelines for using the Context7 MCP server to fetch real-time documentation and code examples.
license: MIT
metadata:
  author: Antigravity
  version: "1.0"
---

# Context7 Usage Guidelines

The `context7` MCP server provides access to real-time, version-specific documentation and code examples for external libraries.

## When to Use

- **Researching Libraries**: When investigating a new library, use `context7` to understand its capabilities and API surface.
- **Implementation**: Before writing code using an external library, use `context7` to fetch the latest syntax, methods, and patterns.
- **Debugging**: When a library usage fails, use `context7` to verify the API usage against the official documentation.
- **Outdated Knowledge**: If you suspect your internal knowledge of a library might be outdated (e.g., major version changes), verify with `context7`.

## Best Practices

1.  **Be Specific**: When querying, specify the library name and ideally the version if known (or ask for the latest).
2.  **Verify Context**: Ensure the returned documentation matches the environment (e.g., specific framework versions).
3.  **Use Examples**: leverage the code examples provided by `context7` to ensure idiomatic usage.

## Tool Usage

Simply use the `context7` tool available in your toolset. You can usually invoke it by asking questions about a library or explicitly asking to "use context7 to check [library]".
