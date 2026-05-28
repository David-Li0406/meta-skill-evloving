# App Development

## Create a New Frappe App

### Using new-app (Recommended)

```bash
bench new-app my_custom_app
```

Creates a new Frappe application in the `apps/` directory with boilerplate code.

**What it creates:**
- Basic app structure with modules
- `hooks.py` for app configuration
- `setup.py` for Python packaging
- Git repository (automatically initialized)
- License and README files

**Options:**
```bash
# Create app without initializing git
bench new-app my_custom_app --no-git
```

**After creating:**
1. The app is created in `apps/my_custom_app/`
2. Install it to a site: `bench --site development.localhost install-app my_custom_app`
3. Start development: `cd apps/my_custom_app`

### Using make-app (Alternative)

```bash
bench --site development.localhost make-app apps my_custom_app
```

Similar to `new-app` but requires specifying the destination directory.

**Note:** `new-app` is preferred for modern Frappe versions.

## Managing App Remotes

### View Remote URLs

```bash
bench remote-urls
```

Shows Git remote URLs for all apps in the bench.

**Example output:**
```
frappe                  https://github.com/frappe/frappe.git
erpnext                 https://github.com/frappe/erpnext.git
soldamundo              https://github.com/kehwar/frappe_soldamundo.git
tweaks                  https://github.com/kehwar/frappe_tweaks.git
```

### Change App Remote URL

```bash
# Change to your fork
cd apps/frappe
bench remote-set-url https://github.com/your-username/frappe.git

# Change back to official frappe repository
cd apps/frappe
bench remote-reset-url frappe
```

**Use cases:**
- Point to your fork for custom development
- Switch between HTTPS and SSH URLs
- Update remote after repository migration

## Branch Management

### Switch Single App to Branch

```bash
cd apps/soldamundo
git checkout main
git pull
```

Standard git workflow for single app.

### Switch Multiple Apps to Same Branch

```bash
# Switch all apps to 'develop' branch
bench switch-to-branch develop

# Switch specific apps only
bench switch-to-branch develop frappe erpnext

# Switch and run update
bench switch-to-branch develop --upgrade
```

**Flags:**
- `--upgrade`: After switching, runs `bench update` (pull, migrate, build)

**Common branches:**
- `develop` - Latest development code
- `version-15` - Specific version branch
- `main` / `master` - Stable release

### Switch to Develop (Frappe + ERPNext)

```bash
bench switch-to-develop
```

Convenience command to switch both `frappe` and `erpnext` to their develop branches.

**Equivalent to:**
```bash
bench switch-to-branch develop frappe erpnext
```

## Dependency Management

### Validate Dependencies

```bash
bench validate-dependencies
```

Checks if all required dependencies specified in `frappe-dependencies` are currently met.

**What it validates:**
- Python package versions
- Node.js package versions
- System package requirements
- Inter-app dependencies

**Use when:**
- After updating apps
- Before major version upgrades
- Troubleshooting installation issues
- Setting up new development environment

**Common issues detected:**
- Mismatched Python package versions
- Missing system dependencies
- Incompatible app versions
- Node.js version conflicts

## App Development Workflow

### Complete New App Setup

```bash
# 1. Create the app
bench new-app my_custom_app

# 2. Install to your development site
bench --site development.localhost install-app my_custom_app

# 3. Run migrations
bench --site development.localhost migrate

# 4. Enable developer mode (if not already enabled)
bench --site development.localhost set-config developer_mode 1

# 5. Clear cache
bench clear-cache

# 6. Start development server
bench start
```

### Fork and Customize Existing App

```bash
# 1. Fork the repository on GitHub

# 2. Change remote to your fork
cd apps/erpnext
bench remote-set-url https://github.com/your-username/erpnext.git

# 3. Create a custom branch
git checkout -b custom-features

# 4. Make your changes

# 5. Commit and push
git add .
git commit -m "Add custom features"
git push origin custom-features

# 6. Clear cache and rebuild
bench clear-cache
bench build
```

### Update Custom App from Upstream

```bash
# 1. Add upstream remote (if not already added)
cd apps/erpnext
git remote add upstream https://github.com/frappe/erpnext.git

# 2. Fetch upstream changes
git fetch upstream

# 3. Merge or rebase
git checkout custom-features
git rebase upstream/develop

# 4. Push to your fork
git push origin custom-features --force

# 5. Run migrations and rebuild
bench --site development.localhost migrate
bench build
```

### Testing App Before Release

```bash
# 1. Validate dependencies
bench validate-dependencies

# 2. Run tests
bench --site development.localhost run-tests --app my_custom_app

# 3. Check for schema issues
bench --site development.localhost migrate --skip-failing

# 4. Build production assets
bench build --production

# 5. Check for errors
bench --site development.localhost doctor
```

## Publishing App to GitHub

### Initial Setup

```bash
# 1. Create repository on GitHub

# 2. Add remote (if created without git)
cd apps/my_custom_app
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/my_custom_app.git
git push -u origin main

# 3. Add to .gitignore
cat >> .gitignore << EOF
*.pyc
__pycache__/
.DS_Store
*.egg-info/
node_modules/
EOF
```

### Version Tagging

```bash
# Tag a release
cd apps/my_custom_app
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# List tags
git tag -l
```

## Multi-App Development

### Install Multiple Custom Apps

```bash
# Install all your custom apps
bench --site development.localhost install-app soldamundo
bench --site development.localhost install-app tweaks
bench --site development.localhost install-app custom_reports

# Run migrations for all
bench --site development.localhost migrate
```

### Update All Apps

```bash
# Update all apps to latest on current branch
bench update --pull

# Update and run patches
bench update --pull --patch

# Full update with build
bench update
```

## Troubleshooting

### App Not Found After Creation

```bash
# Ensure app is in apps.txt
cat sites/apps.txt

# If missing, add manually
echo "my_custom_app" >> sites/apps.txt

# Reinstall
bench --site development.localhost install-app my_custom_app
```

### Remote URL Issues

```bash
# Check current remotes
cd apps/my_app
git remote -v

# Fix remote URL
bench remote-set-url https://correct-url.git

# Or use git directly
git remote set-url origin https://correct-url.git
```

### Branch Switching Conflicts

```bash
# Stash changes before switching
cd apps/frappe
git stash
bench switch-to-branch develop
git stash pop

# Or discard changes
git reset --hard
bench switch-to-branch develop
```

### Dependency Conflicts

```bash
# Validate and see what's wrong
bench validate-dependencies

# Update Python packages
bench pip install -U -r apps/frappe/requirements.txt

# Rebuild virtual environment
bench migrate-env python3.11
```
