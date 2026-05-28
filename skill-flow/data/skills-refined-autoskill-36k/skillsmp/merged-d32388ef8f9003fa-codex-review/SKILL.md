---
name: codex-review
description: Use this skill to perform code, configuration file, and document reviews using the OpenAI Codex CLI when prompted with requests like "review this file" or "Codex, please review."
---

# Codex Review Skill

This skill utilizes the OpenAI Codex CLI to execute reviews of specified files, including code and configuration files.

## Usage

Invoke this skill when the user makes requests such as:
- "Codex にレビューしてもらって"
- "Codex でレビューして"
- "OpenAI にレビューしてもらって"
- "codex review"
- "このコードを Codex に見てもらって"

## Workflow

### 1. Confirm File Path

If the user does not specify a file path, ask for the file to review.

### 2. Execute Review with Codex CLI

Run the following command to review the specified file. Replace `<file_path>` with the actual file path.

```bash
cat <file_path> | codex exec "<review_instruction>"
```

### 3. Review Instructions Template

#### General Code Review
```
このコードをレビューしてください。以下の観点で問題点や改善点を指摘してください：
- バグや論理エラー
- セキュリティ上の問題
- パフォーマンスの問題
- コードの可読性
- ベストプラクティスへの準拠
```

#### Configuration File Review
```
この設定ファイルをレビューしてください。以下の観点で問題点や改善点を指摘してください：
- セキュリティリスク
- 設定の妥当性
- 不足している設定
- 改善の余地
```

#### Security-Focused Review
```
このコードのセキュリティレビューを行ってください。以下の観点で脆弱性を指摘してください：
- インジェクション攻撃
- 認証・認可の問題
- 機密情報の露出
- OWASP Top 10 の脆弱性
```

### 4. Display Results

Present the review results in Japanese or English, depending on the prompt language.

### 5. Summary

Summarize key findings and actionable recommendations in Japanese.

## Important Notes

- If the file does not exist, notify the user.
- For very large files, consider focusing the review on key functions or sections.
- Adjust prompts appropriately for languages other than Go.

## Troubleshooting

### Codex CLI Not Found

```bash
# Install via npm
npm install -g @openai/codex
```

### Authentication Error

Ensure that the OpenAI API key is set correctly.

## Prerequisites for Codex CLI

- The `codex` command must be in the PATH.
- The OpenAI API key must be configured (authenticated with `codex auth login`).