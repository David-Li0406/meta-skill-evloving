# Workflow Templates

This reference provides complete GitHub Actions workflow templates for Frappe applications, based on official Frappe framework patterns.

## Server Tests Workflow

Complete workflow for running server-side unit and integration tests.

### Basic Server Tests (Single Database)

```yaml
name: Server Tests

on:
  pull_request:
  workflow_dispatch:
  push:
    branches: [main, develop]

concurrency:
  group: server-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    timeout-minutes: 30

    services:
      mariadb:
        image: mariadb:10.6.24
        env:
          MARIADB_ROOT_PASSWORD: travis
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3

    steps:
      - name: Clone
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Check for valid Python & Merge Conflicts
        run: |
          python -m compileall -q -f "${GITHUB_WORKSPACE}"
          if grep -lr --exclude-dir=node_modules "^<<<<<<< " "${GITHUB_WORKSPACE}"
              then echo "Found merge conflicts"
              exit 1
          fi

      - uses: actions/setup-node@v3
        with:
          node-version: 24
          check-latest: true

      - name: Add to Hosts
        run: |
          echo "127.0.0.1 test_site" | sudo tee -a /etc/hosts

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt', '**/pyproject.toml', '**/setup.py') }}
          restore-keys: |
            ${{ runner.os }}-pip-
            ${{ runner.os }}-

      - name: Get yarn cache directory path
        id: yarn-cache-dir-path
        run: echo "dir=$(yarn cache dir)" >> $GITHUB_OUTPUT

      - uses: actions/cache@v3
        id: yarn-cache
        with:
          path: ${{ steps.yarn-cache-dir-path.outputs.dir }}
          key: ${{ runner.os }}-yarn-${{ hashFiles('**/yarn.lock') }}
          restore-keys: |
            ${{ runner.os }}-yarn-

      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install Yarn
        run: npm install -g yarn

      - name: Install Dependencies
        run: |
          bash ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
          bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
        env:
          TYPE: server
          DB: mariadb

      - name: Run Tests
        run: bench --site test_site run-parallel-tests --app your_app_name
        working-directory: /home/runner/frappe-bench

      - name: Show bench output
        if: ${{ always() }}
        run: |
          cd ~/frappe-bench
          cat bench_start.log || true
          cd logs
          for f in ./*.log*; do
            echo "Printing log: $f";
            cat $f
          done
```

### Multi-Database Matrix Tests

Test against both MariaDB and PostgreSQL:

```yaml
name: Server Tests

on:
  pull_request:
  workflow_dispatch:

concurrency:
  group: server-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    name: Unit Tests (${{ matrix.db }})
    runs-on: ubuntu-latest
    timeout-minutes: 30

    strategy:
      fail-fast: false
      matrix:
        db: [mariadb, postgres]

    services:
      mariadb:
        image: mariadb:10.6.24
        env:
          MARIADB_ROOT_PASSWORD: travis
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3

      postgres:
        image: postgres:12.4
        env:
          POSTGRES_PASSWORD: travis
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Clone
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - uses: actions/setup-node@v3
        with:
          node-version: 24
          check-latest: true

      - name: Add to Hosts
        run: echo "127.0.0.1 test_site" | sudo tee -a /etc/hosts

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt', '**/pyproject.toml', '**/setup.py') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Get yarn cache directory path
        id: yarn-cache-dir-path
        run: echo "dir=$(yarn cache dir)" >> $GITHUB_OUTPUT

      - uses: actions/cache@v3
        id: yarn-cache
        with:
          path: ${{ steps.yarn-cache-dir-path.outputs.dir }}
          key: ${{ runner.os }}-yarn-${{ hashFiles('**/yarn.lock') }}

      - name: Install Dependencies
        run: |
          bash ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
          bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
        env:
          TYPE: server
          DB: ${{ matrix.db }}

      - name: Run Tests
        run: bench --site test_site run-parallel-tests --app your_app_name
        working-directory: /home/runner/frappe-bench

      - name: Show bench output
        if: ${{ always() }}
        run: cat ~/frappe-bench/bench_start.log || true
```

## UI Tests Workflow

Complete workflow for running Cypress UI tests with parallel execution.

```yaml
name: UI Tests

on:
  pull_request:
  workflow_dispatch:

concurrency:
  group: ui-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    strategy:
      fail-fast: false
      matrix:
        # Adjust based on number of test files
        container: [1, 2, 3]

    name: UI Tests (Cypress) - ${{ matrix.container }}

    services:
      mariadb:
        image: mariadb:10.6.24
        env:
          MARIADB_ROOT_PASSWORD: travis
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3

    steps:
      - name: Clone
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - uses: actions/setup-node@v3
        with:
          node-version: 24
          check-latest: true

      - name: Add to Hosts
        run: echo "127.0.0.1 test_site" | sudo tee -a /etc/hosts

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt', '**/pyproject.toml', '**/setup.py') }}

      - name: Get yarn cache directory path
        id: yarn-cache-dir-path
        run: echo "dir=$(yarn cache dir)" >> $GITHUB_OUTPUT

      - uses: actions/cache@v3
        id: yarn-cache
        with:
          path: ${{ steps.yarn-cache-dir-path.outputs.dir }}
          key: ${{ runner.os }}-yarn-ui-${{ hashFiles('**/yarn.lock') }}

      - name: Cache cypress binary
        uses: actions/cache@v3
        with:
          path: ~/.cache/Cypress
          key: ${{ runner.os }}-cypress

      - name: Install Dependencies
        run: |
          bash ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
          bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
        env:
          TYPE: ui
          DB: mariadb

      - name: Build
        run: cd ~/frappe-bench/ && bench build --apps your_app_name

      - name: Site Setup
        run: |
          cd ~/frappe-bench/
          bench --site test_site execute frappe.utils.install.complete_setup_wizard
          bench --site test_site execute frappe.tests.ui_test_helpers.create_test_user

      - name: UI Tests
        run: cd ~/frappe-bench/ && bench --site test_site run-ui-tests your_app_name --headless --parallel --ci-build-id $GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT

      - name: Show bench output
        if: ${{ always() }}
        run: cat ~/frappe-bench/bench_start.log || true
```

## Patch Tests Workflow

Test database migrations from older versions:

```yaml
name: Patch Tests

on:
  pull_request:
  workflow_dispatch:

concurrency:
  group: patch-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    name: Patch Migration Tests
    runs-on: ubuntu-latest
    timeout-minutes: 60

    services:
      mariadb:
        image: mariadb:10.6.24
        env:
          MARIADB_ROOT_PASSWORD: travis
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=5s --health-timeout=2s --health-retries=3

    steps:
      - name: Clone
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 24
          check-latest: true

      - name: Add to Hosts
        run: echo "127.0.0.1 test_site" | sudo tee -a /etc/hosts

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt', '**/pyproject.toml', '**/setup.py') }}

      - name: Install Dependencies
        run: |
          bash ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
          pip install frappe-bench
          bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
        env:
          TYPE: server
          DB: mariadb

      - name: Run Patch Tests
        run: |
          cd ~/frappe-bench/
          sed -i 's/^worker:/# worker:/g' Procfile
          
          # Download older version database backup
          wget https://example.com/old-version-backup.sql.gz
          bench --site test_site --force restore ~/frappe-bench/old-version-backup.sql.gz

          source env/bin/activate
          cd apps/your_app_name/

          # Test migration
          bench --site test_site migrate

      - name: Show bench output
        if: ${{ always() }}
        run: cat ~/frappe-bench/bench_start.log || true
```

## Customizing Workflows for Your App

### Minimal Changes Required

1. **App Name**: Replace `your_app_name` with your app's name
2. **Repository**: Workflow runs on your repo automatically
3. **Helper Scripts**: Copy helper scripts from Frappe or create custom ones
4. **Database Config**: Copy DB config files from Frappe

### Adding Custom Dependencies

If your app needs additional system packages:

```yaml
      - name: Install App-Specific Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y your-package-name
```

If your app needs additional Python packages not in requirements.txt:

```yaml
      - name: Install Python Dependencies
        run: |
          pip install special-package
```

### Testing Against Multiple Frappe Versions

```yaml
    strategy:
      matrix:
        frappe-version: [version-14, version-15, develop]

    steps:
      # ... other steps ...
      
      - name: Install Frappe Version
        run: |
          cd ~/frappe-bench/apps/frappe
          git fetch --depth 1 origin ${{ matrix.frappe-version }}:${{ matrix.frappe-version }}
          git checkout ${{ matrix.frappe-version }}
```

### Adding Code Coverage

For server tests with coverage reporting:

```yaml
      - name: Run Tests with Coverage
        run: |
          cd ~/frappe-bench
          bench --site test_site run-parallel-tests --app your_app_name --with-coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ~/frappe-bench/apps/your_app_name/coverage.xml
          flags: server
          name: Server Tests
```

## Workflow Triggers

### Common Trigger Patterns

**On pull requests only:**
```yaml
on:
  pull_request:
```

**On pull requests and manual dispatch:**
```yaml
on:
  pull_request:
  workflow_dispatch:
```

**On PR, push to main, and schedule:**
```yaml
on:
  pull_request:
  push:
    branches: [main, develop]
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight UTC
  workflow_dispatch:
```

**On specific paths:**
```yaml
on:
  pull_request:
    paths:
      - '**.py'
      - '**.js'
      - '**/requirements.txt'
      - '.github/workflows/**'
```

## Debugging Options

### Interactive Debugging with tmate

Add this step for SSH access to the runner:

```yaml
      - name: Setup tmate session
        uses: mxschmitt/action-tmate@v3
        if: ${{ contains(github.event.pull_request.labels.*.name, 'debug-gha') }}
```

Then add the `debug-gha` label to your PR to enable.

### Detailed Logging

Always include log output steps:

```yaml
      - name: Show bench output
        if: ${{ always() }}
        run: |
          cd ~/frappe-bench
          cat bench_start.log || true
          cd logs
          for f in ./*.log*; do
            echo "Printing log: $f"
            cat $f
          done
```

## Python and Node.js Versions

### Current Recommendations

Official Frappe apps use varying Python and Node versions:

```yaml
# Modern apps (Helpdesk, CRM)
- name: Setup Python
  uses: actions/setup-python@v5  # or v6
  with:
    python-version: '3.14'

- name: Setup Node
  uses: actions/setup-node@v6
  with:
    node-version: 24
    check-latest: true

- name: Install Yarn
  run: npm install -g yarn

# Older apps (ERPNext v14 and earlier)
- name: Setup Python
  uses: actions/setup-python@v2
  with:
    python-version: '3.11'

- name: Setup Node
  uses: actions/setup-node@v2
  with:
    node-version: 24
    check-latest: true
```

### Version Guidelines

- **Python 3.10-3.11**: Frappe v14-v15
- **Python 3.14**: Latest Frappe apps (experimental/preview)
- **Node 24**: Recommended for all Frappe apps (v14+)
- **Node 18**: Legacy support (older Frappe v14 setups)
- **Always use**: `check-latest: true` for security updates

### Yarn Installation

Modern workflows explicitly install yarn globally:

```yaml
- name: Install Yarn
  run: npm install -g yarn
```

This ensures yarn is available even with newer Node versions.

### Action Versions

Use the latest stable versions for better features and security:

```yaml
# Latest versions
uses: actions/checkout@v6
uses: actions/setup-python@v6
uses: actions/setup-node@v6
uses: actions/cache@v4

# Older but still supported
uses: actions/checkout@v4
uses: actions/setup-python@v4
uses: actions/setup-node@v3
uses: actions/cache@v3
```

## Performance Optimization

### Concurrency Control

Prevent multiple runs of the same workflow:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true
```

### Timeout Settings

Set appropriate timeouts:

```yaml
jobs:
  test:
    timeout-minutes: 30  # Adjust based on your test suite
```

### Conditional Execution

Skip tests when only docs change:

```yaml
on:
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

## Multi-App Testing

If your app depends on other Frappe apps:

```yaml
      - name: Install Dependency Apps
        run: |
          cd ~/frappe-bench
          bench get-app https://github.com/frappe/erpnext.git --branch version-15
          bench --site test_site install-app erpnext
          bench get-app https://github.com/your-org/your-other-app.git
          bench --site test_site install-app your_other_app
```

Then install and test your app:

```yaml
      - name: Install and Test App
        run: |
          cd ~/frappe-bench
          bench --site test_site install-app your_app_name
          bench --site test_site run-parallel-tests --app your_app_name
```
