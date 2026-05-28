# Maven Package Manager

**Ecosystem**: Java/JVM
**Package Registry**: https://repo.maven.apache.org/maven2 (Maven Central)
**Documentation**: https://maven.apache.org/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `pom.xml` | Yes | Project Object Model |
| `settings.xml` | No | User/global configuration |
| `.mvn/maven.config` | No | Project-specific Maven options |

### pom.xml Detection

**Pattern**: `pom\.xml$`
**Confidence**: 98% (HIGH)

### Required Sections for SBOM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.1.0</version>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

### Dependency Scopes

| Scope | Included in SBOM | Notes |
|-------|------------------|-------|
| `compile` | Yes (always) | Default scope, production runtime |
| `runtime` | Yes (always) | Runtime only, not compile-time |
| `provided` | Configurable | Expected from container |
| `test` | Configurable | Testing only |
| `system` | Yes | Local JAR (deprecated) |
| `import` | Resolved | BOM imports |

---

## TIER 2: Effective POM Resolution

Maven does not have a traditional lock file. Instead, dependency resolution produces an "effective POM."

### Generating Effective POM

```bash
# Generate effective POM with all resolved versions
mvn help:effective-pom -Doutput=effective-pom.xml

# Show dependency tree
mvn dependency:tree

# Output to file
mvn dependency:tree -DoutputFile=dependency-tree.txt
```

### Dependency Tree Format

```
[INFO] com.example:my-app:jar:1.0.0
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:3.1.0:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:3.1.0:compile
[INFO] |  |  +- org.springframework.boot:spring-boot:jar:3.1.0:compile
[INFO] |  |  \- org.springframework.boot:spring-boot-autoconfigure:jar:3.1.0:compile
```

### Key Resolution Concepts

| Concept | Description |
|---------|-------------|
| Nearest Definition | First declaration wins in tree |
| Dependency Management | Centralized version control |
| BOM (Bill of Materials) | Import shared version definitions |
| Exclusions | Remove transitive dependencies |

---

## TIER 3: Configuration Extraction

### Repository Configuration

**File**: `settings.xml` (located in `~/.m2/` or `$MAVEN_HOME/conf/`)

**Pattern**: `<url>([^<]+)</url>`
**Context**: Inside `<repository>` or `<mirror>` elements

### Common Configuration

```xml
<!-- settings.xml -->
<settings>
    <mirrors>
        <mirror>
            <id>internal-repo</id>
            <mirrorOf>central</mirrorOf>
            <url>https://nexus.mycompany.com/repository/maven-public/</url>
        </mirror>
    </mirrors>

    <servers>
        <server>
            <id>internal-repo</id>
            <username>${env.MAVEN_USERNAME}</username>
            <password>${env.MAVEN_PASSWORD}</password>
        </server>
    </servers>

    <profiles>
        <profile>
            <id>internal</id>
            <repositories>
                <repository>
                    <id>internal-releases</id>
                    <url>https://nexus.mycompany.com/repository/releases/</url>
                </repository>
            </repositories>
        </profile>
    </profiles>
</settings>
```

### pom.xml Repository Configuration

```xml
<repositories>
    <repository>
        <id>spring-milestones</id>
        <url>https://repo.spring.io/milestone</url>
    </repository>
</repositories>
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `MAVEN_HOME` | Maven installation directory |
| `MAVEN_OPTS` | JVM options for Maven |
| `MAVEN_USERNAME` | Repository username |
| `MAVEN_PASSWORD` | Repository password |

---

## SBOM Generation

### Using CycloneDX Maven Plugin

```xml
<!-- Add to pom.xml -->
<plugin>
    <groupId>org.cyclonedx</groupId>
    <artifactId>cyclonedx-maven-plugin</artifactId>
    <version>2.7.11</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>makeAggregateBom</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <projectType>application</projectType>
        <schemaVersion>1.5</schemaVersion>
        <includeBomSerialNumber>true</includeBomSerialNumber>
        <includeCompileScope>true</includeCompileScope>
        <includeProvidedScope>false</includeProvidedScope>
        <includeRuntimeScope>true</includeRuntimeScope>
        <includeSystemScope>false</includeSystemScope>
        <includeTestScope>false</includeTestScope>
        <includeLicenseText>false</includeLicenseText>
        <outputFormat>json</outputFormat>
    </configuration>
</plugin>
```

```bash
# Generate SBOM
mvn cyclonedx:makeAggregateBom

# Output location: target/bom.json
```

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type maven -o sbom.json
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
| `includeCompileScope` | Include compile dependencies | true |
| `includeRuntimeScope` | Include runtime dependencies | true |
| `includeTestScope` | Include test dependencies | false |
| `includeProvidedScope` | Include provided dependencies | false |
| `outputFormat` | json or xml | json |
| `schemaVersion` | CycloneDX version | 1.5 |

---

## Cache Locations

| Location | Path |
|----------|------|
| Local Repository | `~/.m2/repository/` |
| Downloaded POMs | `~/.m2/repository/<group>/<artifact>/` |
| Plugin Cache | `~/.m2/repository/org/apache/maven/plugins/` |

```bash
# Find Maven home
mvn --version

# Purge local repository
mvn dependency:purge-local-repository

# Download all dependencies
mvn dependency:go-offline
```

---

## Best Practices Detection

Patterns to detect good dependency management practices in CI/CD, Makefiles, and scripts.

### mvn dependency:tree
**Pattern**: `mvn\s+.*dependency:tree`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Visualizing dependency tree
- Helps identify conflicts and transitive dependencies

### mvn dependency:analyze
**Pattern**: `mvn\s+.*dependency:analyze`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Finding unused and undeclared dependencies
- Code hygiene check

### mvn verify
**Pattern**: `mvn\s+(verify|clean\s+verify)`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Running all checks including tests
- Full build verification

### mvn dependency:go-offline
**Pattern**: `mvn\s+.*dependency:go-offline`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Downloading dependencies for offline use
- Useful for air-gapped builds

### OWASP dependency check
**Pattern**: `org\.owasp:dependency-check-maven|dependency-check:check`
**Type**: regex
**Severity**: info
**Context**: pom.xml, CI/CD
- Vulnerability scanning with OWASP
- Supply chain security

### versions:display-dependency-updates
**Pattern**: `versions:display-dependency-updates`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Checking for available updates
- Staying current with dependencies

### CycloneDX plugin
**Pattern**: `cyclonedx-maven-plugin|cyclonedx:make`
**Type**: regex
**Severity**: info
**Context**: pom.xml, CI/CD
- SBOM generation
- Supply chain transparency

---

## Anti-Patterns Detection

Patterns that indicate potential issues.

### SNAPSHOT in release builds
**Pattern**: `<version>.*-SNAPSHOT</version>`
**Type**: regex
**Severity**: medium
**Context**: pom.xml
- SNAPSHOT versions are mutable
- Should not be in production releases

### HTTP repositories
**Pattern**: `<url>http://[^<]+</url>`
**Type**: regex
**Severity**: high
**Context**: pom.xml, settings.xml
- Using HTTP for repository URLs
- Vulnerable to MITM attacks

### System scope dependencies
**Pattern**: `<scope>system</scope>`
**Type**: regex
**Severity**: medium
**Context**: pom.xml
- System scope dependencies are deprecated
- Not portable across environments

### Skipping tests in CI
**Pattern**: `-DskipTests|-Dmaven\.test\.skip=true`
**Type**: regex
**Severity**: medium
**Context**: CI/CD
- Skipping tests in CI pipeline
- May hide security issues

### Version ranges
**Pattern**: `<version>\[[^\]]+\]</version>|<version>\([^\)]+\)</version>`
**Type**: regex
**Severity**: medium
**Context**: pom.xml
- Version ranges are non-deterministic
- Can break builds unexpectedly

---

## Best Practices Summary

1. **Use dependency management** in parent POM for version control
2. **Lock versions** with `<dependencyManagement>` section
3. **Use BOMs** for framework version alignment
4. **Generate SBOM during CI/CD** for consistency
5. **Exclude unnecessary transitive dependencies**
6. **Run `mvn dependency:analyze`** to find unused dependencies

### Dependency Management Pattern

```xml
<dependencyManagement>
    <dependencies>
        <!-- Import Spring Boot BOM -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.1.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Version Locking with versions-maven-plugin

```bash
# Lock all SNAPSHOT versions
mvn versions:lock-snapshots

# Update to latest versions
mvn versions:use-latest-releases

# Display dependency updates
mvn versions:display-dependency-updates
```

---

## Troubleshooting

### Dependency Not Found
```bash
# Force update snapshots and releases
mvn clean install -U

# Check effective settings
mvn help:effective-settings
```

### Version Conflicts
```bash
# Show dependency tree with conflicts
mvn dependency:tree -Dverbose

# Analyze dependencies
mvn dependency:analyze

# Show why a dependency was included
mvn dependency:tree -Dincludes=groupId:artifactId
```

### Private Repository Issues
```xml
<!-- In settings.xml -->
<server>
    <id>my-repo</id>
    <username>user</username>
    <password>password</password>
</server>
```

### Offline Mode
```bash
# Work offline with cached dependencies
mvn -o clean install

# Download all for offline use
mvn dependency:go-offline
```

---

## Multi-Module Projects

Maven multi-module projects affect SBOM generation:

```xml
<!-- Parent pom.xml -->
<modules>
    <module>module-a</module>
    <module>module-b</module>
    <module>module-c</module>
</modules>
```

**SBOM Options**:
- `makeAggregateBom` - Single SBOM for all modules
- `makeBom` - Individual SBOM per module

```bash
# Aggregate BOM for all modules
mvn cyclonedx:makeAggregateBom -pl :parent-module

# Individual BOMs
mvn cyclonedx:makeBom -pl :specific-module
```

---

## References

- [Maven Documentation](https://maven.apache.org/)
- [Maven POM Reference](https://maven.apache.org/pom.html)
- [CycloneDX Maven Plugin](https://github.com/CycloneDX/cyclonedx-maven-plugin)
- [Maven Dependency Plugin](https://maven.apache.org/plugins/maven-dependency-plugin/)
- [Versions Maven Plugin](https://www.mojohaus.org/versions/versions-maven-plugin/)
