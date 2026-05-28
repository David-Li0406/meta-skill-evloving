# 中斷與恢復

## 設計理念

**中斷應該是無痛的** — 用戶可以在任何時刻離開，下次回來時無縫繼續。

## Session 狀態

### 狀態結構

```json
{
  "session_id": "session-001",
  "plan_id": "ecommerce-mvp",
  "created_at": "2025-01-21T10:00:00Z",
  "last_active": "2025-01-21T11:30:00Z",

  "status": "active",  // active | paused | completed | abandoned

  "current_task": {
    "id": "backend-api",
    "phase": "do",  // plan | do | check | act
    "progress": 60,
    "checkpoint": {
      "files_modified": ["src/api/user.ts"],
      "pending_changes": ["src/api/auth.ts"],
      "last_commit": "abc123"
    }
  },

  "context": {
    "working_directory": "/path/to/project",
    "branch": "feature/user-auth",
    "environment_vars": {}
  }
}
```

### 狀態保存時機

```yaml
save_triggers:
  # 自動保存
  - "任務階段轉換"
  - "每 5 分鐘"
  - "重要操作完成"

  # 強制保存
  - "Session 結束"
  - "用戶請求暫停"
  - "錯誤發生"
```

## 中斷處理

### 優雅中斷

```bash
# 用戶主動暫停
/claude-plan --pause
```

**執行動作**：
1. 完成當前原子操作
2. 保存 Session 狀態
3. 釋放任務鎖（可配置）
4. commit 已完成的變更

### 意外中斷

```
Session 意外終止（關閉終端、網路斷線等）
         ↓
┌─────────────────────────────────────────────────────────┐
│  自動恢復機制                                            │
│  1. 任務鎖設有過期時間（預設 1 小時）                     │
│  2. 下次啟動時檢查未完成的 checkpoint                    │
│  3. 回滾到最後一個 commit（如有未提交變更）              │
│  4. 提供恢復選項                                         │
└─────────────────────────────────────────────────────────┘
```

## 恢復流程

### 啟動時檢查

```python
def startup():
    # 1. 檢查是否有進行中的計畫
    plans = load_plans()
    active = [p for p in plans if p.status == "active"]

    if not active:
        # 沒有進行中的計畫，正常啟動
        return start_new_or_claim()

    # 2. 檢查是否有屬於這個用戶的 Session
    my_sessions = find_my_sessions()

    if my_sessions:
        # 有之前的 Session
        return offer_resume(my_sessions)

    # 3. 沒有之前的 Session，認領新任務
    return claim_available_task()
```

### 恢復選項

```
檢測到未完成的計畫：電商 MVP

您之前的 Session 狀態：
  - 任務: 後端 API
  - 進度: 60%
  - 最後活動: 2 小時前
  - 未提交變更: 2 個檔案

選擇操作：
  [1] 繼續之前的任務（推薦）
  [2] 放棄之前的進度，認領新任務
  [3] 查看詳細狀態
```

### 恢復模式

```yaml
resume_modes:
  # 繼續之前的任務
  continue:
    - 載入 Session 狀態
    - 恢復工作目錄
    - 從 checkpoint 繼續

  # 放棄並重新認領
  abandon:
    - 回滾未提交的變更
    - 釋放任務鎖
    - 認領新的可用任務

  # 轉移給其他 Session
  handover:
    - 保存當前進度
    - 標記為可認領
    - 其他 Session 可以接手
```

## 智能需求插入

### 觸發方式

```bash
/claude-plan --add "新增支付功能"
```

### 處理流程

```
新需求: "新增支付功能"
         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: 需求分析                                        │
│  • 類型: 新功能                                          │
│  • 複雜度: high                                          │
│  • 依賴: 購物車、用戶系統                                │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: 緊急程度評估                                    │
│  • P0: 阻塞其他功能                                      │
│  • P1: 重要但不阻塞                                      │
│  • P2: 一般優先級                                        │
│  • P3: 可延後                                            │
│                                                         │
│  AI 判斷: P1（支付是 MVP 核心功能）                       │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: 排程決策                                        │
│  • 插隊條件: P0 或用戶指定                               │
│  • 排隊條件: P1-P3                                       │
│                                                         │
│  決策: 加入佇列，排在「訂單系統」之前                     │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: 通知與更新                                      │
│  • 更新 plan.md                                          │
│  • 更新 tasks.md                                         │
│  • 通知相關 Session                                      │
│  • commit 變更                                           │
└─────────────────────────────────────────────────────────┘
```

### 優先級定義

```yaml
priority_levels:
  P0_blocker:
    description: "阻塞其他任務，必須立即處理"
    action: "中斷當前任務（完成當前原子操作後）"

  P1_high:
    description: "重要功能，影響 MVP"
    action: "加入佇列頭部"

  P2_medium:
    description: "一般功能"
    action: "加入佇列中間"

  P3_low:
    description: "可延後，nice-to-have"
    action: "加入佇列尾部"
```

## 跨 Session 通信

### 通知機制

```yaml
notifications:
  # 新需求插入
  requirement_added:
    target: "all_sessions"
    message: "新需求已加入: {requirement_name}"

  # 任務完成
  task_completed:
    target: "blocked_tasks"
    message: "依賴已解除: {task_name}"

  # 衝突警告
  conflict_warning:
    target: "conflicting_sessions"
    message: "偵測到檔案衝突: {files}"
```

### 實現方式

```
.claude/plans/{plan_id}/
├── notifications.json      # 通知佇列
└── sessions/
    ├── session-001.json
    └── session-002.json

每個 Session 定期檢查 notifications.json
```
