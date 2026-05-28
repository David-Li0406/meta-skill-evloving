---
name: mcp-browser-verify
description: Use browser automation MCP (Playwright/Browser/Browser-Use) to validate UI flows, capture screenshots, and reproduce issues. Use when visual verification or web flow testing is needed.
compatibility: Requires a browser MCP server; target app must be reachable.
allowed-tools: MCP(*)
---

# mcp-browser-verify

## Activation
- UI bug, layout mismatch, flow verification, auth journey, “sprawdź w przeglądarce”.

## Procedure
1. Define scenario: URL, credentials (if any), steps, expected result.
2. Run scripted navigation.
3. Capture evidence: screenshots + console/network errors.
4. Report deltas + actionable fix hints.

## Output
- Scenario + evidence + pass/fail + next fix step.
