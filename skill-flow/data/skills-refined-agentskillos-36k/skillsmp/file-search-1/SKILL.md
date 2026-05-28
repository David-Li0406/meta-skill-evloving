---
name: file-search
description: Rustプロジェクトのファイル検索スキル。ファイル名パターン検索、コード内文字列検索、シンボル（関数、構造体、enum、trait、impl）検索。検索実行時は必ずエージェント（Task tool）を使用し、直接Bashで検索コマンドを実行しない。
---

# File Search Skill

ファイル検索時は **必ずエージェント（Task tool）を使用** する。

## 実行方法

Task tool を使用:
- subagent_type: "Explore"
- prompt: "file-search-agentの指示に従い、ファイル検索を実行"

## 参照するエージェント

`agents/file-search-agent.md` を参照して実行する。
