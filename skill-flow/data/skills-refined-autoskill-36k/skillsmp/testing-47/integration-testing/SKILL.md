---
name: integration-testing
description: 統合テスト設計・実装。コンポーネント間連携とデータフロー検証。
---

# Integration Testing

## トリガー

- コンポーネント連携の検証
- API境界のテスト
- データフロー確認

---

## 基本原則

**境界を跨ぐ振る舞いを検証。内部実装は問わない。**

| 項目 | 基準 |
|------|------|
| 件数 | 3-8件/コンポーネント境界 |
| 対象 | インターフェース契約 |
| 実行時間 | 1件5秒以内目標 |

---

## テスト層の実行順序

```text
1. Database Layer
2. Repository/DAO Layer
3. Service Layer
4. API Layer
5. Frontend Integration
```

**前の層が安定するまで次に進まない。**

---

## 必須テスト対象

### Database統合

| 対象 | 検証内容 |
|------|----------|
| CRUD | 作成・読取・更新・削除 |
| トランザクション | コミット・ロールバック |
| 制約 | UNIQUE, FK, NOT NULL |
| マイグレーション | スキーマ変更の正確性 |

### API統合

| 対象 | 検証内容 |
|------|----------|
| 正常系 | 期待レスポンス |
| 異常系 | エラーコード・メッセージ |
| 認証 | トークン検証 |
| バリデーション | 入力制約 |

### 外部サービス

| 対象 | 検証内容 |
|------|----------|
| 接続 | タイムアウト処理 |
| リトライ | 再試行ロジック |
| フォールバック | 代替処理 |

---

## テスト設計チェックリスト

### 作成前

- [ ] コンポーネント境界を特定したか?
- [ ] インターフェース契約を理解したか?
- [ ] Usefulness Score ≥12 か?
- [ ] Unitで十分でないか?

### 作成中

- [ ] 実DBを使用しているか? (インメモリ非推奨)
- [ ] テストデータは独立しているか?
- [ ] トランザクション分離は適切か?
- [ ] クリーンアップ処理があるか?

### 作成後

- [ ] 単独実行で成功するか?
- [ ] 並列実行で競合しないか?
- [ ] 失敗理由が特定可能か?

---

## 構造パターン

```typescript
describe('Integration: [Component A] → [Component B]', () => {
  let db: Database;
  let service: Service;

  beforeAll(async () => {
    db = await createTestDatabase();
    service = new Service(db);
  });

  afterAll(async () => {
    await db.cleanup();
  });

  beforeEach(async () => {
    await db.truncateAll();
  });

  describe('正常系', () => {
    it('should [expected behavior]', async () => {
      // Arrange: テストデータ投入
      await db.insert('users', testUser);

      // Act: 境界を跨ぐ操作
      const result = await service.process(input);

      // Assert: 結果検証
      expect(result).toEqual(expected);

      // Assert: 副作用検証
      const dbState = await db.query('SELECT * FROM users');
      expect(dbState).toContain(expectedRecord);
    });
  });

  describe('異常系', () => {
    it('should handle [error case]', async () => {
      // エラー条件設定
      // 操作実行
      // エラー検証
    });
  });
});
```

---

## モック戦略

| 対象 | 方針 |
|------|------|
| 内部コンポーネント | モックしない |
| DB | 実DB使用 (Dockerized) |
| 外部API | モック化 |
| 時刻 | モック化 |
| ランダム | シード固定 |

**原則**: 境界内は実物、境界外はモック。

---

## テスト環境

```yaml
# docker-compose.test.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: test
    tmpfs: /var/lib/postgresql/data  # 高速化
```

---

## 禁止事項

- ❌ インメモリDB使用 (本番との乖離)
- ❌ モック過多 (統合テストの意味喪失)
- ❌ テスト間でのDB状態共有
- ❌ 固定IDのハードコード
- ❌ 8件超/境界

---

## 品質ゲート

| 指標 | 閾値 |
|------|------|
| 成功率 | 100% |
| 実行時間 | 2分以内/スイート |
| カバレッジ | 境界100% |
