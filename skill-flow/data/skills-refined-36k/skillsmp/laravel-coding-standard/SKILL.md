---
name: "laravel-coding-standard"
description: "Activates when user writes or reviews PHP/Laravel code, requiring Laravel-specific coding standards validation. Do NOT use for basic indentation/whitespace checks (handled by linter). Examples: 'Check naming conventions', 'Review validation format', 'Check array style'."
---

# Laravel Coding Standard Skill

## 🧠 Expertise

PHP / Laravel Coding Style 守門員，專精於語意化命名、陣列結構、Validation 格式、Enum 實作與分層架構規範。

> **核心原則**：一致性、可讀性、可維護性。
> **忽略項目**（假設已由 linter/IDE/CI 處理）：縮排、空格、空行、大括弧位置、檔案編碼與換行符號。

---

## 1. 命名規範 (Naming Conventions)

### 1.1 變數與常數

| 類型 | 規則 | 正確範例 | 錯誤範例 |
|-----|------|---------|---------|
| **變數** | **camelCase** | `$userEmail` | `$user_email`, `$UserEmail` |
| **陣列(單筆)** | **單數** | `$user = []` | `$users = []` (若僅含一筆) |
| **陣列(多筆)** | **複數** | `$userIds = []` | `$userId = []` (若含多筆) |
| **常數** | **UPPER_SNAKE_CASE** | `MAX_COUNT` | `MaxCount`, `max_count` |

### 1.2 類別與介面

| 類型 | 規則 | 正確範例 | 錯誤範例 |
|-----|------|---------|---------|
| **類別** | **PascalCase** | `MemberController` | `member_controller` |
| **介面** | **I 開頭** | `IGameService` | `GameInterface` |
| **Enum** | **PascalCase** | `OrderStatus` | `order_status` |

### 1.3 函數與方法

- **動作導向**：必須以 **動詞** 開頭。
- **List 方法**：若回傳列表，方法名稱應加 `s`。
- **格式**：**camelCase**。

```php
// ✅ 正確
public function getUserById($id) { }
public function createOrder($data) { }
public function gameListsByPlatform($platform) { }

// ❌ 錯誤
public function userById($id) { }           // 缺少動詞
public function gameListByPlatform() { }    // List 應加 s
```

---

## 2. 陣列使用規範 (Array Usage)

### 2.1 語法與結構

- **宣告**：統一使用短陣列語法 `[]`，禁止 `array()`。
- **單行陣列**：前後需加上空格 `[ 'a', 'b' ]`。
- **多行陣列**：
  - 結尾逗號：**必須** 包含（Trailing Comma）。
  - 縮排：內容向右縮排一個 Tab。
  - 對齊：結束括號 `]` 與變數宣告對齊。

```php
// ✅ 正確
$users = [
    'Test1',
    'Test2', // 結尾逗號
];

// ❌ 錯誤
$users = array();           // 禁止舊式
$users = ['a','b','c'];     // 缺少空格
```

### 2.2 鍵值對

- **格式**：`=>` 前後需有空格。
- **多行**：鍵值對陣列建議多行撰寫。

```php
// ✅ 正確
$user = [
    'name' => 'Neil',
    'email' => 'neil@example.com',
];

// ❌ 錯誤
$user = ['name'=>'Neil'];  // 缺少空格
```

---

## 3. Validation Rules 規範

### 3.1 陣列格式強制

在 Controller 與 FormRequest 中，驗證規則 **必須使用陣列格式**，禁止使用管道符號 `|` 字串格式。

```php
// ✅ 正確
$request->validate([
    'email' => [
        'required',
        'email',
        Rule::unique('users')->ignore($id),
    ],
    'status' => [ 'required', Rule::enum(OrderStatus::class) ],
]);

// ❌ 錯誤
$request->validate([
    'email' => 'required|email|unique:users',
]);
```

**理由**：
- 可讀性更高
- 易於 diff 與維護
- 支援 Rule 物件與閉包

---

## 4. Enum 使用規範

### 4.1 命名與結構

- **類別命名**：**PascalCase**，如 `OrderStatus`。
- **檔案位置**：`app/Enums/`。
- **使用 PHP 8.1+ Backed Enum**。

### 4.2 實作要求

Enum 必須包含業務邏輯方法：

1. **getLabel()**：回傳顯示用的文字（如 '已出貨'）。
2. **getColor()**：回傳前端顯示顏色（如 'success', 'danger'）。
3. **static getOptions()**：回傳 `value => label` 陣列。

```php
enum OrderStatus: string
{
    case PENDING = 'pending';
    case COMPLETED = 'completed';
    
    public function getLabel(): string
    {
        return match($this) {
            self::PENDING => '待處理',
            self::COMPLETED => '已完成',
        };
    }
    
    public static function getOptions(): array
    {
        return array_column(self::cases(), 'value', 'name');
    }
}
```

---

## 5. 分層架構規範

### 5.1 Controller 職責

| 允許 | 禁止 |
|-----|------|
| 接收請求、呼叫 Service、回傳 Response | 業務邏輯、直接資料庫操作 |

```php
// ✅ 正確
public function store(StoreUserRequest $request): JsonResponse
{
    $user = $this->userService->createUser($request->validated());
    
    return response()->json([ 'data' => $user ]);
}

// ❌ 錯誤：業務邏輯寫在 Controller
public function store(Request $request): JsonResponse
{
    if (User::where('email', $request->email)->exists()) { ... }
    $user = User::create($request->all());
}
```

### 5.2 Service 職責

| 允許 | 禁止 |
|-----|------|
| 業務邏輯、交易管理、快取策略 | 直接 Model 操作、HTTP 回應格式化 |

```php
// ✅ 正確：透過 Repository 操作
$this->userRepository->create($data);

// ❌ 錯誤：直接使用 Model
User::create($data);
```

### 5.3 介面優先原則

- Service 必須定義 `I{Domain}Service` 介面。
- Repository 必須定義 `I{Domain}Repository` 介面。
- 依賴透過介面注入，不直接實例化。

```php
// ✅ 正確
public function __construct(
    private IUserRepository $userRepository,
    private IWalletService $walletService,
) {}

// ❌ 錯誤
$this->userRepo = new UserRepository();
```

---

## 6. Import 順序規範

```php
// 1. Vendor 核心引用
use Carbon\Carbon;
use Illuminate\Support\Facades\DB;

// 2. Exception 類別
use App\Exceptions\ValidationException;

// 3. 自定義 Class
use App\Enums\OrderStatus;
use App\Models\Order;

// 4. Interface
use App\Contracts\Services\IOrderService;
use App\Contracts\Repositories\IOrderRepository;
```

---

## 7. 快取命名規範

**格式**：`前綴_描述:變數`

```php
// ✅ 正確
"user_profile:123"
"game_list:platform_1:active"

// ❌ 錯誤
"userProfile:123"     // 命名不一致
"data:123"            // 缺乏語意
```

---

## 8. 審查檢查清單

### 命名與格式
- [ ] 變數是否使用 camelCase？
- [ ] 常數是否使用 UPPER_SNAKE_CASE？
- [ ] 介面是否以 `I` 開頭？
- [ ] 陣列是否使用 `[]` 且有多行結尾逗號？

### Validation
- [ ] 驗證規則是否為陣列格式（非字串 `|`）？
- [ ] 是否使用 `Rule::enum()` 驗證 Enum？

### 分層架構
- [ ] Controller 是否只做請求處理與回應？
- [ ] Service 是否透過 Repository 介面操作資料？
- [ ] 依賴是否透過介面注入？

### Enum
- [ ] Enum 是否包含 `getLabel()` 方法？
- [ ] Enum 是否包含 `getOptions()` 方法？
