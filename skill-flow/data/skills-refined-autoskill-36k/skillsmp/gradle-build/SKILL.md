---
name: Gradle Build
description: Kotlin DSL, dependencies, tasks, plugins, and multi-project builds.
metadata:
  labels: [java, gradle, build]
  triggers:
    files: ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts']
    keywords: [dependencies, plugins, tasks, implementation, testImplementation, kotlin]
---

# Gradle Build Standards

## Kotlin DSL Structure

```kotlin
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "1.0.0-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.test {
    useJUnitPlatform()
}
```

## Dependency Configurations

```kotlin
dependencies {
    implementation("...")       // Compile + runtime, not exposed
    api("...")                  // Compile + runtime, exposed to consumers
    compileOnly("...")          // Compile only (like Lombok)
    runtimeOnly("...")          // Runtime only (JDBC drivers)
    testImplementation("...")   // Test compile + runtime
    annotationProcessor("...")  // Annotation processing
}
```

## Custom Tasks

```kotlin
tasks.register("hello") {
    group = "custom"
    description = "Prints hello"
    doLast {
        println("Hello, Gradle!")
    }
}

tasks.register<Copy>("copyResources") {
    from("src/main/resources")
    into("build/resources")
}
```

## Common Commands

```bash
./gradlew build          # Build project
./gradlew test           # Run tests
./gradlew bootRun        # Run Spring Boot
./gradlew dependencies   # Show dependencies
./gradlew tasks          # List tasks
```

## References

- [Kotlin DSL](references/kotlin-dsl.md) - Migration from Groovy, type-safe configuration
