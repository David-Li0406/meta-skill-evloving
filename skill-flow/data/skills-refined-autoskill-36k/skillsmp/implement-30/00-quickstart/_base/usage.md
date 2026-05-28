# Quick Start Guide

> 3 分鐘快速上手 Multi-Agent Implement

## 最簡用法

```bash
/multi-implement --from-plan user-auth
```

這會：
1. 載入 user-auth 的實作計劃
2. 啟動 4 個監督視角
3. 主 Agent 按計劃實作
4. 視角即時審查並回饋
5. 產出程式碼和記錄

## 常用模式

### 從計劃檔案載入

```bash
/multi-implement plans/user-auth/implementation-plan.md
```

### 直接指定任務

```bash
/multi-implement --task "新增登入功能"
```

適用：沒有預先規劃的小任務

### 快速實作（2 視角）

```bash
/multi-implement --quick --from-plan small-feature
```

適用：小型功能、低風險變更

### 嚴格實作（6 視角）

```bash
/multi-implement --deep --from-plan core-system
```

適用：核心功能、高風險變更

## 監督模式解說

### 實作循環

```
寫程式碼 → 視角審查 → 收到回饋 → 修正 → 繼續
    ↑__________________________|
```

### 回饋類型

| 符號 | 意義 | 行動 |
|------|------|------|
| ✅ | 通過 | 繼續下一步 |
| ⚠️ | 警告 | 記錄，可繼續 |
| ❌ | 阻擋 | 必須修正 |
| 💡 | 建議 | 可選改進 |

### 範例回饋

```
TDD 守護者：
  ❌ 函數 login() 缺少測試
  💡 建議添加邊界案例

主 Agent 回應：
  → 添加 login() 的單元測試
  → 添加空密碼、錯誤密碼測試
```

## 輸出位置

所有實作結果存儲在：

```
.claude/memory/implementations/[feature-id]/
├── implementation-log.md  ← 實作記錄（先看這個）
├── changes-summary.md     ← 變更摘要
├── pass-at-k-metrics.md   ← 成功率統計
└── perspectives/          ← 各視角報告
    ├── tdd-report.md
    ├── performance-report.md
    ├── security-report.md
    └── maintainability.md
```

## pass@k 機制

### 什麼是 pass@k

嘗試 k 次，計算成功率：
- pass@1 = 一次通過率
- pass@3 = 三次內通過率

### 失敗重試

```
嘗試 1: 編譯失敗
  → 分析錯誤
  → 修正問題
嘗試 2: 測試失敗
  → 分析錯誤
  → 修正問題
嘗試 3: 通過 ✅

pass@3 = 100%
```

## 進階技巧

### 調整 pass@k

```bash
/multi-implement --pass-k 5 --from-plan complex-feature
```

增加重試次數（適用於複雜功能）

### 指定視角數量

```bash
/multi-implement --perspectives 3 --from-plan feature
```

### 不存檔

```bash
/multi-implement --no-memory --task "臨時修改"
```

### 與 evolve 整合

實作過程會自動與 evolve Checkpoint 同步：
- CP1: 環境驗證
- CP2: Build + Test
- CP5: 失敗分析（如需要）
- CP3.5: 完成後更新 index.md

## 實作失敗後

### 1. 查看失敗原因

```bash
cat .claude/memory/implementations/user-auth/pass-at-k-metrics.md
```

### 2. 查看視角建議

```bash
cat .claude/memory/implementations/user-auth/perspectives/tdd-report.md
```

### 3. 重新實作

```bash
/multi-implement --from-plan user-auth
```

## 下一步

- [了解預設視角](../../01-perspectives/_base/default-perspectives.md)
- [監督模式說明](../../config/supervision-mode.md)
- [回饋循環配置](../../config/feedback-loop.md)
