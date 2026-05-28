# Android APK 签名配置指南

## 1. 生成签名密钥

```bash
keytool -genkey -v \
  -keystore cretas-release.keystore \
  -alias cretas \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

## 2. Gradle 签名配置

创建 `android/gradle.properties` (不要提交到 Git):

```properties
MYAPP_UPLOAD_STORE_FILE=cretas-release.keystore
MYAPP_UPLOAD_KEY_ALIAS=cretas
MYAPP_UPLOAD_STORE_PASSWORD=your_store_password
MYAPP_UPLOAD_KEY_PASSWORD=your_key_password
```

在 `android/app/build.gradle` 中:

```gradle
android {
    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {
                storeFile file(MYAPP_UPLOAD_STORE_FILE)
                storePassword MYAPP_UPLOAD_STORE_PASSWORD
                keyAlias MYAPP_UPLOAD_KEY_ALIAS
                keyPassword MYAPP_UPLOAD_KEY_PASSWORD
            }
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

## 3. Git 忽略

```gitignore
*.keystore
*.jks
android/gradle.properties
```

## 4. 验证签名

```bash
# 查看密钥库
keytool -list -keystore cretas-release.keystore

# 验证 APK 签名
$ANDROID_HOME/build-tools/34.0.0/apksigner verify --verbose app-release.apk

# 查看 APK 证书
keytool -printcert -jarfile app-release.apk
```

## 常见问题

| 问题 | 答案 |
|------|------|
| 忘记密码 | 无法恢复，需新密钥重新发布 |
| 更换密钥 | Play Store 用 App Signing 升级，否则需发布新应用 |
| 调试/发布同密钥 | 不建议，调试用 debug.keystore |

## 发布检查清单

- [ ] 签名密钥已备份
- [ ] gradle.properties 已配置
- [ ] .gitignore 包含密钥文件
- [ ] APK 签名已验证
- [ ] 版本号已更新
