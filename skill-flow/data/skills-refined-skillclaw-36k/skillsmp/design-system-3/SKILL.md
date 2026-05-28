---
name: design-system
description: Panda CSSベースのデザインシステム管理。カラーパレット（OKLCH）、セマンティックトークン、スペーシング、フォントサイズ、レシピ（コンポーネントバリアント）の追加・更新・検証を行う。packages/panda-config/配下のデザイントークンを管理し、型安全なスタイル定義をサポート。
model: claude-sonnet-4-5-20250929
user-invocable: true
---

# デザインシステム管理 Skill

このskillは、TakakiAraki09プロジェクトのPanda CSSベースのデザインシステムを管理するのだ！

## プロジェクト構造

```
packages/panda-config/          # 共有デザインシステムパッケージ
├── config/
│   ├── index.ts               # 全設定のエントリーポイント
│   ├── baseColors.ts          # OKLCHベースカラー定義
│   ├── colors.ts              # セマンティックカラートークン
│   ├── spacing.ts             # スペーシングトークン（0-49）
│   ├── fontSizes.ts           # フォントサイズトークン
│   ├── radii.ts               # 角丸トークン
│   ├── fontWeights.ts         # フォントウェイト
│   ├── shadows.ts             # シャドウ
│   ├── sizes.ts               # サイズ
│   ├── durations.ts           # アニメーション時間
│   ├── easings.ts             # イージング関数
│   ├── breakpoints.ts         # レスポンシブブレークポイント
│   ├── utilities.ts           # カスタムユーティリティ
│   ├── conditions.ts          # カスタムConditions
│   ├── interfaces.ts          # 型定義
│   └── recipes/               # コンポーネントレシピ
│       ├── index.ts
│       ├── button.ts
│       ├── card.ts
│       └── header.ts
├── panda.preset.ts            # Pandaプリセット定義
└── panda.config.ts            # Panda設定

apps/web/                       # Qwikアプリケーション
├── panda.config.ts            # アプリ固有のPanda設定
└── src/
    ├── components/            # コンポーネント
    └── styles/                # コンポーネント固有スタイル
```

## デザイントークン

### 1. ベースカラー (`baseColors.ts`)

**OKLCHカラースペース**を使用：
- 知覚的に均等な色空間
- 明度を直感的にコントロール可能

**現在の定義**：
- `gray`, `blue`, `green`, `red`, `yellow`
- 各色に100-900の段階
- `black`（#222222）、`white`（#EEEEEE）

**構造**：
```typescript
const createOklch = (l: number) => ({
  100: { value: `oklch(94% 0.12 ${l})` },
  // ... 900まで
});
```

### 2. セマンティックカラー (`colors.ts`)

**3つのカテゴリ**：
1. **bg**: 背景色
   - `primary`, `secondary`, `info`, `success`, `error`, `warn`, `disabled`
2. **contents**: コンテンツ/テキスト色
   - 同上
3. **accent**: アクセント/ボーダー色
   - 同上

**特徴**：
- すべてライト/ダークモード対応（`_light` / `_dark`）
- ベースカラーを参照（例: `{colors.blue.200}`）

### 3. スペーシング (`spacing.ts`)

- **0-49**の値（4pxずつ増加）
- インデックスベース：`spacing: "5"` → 20px

### 4. フォントサイズ (`fontSizes.ts`)

**3つのカテゴリ**：
- **body系**: `body` (16px), `body-sm` (14px), `body-xs` (12px)
- **heading系**: `heading-sm` (18px), `heading` (20px), `heading-lg` (24px)
- **display系**: `display-sm` (30px), `display` (36px)

### 5. 角丸 (`radii.ts`)

- `inner`: 8px（小さめ）
- `outer`: 16px（大きめ）
- `full`: 9999px（円形）

### 6. その他のトークン

- `fontWeights`: light, normal, medium, semibold, bold
- `shadows`: sm, md, lg
- `sizes`: container, screen幅など
- `durations`: fast, normal, slow
- `easings`: ease-in, ease-out, etc.
- `breakpoints`: sm, md, lg, xl

## レシピ（コンポーネントバリアント）

レシピは**再利用可能なコンポーネントスタイル**を定義するのだ。

### 構造

```typescript
import type { RecipeConfig } from "@pandacss/dev";

export const componentName: RecipeConfig = {
  className: "component-name",
  description: "説明",
  base: {
    // すべてのバリアントに適用される基本スタイル
  },
  variants: {
    variantName: {
      value1: { /* スタイル */ },
      value2: { /* スタイル */ },
    }
  },
  defaultVariants: {
    variantName: "value1"
  }
};
```

### 現在のレシピ

1. **button** (`recipes/button.ts`)
   - サイズ: sm, md
   - バリアント: primary, secondary
   - 基本スタイル: flexbox, 角丸, トランジション

2. **card** (`recipes/card.ts`)
   - カードコンポーネント用

3. **header** (`recipes/header.ts`)
   - ヘッダーコンポーネント用
   - ※注意：まだ`recipes/index.ts`でエクスポートされていない

## タスク実行ガイド

### パラメータ受け取り

`$ARGUMENTS` から以下の形式でパラメータを受け取るのだ：

```
action: <add|update|check|validate>
type: <color|recipe|token|component>
target: <追加/更新する対象>
details: <追加の詳細情報>
```

### タスク1: 新しいベースカラーを追加

**コマンド例**：
```
/design-system add color purple
```

**実行手順**：
1. `packages/panda-config/config/baseColors.ts`を読む
2. 新しい色のhue値を決定（OKLCHのhue: 0-360）
3. `types`オブジェクトに追加
4. 必要に応じて`colors.ts`にセマンティックトークンを追加
5. MCPの`get_diagnostics`で型エラーをチェック

**注意点**：
- OKLCHのhue値は色相環に基づく（赤: 40, 黄: 85, 緑: 145, 青: 260, 紫: 300くらい）
- 明度（L）とクロマ（C）は既存のパターンに従う

### タスク2: セマンティックカラーを追加

**コマンド例**：
```
/design-system add semantic-color bg tertiary
```

**実行手順**：
1. `packages/panda-config/config/colors.ts`を読む
2. 該当カテゴリ（bg/contents/accent）に追加
3. `_light`と`_dark`の両方を定義
4. 既存のベースカラーを参照

### タスク3: 新しいレシピを追加

**コマンド例**：
```
/design-system add recipe input size,variant
```

**実行手順**：
1. `packages/panda-config/config/recipes/input.ts`を作成
2. RecipeConfigを定義：
   - className
   - description
   - base（基本スタイル）
   - variants（サイズ、バリアントなど）
   - defaultVariants
3. `packages/panda-config/config/recipes/index.ts`でエクスポート追加
4. MCPの`get_diagnostics`で型エラーをチェック

### タスク4: コンポーネントスタイルを生成

**コマンド例**：
```
/design-system create-component-style Modal
```

**実行手順**：
1. ユーザーに要件を確認（AskUserQuestion）：
   - どんなバリアントが必要？
   - サイズ展開は？
   - デフォルト値は？
2. `apps/web/src/styles/modal.tsx`にcvaスタイルを作成
3. コンポーネントファイル作成（オプション）

### タスク5: スペーシングを拡張

**コマンド例**：
```
/design-system extend spacing 60
```

**実行手順**：
1. `packages/panda-config/config/spacing.ts`を読む
2. 配列の長さを変更（例: 50 → 60）
3. 変更後のファイルを保存

### タスク6: フォントサイズを追加

**コマンド例**：
```
/design-system add font-size display-xl 3rem
```

**実行手順**：
1. `packages/panda-config/config/fontSizes.ts`を読む
2. 適切なカテゴリに追加
3. 命名規則に従う（body-*, heading-*, display-*）
4. remベースで定義

### タスク7: デザインシステム全体をチェック

**コマンド例**：
```
/design-system check all
```

**実行手順**：
1. 各設定ファイルを読む
2. 以下を確認：
   - レシピがすべてエクスポートされているか
   - セマンティックトークンに_light/_darkが両方あるか
   - タイポがないか（例: "sccess" → "success"）
   - 型エラーがないか
3. 問題をリストアップして報告

## ベストプラクティス

### 1. セマンティックトークンを優先

❌ **ダメな例**：
```typescript
color: "blue.500"
```

✅ **良い例**：
```typescript
color: "accent.info"
```

### 2. レシピで再利用性を高める

同じスタイルパターンが複数箇所で使われるなら、レシピを作るのだ。

### 3. OKLCHカラーを使う

新しい色を追加するときは、必ずOKLCHで定義するのだ。

### 4. 型安全性を保つ

- `as`、`!`、`any`は使わない
- 型定義（`GetPandaConfigMap`、`GetPandaSematicToken`）を活用

### 5. MCPツールを活用

- シンボルのリネーム: `mcp__typescript__rename_symbol`
- 参照検索: `mcp__typescript__find_references`
- 型情報取得: `mcp__typescript__get_type_at_symbol`
- 診断: `mcp__typescript__get_diagnostics`

### 6. 命名規則を守る

- **トークン**: ケバブケース（`font-size`, `body-sm`）
- **レシピ**: キャメルケース（`buttonStyle`）
- **セマンティック**: ドット記法（`bg.primary`）

## 制約事項

プロジェクト設定により以下の制約があるのだ：

1. **strictTokens: true**
   - 未定義のトークンは使えない
   - トークンを追加したらPanda CSSを再ビルド

2. **strictPropertyValues: true**
   - プロパティ値の型チェックが厳密
   - 正しいトークン参照を使う

3. **レシピのエクスポート**
   - レシピを追加したら必ず`recipes/index.ts`でエクスポート
   - エクスポートしないと使えない

4. **ライト/ダークモード**
   - セマンティックトークンは必ず両方を定義
   - 片方だけだとエラーになる

## デバッグ手順

エラーが出たときの対処法：

### 1. Panda CSSを再ビルド

```bash
pnpm build
```

### 2. 型エラーを確認

```
mcp__typescript__get_diagnostics を使う
```

### 3. トークン参照を確認

セマンティックトークンの参照は`{colors.xxx}`形式か確認

### 4. エクスポートを確認

レシピやトークンが正しくエクスポートされているか確認

## 実行時の注意

### タスク管理

- **TodoWrite**を使ってタスクを分解
- 一つずつ確実に実行
- 完了したらすぐにマーク

### ユーザー確認

曖昧な部分があれば**AskUserQuestion**で必ず確認：
- 色のhue値
- バリアント名
- デフォルト値

### MCPの活用

TypeScript操作は必ずMCPツールを使う：
- ファイル移動
- シンボルリネーム
- 参照検索

### 型安全性

- `as`、`!`、`any`は絶対に使わない
- 使う必要があれば説明して確認を取る

## よくある問題と解決法

### 問題1: レシピが反映されない

**原因**: `recipes/index.ts`でエクスポートしていない

**解決法**:
1. `recipes/index.ts`を確認
2. 新しいレシピをインポート＆エクスポート
3. Panda CSSを再ビルド

### 問題2: トークンが使えない

**原因**: strictTokensがtrueで未定義のトークンを使っている

**解決法**:
1. トークン定義を確認
2. 正しいトークン名を使う
3. または新しいトークンを定義

### 問題3: 型エラーが出る

**原因**: 型定義と実装が合っていない

**解決法**:
1. `mcp__typescript__get_diagnostics`で詳細確認
2. `interfaces.ts`の型定義を確認
3. 正しい型を使う

## パフォーマンス最適化

- トークン数が増えすぎないように定期的にレビュー
- 未使用のレシピは削除
- セマンティックトークンで抽象化

## セキュリティ

- カラー値を直接ハードコードしない
- ユーザー入力を直接トークン名にしない
- バリデーションを実装

## まとめ

このskillを使えば、デザインシステムの管理が超楽になるのだ！
型安全で、MCPツールを活用して、ユーザーに確認しながら進めるのだ！

頑張るのだ！
