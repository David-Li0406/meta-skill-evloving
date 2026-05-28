# 快速開始

## 30 秒上手

```bash
# 1. 啟動新計畫
/claude-plan 建立一個待辦事項 App

# 2. 新 Session 自動加入（在另一個終端）
/claude-plan

# 3. 查看進度
/claude-plan --dashboard
```

## 常用命令

| 命令 | 說明 |
|------|------|
| `/claude-plan [描述]` | 啟動新計畫 / 自動認領任務 |
| `/claude-plan --dashboard` | 開啟視覺化追蹤 |
| `/claude-plan --add "需求"` | 插入新需求 |
| `/claude-plan --resume` | 從中斷處繼續 |
| `/claude-plan --list` | 列出所有計畫 |
| `/claude-plan --switch "名稱"` | 切換專案 |

## 典型工作流程

### 單人模式

```bash
/claude-plan 建立部落格系統
# Claude 自動：
# 1. 分解任務
# 2. 依序執行 PDCA
# 3. 每完成一個任務自動 commit
# 4. 全部完成後 push + 開 PR
```

### 多人/多 Session 模式

```bash
# 終端 1
/claude-plan 建立電商平台

# 終端 2（自動認領不同任務）
/claude-plan

# 終端 3
/claude-plan

# 三個 Session 並行處理不同任務
```

### 中斷後恢復

```bash
# 工作到一半需要離開
# 直接關閉終端即可

# 下次回來
/claude-plan --resume
# 或直接
/claude-plan  # 會自動偵測未完成的計畫
```

## 進階用法

### 指定並行度

```bash
# 最多同時 3 個任務並行（預設無限制）
/claude-plan --max-parallel 3
```

### 跳過自動 GitHub

```bash
# 只執行，不自動 push
/claude-plan --no-push
```

### 強制重新規劃

```bash
# 重新分解任務（不影響已完成的）
/claude-plan --replan
```
