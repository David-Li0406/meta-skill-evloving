---
name: review-pr
description: Review GitHub Pull Request and provide insights for human reviewers
---

Review GitHub Pull Request and provide insights for human reviewers: $ARGUMENTS

## Prerequisites
- $ARGUMENTS: PR number (123) or URL
- Run from repository root

## Process

1. Fetch PR information in parallel (independent):
   - PR metadata: `gh pr view $ARGUMENTS`
   - PR diff: `gh pr diff $ARGUMENTS`
2. Analyze the changes using Task tool (subagent_type=general-purpose):
   - Provide both PR metadata and diff as context to the agent
   - Agent should analyze: code quality, security risks, performance, test adequacy
   - Agent should output structured findings with file:line references
3. Transform agent findings into human reviewer context:
   - Summarize architectural changes and design decisions
   - Highlight security risks with specific remediation steps
   - Note performance concerns with impact assessment
   - Identify missing test coverage
4. Output comprehensive review report in Markdown format

## Output Format

The review should be structured as follows:

```markdown
# PR一次レビュー結果

## 変更サマリー
[What was changed and why - include architectural decisions, affected components, scope of changes]

## Claudeによる一次レビュー

### コードの品質・設計
[Analysis of code quality, design patterns, naming conventions, function responsibilities, readability]
- 具体的な問題点や改善提案があれば、ファイルパスと行番号を含めて記載

### セキュリティリスク
[Security vulnerability analysis including XSS, SQL injection, authentication issues, secret exposure risks]
- 問題が見つかった場合は、WARNING として明示し、具体的な対策を提案

### パフォーマンス
[Performance analysis including algorithmic complexity, memory usage, database queries, caching opportunities]
- パフォーマンス上の懸念があれば、具体的な影響範囲と改善案を記載

### テストの妥当性
[Test coverage analysis, test case appropriateness, edge cases, integration tests]
- 不足しているテストケースがあれば具体的に指摘

## レビューに必要な情報

### 変更の背景とコンテキスト
[Why these changes were made, related issues, design decisions, architectural considerations]

### 影響範囲
[What parts of the system are affected, potential side effects, downstream dependencies]

### 確認が必要な項目
[Specific aspects that require human judgment - business logic validation, edge cases, integration points]
1. [Item requiring validation]
2. [Complex logic requiring domain expertise]
3. [Breaking changes or API changes]

### 関連ファイルと依存関係
[Files that are related but not changed, dependencies that might be affected, configuration changes needed]
```

## Notes

- Focus on providing context that is not obvious from reading the PR description
- If PR diff is too large (>10 files or >500 lines), focus on critical changes
- For security issues, mark them clearly with WARNING and provide specific remediation steps
- Provide actionable feedback with concrete suggestions
- Highlight breaking changes or backward compatibility concerns
- Analyze integration points (APIs, message queues, shared databases) and system-wide impact (breaking changes, performance, dependencies)
- Omit redundant information that can be easily seen in the PR itself (title, author, file list, etc.)
