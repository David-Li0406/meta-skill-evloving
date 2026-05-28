---
name: testing
description: 単体テストルール。フラット構造、モック使用制限、パラメータ化テスト、テストピラミッドなどの規約を定義。Vitest/Jest使用時に参照。
---

# 単体テストルール

単体テスト実装における規約を定義するスキル。

## 基本ルール

- **網羅テスト**: 正常系・異常系・境界値のテストケースを作成
- **振る舞いのテスト**: 実装詳細ではなく振る舞いを確認
- **モックは最小限**: 基本はモックを使用しない
- **フラット構造**: describeブロックの過度な使用を避ける
- **テストケース名**: 日本語で記述
- **パラメータ化**: `test.each` を活用

## テスト構造（フラット原則）

```typescript
// ✅ 推奨: describeなしのフラット構造
test("有効な認証情報でログインするとトークンが返る", () => {
  const result = login({ email: "test@example.com", password: "valid" });
  expect(result.token).toBeDefined();
});

test("無効なメールではValidationErrorが発生する", () => {
  expect(() => login({ email: "invalid", password: "valid" }))
    .toThrow(ValidationError);
});
```

## モックルール

### モック禁止対象
- 自作の関数・コンポーネント
- プロジェクト内のユーティリティ関数
- 内部状態管理ロジック

### モック許可対象
- HTTPリクエスト（fetch、axiosなど）
- 外部API呼び出し
- ファイルシステムアクセス
- データベース接続
- 時間依存処理（Date、setTimeoutなど）

## パラメータ化テスト

```typescript
test.each([
  [1, 2, 3],
  [5, 5, 10],
  [-1, 1, 0],
])("add(%i, %i) は %i を返す", (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

## テストピラミッド

| レベル | 比率 | 対象 |
|:-|:-|:-|
| 単体テスト | 70-80% | 関数、メソッド、個別コンポーネント |
| 統合テスト | 15-25% | モジュール間連携、API統合 |
| E2Eテスト | 5-10% | ユーザーシナリオ全体 |

## ディレクトリ構成

```
__tests__/
├── user-login.test.ts
├── user-registration.test.ts
├── user-profile.test.ts
└── helpers/
    └── user-test-utils.ts
```

## 適正化指針

- **重複テストの排除**: 同じ振る舞いを複数方法でテストしない
- **実装詳細のテスト禁止**: privateメソッドや内部状態の直接テストは行わない
- **公開インターフェースのみテスト**: 外部から呼び出される関数に集中
- **ファイル分割**: 100-150行を超えたら分割

## 関連スキル

- TDD: `tdd`
- カスタムフック: `custom-hook`
