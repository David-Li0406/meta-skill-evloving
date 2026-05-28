---
description: A hello world prompt demonstrating APM with GitHub integration
mcp:
  - ghcr.io/github/github-mcp-server
input: [name]
---

# Hello World APM Application

Welcome to APM, ${input:name}! This demonstrates:
- ✅ Parameter substitution with ${input:name}
- ✅ MCP server integration with GitHub
- ✅ Reusable, shareable prompt applications

## Instructions

Please:
1. Use the **search_repositories** tool to display my key GitHub Repositories and quickly understand what they do, using my username: ${input:name}
2. Give ${input:name} an enthusiastic welcome to AI-native development
3. Share one interesting insight about their GitHub repositories
4. Suggest their next step with APM based on their GitHub activity

## Expected Output

A personalized greeting with GitHub repository insights and tailored APM recommendations.
