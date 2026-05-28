# Gradle Task Configuration

## Task Types

```kotlin
// Copy task
tasks.register<Copy>("copyResources") {
    from("src/main/resources")
    into(layout.buildDirectory.dir("resources"))
    include("**/*.properties")
    exclude("**/test-*")
}

// Exec task
tasks.register<Exec>("runScript") {
    commandLine("bash", "-c", "echo Hello")
    workingDir = projectDir
}

// Delete task
tasks.register<Delete>("cleanGenerated") {
    delete(layout.buildDirectory.dir("generated"))
}

// Zip task
tasks.register<Zip>("createDist") {
    from(layout.buildDirectory.dir("libs"))
    archiveFileName.set("dist-${project.version}.zip")
    destinationDirectory.set(layout.buildDirectory.dir("distributions"))
}
```

## Task Dependencies

```kotlin
tasks.register("prepare") {
    doLast { println("Preparing...") }
}

tasks.register("build") {
    dependsOn("prepare")
    doLast { println("Building...") }
}

tasks.register("deploy") {
    mustRunAfter("build")
    doLast { println("Deploying...") }
}

// Finalized by
tasks.named("build") {
    finalizedBy("report")
}
```

## Lazy Configuration

```kotlin
// Lazy property
val outputDir = objects.directoryProperty()
outputDir.set(layout.buildDirectory.dir("output"))

tasks.register<Copy>("copyOutput") {
    from(tasks.named("compile"))
    into(outputDir)
}

// Provider API
val jarFile = tasks.named<Jar>("jar").flatMap { it.archiveFile }

tasks.register("printJar") {
    doLast {
        println("JAR: ${jarFile.get().asFile}")
    }
}
```

## Task Avoidance

```kotlin
// DON'T - eagerly creates task
tasks.create("eagerTask") { }

// DO - lazily creates task
tasks.register("lazyTask") { }

// Configure existing task lazily
tasks.named<Test>("test") {
    useJUnitPlatform()
    maxParallelForks = Runtime.getRuntime().availableProcessors()
}
```

## Build Cache

```kotlin
// Enable in gradle.properties
// org.gradle.caching=true

tasks.register("cachedTask") {
    inputs.files("src/main/resources")
    outputs.dir(layout.buildDirectory.dir("cached"))
    
    outputs.cacheIf { true }
    
    doLast {
        // Task action
    }
}
```

## Common Commands

```bash
# List tasks
./gradlew tasks

# Run with info
./gradlew build --info

# Skip tests
./gradlew build -x test

# Parallel execution
./gradlew build --parallel

# Refresh dependencies
./gradlew build --refresh-dependencies

# Build scan
./gradlew build --scan
```
