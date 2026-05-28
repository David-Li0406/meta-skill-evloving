---
name: compose-multiplatform
description: Use this skill when you need to create shared UI components and resources for Android, iOS, Desktop, and Web applications using a declarative UI framework.
---

# Compose Multiplatform

Declarative UI framework for Android, iOS, Desktop, and Web with shared code.

## Setup

### build.gradle.kts (Compose module)

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()
    jvm("desktop")

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs { browser() }

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.components.resources)
            implementation(compose.components.uiToolingPreview)
        }

        androidMain.dependencies {
            implementation(compose.uiTooling)
            implementation(libs.androidx.activity.compose)
        }

        val desktopMain by getting {
            dependencies {
                implementation(compose.desktop.currentOs)
            }
        }
    }
}

compose.resources {
    publicResClass = true
    packageOfResClass = "com.your-project.admin.resources"
    generateResClass = auto
}
```

## Resources

### Directory Structure

```
src/commonMain/composeResources/
├── drawable/              # Images (PNG, WebP, SVG)
│   ├── ic_logo.xml       # Vector drawable
│   └── bg_pattern.png
├── drawable-dark/         # Dark theme variants
├── font/                  # TTF/OTF fonts
│   ├── Inter-Regular.ttf
│   └── Inter-Bold.ttf
├── values/
│   └── strings.xml        # Default strings
├── values-ru/
│   └── strings.xml        # Russian strings
└── files/                 # Raw files
    └── config.json
```

### strings.xml Format

```xml
<!-- values/strings.xml -->
<resources>
    <string name="app_name">My Application</string>
    <string name="welcome_message">Welcome, %1$s!</string>
    <string name="items_count">%1$d items</string>
</resources>

<!-- values-ru/strings.xml -->
<resources>
    <string name="app_name">Мое Приложение</string>
    <string name="welcome_message">Добро пожаловать, %1$s!</string>
    <string name="items_count">%1$d элементов</string>
</resources>
```

### Using Resources

```kotlin
import com.your-project.admin.resources.Res
```