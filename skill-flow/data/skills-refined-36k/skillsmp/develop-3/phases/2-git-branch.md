# Phase 2: 建立 Git 分支

## 目標

根據 Gherkin scenario 建立功能分支，遵循專案分支命名規範，確保開發工作在獨立的分支上進行。

---

## 前置條件

- ✅ 已完成 **Step 1 (Plan Mode)**，明確了解要實作的 Gherkin scenario
- ✅ 工作目錄乾淨（無未提交的變更）
- ✅ 本地 main 分支與遠端同步

---

## 執行步驟

### Step 1: 檢查當前 Git 狀態

**執行命令**:

```bash
git status
```

**預期輸出**:

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**如果有未提交變更**:

```bash
# 選項 1: 提交變更
git add .
git commit -m "chore: save work in progress"

# 選項 2: 暫存變更
git stash push -m "WIP: work in progress"
```

---

### Step 2: 確保在 main 分支並拉取最新代碼

**執行命令**:

```bash
# 切換到 main 分支
git checkout main

# 拉取最新代碼
git pull origin main
```

**預期輸出**:

```
Already on 'main'
Already up to date.
```

---

### Step 3: 根據 Gherkin Scenario 建立分支

#### 3.1 確定分支前綴

根據工作類型選擇適當的前綴:

| 工作類型   | Prefix     | 使用時機                | 範例                                  |
|--------|------------|---------------------|-------------------------------------|
| 新功能    | `feature/` | 實作新的業務功能            | `feature/user-can-purchase-tickets` |
| Bug 修復 | `bugfix/`  | 修復非緊急的 bug          | `bugfix/fix-order-status-update`    |
| 緊急修復   | `hotfix/`  | 修復生產環境緊急問題          | `hotfix/fix-payment-failure`        |
| 測試補充   | `test/`    | 增加測試覆蓋率或測試重構        | `test/add-order-service-tests`      |
| 文件更新   | `docs/`    | 更新文件（非 scenario 相關） | `docs/update-api-documentation`     |
| 維護工作   | `chore/`   | 依賴升級、設定調整等          | `chore/upgrade-next-to-15`          |

#### 3.2 從 Scenario 標題產生分支名稱

**轉換規則**:

1. 提取 Gherkin scenario 的關鍵字
2. 轉換為英文（如為中文）
3. 使用 kebab-case（全小寫 + 連字符）
4. 移除冗餘詞彙（可以、應該、能夠等）

**轉換範例**:

| Gherkin Scenario 標題 | 分支名稱                                        |
|---------------------|---------------------------------------------|
| 使用者可以購買活動票券         | `feature/user-can-purchase-event-tickets`   |
| 管理員可以編輯活動資訊         | `feature/admin-can-edit-event-info`         |
| 修復結帳頁面顯示錯誤金額        | `bugfix/fix-checkout-page-incorrect-amount` |
| 緊急修復生產環境登入失敗        | `hotfix/fix-production-login-failure`       |
| 增加訂單服務單元測試覆蓋率       | `test/increase-order-service-coverage`      |

**非 Scenario 相關工作**:

| 工作描述             | 分支名稱                            |
|------------------|---------------------------------|
| 更新 API 文件        | `docs/update-api-documentation` |
| 升級 Next.js 到 v15 | `chore/upgrade-next-to-15`      |
| 重構資料庫查詢層         | `refactor/database-query-layer` |

#### 3.3 建立分支

**執行命令**:

```bash
git checkout -b {prefix}/{description}
```

**實際範例**:

```bash
# Scenario: 使用者可以購買活動票券
git checkout -b feature/user-can-purchase-event-tickets

# Scenario: 修復訂單狀態更新失敗
git checkout -b bugfix/fix-order-status-update-failure

# 非 scenario: 更新測試文件
git checkout -b docs/update-testing-documentation
```

---

### Step 4: 驗證分支建立成功

**執行命令**:

```bash
git branch --show-current
```

**預期輸出**:

```
feature/user-can-purchase-event-tickets
```

**驗證檢查清單**:

- [ ] 分支名稱使用正確的 prefix
- [ ] 分支名稱使用 kebab-case（全小寫 + 連字符）
- [ ] 分支名稱能清楚表達工作內容
- [ ] 分支名稱長度合理（不超過 50 個字元）

---

## 完成條件

- ✅ Git 工作目錄乾淨
- ✅ 已拉取最新 main 分支代碼
- ✅ 分支名稱符合命名規範
- ✅ 成功切換到新分支
- ✅ 分支名稱能清楚反映 Gherkin scenario 或工作內容

---

## 錯誤處理

### 問題 1: 工作目錄有未提交變更

**錯誤訊息**:

```
error: Your local changes to the following files would be overwritten by checkout
```

**解決方法**:

```bash
# 選項 1: 提交變更
git add .
git commit -m "chore: save work in progress"

# 選項 2: 暫存變更
git stash push -m "WIP before branch switch"

# 然後重新執行 checkout
git checkout main
```

---

### 問題 2: 分支名稱已存在

**錯誤訊息**:

```
fatal: A branch named 'feature/user-can-purchase-tickets' already exists.
```

**解決方法**:

**選項 1**: 切換到現有分支

```bash
git checkout feature/user-can-purchase-tickets
```

**選項 2**: 刪除舊分支（如確定不需要）

```bash
# 先切換到 main
git checkout main

# 刪除本地分支
git branch -D feature/user-can-purchase-tickets

# 重新建立
git checkout -b feature/user-can-purchase-tickets
```

**選項 3**: 使用不同的分支名稱

```bash
git checkout -b feature/user-can-purchase-tickets-v2
```

---

### 問題 3: Git pull 失敗

**錯誤訊息**:

```
fatal: unable to access 'https://github.com/...': Could not resolve host
```

**解決方法**:

1. 檢查網路連線
2. 檢查遠端倉庫 URL:
   ```bash
   git remote -v
   ```
3. 如果網路無法連線，可以跳過 pull，但需注意本地可能不是最新代碼

---

## 分支命名最佳實踐

### ✅ 良好的分支名稱

- `feature/user-authentication` - 清楚、簡潔
- `bugfix/fix-login-redirect` - 使用動詞 "fix"
- `test/add-e2e-checkout-tests` - 明確說明測試範圍
- `docs/update-readme` - 簡單明瞭

### ❌ 不良的分支名稱

- `feature/Feature123` - 使用大寫字母（應使用 kebab-case）
- `fix_bug` - 使用底線（應使用連字符）
- `user-auth` - 缺少 prefix
- `feature/update` - 描述過於模糊
- `feature/user_can_purchase_event_tickets_and_view_order_history` - 過長且包含多個功能

---

## 下一步

分支建立完成後，進入 **Step 3: 啟動 Wallaby** - 啟動即時測試監控

詳見 [3-wallaby-setup.md](3-wallaby-setup.md)
