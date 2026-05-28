# cga-programming 詳細ガイド

AIが自律的にTDDで実装する。

## 実行フロー

```
1. 計画ファイル（doc/plans/*.md）を読み込む
2. Tidy First? 判断
   ├─ 構造の問題あり → /cga-tf-refactoring で整理
   └─ 問題なし → 次へ
3. RED: 失敗するテストを書く
4. GREEN: 最小限の実装で通す
5. REFACTOR: コードを整理
6. 3-5を繰り返す
7. 全テスト・型チェック・リント通過を確認
```

## 基本ルール

- テストファイル: `__tests__/*.test.ts`（対象モジュールと同階層の `__tests__/` ディレクトリに配置）
- カバレッジ80%以上必須
- UseCaseはSQLiteインメモリDB推奨、モックは外部APIのみ
- コミットはこまめに（RED→GREEN→REFACTORごと）
- 実装完了後は全テスト・型チェック・リント通過を最終確認

---

## Tidy First?（ステップ0）

テストを書く前に、対象コードを確認して以下を判断する:

- **構造が複雑でテストしにくい** → `/cga-tf-refactoring` で整理してからテスト
- **責務が混在している** → `/cga-tf-refactoring` で分離してからテスト
- **テスト可能な構造** → そのままREDへ進む

---

## TDDサイクル

### RED: 失敗するテストを書く

テストは仕様書。「何ができるか」の期待する振る舞いがわかる状態を目指す。

### GREEN: 最小限の実装で通す

テストを通す最小限のコードを書く。

### REFACTOR: コードを整理

テストが通った状態を維持しながら、コードを改善する。

---

## テストの分類

| レイヤー | 手法 | 比率 |
| --- | --- | --- |
| ドメインモデル | 純粋関数テスト | 40% |
| UseCase | SQLiteインメモリ | 50% |
| UseCase | モック（外部API） | 5% |
| Controller | E2E | 5% |

## テストの方針

- **ドメインモデル**: interface + 純粋関数で実装し、モック不要で直接テスト
- **UseCase**: SQLiteインメモリDBで実DBに近い形でテスト
- **モック**: 外部API（決済、メール送信など）のみ許可
- **E2E**: Prisma + supertest でController層の統合テスト

## 命名規則

`{条件}の場合は{結果}` または `{動作}できる/できない`

## カバレッジ目標

| 対象 | 目標 |
| --- | --- |
| UseCase | 90%+ |
| Repository | 80%+ |
| Controller | 70%+ |
| Validator | 100% |

---

## 実装パターンリファレンス

新規コードを書く前に、以下のお手本ファイルを Read して構造・命名・パターンを踏襲すること。

### ドメインモデル（集約の状態遷移 = 純粋関数）

- 参照: `src/ordering/models/order.ts`
- パターン:
  - エンティティは `interface`（readonly フィールド）
  - ファクトリ: `createOrder(input): Result<Order, CreateOrderError>`
  - 状態遷移: `confirmOrder(order): Result<Order, ConfirmOrderError>`
  - ガード: `canCancel(order): boolean`
  - 副作用なし、Date生成のみ許容

### UseCase

- 参照: `src/ordering/usecases/create-order.usecase.ts`
- パターン:
  1. Zod Schema でコマンド定義 → `type Command = z.infer<typeof Schema>`
  2. Error型を discriminated union で定義（usecase ファイル内 or `errors/` に配置）
  3. class で UseCase を定義、コンストラクタで Repository / Service を DI
  4. `execute(command)` 内の流れ:
     - Zod バリデーション（IO前）
     - 外部サービス呼び出し（必要な場合）
     - ドメインモデルのファクトリ/状態遷移を呼び出し
     - Repository に永続化
  5. 戻り値は `Result<T, E>`

### UseCase 単体テスト

- 参照: `src/ordering/usecases/__tests__/create-order.usecase.test.ts`
- パターン:
  - `beforeAll`: `createTestPrismaClient()` で SQLite インメモリ接続
  - `beforeEach`: `clearTables(prisma)` でデータクリア
  - `afterAll`: `cleanupTestPrismaClient(prisma)` で切断
  - テストケース: Arrange（入力組立）→ Act（execute呼出）→ Assert（`isOk`/`isErr` で判定）
  - 正常系・異常系を網羅、テスト名は日本語で `正常系: 〇〇` / `異常系: 〇〇`

### E2E テスト（Controller）

- 参照: `src/ordering/controllers/__tests__/cancel-order.e2e.test.ts`
- ファイル命名: `{操作名}.e2e.test.ts`
- パターン:
  - supertest + Express app でHTTPリクエスト送信
  - ステータスコードとレスポンスボディを検証
  - DB状態の事前準備は UseCase 経由で行う

### 共通ユーティリティ

- Result型: `src/shared/result.ts` — `ok(value)` / `err(error)` / `isOk()` / `isErr()`
- イベントバス: `src/shared/events/event-bus.ts` — ドメインイベントの発行・購読
- テストヘルパー: `src/infrastructure/prisma/test-helper.ts`
- バリデーションスキーマ: `src/shared/schemas/address.schema.ts`

---

## 中断条件

以下の条件に該当した場合、実装を即座に中断する。

### テスト5回連続失敗

同一のテストケースに対して5回修正を試みても通らない場合:

1. 試みた修正内容とエラーメッセージをまとめる
2. 変更を一旦コミット（WIP）またはスタッシュ
3. 開発者に状況を報告（AskUserQuestion）
4. `/cga-explore-planning` で計画を再検討

### 計画外の想定外事象

計画に記載のない前提条件の不整合や、計画では実現不可能と判断した場合:

1. 何が想定外だったか、なぜ計画通りに実現できないかを明確にする
2. 変更を一旦コミット（WIP）またはスタッシュ
3. 開発者に状況を報告（AskUserQuestion）
4. `/cga-explore-planning` で計画を再検討
