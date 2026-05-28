---
name: tdd-bdd-typescript
description: TypeScriptにおけるTDD（テスト駆動開発）とBDD（振る舞い駆動開発）のスキル。Given-When-Thenスタイルでテストを記述し、Red-Green-Refactorサイクルで開発を進める。新規コード開発、レガシーコード改善、テストファースト開発、リファクタリング時に適用。Vitest/Jest環境でのTypeScript開発に最適化。
---

# TDD/BDD TypeScript開発スキル

t-wadaの「実録レガシーコード改善」の知見に基づく、TypeScriptでのテスト駆動開発ガイド。

## 核心原則

> 「テストのないコードは悪いコードである。どれだけうまく書かれているかは関係ない」
> — Michael Feathers『レガシーコード改善ガイド』

### TDDの3ステップサイクル

```
1. Red   → 失敗するテストを1つ書く
2. Green → そのテストを最小限のコードで成功させる
3. Refactor → テストが通る状態を維持してリファクタリング
```

## Given-When-Then（BDDスタイル）

テストを「仕様」として読めるように構造化する。

```typescript
describe('注文処理', () => {
  describe('在庫が十分にある場合', () => {
    it('注文が作成されること', () => {
      // Given: 事前条件
      const product = createProduct({ stock: 10 });
      const order = { productId: product.id, quantity: 3 };

      // When: テスト対象の操作
      const result = createOrder(order);

      // Then: 期待される結果
      expect(result.isOk()).toBe(true);
      expect(result.value.quantity).toBe(3);
    });
  });
});
```

### Given-When-Thenの責務

| フェーズ | 責務 | 注意点 |
|---------|------|--------|
| Given | 事前状態の構築 | テストに必要な最小限のセットアップ |
| When | テスト対象の操作（1つだけ） | 副作用を伴う操作は1回のみ |
| Then | 結果の検証 | 1テスト1アサーションが理想 |

## TDD開発ワークフロー

### フェーズ1: TODOリストの作成

実装前に「何をテストするか」をリストアップする。

```typescript
// TODO: 注文機能
// - [ ] 正常系: 在庫十分で注文作成成功
// - [ ] 異常系: 在庫不足でエラー
// - [ ] 異常系: 数量0以下でエラー
// - [ ] 境界値: 在庫ちょうどで注文成功
```

### フェーズ2: Red（失敗するテストを書く）

```typescript
describe('createOrder', () => {
  it('在庫が十分にある場合、注文が作成される', () => {
    // Given
    const getStock = () => 10;  // 接合部: ランダム性/外部依存を制御
    const orderService = createOrderService({ getStock });

    // When
    const result = orderService.create({ productId: 'p1', quantity: 3 });

    // Then
    expect(result.isOk()).toBe(true);
  });
});
```

### フェーズ3: Green（最小限の実装）

テストを通すための最小限のコードを書く。完璧を目指さない。

```typescript
function createOrderService({ getStock }: Dependencies) {
  return {
    create(input: OrderInput): Result<Order, OrderError> {
      const stock = getStock(input.productId);
      if (stock < input.quantity) {
        return err({ type: 'INSUFFICIENT_STOCK' });
      }
      return ok({ id: generateId(), ...input });
    }
  };
}
```

### フェーズ4: Refactor

テストが緑のまま、コードを改善する。

## 接合部（Seam）パターン

### なぜ接合部が重要か

> 「コードを変更するためにはテストを整備する必要がある。
> 多くの場合、テストを整備するためには、コードを変更する必要がある」
> — レガシーコードのジレンマ

接合部とは、コードを直接編集せずに振る舞いを変えられる場所。

### Humble Object Pattern

テスト困難な要素を薄く切り出し、テスト可能範囲を最大化する。

```typescript
// Before: テスト困難（ランダム性が内部に埋め込まれている）
function selectQuestion(questions: Question[]): Question {
  const index = Math.floor(Math.random() * questions.length);
  return questions[index];
}

// After: テスト容易（ランダム性を接合部として分離）
function createQuestionSelector(getNextIndex: () => number) {
  return function selectQuestion(questions: Question[]): Question {
    const index = getNextIndex();
    return questions[index];
  };
}

// 本番コード
const selectQuestion = createQuestionSelector(
  () => Math.floor(Math.random() * questions.length)
);

// テストコード
const selectQuestion = createQuestionSelector(() => 4); // 決定的
```

### 接合部の種類と対処法

| 種類 | 例 | 対処法 |
|------|-----|--------|
| ランダム性 | Math.random(), UUID | 生成関数を引数で注入 |
| 時間依存 | new Date(), Date.now() | 時刻取得関数を注入 |
| 外部API | fetch, DB接続 | インターフェースで抽象化 |
| 環境変数 | process.env | Config オブジェクトで注入 |

## テストの決定性

テストは何度実行しても同じ結果を返すべき。

```typescript
// NG: 非決定的
it('ランダムな質問が選ばれる', () => {
  const question = selectRandomQuestion(questions);
  expect(questions).toContain(question); // 検証が弱い
});

// OK: 決定的
it('指定されたインデックスの質問が選ばれる', () => {
  const getIndex = () => 2;
  const selectQuestion = createQuestionSelector(getIndex);
  
  const question = selectQuestion(questions);
  
  expect(question).toBe(questions[2]);
});
```

## テストダブル使い分け

```typescript
// Stub: 固定値を返す
const getStock = vi.fn().mockReturnValue(10);

// Spy: 呼び出しを記録
const logger = { log: vi.fn() };
expect(logger.log).toHaveBeenCalledWith('注文作成');

// Fake: 簡易実装
const fakeRepository = new Map<string, Order>();
```

## 詳細リファレンス

- TDDサイクルの詳細フロー: [references/tdd-workflow.md](references/tdd-workflow.md)
- Given-When-Thenパターン集: [references/gherkin-patterns.md](references/gherkin-patterns.md)
- レガシーコード改善手法: [references/legacy-code.md](references/legacy-code.md)
