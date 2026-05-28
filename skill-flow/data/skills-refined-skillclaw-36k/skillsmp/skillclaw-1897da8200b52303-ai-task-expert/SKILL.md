---
name: ai-task-expert
description: Use this skill when you need to delegate implementation or research tasks to external AI agents, allowing you to focus on design decisions and user interactions.
---

# AI Task Expert

このスキルは外部のAIエージェントを実行するための専門知識を提供します。実装や調査の作業を別のAIエージェントに委譲することで、トークンとコンテキストを節約し、効率的にタスクを進めることができます。

## 対応するAIエージェント
- Gemini CLI
- Copilot CLI

## 基本的な実行方法
1. **コマンドのインストール確認**
   ```bash
   command -v gemini >/dev/null 2>&1 && echo "gemini installed!"
   command -v copilot >/dev/null 2>&1 && echo "copilot installed!"
   ```
   両方ともインストールされていない場合は、作業を停止し、ユーザにインストールを促してください。

2. **エージェントへのタスク実行**
   - Geminiを使用する場合:
   ```bash
   gemini --approval-mode=auto_edit -p "<Your task here>"
   ```
   - Copilotを使用する場合:
   ```bash
   copilot --allow-all-tools --deny-tool 'shell(rm)' --deny-tool 'shell(git push)' -p "<Your task here>"
   ```

## 指示の出し方
- **具体的なタスクを指示する**: 一度出した指示の変更はできないため、明確に指示を出してください。
- **文脈を含める**: 実行されるエージェントは現在の会話の履歴を知らないため、必要な情報を提供してください。
- **出力形式を指定する**: 調査結果が長くなる場合は、中間ファイルに出力するなど、レビューしやすい形式を選択してください。

## よくあるタスク
- 実装の細かいやり取りをAIエージェントに任せることで、メインの会話でのトークンの無駄を省く。
- 調査タスクをAIエージェントに委譲し、結果を確認する。

このスキルは、効率的にタスクを進めるためのガイドラインを提供します。