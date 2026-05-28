---
name: github-workflow-automation
description: Use this skill when automating GitHub workflows, setting up PR review automation, creating GitHub Actions, or triaging issues with AI assistance.
---

# Skill Body

## 🔧 GitHub Workflow Automation

> Patterns for automating GitHub workflows with AI assistance, inspired by [Gemini CLI](https://github.com/google-gemini/gemini-cli) and modern DevOps practices.

## When to Use This Skill

Use this skill when:

- Automating PR reviews with AI
- Setting up issue triage automation
- Creating GitHub Actions workflows
- Integrating AI into CI/CD pipelines
- Automating Git operations (rebases, cherry-picks)

---

## 1. Automated PR Review

### 1.1 PR Review Action

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          echo "files<<EOF" >> $GITHUB_OUTPUT
          echo "$files" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Get diff
        id: diff
        run: |
          diff=$(git diff origin/${{ github.base_ref }}...HEAD)
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          echo "$diff" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Review
        uses: actions/github-script@v7
        with:
          script: |
            const { Anthropic } = require('@anthropic-ai/sdk');
            const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

            const response = await client.messages.create({
              model: "claude-3-sonnet-20240229",
              max_tokens: 4096,
              messages: [{
                role: "user",
                content: `Review this PR diff and provide feedback:
                
                Changed files: ${{ steps.changed.outputs.files }}
                
                Diff:
                ${{ steps.diff.outputs.diff }}
                
                Provide:
                1. Summary of changes
                2. Potential issues or bugs
                3. Suggestions for improvement
                4. Security
                `
              }]
            });
            console.log(response);
```