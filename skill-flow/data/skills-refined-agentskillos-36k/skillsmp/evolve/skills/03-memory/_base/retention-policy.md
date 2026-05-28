# 記憶保留策略 (Retention Policy)

> Memory 不是只進不出的垃圾桶，需要定期清理

## 保留期限建議

| 類型 | 保留期限 | 清理條件 |
|------|----------|----------|
| **learnings/** | 永久 | 被新經驗取代時標註 `[SUPERSEDED]` |
| **failures/** | 90 天 | 問題已解決且不再重現 |
| **decisions/** | 永久 | 決策被推翻時標註 `[REVERSED]` |
| **patterns/** | 永久 | 發現更好模式時合併 |
| **strategies/** | 180 天 | 策略成功率 < 30% |
| **discoveries/** | 永久 | 假設被證偽時標註 `[DISPROVED]` |

## 清理觸發時機

```
1. 條目超過 30 筆 → 整理
2. 發現新舊衝突 → 標註舊的
3. 季度結束 → 全面審視
4. 專案 Milestone → 回顧整合
```

## 清理操作

### 標註過時（推薦）

```markdown
---
status: superseded
superseded_by: learnings/2026-02-01-better-approach.md
superseded_date: 2026-02-01
---

[SUPERSEDED by 2026-02-01-better-approach.md]

# 原標題
...
```

### 歸檔

將過時但有歷史價值的記錄移到 `archive/`：

```
.claude/memory/
├── learnings/
├── archive/              # 歸檔目錄
│   └── learnings/
│       └── 2025-*.md     # 過期的學習記錄
```

### 刪除

完全過時或錯誤的記錄可直接刪除：

```bash
git rm .claude/memory/failures/2025-01-01-wrong-diagnosis.md
git commit -m "chore: remove obsolete failure record"
```

## 清理 Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  Memory 清理 Checklist（每季度執行）                            │
│                                                                 │
│  □ 1. 統計各類型條目數量                                        │
│       learnings: __ 筆  failures: __ 筆  decisions: __ 筆      │
│                                                                 │
│  □ 2. 識別過時條目                                              │
│       - 超過 90 天的 failures                                   │
│       - 成功率 < 30% 的 strategies                              │
│       - 被新經驗取代的 learnings                                │
│                                                                 │
│  □ 3. 執行清理                                                  │
│       - 標註 [SUPERSEDED] 或 [REVERSED]                        │
│       - 移動到 archive/                                         │
│       - 刪除完全過時的                                          │
│                                                                 │
│  □ 4. 更新 index.md                                             │
│       - 移除已刪除/歸檔的條目                                   │
│       - 更新統計數字                                            │
│       - 更新 Last curated 日期                                  │
│                                                                 │
│  □ 5. 提交變更                                                  │
│       git add .claude/memory/ && git commit -m "chore: memory"  │
└─────────────────────────────────────────────────────────────────┘
```

## 自動化建議

可配置 Claude Code Hook 提醒清理：

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "find .claude/memory -name '*.md' | wc -l | xargs -I {} echo '📊 Memory entries: {}'"
      }
    ]
  }
}
```
