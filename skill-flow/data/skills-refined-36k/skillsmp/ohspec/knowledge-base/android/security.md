# Android 安全最佳实践

## 概述
本文档总结 Android 平台在安全性方面的核心机制和最佳实践。

## 核心安全机制

### 1. 权限系统（Permission System）
- **权限类型**：
  - Normal：低风险权限，安装时自动授予
  - Dangerous：高风险权限，运行时请求
  - Signature：仅相同签名应用可获得
  - SpecialAccess：特殊权限，需要用户在设置中授予
- **运行时权限**：
  - 使用 `ActivityCompat.requestPermissions()` 请求权限
  - 处理权限拒绝和"不再询问"情况
  - 说明权限使用理由（`shouldShowRequestPermissionRationale()`）

### 2. 数据保护（Data Protection）
- **敏感数据存储**：
  - 使用 `EncryptedSharedPreferences` 加密偏好设置
  - 使用 `EncryptedFile` 加密文件
  - 密钥存储在 Android Keystore
- **网络传输**：
  - 强制使用 HTTPS
  - 实施证书固定（Certificate Pinning）
  - 使用 Network Security Config

### 3. 输入验证（Input Validation）
- **防注入攻击**：
  - 参数化查询防止 SQL 注入
  - 验证和清理用户输入
  - 使用 Content Provider 的权限控制
- **Intent 安全**：
  - 验证 Intent 数据
  - 使用显式 Intent 启动组件
  - 对敏感操作验证调用者身份

### 4. 组件安全（Component Security）
- **组件导出控制**：
  - 默认 `exported=false`
  - 必要时使用权限保护
- **深度链接验证**：
  - 验证 App Links
  - 防止 URL 劫持

### 5. 代码混淆（Code Obfuscation）
- **ProGuard/R8**：
  - 启用代码混淆和优化
  - 保护关键逻辑不被反编译
  - 正确配置混淆规则

## 安全最佳实践

### 认证和授权
- 使用 BiometricPrompt API 实现生物识别认证
- 实施多因素认证（MFA）
- 使用 AccountManager 管理用户账户

### 日志安全
- 生产环境禁用敏感日志
- 使用 `BuildConfig.DEBUG` 条件编译
- 避免在日志中输出密码、Token 等敏感信息

### WebView 安全
- 禁用不必要的功能（如 JavaScript、文件访问）
- 验证 JavaScript 接口的调用者
- 使用 Safe Browsing API

## 安全审计工具
- **Lint**：静态代码分析，检测潜在安全问题
- **SafetyNet**：设备完整性验证
- **App Security Improvement Program**：Google Play 安全扫描

## 参考资源
- Android Security: https://developer.android.com/topic/security
- OWASP Mobile Security: https://owasp.org/www-project-mobile-security/
