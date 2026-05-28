# Docker Specialist - Validations

## Using :latest Tag

### **Id**
latest-tag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - FROM.*:latest
  - image:.*:latest
  - FROM.*:$
### **Message**
Using :latest tag breaks reproducibility.
### **Fix Action**
Pin to specific version (e.g., node:20.10.0-alpine)
### **Applies To**
  - **/Dockerfile*
  - **/docker-compose*.yml
  - **/docker-compose*.yaml

## Running as Root User

### **Id**
running-as-root
### **Severity**
error
### **Type**
regex
### **Pattern**
  - USER root
  - Dockerfile(?!.*USER [^r])
### **Message**
Container running as root is security risk.
### **Fix Action**
Add non-root user and USER directive
### **Applies To**
  - **/Dockerfile*

## Secrets in Dockerfile

### **Id**
secrets-in-dockerfile
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ARG.*KEY
  - ARG.*SECRET
  - ARG.*PASSWORD
  - ARG.*TOKEN
  - ENV.*=.*password
### **Message**
Secrets in Dockerfile are visible in image layers.
### **Fix Action**
Use Docker secrets or runtime environment variables
### **Applies To**
  - **/Dockerfile*

## Missing HEALTHCHECK

### **Id**
no-healthcheck
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Dockerfile(?!.*HEALTHCHECK)
### **Message**
No HEALTHCHECK - dead containers appear healthy.
### **Fix Action**
Add HEALTHCHECK instruction
### **Applies To**
  - **/Dockerfile*

## COPY Before Package Install

### **Id**
cache-busting-copy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - COPY \. \.\s*\n.*RUN.*install
  - COPY.*\n.*npm install
  - COPY.*\n.*pip install
### **Message**
COPY all files before install busts cache on every change.
### **Fix Action**
Copy package files first, install, then copy source
### **Applies To**
  - **/Dockerfile*

## Missing .dockerignore

### **Id**
no-ignore-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Dockerfile
### **Message**
.dockerignore file recommended to reduce context size.
### **Fix Action**
Create .dockerignore with node_modules, .git, etc.
### **Applies To**
  - **/Dockerfile*

## Using ADD Instead of COPY

### **Id**
add-instead-of-copy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ADD(?!.*http)
### **Message**
ADD has extra features. Use COPY for local files.
### **Fix Action**
Use COPY unless you need ADD's URL/tar features
### **Applies To**
  - **/Dockerfile*

## No Init Process

### **Id**
no-signal-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CMD \[(?!.*tini)(?!.*dumb-init)
  - ENTRYPOINT \[(?!.*tini)(?!.*dumb-init)
### **Message**
No init process may cause zombie processes.
### **Fix Action**
Use tini or dumb-init as entrypoint
### **Applies To**
  - **/Dockerfile*

## Privileged Container

### **Id**
privileged-container
### **Severity**
error
### **Type**
regex
### **Pattern**
  - privileged.*true
  - --privileged
### **Message**
Privileged mode gives full host access - security risk.
### **Fix Action**
Remove privileged mode, use specific capabilities
### **Applies To**
  - **/docker-compose*.yml
  - **/docker-compose*.yaml
  - **/*.sh

## Hardcoded Host Port

### **Id**
hardcoded-port
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ports:.*"[0-9]+:[0-9]+"
### **Message**
Hardcoded host port may conflict in different environments.
### **Fix Action**
Use environment variables for ports
### **Applies To**
  - **/docker-compose*.yml
  - **/docker-compose*.yaml

## Missing Restart Policy

### **Id**
no-restart-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - services:(?!.*restart)
### **Message**
No restart policy - containers won't recover from crashes.
### **Fix Action**
Add restart: unless-stopped or restart: always
### **Applies To**
  - **/docker-compose*.yml
  - **/docker-compose*.yaml