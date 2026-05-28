---
name: caching
description: キャッシュ、Redis、キャッシュ無効化を実装する際に使用。
---

# Caching

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] キャッシュ戦略を検討する?
- [ ] Redisを導入する?
- [ ] パフォーマンス改善でキャッシュを検討する?
- [ ] キャッシュ無効化を実装する?

### 前提条件
- [ ] キャッシュが本当に必要か確認したか?(複雑さ増加)
- [ ] キャッシュ対象のデータ特性を把握しているか?
- [ ] TTL(有効期限)を検討したか?
- [ ] 無効化タイミングを明確にしたか?

### 禁止事項の確認
- [ ] 機密情報(パスワード、トークン)をキャッシュしようとしていないか?
- [ ] 無限TTLを設定しようとしていないか?
- [ ] キャッシュ無効化を忘れていないか?
- [ ] データ更新時のキャッシュ削除を考慮しているか?

---

## トリガー

- キャッシュ戦略検討時
- Redis導入時
- パフォーマンス改善でキャッシュ検討時
- キャッシュ無効化の実装時

---

## 🚨 鉄則

**キャッシュは複雑さを増す。本当に必要か確認。**

---

## キャッシュ戦略

### Cache-Aside (Lazy Loading)

```typescript
async function getData(key: string) {
  // 1. キャッシュ確認
  const cached = await cache.get(key);
  if (cached) return cached;
  
  // 2. DBから取得
  const data = await db.find(key);
  
  // 3. キャッシュに保存
  await cache.set(key, data, { ttl: 3600 });
  return data;
}
```

### Write-Through

```typescript
async function saveData(key: string, data: Data) {
  // DB保存と同時にキャッシュ更新
  await db.save(key, data);
  await cache.set(key, data);
}
```

---

## ⚠️ キャッシュ無効化

```typescript
// 更新時は必ず無効化
async function updateUser(id: string, data: UserUpdate) {
  await db.users.update(id, data);
  await cache.del(`user:${id}`);       // ⚠️ 忘れずに
  await cache.del(`user:${id}:profile`);
}
```

---

## TTL設定

```typescript
// データ特性に応じて設定
cache.set('static-config', data, { ttl: 86400 });  // 1日
cache.set('user-session', data, { ttl: 3600 });    // 1時間
cache.set('rate-limit', data, { ttl: 60 });        // 1分
```

---

## Redis基本

```typescript
import Redis from 'ioredis';
const redis = new Redis(process.env.REDIS_URL);

await redis.set('key', JSON.stringify(data), 'EX', 3600);
const data = JSON.parse(await redis.get('key') || 'null');
```

---

## 🚫 禁止事項まとめ

- 機密情報をキャッシュ(パスワード、トークン)
- 無限TTL(メモリリーク)
- キャッシュ無効化忘れ(古いデータ表示)
- 更新時のキャッシュ削除漏れ
