# Deployment Examples

## Table of Contents
- [Node.js from Git](#nodejs-from-git)
- [Python Flask from Git](#python-flask-from-git)
- [Local Files with cp](#local-files-with-cp)
- [Check Application Status](#check-application-status)

## Dedicated Examples (Multi-Service)
- **[examples/nodejs-postgresql.md](examples/nodejs-postgresql.md)** - Node.js REST API with PostgreSQL database
- **[examples/wordpress.md](examples/wordpress.md)** - WordPress + MySQL + phpMyAdmin (LAMP stack)

## Node.js from Git

```bash
# Create sandbox with Node.js
bdy sandbox create -i nodejs-app --resources 2x4 \
  --install-command "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -" \
  --install-command "apt-get install -y nodejs"

# Clone and setup
bdy sandbox exec command nodejs-app "git clone https://github.com/user/app.git /app" --wait
bdy sandbox exec command nodejs-app "cd /app && npm install" --wait

# Start server (runs in background by default)
bdy sandbox exec command nodejs-app "cd /app && npm start"

# Expose port 3000
bdy sandbox endpoint add nodejs-app -n web -e 3000
```

## Python Flask from Git

```bash
# Create sandbox
bdy sandbox create -i flask-app --resources 1x2 \
  --install-command "apt-get update && apt-get install -y python3 python3-pip python3-venv"

# Deploy
bdy sandbox exec command flask-app "git clone https://github.com/user/flask-app.git /app" --wait
bdy sandbox exec command flask-app "cd /app && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt" --wait
bdy sandbox exec command flask-app "cd /app && . venv/bin/activate && python3 app.py"

# Expose
bdy sandbox endpoint add flask-app -n api -e 5000
```

**Note:** Ubuntu 24.04 requires venv for pip packages (PEP 668).

## Local Files with cp

Recommended approach for AI agents deploying local projects:

```bash
# Create sandbox with Node.js
bdy sandbox create -i my-local-app --resources 1x2 \
  --install-command "apt-get update && apt-get install -y nodejs npm"

# Copy local project
bdy sandbox cp --silent ./my-project my-local-app:/app

# Install and start
bdy sandbox exec command my-local-app "cd /app && npm install" --wait
bdy sandbox exec command my-local-app "cd /app && npm start"

# Expose
bdy sandbox endpoint add my-local-app -n web -e 3000
```

## Check Application Status

```bash
# Get sandbox info
bdy sandbox get my-app

# List endpoints with URLs
bdy sandbox endpoint list my-app

# List executed commands
bdy sandbox exec list my-app

# View command logs (use command-id from exec list)
bdy sandbox exec logs my-app <command-id>

# Check processes
bdy sandbox exec command my-app "ps aux" --wait
```
