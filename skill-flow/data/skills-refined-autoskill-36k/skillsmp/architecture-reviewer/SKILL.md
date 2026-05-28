---
name: "architecture-reviewer"
description: "Activates when user requests architecture analysis, code review, refactoring suggestions, design pattern evaluation, or SOLID principles assessment. Do NOT use for security-specific audits (use security-auditor) or performance optimization (use performance-analyst). Examples: 'Review this code for SOLID', 'Is this following Clean Architecture?'"
---

# Architecture Reviewer Skill

## 🧠 Expertise

資深軟體架構師，專精於 DDD、Clean Architecture 與 SOLID 原則，擁有 15+ 年企業級系統設計經驗。

---

## 1. SOLID 原則檢查

### 1.1 SRP（Single Responsibility Principle，單一職責原則）

**定義**：每個 class/module 只有單一職責。

**檢查要點**：
- class 名稱是否清楚表達單一職責
- method/function 是否只做一件事
- class 的依賴數量是否合理

**紅旗標誌**：
- ❌ class 名稱包含 `And`、`Or`、`Manager`、`Handler` 但職責不明確
- ❌ method 超過 3 個主要動作
- ❌ 一個 class 依賴超過 7 個其他 class

---

### 1.2 OCP（Open/Closed Principle，開放封閉原則）

**定義**：新功能透過擴展而非修改實現。

**檢查要點**：
- 新增功能是否需要修改現有 class
- 是否使用 Interface 或抽象類別來支援擴展

**紅旗標誌**：
- ❌ 使用 `switch/case` 或 `if-else` 鏈處理類型判斷
- ❌ 修改現有 class 以支援新功能

---

### 1.3 LSP（Liskov Substitution Principle，里氏替換原則）

**定義**：子類別能完全替代父類別。

**檢查要點**：
- 子類別是否改變父類別方法的預期行為
- 子類別是否拋出父類別未定義的例外

**紅旗標誌**：
- ❌ 子類別覆寫方法拋出 `NotImplementedException`
- ❌ 子類別改變父類別方法的預期行為

---

### 1.4 ISP（Interface Segregation Principle，介面隔離原則）

**定義**：介面精簡且專注。

**檢查要點**：
- 介面方法數量是否合理
- 實作類別是否需要實作所有方法

**紅旗標誌**：
- ❌ 介面方法超過 5 個
- ❌ 實作類別有空方法或拋出 `NotSupported`

---

### 1.5 DIP（Dependency Inversion Principle，依賴反轉原則）

**定義**：依賴抽象而非具體實作。

**檢查要點**：
- 是否使用依賴注入
- 是否依賴 Interface 而非具體類別

**紅旗標誌**：
- ❌ 直接實例化具體類別（非 DTO/Entity）
- ❌ 高層模組 import 低層模組具體類別
- ❌ 未使用依賴注入

---

## 2. 多層架構規範

| 層級 | 允許 | 禁止 |
|-----|-----|-----|
| **Controller/Handler** | Request → Service → Response | 業務邏輯、狀態判斷、Repository 直呼 |
| **Validation** | 格式與型別驗證 | DB 查詢、業務判斷 |
| **Service** | 業務規則、狀態檢核、交易 | - |
| **Repository/DAO** | CRUD 資料存取 | 業務邏輯 |

### Service 層要求
- 必須透過 Interface 依賴 Repository（DIP）
- 驗證失敗需拋出具體 Exception（含錯誤語意）

---

## 3. DDD（Domain-Driven Design）概念

### 3.1 Bounded Context（限界上下文）

**定義**：明確的業務邊界，每個上下文內部有獨立的模型與術語。

**紅旗標誌**：
- ❌ 跨上下文直接引用 Entity 或 Value Object
- ❌ 同一術語在不同上下文中有不同含義但未區分

### 3.2 Aggregate（聚合）

**定義**：一組相關物件的集合，有一個 Aggregate Root 作為唯一入口。

**紅旗標誌**：
- ❌ 外部直接存取非 Root 的內部 Entity
- ❌ 單一交易跨越多個 Aggregate
- ❌ Aggregate 過大（超過 5 個 Entity）

### 3.3 Entity vs Value Object

| 類型 | 特性 |
|-----|-----|
| **Entity** | 具有唯一識別（ID），生命週期內可變 |
| **Value Object** | 無識別，不可變，由其屬性值定義 |

**紅旗標誌**：
- ❌ Value Object 有 setter 方法
- ❌ 比較 Value Object 時使用 ID 而非屬性值

### 3.4 Domain Event（領域事件）

**定義**：表達領域中已發生的重要事實。

**紅旗標誌**：
- ❌ 事件名稱使用現在式或命令式（應使用過去式如 `OrderPlaced`）
- ❌ 事件包含領域邏輯
- ❌ 事件有 setter 方法

---

## 4. Clean Architecture 依賴規則

| 層級 | 包含內容 | 可依賴 |
|-----|---------|-------|
| **Domain（核心）** | Entity, Value Object, Domain Event, Repository Interface | 無（最內層） |
| **Application** | Use Case, Application Service, DTO | Domain |
| **Infrastructure** | Repository Impl, External Service, Framework | Application, Domain |
| **Presentation** | Controller, API, UI | Application, Domain |

**紅旗標誌**：
- ❌ Domain 層 import Framework 類別
- ❌ Application 層直接依賴 Infrastructure 實作
- ❌ Entity 繼承 Framework 的 Base Class

---

## 5. 架構選擇指南

| 場景 | 建議架構 |
|-----|---------| 
| 簡單 CRUD 應用 | 多層架構 + SOLID |
| 複雜業務邏輯 | DDD + Clean Architecture |
| 高讀寫比差異 | CQRS |
| 需要審計追蹤、時間旅行 | Event Sourcing |
| 複雜領域 + 高效能需求 | DDD + CQRS + Event Sourcing |

> **注意**：架構複雜度應與業務複雜度相匹配，避免過度設計。
