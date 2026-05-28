# Kotlin

**Category**: languages
**Description**: Kotlin programming language - modern, concise language for JVM, Android, and multiplatform development
**Homepage**: https://kotlinlang.org

## Package Detection

### MAVEN
- `org.jetbrains.kotlin:kotlin-stdlib`
- `org.jetbrains.kotlin:kotlin-stdlib-jdk8`
- `org.jetbrains.kotlin:kotlin-reflect`

### GRADLE
- `org.jetbrains.kotlin:kotlin-gradle-plugin`
- `org.jetbrains.kotlin.jvm`
- `org.jetbrains.kotlin.android`
- `org.jetbrains.kotlin.multiplatform`

## Configuration Files

- `build.gradle.kts`
- `settings.gradle.kts`
- `gradle.properties`
- `kotlin-js-store/`
- `.kotlin/`

## File Extensions

- `.kt`
- `.kts` (Kotlin script)

## Import Detection

### Kotlin
**Pattern**: `^package\s+[\w.]+`
- Package declaration
- Example: `package com.example.app`

**Pattern**: `^import\s+[\w.]+`
- Import statement
- Example: `import kotlinx.coroutines.flow.Flow`

**Pattern**: `^(data\s+)?class\s+\w+`
- Class declaration
- Example: `data class User(val name: String)`

**Pattern**: `^fun\s+\w+\(`
- Function declaration
- Example: `fun main(args: Array<String>) {}`

**Pattern**: `suspend\s+fun`
- Suspend function
- Example: `suspend fun fetchUser(): User {}`

## Environment Variables

- `KOTLIN_HOME`
- `KOTLIN_VERSION`

## Version Indicators

- Kotlin 1.9+ (current)
- Kotlin 1.8 (stable)

## Detection Notes

- Look for `.kt` files in repository
- build.gradle.kts indicates Kotlin DSL
- Check for kotlin {} block in build files
- Often used alongside Java in same project
- Android projects commonly use Kotlin

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **build.gradle.kts Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
