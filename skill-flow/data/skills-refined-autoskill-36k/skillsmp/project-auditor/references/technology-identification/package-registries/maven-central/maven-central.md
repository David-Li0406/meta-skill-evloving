# Maven Central

**Category**: package-registries
**Description**: Primary repository for Java/JVM packages
**Homepage**: https://central.sonatype.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### MAVEN
*Maven-related dependencies*

- `org.apache.maven.plugins:maven-deploy-plugin` - Deploy plugin
- `org.apache.maven.plugins:maven-gpg-plugin` - GPG signing plugin
- `org.sonatype.plugins:nexus-staging-maven-plugin` - Staging plugin

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Maven Central usage*

- `pom.xml` - Maven project file
- `settings.xml` - Maven settings
- `build.gradle` - Gradle build file
- `build.gradle.kts` - Kotlin Gradle build
- `gradle.properties` - Gradle properties
- `.m2/settings.xml` - User Maven settings
- `settings-security.xml` - Maven encrypted settings

### Code Patterns

**Pattern**: `repo1?\.maven\.org|central\.sonatype\.com|search\.maven\.org`
- Maven Central URLs
- Example: `https://repo1.maven.org/maven2/`

**Pattern**: `oss\.sonatype\.org|s01\.oss\.sonatype\.org`
- Sonatype OSSRH (publishing)
- Example: `https://s01.oss.sonatype.org/`

**Pattern**: `<distributionManagement>|mavenCentral\(\)`
- Maven Central publishing configuration
- Example: `repositories { mavenCentral() }`

**Pattern**: `MAVEN_|OSSRH_|SONATYPE_`
- Maven/Sonatype environment variables
- Example: `MAVEN_GPG_PASSPHRASE`

**Pattern**: `gpg:sign|nexus-staging:deploy`
- Maven Central publishing goals
- Example: `mvn gpg:sign nexus-staging:deploy`

---

## Environment Variables

- `MAVEN_USERNAME` - Maven Central username
- `MAVEN_PASSWORD` - Maven Central password
- `MAVEN_GPG_PASSPHRASE` - GPG signing passphrase
- `MAVEN_GPG_KEY` - GPG private key
- `OSSRH_USERNAME` - OSSRH username
- `OSSRH_TOKEN` - OSSRH token/password
- `SONATYPE_USERNAME` - Sonatype username
- `SONATYPE_PASSWORD` - Sonatype password
- `GPG_PASSPHRASE` - GPG passphrase
- `SIGNING_KEY` - GPG signing key
- `SIGNING_PASSWORD` - Signing password

## Detection Notes

- Publishing to Maven Central requires Sonatype OSSRH account
- GPG signing is mandatory for Central
- nexus-staging-maven-plugin automates release process
- Gradle uses maven-publish and signing plugins
- settings.xml should never be committed
- Look for ossrh or sonatype server IDs

---

## Secrets Detection

### Credentials

#### Maven/Sonatype Password
**Pattern**: `(?:MAVEN|OSSRH|SONATYPE).*(?:PASSWORD|TOKEN|password|token)\s*[=:]\s*['"]?([^\s'"<>]+)['"]?`
**Severity**: critical
**Description**: Maven Central/Sonatype credentials
**Example**: `OSSRH_TOKEN=abc123...`

#### GPG Passphrase
**Pattern**: `(?:GPG|MAVEN).*(?:PASSPHRASE|passphrase)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: GPG signing passphrase
**Example**: `MAVEN_GPG_PASSPHRASE=secret`

#### GPG Private Key
**Pattern**: `-----BEGIN PGP PRIVATE KEY BLOCK-----`
**Severity**: critical
**Description**: GPG private key for signing
**Example**: `-----BEGIN PGP PRIVATE KEY BLOCK-----\nVersion: ...`

#### Maven Settings Server Password
**Pattern**: `<server>.*?<id>(?:ossrh|sonatype|central)[^<]*</id>.*?<password>([^<]+)</password>`
**Severity**: critical
**Description**: Server credentials in settings.xml
**Multiline**: true

#### Encrypted Maven Password
**Pattern**: `\{[A-Za-z0-9+/=]{20,}\}`
**Severity**: high
**Description**: Maven encrypted password
**Context Required**: Near <password> or settings.xml
**Example**: `{abc123def456...}`

### Validation

#### API Documentation
- **Central Portal**: https://central.sonatype.org/publish/
- **OSSRH Guide**: https://central.sonatype.org/publish/publish-guide/

#### Validation Endpoint
**API**: Search
**Endpoint**: `https://search.maven.org/solrsearch/select?q=g:{groupId}`
**Method**: GET
**Purpose**: Search packages (no auth required)

Note: Credentials can only be validated by attempting to publish to OSSRH.

---

## TIER 3: Configuration Extraction

### Group ID Extraction

**Pattern**: `<groupId>([a-zA-Z0-9._-]+)</groupId>`
- Maven group ID from pom.xml
- Extracts: `group_id`
- Example: `<groupId>com.example</groupId>`

### Repository URL Extraction

**Pattern**: `<url>(https?://[^<]+maven[^<]*)</url>`
- Maven repository URL
- Extracts: `repo_url`
- Example: `<url>https://repo1.maven.org/maven2/</url>`

### Server ID Extraction

**Pattern**: `<server>.*?<id>([^<]+)</id>`
- Server ID from settings.xml
- Extracts: `server_id`
- Example: `<id>ossrh</id>`
