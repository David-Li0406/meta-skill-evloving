# CI 集成配置

测试质量门禁的 CI/CD 配置模板。

---

## GitHub Actions

### 完整测试工作流（Node.js）

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  # 代码质量检查
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run TypeScript check
        run: npm run type-check

  # 单元测试
  unit-test:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Line coverage: $COVERAGE%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "::error::Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

      - name: Upload to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  # 集成测试
  integration-test:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [lint, unit-test]

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run database migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379

  # E2E 测试
  e2e-test:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [integration-test]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build application
        run: npm run build

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7

  # 变异测试（仅 PR）
  mutation-test:
    name: Mutation Tests
    runs-on: ubuntu-latest
    needs: [unit-test]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run mutation tests
        run: npx stryker run --incremental
        continue-on-error: true

      - name: Upload mutation report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mutation-report
          path: reports/mutation/
```

### 完整测试工作流（Python）

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install ruff mypy

      - name: Run Ruff
        run: ruff check .

      - name: Run MyPy
        run: mypy src/

  test:
    name: Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -e ".[test]"

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-fail-under=80
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.11'
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          fail_ci_if_error: true

  mutation-test:
    name: Mutation Tests
    runs-on: ubuntu-latest
    needs: [test]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -e ".[test]" mutmut

      - name: Run mutation tests
        run: |
          mutmut run --CI || true
          mutmut results

      - name: Generate HTML report
        run: mutmut html

      - name: Upload mutation report
        uses: actions/upload-artifact@v4
        with:
          name: mutation-report
          path: html/
```

---

## GitLab CI

### Node.js 项目

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - mutation

variables:
  NODE_VERSION: '20'

default:
  image: node:${NODE_VERSION}
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

before_script:
  - npm ci

lint:
  stage: lint
  script:
    - npm run lint
    - npm run type-check

unit-test:
  stage: test
  script:
    - npm run test:unit -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

integration-test:
  stage: test
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    POSTGRES_DB: test
    DATABASE_URL: postgresql://test:test@postgres:5432/test
    REDIS_URL: redis://redis:6379
  script:
    - npm run db:migrate
    - npm run test:integration
  needs:
    - lint
    - unit-test

mutation-test:
  stage: mutation
  script:
    - npx stryker run
  artifacts:
    paths:
      - reports/mutation/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: true
```

### Python 项目

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - mutation

variables:
  PYTHON_VERSION: '3.11'
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

default:
  image: python:${PYTHON_VERSION}
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .pip-cache/
      - .venv/

before_script:
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install -e ".[test]"

lint:
  stage: lint
  script:
    - pip install ruff mypy
    - ruff check .
    - mypy src/

test:
  stage: test
  services:
    - postgres:15
  variables:
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    POSTGRES_DB: test
    DATABASE_URL: postgresql://test:test@postgres:5432/test
  script:
    - pytest --cov=src --cov-report=xml --cov-report=term --cov-fail-under=80
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

mutation-test:
  stage: mutation
  script:
    - pip install mutmut
    - mutmut run --CI || true
    - mutmut html
  artifacts:
    paths:
      - html/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: true
```

---

## 质量门禁配置

### 覆盖率门禁

```yaml
# GitHub Actions - 覆盖率检查
- name: Check coverage threshold
  run: |
    # 从 coverage-summary.json 提取覆盖率
    LINES=$(jq '.total.lines.pct' coverage/coverage-summary.json)
    BRANCHES=$(jq '.total.branches.pct' coverage/coverage-summary.json)
    FUNCTIONS=$(jq '.total.functions.pct' coverage/coverage-summary.json)

    echo "Line coverage: $LINES%"
    echo "Branch coverage: $BRANCHES%"
    echo "Function coverage: $FUNCTIONS%"

    # 检查阈值
    THRESHOLD=80

    FAILED=0
    if (( $(echo "$LINES < $THRESHOLD" | bc -l) )); then
      echo "::error::Line coverage $LINES% < $THRESHOLD%"
      FAILED=1
    fi
    if (( $(echo "$BRANCHES < $THRESHOLD" | bc -l) )); then
      echo "::error::Branch coverage $BRANCHES% < $THRESHOLD%"
      FAILED=1
    fi

    exit $FAILED
```

### 断言质量检查

```yaml
# 检查测试文件中是否有无断言的测试
- name: Check assertion quality
  run: |
    # 查找可能没有断言的测试
    echo "Checking for tests without assertions..."

    # 查找 test/it 块但没有 expect/assert 的文件
    ISSUES=$(grep -r -l "it\s*(" tests/ --include="*.ts" --include="*.js" | while read file; do
      # 简单检查：文件中 it 的数量 vs expect 的数量
      IT_COUNT=$(grep -c "it\s*(" "$file" || echo 0)
      EXPECT_COUNT=$(grep -c "expect\s*(" "$file" || echo 0)

      if [ "$IT_COUNT" -gt "$EXPECT_COUNT" ]; then
        echo "$file: $IT_COUNT tests, only $EXPECT_COUNT expects"
      fi
    done)

    if [ -n "$ISSUES" ]; then
      echo "::warning::Potential tests without assertions:"
      echo "$ISSUES"
    fi
```

### PR 测试摘要

```yaml
# 在 PR 中添加测试摘要
- name: Create test summary
  if: always() && github.event_name == 'pull_request'
  run: |
    echo "## Test Results" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY

    # 覆盖率
    LINES=$(jq '.total.lines.pct' coverage/coverage-summary.json)
    BRANCHES=$(jq '.total.branches.pct' coverage/coverage-summary.json)

    echo "### Coverage" >> $GITHUB_STEP_SUMMARY
    echo "| Metric | Value | Threshold |" >> $GITHUB_STEP_SUMMARY
    echo "|--------|-------|-----------|" >> $GITHUB_STEP_SUMMARY
    echo "| Lines | ${LINES}% | 80% |" >> $GITHUB_STEP_SUMMARY
    echo "| Branches | ${BRANCHES}% | 80% |" >> $GITHUB_STEP_SUMMARY

    # 测试结果
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "### Test Suites" >> $GITHUB_STEP_SUMMARY
    echo "- Unit tests: ✅ Passed" >> $GITHUB_STEP_SUMMARY
    echo "- Integration tests: ✅ Passed" >> $GITHUB_STEP_SUMMARY
```

---

## 缓存优化

### Node.js 缓存

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache Playwright browsers
  uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/package-lock.json') }}
```

### Python 缓存

```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt', '**/pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache pytest
  uses: actions/cache@v4
  with:
    path: .pytest_cache
    key: ${{ runner.os }}-pytest-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-pytest-
```

---

## 并行测试

### Jest 并行

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - name: Run tests (shard ${{ matrix.shard }}/4)
        run: npm test -- --shard=${{ matrix.shard }}/4
```

### pytest 并行

```yaml
jobs:
  test:
    strategy:
      matrix:
        group: [1, 2, 3, 4]
    steps:
      - name: Run tests (group ${{ matrix.group }}/4)
        run: |
          pytest --splits 4 --group ${{ matrix.group }}
```

---

## 通知配置

### Slack 通知

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "❌ Tests failed on ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Test Failure*\n• Repository: ${{ github.repository }}\n• Branch: ${{ github.ref_name }}\n• Commit: ${{ github.sha }}\n• <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Run>"
            }
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Discord 通知

```yaml
- name: Notify Discord on failure
  if: failure()
  uses: sarisia/actions-status-discord@v1
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}
    title: "Test Failed"
    description: "Tests failed on ${{ github.repository }}"
```

---

## 最佳实践清单

```yaml
# 推荐的工作流结构
# 1. 快速失败：lint 和类型检查放在最前面
# 2. 依赖关系：集成测试依赖单元测试通过
# 3. 并行执行：无依赖的任务并行运行
# 4. 缓存利用：缓存依赖加速构建
# 5. 增量测试：变异测试使用增量模式
# 6. 清晰报告：生成易读的测试摘要
# 7. 适时通知：只在失败时通知

jobs:
  # Stage 1: 快速检查（并行）
  lint:        # ~30s
  type-check:  # ~30s

  # Stage 2: 单元测试（依赖 Stage 1）
  unit-test:   # ~2min
    needs: [lint, type-check]

  # Stage 3: 集成测试（依赖 Stage 2）
  integration-test:  # ~5min
    needs: [unit-test]

  # Stage 4: E2E 测试（依赖 Stage 3）
  e2e-test:    # ~10min
    needs: [integration-test]

  # 可选：变异测试（仅 PR，可失败）
  mutation-test:
    needs: [unit-test]
    if: github.event_name == 'pull_request'
    continue-on-error: true
```
