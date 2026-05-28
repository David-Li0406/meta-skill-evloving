# New Relic

**Category**: monitoring
**Description**: New Relic observability and APM platform
**Homepage**: https://newrelic.com

## Package Detection

### NPM
*New Relic Node.js and browser agents*

- `newrelic`
- `@newrelic/browser-agent`
- `@newrelic/next`

### PYPI
*New Relic Python agent*

- `newrelic`

### RUBYGEMS
*New Relic Ruby agent*

- `newrelic_rpm`

### MAVEN
*New Relic Java agent*

- `com.newrelic.agent.java:newrelic-api`
- `com.newrelic.agent.java:newrelic-agent`

### GO
*New Relic Go agent*

- `github.com/newrelic/go-agent/v3`

### Related Packages
- `@newrelic/winston-enricher`
- `newrelic-naming`

## Import Detection

### Javascript

**Pattern**: `require\(['"]newrelic['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]newrelic['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@newrelic/browser-agent['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+newrelic`
- Type: python_import

**Pattern**: `from\s+newrelic`
- Type: python_import

**Pattern**: `newrelic\.agent`
- Type: python_import

### Go

**Pattern**: `"github\.com/newrelic/go-agent`
- Type: go_import

### Ruby

**Pattern**: `require\s+['"]newrelic_rpm['"]`
- Type: ruby_require

## Environment Variables

*New Relic license key*

*Application name in New Relic*

*New Relic API key*

*Enable distributed tracing*

*Agent log level*

*Enable/disable agent*

*Use environment variables only*


## Detection Notes

- Check for NEW_RELIC_LICENSE_KEY environment variable
- Look for newrelic.js configuration file
- Free tier available with generous limits

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
