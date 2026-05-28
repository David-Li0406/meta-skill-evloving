---
name: "security-auditor"
description: "Activates when user requests security review, penetration test analysis, sensitive data handling, authentication/authorization design, or OWASP risk assessment. Do NOT use for general code style reviews. Examples: 'Check for SQL injection', 'Review authentication flow'."
---

# Security Auditor Skill

## 🧠 Expertise

資深資安專家，專精於應用程式安全、滲透測試與安全架構設計，熟悉 OWASP Top 10 與企業級安全規範。

---

## 1. OWASP Top 10 風險檢查

### A01:2021 – Broken Access Control（存取控制失效）

**檢查要點**：
- 是否有水平/垂直越權風險
- 是否遵循最小權限原則
- API 端點是否有適當的權限驗證

**紅旗標誌**：
- ❌ 僅依賴前端隱藏功能來控制存取
- ❌ 缺少資源所有權驗證（IDOR 風險）
- ❌ CORS 配置過於寬鬆

---

### A02:2021 – Cryptographic Failures（加密機制失效）

**檢查要點**：
- 敏感資料是否加密傳輸（TLS）
- 密碼是否使用強雜湊演算法（bcrypt、Argon2）
- 加密金鑰是否安全儲存

**紅旗標誌**：
- ❌ 使用 MD5/SHA1 進行密碼雜湊
- ❌ 硬編碼加密金鑰
- ❌ 未使用 HTTPS

---

### A03:2021 – Injection（注入攻擊）

**檢查要點**：
- SQL 查詢是否參數化
- 是否過濾/跳脫用戶輸入
- 命令執行是否安全

**紅旗標誌**：
- ❌ SQL 字串拼接：`"SELECT * FROM users WHERE id = " + id`
- ❌ 直接執行用戶輸入的命令
- ❌ 未驗證的動態查詢建構

**最佳實務**：
```php
// ❌ Bad
$query = "SELECT * FROM users WHERE id = " . $id;

// ✅ Good (Eloquent)
User::where('id', $id)->first();

// ✅ Good (Query Builder)
DB::table('users')->where('id', $id)->first();
```

---

### A04:2021 – Insecure Design（不安全設計）

**檢查要點**：
- 是否有威脅建模
- 是否考慮失敗情境
- 業務邏輯是否有濫用風險

**紅旗標誌**：
- ❌ 無速率限制
- ❌ 缺少業務邏輯驗證
- ❌ 過度信任客戶端輸入

---

### A05:2021 – Security Misconfiguration（安全配置錯誤）

**檢查要點**：
- 預設配置是否安全
- 是否禁用不必要的功能
- 錯誤訊息是否過於詳細

**紅旗標誌**：
- ❌ 生產環境開啟 Debug 模式
- ❌ 預設密碼/帳號未更改
- ❌ 不必要的 HTTP 方法啟用

---

### A06:2021 – Vulnerable Components（易受攻擊的元件）

**檢查要點**：
- 相依套件是否有已知漏洞
- 是否定期更新相依

**建議工具**：
- `npm audit` / `composer audit`
- Snyk、Dependabot

---

### A07:2021 – Authentication Failures（身份驗證失效）

**檢查要點**：
- 密碼政策是否足夠強
- 是否有帳號鎖定機制
- Session 管理是否安全

**紅旗標誌**：
- ❌ 允許弱密碼
- ❌ 無登入失敗次數限制
- ❌ Session ID 可預測

---

### A08:2021 – Data Integrity Failures（資料完整性失效）

**檢查要點**：
- 是否驗證資料來源
- 是否使用數位簽章

**紅旗標誌**：
- ❌ 反序列化不受信任的資料
- ❌ 未驗證下載檔案完整性

---

### A09:2021 – Logging Failures（日誌記錄失效）

**檢查要點**：
- 是否記錄安全相關事件
- 日誌是否包含敏感資訊

**紅旗標誌**：
- ❌ 未記錄登入失敗
- ❌ 日誌中包含密碼/Token
- ❌ 日誌可被竄改

---

### A10:2021 – SSRF（伺服器端請求偽造）

**檢查要點**：
- 是否驗證外部 URL
- 是否限制可存取的協定/IP

**紅旗標誌**：
- ❌ 允許用戶指定任意 URL
- ❌ 可存取內部網路資源

---

## 2. 輸入驗證規範

### 驗證原則
1. **白名單優於黑名單**：定義允許的輸入，而非禁止的輸入
2. **後端驗證必須**：前端驗證僅為 UX，不可作為安全依賴
3. **型別強制**：使用強型別語言特性

### 常見驗證項目

| 輸入類型 | 驗證規則 |
|---------|---------|
| Email | 格式驗證 + 長度限制 |
| ID/Key | 格式驗證（UUID/數字）+ 存在性驗證 |
| 文字輸入 | 長度限制 + HTML 跳脫 |
| 檔案上傳 | MIME 類型 + 大小限制 + 副檔名驗證 |
| URL | 協定白名單 + 域名驗證 |

---

## 3. 敏感資料處理

### 敏感資料分類

| 等級 | 資料類型 | 處理要求 |
|-----|---------|---------|
| **極高** | 密碼、API Key、加密金鑰 | 絕不明文儲存、傳輸加密、存取記錄 |
| **高** | PII（姓名、身分證、Email） | 加密儲存、最小化收集、存取控制 |
| **中** | 業務資料 | 傳輸加密、權限控制 |

### 處理規範

**密碼處理**：
```php
// ✅ Correct
Hash::make($password);  // Laravel 預設使用 bcrypt

// ❌ Wrong
md5($password);
sha1($password);
```

**日誌脫敏**：
```php
// ❌ Wrong
Log::info('User login', ['password' => $password]);

// ✅ Correct
Log::info('User login', ['user_id' => $user->id]);
```

**API 回應脫敏**：
- Response 中不應包含密碼、Token、內部 ID
- 使用 Resource/Transformer 控制輸出欄位

---

## 4. 認證授權最佳實務

### 認證（Authentication）

| 項目 | 建議 |
|-----|-----|
| 密碼政策 | 最少 8 字元、包含大小寫數字 |
| 雜湊演算法 | bcrypt、Argon2 |
| Session 過期 | 閒置 30 分鐘、絕對 24 小時 |
| MFA | 高風險操作強制啟用 |

### 授權（Authorization）

| 項目 | 建議 |
|-----|-----|
| 原則 | 最小權限原則（Least Privilege） |
| 實作 | RBAC / ABAC |
| 驗證位置 | Controller 層 + Service 層雙重檢查 |
| 資源所有權 | 每次操作驗證資源歸屬 |

---

## 5. 審查評分標準

| 嚴重度 | 定義 | 範例 |
|-------|------|------|
| **嚴重** | 可直接導致資料洩漏或系統被入侵 | SQL Injection、硬編碼密碼 |
| **高** | 可繞過安全機制 | 越權存取、Session 固定 |
| **中** | 增加攻擊面 | XSS、不安全配置 |
| **低** | 安全最佳實務偏離 | 日誌不完整、缺少 CSP |
