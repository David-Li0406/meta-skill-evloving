# Docker - Validations

## No USER instruction (runs as root)

### **Id**
running-as-root
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*USER\s+\w).*$
### **Message**
Container will run as root - add USER instruction
### **Fix Action**
Add 'RUN adduser -S app' and 'USER app' before CMD
### **Applies To**
  - Dockerfile*

## Sensitive values in ARG/ENV

### **Id**
secrets-in-args
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ARG\s+(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)
  - ENV\s+\w*(PASSWORD|SECRET|KEY|TOKEN)\s*=
### **Message**
Secrets in build args/env are visible in image layers
### **Fix Action**
Use runtime environment variables or Docker secrets
### **Applies To**
  - Dockerfile*

## Using ADD when COPY would work

### **Id**
add-instead-of-copy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ADD\s+[^h][^\s]+\s+[^\s]+
### **Message**
ADD has extra features (URL, tar extraction) - use COPY for local files
### **Fix Action**
Replace ADD with COPY unless you need URL or tar features
### **Applies To**
  - Dockerfile*

## Using :latest tag or no tag

### **Id**
latest-tag
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FROM\s+\w+:latest
  - FROM\s+\w+\s*$
### **Message**
Pin base image version for reproducible builds
### **Fix Action**
Use specific version: FROM node:20-alpine
### **Applies To**
  - Dockerfile*

## Multiple RUN commands that should be combined

### **Id**
multiple-run-commands
### **Severity**
info
### **Type**
regex
### **Pattern**
  - RUN\s+apt-get\s+update[\s\S]*RUN\s+apt-get\s+install
### **Message**
Combine RUN commands to reduce layers and cache issues
### **Fix Action**
Use: RUN apt-get update && apt-get install -y pkg
### **Applies To**
  - Dockerfile*

## apt-get without cleanup

### **Id**
apt-get-no-clean
### **Severity**
info
### **Type**
regex
### **Pattern**
  - apt-get\s+install(?![\s\S]*rm\s+-rf\s+/var/lib/apt)
### **Message**
Clean apt cache to reduce image size
### **Fix Action**
Add: && rm -rf /var/lib/apt/lists/*
### **Applies To**
  - Dockerfile*

## Missing HEALTHCHECK instruction

### **Id**
no-healthcheck
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*HEALTHCHECK).*$
### **Message**
Consider adding HEALTHCHECK for container orchestration
### **Fix Action**
Add HEALTHCHECK CMD curl -f http://localhost/ || exit 1
### **Applies To**
  - Dockerfile*

## Copying all files before installing dependencies

### **Id**
copy-before-deps
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - COPY\s+\.\s+\.[\s\S]{0,50}RUN\s+(npm|pip|go)\s+(install|ci)
### **Message**
Copy dependency files first for better cache efficiency
### **Fix Action**
COPY package*.json ./ before npm install
### **Applies To**
  - Dockerfile*

## Using deprecated version field in compose

### **Id**
compose-version-deprecated
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^version:\s*["']
### **Message**
The 'version' field is obsolete in Docker Compose v2
### **Fix Action**
Remove version field - it's ignored
### **Applies To**
  - docker-compose*.yml
  - docker-compose*.yaml
  - compose*.yml
  - compose*.yaml