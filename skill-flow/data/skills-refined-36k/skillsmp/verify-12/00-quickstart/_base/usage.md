# Quick Start Guide

> 3 分鐘快速上手 Multi-Agent Verify

## 最簡用法

```bash
/multi-verify user-auth
```

這會：
1. 啟動 4 個並行驗證 Agent
2. 從不同視角執行測試
3. 計算 pass@k 成功率
4. 決定是否可以發布
5. 自動存檔到 Memory

## 常用模式

### 從計劃載入驗收標準

```bash
/multi-verify --from-plan user-auth-plan user-auth
```

自動載入計劃中定義的驗收標準

### 快速驗證（2 視角）

```bash
/multi-verify --quick user-auth
```

適用：快速檢查、小型變更

### 深度驗證（6 視角）

```bash
/multi-verify --deep user-auth
```

適用：重大發布、核心功能

### 驗證所有功能

```bash
/multi-verify --all
```

適用：完整版本發布前

## 輸出位置

所有驗證結果存儲在：

```
.claude/memory/verifications/[feature-id]/
├── release-decision.md  ← 發布決策（先看這個）
├── test-results/
│   ├── pass-at-k.md     ← 成功率統計
│   └── failures.md      ← 失敗分析
├── overview.md          ← 一頁摘要
└── perspectives/        ← 各視角詳細報告
```

## 發布決策

### ✅ SHIP IT

```
條件：
- 功能測試：100% 通過
- 邊界測試：≥ 90% 通過
- 回歸測試：100% 通過
- 驗收測試：100% 通過

行動：可以發布
```

### ❌ BLOCKED

```
條件：任一標準未達標

行動：
1. 查看失敗詳情
2. 修復問題
3. 重新驗證
```

## pass@k 解讀

| 指標 | 意義 |
|------|------|
| pass@1 | 一次通過率 |
| pass@3 | 三次內通過率 |

### 範例

```
測試：登入功能
  執行 1: PASS ✅
  執行 2: FAIL ❌
  執行 3: PASS ✅

pass@1 = 66.7%
pass@3 = 100%（3 次內至少 1 次成功）
```

## 進階技巧

### 調整 pass@k

```bash
/multi-verify --pass-k 5 user-auth
```

增加重試次數（適用於不穩定測試）

### 指定視角數量

```bash
/multi-verify --perspectives 3 user-auth
```

### 不存檔

```bash
/multi-verify --no-memory user-auth
```

### 與 evolve 整合

驗證結果會自動與 evolve Checkpoint 同步：
- CP1: 載入相關記錄
- CP2: Build + Test
- CP6: 發布驗證
- CP3.5: 完成後更新 index.md

## 驗證失敗後

### 1. 分析失敗原因

```bash
# 查看失敗詳情
cat .claude/memory/verifications/user-auth/test-results/failures.md
```

### 2. 修復問題

```bash
# 使用 implement skill 修復
/multi-implement fix-auth-edge-cases
```

### 3. 重新驗證

```bash
/multi-verify user-auth
```

## 下一步

- [了解預設視角](../../01-perspectives/_base/default-perspectives.md)
- [發布標準配置](../../config/release-criteria.md)
- [pass@k 計算詳解](../../config/pass-at-k-metrics.md)
