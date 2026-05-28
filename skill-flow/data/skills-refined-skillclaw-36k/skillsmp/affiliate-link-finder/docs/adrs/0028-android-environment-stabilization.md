# ADR 0028: Android Environment Stabilization

## Status
Accepted

## Context
Android builds were experiencing obsolete Java 8 warnings and runtime GMS (Google Play Services) `SecurityException` errors. The warnings caused build clutter and future compatibility risks, while the GMS errors blocked Firebase connectivity on Android 11+ emulators during development.

## Decision
We implemented several stabilization measures for the Android environment:

1.  **JVMT 17 Enforcement**: Enforced `JvmTarget.JVM_17` and `sourceCompatibility`/`targetCompatibility` to Java 17 across all subprojects (plugins) in `build.gradle.kts`.
2.  **Warning Suppression**: Added `-Xlint:-options` to `JavaCompile` tasks to suppress warnings about obsolete JVM versions from third-party libraries.
3.  **GMS Package Visibility**: Added `<queries>` for `com.google.android.gms` in `AndroidManifest.xml` to comply with Android 11+ package visibility requirements.
4.  **Plugin & Gradle Alignment**: Downgraded `google-services` to `4.3.15` and enabled `Jetifier` to ensure compatibility with modern Android Gradle Plugin (AGP) versions used in the project.

## Consequences
- **Positive**: Clean, warning-free builds; reliable Firebase connectivity on modern Android emulators.
- **Negative**: Adds configuration complexity to the root `build.gradle.kts`.
