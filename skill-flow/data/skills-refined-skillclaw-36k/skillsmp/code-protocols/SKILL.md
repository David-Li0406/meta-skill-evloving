---
name: Code Protocols
description: 開発プロトコル（旧資産Module 01-25）への自動参照
activation: auto
triggers:
  - /do
  - /plan (implementation phase)
hegemonikon: M6-Praxis
---

# Code Protocols Skill

> **目的**: 実装フェーズで開発プロトコルを自動参照
> **発動**: `/do` 実行時、または実装計画作成時

---

## 自動参照ロジック

タスクの種類に応じて、該当するプロトコルを提示する:

| タスク種別 | 参照プロトコル | 原典パス |
|:---|:---|:---|
| 設定ファイル編集 | **DMZ Protocol** | Module 01 |
| 新機能実装 | **TDD Protocol** | Module 04 |
| コミット作成 | **Narrative Commit** | Module 14 |
| 複雑度が高い | **Complexity Budget** | Module 06 |
| セキュリティ関連 | **Red Teaming** | Module 11 |

---

## 原典参照パス

```
M:\Brain\99_🗃️_保管庫｜Archive\プロンプト ライブラリー\モジュール（開発用）\個別のモジュール\
├── Module 01 The Demilitarized Zone (DMZ) Protocol.md
├── Module 04 Retro-Causal Testing Protocol (TDD Enforcement).md
├── Module 06 Complexity Budget Protocol.md
├── Module 07 The Devil's Advocate Protocol (Multi-Persona Critique).md
├── Module 10 Ripple Effect Analysis (Impact Prediction).md
├── Module 11 Automated Red Teaming Protocol.md
├── Module 13 Code Archaeology Protocol (Chesterton's Fence).md
├── Module 14 Narrative Commit Protocol.md
└── ... (全25モジュール)
```

---

## 発動時の出力形式

```
[Hegemonikon] M6 Praxis → Code Protocols
  タスク: {タスク種別}
  該当プロトコル: {プロトコル名}
  原典: view_file "{パス}" で詳細参照可能
```

---

## 使用方法

### 自動発動（Claude）
`/do` 実行時に M6 Praxis が自動でこの Skill を参照し、該当プロトコルを提示。

### 手動発動（Creator）
`/dev` ワークフローで明示的にプロトコル一覧を表示。

---

## モジュール一覧インデックス

詳細は [legacy-modules-index.md](file:///M:/Hegemonikon/docs/archive/legacy-rules/legacy-modules-index.md) を参照。
