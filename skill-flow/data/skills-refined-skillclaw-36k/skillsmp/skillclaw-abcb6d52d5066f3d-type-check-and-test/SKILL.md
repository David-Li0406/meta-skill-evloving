---
name: type-check-and-test
description: Use this skill when you need to perform type checking and testing in TypeScript or Rust projects, ensuring that all commands are executed through the Task tool.
---

# Type Check and Test Skill

型チェックおよびテスト実行時は **必ずエージェント（Task tool）を使用** する。

## 実行方法

### 型チェック

TypeScriptプロジェクトの場合:
- subagent_type: "general-purpose"
- prompt: "type-check-agentの指示に従い、型チェックを実行"

Rustプロジェクトの場合:
- subagent_type: "general-purpose"
- prompt: "type-check-agentの指示に従い、型チェックを実行"

### テスト

TypeScriptプロジェクトの場合:
- subagent_type: "general-purpose"
- prompt: "test-agentの指示に従い、テストを実行"

Rustプロジェクトの場合:
- subagent_type: "general-purpose"
- prompt: "test-agentの指示に従い、テストを実行"

## 参照するエージェント

- 型チェック: `agents/type-check-agent.md`
- テスト: `agents/test-agent.md`