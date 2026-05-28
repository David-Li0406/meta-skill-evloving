# CI Setup Process

This reference explains the step-by-step process of setting up a Frappe bench environment in CI, from system dependencies through site installation.

## Overview

The CI setup process follows these stages:

1. **System Dependencies** - Install required system packages
2. **Python and Node Setup** - Configure language runtimes
3. **Bench Installation** - Install frappe-bench via pip
4. **Bench Initialization** - Create bench directory and clone Frappe
5. **Requirements Installation** - Install Python and Node dependencies
6. **Database Setup** - Create test database and user
7. **Site Creation** - Create test site directory and config
8. **Process Configuration** - Modify Procfile for CI environment
9. **Bench Start** - Start bench processes in background
10. **Site Installation** - Install Frappe and apps on test site

## Stage 1: System Dependencies

### What Gets Installed

```bash
sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client
```

### Package Purposes

- **libcups2-dev**: Required for PDF generation
- **redis-server**: Background job processing and caching
- **mariadb-client**: MySQL/MariaDB command-line tools

### wkhtmltopdf Installation

PDF generation requires wkhtmltopdf:

```bash
wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

This runs in background (`&`) to speed up setup.

### Why Remove mysql-server?

- GitHub Actions runners come with MySQL pre-installed
- We use containerized MariaDB/PostgreSQL services instead
- Removing prevents port conflicts

## Stage 2: Python and Node Setup

### Python Setup

Done in workflow with `actions/setup-python`:

```yaml
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: "3.10"
```

### Node.js Setup

Done in workflow with `actions/setup-node`:

```yaml
- uses: actions/setup-node@v3
  with:
    node-version: 24
    check-latest: true
```

### Version Requirements

- **Python**: 3.10 or 3.11 (Frappe v14+)
- **Node.js**: 24 (recommended for all Frappe apps)
- Always use `check-latest: true` for Node to get security updates

## Stage 3: Bench Installation

### Install frappe-bench

```bash
pip install frappe-bench
```

This installs the bench CLI tool globally in the Python environment.

### Why pip instead of git?

- **Faster**: No need to clone bench repository
- **Stable**: Gets released version from PyPI
- **Simpler**: One command installation
- **Updates**: Easy to upgrade with `pip install -U frappe-bench`

## Stage 4: Bench Initialization

### Initialize Bench

```bash
cd ~ || exit
bench -v init frappe-bench --skip-assets --python "$(which python)" --frappe-path "${GITHUB_WORKSPACE}"
cd ./frappe-bench || exit
```

### Command Breakdown

- `bench -v init frappe-bench`: Create bench directory with verbose output
- `--skip-assets`: Don't build assets during init (saves time)
- `--python "$(which python)"`: Use the Python from setup-python action
- `--frappe-path "${GITHUB_WORKSPACE}"`: Use the cloned Frappe code

### What This Creates

```
~/frappe-bench/
├── apps/
│   └── frappe/          # Symlink or copy of ${GITHUB_WORKSPACE}
├── sites/
│   ├── apps.txt
│   ├── assets/
│   └── common_site_config.json
├── config/
├── logs/
├── env/                 # Python virtual environment
├── Procfile
└── sites/
```

### Why --skip-assets?

- Asset building takes several minutes
- We build assets later as a separate step
- For server tests, may build in background during site installation

## Stage 5: Requirements Installation

### Development Requirements

```bash
bench -v setup requirements --dev
```

Installs:
- All Python packages from `requirements.txt`
- Development dependencies (pytest, coverage, etc.)
- Pre-commit hooks dependencies

### UI Test Requirements

For UI tests, also install Node dependencies:

```bash
if [ "$TYPE" == "ui" ]
then
  bench -v setup requirements --node;
fi
```

Installs:
- Node packages from `package.json`
- Cypress and related testing tools

### Why Separate Node Requirements?

- Server tests don't need frontend dependencies
- Saves 2-3 minutes in CI time
- Only install what's needed for the test type

## Stage 6: Database Setup

### Create Test Site Directory

```bash
mkdir ~/frappe-bench/sites/test_site
cp "${GITHUB_WORKSPACE}/.github/helper/db/$DB.json" ~/frappe-bench/sites/test_site/site_config.json
```

This creates the site directory and copies the database configuration.

### MariaDB Database Creation

```bash
if [ "$DB" == "mariadb" ]
then
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL character_set_server = 'utf8mb4'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";

  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE DATABASE test_frappe";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE USER 'test_frappe'@'localhost' IDENTIFIED BY 'test_frappe'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'localhost'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "FLUSH PRIVILEGES";
fi
```

### PostgreSQL Database Creation

```bash
if [ "$DB" == "postgres" ]
then
  echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_frappe" -U postgres;
  echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_frappe WITH PASSWORD 'test_frappe'" -U postgres;
fi
```

### Character Set Configuration

The MariaDB commands set UTF-8 encoding globally:
- **utf8mb4**: Supports all Unicode characters including emojis
- **utf8mb4_unicode_ci**: Case-insensitive collation

This is critical for proper text handling.

## Stage 7: Process Configuration

### Modify Procfile

The default Procfile includes processes not needed in CI:

```bash
sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

if [ "$TYPE" == "server" ]
then
  sed -i 's/^socketio:/# socketio:/g' Procfile
  sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile
fi

if [ "$TYPE" == "ui" ]
then
  sed -i 's/^web: bench serve/web: bench serve --with-coverage/g' Procfile
fi
```

### Why Disable These Processes?

- **watch**: File watching not needed (no live development)
- **schedule**: Scheduler not needed for tests
- **socketio**: Real-time features not needed for server tests
- **redis_socketio**: Only needed with socketio

### UI Test Coverage

For UI tests, enable coverage in the web server:
```bash
web: bench serve --with-coverage
```

This tracks which backend code is executed during UI tests.

## Stage 8: Start Bench

### Background Start

```bash
bench start &> ~/frappe-bench/bench_start.log &
```

This starts bench processes in the background:
- `&>` redirects all output to log file
- `&` runs in background so setup can continue

### What Processes Start?

With modified Procfile, only these run:
- **web**: Gunicorn web server (port 8000)
- **worker** (short, long, default): Background job workers
- **redis_cache**: Redis for caching
- **redis_queue**: Redis for job queue

### Why Background?

- Tests need bench running but setup continues
- Log file captured for debugging if tests fail
- Processes stay running for the entire test duration

## Stage 9: Site Installation

### Asset Building (Server Tests)

For server tests, start asset build in background:

```bash
if [ "$TYPE" == "server" ]
then
  CI=Yes bench build --app frappe &
  build_pid=$!
fi
```

The `CI=Yes` environment variable optimizes the build for CI.

### Reinstall Site

```bash
bench --site test_site reinstall --yes
```

This:
1. Drops any existing database tables
2. Installs Frappe on the site
3. Creates default data (DocTypes, users, etc.)
4. Sets up admin user with password from config

### Wait for Asset Build

```bash
if [ "$TYPE" == "server" ]
then
  wait $build_pid
fi
```

Waits for background asset build to complete before proceeding to tests.

### Why Reinstall?

- **Clean state**: Each test run starts fresh
- **Fast**: Faster than `new-site` since DB already exists
- **Consistent**: Ensures same starting point every time

## Stage 10: Additional Setup (UI Tests)

### Complete Setup Wizard

For UI tests, complete the setup wizard programmatically:

```bash
bench --site test_site execute frappe.utils.install.complete_setup_wizard
```

This configures:
- Company details
- Currency
- Country
- Language
- Domain settings

### Create Test User

```bash
bench --site test_site execute frappe.tests.ui_test_helpers.create_test_user
```

Creates a test user for Cypress to log in with.

## Hosts File Configuration

### Add Test Site to Hosts

```bash
echo "127.0.0.1 test_site" | sudo tee -a /etc/hosts
```

### Why This Is Needed

Frappe uses hostname-based site resolution:
- Request comes in with `Host: test_site`
- Bench looks up site by hostname
- Without hosts entry, site not found

## Complete Setup Script Example

Here's a complete `install.sh` script combining all stages:

```bash
#!/bin/bash
set -e
cd ~ || exit

echo "::group::Install Bench"
pip install frappe-bench
echo "::endgroup::"

echo "::group::Init Bench"
bench -v init frappe-bench --skip-assets --python "$(which python)" --frappe-path "${GITHUB_WORKSPACE}"
cd ./frappe-bench || exit

bench -v setup requirements --dev
if [ "$TYPE" == "ui" ]
then
  bench -v setup requirements --node;
fi
echo "::endgroup::"

echo "::group::Create Test Site"
mkdir ~/frappe-bench/sites/test_site
cp "${GITHUB_WORKSPACE}/.github/helper/db/$DB.json" ~/frappe-bench/sites/test_site/site_config.json

if [ "$DB" == "mariadb" ]
then
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL character_set_server = 'utf8mb4'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";

  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE DATABASE test_frappe";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE USER 'test_frappe'@'localhost' IDENTIFIED BY 'test_frappe'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'localhost'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "FLUSH PRIVILEGES";
fi

if [ "$DB" == "postgres" ]
then
  echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE DATABASE test_frappe" -U postgres;
  echo "travis" | psql -h 127.0.0.1 -p 5432 -c "CREATE USER test_frappe WITH PASSWORD 'test_frappe'" -U postgres;
fi
echo "::endgroup::"

echo "::group::Modify processes"
sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

if [ "$TYPE" == "server" ]
then
  sed -i 's/^socketio:/# socketio:/g' Procfile
  sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile
fi

if [ "$TYPE" == "ui" ]
then
  sed -i 's/^web: bench serve/web: bench serve --with-coverage/g' Procfile
fi
echo "::endgroup::"

bench start &> ~/frappe-bench/bench_start.log &

echo "::group::Install site"
if [ "$TYPE" == "server" ]
then
  CI=Yes bench build --app frappe &
  build_pid=$!
fi

bench --site test_site reinstall --yes

if [ "$TYPE" == "server" ]
then
  wait $build_pid
fi
echo "::endgroup::"
```

## Troubleshooting Setup

### Common Issues

#### 1. Bench Init Fails

**Error**: `bench: command not found`

**Solution**: Ensure `pip install frappe-bench` ran successfully
```bash
which bench
bench --version
```

#### 2. Database Connection Fails

**Error**: `Can't connect to MySQL server`

**Solution**: Verify service is healthy
```bash
mysqladmin ping -h 127.0.0.1 -u root -ptravis
```

#### 3. Site Installation Fails

**Error**: Database errors during `reinstall`

**Solution**: Check site_config.json has correct credentials
```bash
cat ~/frappe-bench/sites/test_site/site_config.json
```

#### 4. Assets Build Fails

**Error**: Node/yarn errors during asset build

**Solution**: Ensure Node.js setup completed
```bash
node --version
yarn --version
```

#### 5. Bench Won't Start

**Error**: Processes fail to start

**Solution**: Check Procfile modifications
```bash
cat ~/frappe-bench/Procfile
```

### Debugging Setup

Enable debug output:

```bash
set -x  # Enable debug mode
bench -v init frappe-bench ...
```

Check all logs:

```bash
cat ~/frappe-bench/bench_start.log
ls -la ~/frappe-bench/logs/
```

## Performance Optimization

### Parallel Operations

Run independent operations in parallel:

```bash
# Start these in background
install_wkhtmltopdf() {
  wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
  sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
}
install_wkhtmltopdf &

# Start asset build in background
CI=Yes bench build --app frappe &
build_pid=$!

# Continue with other setup
bench --site test_site reinstall --yes

# Wait for parallel operations
wait $build_pid
wait  # Wait for all background jobs
```

### Skip Unnecessary Steps

For server tests without frontend:
- Skip `bench build` if not testing UI
- Skip Node requirements
- Skip UI test setup commands

### Use Caching

Cache these directories between runs:
- `~/.cache/pip` - Python packages
- `yarn cache dir` - Node packages
- `~/.cache/Cypress` - Cypress binary (UI tests)

## Environment Variables

### Used in Setup

- `GITHUB_WORKSPACE`: Path to cloned repository
- `TYPE`: `server` or `ui` - determines setup variations
- `DB`: `mariadb` or `postgres` - determines database setup
- `CI`: Set to `Yes` for CI-optimized operations

### Setting in Workflow

```yaml
env:
  TYPE: server
  DB: mariadb
  NODE_ENV: production
```

## Next Steps

After setup completes:
1. Run tests (see `test-execution.md`)
2. Collect logs on failure (see `ci-patterns.md`)
3. Debug issues (see `ci-patterns.md`)
