# スキル作成ベストプラクティス

## 核心原則

### 1. コンテキストは公共財

スキルはAIのコンテキストウィンドウを消費する。
必要最小限の情報のみを含め、冗長な説明は避ける。

### 2. 500行ルール

SKILL.mdは500行以下に保つ。超える場合は：
- 複数スキルに分割
- 詳細を`references/`に移動
- 不要部分を削除

### 3. 明確なトリガー

`description`に必ず含める：
- `Use when:` - 起動するキーワード・状況
- `Do not use when:` - 起動しない条件

---

## 構造パターン

### ワークフロー型

順番に処理する場合：

```markdown
## ワークフロー

### Step 1: 〇〇
[手順]

### Step 2: △△
[手順]

### Step 3: □□
[手順]
```

### タスク型

複数の独立した機能がある場合：

```markdown
## タスクA
[説明と手順]

## タスクB
[説明と手順]
```

### リファレンス型

標準・仕様を守らせる場合：

```markdown
## ガイドライン
- ルール1
- ルール2

## 仕様
[詳細な仕様]
```

---

## 出力パターン

### テンプレートパターン

```markdown
**必ずこの形式で出力：**

# タイトル
## セクション1
## セクション2
```

### 例示パターン

```markdown
**入力:** 「〇〇」
**出力:** 「△△」
```

---

## チェックリスト

### 作成時

- [ ] `name`はハイフン区切り小文字
- [ ] `description`に`Use when:`がある
- [ ] `description`に`Do not use when:`がある
- [ ] 500行以下
- [ ] 具体例がある
- [ ] ヒアリング項目がある
- [ ] 出力形式が明記されている

### レビュー時

- [ ] トリガーワードでスキルが起動する
- [ ] 期待通りの出力が得られる
- [ ] エッジケースに対応できる
- [ ] 不要な情報がない

---

## アンチパターン

### 避けるべき記述

```yaml
# 悪い例
description: スキルです

# 良い例
description: |
  レポートを作成するスキル。
  Use when: レポート作成, 報告書, まとめ
  Do not use when: プレゼン資料, スライド
```

### 避けるべき構造

```markdown
# 悪い例（1000行以上の巨大スキル）
## セクション1
[100行]
## セクション2
[200行]
...
## セクション10
[300行]

# 良い例（分割）
# report-generator-basic/SKILL.md (基本機能)
# report-generator-advanced/SKILL.md (高度機能)
```

---

## 参考

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
