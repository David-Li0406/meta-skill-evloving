---
name: Web Search
description: This skill should be used when needs to search for unknown information, verify understanding, or avoid hallucination. or when detects knowledge gaps during task execution. Also trigger when the user asks to "search online", "look up information", "verify facts", "check documentation", "find latest version".
version: 0.1.0
---

# Web Search

## Purpose

Guide the agent to break down complex search queries into focused sub-queries, execute systematic web searches for each, and synthesize comprehensive answers.

## When to Use

Load this skill when:
- User explicitly requests online search or information lookup
- Agent encounters unknown information during task execution
- Agent needs to verify potentially incorrect understanding
- Current knowledge may be outdated or incomplete
- Technical details, APIs, or documentation need verification

## Core Approach

### 1. Analyze the Query

Examine the search query to determine if it contains multiple aspects based on 5W1H framework:
- **What**: What is X?
- **Why**: Why does X happen?
- **When**: When did/will X occur?
- **Where**: Where is X located/used?
- **Who**: Who created/uses X?
- **How**: How does X work?

**If the query contains only one 5W1H aspect**, proceed directly with a single search.

**If the query contains multiple 5W1H aspects**, break it down into focused sub-queries.

### 2. Break Down Complex Queries

For queries with multiple aspects, decompose them using 5W1H:

**Example:**
- Original: "What is FastAPI and why is it popular?"
- Sub-query 1 (What): "What is FastAPI?"
- Sub-query 2 (Why): "Why is FastAPI popular?"

**Example:**
- Original: "History of LLM agents and future trends"
- Sub-query 1 (When - past): "History of LLM agents"
- Sub-query 2 (When - future): "Future trends of LLM agents"

**Principles:**
- Each sub-query should focus on one 5W1H aspect
- Keep sub-queries clear and specific
- Maintain the original language and context

### 3. Execute Searches

For each sub-query (or the single query if no breakdown needed):

```
Use subagent tool:
- subrecipe: "web-search"
- parameters: {"search_query": "[sub-query]"}
- summary: true
```

### 4. Synthesize Results

After collecting all search results, synthesize a comprehensive answer that:
- Addresses the original query completely
- Integrates information from all sub-queries
- Maintains coherence and flow
- Preserves important details and nuances
- Cites sources when relevant

The final output should be a direct answer to the original query.

## Key Principles

- **Smart decomposition**: Only break down queries that genuinely have multiple aspects
- **Focused searches**: Each sub-query targets one specific aspect
- **Comprehensive synthesis**: Combine results into a unified answer
- **Maintain context**: Preserve the original question's intent during breakdown

## Notes

- This is a guidance skill, not a rigid workflow
- Use judgment to determine if breakdown is beneficial
- Simple, focused queries don't need decomposition
- The goal is to answer the user's original question effectively
