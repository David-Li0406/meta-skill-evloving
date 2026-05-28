# TypeScript 命名規則 コードレビュー プロンプト

## レビュー観点

### 基本的な命名規則

#### ケーススタイル

- **PascalCase**: クラス、インターフェース、型エイリアス、enum、namespace
- **camelCase**: 変数、関数、メソッド、パラメータ、プロパティ
- **UPPER_SNAKE_CASE**: 定数、環境変数
- **kebab-case**: ファイル名（オプション）

### 型・インターフェース

- インターフェース名に`I`プレフィックスは不要（避ける）
- 型エイリアスは用途を明確に表す名前
- ジェネリック型は`T`, `U`, `V`または意味のある名前（`TItem`, `TKey`）

### 変数・関数

- boolean 型は`is`, `has`, `should`, `can`で始める
- 配列・コレクションは複数形
- 非同期関数は動詞で明確に（`fetchUser`, `loadData`）
- イベントハンドラーは`on`または`handle`プレフィックス

### React/コンポーネント（該当する場合）

- コンポーネント: PascalCase
- Props 型: `ComponentNameProps`
- カスタムフック: `use`プレフィックス

### 特殊なケース

- private/protected メンバーの`_`プレフィックス（チームによる）
- 未使用パラメータの`_`プレフィックス
- enum 値: PascalCase または UPPER_SNAKE_CASE

## チェックリスト

```markdown
□ クラス・型が PascalCase か
□ 変数・関数が camelCase か
□ 定数が UPPER_SNAKE_CASE か
□ boolean 変数が適切なプレフィックスを持つか
□ 配列が複数形か
□ 名前が意図を明確に表しているか
□ 省略形を避けているか（例: usr → user）
□ 一貫性があるか
```

## 出力形式

````markdown
## 命名規則レビュー結果

### ❌ 修正が必要

**該当箇所**: [ファイル:行番号]

```typescript
// 現在
const UserData = {...}  // 変数がPascalCase

// 推奨
const userData = {...}
```
````

**理由**: 変数は camelCase を使用

### ⚠️ 改善推奨

**該当箇所**: [ファイル:行番号]

```typescript
// 現在
const flag = true;

// 推奨
const isEnabled = true;
```

**理由**: boolean 変数は意図を明確にする

### ✅ 良い例

- `fetchUserData`: 非同期関数の命名が明確
- `hasPermission`: boolean 変数の命名が適切

## サマリー

- 修正必要: [件数]
- 改善推奨: [件数]
- 一貫性の問題: [あれば記載]

```

## 重要事項
- チーム/プロジェクトの規約を優先
- 既存コードとの一貫性を重視
- 破壊的変更は慎重に検討
- ドメイン固有の命名規則を尊重
```
