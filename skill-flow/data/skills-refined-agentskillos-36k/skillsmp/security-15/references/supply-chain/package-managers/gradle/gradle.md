# Gradle Package Manager

**Ecosystem**: Java/JVM (also Kotlin, Groovy, Scala)
**Package Registry**: https://repo.maven.apache.org/maven2 (Maven Central)
**Documentation**: https://docs.gradle.org/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `build.gradle` | Yes* | Groovy DSL build script |
| `build.gradle.kts` | Yes* | Kotlin DSL build script |
| `settings.gradle` | No | Multi-project settings |
| `settings.gradle.kts` | No | Kotlin DSL settings |
| `gradle.properties` | No | Build properties |

*One of the build files is required

### build.gradle Detection

**Pattern**: `build\.gradle(\.kts)?$`
**Confidence**: 98% (HIGH)

### Groovy DSL Example

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.1.0'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:3.1.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}
```

### Kotlin DSL Example

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.1.0"
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:3.1.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}
```

### Dependency Configurations

| Configuration | Included in SBOM | Notes |
|---------------|------------------|-------|
| `implementation` | Yes (always) | Compile and runtime |
| `api` | Yes (always) | Exposed to consumers |
| `runtimeOnly` | Yes (always) | Runtime only |
| `compileOnly` | Configurable | Compile-time only |
| `testImplementation` | Configurable | Test dependencies |
| `annotationProcessor` | Configurable | Annotation processing |

---

## TIER 2: Lock File Detection

### Lock Files

| File | Format | Version |
|------|--------|---------|
| `gradle.lockfile` | Text | Gradle 4.8+ |
| `buildscript-gradle.lockfile` | Text | Plugin dependencies |

**Pattern**: `gradle\.lockfile$`
**Confidence**: 98% (HIGH)

### Lock File Structure

```
# This is a Gradle generated file for dependency locking.
# Manual edits can break the build and are not advised.
# This file is expected to be part of source control.
com.fasterxml.jackson.core:jackson-annotations:2.15.2=compileClasspath,runtimeClasspath
com.fasterxml.jackson.core:jackson-core:2.15.2=compileClasspath,runtimeClasspath
com.fasterxml.jackson.core:jackson-databind:2.15.2=compileClasspath,runtimeClasspath
org.springframework.boot:spring-boot:3.1.0=compileClasspath,runtimeClasspath
empty=annotationProcessor
```

### Enabling Dependency Locking

```groovy
// build.gradle
dependencyLocking {
    lockAllConfigurations()
}
```

```kotlin
// build.gradle.kts
dependencyLocking {
    lockAllConfigurations()
}
```

```bash
# Generate lock file
./gradlew dependencies --write-locks

# Update lock file
./gradlew dependencies --update-locks org.springframework:*
```

---

## TIER 3: Configuration Extraction

### Repository Configuration

**File**: `build.gradle` or `build.gradle.kts`

**Pattern (Groovy)**: `url\s+['\"]([^'\"]+)['\"]`
**Pattern (Kotlin)**: `url\s*=\s*uri\(['\"]([^'\"]+)['\"]\)`

### Common Configuration

```groovy
// build.gradle
repositories {
    mavenCentral()

    maven {
        url = "https://nexus.mycompany.com/repository/maven-public/"
        credentials {
            username = System.getenv("MAVEN_USERNAME")
            password = System.getenv("MAVEN_PASSWORD")
        }
    }

    maven {
        url = "https://maven.pkg.github.com/OWNER/REPO"
        credentials {
            username = System.getenv("GITHUB_ACTOR")
            password = System.getenv("GITHUB_TOKEN")
        }
    }
}
```

### gradle.properties

```properties
# gradle.properties
systemProp.http.proxyHost=proxy.mycompany.com
systemProp.http.proxyPort=8080

org.gradle.caching=true
org.gradle.parallel=true

nexusUsername=user
nexusPassword=secret
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `GRADLE_USER_HOME` | Gradle home directory |
| `GRADLE_OPTS` | JVM options |
| `MAVEN_USERNAME` | Repository username |
| `MAVEN_PASSWORD` | Repository password |

---

## SBOM Generation

### Using CycloneDX Gradle Plugin

```groovy
// build.gradle
plugins {
    id 'org.cyclonedx.bom' version '1.8.2'
}

cyclonedxBom {
    includeConfigs = ["runtimeClasspath"]
    skipConfigs = ["testCompileClasspath", "testRuntimeClasspath"]
    projectType = "application"
    schemaVersion = "1.5"
    destination = file("build/reports")
    outputName = "sbom"
    outputFormat = "json"
    includeBomSerialNumber = true
    includeLicenseText = false
    componentVersion = "1.0.0"
}
```

```kotlin
// build.gradle.kts
plugins {
    id("org.cyclonedx.bom") version "1.8.2"
}

tasks.cyclonedxBom {
    setIncludeConfigs(listOf("runtimeClasspath"))
    setSkipConfigs(listOf("testCompileClasspath", "testRuntimeClasspath"))
    setProjectType("application")
    setSchemaVersion("1.5")
    setDestination(project.file("build/reports"))
    setOutputName("sbom")
    setOutputFormat("json")
    setIncludeBomSerialNumber(true)
    setIncludeLicenseText(false)
}
```

```bash
# Generate SBOM
./gradlew cyclonedxBom

# Output: build/reports/sbom.json
```

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type gradle -o sbom.json
```

### Using cdxgen (alternative)

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t java -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `includeConfigs` | Configurations to include | All |
| `skipConfigs` | Configurations to skip | None |
| `projectType` | application or library | application |
| `schemaVersion` | CycloneDX version | 1.5 |
| `outputFormat` | json or xml | json |

---

## Cache Locations

| Location | Path |
|----------|------|
| Gradle User Home | `~/.gradle/` |
| Dependency Cache | `~/.gradle/caches/modules-2/` |
| Build Cache | `~/.gradle/caches/build-cache-1/` |
| Wrapper Cache | `~/.gradle/wrapper/dists/` |

```bash
# Find Gradle user home
echo $GRADLE_USER_HOME || echo ~/.gradle

# Clean caches
./gradlew cleanBuildCache

# Refresh dependencies
./gradlew --refresh-dependencies
```

---

## Best Practices

1. **Enable dependency locking** for reproducible builds
2. **Use Gradle wrapper** (`gradlew`) for consistent Gradle versions
3. **Use version catalogs** (Gradle 7+) for centralized dependency management
4. **Lock configurations** not just dependencies
5. **Generate SBOM in CI/CD** for consistency
6. **Use dependency verification** for integrity

### Version Catalogs (Gradle 7+)

```toml
# gradle/libs.versions.toml
[versions]
spring-boot = "3.1.0"
junit = "5.10.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

```kotlin
// build.gradle.kts
dependencies {
    implementation(libs.spring.boot.starter.web)
    testImplementation(libs.junit.jupiter)
}
```

### Dependency Verification

```bash
# Generate verification metadata
./gradlew --write-verification-metadata sha256 help

# Creates gradle/verification-metadata.xml
```

---

## Troubleshooting

### Dependency Not Found
```bash
# Refresh dependencies
./gradlew --refresh-dependencies

# Check effective repositories
./gradlew dependencies
```

### Version Conflicts
```bash
# Show dependency tree
./gradlew dependencies --configuration runtimeClasspath

# Show conflict resolution
./gradlew dependencyInsight --dependency org.springframework:spring-core
```

### Lock File Issues
```bash
# Resolve lock state
./gradlew dependencies --write-locks

# Update specific dependencies
./gradlew dependencies --update-locks com.fasterxml.jackson:*
```

### Build Cache Issues
```bash
# Clean all caches
./gradlew cleanBuildCache
rm -rf ~/.gradle/caches/

# Disable cache temporarily
./gradlew build --no-build-cache
```

---

## Multi-Project Builds

Gradle multi-project builds affect SBOM generation:

```kotlin
// settings.gradle.kts
rootProject.name = "my-project"
include("module-a", "module-b", "module-c")
```

**SBOM Options**:
- Root project aggregates all modules
- Individual module SBOMs

```bash
# Generate for all modules
./gradlew cyclonedxBom

# Generate for specific module
./gradlew :module-a:cyclonedxBom
```

---

## Best Practices Detection

### Gradle Lock File Present
**Pattern**: `gradle\.lockfile`
**Type**: regex
**Severity**: info
**Languages**: [groovy, kotlin]
**Context**: lock file
- Dependency locking enabled
- Reproducible builds

### Dependency Locking Enabled
**Pattern**: `dependencyLocking\s*\{[\s\S]*lockAllConfigurations`
**Type**: regex
**Severity**: info
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- Lock all configurations
- Best practice for reproducibility

### Gradle Wrapper Present
**Pattern**: `gradlew|gradle-wrapper\.jar`
**Type**: regex
**Severity**: info
**Languages**: [shell]
**Context**: project root
- Using Gradle wrapper
- Consistent Gradle versions

### Version Catalog Usage
**Pattern**: `libs\.versions\.toml`
**Type**: regex
**Severity**: info
**Languages**: [toml]
**Context**: gradle directory
- Centralized version management
- Modern Gradle 7+ practice

### Dependency Verification
**Pattern**: `verification-metadata\.xml`
**Type**: regex
**Severity**: info
**Languages**: [xml]
**Context**: gradle directory
- Checksum verification enabled
- Supply chain security

---

## Anti-Patterns Detection

### Dynamic Version (Plus)
**Pattern**: `['\"][^'\"]+:[^'\"]+:\+['\"]`
**Type**: regex
**Severity**: high
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- Dynamic version with + notation
- CWE-829: Non-deterministic dependency

### Range Version (Latest)
**Pattern**: `['\"][^'\"]+:[^'\"]+:latest\.[^'\"]*['\"]`
**Type**: regex
**Severity**: high
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- latest.release or latest.integration
- CWE-829: Unpinned dependency

### Insecure Repository
**Pattern**: `url\s*[=:]\s*['\"]http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- Non-HTTPS repository
- CWE-319: Cleartext Transmission

### Credentials in Build File
**Pattern**: `(password|username)\s*[=:]\s*['\"][^'\"]{4,}['\"]`
**Type**: regex
**Severity**: critical
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- Hardcoded credentials
- CWE-798: Hardcoded Credentials

### JCenter Repository (Deprecated)
**Pattern**: `jcenter\(\)`
**Type**: regex
**Severity**: medium
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- JCenter is deprecated/sunset
- Should migrate to Maven Central

### Missing Dependency Locking
**Pattern**: `dependencies\s*\{(?![\s\S]*dependencyLocking)`
**Type**: regex
**Severity**: medium
**Languages**: [groovy, kotlin]
**Context**: build.gradle
- No dependency locking enabled
- CWE-829: Non-reproducible builds

---

## References

- [Gradle Documentation](https://docs.gradle.org/)
- [Gradle Dependency Locking](https://docs.gradle.org/current/userguide/dependency_locking.html)
- [CycloneDX Gradle Plugin](https://github.com/CycloneDX/cyclonedx-gradle-plugin)
- [Version Catalogs](https://docs.gradle.org/current/userguide/platforms.html)
- [Dependency Verification](https://docs.gradle.org/current/userguide/dependency_verification.html)
