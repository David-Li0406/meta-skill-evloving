# Tests

Automated tests for the Multi-Repo Workspace skill.

## Running Tests

### Install Dependencies

```bash
cd tests
npm install
```

### Run All Tests

```bash
npm test
```

### Run Tests in Watch Mode

```bash
npm run test:watch
```

### Run Tests with Coverage

```bash
npm run test:coverage
```

## Test Suites

### Configuration Files Tests

Verifies that all core skill files exist and contain required content:
- `skill.md`
- `custom-instructions.md`
- `prompt.md`

### Templates Tests

Validates template files:
- `.claude/config.json` template is valid JSON
- `.claude/context.md` template exists
- `.workspace/config.json` template is valid JSON

### Examples Tests

Validates example configurations:
- Monorepo example
- Microservices example
- Fullstack example

### Documentation Tests

Verifies documentation files exist:
- `setup-guide.md`
- `commands.md`
- `best-practices.md`

### Scripts Tests

Verifies utility scripts exist:
- `auto-generate-config.js`
- `validate-workspace.js`

### Skill Commands Tests

Validates skill content:
- All commands are documented
- Repository types are defined
- Configuration structure is explained

## Adding New Tests

Create a new test file or add to existing:

```javascript
describe('New Feature', () => {
  test('should do something', () => {
    // Test implementation
    expect(true).toBe(true);
  });
});
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test Skill

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd skills/multi-repo-workspace/tests && npm install
      - name: Run tests
        run: cd skills/multi-repo-workspace/tests && npm test
```

## Coverage Goals

Target coverage: 80%+

Current coverage areas:
- Configuration file validation
- Template structure
- Example configurations
- Documentation completeness
- Script existence

## Future Tests

Planned test additions:
- Script functionality tests
- Configuration validation logic
- Dependency graph generation
- Repository type detection
- Command parsing and execution
