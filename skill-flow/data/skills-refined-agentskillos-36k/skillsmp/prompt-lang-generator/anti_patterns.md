# Anti-Patterns
# =============
# Prompt-Lang 生成で避けるべきパターン

## 1. 構文エラー系

### 1.1 YAML インデント不正
**NG**:
```yaml
@constraints:
- 制約1  # インデントなし
- 制約2
```

**OK**:
```yaml
@constraints:
  - 制約1
  - 制約2
```

### 1.2 コロン漏れ / コロン後スペースなし
**NG**:
```yaml
@role シニアエンジニア
@goal:セキュリティレビュー
```

**OK**:
```yaml
@role: シニアエンジニア
@goal: セキュリティレビュー
```

### 1.3 未定義ディレクティブ
**NG**:
```yaml
@objective: ...  # 存在しない
@rules: ...      # @constraints の誤記
```

**OK**: 公式ディレクティブのみ使用
- v1: @role, @goal, @constraints, @format, @examples, @tools, @resources
- v2: @rubric, @if/@else, @activation, @context, @extends, @mixin

---

## 2. ドメイン特有制約欠落

### 2.1 医療ドメインで免責なし
**NG**:
```yaml
@constraints:
  - 正確に抽出すること
```

**OK**:
```yaml
@constraints:
  - 正確に抽出すること
  - 「本情報はAI抽出であり、医療判断に使用しないこと」免責を必ず出力に含める
  - 診断名など医学用語は医学辞典に準拠
```

### 2.2 セキュリティドメインで具体性なし
**NG**:
```yaml
@constraints:
  - セキュリティを考慮すること
```

**OK**:
```yaml
@constraints:
  - OWASP Top 10 に照らして脆弱性を指摘
  - 各指摘に CVE 番号または CWE 番号を付与
  - 攻撃シナリオを具体的に記述
```

---

## 3. @format 曖昧

### 3.1 抽象的なフォーマット指定
**NG**:
```yaml
@format: JSON形式で出力
```

**OK**:
```yaml
@format: |
  ```json
  {
    "summary": "string",
    "issues": [
      {
        "severity": "high | medium | low",
        "description": "string"
      }
    ]
  }
  ```
```

---

## 4. @activation 条件緩すぎ

### 4.1 過度に広いトリガー
**NG**:
```yaml
@activation:
  mode: model_decision
  conditions:
    - input_contains: ["作成"]  # 「ファイル作成」などでも発火
```

**OK**:
```yaml
@activation:
  mode: model_decision
  conditions:
    - input_contains: ["prompt-lang", "プロンプト定義", ".prompt"]
    - input_length: "> 30"
    - intent: "generate structured prompt"
  priority: 3
```

---

## 5. @examples 不足

### 5.1 例なし
**NG**:
```yaml
@examples: []
```

### 5.2 非現実的な例
**NG**:
```yaml
@examples:
  - input: "test"
    output: "test output"
```

**OK**:
```yaml
@examples:
  - input: "患者: 山田太郎、45歳男性。診断: 緊張型頭痛"
    output: |
      {
        "patient_name": "山田太郎",
        "age": 45,
        "gender": "male",
        "diagnosis": ["緊張型頭痛"]
      }
```

---

## 6. 曖昧語の使用

### 禁止語リスト
- 「適切に」→ 「〇〇の場合は△△する」
- 「うまく」→ 具体的な成功基準
- 「いい感じ」→ 禁止、要件明確化を要求
- 「必要に応じて」→ トリガー条件を明示
- 「などなど」→ 項目を列挙
- 「できるだけ」→ 優先度 N、制約の範囲内で最大化

---

## 7. Error Handling 未定義

### 7.1 必須カバー3パターン
1. **構文エラー時**: パーサー出力を添えて箇所を明示
2. **曖昧入力時**: 追加質問で明確化
3. **ドメイン外時**: 対応外を明示 + 代替 Skill 提案
