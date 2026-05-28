---
name: web-verification
description: Grounds clinical diagnosis via live medical literature search using Google Search Tool
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I ground the AI-generated diagnosis in real medical literature by searching for relevant sources. I verify that the diagnosis aligns with current clinical guidelines and research.

## When to use me

Use this when:

- Fairness validation is complete and you need web verification
- You need to cite authoritative sources for the diagnosis
- You're ensuring the diagnosis aligns with current medical knowledge

## Key Concepts

- **Google Search Tool**: Live web search for medical literature
- **Source Verification**: Confirm diagnosis with clinical guidelines
- **Web Evidence**: Citations from peer-reviewed sources
- **web_verified**: State flag after verification complete

## Source Files

- `services/router.ts`: Web verification routing
- `types.ts`: AnalysisResult with webVerification field

## Code Patterns

- Search for relevant medical literature based on detected conditions
- Verify diagnosis aligns with clinical guidelines
- Return verified flag, sources, and summary

## Operational Constraints

- Must provide at least one authoritative source
- Non-critical failure - return "skipped" rather than crash
- Flag AI reasoning vs. grounded web sources in output
