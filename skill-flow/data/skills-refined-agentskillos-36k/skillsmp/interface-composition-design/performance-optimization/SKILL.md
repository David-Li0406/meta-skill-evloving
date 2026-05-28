---
name: performance-optimization
description: パフォーマンス最適化やプロファイリング時に使用。計測とよくあるボトルネックをカバー。
---

# Performance Optimization

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] パフォーマンス問題が発生している?
- [ ] ボトルネックを調査する?
- [ ] クエリを最適化する?
- [ ] プロファイリングを実施する?

### 前提条件
- [ ] 計測してから最適化しているか?
- [ ] ボトルネックを特定したか?
- [ ] 最適化の目標値を設定したか?

### 禁止事項の確認
- [ ] 計測なしで最適化しようとしていないか?
- [ ] 推測だけで「遅い」と判断していないか?
- [ ] 早すぎる最適化をしていないか?

---

## トリガー

- パフォーマンス問題発生時
- ボトルネック調査時
- クエリ最適化時
- プロファイリング実施時

---

## 🚨 鉄則

**計測なき最適化は推測。Profile → Measure → Optimize → Verify**

---

## プロファイリング

```bash
# Node.js
node --prof app.js

# Python
python -m cProfile -o output.prof script.py
```

---

## よくあるボトルネック

### N+1クエリ

```typescript
// ❌ N+1
for (const user of users) {
  const posts = await db.posts.find({ userId: user.id });
}

// ✅ 一括取得
const posts = await db.posts.find({ userId: { $in: userIds } });
```

### 不要な再レンダリング(React)

```typescript
// ❌ 毎回新しいオブジェクト
<Component style={{ color: 'red' }} />

// ✅ メモ化
const style = useMemo(() => ({ color: 'red' }), []);
<Component style={style} />
```

---

## 計測ツール

- ブラウザ: Chrome DevTools Performance
- Node.js: clinic.js, 0x
- DB: EXPLAIN ANALYZE

---

## 🚫 禁止事項まとめ

- 計測なしの最適化
- 推測だけの判断
- 早すぎる最適化
- 最適化後の検証忘れ
