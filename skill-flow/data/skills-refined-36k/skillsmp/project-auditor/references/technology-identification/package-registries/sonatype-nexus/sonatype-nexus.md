# Sonatype Nexus Repository

**Category**: package-registries
**Description**: Universal repository manager for Maven, npm, Docker, and more
**Homepage**: https://www.sonatype.com/products/nexus-repository

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### MAVEN
*Nexus-related dependencies*

- `org.sonatype.nexus:nexus-repository` - Nexus repository
- `org.sonatype.nexus:nexus-core` - Nexus core
- `org.sonatype.nexus.plugins:nexus-staging-maven-plugin` - Staging plugin

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Nexus usage*

- `settings.xml` - Maven settings with Nexus repositories
- `.npmrc` - NPM config with Nexus registry
- `pip.conf` - Pip config with Nexus PyPI proxy
- `nuget.config` - NuGet config with Nexus source
- `build.gradle` - Gradle with Nexus repository
- `pom.xml` - Maven POM with Nexus distributionManagement
- `.docker/config.json` - Docker config with Nexus registry

### Code Patterns

**Pattern**: `nexus\..*\.com|sonatype\.org`
- Nexus server URLs
- Example: `https://nexus.mycompany.com/repository/`

**Pattern**: `/repository/maven-|/repository/npm-|/repository/docker-`
- Nexus repository paths
- Example: `https://nexus.example.com/repository/maven-releases/`

**Pattern**: `nexus-staging-maven-plugin|nexus-publish-plugin`
- Nexus Maven/Gradle plugins
- Example: `<artifactId>nexus-staging-maven-plugin</artifactId>`

**Pattern**: `NEXUS_|SONATYPE_`
- Nexus environment variables
- Example: `NEXUS_USERNAME=admin`

**Pattern**: `oss\.sonatype\.org|s01\.oss\.sonatype\.org`
- Sonatype OSS Nexus (Maven Central staging)
- Example: `https://s01.oss.sonatype.org/`

---

## Environment Variables

- `NEXUS_URL` - Nexus server URL
- `NEXUS_USERNAME` - Nexus username
- `NEXUS_PASSWORD` - Nexus password
- `NEXUS_REPOSITORY` - Default repository name
- `SONATYPE_USERNAME` - Sonatype OSS username
- `SONATYPE_PASSWORD` - Sonatype OSS password
- `OSSRH_USERNAME` - OSS Repository Hosting username
- `OSSRH_TOKEN` - OSS Repository Hosting token

## Detection Notes

- Maven settings.xml with non-central repositories indicates Nexus
- Nexus URL patterns: /repository/<repo-name>/
- OSS Sonatype is used for Maven Central publishing
- Docker registries often use port 8082 or 8083
- Look for nexus-staging-maven-plugin in pom.xml

---

## Secrets Detection

### Credentials

#### Nexus Password
**Pattern**: `(?:nexus|NEXUS).*(?:password|PASSWORD|pass|PASS)\s*[=:]\s*['"]?([^\s'"<>]+)['"]?`
**Severity**: critical
**Description**: Nexus repository password
**Example**: `NEXUS_PASSWORD=secretpass`

#### Nexus API Token
**Pattern**: `(?:nexus|NEXUS).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]{20,})['"]?`
**Severity**: critical
**Description**: Nexus API/user token
**Example**: `NEXUS_TOKEN=abc123...`

#### Maven Server Credentials
**Pattern**: `<server>.*?<id>([^<]+)</id>.*?<password>([^<]+)</password>.*?</server>`
**Severity**: critical
**Description**: Maven settings.xml server credentials
**Multiline**: true

#### Sonatype OSSRH Credentials
**Pattern**: `(?:OSSRH|SONATYPE|ossrh|sonatype).*(?:password|PASSWORD|token|TOKEN)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Sonatype OSS Repository Hosting credentials
**Example**: `OSSRH_TOKEN=abc123...`

### Validation

#### API Documentation
- **REST API**: https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api
- **Staging API**: https://oss.sonatype.org/nexus-staging-plugin/default/docs/index.html

#### Validation Endpoint
**API**: Status
**Endpoint**: `{nexus_url}/service/rest/v1/status`
**Method**: GET
**Headers**: `Authorization: Basic {base64(user:pass)}`
**Purpose**: Validates connectivity and authentication

```bash
# Validate Nexus credentials
curl -u "$NEXUS_USERNAME:$NEXUS_PASSWORD" \
     "$NEXUS_URL/service/rest/v1/status"
```

---

## TIER 3: Configuration Extraction

### Repository URL Extraction

**Pattern**: `<url>https?://([^<]+)/repository/([^<]+)</url>`
- Nexus repository from Maven POM/settings
- Extracts: `nexus_host`, `repo_name`
- Example: `<url>https://nexus.example.com/repository/maven-releases/</url>`

**Pattern**: `registry\s*=\s*https?://([^/]+)/repository/([^\s]+)`
- Nexus NPM registry from .npmrc
- Extracts: `nexus_host`, `repo_name`
- Example: `registry=https://nexus.example.com/repository/npm-group/`
