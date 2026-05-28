# デザインシステム Skill - リファレンス

このドキュメントは、design-system skillの詳細な使用例とAPIリファレンスなのだ！

## 目次

1. [コマンドリファレンス](#コマンドリファレンス)
2. [カラー管理](#カラー管理)
3. [レシピ管理](#レシピ管理)
4. [トークン管理](#トークン管理)
5. [コンポーネント生成](#コンポーネント生成)
6. [検証とチェック](#検証とチェック)
7. [実例集](#実例集)

## コマンドリファレンス

### 基本構文

```
/design-system <action> <type> <target> [options]
```

### アクション一覧

| アクション | 説明 | 対応する型 |
|----------|------|-----------|
| `add` | 新しい要素を追加 | color, recipe, token, semantic-color |
| `update` | 既存の要素を更新 | color, recipe, token |
| `check` | デザインシステムをチェック | all, colors, recipes, tokens |
| `validate` | 特定の要素を検証 | component, recipe |
| `create` | コンポーネントスタイルを生成 | component-style |
| `extend` | トークンを拡張 | spacing, font-sizes |
| `fix` | 問題を修正 | typos, exports, missing |

## カラー管理

### 1. ベースカラーを追加

**コマンド**：
```
/design-system add color <color-name> [hue]
```

**例**：
```
/design-system add color purple 300
/design-system add color orange
```

**パラメータ**：
- `color-name`: 色の名前（purple, orange, pinkなど）
- `hue` (オプション): OKLCHのhue値（0-360）。省略すると推奨値を提案

**処理フロー**：
1. `baseColors.ts`を読み込む
2. hue値を確認（未指定なら提案）
3. `types`オブジェクトに追加
4. ファイルを保存
5. 型エラーをチェック
6. 使用例を提示

**色相の目安**：
- 赤系: 0-40
- オレンジ系: 40-60
- 黄色系: 60-100
- 緑系: 100-180
- シアン系: 180-220
- 青系: 220-280
- 紫系: 280-320
- マゼンタ系: 320-360

### 2. セマンティックカラーを追加

**コマンド**：
```
/design-system add semantic-color <category> <name>
```

**例**：
```
/design-system add semantic-color bg tertiary
/design-system add semantic-color accent highlight
```

**パラメータ**：
- `category`: カテゴリ（bg, contents, accent）
- `name`: セマンティック名（tertiary, highlight, muteなど）

**処理フロー**：
1. `colors.ts`を読み込む
2. カテゴリを確認
3. ライト/ダークの両方の値をユーザーに確認
4. セマンティックトークンを追加
5. ファイルを保存
6. 型エラーをチェック

**セマンティック名の例**：
- **bg系**: tertiary, mute, highlight, hover, active
- **contents系**: secondary, tertiary, placeholder, link
- **accent系**: focus, highlight, border

### 3. 既存カラーを更新

**コマンド**：
```
/design-system update color <color-name> <property> <value>
```

**例**：
```
/design-system update color blue hue 270
/design-system update semantic-color bg.primary light {colors.white}
```

## レシピ管理

### 1. 新しいレシピを作成

**コマンド**：
```
/design-system add recipe <component-name> [variants...]
```

**例**：
```
/design-system add recipe input size,variant,state
/design-system add recipe badge size,color
/design-system add recipe avatar size,shape
```

**パラメータ**：
- `component-name`: コンポーネント名（input, badge, avatarなど）
- `variants`: バリアント名のカンマ区切りリスト（オプション）

**処理フロー**：
1. ユーザーに詳細を確認（AskUserQuestion）：
   - 各バリアントの値は？
   - デフォルト値は？
   - 基本スタイルは？
2. `recipes/component-name.ts`を作成
3. RecipeConfigを定義
4. `recipes/index.ts`に追加
5. 型エラーをチェック
6. 使用例を提示

**バリアントの例**：
- **size**: xs, sm, md, lg, xl
- **variant**: primary, secondary, tertiary, ghost, outline
- **state**: default, hover, active, disabled
- **color**: info, success, error, warn
- **shape**: square, circle, rounded

### 2. レシピを更新

**コマンド**：
```
/design-system update recipe <component-name> <action>
```

**例**：
```
/design-system update recipe button add-variant ghost
/design-system update recipe button update-size lg
```

### 3. レシピを検証

**コマンド**：
```
/design-system validate recipe <component-name>
```

**検証項目**：
- base スタイルが定義されているか
- defaultVariants が設定されているか
- variants が適切に定義されているか
- エクスポートされているか

## トークン管理

### 1. スペーシングを拡張

**コマンド**：
```
/design-system extend spacing <max-index>
```

**例**：
```
/design-system extend spacing 60
/design-system extend spacing 100
```

**処理フロー**：
1. `spacing.ts`を読み込む
2. 現在の最大値を確認
3. 指定値まで拡張
4. ファイルを保存

### 2. フォントサイズを追加

**コマンド**：
```
/design-system add font-size <name> <value>
```

**例**：
```
/design-system add font-size display-xl 3rem
/design-system add font-size body-lg 1.125rem
```

**命名規則**：
- **body系**: body-xs, body-sm, body, body-lg, body-xl
- **heading系**: heading-xs, heading-sm, heading, heading-lg, heading-xl
- **display系**: display-sm, display, display-lg, display-xl

### 3. 角丸を追加

**コマンド**：
```
/design-system add radii <name> <value>
```

**例**：
```
/design-system add radii sm 4px
/design-system add radii xl 24px
```

### 4. その他のトークンを追加

**コマンド**：
```
/design-system add <token-type> <name> <value>
```

**例**：
```
/design-system add shadow xl "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
/design-system add duration slower 1000ms
/design-system add easing bounce "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
```

## コンポーネント生成

### 1. コンポーネントスタイルを生成

**コマンド**：
```
/design-system create component-style <ComponentName>
```

**例**：
```
/design-system create component-style Modal
/design-system create component-style Tooltip
```

**処理フロー**：
1. ユーザーに要件を確認：
   - レシピを使う？ それともcva？
   - どんなバリアントが必要？
   - デフォルト値は？
2. スタイルファイルを生成
3. オプションでコンポーネントファイルも生成
4. 使用例を提示

**生成ファイル例**（cvaの場合）：
```typescript
// src/styles/modal.tsx
import { cva } from "~/styled-system/css";

export const modalStyle = cva({
  base: {
    position: "fixed",
    inset: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    bg: "rgba(0, 0, 0, 0.5)",
  },
  variants: {
    size: {
      sm: { maxWidth: "400px" },
      md: { maxWidth: "600px" },
      lg: { maxWidth: "800px" },
    },
  },
  defaultVariants: {
    size: "md",
  },
});
```

### 2. レシピベースのコンポーネント生成

**コマンド**：
```
/design-system create recipe-component <ComponentName>
```

**例**：
```
/design-system create recipe-component Button
```

**処理フロー**：
1. 既存のレシピを確認
2. レシピが無ければ作成を提案
3. styledコンポーネントを生成
4. 使用例を提示

## 検証とチェック

### 1. デザインシステム全体をチェック

**コマンド**：
```
/design-system check all
```

**チェック項目**：
- [ ] すべてのレシピが`recipes/index.ts`でエクスポートされているか
- [ ] セマンティックトークンに`_light`/`_dark`が両方あるか
- [ ] タイポがないか（特に"sccess" → "success"）
- [ ] 未使用のトークンがないか
- [ ] 型エラーがないか
- [ ] 命名規則に従っているか

### 2. カラーをチェック

**コマンド**：
```
/design-system check colors
```

**チェック項目**：
- [ ] OKLCHの値が正しいか
- [ ] セマンティックトークンのライト/ダーク両方定義
- [ ] 参照しているベースカラーが存在するか

### 3. レシピをチェック

**コマンド**：
```
/design-system check recipes
```

**チェック項目**：
- [ ] すべてのレシピにbaseスタイルがあるか
- [ ] defaultVariantsが設定されているか
- [ ] エクスポートされているか

### 4. コンポーネントを検証

**コマンド**：
```
/design-system validate component <ComponentName>
```

**例**：
```
/design-system validate component Button
/design-system validate component Header, Footer
```

**検証項目**：
- [ ] デザイントークンを使っているか
- [ ] ハードコードされた値がないか
- [ ] セマンティックトークンを使っているか
- [ ] アクセシビリティに配慮しているか

## 実例集

### 例1: 新しい色（teal）を追加

```
ユーザー: /design-system add color teal

Claude:
1. baseColors.tsを確認
2. tealのhue値を提案: 180（シアン系）
3. typesオブジェクトに追加:
   teal: 180
4. セマンティックトークンも追加する？（AskUserQuestion）
5. bg.teal, contents.teal, accent.tealを追加
6. 完了！使用例を提示
```

### 例2: Inputコンポーネントのレシピを作成

```
ユーザー: /design-system add recipe input size,variant,state

Claude:
1. AskUserQuestion:
   - sizeの値: sm, md, lg
   - variantの値: outline, filled, ghost
   - stateの値: default, error, disabled
   - デフォルト: size=md, variant=outline, state=default
2. recipes/input.tsを作成
3. recipes/index.tsに追加
4. 完了！使用例を提示:

import { styled } from "~/styled-system/jsx";

export const Input = styled("input", {
  base: {
    borderRadius: "inner",
    transition: "all",
    transitionDuration: "fast",
  },
  variants: {
    size: {
      sm: { paddingX: "3", paddingY: "2", fontSize: "body-sm" },
      md: { paddingX: "4", paddingY: "3", fontSize: "body" },
      lg: { paddingX: "5", paddingY: "4", fontSize: "body" },
    },
    variant: {
      outline: {
        border: "1px solid",
        borderColor: "accent.primary",
        bg: "transparent",
      },
      filled: {
        border: "none",
        bg: "bg.secondary",
      },
      ghost: {
        border: "none",
        bg: "transparent",
      },
    },
    state: {
      default: {},
      error: {
        borderColor: "accent.error",
        color: "contents.error",
      },
      disabled: {
        opacity: 0.5,
        cursor: "not-allowed",
      },
    },
  },
  defaultVariants: {
    size: "md",
    variant: "outline",
    state: "default",
  },
});
```

### 例3: Modalコンポーネントスタイルを生成

```
ユーザー: /design-system create component-style Modal

Claude:
1. AskUserQuestion:
   Q1: レシピを使う？ それともcva？
   - レシピ（recipes/）: プロジェクト全体で再利用
   - cva（src/styles/）: このアプリ専用
   選択: cva

   Q2: どんなバリアントが必要？
   - size: sm, md, lg
   - centered: true/false
   選択: size, centered

   Q3: デフォルト値は？
   - size: md
   - centered: true

2. src/styles/modal.tsxを作成
3. 完了！使用例を提示:

import { styled } from "~/styled-system/jsx";
import { modalStyle } from "~/styles/modal";

const ModalContainer = styled("div", modalStyle);

export const Modal = ({ size = "md", centered = true, children }) => (
  <ModalContainer size={size} centered={centered}>
    {children}
  </ModalContainer>
);
```

### 例4: デザインシステムをチェック

```
ユーザー: /design-system check all

Claude:
1. 各ファイルを読み込む
2. チェックを実行
3. 発見した問題:

   ❌ colors.ts: タイポ "sccess" → "success"
   ❌ recipes/header.ts: recipes/index.tsでエクスポートされていない
   ✅ すべてのセマンティックトークンに_light/_darkがある
   ✅ 型エラーなし

4. 修正しますか？（AskUserQuestion）
   選択: はい

5. 修正実行:
   - colors.tsの"sccess"を"success"にリネーム（MCPのrename_symbol使用）
   - recipes/index.tsにheaderを追加

6. 完了！
```

### 例5: スペーシングを拡張

```
ユーザー: /design-system extend spacing 80

Claude:
1. spacing.tsを読み込む
2. 現在: 0-49（50個）
3. 新しい: 0-79（80個）
4. 配列の長さを変更
5. 完了！
   - spacing: "60" = 240px
   - spacing: "79" = 316px
```

## トラブルシューティング

### Q: レシピが反映されない

A: 以下を確認するのだ：
```
/design-system check recipes
```
- recipes/index.tsでエクスポートされているか
- Panda CSSを再ビルドしたか（pnpm build）

### Q: トークンが使えないと言われる

A: strictTokens: trueなので、未定義のトークンは使えないのだ：
```
/design-system check tokens
```
- トークンが正しく定義されているか
- スペルミスがないか

### Q: 型エラーが出る

A: MCPで診断するのだ：
```typescript
mcp__typescript__get_diagnostics を使って確認
```

### Q: ライト/ダークモードで表示がおかしい

A: セマンティックトークンを確認するのだ：
```
/design-system check colors
```
- _light と _dark の両方が定義されているか
- 参照しているベースカラーが存在するか

## まとめ

このskillを使えば、デザインシステムの管理が超効率的になるのだ！

**重要なポイント**：
1. **型安全**: MCPツールを活用して型エラーを防ぐ
2. **ユーザー確認**: 曖昧な部分はAskUserQuestionで確認
3. **TodoWrite**: タスクを分解して管理
4. **ベストプラクティス**: セマンティックトークンとレシピを活用

頑張って素晴らしいデザインシステムを作るのだ！
