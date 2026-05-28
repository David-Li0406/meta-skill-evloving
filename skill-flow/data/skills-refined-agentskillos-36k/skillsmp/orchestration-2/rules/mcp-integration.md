---
title: MCP Integration
impact: MEDIUM
tags: orchestration, mcp, tools
---

# MCP Integration (Global Tools)

You have access to global MCP servers that provide real-time external capabilities:

## Global MCP Servers

### PERPLEXITY MCP (Research & Real-time Data)
- `perplexity_search` -- Direct web search
- `perplexity_ask` -- Conversational AI + web search
- `perplexity_research` -- Deep research with citations
- `perplexity_reason` -- Advanced reasoning

### CONTEXT7 MCP (Up-to-date Documentation)
- Retrieves latest docs for ANY library/framework
- Just add "use context7" to agent prompts

### PLAYWRIGHT MCP (Browser Automation)
- `playwright_navigate` -- Go to a URL
- `playwright_screenshot` -- Capture page/element screenshots
- `playwright_click` -- Click elements
- `playwright_fill` -- Fill form inputs
- `playwright_select` -- Select dropdown options
- `playwright_hover` -- Hover over elements
- `playwright_evaluate` -- Execute JavaScript in page
- `playwright_get_content` -- Get HTML or accessibility tree

## When to Use MCPs

### USE PERPLEXITY MCP WHEN:
- User asks about current events or recent data
- Need to verify up-to-date pricing, APIs, or versions
- Researching best practices or industry standards
- Finding solutions to errors or compatibility issues
- Validating technical claims or documentation
- Any question requiring information beyond training

### USE CONTEXT7 MCP WHEN:
- Implementing with a library you're unfamiliar with
- Library/framework APIs may have changed
- Need accurate, current documentation examples
- Building with new or rapidly-evolving technologies
- User asks "how do I use X?" for external libraries

### USE PLAYWRIGHT MCP WHEN:
- Need to visually verify a web page or component
- Testing form interactions without full E2E setup
- Debugging UI issues with screenshots
- Inspecting DOM structure via accessibility tree
- Quick ad-hoc E2E testing without test framework
- Visual regression checking (screenshot before/after)

## Worker Agents + MCPs

**IMPORTANT:** Workers CAN and SHOULD use MCPs when their task requires external data.

**Include in worker prompts when relevant:**

```
MCP TOOLS AVAILABLE:
- If you need current documentation -> use context7 MCP
- If you need to research something -> use perplexity MCP tools
- Prefer MCP data over potentially outdated training knowledge
```

## Example Worker Prompt with MCP

```python
Task(
    subagent_type="general-purpose",
    description="Implement Stripe webhooks",
    prompt="""WORKER. Production code only. No mocks/stubs.

MCP TOOLS: Use context7 for current Stripe webhook docs.
Use perplexity_research if you need implementation patterns.

TASK: Implement Stripe webhook handlers for:
- checkout.session.completed
- invoice.payment_succeeded
- customer.subscription.deleted

Follow Stripe's latest best practices.

REPORT: Files created + webhook signatures handled.
""",
    run_in_background=True
)
```

## Orchestrator MCP Delegation

As the orchestrator, you NEVER use MCPs directly. Instead:

```
User asks: "How do I implement X with the latest API?"

You spawn:
Agent 1 -> "Use context7 to get current X documentation"
Agent 2 -> "Use perplexity to research X best practices"
Agent 3 -> "Implement X based on research findings"

The agents use MCPs. You synthesize their results.
```

## MCP-Aware Research Pattern

When a task might benefit from current information:

```python
# First wave: Research with MCPs
Task(subagent_type="general-purpose",
     prompt="Use perplexity_research to find current best practices for [topic]. Report key findings.",
     run_in_background=True)

Task(subagent_type="general-purpose",
     prompt="Use context7 to get latest [library] documentation for [feature]. Report API signatures.",
     run_in_background=True)

# Second wave: Implementation with research results
# (spawn after research completes, with findings in prompt)
```

## Playwright MCP Usage Examples

### Quick Visual Check
```python
Task(
    subagent_type="general-purpose",
    description="Verify homepage renders correctly",
    prompt="""WORKER. Use Playwright MCP tools.

1. playwright_navigate to http://localhost:3000
2. playwright_screenshot (full page)
3. playwright_get_content (format="a11y")

REPORT: Screenshot taken, accessibility issues found (if any).
""",
    run_in_background=True
)
```

### Form Testing
```python
Task(
    subagent_type="general-purpose",
    description="Test login form validation",
    prompt="""WORKER. Use Playwright MCP tools.

1. playwright_navigate to /login
2. playwright_click on submit (empty form)
3. playwright_screenshot - capture validation errors
4. playwright_fill email field with "test@example.com"
5. playwright_fill password field with "short"
6. playwright_click submit
7. playwright_screenshot - capture password validation error

REPORT: Validation messages shown correctly? Screenshots attached.
""",
    run_in_background=True
)
```

### UI Audit with Guidelines
```python
# First: capture state with Playwright
Task(
    subagent_type="general-purpose",
    prompt="Use playwright_navigate to /dashboard, then playwright_get_content with a11y format. Save accessibility tree.",
    run_in_background=True
)

# Then: apply web-design-guidelines to findings
Task(
    subagent_type="general-purpose",
    prompt="Review the accessibility tree from Playwright against web-design-guidelines. Report violations.",
    run_in_background=True
)
```

## MCP Anti-Patterns

| Don't | Do |
|-------|-----|
| Use MCPs as orchestrator | Delegate MCP use to worker agents |
| Assume training data is current | Use context7 for library docs |
| Skip research for complex topics | Use perplexity for real-time validation |
| Ignore MCP results | Integrate MCP findings into synthesis |
| Write full E2E suites with MCP | Use MCP for ad-hoc, CLI for suites |
| Trust MCP screenshots blindly | Verify with actual test runs in CI |
