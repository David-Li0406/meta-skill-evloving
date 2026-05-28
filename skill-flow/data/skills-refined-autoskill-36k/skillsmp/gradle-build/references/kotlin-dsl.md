# Gradle Kotlin DSL

## Basic Build Script

```kotlin
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    
    runtimeOnly("org.postgresql:postgresql")
    
    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")
    
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}
```

## Version Catalogs

```toml
# gradle/libs.versions.toml
[versions]
spring-boot = "3.2.0"
lombok = "1.18.30"
junit = "5.10.0"

[libraries]
spring-boot-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
lombok = { module = "org.projectlombok:lombok", version.ref = "lombok" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

```kotlin
// build.gradle.kts
plugins {
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(libs.spring.boot.web)
    implementation(libs.spring.boot.jpa)
    compileOnly(libs.lombok)
    testImplementation(libs.junit.jupiter)
}
```

## Custom Tasks

```kotlin
tasks.register<Copy>("copyDocs") {
    from("docs")
    into(layout.buildDirectory.dir("documentation"))
}

tasks.named("build") {
    dependsOn("copyDocs")
}

// Task with typed configuration
tasks.register<Jar>("sourcesJar") {
    archiveClassifier.set("sources")
    from(sourceSets.main.get().allSource)
}
```

## Multi-Project Builds

```kotlin
// settings.gradle.kts
rootProject.name = "my-project"
include("core", "api", "web")

// root build.gradle.kts
subprojects {
    apply(plugin = "java")
    
    repositories {
        mavenCentral()
    }
    
    dependencies {
        testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    }
}

// api/build.gradle.kts
dependencies {
    implementation(project(":core"))
}
```
