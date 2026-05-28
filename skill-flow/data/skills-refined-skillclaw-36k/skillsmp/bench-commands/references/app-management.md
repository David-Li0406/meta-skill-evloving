# App Management

## Install Apps to Site

```bash
# Install single app
bench --site development.localhost install-app soldamundo

# Install multiple apps at once
bench --site development.localhost install-app soldamundo tweaks
```

Installs one or more Frappe apps to the specified site.

**Important:** Always run migrations after installing apps:
```bash
bench --site development.localhost migrate
```

## Uninstall Apps from Site

```bash
# Uninstall without backup (faster for development)
bench --site development.localhost uninstall-app tweaks --yes --no-backup

# Uninstall with confirmation and backup
bench --site development.localhost uninstall-app tweaks
```

**Flags:**
- `--yes`: Skip confirmation prompt
- `--no-backup`: Don't create backup before uninstalling (recommended for development)

## Get New App from Repository

```bash
# Clone app from GitHub
bench get-app https://github.com/kehwar/frappe_soldamundo.git
bench get-app https://github.com/kehwar/frappe_tweaks.git

# Clone from specific branch
bench get-app https://github.com/kehwar/frappe_soldamundo.git --branch develop
```

Downloads an app's code from a Git repository and adds it to the bench's apps directory.

**Note:** After getting an app, you still need to install it to your site using `install-app`.

## Complete App Installation Workflow

```bash
# 1. Get the app code
bench get-app https://github.com/user/app-name.git

# 2. Install to site
bench --site development.localhost install-app app-name

# 3. Run migrations
bench --site development.localhost migrate

# 4. Clear cache and rebuild
bench clear-cache
bench build
```
