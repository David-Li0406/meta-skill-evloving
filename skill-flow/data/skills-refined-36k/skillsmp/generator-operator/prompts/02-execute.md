# 実行プロンプト

## AI役割定義

あなたは実行の専門家です。npm run generateコマンドを実行し、結果を確認してください。

## 思考プロセス（CoT）

```text
Step 1: コマンド構築
  → パラメータからコマンドを構築

Step 2: コマンド実行
  → scripts/run-generate.sh を実行

Step 3: 結果確認
  → 生成されたファイルを確認

Step 4: エラーハンドリング
  → エラーがあればprompts/03-handle-error.mdへ
```

## 実行手順

### 1. コマンド構築

```bash
npm run generate -- \
  --category {category} \
  --{subtype-flag} {subtype} \
  --service {service} \
  --section {section} \
  --name {name}
```

### 2. コマンド実行

```bash
bash .claude/skills/generator-operator/scripts/run-generate.sh \
  {category} {subtype} {service} {section} {name}
```

### 3. 結果確認

生成されたファイルを確認：

```bash
# 例: component
cat app/components/{service}/{section}/{name}.tsx
```

## Output形式

```markdown
## ファイル生成完了

**生成ファイル**: app/{path}/{service}/{section}/{name}.{ext}

**内容確認**:
```{ext}
{generated-file-content}
```
```
