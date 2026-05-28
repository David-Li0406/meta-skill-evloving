---
name: github-issue-management
description: Use this skill when you need to create or continue working on GitHub issues based on conversation context.
---

# Skill body

## Overview

This skill allows you to create well-structured GitHub issues or continue working on existing ones by leveraging the context of ongoing conversations. It adapts to the content of discussions, ensuring that issues are relevant and actionable.

## Operations

### 1. Create Issue

#### Purpose

Transform organic development discussions into trackable GitHub issues without requiring users to explicitly categorize their thoughts.

#### Workflow

1. **Analyze Conversation Context**
   - Identify user goals, problems discussed, decisions made, and relevant technical context.
   - Prioritize actionable information.

2. **Determine Issue Nature**
   - Classify the issue type based on conversation content (e.g., feature request, bug report, task).
   - Avoid forcing categories; let the content guide you.

3. **Clarify with User (Required)**
   - Confirm your understanding of the issue with the user.

### 2. Continue Working on Issue

#### Important Notes

- Automatically uses the issue from the current conversation context; no issue ID is required.
- Follow best practices for software engineering, including small iterations and proper commit messages.

#### Workflow

1. **Retrieve Context**
   - Find the issue ID from conversation history. If not found, ask the user for it.
   - Locate relevant artifacts in `/tmp/deep-dive/{task-name}/`.

2. **Fetch Latest Updates**
   - Use `gh issue view {issue-id} --json title,body,comments,labels` to get the latest comments.

3. **Remove Pending Label**
   - Indicate that work has resumed by removing the pending label.

4. **Analyze Feedback**
   - Review new comments for plan approval, modification requests, or additional requirements.

5. **Take Action Based on Feedback**
   - If the plan is approved, proceed to implementation.
   - If changes are requested, adjust the plan accordingly.

## Core Principles

- **Intelligent Context Extraction**: Understand user needs and capture relevant details.
- **Flexible and Adaptive**: Adapt to the conversation's natural structure without rigid templates.
- **Continuous Iteration**: Implement small, focused changes and verify functionality through testing.