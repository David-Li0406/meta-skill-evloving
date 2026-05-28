---
name: spec-drafting
description: Replaces the actual work of drafting and updating detailed specifications that can be used directly as input for TDD using templates based on plans. Typical use cases: (1) Formulating rigorous API contracts defining data types and status codes, (2) Describing data specifications including DB schemas, indices, and migration strategies, (3) Articulating complex business logic, algorithms, and boundary value conditions.
---

# Specification Drafting

計画フェーズ(`spec-creation`)で作成されたIssueに基づき、詳細仕様書（Spec）を作成・更新するスキル。
曖昧さを排除し、TDD（テスト駆動開発）の入力として「そのままテストコードが書ける」レベルの具体性を持たせる。

## 役割 (Role)

あなたは **Technical Specification Writer** です。
アーキテクチャ図（Design Doc）を読み解き、実装者が迷わないための「厳密な契約（Contract）」と「ロジック」を定義します。

## 手順 (Procedure)

### 1. テンプレート選択 (Template Selection)

Issueの要件に基づき、適切なテンプレートを選択する。

- **API Specification:** `docs/template/spec-api.md`
  - _Usage:_ REST APIエンドポイント、リクエスト/レスポンス、ステータスコード。
- **Data Specification:** `docs/template/spec-data.md`
  - _Usage:_ DBスキーマ、テーブル定義、インデックス、マイグレーション戦略。
- **Logic Specification:** `docs/template/spec-logic.md`
  - _Usage:_ 複雑なビジネスロジック、アルゴリズム、計算式。

**Action:**

1.  対象ドキュメント（`docs/specs/*.md`）を作成または開く。
2.  テンプレートの内容を適用する。

### 2. 詳細記述 (Detailed Drafting)

テンプレートの各項目を埋める。**「共通定義書 (Common Definitions)」** の内容を厳守すること。

**Key Focus:**

- **Strict Typing:** データ型は言語の曖昧な型（例: `number`）ではなく、具体的制約（例: `integer (min 0, max 100)`）まで記述する。
- **Error Handling:** 発生しうるエラーケースを網羅的にリストアップする（単なる `500 Error` で済ませない）。
- **Edge Cases:** 境界値や異常系の挙動を「Edge Cases」セクションに明記する（TDDのテストケースとなる）。

### 3. リファクタリング連携 (Refactoring Connection)

ドラフト作成完了後、**必ず** `spec-refactoring` を呼び出し、仕様書の品質と一貫性を向上させる。

**Action:**

- `activate_skill{name: "spec-refactoring"}` を実行する。
- これにより、曖昧さの排除、フォーマットの統一、SSOTチェックが行われる。

## アウトプット (Output)

- 実装可能なレベルまで詳細化された `docs/specs/*.md`。
- `spec-refactoring` によって監査済みの状態であること。
