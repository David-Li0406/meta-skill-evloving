---
name: ssot-verification
description: Replaces the task of strictly verifying whether proposals or deliverables conceptually align with the project's Single Source of Truth (SSOT). Typical use cases: (1) Confirming new design proposals do not violate past ADRs or design principles, (2) Checking ubiquitous language consistency and system boundary compliance, (3) Outputting findings with logical reasoning to guarantee consistency.
---

# SSOTとの整合性検証プロトコル (Conceptual Integrity & Scrutiny)

設計や計画の妥当性を保証するため、既読・未読にかかわらず、以下の手順で「立ち止まって再検証」することを標準化する。

## 手順

1. **重要ドキュメントの再読 (Fresh Read):**
   - `docs/system-context.md` や `reqs/design/_approved/` 以下の**関連するSSOT（承認済みADRを含む）**、およびIssue等で指定されている関連ドキュメントを、**新規に `read_file` で読み込む**。
   - 以前のターンで読み込んでいても、キャッシュに頼らず最新の状態を確認することを優先する。

2. **ドメイン観点での精査 (Scrutiny):**
   - 読み込んだドキュメントと現在の提案内容（または成果物）を突き合わせ、以下のチェックリストで精査する。
     - [ ] **用語の一貫性:** ユビキタス言語から逸脱していないか？
     - [ ] **境界の遵守:** システム境界（In-Scope/Out-of-Scope）を侵していないか？
     - [ ] **原則の継承:** 過去の ADR で決定した設計原則や戦略的トレードオフに反していないか？
     - [ ] **要件の充足:** SSOTで定義された機能要件・非機能要件を満たしているか？
     - [ ] **アーキテクチャ整合性:** 既存のコンポーネント構成やデータフローと矛盾していないか？
     - [ ] **セキュリティとコンプライアンス:** 既存のセキュリティポリシーや制約事項に違反していないか？
     - [ ] **検証可能性:** テスト可能な設計になっているか？（テスト戦略との整合性）

3. **考察結果の出力 (Synthesis):**
   - 前段の精査（Scrutiny）結果に基づき、単に「矛盾なし」とするのではなく、以下の観点を含めた論理的な考察（思考プロセス）を詳細に出力する。
   - **考察の観点:**
     - **具体的根拠:** どのドキュメントのどの記述に基づいているか。
     - **トレードオフ:** 検討した代案や、選択に伴うメリット・デメリット。
     - **一貫性の結論:** 全体最適の観点から、今回の設計/成果物が SSOT とどう調和するか。

   - **アウトプット形式 (Markdown):**

     ```markdown
     ### 整合性検証結果

     - **具体的根拠:** [ドキュメント名]の「[セクション名]」における「[具体的な記述]」に基づき、今回の設計は適切である。なぜなら...
     - **トレードオフの検討:** [代案A]も検討したが、[制約事項]を考慮し、[設計方針]との整合性が高い[現在の案]を選択した。
     - **一貫性の保証:** 今回の変更はシステム境界を遵守しており、既存の原則である[原則名]を正しく継承している。
     ```
