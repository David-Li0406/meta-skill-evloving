# ベストプラクティス

テンプレート作成・修正時のベストプラクティス。

## テンプレート作成

### 1. 命名規則

- **ファイル名**: `{name}.template.{ext}`
- **プレースホルダー**: `{{SERVICE}}`, `{{SECTION}}`, `{{NAME}}`

### 2. 3大層アーキテクチャ準拠

- UI層: loader/actionのみ
- lib層: 純粋関数のみ
- data-io層: 副作用を含む

### 3. import文の整理

テンプレートのimport文は、生成後のファイルで使用されるものを記載：

```typescript
import { type LoaderArgs } from '@remix-run/cloudflare';
```

## config.json更新

### 1. 整合性の維持

- テンプレートファイル名とconfig.jsonの定義が一致
- output pathが正しい

### 2. カテゴリ分類

- ui: route, component
- lib: logic, helper
- data-io: data-io
- documents: requirements, spec

## 検証

### 1. 必ず検証

```bash
bash scripts/validate-config.sh
bash scripts/validate-templates.sh
```

### 2. テスト実行

```bash
npm run generate -- --category {category} --name test
```

## よくあるエラー

### config.jsonの構文エラー

```json
{
  "templates": {
    "ui": {
      "route": {
        "template": "templates/route.template.tsx",  // ← カンマ忘れ
        "output": "app/routes/{{SERVICE}}.{{SECTION}}.tsx"
      }
    }
  }
}
```

### テンプレートファイルが見つからない

- config.jsonで定義したファイルが存在しない
- ファイル名のtypo
