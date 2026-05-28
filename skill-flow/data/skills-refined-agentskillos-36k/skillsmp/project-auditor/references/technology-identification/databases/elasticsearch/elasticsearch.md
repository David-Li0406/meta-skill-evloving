# Elasticsearch

**Category**: databases
**Description**: Elasticsearch search and analytics engine
**Homepage**: https://www.elastic.co/elasticsearch

## Package Detection

### NPM
*Elasticsearch Node.js clients*

- `@elastic/elasticsearch`
- `elasticsearch`

### PYPI
*Elasticsearch Python clients*

- `elasticsearch`
- `elasticsearch-dsl`

### MAVEN
*Elasticsearch Java clients*

- `org.elasticsearch.client:elasticsearch-rest-high-level-client`
- `co.elastic.clients:elasticsearch-java`

### GO
*Elasticsearch Go client*

- `github.com/elastic/go-elasticsearch`

### RUBYGEMS
*Elasticsearch Ruby clients*

- `elasticsearch`
- `searchkick`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@elastic/elasticsearch['"]`
- Type: esm_import

**Pattern**: `require\(['"]@elastic/elasticsearch['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `from\s+elasticsearch`
- Type: python_import

**Pattern**: `import\s+elasticsearch`
- Type: python_import

### Go

**Pattern**: `"github\.com/elastic/go-elasticsearch`
- Type: go_import

## Environment Variables

*Elasticsearch URL*

*Elasticsearch URL*

*Elasticsearch host*

*Elastic Cloud ID*

*Elastic API key*

*Elasticsearch username*

*Elasticsearch password*


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
