# ドキュメントテンプレート

## features/*.md テンプレート

```markdown
# 機能名

## 概要

[機能の説明]

## 関連ファイル

- **Routes**: `src/routes/...`
- **Pages**: `src/components/pages/...`
- **Features**: `src/components/features/...`
- **Convex**: `convex/[domain]/`

## 主な機能

- 機能1
- 機能2

## データモデル

\`\`\`typescript
tableName = {
  field1: type,
  field2: type,
}
\`\`\`

## 画面一覧

| 画面 | パス | 説明 |
|------|------|------|
| 画面名 | `/path` | 説明 |

## コンポーネント構成

[構成の説明]

## API

### Queries
- `domain.queries.xxx` - 説明

### Mutations
- `domain.mutations.xxx` - 説明
```

---

## INDEX.md への追記形式

```markdown
| 機能名 | [機能名.md](features/機能名.md) | 概要説明 |
```

---

## ARCHITECTURE.md 機能マッピング形式

### 機能→ファイルマッピング
```markdown
| 機能名 | `Pages/...` | `Features/...` | `domain/queries`, `mutations` |
```

### ファイル→機能マッピング（逆引き）
```markdown
### 機能名
| ファイルパス | 責務 |
|-------------|------|
| `src/routes/...` | ルーティング |
| `src/components/pages/...` | useQuery、エラー/ローディング処理 |
| `src/components/features/...` | ドメインロジック、UI |
| `convex/domain/` | DB操作 |
```

---

## 状態管理（Jotai）追加形式

```markdown
| `xxxAtom` | 責務説明 | メモリ or localStorage |
```