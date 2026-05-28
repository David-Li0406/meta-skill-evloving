# Helper Scripts

This reference provides templates and explanations for CI helper scripts used in Frappe app testing.

## Script Organization

### Recommended Structure

```
.github/
├── helper/          # or helpers/ (some apps use plural)
│   ├── install.sh                 # Bench setup and site installation
│   ├── site_config.json           # OR site_config_mariadb.json
│   └── site_config_postgres.json  # (if supporting multiple databases)
└── workflows/
    └── server-tests.yml
```

**Note**: Official apps vary in directory naming:
- ERPNext, CRM: `.github/helper/`
- Helpdesk: `.github/helpers/` (plural)

## install_dependencies.sh

Installs system-level dependencies required for Frappe. Note that some official apps integrate this into `install.sh` instead of a separate file.

### Complete Script

```bash
#!/bin/bash
set -e

echo "Setting Up System Dependencies..."

sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client libmariadb-dev

install_wkhtmltopdf() {
  wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
  sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
}
install_wkhtmltopdf &
```

### Alternative wkhtmltopdf Installation (tar.xz method)

Some official apps (Helpdesk, CRM) use this method:

```bash
install_whktml() {
    wget -O /tmp/wkhtmltox.tar.xz https://github.com/frappe/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
    sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
    sudo chmod o+x /usr/local/bin/wkhtmltopdf
}
install_whktml &
```

### What This Does

1. **Updates package lists**: `sudo apt update`
2. **Removes conflicting MySQL**: Prevents port conflicts with containerized database
3. **Installs essential packages**:
   - `libcups2-dev`: CUPS library for PDF generation
   - `redis-server`: Redis for caching and background jobs
   - `mariadb-client`: MySQL/MariaDB command-line client
   - `libmariadb-dev`: MariaDB development libraries (required for some Python packages)
   - `libcups2-dev`: CUPS library for PDF generation
   - `redis-server`: Redis for caching and background jobs
   - `mariadb-client`: MySQL/MariaDB command-line client
4. **Installs wkhtmltopdf**: PDF rendering engine (runs in background for speed)

### Customizing for Your App

Add app-specific dependencies:

```bash
#!/bin/bash
set -e

echo "Setting Up System Dependencies..."

echo "::group::apt packages"
sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client

# Your app-specific packages
sudo apt install imagemagick  # For image processing
sudo apt install ffmpeg        # For video processing
sudo apt install fonts-liberation  # Additional fonts

install_wkhtmltopdf() {
  wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
  sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
}
install_wkhtmltopdf &
echo "::endgroup::"
```

### Alternative wkhtmltopdf Versions

For different Ubuntu versions:

```bash
# Ubuntu 22.04 (Jammy)
wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Ubuntu 20.04 (Focal)
wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
```

## install.sh

Sets up bench, creates test site, and installs Frappe.

### Complete Script

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

### Script Parameters

The script uses environment variables:
- `GITHUB_WORKSPACE`: Path to cloned repository (automatically set by GitHub Actions)
- `TYPE`: Either `server` or `ui` (set in workflow)
- `DB`: Either `mariadb` or `postgres` (set in workflow)

### Customizing for Your App

#### Testing Your Own App

If testing a custom app (not Frappe itself):

```bash
#!/bin/bash
set -e
cd ~ || exit

echo "::group::Install Bench"
pip install frappe-bench
echo "::endgroup::"

echo "::group::Init Bench"
# Use the version of Frappe you want to test against
bench -v init frappe-bench --skip-assets --python "$(which python)" --frappe-branch version-14
cd ./frappe-bench || exit

bench -v setup requirements --dev
echo "::endgroup::"

echo "::group::Get Your App"
# Get your app from repository
bench get-app ${GITHUB_WORKSPACE}
echo "::endgroup::"

echo "::group::Create Test Site"
mkdir ~/frappe-bench/sites/test_site
cp "${GITHUB_WORKSPACE}/.github/helper/db/$DB.json" ~/frappe-bench/sites/test_site/site_config.json

# Database setup (same as above)
if [ "$DB" == "mariadb" ]
then
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL character_set_server = 'utf8mb4'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE DATABASE test_frappe";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "CREATE USER 'test_frappe'@'localhost' IDENTIFIED BY 'test_frappe'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'localhost'";
  mariadb --host 127.0.0.1 --port 3306 -u root -ptravis -e "FLUSH PRIVILEGES";
fi
echo "::endgroup::"

echo "::group::Modify processes"
sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile
sed -i 's/^socketio:/# socketio:/g' Procfile
sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile
echo "::endgroup::"

bench start &> ~/frappe-bench/bench_start.log &

echo "::group::Install site"
bench --site test_site reinstall --yes
bench --site test_site install-app your_app_name
echo "::endgroup::"
```

#### Installing Dependent Apps

If your app depends on ERPNext or other apps:

```bash
echo "::group::Install Dependencies"
# Get ERPNext
bench get-app erpnext --branch version-14

# Get other dependencies
bench get-app https://github.com/some-org/some-app.git --branch main
echo "::endgroup::"

echo "::group::Install site"
bench --site test_site reinstall --yes

# Install apps in order
bench --site test_site install-app erpnext
bench --site test_site install-app some_app
bench --site test_site install-app your_app_name
echo "::endgroup::"
```

## Database Configuration Files

### mariadb.json

Place in `.github/helper/db/mariadb.json`:

```json
{
    "db_host": "127.0.0.1",
    "db_port": 3306,
    "db_name": "test_frappe",
    "db_password": "test_frappe",
    "allow_tests": true,
    "db_type": "mariadb",
    "auto_email_id": "test@example.com",
    "mail_server": "localhost",
    "mail_port": 2525,
    "mail_login": "test@example.com",
    "mail_password": "test",
    "admin_password": "admin",
    "root_login": "root",
    "root_password": "travis",
    "host_name": "http://test_site:8000",
    "monitor": 1,
    "server_script_enabled": true
}
```

### postgres.json

Place in `.github/helper/db/postgres.json`:

```json
{
    "db_host": "127.0.0.1",
    "db_port": 5432,
    "db_name": "test_frappe",
    "db_password": "test_frappe",
    "db_type": "postgres",
    "allow_tests": true,
    "auto_email_id": "test@example.com",
    "mail_server": "localhost",
    "mail_port": 2525,
    "mail_login": "test@example.com",
    "mail_password": "test",
    "admin_password": "admin",
    "root_login": "postgres",
    "root_password": "travis",
    "host_name": "http://test_site:8000",
    "server_script_enabled": true
}
```

## Script Best Practices

### Error Handling

Always use `set -e`:

```bash
#!/bin/bash
set -e  # Exit immediately if any command fails

# Your commands here
```

### Verbose Output

Use GitHub Actions log groups:

```bash
echo "::group::Stage Name"
# Commands for this stage
echo "::endgroup::"
```

This creates collapsible sections in the workflow logs.

### Working Directory

Explicitly change to expected directory:

```bash
cd ~ || exit  # Go to home directory or exit if it fails
cd ./frappe-bench || exit  # Go to bench or exit if it doesn't exist
```

### Background Processes

For long-running tasks that can run in parallel:

```bash
# Start in background
slow_command &
background_pid=$!

# Do other work
fast_command

# Wait for background task
wait $background_pid
```

### Conditional Execution

Use environment variables for different test types:

```bash
if [ "$TYPE" == "ui" ]
then
  # UI-specific setup
  bench -v setup requirements --node
fi

if [ "$TYPE" == "server" ]
then
  # Server-specific setup
  sed -i 's/^socketio:/# socketio:/g' Procfile
fi
```

## Debugging Scripts

### Add Debug Output

```bash
#!/bin/bash
set -ex  # -x prints each command before executing

# Rest of script
```

### Print Environment

```bash
echo "::group::Environment Info"
echo "GITHUB_WORKSPACE: ${GITHUB_WORKSPACE}"
echo "TYPE: ${TYPE}"
echo "DB: ${DB}"
echo "Python: $(which python)"
echo "Python version: $(python --version)"
echo "Node: $(which node)"
echo "Node version: $(node --version)"
echo "::endgroup::"
```

### Check Each Stage

Add verification after each stage:

```bash
echo "::group::Install Bench"
pip install frappe-bench
which bench  # Verify bench is in PATH
bench --version  # Verify bench works
echo "::endgroup::"
```

## Common Script Issues

### Issue: bench Not Found

**Cause**: PATH not updated after pip install

**Solution**: Use full path or refresh PATH
```bash
pip install frappe-bench
export PATH="$HOME/.local/bin:$PATH"
bench --version
```

### Issue: Database Connection Failed

**Cause**: Service not ready when script runs

**Solution**: Add retry logic
```bash
# Wait for MariaDB to be ready
for i in {1..30}; do
  if mysqladmin ping -h 127.0.0.1 -u root -ptravis &> /dev/null; then
    echo "MariaDB is ready"
    break
  fi
  echo "Waiting for MariaDB..."
  sleep 1
done
```

### Issue: Permissions Error

**Cause**: Trying to write to protected directory

**Solution**: Use home directory or temp directory
```bash
cd ~ || exit  # Use home directory
mkdir -p ~/frappe-bench  # Create in home
```

### Issue: Site Config Not Found

**Cause**: Path to DB config file incorrect

**Solution**: Verify path exists
```bash
if [ ! -f "${GITHUB_WORKSPACE}/.github/helper/db/$DB.json" ]; then
  echo "Error: Config file not found"
  ls -la "${GITHUB_WORKSPACE}/.github/helper/db/"
  exit 1
fi
```

## Running Scripts in Workflow

### Execution in Workflow

```yaml
- name: Install Dependencies
  run: |
    bash ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
    bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
  env:
    TYPE: server
    DB: mariadb
```

### Making Scripts Executable

Scripts don't need to be executable in git (bash is called explicitly).

If you want to make them executable:

```bash
chmod +x .github/helper/install_dependencies.sh
chmod +x .github/helper/install.sh
git add .github/helper/*.sh
git commit -m "Make scripts executable"
```

Then call without bash:

```yaml
- name: Install Dependencies
  run: |
    ${GITHUB_WORKSPACE}/.github/helper/install_dependencies.sh
    ${GITHUB_WORKSPACE}/.github/helper/install.sh
```

## Alternative: Inline Scripts

For simpler setups, you can skip helper scripts and use inline commands:

```yaml
- name: Setup Bench
  run: |
    cd ~
    pip install frappe-bench
    bench init frappe-bench --skip-assets --python "$(which python)" --frappe-branch version-14
    cd frappe-bench
    bench setup requirements --dev
  env:
    DB: mariadb

- name: Create Site
  run: |
    cd ~/frappe-bench
    bench new-site test_site --db-root-password travis --admin-password admin
    bench --site test_site install-app your_app_name
```

This approach is simpler but less reusable across workflows.

## Testing Scripts Locally

Before committing, test scripts locally:

```bash
# Set environment variables
export GITHUB_WORKSPACE=$(pwd)
export TYPE=server
export DB=mariadb

# Run scripts
bash .github/helper/install_dependencies.sh
bash .github/helper/install.sh
```

Note: This requires Docker services or local database installed.
