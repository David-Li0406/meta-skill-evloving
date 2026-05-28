# Gcp Cloud Run - Validations

## Hardcoded GCP Credentials

### **Id**
hardcoded-gcp-credentials
### **Severity**
error
### **Description**
GCP credentials must never be hardcoded in source code
### **Pattern**
  ("type":\s*"service_account"|private_key.*BEGIN.*PRIVATE|"client_email":\s*"[^"]+@[^"]+\.iam\.gserviceaccount\.com")
  
### **Message**
Hardcoded GCP service account credentials. Use Secret Manager or Workload Identity.
### **Autofix**


## GCP API Key in Source Code

### **Id**
gcp-api-key-in-code
### **Severity**
error
### **Description**
API keys should use Secret Manager
### **Pattern**
  (AIza[0-9A-Za-z-_]{35}|[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com)
  
### **Message**
Hardcoded GCP API key. Use Secret Manager.
### **Autofix**


## Credentials JSON File in Repository

### **Id**
credentials-json-in-repo
### **Severity**
error
### **Description**
Service account JSON files should not be in source control
### **Pattern**
  (credentials\.json|service[-_]?account\.json|.*-key\.json)
  
### **File Pattern**
*.json
### **Message**
Credentials file detected. Add to .gitignore and use Secret Manager.
### **Autofix**


## Running as Root User

### **Id**
dockerfile-root-user
### **Severity**
warning
### **Description**
Containers should not run as root for security
### **File Pattern**
Dockerfile*
### **Pattern**
  ^(?!.*USER\s+\d+|.*USER\s+\w+).*
  
### **Anti Pattern**
  USER\s+(\d+|[a-z]+)
  
### **Message**
Dockerfile runs as root. Add USER directive for security.
### **Autofix**


## Missing Health Check in Dockerfile

### **Id**
dockerfile-no-healthcheck
### **Severity**
info
### **Description**
Cloud Run uses HTTP health checks, Dockerfile HEALTHCHECK is optional
### **File Pattern**
Dockerfile*
### **Pattern**
  ^(?!.*HEALTHCHECK).*
  
### **Message**
No HEALTHCHECK in Dockerfile. Cloud Run uses its own health checks.
### **Autofix**


## Hardcoded Port in Application

### **Id**
hardcoded-port
### **Severity**
warning
### **Description**
Port should come from PORT environment variable
### **Pattern**
  (listen\(8080\)|\.listen\(\d+\)|port\s*=\s*\d+)
  
### **Anti Pattern**
  (PORT|process\.env\.PORT|os\.environ\.get\(['"]PORT)
  
### **Message**
Hardcoded port. Use PORT environment variable for Cloud Run.
### **Autofix**


## Large File Writes to /tmp

### **Id**
large-tmp-writes
### **Severity**
warning
### **Description**
/tmp uses container memory, large writes can cause OOM
### **Pattern**
  (\/tmp\/|tempfile\.|NamedTemporaryFile|mktemp)
  
### **Message**
/tmp writes consume memory. Consider Cloud Storage for large files.
### **Autofix**


## Synchronous File Operations

### **Id**
synchronous-file-operations
### **Severity**
warning
### **Description**
Sync file ops block the event loop in async apps
### **Pattern**
  (readFileSync|writeFileSync|appendFileSync|existsSync|readdirSync)
  
### **Message**
Synchronous file operations. Use async versions for better concurrency.
### **Autofix**


## Global Mutable State

### **Id**
global-mutable-state
### **Severity**
warning
### **Description**
Global state issues with concurrent requests
### **Pattern**
  (global\s+\w+\s*=|let\s+\w+\s*=.*(?:outside|module).*function)
  
### **Message**
Global mutable state may cause issues with concurrent requests.
### **Autofix**


## Thread-Unsafe Singleton Pattern

### **Id**
thread-unsafe-singleton
### **Severity**
warning
### **Description**
Singletons need thread safety for concurrency > 1
### **Pattern**
  (if\s+.*instance.*is\s+None|if\s+not\s+.*_instance|_instance\s*=\s*None)
  
### **Message**
Singleton pattern - ensure thread safety if using concurrency > 1.
### **Autofix**


## Database Connections Without Pool

### **Id**
connection-pool-missing
### **Severity**
warning
### **Description**
Use connection pooling for database connections
### **Pattern**
  (psycopg2\.connect|mysql\.connector\.connect|MongoClient\()
  
### **Anti Pattern**
  (pool|Pool|connection_pool|pool_size)
  
### **Message**
Database connection without pooling. Use connection pool for Cloud Run.
### **Autofix**


## Long-Lived Connections Without Keep-Alive

### **Id**
long-lived-connections
### **Severity**
info
### **Description**
VPC connections need keep-alive due to 10-min idle timeout
### **Pattern**
  (redis\.Redis\(|redis\.StrictRedis\(|create_engine\()
  
### **Anti Pattern**
  (socket_keepalive|keepalive|pool_recycle|pool_pre_ping)
  
### **Message**
Long-lived connection - consider keep-alive for VPC idle timeout.
### **Autofix**


## Missing Graceful Shutdown Handler

### **Id**
missing-graceful-shutdown
### **Severity**
info
### **Description**
Handle SIGTERM for graceful shutdown
### **Pattern**
  (app\.listen|uvicorn\.run|serve\()
  
### **Anti Pattern**
  (SIGTERM|signal\.signal|process\.on\(['"]SIGTERM|shutdown)
  
### **Message**
Consider handling SIGTERM for graceful shutdown in Cloud Run.
### **Autofix**


## Blocking Operations at Startup

### **Id**
blocking-startup
### **Severity**
warning
### **Description**
Heavy startup work delays container readiness
### **Pattern**
  (import.*time\.sleep|Thread\.sleep|await.*asyncio\.sleep)
  
### **Message**
Blocking operation at startup. Consider lazy initialization.
### **Autofix**
