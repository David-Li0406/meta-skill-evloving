# TASKS Skill 快速開始

> 3 分鐘入門任務分解

## 基本用法

```bash
# 從 plan ID 載入並分解任務
/multi-tasks user-auth

# 等同於
/multi-tasks --from-plan user-auth
```

## 執行模式

```bash
# 快速模式：2 視角，適合小功能
/multi-tasks --quick user-auth

# 標準模式：4 視角（預設）
/multi-tasks user-auth

# 深度模式：6 視角，適合大功能
/multi-tasks --deep user-auth
```

## 前置條件

確保已完成 PLAN 階段：

```
.claude/memory/plans/{plan-id}/
├── implementation-plan.md   # 必須
├── milestones.md            # 必須
└── risk-mitigation.md       # 可選
```

## 輸出結果

```
.claude/memory/tasks/{feature-id}/
├── tasks.yaml              # 主輸出：任務定義
├── dependency-graph.md     # 依賴圖
└── execution-plan.md       # 執行計劃
```

## 常用選項

```bash
--tdd              # 強制 TDD 順序（測試任務優先）
--no-memory        # 不存檔到 Memory
--perspectives N   # 使用 N 個視角
```

## 輸出範例

```
✅ 任務分解完成：user-auth

📊 分解摘要：
   - 4 個視角完成
   - 15 個任務產出
   - 3 個 Wave 分組
   - 預估總時長：8h

📋 任務分佈：
   - 功能任務 (T-F-*): 6 個
   - 測試任務 (TEST-*): 5 個
   - 風險任務 (RISK-*): 4 個

📁 已存檔：
   .claude/memory/tasks/user-auth/tasks.yaml
```

## 下一步

任務分解完成後，進入 IMPLEMENT 階段：

```bash
/multi-implement --from-tasks user-auth
```
