---
name: web-search 
description: search the web for information when user explicitly requests web searches, by identifying the nature of the request and delegating to appropriate subagents (@code-researcher for documentation/code examples, @web-researcher for general information)
---

# Web Search

## Overview
An intelligent routing skill that analyzes user web search requests and delegates to specialized subagents based on the nature of the information needed. Optimizes search quality by matching request type to the most appropriate search tool.

## When to Use
Use this skill when:
- User explicitly requests to search the web
- User asks to "look up", "find information about", or "search for" something
- Current information or documentation beyond knowledge cutoff is needed
- User needs code examples, API documentation, or technical references
- User requires factual information, trends, or recent developments

## Available Subagents

### `@code-researcher`
**Capabilities**: Equipped with `exa` and `context7` MCP tools
**Best for**:
- Retrieving API documentation and library references
- Finding code examples and implementation patterns
- Searching GitHub repositories for solutions
- Accessing StackOverflow discussions and technical Q&A
- Looking up framework/library usage patterns
- Finding SDK and package documentation

**Strengths**: High-quality, developer-focused results from curated technical sources

### `@web-researcher`
**Capabilities**: Broad web search and fact-checking tools
**Best for**:
- General information and encyclopedia-style content
- Current events and news
- Product research and comparisons
- Company information and business intelligence
- Trends, statistics, and market data
- Non-technical documentation and guides
- Fact-checking and verification

**Strengths**: Comprehensive coverage of general knowledge domains

## Workflow

### Step 1: Analyze the Request
Examine the user's query to determine:
- **Domain**: Is it technical/programming-related or general knowledge?
- **Information type**: Documentation, examples, facts, trends, explanations?
- **Specificity**: Narrow technical query vs broad exploratory search?
- **Recency requirements**: Does it need current/real-time information?

### Step 2: Formulate Search Strategy
Based on analysis, determine:
- **Primary subagent**: Which subagent is best suited?
- **Query refinement**: Should the query be rephrased for better results?
- **Fallback plan**: What to do if primary search yields poor results?

**Decision Criteria**:
```
IF query contains: APIs, libraries, frameworks, code, packages, SDKs, programming languages
  → Use @code-researcher

ELSE IF query about: documentation for dev tools, implementation examples, technical patterns
  → Use @code-researcher

ELSE IF query about: general knowledge, news, products, companies, trends, facts
  → Use @web-researcher

ELSE IF uncertain but has technical keywords
  → Start with @code-researcher, fallback to @web-researcher

ELSE
  → Use @web-researcher
```

### Step 3: Delegate to Subagent
Invoke the selected subagent with:
- Clear, specific instructions on what information to find
 Context from the user's original request
- Expected format or depth of results
- Any constraints (date ranges, specific sources, etc.)

**Delegation template**:
```
Search for [specific information] related to [user's topic].
Focus on [documentation/examples/explanations/etc.].
Return [code examples/API references/factual summary/etc.].
```

### Step 4: Evaluate Results
When subagent returns:
- **Quality check**: Are results relevant and comprehensive?
- **Completeness**: Does it answer the user's question?
- **Accuracy**: Do results appear credible and current?

### Step 5: Fallback Strategy (if needed)
If primary subagent results are insufficient:
- **@code-researcher → @web-researcher**: When technical docs are sparse, try broader web search
- **@web-researcher → @code-researcher**: When general search returns too much code/technical content
- **Combine results**: Use both subagents for hybrid queries (e.g., "how does company X implement feature Y?")

**Fallback scenarios**:
- No relevant results found
- Results too technical or not technical enough
- Missing crucial context or examples
- User's question spans multiple domains

## Instructions

### Best Practices
- **Be specific**: Provide clear search objectives to subagents
- **Consider recency**: If topic is time-sensitive, explicitly request current information
- **Verify sources**: Note when results come from authoritative vs community sources
- **Iterate if needed**: Don't hesitate to refine and re-search if first attempt is poor
- **Combine when useful**: For complex queries, use both subagents to get comprehensive coverage

### Query Refinement Tips
- Extract key technical terms from user's natural language query
- Remove ambiguous words and clarify acronyms
- Add context about programming language or framework if missing
- Specify version numbers when relevant (e.g., "React 18 hooks" vs "React hooks")

### Common Patterns

**Pattern 1: Pure technical query**
```
User: "How do I use async/await in Python?"
→ @code-researcher: Search for Python async/await documentation and examples
```

**Pattern 2: General information query**
```
User: "What are the latest trends in AI?"
→ @web-researcher: Search for recent AI trends and developments
```

**Pattern 3: Hybrid query**
```
User: "How does Stripe handle payment processing?"
→ @code-researcher: Get Stripe API documentation and integration examples
→ @web-researcher: Get Stripe's business model and payment flow overview
→ Combine both for comprehensive answer
```

**Pattern 4: Fallback scenario**
```
User: "How to implement OAuth in my app?"
→ Try @code-researcher first for technical implementation
→ If results too abstract, fallback to @web-researcher for conceptual guides
```

## Report Format

After subagent(s) complete their search, structure the response as:

### Summary
- Brief overview of what was found
- Which subagent(s) were used and why

### Key Findings
- Main points from the search results
- Relevant code examples or documentation links
- Important caveats or considerations

### Sources
- Note primary sources consulted
- Indicate if results are from official docs, community resources, or general web

### Recommendations
- Suggest next steps if applicable
- Point out gaps that might need deeper research
- Mention related topics worth exploring

Keep the report concise and focused on addressing the user's original request. Avoid verbose explanations of the search process unless the user specifically wants to understand the methodology.
