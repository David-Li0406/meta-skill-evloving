---
id: "T8"
name: "Anamnēsis"
category: "memory"
description: "記憶モジュール (A-P-S)。長期記憶への保存と取得を管理する。"

triggers:
  - session end
  - important event detected
  - /hist workflow
  - memory retrieval needed

keywords:
  - memory
  - recall
  - save
  - history
  - vault
  - long-term

when_to_use: |
  セッション終了時、重要イベント検出時、過去知見の取得が必要な時。
  /hist, /boot ワークフロー発動時。

when_not_to_use: |
  - セッション内の一時的な情報のみ
  - 記録価値がない情報

fep_code: "A-P-S"
version: "2.0"
---

# T8: Anamnēsis (ἀνάμνησις) — 記憶

> **FEP Code:** A-P-S (Action × Pragmatic × Slow)
>
> **問い**: 何を覚えておくべきか？何を思い出すべきか？
>
> **役割**: 長期記憶への保存と取得を管理する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- セッション終了時（/hist で同期）
- 重要なイベント/決定が発生
- ユーザーが「覚えておいて」と依頼
- 過去の知見が必要（/boot で取得）
- T3/T4 が過去パターンを要求

### ✗ Not Trigger
- セッション内の一時的な情報のみ
- 記録価値がない情報
- 既に Vault に保存済み

**注意**: Antigravity はセッション間で状態を永続化しない。外部ストレージ（Vault）への明示的な保存が必要。

---

## Core Function

**役割:** 長期記憶への保存と取得を管理する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 価値関数 E[P(o)] の長期最適化 |
| **本質** | 「何を覚えておくべきか」を決定する |
| **位置** | 長期学習ループの一部 |
| **依存** | T7 からの検証結果、各モジュールからのイベント |

---

## Processing Logic（フロー図）

```
┌─ T8 発動トリガー検出
│
├─ 保存モード（Save）？
│  ├─ Phase 1: 記録価値判定
│  │   ├─ 重要度評価
│  │   ├─ 新規性評価
│  │   └─ 価値 > 閾値 → 保存
│  ├─ Phase 2: 構造化
│  │   ├─ Vault フォーマットに変換
│  │   └─ メタデータ付与
│  └─ Phase 3: 保存
│      └─ Vault に書き込み
│
└─ 取得モード（Recall）？
   ├─ Phase 1: クエリ解析
   │   ├─ 検索対象を特定
   │   └─ 時間範囲を設定
   ├─ Phase 2: 検索
   │   └─ Vault から取得
   └─ Phase 3: 出力
       └─ T1/T3/T4 へ提供
```

---

## Memory Types

| 記憶種別 | 保存先 | 内容 | 保持期間 |
|----------|--------|------|----------|
| **エピソード記憶** | Vault/daily | 日々のイベント | 恒久 |
| **意味記憶** | Knowledge Items | 抽象化された知識 | 恒久 |
| **手続き記憶** | Workflows/Skills | 手順・スキル | 恒久 |
| **作業記憶** | セッション内 | 一時的な情報 | セッション終了まで |

---

## Importance Evaluation

```yaml
importance_score:
  formula: (novelty × 0.3) + (impact × 0.4) + (frequency × 0.3)
  
  novelty:
    - 初めてのイベント: 1.0
    - 類似イベント過去3回未満: 0.7
    - 類似イベント過去3回以上: 0.3
    
  impact:
    - 目標達成に直結: 1.0
    - 目標に間接的影響: 0.5
    - 目標に無関係: 0.1
    
  frequency:
    - 再利用される可能性高: 1.0
    - 再利用される可能性低: 0.3
    
  threshold: 0.5  # これ以上なら保存
```

---

## Vault Format

```markdown
# YYYY-MM-DD (曜日) - Daily Log

## Context (開始時の状況要約)
- ...

## Key Events
- [HH:MM] Event 1
- [HH:MM] Event 2

## Decisions Made
- Decision 1: 理由
- Decision 2: 理由

## Lessons Learned
- Lesson 1
- Lesson 2

## Tomorrow / Next Actions
- [ ] Action 1
- [ ] Action 2

## Metadata
- session_id: ...
- modules_activated: [T1, T2, ...]
- importance_score: 0.X
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: Vault アクセス不可
**症状**: ファイルシステムエラー  
**対処**: セッション内に一時保存、後で再試行

### ⚠️ Failure 2: 記憶過多
**症状**: Vault が肥大化  
**対処**: 低重要度の記憶を圧縮/削除

### ⚠️ Failure 3: 検索失敗
**症状**: 関連記憶が見つからない  
**対処**: 検索範囲を拡大、曖昧検索

### ⚠️ Failure 4: 矛盾する記憶
**症状**: 過去の記憶と現在が矛盾  
**対処**: 新しい記憶を優先、矛盾を記録

### ✓ Success Pattern
**事例**: セッション終了 → 重要イベント抽出 → Vault 保存 → 完了

---

## Test Cases（代表例）

### Test 1: セッション終了時保存
**Input**: /hist 発動  
**Expected**: 重要イベントを Vault に保存  
**Actual**: ✓ daily ノート作成

### Test 2: 過去知見取得
**Input**: /boot 発動  
**Expected**: 過去 7 日の履歴を取得  
**Actual**: ✓ 文脈サマリ生成

### Test 3: 低重要度イベント
**Input**: importance_score < 0.5  
**Expected**: 保存スキップ  
**Actual**: ✓ 作業記憶のみ

---

## Configuration

```yaml
importance_threshold: 0.5       # 保存閾値
history_scan_days: 7            # 取得時のスキャン日数
max_vault_size_mb: 100          # Vault 最大サイズ
compression_enabled: true       # 低重要度記憶の圧縮
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T7 Dokimē | 検証結果 |
| **Precondition** | 各モジュール | イベント通知 |
| **Postcondition** | T1 Aisthēsis | 過去知見提供（/boot） |
| **Postcondition** | T3 Theōria | パターン情報提供 |
| **Postcondition** | T4 Phronēsis | 価値関数提供 |

---

## 旧 forge/modules より移行

### 頭を切り替える [Switch] テンプレート

> **元ファイル**: `forge/modules/find/🔄 頭を切り替える.md`
> **役割**: あなたは「認知の転轍手（Context Switcher）」です。

**Core Objective**:
1.  **Save State**: 現在の作業状態を「セーブポイント」として記録し、安心して忘れられるようにする。
2.  **Clear Cache**: 短期記憶をリセットするための物理的・精神的アクションを促す。
3.  **Prime Next**: 次のタスクの「最初の一歩（Entry Point）」を明確にする。

**入力形式**:
```xml
<switch_context>
【終わらせるタスク (Current Task)】
（例：メール返信、コードのデバッグ）

【次にやるタスク (Next Task)】
（例：企画書作成、休憩）

【今の脳の状態】
（例：疲れてる、興奮してる）
</switch_context>
```

**出力形式**:
```markdown
## 🔄 Context Switch Sequence

### 1. 💾 Save Point (前のタスクの保存)
- **Status**: [完了 / 中断]
- **Next Action for Resume**: ...
- **Memo**: ...

### 2. 🧹 Clear Cache (リセット儀式)
- [ ] **Physical**: ...
- [ ] **Mental**: ...

### 3. 🚀 Prime Next (次のタスクへ)
- **Target**: [次のタスク名]
- **First Step**: ...
```

---

## 旧 forge/modules より移行

### 脳内を吐き出す [Brain Dump] テンプレート

> **元ファイル**: `forge/modules/find/🤯 脳内を吐き出す.md`
> **役割**: あなたは「認知の清掃人（Cognitive Cleaner）」です。

**Core Objective**:
1.  **Acceptance**: どんなに支離滅裂な入力でも、批判せず、要約しすぎず、全てを拾い上げてください。
2.  **Clarification**: 曖昧な名詞がある場合のみ、優しく具体化を促してください。
3.  **Buckets**: Action, Schedule, Idea, Noise の4つに分類します。

**入力形式**:
```xml
<brain_dump>
ここに、今頭にあることを箇条書きでも文章でも、思いつくままに書き殴ってください。
</brain_dump>
```

**出力形式**:
```markdown
## 🧹 Brain Dump Result

### 🔥 Action (やるべきこと)
- [ ] タスク名 [推定所要時間]

### 📅 Schedule (予定)
- [ ] 日時: イベント名

### 💡 Idea/Memo (保存)
- ...

### 🗑️ Noise (吐き出し完了)
- ...
```

---

## 旧 forge/modules より移行

### 記録する [Archive] テンプレート

> **元ファイル**: `forge/modules/reflect/💾 記録する.md`
> **役割**: あなたは「知識の司書（Knowledge Librarian）」です。

**Core Objective**:
1.  **Summarize**: 内容を簡潔に要約し、中身を読まなくても概要がわかるようにする。
2.  **Tagging**: 検索に引っかかりやすいキーワード（タグ）を適切に付与する。
3.  **Format**: 指定されたツール（Markdown, Notion, JSONなど）に適した形式で整形する。

**入力形式**:
```xml
<archive_target>
【保存したい内容】
（例：先ほどのチャットの結論、会議のメモ）

【保存先/形式】
（例：Obsidian、Notion）

【付与したい文脈】
（例：プロジェクトAに関するもの）
</archive_target>
```

**出力形式**:
```markdown
## 💾 Archived Record

### 1. Copyable Content (保存用テキスト)
```markdown
---
title: [具体的で検索しやすいタイトル]
date: 202X-XX-XX
tags: [タグ1, タグ2]
---

# [タイトル]

## 📝 Summary
...

## 💡 Key Insights
...
```

### 2. Librarian's Note (整理のヒント)
- **Suggested Filename**: ...
- **Storage Location**: ...
```
