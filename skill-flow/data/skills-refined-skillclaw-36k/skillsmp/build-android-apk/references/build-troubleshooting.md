# APK 构建常见问题排查

## 环境问题

| 问题 | 解决方案 |
|------|----------|
| `JAVA_HOME is not set` | `export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home` |
| `Android SDK not found` | `export ANDROID_HOME=$HOME/Library/Android/sdk` |
| `Build tools not found` | Android Studio → SDK Manager → 安装 Build-Tools 34.0.0+ |

## Gradle 构建问题

| 问题 | 解决方案 |
|------|----------|
| `Could not resolve all files` | `./gradlew clean && ./gradlew --refresh-dependencies` |
| `mergeReleaseResources failed` | 清理: `./gradlew clean && rm -rf ~/.gradle/caches/` |
| `Out of memory: Java heap` | `gradle.properties` 添加: `org.gradle.jvmargs=-Xmx4096m` |

## 签名问题

| 问题 | 解决方案 |
|------|----------|
| `Keystore password incorrect` | 确认密码正确，或重新生成 keystore |
| `No key with alias found` | `keytool -list -keystore release.keystore` 查看别名 |

## Expo 相关问题

| 问题 | 解决方案 |
|------|----------|
| `expo-modules-autolinking failed` | `rm -rf node_modules android && npm install && npx expo prebuild --clean` |
| `Duplicate class found` | `npm dedupe && npx expo doctor` |

## 完全重置构建

```bash
cd frontend/CretasFoodTrace
rm -rf node_modules android .expo
npm install
npx expo prebuild --clean --platform android
cd android && ./gradlew clean && ./gradlew assembleRelease
```

## Gradle 性能配置

`android/gradle.properties`:
```properties
org.gradle.daemon=true
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.jvmargs=-Xmx4096m
```

## 快速检查清单

- [ ] Java 17+ (`java -version`)
- [ ] Android SDK 配置 (`echo $ANDROID_HOME`)
- [ ] node_modules 完整 (`npm install`)
- [ ] android 目录存在 (`npx expo prebuild`)
- [ ] Gradle 缓存清理 (`./gradlew clean`)
- [ ] 签名配置正确
