# cga-tf-refactoring 詳細ガイド

Kent Beck著「Tidy First?」の考え方に基づき、機能変更の前に小さな構造改善を行う。

## 基本ルール

- **小さく**: 1つのTidyingは5分以内で完了する規模
- **安全に**: 振る舞いを変えない。テストが通り続ける
- **分離して**: Tidyingと機能変更は別コミットにする
- **過剰にしない**: 今回の変更に必要な整理だけ行う

## 原則

1. **振る舞いを変えない** — 外部から見た動作は一切変わらない
2. **小さく、頻繁に** — 1つのTidyingは5分以内。大きなリファクタリングは複数に分解
3. **機能変更と分離** — Tidyingと機能変更は別コミット

## Tidyingパターン

各パターンのコード例は [patterns.md](patterns.md) を参照。適用するパターンを特定してから、該当セクションを読む。

| パターン | いつ使うか |
|---------|-----------|
| Guard Clauses | if-elseのネストが深いとき |
| Extract Helper | 同じ処理が複数箇所にあるとき |
| Normalize Symmetries | 似た処理が異なるスタイルで書かれているとき |
| Chunk Statements | 長い手続きで関連性が見えにくいとき |
| Rename | 変数名・関数名から意図が読み取れないとき |
| Explicit Parameters | グローバルやクロージャへの暗黙依存があるとき |
| Move to Model | UseCaseに状態判定・遷移が直書きされているとき |
| Move to Service | 複数集約にまたがるロジックがUseCaseにあるとき |
| Delete Dead Code | 呼ばれない関数・到達しない分岐があるとき |

## 判断基準: Tidy First?

すべてのコードを整理する必要はない。以下の質問で判断する。

### Tidyingすべきとき

1. **これから変更する箇所か？**
   - Yes → 変更しやすくするためにTidy
   - No → 触らない

2. **整理すると変更が楽になるか？**
   - 明らかに楽になる → Tidy
   - 微妙 → 機能変更を先に試す

3. **5分以内で終わるか？**
   - Yes → Tidy
   - No → 分割するか、今回は見送る

### Tidyingを見送るとき

- 今回の変更に関係ない箇所
- 整理してもあまり楽にならない
- 大規模な書き換えが必要
- テストがなく、安全に変更できない

## ワークフロー

```text
1. 変更対象のコードを読む
   ↓
2. 「このまま機能追加できるか？」を考える
   ↓
3-A. できる → そのまま /cga-programming へ
3-B. 整理したい → Tidyingを特定
   ↓
4. Tidyingを実施（テストが通ることを確認）
   ↓
5. Tidyingをコミット（"tidy:" プレフィックス）
   ↓
6. /cga-programming で機能変更を実施
```

## コミットメッセージ

```text
tidy: Guard Clausesで早期リターンに変換
tidy: calculateSubtotalを共通関数に抽出
tidy: 変数名をdataからorderDetailsに変更
tidy: 使われていないlegacyProcessを削除
tidy: キャンセル判定をOrderモデルに移動
tidy: 割引計算をDiscountServiceに抽出
```

## アンチパターン

```typescript
// ❌ 過剰なTidying: 今回の変更に関係ない箇所まで整理
// 「ついでにこっちも」は禁止

// ❌ 振る舞いの変更: Tidyingのつもりがバグ修正も混ぜる
// 別コミットに分ける

// ❌ 大規模リファクタリング: 「全部書き直す」
// 小さなTidyingに分解するか、別タスクにする

// ❌ テストなしでTidying: 壊れたかわからない
// 先にテストを書くか、Tidyingを見送る
```

## 参考

- Kent Beck「Tidy First?: A Personal Exercise in Empirical Software Design」
- Martin Fowler「Refactoring: Improving the Design of Existing Code」
