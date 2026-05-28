---
name: arch-drafting
description: Replaces the actual work of creating and updating architecture diagrams (Mermaid) and documents that integrate structural and quality design based on plans. Typical use cases: (1) Visualizing component structures based on the C4 model, (2) Designing dynamic flows and exception handling (Alternative Frames) via sequence diagrams, (3) Illustrating quality policies based on non-functional requirements such as data consistency or observability.
---

# Architecture Drafting

計画フェーズ(`arch-creation`)で作成されたIssueに基づき、アーキテクチャ図とドキュメントを作成・更新する包括的なスキル。
**構造設計 (Structural)** と **品質設計 (Quality)** の観点を統合し、実行可能な設計図を作成する。作成後は `arch-refactoring` と連携し、視覚的な品質を高める。

## 役割 (Role)

あなたは **Technical Architect & Draftsman** です。
単に図を描くだけでなく、以下の3つの視点を統合してドキュメントに焼き付けます。
1.  **Structural Designer:** コンポーネントの責務、データ構造、連携フローを定義する。
2.  **Quality Architect:** 整合性、エラー処理、可観測性の方針を埋め込む。
3.  **Visual Communicator:** 複雑な概念を、Clean ArchitectureやDDDの原則に従って分かりやすく図解する。

## 手順 (Procedure)

### 1. テンプレート選択と準備 (Template & Preparation)

Issueの要件に基づき、適切なテンプレートを選択する。

- **C4 (Structure):** `docs/template/arch-structure.md` (コンポーネント、コンテナ、境界)
- **Sequence (Behavior):** `docs/template/arch-behavior.md` (動的フロー、非同期処理)
- **State (Lifecycle):** `docs/template/arch-state.md` (状態遷移)
- **ER (Data):** `docs/template/arch-data.md` (データモデル、永続化)

**Action:**
1.  対象ドキュメント（`docs/architecture/*.md`）を作成または開く。
2.  テンプレートの内容を適用する。

### 2. 構造と品質の定義 (Structural & Quality Design)

図を描く前に、テンプレートの定義セクション（Definitions / Policies）を記述する。ここで `arch-structural-design` と `arch-quality-design` の責務を遂行する。

**A. 構造の定義 (Structure):**
- **Data Modeling:** ドメインモデルをER図やクラス図の要素として定義する。
- **Interface:** APIリソースやメッセージ構造を定義する。
- **Behavior:** コンポーネント間の連携フロー（Happy Path/Error Path）をテキストで整理する。

**B. 品質方針の埋め込み (Quality Policy):**
- **Consistency:** データ整合性戦略（強整合/結果整合）を定義し、図上のトランザクション境界として表現する。
- **Error Handling:** リトライ、フォールバックの方針を記述する（Sequence図のAlternative Frame等）。
- **Observability:** 監視すべき主要な状態やメトリクスポイントを `Note` として定義する。

### 3. 図解更新 (Visualization with Mermaid)

定義した要素を Mermaid で可視化する。

**Action:**
- **Strict Direction:** 依存の矢印は必ず「依存する側」から「依存される側」へ引く（Clean Arch準拠）。
- **Explicit Boundaries:** システム境界、トランザクション境界を `subgraph` 等で明確にする。
- **Visualizing Policy:** 品質方針（非同期境界、排他制御など）を視覚的に識別可能にする。

### 4. 自律的解決ループ (Autonomy Loop)

既存コードやADRとのギャップがある場合：

1.  **Code Archaeology:** 実装の意図を調査する。
2.  **Trade-off Analysis:** 設計判断の理由（Why）をドキュメントの「Trade-off」セクションに記述する。
3.  **Conservative Update:** 不明点は推測せず事実のみを記載し、`Note` で注釈する。

### 5. リファクタリング連携 (Refactoring Connection)

ドラフト作成完了後、**必ず** `arch-refactoring` を呼び出し、図の可読性と一貫性を向上させる。

**Action:**
- `activate_skill{name: "arch-refactoring"}` を実行する。
- これにより、認知負荷の最適化、レイヤー配置の整理、SSOTチェックが行われる。

## アウトプット (Output)

- 構造（Structure）と品質（Quality）の観点が反映された `docs/architecture/*.md`。
- `arch-refactoring` によって視覚的に洗練された状態であること。