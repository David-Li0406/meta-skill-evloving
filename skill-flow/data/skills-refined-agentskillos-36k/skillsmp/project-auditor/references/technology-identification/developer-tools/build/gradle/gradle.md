# Gradle

**Category**: developer-tools/build
**Description**: Gradle - build automation tool for multi-language software development
**Homepage**: https://gradle.org

## Package Detection

### Maven Central
- `org.gradle:gradle-core`
- `org.gradle:gradle-tooling-api`

## Configuration Files

- `build.gradle`
- `build.gradle.kts`
- `settings.gradle`
- `settings.gradle.kts`
- `gradle.properties`
- `gradle-wrapper.properties`
- `gradlew`
- `gradlew.bat`

## Environment Variables

- `GRADLE_HOME`
- `GRADLE_USER_HOME`
- `GRADLE_OPTS`

## Detection Notes

- Standard build tool for Java/Kotlin/Android projects
- Look for build.gradle or build.gradle.kts in repository root
- Gradle wrapper (gradlew) indicates project uses specific Gradle version
- Often found in multi-module projects with subproject build files

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
