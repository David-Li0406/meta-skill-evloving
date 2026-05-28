# iOS/macOS 安全最佳实践

## 概述
本文档总结 Apple 平台在安全性方面的核心机制和最佳实践。

## 核心安全机制

### 1. 数据保护（Data Protection）
- **文件保护**：
  - 使用 Data Protection API
  - 保护级别：Complete、CompleteUnlessOpen、CompleteUntilFirstUserAuthentication、None
  - 敏感文件使用 `Complete` 级别
- **Keychain**：
  - 存储密码、证书、密钥
  - 支持 Touch ID/Face ID 保护
  - 使用 `kSecAttrAccessible` 控制访问时机

### 2. 网络安全（Network Security）
- **App Transport Security (ATS)**：
  - 默认强制 HTTPS
  - 使用 TLS 1.2+ 和强加密套件
  - 避免禁用 ATS（除非必要）
- **Certificate Pinning**：
  - 固定服务器证书或公钥
  - 防止中间人攻击
  - 使用 `URLSessionDelegate` 实现

### 3. 身份认证（Authentication）
- **LocalAuthentication Framework**：
  - 支持 Touch ID、Face ID、密码
  - 使用 `LAContext` 进行生物识别
- **AuthenticationServices**：
  - Sign in with Apple
  - 自动强密码和密码管理
  - Web 认证（WebAuthn）

### 4. 代码签名和沙箱（Code Signing & Sandboxing）
- **代码签名**：
  - 确保代码完整性
  - 防止代码篡改
  - 使用 Entitlements 声明权限
- **沙箱（macOS）**：
  - 限制应用访问资源
  - 使用 Entitlements 请求权限
  - 遵循最小权限原则

### 5. 隐私保护（Privacy）
- **权限请求**：
  - Info.plist 中说明使用理由
  - 运行时请求权限
  - 处理权限拒绝情况
- **隐私敏感数据**：
  - 照片、联系人、位置、麦克风、相机等
  - 透明说明数据使用方式
  - 提供隐私政策

## 安全最佳实践

### 安全编码
```swift
// 使用 Keychain 存储敏感数据
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "user@example.com",
    kSecValueData as String: passwordData,
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked
]
SecItemAdd(query as CFDictionary, nil)

// 使用生物识别
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
                       localizedReason: "解锁应用") { success, error in
    if success {
        // 认证成功
    }
}
```

### 输入验证
- 验证所有外部输入
- 使用参数化查询防止注入
- 对 URL Scheme 输入进行验证

### 安全通信
```swift
// Certificate Pinning 示例
func urlSession(_ session: URLSession,
                didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    if let trust = challenge.protectionSpace.serverTrust,
       SecTrustGetCertificateCount(trust) > 0 {
        // 验证证书
        if let certificate = SecTrustGetCertificateAtIndex(trust, 0) {
            let data = SecCertificateCopyData(certificate) as Data
            if data == pinnedCertData {
                completionHandler(.useCredential, URLCredential(trust: trust))
                return
            }
        }
    }
    completionHandler(.cancelAuthenticationChallenge, nil)
}
```

### 日志安全
- 避免在日志中输出敏感信息
- 使用 `os_log` 进行结构化日志记录
- 生产环境禁用调试日志

## 安全审计工具
- **Static Analyzer**：Xcode 内置静态分析
- **Address Sanitizer**：内存安全检测
- **Thread Sanitizer**：并发问题检测
- **App Review**：提交前安全审查

## 参考资源
- Security: https://developer.apple.com/security/
- Secure Coding Guide: https://developer.apple.com/library/archive/documentation/Security/Conceptual/SecureCodingGuide/
- App Privacy Details: https://developer.apple.com/app-store/app-privacy-details/
