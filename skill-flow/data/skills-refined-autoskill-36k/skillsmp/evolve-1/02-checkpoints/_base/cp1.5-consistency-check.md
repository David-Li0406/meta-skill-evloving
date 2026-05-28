# Checkpoint 1.5: 一致性檢查 (Consistency Check)

> 🚨 **強制檢查點** - 不可跳過

## 核心理念

**先找現有的，再決定要不要新建**

- ❌ 錯誤：直接寫新的 → 事後發現重複
- ✅ 正確：先搜尋 → 確認沒有 → 才動手

## 檢查流程

**Phase 1: 基礎檢查（必執行）** → 偵測是否為架構級變更 → **Phase 2: 架構檢查（自動觸發）**

| Phase | 檢查項目 |
|-------|----------|
| Phase 1 | 搜尋現有實作、檢查專案慣例、檢查 Schema/API |
| Phase 2 | 依賴方向、錯誤處理一致性、橫切關注點、模式一致性 |

---

## Phase 1: 基礎檢查（必執行）

🔗 **開始寫程式碼前（強制）**

在 CP1 (Memory Search) 完成後、實際寫程式碼前：

- [ ] **1. 搜尋現有實作**：用關鍵字搜尋 `src/` → 有類似則複用，無則記錄「已確認無重複」
- [ ] **2. 檢查專案慣例**：閱讀 `CLAUDE.md` / `README.md` 確認命名、目錄結構、錯誤處理
- [ ] **3. 檢查 Schema/API**：若涉及資料結構或 API，搜尋現有定義確保一致

❌ 禁止：不搜尋就開始寫、發現類似的還另起爐灶
✅ 必須：先確認「不是重複造輪子」、新程式碼符合既有風格

## 搜尋範例

### 1. 搜尋現有實作

```python
# 搜尋功能相關的程式碼
Grep(
    pattern="formatDate|dateFormat|formatTime",
    path="src/",
    output_mode="files_with_matches"
)

# 搜尋類似的 utility 函數
Grep(
    pattern="export (function|const) .*[Ff]ormat",
    path="src/utils/",
    output_mode="content",
    C=3
)

# 找到後閱讀內容
Read(file_path="src/utils/time.ts")
```

### 2. 檢查專案慣例

```python
# 閱讀專案規範
Read(file_path="CLAUDE.md")
Read(file_path="docs/CONTRIBUTING.md")

# 找類似功能的實作作為參考
Grep(
    pattern="export (function|class)",
    path="src/utils/",
    output_mode="files_with_matches",
    head_limit=5
)
# 然後閱讀其中一個作為風格參考
```

### 3. 檢查 Schema / API

```python
# 搜尋相關型別定義
Grep(
    pattern="interface.*User|type.*User",
    path="src/types/",
    output_mode="content"
)

# 搜尋相關 API 端點
Grep(
    pattern="/api/user|userRouter",
    path="src/",
    output_mode="files_with_matches"
)
```

## 決策樹

| 搜尋結果 | 行動 |
|----------|------|
| 找到完全符合的實作 | 直接使用，不要新建 |
| 找到部分符合的實作 | 擴展現有實作 |
| 找到類似但不同用途 | 參考其風格，確保一致性 |
| 完全沒找到 | 記錄「已確認無重複」，開始新建 |

## 一致性檢查清單

| 檢查項 | 問題 | 若不符合 |
|--------|------|----------|
| **功能重複** | 這個功能是否已經存在？ | 複用現有的 |
| **命名一致** | 命名是否符合專案慣例？ | 調整命名 |
| **位置正確** | 檔案應該放在哪個目錄？ | 放到正確位置 |
| **風格一致** | 是否符合專案程式碼風格？ | 參考現有實作 |
| **介面一致** | API/Schema 是否與現有設計一致？ | 調整設計 |

## 常見違規場景

| 場景 | 問題 | 正確做法 |
|------|------|----------|
| 新增 `formatDate()` | 已有 `src/helpers/time.ts` 的 `formatDateTime()` | 擴展現有函數 |
| 新增 `UserCard` 組件 | 已有 `src/components/cards/` 目錄 | 放到正確目錄 |
| 新增 `fetchUser` API | 已有 `userService.ts` 處理 user 相關 | 加到現有 service |
| 命名為 `get_user_data` | 專案慣例是 camelCase | 改為 `getUserData` |

---

## Phase 2: 架構檢查（自動偵測觸發）

> Phase 2 不是每次都執行，而是根據變更範圍自動判斷

### 觸發條件

以下**任一條件**成立時，自動觸發架構檢查：

| 條件 | 說明 | 範例 |
|------|------|------|
| **新增目錄/模組** | 建立新的目錄結構 | `mkdir src/newModule/` |
| **變更涉及 3+ 目錄** | 跨多個層級的修改 | 同時改 controller + service + repository |
| **新增外部依賴** | 修改依賴配置檔 | 編輯 `package.json`、`requirements.txt` |
| **觸及核心目錄** | 路徑含關鍵字 | `core/`、`infra/`、`domain/`、`shared/`、`lib/` |
| **新增公開 API** | 建立對外介面 | 新增 REST endpoint、GraphQL schema |

### 架構檢查項目

🏗️ **架構檢查（觸發時執行）**

- [ ] **1. 依賴方向檢查**：確認沒有「下層依賴上層」違規（如 repository/ 不應 import controller/）
- [ ] **2. 錯誤處理一致性**：搜尋現有模式，新程式碼使用相同 Error 類別
- [ ] **3. 橫切關注點**：使用現有 logger/metrics，不要自己造輪子
- [ ] **4. 模式一致性**：遵循 `.claude/memory/patterns/` 記錄的設計模式

❌ 禁止：違反依賴方向、混用錯誤處理風格
✅ 必須：使用既有機制、遵循已採用的模式

### 架構檢查範例

#### 1. 依賴方向檢查

```python
# 搜尋可能的違規依賴
# 假設專案分層：controller → service → repository

# 檢查 repository 是否錯誤依賴 controller
Grep(
    pattern="from.*controller|import.*controller",
    path="src/repositories/",
    output_mode="content"
)

# 檢查 service 是否錯誤依賴 controller
Grep(
    pattern="from.*controller|import.*controller",
    path="src/services/",
    output_mode="content"
)
```

#### 2. 錯誤處理一致性

```python
# 搜尋現有的錯誤處理模式
Grep(
    pattern="throw new|raise |class.*Error|catch|except",
    path="src/",
    output_mode="content",
    head_limit=20
)

# 找到後確認新程式碼使用相同模式
# 例：專案用 AppError → 新程式碼也應該用 AppError
```

#### 3. 橫切關注點

```python
# 搜尋現有的 logging 機制
Grep(
    pattern="logger\\.|log\\.|console\\.log",
    path="src/",
    output_mode="files_with_matches"
)

# 若專案有統一的 logger，新程式碼不應該直接用 console.log
```

#### 4. 模式一致性

```python
# 檢查專案是否有記錄設計模式
Read(file_path=".claude/memory/patterns/design-patterns-in-use.md")

# 或搜尋現有的 pattern 實作
Grep(
    pattern="Repository|Factory|Strategy|Singleton",
    path="src/",
    output_mode="files_with_matches"
)
```

### 架構檢查清單

| 檢查項 | 問題 | 若不符合 |
|--------|------|----------|
| **依賴方向** | 是否有逆向依賴？ | 調整依賴關係 |
| **錯誤處理** | 是否與現有模式一致？ | 使用專案的 Error 類別 |
| **Logging** | 是否使用統一的 logger？ | 改用專案的 logging 機制 |
| **Metrics** | 是否使用統一的 metrics？ | 整合到現有 metrics 系統 |
| **設計模式** | 是否符合已採用的模式？ | 遵循專案的 pattern |

### 觸發判斷邏輯

**Phase 1 完成** → 檢查變更範圍 → **觸發條件判斷**（任一為 Yes → Phase 2，否則跳過）

---

## 與 CP1 的關係

| 階段 | 搜尋目標 | 輸出 |
|------|----------|------|
| CP1 (Memory Search) | `.claude/memory/` 過去經驗 | 相關經驗 |
| CP1.5 Phase 1 | `src/` 現有程式碼 | 一致性確認 |
| CP1.5 Phase 2 | 架構層級檢查（若觸發） | 架構合規 |

→ 所有檢查完成後才開始寫程式碼

## 為什麼重要

1. **避免重複造輪子** - 不要寫已經存在的東西
2. **維持程式碼一致性** - 新舊程式碼風格統一
3. **降低維護成本** - 不會有多個做相同事情的實作
4. **加速開發** - 複用比新建更快
