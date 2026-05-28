# 構造レビュー プロンプト

コード構造の改善可能箇所を特定する。Kent Beck「Tidy First?」のパターンに基づく。

## レビュー観点

### 優先度: 高
- **Guard Clauses**: 早期リターンでネストを浅く
- **Dead Code Removal**: 未使用コードの削除
- **Normalize Symmetries**: 対称性の統一
- **Extract Helper**: 共通処理の抽出
- **型定義の明確化**: any型の排除

### 優先度: 中
- **Reading Order**: 読みやすい順序に並び替え
- **Cohesion Order**: 関連コードをまとめる
- **Explicit Parameters**: 暗黙のパラメータを明示化
- **Chunk Statements**: 関連文をグループ化

### 優先度: 低
- **Explaining Variables**: 複雑な式に名前を付ける
- **Explaining Constants**: マジックナンバーに名前を付ける
- **Rename**: より良い名前に変更

## 具体例

### Guard Clauses
```typescript
// Before
if (user && user.isActive) {
  if (user.hasPermission) {
    return <Component />;
  }
}

// After
if (!user?.isActive) return null;
if (!user.hasPermission) return null;
return <Component />;
```

### 型の明確化
```typescript
// Before
const handler = (data: any) => {...}

// After
const handler = (data: UserData) => {...}
```

## 出力形式

```markdown
### [優先度] - [パターン名]
**該当箇所**: [ファイル:行番号]
**理由**: [簡潔な説明]
```