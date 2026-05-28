---
name: typescript-strict
description: TypeScriptの設定や型エラー対応時に使用。
---

# TypeScript Strict Mode

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] TypeScriptを設定する?
- [ ] 型エラーに対応する?
- [ ] any型を削減する?
- [ ] 型安全性を向上させる?

### 前提条件
- [ ] tsconfig.jsonを確認したか?
- [ ] strictモードが有効か確認したか?
- [ ] 型定義ファイル(@types)を確認したか?

### 禁止事項の確認
- [ ] any型を使おうとしていないか?
- [ ] @ts-ignoreを安易に使おうとしていないか?
- [ ] as anyでキャストしようとしていないか?
- [ ] 型チェックをスキップしようとしていないか?

---

## トリガー

- TypeScript設定時
- 型エラー対応時
- any型削減時
- 型安全性向上時

---

## 🚨 鉄則

**anyは禁止。型で安全性を保証。**

---

## 推奨tsconfig

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true
  }
}
```

---

## any回避パターン

```typescript
// ❌ any
function process(data: any) { }

// ✅ unknown + 型ガード
function process(data: unknown) {
  if (isValidData(data)) {
    // 型が絞られる
  }
}

// ✅ ジェネリクス
function process<T>(data: T): T { }
```

---

## 型ガード

```typescript
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  );
}
```

---

## 🚫 禁止事項まとめ

- any型の使用
- @ts-ignoreの安易な使用
- as anyキャスト
- 型チェックのスキップ
