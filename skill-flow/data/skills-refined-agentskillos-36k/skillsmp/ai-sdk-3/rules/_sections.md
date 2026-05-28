# Sections

This file defines all sections, their ordering, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Provider Setup (provider)

**Impact:** CRITICAL
**Description:** Configuring model providers. AI Gateway is recommended for simplicity.

## 2. Text Generation (generate)

**Impact:** HIGH
**Description:** Core patterns for generateText and streamText functions.

## 3. Tool Definitions (tool)

**Impact:** HIGH
**Description:** v6 tool() function syntax with inputSchema and execute.

## 4. Multi-Step Agents (agent)

**Impact:** HIGH
**Description:** stopWhen patterns for agentic workflows with tool loops.

## 5. Result Extraction (result)

**Impact:** MEDIUM
**Description:** Accessing text, tool calls, reasoning, and usage from results.

## 6. Message Types (message)

**Impact:** MEDIUM
**Description:** ModelMessage type and message array construction.

## 7. Error Handling (error)

**Impact:** MEDIUM
**Description:** AISDKError handling and common error patterns.
