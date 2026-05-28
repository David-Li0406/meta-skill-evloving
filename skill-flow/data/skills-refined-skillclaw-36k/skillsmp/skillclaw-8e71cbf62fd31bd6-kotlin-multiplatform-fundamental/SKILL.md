---
name: kotlin-multiplatform-fundamentals
description: Use this skill when setting up a Kotlin Multiplatform project, including project structure, expect/actual patterns, source sets, and platform-specific code.
---

# Kotlin Multiplatform (KMP) Fundamentals

Kotlin Multiplatform enables sharing code across Android, iOS, Desktop, Web (WASM), and Server.

## Project Structure

### Multi-Module Architecture (Feature-based + api/impl)

```
your-project-admin/
├── build.gradle.kts              # Root build config
├── settings.gradle.kts           # Module includes
├── gradle/libs.versions.toml     # Version catalog
│
├── core/
│   ├── common/                   # Utilities, Result types, extensions
│   │   └── src/commonMain/kotlin/
│   ├── data/                     # Data abstractions, DataStore
│   │   ├── src/commonMain/kotlin/
│   │   ├── src/androidMain/kotlin/
│   │   └── src/iosMain/kotlin/
│   ├── database/                 # Room (Android/iOS/JVM only)
│   │   └── src/commonMain/kotlin/
│   ├── network/                  # Ktor client
│   │   └── src/commonMain/kotlin/
│   └── ui/                       # Design system, theme
│       └── src/commonMain/kotlin/
│
├── feature/
│   ├── auth/
│   │   ├── api/                  # Public interfaces, models
│   │   │   └── src/commonMain/kotlin/
│   │   └── impl/                 # Implementation, UI
│   │       └── src/commonMain/kotlin/
│   └── home/
│       ├── api/
│       └── impl/
│
├── composeApp/                   # Platform entry points
│   ├── src/commonMain/           # App composition, DI graph
│   ├── src/androidMain/          # MainActivity
│   ├── src/iosMain/              # iOS entry
│   ├── src/jvmMain/              # Desktop main()
│   └── src/wasmJsMain/           # Web entry
│
└── iosApp/                       # Xcode project
```

### Source Sets Hierarchy

```
commonMain
├── androidMain
├── iosMain
│   ├── iosX64Main
│   ├── iosArm64Main
│   └── iosSimulatorArm64Main
├── jvmMain
├── wasmJsMain
└── jsMain (fallback)
```

## Gradle Setup

### Root build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.composeMultiplatform) apply false
    alias(libs.plugins.composeCompiler) apply false
    alias(libs.plugins.kotlinSerialization) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.room) apply false
    alias(libs.plugins.metro) apply false
}
```

### settings.gradle.kts

```
```