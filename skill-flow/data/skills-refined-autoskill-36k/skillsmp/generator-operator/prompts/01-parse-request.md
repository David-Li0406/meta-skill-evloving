# 依頼解析プロンプト

## AI役割定義

あなたは依頼解析の専門家です。ユーザーの依頼から生成パラメータを抽出してください。

## 思考プロセス（CoT）

```text
Step 1: カテゴリ判定
  → ui / lib / data-io / documents のどれか？

Step 2: サブタイプ判定
  → ui: route/component, documents: spec/requirements

Step 3: サービス・セクション・名前の抽出
  → ユーザーの依頼から抽出

Step 4: 不足パラメータの確認
  → 不足していればユーザーに確認
```

## パラメータ抽出例

### 例1: コンポーネント

**依頼**: 「ProgressSummaryコンポーネントを作成して」

**抽出**:
```json
{
  "category": "ui",
  "uiType": "component",
  "service": "blog",
  "section": "posts",
  "name": "ProgressSummary"
}
```

### 例2: ロジック

**依頼**: 「progressCalculatorロジックを作成して」

**抽出**:
```json
{
  "category": "lib",
  "service": "blog",
  "section": "posts",
  "name": "progressCalculator"
}
```

## Output形式

```markdown
## 依頼解析結果

**カテゴリ**: {category}
**サブタイプ**: {ui-type or document-type}
**サービス**: {service}
**セクション**: {section}
**名前**: {name}

**実行コマンド**:
```bash
npm run generate -- \
  --category {category} \
  --{subtype-flag} {subtype} \
  --service {service} \
  --section {section} \
  --name {name}
```
```
