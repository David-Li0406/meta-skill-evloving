---
name: tdd
description: TDD（テスト駆動開発）ルール。t-wada式のRed-Green-Refactorサイクル、三角測量、ベイビーステップなどの手法を定義。TDD実践時に参照。
---

# TDD（テスト駆動開発）ルール

t-wada式テスト駆動開発の手法を定義するスキル。

## 基本理念

- **テストファースト**: 実装前に必ずテストを書く
- **Red-Green-Refactor**: 失敗 → 成功 → 改善のサイクル
- **ベイビーステップ**: 小さな一歩ずつ進む
- **意図を表明**: テストでコードの意図を明確に示す

## TDDサイクル

### 1. Red（レッド）
まず失敗するテストを書く

```typescript
test("2つの数を足すことができる", () => {
  const calculator = new Calculator();
  expect(calculator.add(2, 3)).toBe(5);
});
// → Calculatorクラスは存在しない → テスト失敗
```

### 2. Green（グリーン）
テストが通る最小限のコードを書く

```typescript
class Calculator {
  add(a: number, b: number): number {
    return 5; // 仮実装
  }
}
```

### 3. Refactor（リファクタ）
重複を排除し、コードを改善

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b; // 三角測量で正しい実装へ
  }
}
```

## 三角測量

```typescript
// 1つ目のテスト
test("2 + 3 = 5", () => {
  expect(calculator.add(2, 3)).toBe(5);
});
// 仮実装: return 5;

// 2つ目のテスト（三角測量）
test("3 + 4 = 7", () => {
  expect(calculator.add(3, 4)).toBe(7);
});
// → 一般化が必要になり return a + b; へ
```

## テストの粒度

```typescript
// ❌ 粗すぎる
test("ユーザー管理機能", () => { /* 全部テスト */ });

// ✅ 適切
test("ユーザーを作成できる", () => { ... });
test("ユーザーを更新できる", () => { ... });
```

## 明確なテスト名

```typescript
// ❌ 曖昧
test("ユーザーテスト", () => {});

// ✅ 明確
test("有効な名前でユーザーを作成できる", () => {});
test("空の名前でユーザー作成時にエラーが発生する", () => {});
```

## 実行手順

1. 空の関数・クラスのスケルトンを作成
2. テストを書く
3. `pnpm test` でテスト失敗を確認（Red）
4. テストが通る最小限のコードを実装（Green）
5. `pnpm test` でテストパスを確認
6. 必要に応じてリファクタリング（Refactor）

## デイリーチェック

- [ ] 新機能は必ずテストから開始
- [ ] テストが失敗することを確認してから実装
- [ ] 仮実装から始めて段階的に一般化
- [ ] グリーンになったらリファクタを検討
- [ ] テストが文書として機能しているか確認
