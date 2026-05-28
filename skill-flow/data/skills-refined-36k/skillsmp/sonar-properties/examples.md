# SonarQube Properties Examples

## ⚠️ CRITICAL DEPRECATION WARNING

**Date**: December 2025
**Status**: This example may be outdated

**🚨 HIGH PRIORITY - DO NOT USE WITHOUT VERIFICATION**

Before using this example:
1. ✅ **Verify SonarQube version**: Check which version your organization uses
2. ✅ **Check property compatibility**: SonarQube properties may change between versions
3. ✅ **Detect test framework**: Determine if project uses Vitest or Jest
4. ✅ **Verify coverage paths**: Confirm test framework generates expected reports
5. ✅ **Review exclusion patterns**: Ensure patterns match your project structure
6. ✅ **Update project metadata**: Review projectKey, projectName, and projectDescription

**Important Notes**:
- **SonarQube 9.0+**: Some properties deprecated, check migration guide
- **SonarCloud**: May require additional properties (organization key)
- **Coverage formats**: Verify your test framework supports expected formats

---

## Example 1: sonar-project.properties (Vitest) - Recommended

**Configuration Date**: December 2025
**Test Framework**: Vitest 4.x
**Coverage Provider**: v8 or istanbul
**Use Case**: Vue 3 projects with Vitest testing

```properties
sonar.projectKey=my-vue-app
sonar.projectName=my-vue-app
sonar.projectDescription=Vue 3 application for my-vue-app
sonar.sources=src
sonar.language=ts
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
sonar.qualitygate.wait=true
sonar.javascript.lcov.reportPaths=./coverage/lcov.info
sonar.tests=src
sonar.test.inclusions=src/**/*.spec.ts
sonar.exclusions=src/**/*.spec.ts
sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts
```

---

## Example 2: sonar-project.properties (Jest) - Legacy

**Configuration Date**: December 2025
**Test Framework**: Jest 29.x
**Coverage Provider**: v8 or babel
**Use Case**: Vue 3 projects with Jest testing

```properties
sonar.projectKey=my-vue-app
sonar.projectName=my-vue-app
sonar.projectDescription=Vue 3 application for my-vue-app
sonar.sources=src
sonar.language=ts
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
sonar.qualitygate.wait=true
sonar.javascript.lcov.reportPaths=./coverage/lcov.info
sonar.clover.reportPaths=./coverage/clover.xml
sonar.tests=src
sonar.test.inclusions=src/**/*.spec.ts
sonar.exclusions=src/**/*.spec.ts
sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts
```

**Difference from Vitest version**:
- ✅ Added: `sonar.clover.reportPaths=./coverage/clover.xml` (Jest generates Clover XML)
- ⚠️ Note: Vitest does not generate Clover format

---

## Property Explanations

### Project Identification Properties

**`sonar.projectKey={application_name}`**
- Unique identifier for the project in SonarQube
- **Format**: Usually kebab-case, no spaces
- **Why**: Required for SonarQube to track project over time
- **Example**: `omni-inventory-manager-web`, `calculator-app`
- **⚠️ USER ACTION REQUIRED**: Review and update to match your organization's naming convention

**`sonar.projectName={application_name}`**
- Display name for the project in SonarQube UI
- **Format**: Can include spaces, more readable than projectKey
- **Why**: Human-readable identifier in dashboards
- **Example**: `Omni Inventory Manager`, `Calculator App`
- **⚠️ USER ACTION REQUIRED**: Review and update for better readability

**`sonar.projectDescription=Vue 3 application for {application_name}`**
- Description of the project
- **Why**: Provides context in SonarQube dashboard
- **Example**: `Vue 3 micro-frontend for inventory management`
- **⚠️ USER ACTION REQUIRED**: Customize to describe your application's purpose

### Source Configuration Properties

**`sonar.sources=src`**
- Directory containing source code to analyze
- **Default**: `src` (standard Vue project structure)
- **Why**: Tells SonarQube where to find code to analyze
- **Alternatives**: `src,lib` (multiple directories), `app` (non-standard structure)
- **Verify**: Ensure `src/` directory exists in your project

**`sonar.language=ts`**
- Primary programming language
- **Values**: `ts` (TypeScript) | `js` (JavaScript)
- **Why**: Helps SonarQube apply language-specific rules
- **Auto-detect**: Check for `typescript` in package.json dependencies
- **Note**: Vue files are automatically recognized as JavaScript/TypeScript

**`sonar.sourceEncoding=UTF-8`**
- Character encoding of source files
- **Standard**: `UTF-8` (universal modern standard)
- **Why**: Ensures proper parsing of non-ASCII characters
- **Note**: All modern projects should use UTF-8

### Version Control Properties

**`sonar.scm.provider=git`**
- Source control management system
- **Values**: `git` | `svn` | `mercurial` | `perforce`
- **Why**: Enables blame data and SCM integration features
- **Standard**: `git` (most common for Vue projects)
- **Verify**: Check `.git` directory exists

### Quality Gate Properties

**`sonar.qualitygate.wait=true`**
- Wait for quality gate computation before returning
- **Values**: `true` | `false`
- **Why**: CI/CD pipeline can fail if quality gate not met
- **Use Case**: Prevent merging code that fails quality standards
- **Impact**: Build will wait for SonarQube analysis to complete
- **Timeout**: Configured on SonarQube server (usually 5-10 minutes)

### Coverage Report Properties

**`sonar.javascript.lcov.reportPaths=./coverage/lcov.info`**
- Path to LCOV coverage report
- **Format**: LCOV tracefile format
- **Generated by**: Both Jest and Vitest
- **Why**: Universal coverage format for JavaScript/TypeScript
- **Multiple paths**: Comma-separated if multiple reports
- **⚠️ Verify**: Ensure test framework generates this file

**`sonar.clover.reportPaths=./coverage/clover.xml`** (Jest only)
- Path to Clover XML coverage report
- **Format**: Clover XML format
- **Generated by**: Jest with `clover` reporter
- **Why**: Additional coverage data format
- **⚠️ Note**: Vitest does NOT generate this format
- **When to include**: Only for Jest projects

### Test Configuration Properties

**`sonar.tests=src`**
- Directory containing test files
- **Standard**: `src` (tests co-located with source)
- **Why**: Tells SonarQube where test files are located
- **Alternative**: `tests`, `__tests__` (separate test directory)
- **Note**: Used with `sonar.test.inclusions` to identify test files

**`sonar.test.inclusions=src/**/*.spec.ts`**
- Pattern to identify test files
- **Format**: Glob pattern
- **Standard**: `**/*.spec.ts` (test files ending in .spec.ts)
- **Why**: Separates test files from production code in analysis
- **Alternatives**: 
  - `**/*.test.ts` (alternative naming convention)
  - `**/*.{spec,test}.ts` (both conventions)
- **Note**: Files matching this pattern excluded from coverage calculations

### Exclusion Properties

**`sonar.exclusions=src/**/*.spec.ts`**
- Files to exclude from analysis
- **Format**: Comma-separated glob patterns
- **Standard**: Exclude test files from code analysis
- **Why**: Test files shouldn't count toward code metrics
- **Additional patterns**:
  - `**/node_modules/**` (dependencies, usually auto-excluded)
  - `**/dist/**` (build output)
  - `**/coverage/**` (coverage reports)

**`sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts`**
- Files to exclude from coverage calculations
- **Format**: Comma-separated patterns (NO SPACES after commas)
- **Why**: Some files are not meaningfully unit-testable
- **Common exclusions**:
  - `src/main.ts` - Application entry point (tested via E2E)
  - `src/services/**/*.ts` - API services (tested with mocks)
  - `src/**/router/*.ts` - Route configuration (tested via E2E)
  - `src/store/index.ts` - Store setup (configuration file)
  - `src/**/interfaces/*.ts` - Type definitions (no runtime code)
  - `src/**/shared/constants/**/*.ts` - Static constants (no logic)

---

## How to Detect Test Framework

### Method 1: Check package.json Dependencies

```bash
# Check for Vitest
grep -q '"vitest"' package.json && echo "Vitest detected"

# Check for Jest
grep -q '"jest"' package.json && echo "Jest detected"

# One-liner to detect both
if grep -q '"vitest"' package.json; then
  echo "Test Framework: Vitest (use LCOV only)"
elif grep -q '"jest"' package.json; then
  echo "Test Framework: Jest (use LCOV + Clover)"
else
  echo "No test framework detected (default to Vitest)"
fi
```

### Method 2: Check for Config Files

```bash
# Vitest config files
if [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ]; then
  echo "Vitest config found"
fi

# Jest config files
if [ -f "jest.config.js" ] || [ -f "jest.config.ts" ] || [ -f "jest.config.cjs" ]; then
  echo "Jest config found"
fi
```

### Decision Matrix

| Condition | Test Framework | Coverage Reports |
|-----------|----------------|------------------|
| `"vitest"` in package.json | Vitest | LCOV only |
| `"jest"` in package.json | Jest | LCOV + Clover |
| Neither found | Default to Vitest | LCOV only |
| Both found | Use Vitest | LCOV only |

---

## Coverage Path Verification

### Verify Coverage Reports Exist

**For Vitest projects**:
```bash
# Run tests with coverage
npm run test:unit -- --coverage

# Verify LCOV report generated
if [ -f "coverage/lcov.info" ]; then
  echo "✓ LCOV report exists"
else
  echo "✗ LCOV report missing"
fi
```

**For Jest projects**:
```bash
# Run tests with coverage
npm run test:unit -- --coverage

# Verify LCOV report
if [ -f "coverage/lcov.info" ]; then
  echo "✓ LCOV report exists"
else
  echo "✗ LCOV report missing"
fi

# Verify Clover report
if [ -f "coverage/clover.xml" ]; then
  echo "✓ Clover report exists"
else
  echo "✗ Clover report missing (check jest.config for 'clover' reporter)"
fi
```

### Check Coverage Configuration

**Vitest** (vitest.config.ts):
```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html', 'lcov'], // lcov required
      reportsDirectory: './coverage'
    }
  }
});
```

**Jest** (jest.config.cjs):
```javascript
module.exports = {
  collectCoverage: true,
  coverageReporters: ['text', 'lcov', 'clover'], // both lcov and clover
  coverageDirectory: './coverage'
};
```

---

## Coverage Exclusion Patterns Explained

### Always Exclude

**Test files**: `src/**/*.spec.ts`
- **Reason**: Tests are not production code
- **Impact**: Prevents test code from inflating metrics
- **Pattern**: Matches all .spec.ts files recursively

### Conditionally Exclude (Check if exists)

**Entry point**: `src/main.ts`
- **Reason**: Bootstrap code, tested through E2E
- **Impact**: Avoids forcing unit tests for initialization
- **Check**: `[ -f "src/main.ts" ]`

**Services**: `src/services/**/*.ts`
- **Reason**: API layer, tested with mocks, not unit testable
- **Impact**: Prevents false coverage expectations
- **Check**: `[ -d "src/services" ]`

**Router**: `src/**/router/*.ts`
- **Reason**: Route configuration, tested through E2E navigation
- **Impact**: Configuration files don't need unit tests
- **Check**: `find src -type d -name "router" | head -n 1`

**Store index**: `src/store/index.ts`
- **Reason**: Vuex/Pinia store setup, configuration only
- **Impact**: Setup files are not meaningfully unit testable
- **Check**: `[ -f "src/store/index.ts" ]`

**Interfaces**: `src/**/interfaces/*.ts`
- **Reason**: TypeScript type definitions, no runtime code
- **Impact**: No executable code to test
- **Check**: `find src -type d -name "interfaces" | head -n 1`

**Constants**: `src/**/shared/constants/**/*.ts`
- **Reason**: Static data, no logic to test
- **Impact**: Constant values don't need coverage
- **Check**: `[ -d "src/shared/constants" ]`

---

## Customization Examples

### Example 3: SonarCloud Configuration

**For SonarCloud** (cloud-hosted SonarQube):
```properties
# Organization required for SonarCloud
sonar.organization=my-organization-key

sonar.projectKey=my-organization-key_my-vue-app
sonar.projectName=My Vue App
sonar.projectDescription=Vue 3 application for inventory management

# Standard configuration
sonar.sources=src
sonar.language=ts
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
sonar.qualitygate.wait=true

# Coverage
sonar.javascript.lcov.reportPaths=./coverage/lcov.info
sonar.tests=src
sonar.test.inclusions=src/**/*.spec.ts
sonar.exclusions=src/**/*.spec.ts
sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts

# Authentication (usually in CI/CD environment variable)
# sonar.login=${SONAR_TOKEN}
```

### Example 4: Branch Analysis

**For branch-specific analysis**:
```properties
# Base configuration
sonar.projectKey=my-vue-app
sonar.projectName=My Vue App
sonar.sources=src

# Branch analysis
sonar.branch.name=${BRANCH_NAME}
sonar.branch.target=main

# Rest of standard configuration...
```

### Example 5: Pull Request Decoration

**For PR analysis** (GitHub, GitLab, etc.):
```properties
# Base configuration
sonar.projectKey=my-vue-app
sonar.sources=src

# PR analysis properties
sonar.pullrequest.key=${PR_NUMBER}
sonar.pullrequest.branch=${PR_BRANCH}
sonar.pullrequest.base=${TARGET_BRANCH}

# GitHub specific
sonar.pullrequest.github.repository=owner/repo

# Rest of standard configuration...
```

### Example 6: Multiple Coverage Reports

**For projects with multiple test suites**:
```properties
# Multiple LCOV reports
sonar.javascript.lcov.reportPaths=./coverage/unit/lcov.info,./coverage/integration/lcov.info

# Multiple Clover reports (Jest)
sonar.clover.reportPaths=./coverage/unit/clover.xml,./coverage/integration/clover.xml
```

### Example 7: Extended Coverage Exclusions

**For larger projects with more exclusions**:
```properties
sonar.coverage.exclusions=\
  src/main.ts,\
  src/services/**/*.ts,\
  src/**/router/*.ts,\
  src/store/index.ts,\
  src/**/interfaces/*.ts,\
  src/**/shared/constants/**/*.ts,\
  src/**/shared/EnvConsts.ts,\
  src/**/*.d.ts,\
  src/shims-vue.d.ts
```

**Note**: Use backslash `\` for multi-line properties

---

## Common Issues and Solutions

**Issue**: Coverage reports not found by SonarQube
- **Solution**: Verify reports generated before SonarQube analysis
- **Check**: Run `npm run test:unit -- --coverage` first
- **Verify**: Confirm files exist at specified paths

**Issue**: Test files included in coverage calculations
- **Solution**: Ensure `sonar.exclusions` includes test file patterns
- **Check**: Verify pattern matches your test file naming (`.spec.ts` vs `.test.ts`)

**Issue**: Entry point (main.ts) flagged for low coverage
- **Solution**: Add to `sonar.coverage.exclusions`
- **Reason**: Bootstrap code tested through E2E, not unit tests

**Issue**: Services show 0% coverage but are tested
- **Solution**: Services tested with mocks, add to coverage exclusions
- **Alternative**: Write integration tests that run actual service code

**Issue**: Quality gate timeout in CI/CD
- **Solution**: Increase timeout or disable `sonar.qualitygate.wait`
- **Check**: SonarQube server performance and analysis queue

**Issue**: Incorrect projectKey format rejected by SonarQube
- **Solution**: Use kebab-case, no spaces, organization prefix if required
- **Format**: `org-name_project-name` or `project-name`

**Issue**: Clover report not generated (Vitest)
- **Solution**: Remove `sonar.clover.reportPaths` property
- **Reason**: Vitest doesn't support Clover format (Jest only)

**Issue**: LCOV report empty or missing coverage data
- **Solution**: Verify coverage provider configured correctly
- **Check**: Vitest `coverage.provider` or Jest `coverageProvider` setting

---

## Testing Configuration

### Validate Properties File

```bash
# Check file exists
if [ -f "sonar-project.properties" ]; then
  echo "✓ sonar-project.properties exists"
else
  echo "✗ File missing"
fi

# Check required properties
REQUIRED=("projectKey" "projectName" "sources" "language")
for prop in "${REQUIRED[@]}"; do
  if grep -q "^sonar.$prop=" sonar-project.properties; then
    echo "✓ sonar.$prop is set"
  else
    echo "✗ sonar.$prop is missing"
  fi
done
```

### Run SonarQube Analysis Locally

```bash
# Install SonarScanner (if not already installed)
# brew install sonar-scanner (macOS)
# Or download from https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Run analysis (requires SonarQube server or SonarCloud)
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN

# Or use SonarCloud
sonar-scanner \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_SONARCLOUD_TOKEN
```

### CI/CD Integration Example

**GitHub Actions**:
```yaml
- name: Run tests with coverage
  run: npm run test:unit -- --coverage

- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

---

## SonarQube Version Compatibility

### SonarQube 9.0+

**Deprecated properties** (verify in your version):
- Some older JavaScript-specific properties may be deprecated
- Check: https://docs.sonarqube.org/latest/project-administration/narrowing-the-focus/

**New features**:
- Improved TypeScript support
- Better Vue.js file handling
- Enhanced coverage reporting

### SonarCloud

**Additional requirements**:
- `sonar.organization` property required
- GitHub/GitLab/Bitbucket integration available
- PR decoration built-in

### Verify Current Documentation

```bash
# Check SonarQube version
curl -u admin:admin http://localhost:9000/api/server/version

# Or for SonarCloud
# Visit https://sonarcloud.io/account/organizations
```

---

## Important Reminders

1. **Always Review Metadata**: Update projectKey, projectName, and projectDescription
2. **Detect Test Framework**: Check package.json to determine Vitest vs Jest
3. **Verify Coverage Paths**: Ensure reports exist before running SonarQube analysis
4. **Smart Exclusions**: Only exclude files that exist in your project
5. **No Spaces in Comma Lists**: Coverage exclusions must be comma-separated without spaces
6. **Quality Gate Impact**: `wait=true` will block CI/CD if quality gate fails
7. **Coverage Philosophy**: Exclude files that aren't meaningfully unit-testable
8. **Test Files Excluded**: Always exclude test files from coverage calculations
9. **CI/CD Integration**: Run coverage generation before SonarQube analysis
10. **Version Compatibility**: Check SonarQube docs for your specific version

