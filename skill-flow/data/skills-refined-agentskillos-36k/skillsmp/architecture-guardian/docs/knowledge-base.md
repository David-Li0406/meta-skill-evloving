# 知識ベース

ArchitectureGuardianが参照するプロジェクトドキュメント一覧。

## 必須ドキュメント

設計思想の定義源となる必須ドキュメント。

### 基本原則

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `README.md` | プロジェクト概要、要件単純化原則 | 設計提案時、教育時 |
| `CLAUDE.md` | Claudeとの協調開発のルール、Remix特性 | 全フェーズ |

### アーキテクチャ

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `docs/ARCHITECTURE_MANIFESTO2.md` | 3大層アーキテクチャの詳細定義 | 設計提案時、違反検出時、教育時 |
| `develop/service-name/GUIDING_PRINCIPLES.md` | Outside-In TDDの実践ガイド | 設計提案時、TDDチェック時 |

### テスト

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `docs/E2E_TEST_CRITERIA.md` | E2Eテストの基準 | TDDチェック時、設計提案時 |
| `docs/ユニットテストの最低基準.md` | ユニットテストの基準 | TDDチェック時 |
| 各機能の `TDD_WORK_FLOW.md` | 機能ごとのTDDフロー | 設計提案時 |

### スタイリング

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `docs/design-token-specification.md` | デザイントークンの定義 | デザイントークンチェック時、設計提案時 |
| `docs/CSS_structure/STYLING_CHARTER.md` | スタイリング規律の詳細 | デザイントークンチェック時 |

### テンプレート

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `scripts/generate/config.json` | テンプレート定義 | 設計提案時、テンプレート起点チェック時 |
| `scripts/generate/README.md` | テンプレート使用方法 | 設計提案時 |

### サブエージェント

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| `docs/agents/README.md` | サブエージェント構成 | サブエージェント推薦時 |

## 外部参照

### Remix公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://remix.run> | 基本原則の確認 |
| **loader/action** | <https://remix.run/docs/en/main/route/loader> | Remixアーキテクチャチェック時 |
| **段階的強化** | <https://remix.run/docs/en/main/guides/progressive-enhancement> | Remixアーキテクチャチェック時 |
| **フォーム** | <https://remix.run/docs/en/main/components/form> | Remixアーキテクチャチェック時 |

### Cloudflare Pages

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://pages.cloudflare.com> | デプロイ環境の理解 |

## ドキュメントの読み込み順序

設計提案時の推奨読み込み順序：

1. `README.md` - プロジェクト概要の把握
2. `CLAUDE.md` - 開発規範の確認
3. `docs/ARCHITECTURE_MANIFESTO2.md` - 3大層の理解
4. `develop/service-name/GUIDING_PRINCIPLES.md` - TDDフローの確認
5. `scripts/generate/config.json` - 使用可能なテンプレートの確認

違反検出時の推奨読み込み順序：

1. `docs/ARCHITECTURE_MANIFESTO2.md` - 3大層の違反チェック
2. `docs/design-token-specification.md` - スタイリング規約の確認
3. Remix公式ドキュメント - Remix原則の確認

## ドキュメント更新時の対応

プロジェクトドキュメントが更新された場合、ArchitectureGuardianの知識も自動的に更新されます。

**重要な更新**:
- 3大層アーキテクチャの変更 → `docs/ARCHITECTURE_MANIFESTO2.md`
- テンプレート追加 → `scripts/generate/config.json`
- 新しいサブエージェント追加 → `docs/agents/README.md`

更新時はこの`knowledge-base.md`も併せて更新してください。

## クイックリファレンス

よく参照するドキュメントのクイックリンク：

| 用途 | ドキュメント |
| :--- | :--- |
| 3大層の責務を確認したい | `docs/ARCHITECTURE_MANIFESTO2.md` |
| TDDフローを確認したい | `develop/service-name/GUIDING_PRINCIPLES.md` |
| テンプレートを確認したい | `scripts/generate/config.json` |
| スタイリング規則を確認したい | `docs/CSS_structure/STYLING_CHARTER.md` |
| E2Eテストの書き方を確認したい | `docs/E2E_TEST_CRITERIA.md` |
| Remixの使い方を確認したい | <https://remix.run/docs> |
