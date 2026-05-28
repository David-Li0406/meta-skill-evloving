---
name: code-review
description: Perform comprehensive code quality assessment and provide improvement suggestions
author: StrRay Framework
version: 1.0.0
tags: [review, quality, assessment, improvement]

mcp:
  code-review:
    command: node
    args: [node_modules/strray-ai/dist/plugin/mcps/knowledge-skills/code-review.server.js]
---

# Code Review Skill

Provides automated code review capabilities with quality assessment and improvement suggestions.

## Tools Available

- **analyze_code_quality**: Analyze code quality metrics, identify issues, and provide improvement suggestions
- **review_pull_request**: Review pull requests by analyzing changed files and providing comprehensive feedback
- **check_best_practices**: Check adherence to coding best practices and standards

## Usage

This skill performs automated code reviews including:
- Code quality analysis and metrics
- Pull request review and feedback
- Best practices compliance checking
- Improvement recommendations and suggestions

## Integration

Activated for code review requests, pull request analysis, and quality assessments through the skills system.