---
name: security-audit
description: 協助執行 PHP/Laravel 應用程式的安全性審計。當需要檢查安全漏洞、審查敏感資料處理、或評估 OWASP Top 10 風險時載入此技能。
---

# 安全性審計技能

本技能提供 PHP/Laravel 應用程式的安全性檢查指引，聚焦於 OWASP Top 10 與常見漏洞模式。

## 嚴重漏洞檢查

### SQL Injection (SQL 注入)

**嚴重程度**: 🔴 嚴重

**檢測模式**:
```php
// ❌ 危險 - 字串拼接
$query = "SELECT * FROM users WHERE id = " . $id;
DB::select("SELECT * FROM users WHERE name = '$name'");

// ✅ 安全 - 參數化查詢
User::where('id', $id)->first();
DB::select("SELECT * FROM users WHERE name = ?", [$name]);
```

**檢查要點**:
- 是否有原生 SQL 字串拼接
- 是否使用 `DB::raw()` 處理使用者輸入
- `whereRaw()` 是否有參數綁定

---

### XSS (跨站腳本攻擊)

**嚴重程度**: 🔴 嚴重

**檢測模式**:
```php
// ❌ 危險 - 直接輸出
{!! $userInput !!}
echo $request->input('name');

// ✅ 安全 - 自動跳脫
{{ $userInput }}
e($request->input('name'));
```

**檢查要點**:
- Blade 模板中是否使用 `{!! !!}` 輸出使用者輸入
- 是否有 `echo` 直接輸出未消毒的資料
- JavaScript 中是否嵌入未編碼的資料

---

### 硬編碼秘密 (Hardcoded Secrets)

**嚴重程度**: 🔴 嚴重

**檢測模式**:
```php
// ❌ 危險 - 硬編碼
$apiKey = "sk-1234567890abcdef";
$password = "admin123";

// ✅ 安全 - 環境變數
$apiKey = config('services.api.key');
$password = env('DB_PASSWORD');
```

**檢查要點**:
- 程式碼中是否包含 API 金鑰、密碼、Token
- 設定檔是否有敏感資料（應使用 `.env`）
- Git 歷史中是否曾經提交過秘密

---

### 認證與授權漏洞

**嚴重程度**: 🟡 高

**檢查要點**:
- 是否驗證當前使用者有權存取資源
- 是否有 IDOR (Insecure Direct Object Reference)
- 是否遵循最小權限原則
- Session 管理是否安全

```php
// ❌ 危險 - IDOR
public function show($id) {
    return User::find($id); // 未驗證權限
}

// ✅ 安全 - 權限檢查
public function show($id) {
    $user = User::find($id);
    $this->authorize('view', $user);
    return $user;
}
```

---

### 敏感資料暴露

**嚴重程度**: 🟡 高

**檢查要點**:
- API Response 是否包含不必要的敏感欄位
- Log 是否記錄密碼、Token、信用卡號
- 錯誤訊息是否暴露系統細節

```php
// ❌ 危險 - 暴露密碼
Log::info('User login', ['password' => $request->password]);

// ✅ 安全 - 遮蔽敏感資料
Log::info('User login', ['user_id' => $user->id]);
```

---

## Mass Assignment 風險

**檢查要點**:
- Model 是否設定 `$fillable` 或 `$guarded`
- 是否使用 `$request->all()` 直接寫入資料庫

```php
// ❌ 危險
User::create($request->all());

// ✅ 安全
User::create($request->only(['name', 'email']));
```

---

## 檔案上傳安全

**檢查要點**:
- 是否驗證檔案類型（MIME type）
- 是否限制檔案大小
- 是否使用隨機檔名儲存
- 上傳目錄是否在 webroot 外

---

## 輸出格式

對每個安全檢查提供：

| 類型 | 嚴重程度 | 檔案:行號 | 問題描述 | 修復建議 |
|------|---------|----------|---------|---------|
| SQL Injection | 🔴 嚴重 | path:123 | 描述 | 建議 |
