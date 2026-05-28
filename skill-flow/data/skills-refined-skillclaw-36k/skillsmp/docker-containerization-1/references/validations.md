# Docker Containerization - Validations

## Using Latest Tag for Base Image

### **Id**
docker-latest-tag
### **Severity**
error
### **Type**
regex
### **Pattern**
  - FROM\s+[a-zA-Z0-9_/-]+:latest
  - FROM\s+[a-zA-Z0-9_/-]+\s*$
  - FROM\s+[a-zA-Z0-9_/-]+\s+AS
### **Message**
Base image using :latest tag or no tag. Builds become non-deterministic and rollbacks may not work.
### **Fix Action**
Pin to specific version (e.g., node:20.10.0-alpine) or use SHA digest
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Shell Form CMD or ENTRYPOINT

### **Id**
docker-shell-form-cmd
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CMD\s+[a-zA-Z]+
  - ENTRYPOINT\s+[a-zA-Z]+
  - CMD\s+"
### **Message**
Shell form CMD/ENTRYPOINT detected. Signals won't be forwarded to application, causing slow shutdowns.
### **Fix Action**
Use exec form: CMD ["node", "server.js"] or add tini/dumb-init as init process
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## No USER Directive

### **Id**
docker-running-as-root
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?<!USER\s+)FROM.*\n(?:(?!USER).*\n)*CMD
  - USER\s+root
### **Message**
Container may run as root. Container escapes become full node compromises.
### **Fix Action**
Add USER directive with non-root user before CMD
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Using ADD Instead of COPY

### **Id**
docker-add-instead-of-copy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ADD\s+(?!https?://)
  - ADD\s+\.\s+\.
### **Message**
ADD used for local files. ADD has implicit behaviors (auto-extract, URL fetch) that can be surprising.
### **Fix Action**
Use COPY for local files. Use RUN curl/wget for remote URLs.
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## apt-get update in Separate Layer

### **Id**
docker-apt-separate-layers
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - RUN\s+apt-get\s+update\s*$
  - RUN\s+apt-get\s+update\s*\n\s*RUN
### **Message**
apt-get update in separate layer. Cache invalidation causes install failures later.
### **Fix Action**
Combine apt-get update && apt-get install in single RUN command
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## No apt Cache Cleanup

### **Id**
docker-no-apt-cleanup
### **Severity**
info
### **Type**
regex
### **Pattern**
  - apt-get install(?!.*rm -rf /var/lib/apt/lists)
### **Message**
apt cache not cleaned after install. Adds unnecessary size to layer.
### **Fix Action**
Add && rm -rf /var/lib/apt/lists/* after apt-get install
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Suboptimal Layer Ordering

### **Id**
docker-copy-then-install
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - COPY\s+\.\s+\.\s*\n.*npm install
  - COPY\s+\.\s+\.\s*\n.*pip install
  - COPY\s+\.\s+\.\s*\n.*go mod download
### **Message**
COPY . . before dependency install. Any code change invalidates dependency cache.
### **Fix Action**
Copy package.json first, install dependencies, then COPY rest of code
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Hardcoded Secrets in Dockerfile

### **Id**
docker-hardcoded-secrets
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ENV\s+.*PASSWORD\s*=
  - ENV\s+.*SECRET\s*=
  - ENV\s+.*API_KEY\s*=
  - ENV\s+.*TOKEN\s*=(?!.*\$)
  - ARG\s+.*PASSWORD\s*=
### **Message**
Hardcoded secrets in Dockerfile. Visible in docker history and image layers.
### **Fix Action**
Use BuildKit secrets (--mount=type=secret) or pass at runtime via -e
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## No HEALTHCHECK Instruction

### **Id**
docker-no-healthcheck
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*HEALTHCHECK).*CMD\s+\[
### **Message**
No HEALTHCHECK defined. Orchestrators can't detect unhealthy containers.
### **Fix Action**
Add HEALTHCHECK instruction with appropriate health endpoint
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Using npm install Instead of npm ci

### **Id**
docker-npm-install-not-ci
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - npm install(?!\s+--)
  - RUN npm install\s*$
### **Message**
npm install may ignore lockfile. Use npm ci for reproducible builds.
### **Fix Action**
Use npm ci for CI/production builds (uses exact lockfile versions)
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Missing EXPOSE Instruction

### **Id**
docker-expose-without-port
### **Severity**
info
### **Type**
regex
### **Pattern**
  - CMD.*(?:server|start|run)(?!.*EXPOSE)
### **Message**
Server command without EXPOSE instruction. Port documentation missing.
### **Fix Action**
Add EXPOSE instruction to document which ports the container listens on
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Relative Path in WORKDIR

### **Id**
docker-workdir-relative
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - WORKDIR\s+(?!/)[a-zA-Z]
  - WORKDIR\s+\.
### **Message**
Relative WORKDIR path. Can cause unexpected directory locations.
### **Fix Action**
Use absolute paths in WORKDIR (e.g., WORKDIR /app)
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Copying Potentially Sensitive Files

### **Id**
docker-copy-sensitive-files
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - COPY.*\.env
  - COPY.*\.aws
  - COPY.*\.npmrc
  - COPY.*credentials
  - COPY.*\.pem
  - COPY.*\.key
### **Message**
Copying potentially sensitive files into image. Check .dockerignore.
### **Fix Action**
Add sensitive files to .dockerignore or use BuildKit secrets
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Using Ubuntu Base Image

### **Id**
docker-ubuntu-base
### **Severity**
info
### **Type**
regex
### **Pattern**
  - FROM\s+ubuntu
  - FROM\s+debian(?!.*slim)
### **Message**
Using large base image. Consider slim or alpine variants for smaller images.
### **Fix Action**
Use language-specific slim images (node:20-slim) or alpine variants
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Single Stage Build for Production

### **Id**
docker-single-stage-prod
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^FROM(?!.*AS).*\n(?:(?!FROM).*\n)*RUN.*(npm|pip|go|cargo|maven).*install
### **Message**
Single-stage build may include build tools in production image.
### **Fix Action**
Use multi-stage build to separate build dependencies from runtime
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## Using sudo in Dockerfile

### **Id**
docker-sudo-in-dockerfile
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - RUN\s+sudo
  - sudo\s+apt
  - sudo\s+yum
### **Message**
sudo used in Dockerfile. Build runs as root by default, sudo is unnecessary.
### **Fix Action**
Remove sudo - Dockerfile RUN commands execute as root unless USER is set
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## pip Without --no-cache-dir

### **Id**
docker-pip-no-cache
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pip install(?!.*--no-cache-dir)
  - pip3 install(?!.*--no-cache-dir)
### **Message**
pip without --no-cache-dir. Cache stored in layer unnecessarily.
### **Fix Action**
Add --no-cache-dir to pip install to reduce image size
### **Applies To**
  - Dockerfile*
  - *.dockerfile

## No .dockerignore File

### **Id**
dockerignore-missing
### **Severity**
warning
### **Type**
file_existence
### **Pattern**
  - !.dockerignore
### **Message**
No .dockerignore file. Entire directory including secrets may be sent to build context.
### **Fix Action**
Create .dockerignore with node_modules, .git, .env, and other unnecessary files
### **Applies To**
  - Dockerfile*

## ARG Used for Secrets

### **Id**
docker-arg-secret-usage
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ARG\s+\w*SECRET
  - ARG\s+\w*PASSWORD
  - ARG\s+\w*KEY
  - ARG\s+\w*TOKEN
### **Message**
ARG used for secrets. Values visible in docker history and image metadata.
### **Fix Action**
Use BuildKit --mount=type=secret or pass secrets at runtime
### **Applies To**
  - Dockerfile*
  - *.dockerfile