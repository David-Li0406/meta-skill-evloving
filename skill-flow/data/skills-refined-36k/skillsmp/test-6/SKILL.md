---
name: test
description: TypeScriptプロジェクトのテスト実行スキル。ユニットテスト、統合テストの実行とレポート。テスト実行時は必ずエージェント（Task tool）を使用し、直接Bashでテストコマンドを実行しない。
---

# Test Skill

テスト実行時は **必ずエージェント（Task tool）を使用** する。

## 実行方法

Task tool を使用:
- subagent_type: "general-purpose"
- prompt: "test-agentの指示に従い、テストを実行"

## 参照するエージェント

`agents/test-agent.md` を参照して実行する。
