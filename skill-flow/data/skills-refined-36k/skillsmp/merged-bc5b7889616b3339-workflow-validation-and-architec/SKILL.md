---
name: workflow-validation-and-architecture-check
description: Use this skill to validate project workflows against brainbase standards and check compliance with architecture patterns, generating reports and improvement suggestions.
---

# Workflow Validation and Architecture Check

**目的**: brainbaseのワークフローとアーキテクチャパターンへの準拠をチェックし、課題を特定して修正提案を行う。

このSkillは、プロジェクトのワークフローを検証し、brainbase標準プロセスとの整合性を確認し、アーキテクチャパターンへの準拠を自動的にチェックします。

## Workflow Overview

```
Phase 1: 要件分析 / EventBus パターンチェック
└── agents/phase1_requirements_analysis.md / agents/phase1_eventbus_checker.md
    └── 課題リスト、整合性チェック結果
    └── Event発火が適切か判断
    └── 直接呼び出しのアンチパターンを検出

Phase 2: 検証レポート生成 / Reactive Store パターンチェック
└── agents/phase2_report_generation.md / agents/phase2_store_checker.md
    └── 検証レポート（課題 + 推奨アクション）
    └── Store経由で状態更新しているか判断
```

## Phase詳細

### Phase 1: 要件分析 / EventBus パターンチェック

**Subagent**: `agents/phase1_requirements_analysis.md` / `agents/phase1_eventbus_checker.md`

**目的**: プロジェクトの既存ワークフロー（タスク、マイルストーン）を調査し、brainbase標準との整合性をチェックし、EventBusパターンの適用を確認。

**使用Skills**:
- `task-format`: タスク管理標準フォーマットとの照合
- `milestone-management`: マイルストーン管理ルールとの照合

**入力**:
- プロジェクト名
- チェック対象のファイルパス（または現在の変更）

**出力**:
```markdown
## 課題リスト
- 課題1: タスクフォーマット不整合
- 課題2: マイルストーン粒度が大きすぎる
- 違反箇所のリスト
```

### Phase 2: 検証レポート生成 / Reactive Store パターンチェック

**Subagent**: `agents/phase2_report_generation.md` / `agents/phase2_store_checker.md`

**目的**: Phase 1で特定した課題に対して、推奨アクションを含む検証レポートを生成し、Reactive Storeパターンの適用を確認。

**使用Skills**:
- `principles`: brainbase価値観に基づいた優先度付け

**入力** (Phase 1から):
- 課題リスト
- 整合性チェック結果

**出力**:
```markdown
## 検証レポート

### 課題サマリー
- 課題総数: X件
- 重大度別: Critical Y件、Medium Z件

### 推奨アクション
1. タスクフォーマット統一（優先度: P0）
2. マイルストーン粒度見直し（優先度: P1）
```

## Success Criteria

- [ ] Phase 1の成果物が存在するか（課題リスト、整合性チェック結果）
- [ ] Phase 2の成果物が存在するか（検証レポート）
- [ ] 各PhaseのSuccess Criteriaが100%達成
- [ ] 課題が最低3件以上特定されている
- [ ] 推奨アクションに優先度（P0/P1/P2）が付与されている

## 使い方

```bash
# プロジェクトワークフローを検証
/workflow-validation-and-architecture-check brainbase-ui

# 特定のファイルをチェック
/workflow-validation-and-architecture-check public/modules/domain/task/task-service.js

# 現在の変更をチェック（git diff）
/workflow-validation-and-architecture-check --changed-only
```

## Troubleshooting

### Phase 1で失敗する

**症状**: "_codex/projects/{project}/ が見つかりません" エラー

**対処**:
1. プロジェクト名を確認（brainbase-ui, mana等）
2. _codex/projects/ 配下のディレクトリ構造を確認

### Phase間のデータ受け渡しが失敗する

**症状**: Phase 2で「Phase 1の出力が見つからない」エラー

**対処**:
1. Phase 1のSuccess Criteriaを確認
2. Phase 1の出力形式を確認（markdown見出しが正しいか）

---

## 参照

- **CLAUDE.md**: `§1 Architecture Principles`
- **Skills**: task-format, milestone-management, principles
- **Model**: sonnet（全Phase）

---

最終更新: 2025-12-31
brainbase開発ワークフロー自動化