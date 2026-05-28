# テンプレート構造

テンプレートの基本構造とプレースホルダーの使い方。

## プレースホルダー

| プレースホルダー | 説明 | 例 |
| :--- | :--- | :--- |
| `{{SERVICE}}` | サービス名 | blog, account |
| `{{SECTION}}` | セクション名 | posts, users |
| `{{NAME}}` | ファイル名 | ProgressSummary |

## テンプレート例

### UI層（route）

```tsx
// app/routes/{{SERVICE}}.{{SECTION}}.tsx
export default function {{NAME}}() {
  return <div>{{NAME}}</div>;
}
```

### lib層（logic）

```typescript
// app/lib/{{SERVICE}}/{{SECTION}}/{{NAME}}.ts
export function {{NAME}}(input: string): string {
  return input;
}
```

### data-io層

```typescript
// app/data-io/{{SERVICE}}/{{SECTION}}/{{NAME}}.server.ts
export async function {{NAME}}() {
  const response = await fetch('/api/...');
  return response.json();
}
```

## 3大層アーキテクチャ

- **UI層**: 副作用なし、loader/actionのみ
- **lib層**: 純粋関数のみ
- **data-io層**: 副作用を含む

**詳細**: `docs/ARCHITECTURE_MANIFESTO2.md`
