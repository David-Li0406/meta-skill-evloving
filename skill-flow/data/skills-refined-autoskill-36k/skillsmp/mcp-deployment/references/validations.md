# Mcp Deployment - Validations

## Missing Dockerfile

### **Id**
mcp-no-dockerfile
### **Severity**
warning
### **Type**
regex
### **Pattern**
setRequestHandler
### **Negative Pattern**
Dockerfile|docker-compose|container
### **Message**
MCP server without containerization. Docker is recommended for production.
### **Fix Action**
Create Dockerfile for consistent deployment
### **Applies To**
  - *.ts
  - *.js

## Hardcoded Port

### **Id**
mcp-hardcoded-port
### **Severity**
info
### **Type**
regex
### **Pattern**
listen\s*\(\s*\d{4}
### **Message**
Hardcoded port. Use environment variable for flexibility.
### **Fix Action**
Use process.env.PORT || 3000
### **Applies To**
  - *.ts
  - *.js

## Missing Health Check

### **Id**
mcp-no-health-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
express\(\)|createServer|new Server
### **Negative Pattern**
/health|healthcheck|readiness
### **Message**
No health check endpoint. Required for container orchestration.
### **Fix Action**
Add GET /health endpoint that returns 200 when ready
### **Applies To**
  - *.ts
  - *.js

## Missing Graceful Shutdown

### **Id**
mcp-no-graceful-shutdown
### **Severity**
warning
### **Type**
regex
### **Pattern**
listen\s*\(|createServer
### **Negative Pattern**
SIGTERM|SIGINT|graceful|shutdown
### **Message**
No graceful shutdown handling. Connections may drop on restart.
### **Fix Action**
Handle SIGTERM/SIGINT for graceful connection draining
### **Applies To**
  - *.ts
  - *.js

## Secrets in Dockerfile

### **Id**
mcp-secrets-in-dockerfile
### **Severity**
critical
### **Type**
regex
### **Pattern**
ENV\s+(?:API_KEY|SECRET|PASSWORD|TOKEN)\s*=|COPY.*\.env
### **Message**
Secrets may be baked into container image. Security vulnerability.
### **Fix Action**
Use runtime environment variables or secret managers
### **Applies To**
  - Dockerfile
  - *.dockerfile

## Missing Resource Limits

### **Id**
mcp-no-resource-limits
### **Severity**
info
### **Type**
regex
### **Pattern**
image:|container_name:
### **Negative Pattern**
mem_limit|memory|cpu|resources
### **Message**
Container without resource limits. May consume unlimited resources.
### **Fix Action**
Set memory and CPU limits in docker-compose or Kubernetes
### **Applies To**
  - docker-compose*.yml
  - docker-compose*.yaml