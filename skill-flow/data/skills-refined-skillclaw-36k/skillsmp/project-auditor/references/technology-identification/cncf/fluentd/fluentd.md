# Fluentd

**Category**: cncf
**Description**: Data collector for unified logging layer
**Homepage**: https://fluentd.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Fluentd JavaScript packages*

- `fluent-logger` - Fluentd logger for Node.js
- `fluent-ffmpeg` - Different project

#### PYPI
*Fluentd Python packages*

- `fluent-logger` - Fluentd Python logger
- `fluent` - Alternative logger

#### RUBYGEMS
*Fluentd Ruby packages*

- `fluentd` - Fluentd core
- `fluent-logger` - Ruby logger
- `fluent-plugin-*` - Fluentd plugins

#### GO
*Fluentd Go packages*

- `github.com/fluent/fluent-logger-golang` - Go logger

#### MAVEN
*Fluentd Java packages*

- `org.fluentd:fluent-logger` - Java logger

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Fluentd usage*

- `fluent.conf` - Fluentd configuration
- `fluentd.conf` - Alternative config name
- `td-agent.conf` - td-agent configuration
- `fluent-bit.conf` - Fluent Bit configuration
- `parsers.conf` - Parser configuration
- `plugins/` - Plugin directory

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^from\s+fluent\s+import`
- Fluent Python import
- Example: `from fluent import sender`

#### Ruby
Extensions: `.rb`

**Pattern**: `require\s+['"]fluentd['"]`
- Fluentd Ruby require
- Example: `require 'fluentd'`

### Code Patterns

**Pattern**: `<source>|<match>|<filter>|@type\s+forward`
- Fluentd configuration directives
- Example: `<source>\n@type forward\n</source>`

**Pattern**: `fluentd\.org|td-agent|fluent-bit`
- Fluentd references
- Example: `fluentd:24224`

**Pattern**: `FLUENT_|FLUENTD_`
- Fluentd environment variables
- Example: `FLUENT_ELASTICSEARCH_HOST`

**Pattern**: `:24224|:9880`
- Fluentd default ports
- Example: `localhost:24224`

**Pattern**: `@include|@type|@id|@label`
- Fluentd config directives
- Example: `@type elasticsearch`

---

## Environment Variables

- `FLUENT_ELASTICSEARCH_HOST` - Elasticsearch host
- `FLUENT_ELASTICSEARCH_PORT` - Elasticsearch port
- `FLUENT_ELASTICSEARCH_USER` - Elasticsearch user
- `FLUENT_ELASTICSEARCH_PASSWORD` - Elasticsearch password
- `FLUENTD_CONF` - Config file path
- `FLUENTD_OPT` - Additional options

## Detection Notes

- Default forward port is 24224
- td-agent is the enterprise distribution
- Fluent Bit is the lightweight alternative
- Plugins extend functionality significantly

---

## Secrets Detection

### Credentials

#### Fluentd Elasticsearch Password
**Pattern**: `(?:fluent|FLUENT).*(?:password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Fluentd Elasticsearch password
**Example**: `FLUENT_ELASTICSEARCH_PASSWORD=secret`

#### Fluentd HTTP Auth
**Pattern**: `<(?:source|match|filter)[^>]*>[\s\S]*?password\s+['"]?([^\s'"<>]{4,})['"]?`
**Severity**: high
**Description**: Password in Fluentd config block

---

## TIER 3: Configuration Extraction

### Tag Pattern Extraction

**Pattern**: `<match\s+([^>]+)>`
- Match tag pattern
- Extracts: `tag_pattern`
- Example: `<match app.**>`

### Output Type Extraction

**Pattern**: `@type\s+(['"]?[a-zA-Z0-9_-]+['"]?)`
- Output plugin type
- Extracts: `output_type`
- Example: `@type elasticsearch`
