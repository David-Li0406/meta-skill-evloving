# JFrog Artifactory

**Category**: package-registries
**Description**: Universal artifact repository manager for all package types
**Homepage**: https://jfrog.com/artifactory

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*JFrog client libraries*

- `jfrog-client-js` - JFrog client for JavaScript
- `@jfrog/jfrog-cli-v2` - JFrog CLI npm package

#### PYPI
*JFrog Python tools*

- `jfrog-python-sdk` - JFrog SDK for Python
- `artifactory` - Python Artifactory client
- `dohq-artifactory` - Alternative Artifactory client

#### MAVEN
*JFrog Java SDK*

- `org.jfrog.artifactory.client:artifactory-java-client-services` - Java client
- `org.jfrog.buildinfo:build-info-extractor` - Build info extractor

#### GO
*JFrog Go client*

- `github.com/jfrog/jfrog-client-go` - JFrog client for Go

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Artifactory usage*

- `.jfrog/` - JFrog CLI configuration directory
- `jfrog-cli.conf` - JFrog CLI configuration
- `artifactory.properties` - Artifactory properties
- `settings.xml` - Maven settings with Artifactory repos
- `.npmrc` - NPM config with Artifactory registry
- `pip.conf` - Pip config with Artifactory PyPI
- `pyproject.toml` - Python project with Artifactory source
- `build.gradle` - Gradle with Artifactory plugin
- `build.gradle.kts` - Kotlin DSL with Artifactory
- `.yarnrc.yml` - Yarn config with Artifactory registry

### Configuration Directories
*Known directories that indicate Artifactory usage*

- `.jfrog/` - JFrog CLI directory

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^from\s+artifactory\s+import`
- Artifactory Python client import
- Example: `from artifactory import ArtifactoryPath`

**Pattern**: `^import\s+dohq_artifactory`
- Alternative client import
- Example: `import dohq_artifactory`

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.jfrog\.artifactory`
- Artifactory Java client
- Example: `import org.jfrog.artifactory.client.Artifactory;`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/jfrog/jfrog-client-go`
- JFrog Go client import
- Example: `import "github.com/jfrog/jfrog-client-go/artifactory"`

### Code Patterns

**Pattern**: `\.jfrog\.io|artifactory\.[a-zA-Z0-9-]+\.(com|io|net)`
- JFrog cloud or self-hosted Artifactory URL
- Example: `https://mycompany.jfrog.io/artifactory/`

**Pattern**: `artifactoryPublish|artifactoryDeploy`
- Gradle Artifactory plugin tasks
- Example: `tasks.named("artifactoryPublish")`

**Pattern**: `jfrog rt upload|jfrog rt download|jfrog rt build`
- JFrog CLI commands in scripts
- Example: `jfrog rt upload "*.jar" libs-release-local/`

---

## Environment Variables

- `JFROG_URL` - JFrog platform URL
- `JFROG_ARTIFACTORY_URL` - Artifactory URL
- `JFROG_ACCESS_TOKEN` - JFrog access token
- `JFROG_USER` - JFrog username
- `JFROG_PASSWORD` - JFrog password
- `JFROG_API_KEY` - JFrog API key (deprecated)
- `ARTIFACTORY_URL` - Artifactory server URL
- `ARTIFACTORY_USER` - Artifactory username
- `ARTIFACTORY_PASSWORD` - Artifactory password
- `ARTIFACTORY_API_KEY` - Artifactory API key
- `NPM_REGISTRY` - NPM registry (often Artifactory)
- `PYPI_REPOSITORY_URL` - PyPI repository URL

## Detection Notes

- Look for registry URLs pointing to jfrog.io or custom Artifactory domains
- Maven settings.xml with non-central repositories is a strong indicator
- .npmrc with custom registry URLs suggests Artifactory for npm
- pip.conf or pyproject.toml with custom index-url indicates Python repos
- JFrog CLI creates `.jfrog/` directory for configuration
- Gradle/Maven plugins for Artifactory deployment are common

---

## Secrets Detection

### API Keys and Tokens

#### JFrog Access Token
**Pattern**: `(?:jfrog|artifactory).*(?:token|access)['":\s]*[=:]\s*['"]?([a-zA-Z0-9._-]{64,})['"]?`
**Severity**: critical
**Description**: JFrog access token for API authentication
**Example**: `JFROG_ACCESS_TOKEN=cmVmdGtuOjAxOjE3...`

#### JFrog API Key
**Pattern**: `(?:jfrog|artifactory).*api[_-]?key['":\s]*[=:]\s*['"]?([a-zA-Z0-9]{64,})['"]?`
**Severity**: critical
**Description**: JFrog API key (deprecated but still used)
**Example**: `artifactory_api_key: AKCp8...`

#### Artifactory Encrypted Password
**Pattern**: `\{DESede\}[A-Za-z0-9+/=]+`
**Severity**: high
**Description**: Encrypted password in Maven settings
**Example**: `<password>{DESede}abc123...</password>`

### Validation

#### API Documentation
- **REST API**: https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API
- **Access Tokens**: https://www.jfrog.com/confluence/display/JFROG/Access+Tokens

#### Validation Endpoint
**API**: System Ping
**Endpoint**: `{artifactory_url}/api/system/ping`
**Method**: GET
**Headers**: `Authorization: Bearer {token}` or `X-JFrog-Art-Api: {api_key}`
**Purpose**: Validates connectivity and authentication

```bash
# Validate JFrog credentials
curl -H "Authorization: Bearer $JFROG_ACCESS_TOKEN" \
     "$JFROG_URL/artifactory/api/system/ping"
```

---

## TIER 3: Configuration Extraction

### Repository URL Extraction

**Pattern**: `https?://([a-zA-Z0-9-]+)\.jfrog\.io/artifactory/([a-zA-Z0-9_-]+)`
- JFrog Cloud repository URL
- Extracts: `org_name`, `repo_name`
- Example: `https://mycompany.jfrog.io/artifactory/npm-local/`

**Pattern**: `url\s*[=:]\s*['"]https?://[^'"]+/artifactory/([^'"]+)['"]`
- Artifactory repository from config
- Extracts: `repo_path`
- Example: `url = "https://artifactory.example.com/artifactory/libs-release/"`

### Maven Repository Extraction

**Pattern**: `<url>https?://([^<]+)/artifactory/([^<]+)</url>`
- Artifactory repo in Maven settings/pom
- Extracts: `artifactory_host`, `repo_name`
- Example: `<url>https://company.jfrog.io/artifactory/libs-release/</url>`
