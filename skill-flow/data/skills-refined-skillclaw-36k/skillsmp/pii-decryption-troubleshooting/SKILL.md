---
name: pii-decryption-troubleshooting
description: PII暗号化/復号化の問題をトラブルシューティングするためのフロー。暗号文がそのまま表示される、復号化に失敗する等の問題を調査・解決する際に使用。
---

# PII Decryption Troubleshooting

PII（個人識別情報）暗号化/復号化の問題を調査・解決するためのトラブルシューティングガイドです。

## When to Use

- ブラウザ画面で暗号文がそのまま表示されている
- 電話番号やメールアドレスが正しく表示されない
- 復号化処理がエラーを出している
- 新規環境セットアップ後にPIIが表示されない

## Symptom-Cause Matrix

| 症状 | 原因 | 優先度 |
|------|------|--------|
| 暗号文がそのまま表示される | 環境変数 `PII_ENCRYPTION_KEY` が未設定または不正 | 高 |
| 一部のデータだけ暗号文 | 平文と暗号文が混在（移行期間中のデータ） | 中 |
| 全てのデータが復号化失敗 | キーが異なる環境で暗号化された | 高 |
| `null`が表示される | 暗号化前の値が空、または復号化エラー | 低 |

## Investigation Flow

### Step 1: ブラウザで症状を確認

1. 問題が発生しているページを開く
2. 表示されている値を確認:
   - 暗号文（例: `AbCd123...`のBase64url文字列）→ 復号化されていない
   - 正しい値（例: `09012345678`）→ 正常
   - `null`または空欄 → 元データが空か復号化エラー

### Step 2: データベースの値を確認

Supabase SQL Editorで実際の格納値を確認:

```sql
-- 例: children テーブルの guardian_phone を確認
SELECT id, guardian_phone
FROM m_children
WHERE id = 'YOUR-CHILD-UUID'
LIMIT 1;
```

確認ポイント:
- 値がBase64url形式（`AbCd...`）→ 暗号化済み
- 値が平文（`09012345678`）→ 未暗号化（移行前データ）
- 値が`null`→ データが存在しない

### Step 3: 環境変数の確認

`.env.local`ファイルを確認:

```bash
# 必須設定
PII_ENCRYPTION_KEY=<64文字の16進数文字列>
```

確認項目:
- [ ] `PII_ENCRYPTION_KEY`が設定されているか
- [ ] 値が64文字（32バイトの16進数）か
- [ ] 値が本番環境と同じキーか（既存データを復号化する場合）

### Step 4: キーの長さを検証

```bash
# .env.local の PII_ENCRYPTION_KEY の長さを確認
echo -n "YOUR_KEY_HERE" | wc -c
# 出力が64であること
```

または、アプリケーション起動時のエラーログを確認:

```
Error: PII_ENCRYPTION_KEY must be 64 hex characters (32 bytes), got XX bytes
```

## Encryption Format

### v2形式（現行）

バイナリ連結をBase64urlエンコード:

```
[IV 12B][AuthTag 12B][暗号文]
↓ Base64url encode
AbCdEfGh...
```

- **IV**: 12バイトのランダム初期化ベクトル
- **AuthTag**: 12バイトの認証タグ（GCMモード）
- **暗号文**: 可変長

### v1形式（レガシー）

コロン区切りの16進数文字列をBase64urlエンコード:

```
<IV hex>:<AuthTag hex>:<encrypted hex>
↓ Base64url encode
AbCdEfGh...
```

- **IV**: 16バイト（32文字の16進数）
- **AuthTag**: 16バイト（32文字の16進数）

**Note**: 復号化処理は両形式を自動判別して処理します。

## Implementation Patterns

### 暗号化（データ保存時）

PIIデータをデータベースに保存する際は `encryptPII()` を使用:

```typescript
import { encryptPII, generateSearchHash } from '@/utils/crypto/piiEncryption';

// API Route での保存例
async function saveChild(data: { familyName: string; phone: string }) {
  const supabase = await createClient();

  const { error } = await supabase
    .from('m_children')
    .insert({
      family_name: encryptPII(data.familyName),        // 暗号化して保存
      phone_hash: generateSearchHash(data.phone),      // 検索用ハッシュ
      guardian_phone: encryptPII(data.phone),          // 暗号化して保存
    });
}
```

**ポイント**:
- `encryptPII()`: null/空文字列の場合は`null`を返す
- `generateSearchHash()`: 検索用のSHA-256ハッシュを生成（電話番号検索等で使用）
- 同じ値でも毎回異なる暗号文になる（IVが毎回ランダム）

### 復号化（データ表示時）

APIレスポンスでPIIデータを返す際は `decryptOrFallback()` を使用:

```typescript
import { decryptOrFallback, formatName } from '@/utils/crypto/decryption-helper';

// API Route での取得例
async function getChild(childId: string) {
  const supabase = await createClient();

  const { data } = await supabase
    .from('m_children')
    .select('family_name, given_name, guardian_phone')
    .eq('id', childId)
    .single();

  // 復号化してレスポンス
  return {
    name: formatName([
      decryptOrFallback(data.family_name),
      decryptOrFallback(data.given_name),
    ]),
    phone: decryptOrFallback(data.guardian_phone),
  };
}
```

**ポイント**:
- `decryptOrFallback()`: 復号化失敗時は元の値をそのまま返す（後方互換性）
- `formatName()`: 名前パーツを結合してフォーマット
- エラーをスローしないので、移行期間中の平文データも処理可能

### バルク処理（複数レコード）

```typescript
// 複数の児童データを復号化
const children = rawChildren.map((child) => ({
  child_id: child.id,
  name: formatName([
    decryptOrFallback(child.family_name),
    decryptOrFallback(child.given_name),
  ]),
  kana: formatName([
    decryptOrFallback(child.family_name_kana),
    decryptOrFallback(child.given_name_kana),
  ]),
}));
```

### 検索パターン

暗号化されたデータは直接検索できないため、ハッシュを使用:

```typescript
import { generateSearchHash } from '@/utils/crypto/piiEncryption';

// 電話番号で検索
async function findByPhone(phone: string) {
  const phoneHash = generateSearchHash(phone);

  const { data } = await supabase
    .from('m_guardians')
    .select('*')
    .eq('phone_hash', phoneHash);  // ハッシュで検索

  return data;
}
```

## Recovery Procedures

### Case 1: キーが設定されていない

1. `.env.local`に`PII_ENCRYPTION_KEY`を追加
2. 既存データを復号化できる正しいキーを使用
3. Next.jsサーバーを再起動

```bash
# .env.local
PII_ENCRYPTION_KEY=<production-key-here>
```

### Case 2: キーが失われた（復旧不可）

**警告**: 暗号化キーが完全に失われた場合、既存の暗号化データは復号化できません。

選択肢:
1. **データ再入力**: 平文データを再度入力し、新しいキーで暗号化
2. **バックアップからキー復元**: 環境変数のバックアップがあれば復元
3. **部分的な復旧**: 平文のまま残っているデータは利用可能

### Case 3: 平文と暗号文が混在

移行期間中のデータでは、`decryptOrFallback()`を使用:

```typescript
import { decryptOrFallback } from '@/utils/crypto/decryption-helper';

// 暗号化データ → 復号化された値
// 平文データ → そのまま返す
const phone = decryptOrFallback(guardianPhone);
```

## Prevention Best Practices

### 環境変数の管理

1. **バックアップ**: `PII_ENCRYPTION_KEY`は安全な場所にバックアップ
2. **ローテーション**: キー変更時は既存データの再暗号化が必要
3. **共有**: 開発チーム間で安全にキーを共有（パスワードマネージャー等）

### 新規環境セットアップ

1. `.env.sample`を参考に`.env.local`を作成
2. 本番環境と同じ`PII_ENCRYPTION_KEY`を設定（既存データ復号化のため）
3. サーバー起動前に環境変数が正しく読み込まれることを確認

### デバッグ用チェックリスト

- [ ] `.env.local`に`PII_ENCRYPTION_KEY`が存在する
- [ ] キーが64文字の16進数である
- [ ] サーバー再起動後に変更が反映されている
- [ ] データベースの値が暗号化形式か平文か確認した
- [ ] APIレスポンスで復号化処理が呼ばれているか確認した

## Related Files

| File | Description |
|------|-------------|
| `utils/crypto/piiEncryption.ts` | 暗号化/復号化のコア実装 |
| `utils/crypto/decryption-helper.ts` | 復号化ヘルパー関数（`decryptOrFallback`） |
| `.env.sample` | 環境変数のサンプル |

## Related Skills

- `supabase-query-patterns` - データベースクエリのパターン
- `supabase-jwt-auth` - JWT認証のトラブルシューティング
