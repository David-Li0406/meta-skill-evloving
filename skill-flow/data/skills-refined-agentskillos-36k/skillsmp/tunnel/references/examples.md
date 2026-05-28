# Tunnel Examples

Practical examples for common Buddy tunnel use cases.

## Table of Contents
- [HTTP Tunnel Examples](#http-tunnel-examples)
- [TCP Tunnel Examples](#tcp-tunnel-examples)
- [TLS Tunnel Examples](#tls-tunnel-examples)
- [Configuration File Workflows](#configuration-file-workflows)
- [Common Use Cases](#common-use-cases)

## HTTP Tunnel Examples

### Basic Web Server

Expose a local web server on port 3000:

```bash
bdy tunnel http localhost:3000
```

**Output:**
```
Tunnel started: https://abc123.buddy.works → http://localhost:3000
```

Access your local server at the provided URL.

### React Development Server

Expose React app during development:

```bash
# Start React app
npm start  # Runs on localhost:3000

# In another terminal, create tunnel
bdy tunnel http localhost:3000 -n react-demo
```

Share the tunnel URL to demo your React app.

### API with Authentication

Protect API endpoint with basic auth:

```bash
bdy tunnel http localhost:8080 -n secure-api -a apiuser:secret123
```

Clients must provide credentials:
```bash
curl -u apiuser:secret123 https://abc123.buddy.works/api/data
```

### API with IP Whitelist

Restrict access to specific IP addresses:

```bash
# Single IP
bdy tunnel http localhost:3000 -w 203.0.113.45/32

# IP range
bdy tunnel http localhost:3000 -w 203.0.113.0/24

# Multiple ranges
bdy tunnel http localhost:3000 \
  -w 203.0.113.0/24 \
  -w 198.51.100.0/24
```

### Static File Server

Serve static files directly:

```bash
# Build your site
npm run build

# Serve the build directory
bdy tunnel http -s ./dist -n static-demo
```

No local server needed - Buddy serves the files.

### API with Custom Headers

Add custom headers to requests and responses:

```bash
bdy tunnel http localhost:3000 \
  --header X-API-Key:secret \
  --header X-Request-ID:generated \
  --response-header X-Frame-Options:DENY \
  --response-header X-Content-Type-Options:nosniff
```

### Logging HTTP Requests

Debug by logging all requests:

```bash
bdy tunnel http localhost:3000 -l -n debug-api
```

See request details in terminal output.

### HTTP/2 with Compression

Optimize performance with HTTP/2 and compression:

```bash
bdy tunnel http localhost:3000 -2 -c -n optimized-api
```

### User-Agent Filtering

Allow only specific browsers:

```bash
# Allow Chrome and Firefox
bdy tunnel http localhost:3000 \
  --useragent /Chrome/ /Firefox/

# Block specific user-agents
bdy tunnel http localhost:3000 \
  --useragent /^((?!bot|crawler).)*$/
```

### Regional Selection

Choose region for best performance:

```bash
# Europe (default)
bdy tunnel http localhost:3000 -r eu

# United States
bdy tunnel http localhost:3000 -r us

# Asia-Pacific
bdy tunnel http localhost:3000 -r as
```

## TCP Tunnel Examples

### PostgreSQL Database

Expose PostgreSQL for remote access:

```bash
bdy tunnel tcp localhost:5432 -n postgres-tunnel
```

**Connect from remote machine:**
```bash
psql -h abc123.buddy.works -p 12345 -U postgres -d mydb
```

Port number is provided in tunnel output.

### PostgreSQL with IP Restriction

Secure database tunnel with IP whitelist:

```bash
bdy tunnel tcp localhost:5432 \
  -n postgres-secure \
  -w 203.0.113.0/24
```

Only whitelisted IPs can connect.

### MySQL Database

Expose MySQL database:

```bash
bdy tunnel tcp localhost:3306 -n mysql-tunnel
```

**Connect from remote machine:**
```bash
mysql -h abc123.buddy.works -P 12345 -u root -p
```

### MongoDB Database

Expose MongoDB:

```bash
bdy tunnel tcp localhost:27017 -n mongo-tunnel
```

**Connect from application:**
```javascript
mongodb://abc123.buddy.works:12345/mydb
```

### Redis Cache

Expose Redis server:

```bash
bdy tunnel tcp localhost:6379 -n redis-tunnel -w your-ip/32
```

**Connect with redis-cli:**
```bash
redis-cli -h abc123.buddy.works -p 12345
```

### SSH Server

Expose SSH for remote access:

```bash
bdy tunnel tcp localhost:22 -n ssh-tunnel -w trusted-ip/32
```

**Connect via tunnel:**
```bash
ssh user@abc123.buddy.works -p 12345
```

### Game Server (Minecraft)

Expose Minecraft server:

```bash
bdy tunnel tcp localhost:25565 -n minecraft -t 3600
```

Players connect using tunnel address. Longer timeout for persistent connections.

### Custom Application

Expose any TCP service:

```bash
bdy tunnel tcp localhost:9000 -n custom-app
```

## TLS Tunnel Examples

### Basic TLS Tunnel

Expose HTTPS service:

```bash
bdy tunnel tls localhost:8443
```

### TLS with Custom Certificate

Use your own TLS certificate:

```bash
bdy tunnel tls localhost:8443 \
  -k /path/to/private-key.pem \
  -c /path/to/certificate.pem \
  -n secure-service
```

### Mutual TLS Authentication

Require client certificates:

```bash
bdy tunnel tls localhost:8443 \
  -k /path/to/server-key.pem \
  -c /path/to/server-cert.pem \
  --ca /path/to/ca-cert.pem \
  -n mtls-service
```

Clients must present valid certificates signed by the CA.

### TLS Termination at Agent

Terminate TLS at local agent:

```bash
bdy tunnel tls localhost:8443 \
  -i agent \
  -k /path/to/key.pem \
  -c /path/to/cert.pem
```

### TLS Pass-Through

No TLS termination, pass encrypted traffic directly:

```bash
bdy tunnel tls localhost:8443 -i target -n passthrough
```

Application handles TLS directly.

### TLS with IP Whitelist

Secure TLS tunnel with IP restrictions:

```bash
bdy tunnel tls localhost:8443 \
  -k /path/to/key.pem \
  -c /path/to/cert.pem \
  -w 203.0.113.0/24
```

## Configuration File Workflows

### Save Frequently Used Tunnels

**Add development API configuration:**
```bash
bdy tunnel config add http dev-api http://localhost:3000 \
  -a dev:secret \
  -t 300
```

**Add staging API configuration:**
```bash
bdy tunnel config add http staging-api https://localhost:8080 \
  -a staging:secret \
  -w office-ip/24
```

**Add database tunnel:**
```bash
bdy tunnel config add tcp dev-postgres localhost:5432 \
  -w developer-ip/32
```

### Start Saved Tunnels

```bash
# Start development API
bdy tunnel start dev-api

# Start staging API
bdy tunnel start staging-api

# Start database tunnel
bdy tunnel start dev-postgres
```

### Set Global Defaults

```bash
# Set default region
bdy tunnel config set region us

# Set default timeout
bdy tunnel config set timeout 600

# Set default whitelist
bdy tunnel config set whitelist your-office-ip/24
```

### Manage Multiple Configurations

```bash
# List all saved tunnels
bdy tunnel config get tunnels

# View specific tunnel
bdy tunnel config get tunnel dev-api

# Remove tunnel
bdy tunnel config rm tunnel old-api
```

### Export and Share Configurations

Configuration files are stored in `~/.buddy/tunnel-config.json`:

```bash
# Backup configuration
cp ~/.buddy/tunnel-config.json ~/tunnel-backup.json

# Share with team (remove sensitive data first)
cat ~/.buddy/tunnel-config.json | jq 'del(.token)' > team-tunnels.json
```

## Common Use Cases

### Webhook Testing

**Scenario:** Test Stripe webhooks during development

```bash
# Start local dev server
npm run dev  # Running on localhost:3000

# Create tunnel
bdy tunnel http localhost:3000 -n stripe-webhooks

# Output: https://abc123.buddy.works → http://localhost:3000

# Configure in Stripe Dashboard:
# Webhook URL: https://abc123.buddy.works/api/webhooks/stripe
```

Stripe sends webhooks to your local server for testing.

### Client Demo

**Scenario:** Demo work-in-progress to client

```bash
# Start application
npm start

# Create tunnel with auth
bdy tunnel http localhost:3000 -n client-demo -a demo:preview

# Share with client:
# URL: https://abc123.buddy.works
# Username: demo
# Password: preview
```

Client can view your work without deployment.

### Mobile Device Testing

**Scenario:** Test responsive design on mobile devices

```bash
# Start dev server
npm run dev

# Create tunnel
bdy tunnel http localhost:3000 -n mobile-test

# Access from mobile:
# Open https://abc123.buddy.works on phone/tablet
```

Test on real devices without complex network configuration.

### Remote Database Access

**Scenario:** Grant temporary database access to consultant

```bash
# Create tunnel with IP restriction
bdy tunnel tcp localhost:5432 \
  -n consultant-db \
  -w consultant-ip/32 \
  -t 7200

# Share connection details:
# Host: abc123.buddy.works
# Port: [provided by tunnel]
# Only consultant's IP can connect
```

### API Integration Testing

**Scenario:** Test API integration with third-party service

```bash
# Start local API
npm run api-server  # localhost:8080

# Create tunnel
bdy tunnel http localhost:8080 -n integration-test -l

# Configure third-party service to use:
# https://abc123.buddy.works/api

# Watch requests in terminal (logging enabled)
```

### Cross-Team Collaboration

**Scenario:** Share local service with backend team

```bash
# Start frontend dev server
npm run dev

# Create tunnel with team IP whitelist
bdy tunnel http localhost:3000 \
  -n team-frontend \
  -w team-office-ip/24

# Backend team can access:
# https://abc123.buddy.works
```

### Temporary File Sharing

**Scenario:** Share files without file hosting service

```bash
# Serve files directly
bdy tunnel http -s ~/Documents/project-files -n file-share -a user:pass

# Share credentials with recipient
```

### WebSocket Testing

**Scenario:** Test WebSocket connections

```bash
# Start WebSocket server
node ws-server.js  # localhost:8080

# Create tunnel with long timeout
bdy tunnel http localhost:8080 -n websocket-test -t 3600

# Test WebSocket connection:
# ws://abc123.buddy.works or wss://abc123.buddy.works
```

### OAuth Callback Testing

**Scenario:** Test OAuth flows requiring public callback URL

```bash
# Start auth server
npm run auth-server  # localhost:3000

# Create tunnel
bdy tunnel http localhost:3000 -n oauth-test

# Configure OAuth app:
# Callback URL: https://abc123.buddy.works/auth/callback
```

### Load Testing Preparation

**Scenario:** Expose local service for load testing

```bash
# Start service
npm run production-mode

# Create tunnel with high timeout
bdy tunnel http localhost:8080 \
  -n load-test \
  -t 7200 \
  --circuit-breaker 0.8
```

Circuit breaker helps prevent overload during testing.

### Multi-Service Development

**Scenario:** Expose multiple local services simultaneously

```bash
# Terminal 1: Frontend
bdy tunnel http localhost:3000 -n frontend

# Terminal 2: API
bdy tunnel http localhost:8080 -n api

# Terminal 3: Database
bdy tunnel tcp localhost:5432 -n database

# Share all three URLs with team
```

### Docker Container Exposure

**Scenario:** Expose containerized application

```bash
# Start Docker container
docker run -p 8080:80 my-app

# Create tunnel
bdy tunnel http localhost:8080 -n docker-demo

# Container accessible at public URL
```

## Tips and Best Practices

### Always Use Authentication

For sensitive services, always add authentication:
```bash
bdy tunnel http localhost:3000 -a user:secure-password
```

### Whitelist IPs When Possible

Limit access to known IPs:
```bash
bdy tunnel tcp localhost:5432 -w your-ip/32
```

### Use Named Tunnels

Name tunnels for easy identification:
```bash
bdy tunnel http localhost:3000 -n descriptive-name
```

### Set Appropriate Timeouts

Match timeout to service type:
```bash
# Short for APIs
bdy tunnel http localhost:3000 -t 60

# Long for WebSockets/persistent connections
bdy tunnel http localhost:8080 -t 3600
```

### Save Common Configurations

Save frequently used tunnels:
```bash
bdy tunnel config add http dev http://localhost:3000 -a dev:secret
bdy tunnel start dev  # Quick start
```

### Choose Optimal Region

Select region closest to users:
```bash
bdy tunnel http localhost:3000 -r eu  # For European users
```

### Enable Logging for Debugging

Use logging when troubleshooting:
```bash
bdy tunnel http localhost:3000 -l
```

### Test Binding

Ensure application binds to `0.0.0.0`:
```bash
# Good
npm start --host 0.0.0.0

# Bad (won't work with tunnel)
npm start --host 127.0.0.1
```
