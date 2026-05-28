---
name: docs-test-review
description: ドキュメント・テスト品質レビュー - コメント品質、API仕様、テストの意味、カバレッジを統合評価
requires-guidelines:
  - common
---

# ドキュメント・テスト品質レビュー（統合版）

## 統合スコープ

1. **ドキュメント** - コメント品質、API仕様、型定義コメント
2. **テスト品質** - テストの意味、カバレッジ、モック適切性

## 使用タイミング

- API実装時 / 公開ライブラリ作成時
- /test, /docs コマンド実行時

---

## レビュー観点

### 🔴 Critical

| 観点 | 問題 | 対策 |
|------|------|------|
| ドキュメント | 公開API・型に説明なし | JSDoc/GoDoc追加 |
| ドキュメント | 嘘のコメント（実装と不一致） | コメント修正 |
| テスト | 意味のないテスト（`expect(user).toBeDefined()`のみ） | 実際の振る舞いをテスト |
| テスト | 実装詳細のテスト（内部関数呼び出し確認） | ユーザー視点でテスト |
| テスト | 過剰なモック（全モックで実際の動作なし） | 境界のみモック |

### 🟡 Warning

| 観点 | 問題 | 対策 |
|------|------|------|
| ドキュメント | 自明なコメント（`// カウンターをインクリメント`） | 削除 |
| ドキュメント | 不十分なエラー説明 | 具体的なエラー型明記 |
| ドキュメント | 古いTODO放置 | Issue化または実装 |
| テスト | テスト独立性欠如（共有状態） | 各テストで独立データ |
| テスト | 不安定なテスト（setTimeout依存） | イベント待機に変更 |
| テスト | カバレッジ不足（エラーケース未テスト） | 正常・異常両方テスト |

---

## 主要パターン

```typescript
// ✅ 公開API説明
/**
 * ユーザー作成
 * @throws {ValidationError} 入力データが不正な場合
 * @throws {DuplicateEmailError} メールが既存の場合
 */
function createUser(data: CreateUserInput): Promise<User>

// ✅ 実際の振る舞いをテスト
test('createUser saves user to database', async () => {
  const user = await createUser({ name: 'test' });
  const saved = await db.findUser(user.id);
  expect(saved.name).toBe('test');
});

// ✅ ユーザー視点でテスト
test('button click shows success message', () => {
  render(<Button />);
  fireEvent.click(screen.getByRole('button'));
  expect(screen.getByText('Success')).toBeInTheDocument();
});
```

---

## チェックリスト

### ドキュメント
- [ ] 公開API全てに説明があるか
- [ ] パラメータ・戻り値・エラー条件が明記されているか
- [ ] コメントと実装が一致しているか

### テスト品質
- [ ] 何をテストしているか明確か
- [ ] ユーザー視点でテストしているか
- [ ] Arrange-Act-Assertパターンか
- [ ] テストが独立しているか
- [ ] 必要最小限のモックか
- [ ] 正常系・異常系両方テストしているか

---

## 出力形式

```
## ドキュメント・テスト品質レビュー結果

### ドキュメント
🔴 **Critical**: `api.ts:45` - 公開API説明なし → JSDoc追加
🟡 **Warning**: `utils.ts:12` - 自明なコメント → 削除推奨

### テスト品質
🔴 **Critical**: `user.test.ts:20` - 意味のないテスト → 振る舞いテストに変更
🟡 **Warning**: `order.test.ts:50` - エラーケース未テスト → 追加推奨

📊 **Summary**: Critical 2件 / Warning 2件
```

---

## 関連ガイドライン

- `common/document-management.md`
- `common/testing-guidelines.md`

## 外部知識ベース（Context7）

- Microsoft/Google Writing Style Guide
- JSDoc/TSDoc/GoDoc規約
- Jest/Vitest/pytest公式ドキュメント
