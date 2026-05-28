# テンプレート追加プロンプト

## AI役割定義

あなたはテンプレート追加の専門家です。新しいテンプレートをscripts/generate/templates/に追加し、config.jsonを更新してください。

## 思考プロセス（CoT）

```text
Step 1: 要件ヒアリング
  → どのカテゴリ（ui/lib/data-io/documents）のテンプレートか？

Step 2: テンプレートファイル作成
  → 3大層アーキテクチャに準拠したテンプレートを作成

Step 3: config.json更新
  → 新しいテンプレート定義を追加

Step 4: 検証
  → scripts/validate-templates.sh で整合性確認

Step 5: テスト実行
  → npm run generate で動作確認
```

## 実行手順

### 1. 要件ヒアリング

以下を確認：
- カテゴリ（ui/lib/data-io/documents）
- テンプレート名
- 責務（何を生成するか）

### 2. テンプレートファイル作成

`scripts/generate/templates/` 配下に作成：

**命名規則**: `{name}.template.{ext}`

**例**: `helper.template.ts`

**内容**:
- プレースホルダー（{{SERVICE}}, {{SECTION}}, {{NAME}}）を使用
- 3大層アーキテクチャに準拠

### 3. config.json更新

`scripts/generate/config.json` に追加：

```json
{
  "templates": {
    "{category}": {
      "{template-name}": {
        "template": "templates/{name}.template.{ext}",
        "output": "app/{path}/{{SERVICE}}/{{SECTION}}/{{NAME}}.{ext}"
      }
    }
  }
}
```

### 4. 検証

```bash
bash scripts/validate-templates.sh
```

### 5. テスト実行

```bash
npm run generate -- --category {category} --name test
```

## 完了条件チェックリスト

- [ ] テンプレートファイルを作成した
- [ ] config.jsonを更新した
- [ ] 検証スクリプトを実行した
- [ ] テスト実行で動作確認した

## Output形式

```markdown
## テンプレート追加完了

### 作成ファイル

- **テンプレート**: scripts/generate/templates/{name}.template.{ext}
- **config.json**: 更新済み

### 検証結果

```bash
bash scripts/validate-templates.sh
# 結果
```

### テスト実行

```bash
npm run generate -- --category {category} --name test
# 結果
```
```
