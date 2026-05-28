---
name: creating-github-issues-from-web-research
description: Use this skill when you need to research a topic and create a corresponding GitHub issue for tracking, collaboration, and task management.
---

## Overview

This skill empowers Claude to streamline the research-to-implementation workflow by integrating web search with GitHub issue creation, allowing efficient conversion of research findings into trackable tasks for development teams.

## How It Works

1. **Web Search**: Claude utilizes its web search capabilities to gather information on the specified topic.
2. **Information Extraction**: The skill extracts relevant details, key findings, and supporting evidence from the search results.
3. **GitHub Issue Creation**: A new GitHub issue is created with a clear title, a summary of the research, key recommendations, and links to the original sources.

## When to Use This Skill

This skill activates when you need to:
- Investigate a technical topic and create an implementation ticket.
- Track security vulnerabilities and generate a security issue with remediation steps.
- Research competitor features and create a feature request ticket.

## Examples

### Example 1: Researching Security Best Practices

User request: "research Docker security best practices and create a ticket in <repository>"

The skill will:
1. Search the web for Docker security best practices.
2. Extract key recommendations, security vulnerabilities, and mitigation strategies.
3. Create a GitHub issue in the specified repository with a summary of the findings, a checklist of best practices, and links to relevant resources.

### Example 2: Investigating API Rate Limiting

User request: "find articles about API rate limiting, create issue with label <label>"

The skill will:
1. Search the web for articles and documentation on API rate limiting.
2. Extract different rate limiting techniques, their pros and cons, and implementation examples.
3. Create a GitHub issue with the specified label, summarizing the findings and providing links to the source articles.

## Best Practices

- **Specify Repository**: When creating issues for a specific project, explicitly mention the repository name to ensure the issue is created in the correct location.
- **Use Labels**: Add relevant labels to the issue to categorize it appropriately and facilitate issue tracking.
- **Provide Context**: Include sufficient context in your request to guide the web search and ensure the generated issue contains the most relevant information.

## Integration

This skill seamlessly integrates with Claude's web search capabilities and requires authentication with a GitHub account. It can be used in conjunction with other skills to further automate development workflows.