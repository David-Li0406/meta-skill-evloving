---
name: sandbox
description: Deploy and test applications in Buddy Sandbox cloud environments. Use when user asks about "deploy app", "create sandbox", "test in cloud", "isolated environment", "remote environment", "run app in sandbox", or mentions deploying, testing, or running applications in cloud sandboxes.
---

# Buddy Sandbox Deployment

On-demand cloud environments for deploying and testing applications with public HTTP/TCP endpoints.

## CRITICAL: AI Agent Requirements

> **STOP: Read this section before any sandbox operation.**

### 1. Always use `--silent` with `bdy sandbox cp`

Without `--silent`, file copy floods stdout and breaks your execution:
```bash
bdy sandbox cp --silent ./src my-app:/app    # correct
bdy sandbox cp ./src my-app:/app             # WRONG - floods output
```

### 2. Commands run in background by default

Commands execute asynchronously by default. Use `--wait` to block until completion:
```bash
bdy sandbox exec command my-app "npm start"          # runs in background (default)
bdy sandbox exec command my-app "npm install" --wait # blocks until done
```

### 3. Apps must bind to `0.0.0.0`

Applications MUST bind to `0.0.0.0`, NOT `127.0.0.1` or `localhost`.

### 4. Python on Ubuntu 24.04 requires venv

PEP 668 enforced - pip install fails without venv:
```bash
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
```

### 5. Creating config files: write locally → cp

Never use heredoc through `exec command` for complex files - escaping is error-prone. Instead:
```bash
# 1. Write file locally (content exactly as needed)
cat > /tmp/config.php << 'EOF'
<?php
$cfg['blowfish_secret'] = 'your-secret-key';
$cfg['Servers'][1]['host'] = 'localhost';
EOF

# 2. Copy to sandbox (no escaping issues)
bdy sandbox cp --silent /tmp/config.php my-app:/etc/app/config.php
```

### 6. Web apps run behind reverse proxy

Apps must handle `X-Forwarded-Proto` header for correct HTTPS detection:
```php
// PHP
if ($_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') $_SERVER['HTTPS'] = 'on';
```
```js
// Express.js
app.set('trust proxy', true);
```
Without this, apps may redirect to localhost or generate incorrect URLs.

### 7. MUST READ stack-specific guides before deploying

If deploying WordPress, CMS, or multi-service stacks - you MUST read the reference guide BEFORE starting:
- **WordPress/PHP** → [references/examples/wordpress.md](references/examples/wordpress.md)
- **Node.js + DB** → [references/examples/nodejs-postgresql.md](references/examples/nodejs-postgresql.md)

These contain critical configuration (reverse proxy URLs, service setup) that WILL cause failures if skipped.

## Prerequisites

**Authentication Required:** Verify with `bdy whoami`. If fails, user must run `bdy login` in separate terminal.

## Quick Deployment Workflow

### 1. Create Sandbox

```bash
bdy sandbox create -i my-app --resources 2x4 \
  --install-command "apt-get update && apt-get install -y nodejs npm"
```

Resources: 1x2, 2x4, 4x8, 8x16, 12x24 (CPUxRAM). Default OS: Ubuntu 24.04.

### 2. Deploy Application

```bash
bdy sandbox cp --silent ./src my-app:/app
bdy sandbox exec command my-app "cd /app && npm install" --wait
bdy sandbox exec command my-app "cd /app && npm start"
```

### 3. Expose Endpoint

```bash
bdy sandbox endpoint add my-app -n web -e 3000
```

With auth: `--auth BASIC --username admin --password secret`

### 4. Check Status

```bash
bdy sandbox endpoint list my-app                   # Get public URL
bdy sandbox exec list my-app                       # List executed commands
bdy sandbox exec logs my-app <command-id>          # View command logs
```

### 5. Verify Deployment

```bash
curl -I <public-url>  # Expect 200 OK, not redirect to localhost
```
If redirects to localhost → configure reverse proxy headers (see CRITICAL #6).

## References

- [references/commands.md](references/commands.md) - Full command reference
- [references/examples.md](references/examples.md) - Simple deployment examples (Node.js, Flask)
