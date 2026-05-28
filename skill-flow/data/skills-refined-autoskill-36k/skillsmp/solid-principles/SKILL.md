---
name: solid-principles
description: 協助檢查 PHP/Laravel 程式碼是否符合 SOLID 原則。當需要審查程式碼架構、重構建議、或評估設計品質時載入此技能。
---

# SOLID 原則檢查技能

本技能提供 PHP/Laravel 程式碼的 SOLID 原則審查指引。

## 檢查項目

### SRP - 單一職責原則 (Single Responsibility Principle)

**檢查重點**: 每個 class/method 是否只有單一職責

**警示信號**:
- class 名稱包含 `And`、`Or`、`Manager`、`Handler` 但職責不明確
- method 超過 3 個主要動作
- 一個 class 依賴超過 7 個其他 class
- Service 同時處理用戶邏輯、郵件發送、報表生成

**修正範例**:
```php
// ❌ 違反 SRP
class UserService {
    public function createUser() { ... }
    public function sendEmail() { ... }      // 應移至 EmailService
    public function generateReport() { ... } // 應移至 ReportService
}

// ✅ 符合 SRP
class UserService { /* 只處理用戶邏輯 */ }
class EmailService { /* 只處理郵件 */ }
class ReportService { /* 只處理報表 */ }
```

---

### OCP - 開放封閉原則 (Open/Closed Principle)

**檢查重點**: 新功能是否透過擴展而非修改實現

**警示信號**:
- `switch/case` 或 `if-else` 鏈處理類型判斷
- 修改現有 class 以支援新功能
- 每次新增類型都需要改動多處程式碼

**修正範例**:
```php
// ❌ 違反 OCP
if ($type == 'A') { ... }
elseif ($type == 'B') { ... }
elseif ($type == 'C') { ... }

// ✅ 符合 OCP - 使用策略模式
interface IPaymentProcessor {
    public function process(): void;
}
class CreditCardProcessor implements IPaymentProcessor { ... }
class PayPalProcessor implements IPaymentProcessor { ... }
```

---

### LSP - 里氏替換原則 (Liskov Substitution Principle)

**檢查重點**: 子類別是否能完全替代父類別

**警示信號**:
- 子類別覆寫方法拋出 `NotImplementedException`
- 子類別改變父類別方法的預期行為
- 子類別強化前置條件或弱化後置條件

---

### ISP - 介面隔離原則 (Interface Segregation Principle)

**檢查重點**: 介面是否精簡且專注

**警示信號**:
- 介面方法超過 5 個
- 實作類別有空方法或拋出 `NotSupported`
- 客戶端被迫依賴不需要的方法

---

### DIP - 依賴反轉原則 (Dependency Inversion Principle)

**檢查重點**: 是否依賴抽象而非具體實作

**警示信號**:
- 直接 `new` 具體類別（非 DTO/Entity）
- 高層模組 import 低層模組具體類別
- 未使用依賴注入
- Service 直接實例化 Repository

**修正範例**:
```php
// ❌ 違反 DIP
class UserService {
    public function __construct() {
        $this->repo = new UserRepository(); // 直接依賴具體類別
    }
}

// ✅ 符合 DIP
class UserService {
    public function __construct(IUserRepository $repo) {
        $this->repo = $repo; // 依賴抽象介面
    }
}
```

---

## 輸出格式

對每個檢查項目提供：
1. **狀態**: ✅ 通過 / ⚠️ 警告 / ❌ 違反
2. **問題描述**: 具體說明違反原則的位置
3. **修正建議**: 提供重構方向或程式碼範例
