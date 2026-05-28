# {機能名} - 技術設計

**ステータス**: 下書き | レビュー中 | 承認済み
**作成日**: {YYYY-MM-DD}
**最終更新日**: {YYYY-MM-DD}
**要件**: [requirements.md](./requirements.md)

---

## 1. アーキテクチャ概要

### システムフロー

<!-- 処理の流れをステップで記述 -->

1. <!-- ステップ1 -->
2. <!-- ステップ2 -->
3. <!-- ステップ3 -->

### 主要コンポーネント

| コンポーネント | パス | 責務 |
|---------------|------|------|
| <!-- 名前 --> | `@/path/to/file` | <!-- 役割の説明 --> |
| <!-- 名前 --> | `@/path/to/file` | <!-- 役割の説明 --> |

---

## 2. データ設計

### 新規/変更テーブル

```sql
-- 例: 新規テーブル
CREATE TABLE entity_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    field_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP  -- 論理削除
);

-- インデックス
CREATE INDEX idx_entity_user ON entity_name(user_id);
```

### Prismaスキーマ

```prisma
model EntityName {
  id        String   @id @default(uuid())
  userId    String   @map("user_id")
  fieldName String   @map("field_name")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  user User @relation(fields: [userId], references: [id])

  @@map("entity_name")
}
```

### 既存テーブルへの影響

- [ ] 影響なし
- [ ] 以下のテーブルに影響:
  - `table_name`: <!-- 変更内容 -->

---

## 3. API設計

### エンドポイント一覧

| メソッド | パス | 説明 | 認証 |
|----------|------|------|------|
| POST | `/api/resource` | リソース作成 | 必須 |
| GET | `/api/resource/{id}` | リソース取得 | 必須 |
| PUT | `/api/resource/{id}` | リソース更新 | 必須 |
| DELETE | `/api/resource/{id}` | リソース削除 | 必須 |

### リクエスト/レスポンス型

```typescript
// POST /api/resource - リクエスト
const CreateResourceSchema = z.object({
  field: z.string().min(1).max(255),
});
type CreateResourceRequest = z.infer<typeof CreateResourceSchema>;

// レスポンス
interface ResourceResponse {
  id: string;
  field: string;
  createdAt: string;
  updatedAt: string;
}
```

### エラーハンドリング

| エラーコード | HTTPステータス | 説明 |
|-------------|----------------|------|
| RESOURCE_NOT_FOUND | 404 | リソースが存在しない |
| VALIDATION_ERROR | 400 | 入力が無効 |
| UNAUTHORIZED | 401 | 認証エラー |
| FORBIDDEN | 403 | 権限エラー |

---

## 4. UI設計

### 画面構成

<!-- 追加/変更する画面とその概要 -->

### コンポーネント構成

<!-- 新規作成するコンポーネントと既存コンポーネントとの関係 -->

```
ParentComponent
├── NewComponent
│   ├── SubComponentA
│   └── SubComponentB
└── ExistingComponent（修正）
```

### 状態管理

<!-- フロントエンドの状態管理方針 -->

---

## 5. セキュリティとパフォーマンス

### セキュリティ考慮事項

- [ ] 認証: `authenticateRequest()` 使用
- [ ] 認可: ユーザー所有データのみアクセス可能
- [ ] 入力検証: Zodスキーマでバリデーション
- [ ] <!-- その他の考慮事項 -->

### パフォーマンス考慮事項

- [ ] インデックス設計: <!-- 対象カラム -->
- [ ] クエリ最適化: <!-- 必要な対応 -->
- [ ] キャッシュ: <!-- 戦略 -->

---

## 6. テスト戦略

### テスト方針

**TDDアプローチ**: 厳格（Red-Green-Refactor）
**カバレッジ目標**: 80%

### テスト対象一覧

| 対象 | ファイルパス | テストファイル | 優先度 |
|------|-------------|---------------|--------|
| <!-- APIルート --> | `src/app/api/resource/route.ts` | `route.test.ts` | 必須 |
| <!-- カスタムフック --> | `src/hooks/useResource.ts` | `useResource.test.ts` | 必須 |
| <!-- コンポーネント --> | `src/components/ResourceForm.tsx` | `ResourceForm.test.tsx` | 推奨 |
| <!-- ユーティリティ --> | `src/utils/resourceHelper.ts` | `resourceHelper.test.ts` | 推奨 |

### テストケース詳細

#### APIルート: `POST /api/resource`

**正常系**:
- [ ] 有効なリクエストで201を返す
- [ ] 作成されたリソースがレスポンスに含まれる
- [ ] DBにレコードが保存される

**異常系**:
- [ ] 認証なしで401を返す
- [ ] 無効なリクエストボディで400を返す
- [ ] 存在しないリソース参照で404を返す
- [ ] 権限エラーで403を返す

**境界値**:
- [ ] 文字列長の上限（255文字）
- [ ] 文字列長の下限（1文字）

#### カスタムフック: `useResource`

**状態管理**:
- [ ] 初期状態が正しい（data: null, loading: true, error: null）
- [ ] データ取得後に状態が更新される
- [ ] ローディング状態が正しく遷移する

**エラーハンドリング**:
- [ ] APIエラー時にerror状態になる
- [ ] ネットワークエラー時にerror状態になる

#### コンポーネント: `ResourceForm`

**レンダリング**:
- [ ] 初期状態で正しくレンダリングされる
- [ ] ローディング状態でスピナーが表示される
- [ ] エラー状態でエラーメッセージが表示される

**ユーザー操作**:
- [ ] フォーム入力が正しく動作する
- [ ] 送信ボタンクリックでAPIが呼ばれる
- [ ] バリデーションエラーが表示される
- [ ] 成功時にコールバックが呼ばれる

### モック戦略

| 依存 | モック方法 | 備考 |
|------|-----------|------|
| Prisma | `jest.mock('@/utils/prisma')` | `__mocks__/prisma.ts` 使用 |
| Supabase Auth | `jest.mock('@/utils/supabase-server')` | `__mocks__/supabase.ts` 使用 |
| Next.js Router | jest.setup.ts で設定済み | 自動適用 |
| API呼び出し | `jest.fn()` | 各テストで設定 |

### テストファイル命名規則

- コンポーネント: `ComponentName.test.tsx`（同階層に配置）
- カスタムフック: `useHookName.test.ts`（同階層に配置）
- APIルート: `route.test.ts`（同階層に配置）
- ユーティリティ: `utilName.test.ts`（同階層に配置）

---

## 7. 影響範囲

### 直接影響を受けるファイル

| ファイル | 変更内容 | 影響レベル |
|----------|----------|-----------|
| `path/to/file` | <!-- 変更内容 --> | Critical / High / Medium / Low |

### 間接的に影響を受ける可能性のあるファイル

- `path/to/file` - <!-- 確認が必要な理由 -->

---

## 8. リスクと代替案

### リスク

| リスク | 影響度 | 軽減策 |
|--------|--------|--------|
| <!-- リスク1 --> | 高 / 中 / 低 | <!-- 軽減策 --> |

### 検討した代替案

#### 代替案A: {名前}

- **説明**: <!-- 概要 -->
- **メリット**: <!-- 利点 -->
- **デメリット**: <!-- 欠点 -->
- **却下理由**: <!-- 選択しなかった理由 -->

---

## 9. 未解決の質問

- [ ] <!-- 質問1 -->
- [ ] <!-- 質問2 -->

---

## 参考資料

- <!-- 関連ドキュメントへのリンク -->
- <!-- 参考実装へのリンク -->
