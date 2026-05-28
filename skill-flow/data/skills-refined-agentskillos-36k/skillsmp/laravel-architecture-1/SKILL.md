---
name: laravel-architecture
description: 協助遵循 Laravel 多層架構規範。當需要設計新功能、重構程式碼、或審查架構時載入此技能。適用於 Controller、Service、Repository 分層設計。
---

# Laravel 多層架構技能

本技能提供 Laravel 專案的多層架構設計指引，確保程式碼職責分離與可維護性。

## 架構分層

```
┌─────────────────────────────────────────┐
│              Controller                  │  ← 只處理 HTTP Request/Response
├─────────────────────────────────────────┤
│              FormRequest                 │  ← 只處理格式驗證
├─────────────────────────────────────────┤
│               Service                    │  ← 所有業務邏輯在此
├─────────────────────────────────────────┤
│              Repository                  │  ← 只處理資料存取
├─────────────────────────────────────────┤
│                Model                     │  ← 資料結構與關聯定義
└─────────────────────────────────────────┘
```

---

## Controller 規範

**職責**: Request → Service → Response

**允許**:
- 接收 HTTP Request
- 呼叫 Service
- 回傳 Response

**禁止**:
- ❌ 業務邏輯
- ❌ 狀態判斷
- ❌ 直接呼叫 Repository 或 Model

```php
// ✅ 正確
class UserController
{
    public function store(StoreUserRequest $request, IUserService $service)
    {
        $user = $service->createUser($request->validated());
        return response()->json($user, 201);
    }
}

// ❌ 錯誤 - 業務邏輯不應在 Controller
class UserController
{
    public function store(Request $request)
    {
        if (User::where('email', $request->email)->exists()) {
            throw new Exception('Email exists');
        }
        $user = User::create($request->all());
        Mail::send(...); // 不應在此
        return response()->json($user);
    }
}
```

---

## FormRequest 規範

**職責**: 格式與型別驗證

**允許**:
- 格式驗證 (required, string, max, email...)
- 型別檢查

**禁止**:
- ❌ `exists`、`unique` 等 DB 查詢規則（應在 Service 驗證）
- ❌ 任何業務判斷

```php
// ✅ 正確
class StoreUserRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:100'],
            'email' => ['required', 'email'],
            'age' => ['required', 'integer', 'min:0'],
        ];
    }
}

// ❌ 錯誤 - DB 查詢應在 Service
class StoreUserRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'email' => ['required', 'unique:users,email'], // ❌
        ];
    }
}
```

---

## Service 規範

**職責**: 所有業務邏輯

**必須**:
- ✅ 所有業務規則、狀態檢核
- ✅ 透過 Interface 依賴 Repository（DIP）
- ✅ 資料庫交易管理
- ✅ 驗證失敗拋出具體 Exception

```php
// ✅ 正確
class UserService implements IUserService
{
    public function __construct(
        private readonly IUserRepository $userRepo
    ) {}

    public function createUser(array $data): User
    {
        // 業務規則驗證
        if ($this->userRepo->existsByEmail($data['email'])) {
            throw new EmailExistsException();
        }

        return DB::transaction(function () use ($data) {
            $user = $this->userRepo->create($data);
            // 其他業務邏輯...
            return $user;
        });
    }
}
```

---

## Repository 規範

**職責**: 資料存取 (CRUD)

**允許**:
- 資料的新增、讀取、更新、刪除
- 查詢條件組合

**禁止**:
- ❌ 業務邏輯
- ❌ 狀態判斷

```php
// ✅ 正確
class UserRepository implements IUserRepository
{
    public function existsByEmail(string $email): bool
    {
        return User::where('email', $email)->exists();
    }

    public function create(array $data): User
    {
        return User::create($data);
    }
}
```

---

## 命名規範

| 元件 | 命名規則 | 範例 |
|------|---------|------|
| Controller | `{Entity}Controller` | `UserController` |
| Service | `{Entity}Service` | `UserService` |
| Interface | `I{Entity}{Type}` | `IUserService`, `IUserRepository` |
| Repository | `{Entity}Repository` | `UserRepository` |
| FormRequest | `{Action}{Entity}Request` | `StoreUserRequest` |
| Exception | `{描述}Exception` | `EmailExistsException` |

---

## 依賴注入綁定

```php
// AppServiceProvider
public function register(): void
{
    $this->app->bind(IUserService::class, UserService::class);
    $this->app->bind(IUserRepository::class, UserRepository::class);
}
```

---

## 檔案結構

```
app/
├── Http/
│   ├── Controllers/
│   │   └── UserController.php
│   └── Requests/
│       └── StoreUserRequest.php
├── Services/
│   ├── Interfaces/
│   │   └── IUserService.php
│   └── UserService.php
├── Repositories/
│   ├── Interfaces/
│   │   └── IUserRepository.php
│   └── UserRepository.php
├── Models/
│   └── User.php
└── Exceptions/
    └── EmailExistsException.php
```
