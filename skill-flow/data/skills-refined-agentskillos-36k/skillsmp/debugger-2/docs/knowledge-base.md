# 知識ベース

Debuggerが参照するプロジェクトドキュメント一覧。

## 必須ドキュメント

デバッグ時に常に参照すべき必須ドキュメント。

### アーキテクチャ

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| **ARCHITECTURE_MANIFESTO2.md** | 3大層アーキテクチャの詳細定義 | レイヤー判定時、アーキテクチャ違反の確認時 |
| **CLAUDE.md** | Claudeとの協調開発のルール | 全フェーズ |

**参照先**: `docs/ARCHITECTURE_MANIFESTO2.md`

**重要な確認項目**:
- lib層の責務（純粋関数のみ）
- data-io層の責務（副作用のみ）
- ui層の責務（ユーザーインターフェース）
- 層間の依存関係

### テスト

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| **TDD_WORK_FLOW.md** | TDDフローの定義 | テスト失敗時、テスト戦略策定時 |
| **E2E_TEST_CRITERIA.md** | E2Eテストの基準 | E2Eテスト失敗時 |
| **ユニットテストの最低基準.md** | ユニットテストの基準 | ユニットテスト失敗時 |

**参照先**:
- `develop/service-name/*/TDD_WORK_FLOW.md`（各機能ごと）
- `docs/E2E_TEST_CRITERIA.md`
- `docs/ユニットテストの最低基準.md`

**重要な確認項目**:
- Outside-In TDDのフロー
- E2Eテストの成功/失敗シナリオ
- ユニットテストのカバレッジ基準（80%以上）

### プロジェクト基本

| ドキュメント | 内容 | 参照タイミング |
| :--- | :--- | :--- |
| **README.md** | プロジェクト概要 | 全体像の把握時 |
| **package.json** | 依存関係、スクリプト | ビルドエラー、依存関係エラー時 |

---

## デバッグタイプ別の参照ドキュメント

### runtime-error（実行時エラー）

**参照**:
- `docs/ARCHITECTURE_MANIFESTO2.md` - レイヤー判定
- TypeScript公式ドキュメント - 型エラーの理解

### test-failure（テスト失敗）

**参照**:
- `develop/service-name/*/TDD_WORK_FLOW.md` - TDDフロー確認
- `docs/E2E_TEST_CRITERIA.md` - E2Eテスト基準
- `docs/ユニットテストの最低基準.md` - ユニットテスト基準

### type-error（TypeScriptエラー）

**参照**:
- TypeScript公式ドキュメント
- `tsconfig.json` - TypeScript設定

### build-error（ビルドエラー）

**参照**:
- `package.json` - 依存関係確認
- `tsconfig.json` - ビルド設定
- Remix公式ドキュメント - Remixビルド仕様

### logic-error（ロジックエラー）

**参照**:
- `docs/ARCHITECTURE_MANIFESTO2.md` - lib層の責務確認
- `develop/service-name/*/TDD_WORK_FLOW.md` - テスト駆動開発

### integration-error（統合エラー）

**参照**:
- API仕様ドキュメント
- `app/data-io/` - data-io層の実装パターン

### performance-issue（パフォーマンス問題）

**参照**:
- Remix公式ドキュメント - パフォーマンス最適化
- React公式ドキュメント - レンダリング最適化

---

## 外部参照

### Remix公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://remix.run> | Remix関連エラー時 |
| **loader/action** | <https://remix.run/docs/en/main/route/loader> | データ取得エラー時 |
| **エラーハンドリング** | <https://remix.run/docs/en/main/route/error-boundary> | UIエラー時 |
| **パフォーマンス** | <https://remix.run/docs/en/main/guides/performance> | パフォーマンス問題時 |

### React公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://react.dev> | React関連エラー時 |
| **Hooks** | <https://react.dev/reference/react> | Hook使用エラー時 |
| **パフォーマンス** | <https://react.dev/learn/render-and-commit> | レンダリング問題時 |

### TypeScript公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://www.typescriptlang.org> | 型エラー時 |
| **Handbook** | <https://www.typescriptlang.org/docs/handbook/intro.html> | 型システムの理解 |
| **Playground** | <https://www.typescriptlang.org/play> | 型推論の確認 |

### Vitest公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://vitest.dev> | テストエラー時 |
| **API** | <https://vitest.dev/api/> | テストAPI確認時 |
| **UIモード** | <https://vitest.dev/guide/ui.html> | デバッグ時 |

### Playwright公式ドキュメント

| トピック | URL | 参照タイミング |
| :--- | :--- | :--- |
| **公式トップ** | <https://playwright.dev> | E2Eテストエラー時 |
| **デバッグ** | <https://playwright.dev/docs/debug> | E2Eデバッグ時 |
| **Trace Viewer** | <https://playwright.dev/docs/trace-viewer> | トレース確認時 |

---

## ドキュメントの読み込み順序

### エラー診断時（01-diagnose.md）

1. **エラーメッセージの確認**
2. **レイヤー判定**: `docs/ARCHITECTURE_MANIFESTO2.md`
3. **環境情報の確認**: `package.json`, `tsconfig.json`

### 根本原因分析時（02-analyze.md）

1. **レイヤー別の問題確認**: `docs/ARCHITECTURE_MANIFESTO2.md`
2. **TDDフロー確認**: `develop/service-name/*/TDD_WORK_FLOW.md`
3. **テスト基準確認**: `docs/E2E_TEST_CRITERIA.md`, `docs/ユニットテストの最低基準.md`

### 修正案生成時（03-fix.md）

1. **レイヤー別のベストプラクティス**: `docs/ARCHITECTURE_MANIFESTO2.md`
2. **テスト戦略**: `develop/service-name/*/TDD_WORK_FLOW.md`
3. **外部ドキュメント**: Remix/React/TypeScript公式

---

## クイックリファレンス

よく参照するドキュメントのクイックリンク。

| 用途 | ドキュメント |
| :--- | :--- |
| レイヤー判定 | `docs/ARCHITECTURE_MANIFESTO2.md` |
| TDDフロー確認 | `develop/service-name/*/TDD_WORK_FLOW.md` |
| E2Eテスト基準 | `docs/E2E_TEST_CRITERIA.md` |
| ユニットテスト基準 | `docs/ユニットテストの最低基準.md` |
| Remixエラー処理 | <https://remix.run/docs/en/main/route/error-boundary> |
| React Hooks | <https://react.dev/reference/react> |
| TypeScript型システム | <https://www.typescriptlang.org/docs/handbook/intro.html> |

---

## ドキュメント更新時の対応

プロジェクトドキュメントが更新された場合、Debuggerの知識も自動的に更新されます。

**重要な更新**:
- 3大層アーキテクチャの変更 → `docs/ARCHITECTURE_MANIFESTO2.md`
- TDDフローの変更 → `develop/service-name/*/TDD_WORK_FLOW.md`
- テスト基準の変更 → `docs/E2E_TEST_CRITERIA.md`, `docs/ユニットテストの最低基準.md`

更新時はこの`knowledge-base.md`も併せて更新してください。

---

## 関連スキル

| スキル | 連携タイミング |
| :--- | :--- |
| **ArchitectureGuardian** | アーキテクチャ違反の確認 |
| **CodeReviewer** | 修正後のレビュー依頼 |
| **GeneratorMaintainer** | テンプレート起因のバグ時 |
| **GeneratorOperator** | ファイル生成後のテスト失敗時 |
