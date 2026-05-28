---
name: docker-build-debugger
description: Diagnoses Docker build failures for Node.js applications, identifies common patterns (COPY order, layer caching, context issues), and suggests fixes.
scripts:
  - name: analyze-dockerfile
    command: node .github/skills/docker-build-debugger/analyze-dockerfile.js
    description: Validates Dockerfile for common issues (COPY order, WORKDIR, caching patterns)
templates:
  - name: dockerfile-template.md
    description: Production-ready Dockerfile templates for Node.js applications (API, frontend, multi-stage)
---

# Docker Build Debugger Skill

This skill helps diagnose Docker build failures for FanHub's Node.js frontend and backend services.

## Common Docker Build Failure Patterns

### 1. ENOENT Errors (Missing Files)

**Symptom**:
```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /app/package.json
npm ERR! errno -2
```

**Root Cause**: `RUN npm install` appears before `COPY package.json`

**Fix**:
```dockerfile
# ❌ Wrong order
FROM node:18-alpine
RUN npm install          # Fails - package.json doesn't exist yet
COPY package*.json ./

# ✅ Correct order
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./    # Copy dependencies first
RUN npm ci               # Now package.json exists
COPY . .                 # Copy code last
```

---

### 2. "No Source Files" Errors

**Symptom**:
```
COPY failed: file not found in build context or excluded by .dockerignore: 
stat package.json: file does not exist
```

**Root Causes**:
- COPY path is relative to build context, not Dockerfile location
- File is excluded by .dockerignore
- Wrong context directory specified in docker build command

**Diagnostic Questions**:
- Where is the Dockerfile? (`backend/Dockerfile`)
- Where is the context? (Usually project root: `.`)
- What's the build command? (`docker build -f backend/Dockerfile .`)

**Fix Example**:
```dockerfile
# If Dockerfile is in backend/, but context is project root:
COPY backend/package*.json ./     # Path relative to context
```

Or adjust build command:
```bash
# Build with backend/ as context
docker build -f backend/Dockerfile ./backend
```

---

### 3. Layer Caching Issues (Slow Rebuilds)

**Symptom**: Every code change re-runs `npm install` (5+ minutes wasted)

**Root Cause**: `COPY . .` before `RUN npm install` breaks layer caching

**How Layer Caching Works**:
- Docker caches each layer
- If a layer's inputs change, that layer + all following layers rebuild
- Code changes more often than dependencies

**Bad Pattern** (slow):
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .                # Copies EVERYTHING (including code)
RUN npm ci              # Rebuilds whenever ANY file changes
CMD ["node", "src/index.js"]
```

**Good Pattern** (fast):
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./   # Only copy dependency files
RUN npm ci              # Cached unless package.json changes
COPY . .                # Copy code last (fast layer)
CMD ["node", "src/index.js"]
```

**Time saved**: 5-10 minutes per rebuild

---

### 4. Context Too Large

**Symptom**: 
```
Sending build context to Docker daemon  1.2GB
```
Build is slow or fails with timeout.

**Root Cause**: Missing or incomplete `.dockerignore`

**Fix**: Create/update `.dockerignore`:
```
node_modules
.git
*.log
.env
.vscode
dist
coverage
__tests__
*.md
```

**Rule**: Only include files needed in the final image.

---

### 5. Executor Failed Running Commands

**Symptom**:
```
executor failed running [/bin/sh -c npm install]: exit code 1
```

**Diagnostic Approach**:
1. Read the full error output (not just the exit code)
2. Look for the actual npm/node error
3. Check if the command works locally

**Common Causes**:
- Dependency install failure (check npm ERR! lines)
- Build step failure (e.g., `npm run build` fails)
- Missing environment variable
- Wrong Node version

---

## FanHub-Specific Docker Patterns

**For creating new Dockerfiles**: See `dockerfile-template.md` for production-ready templates.

**Common issues with FanHub's existing Dockerfiles**:

### Frontend (React App)
- Build fails: Check `npm run build` works locally
- Missing env vars: Use `ARG` for build-time vars (e.g., `REACT_APP_API_URL`)
- Slow builds: Ensure package.json copied before source code

### Backend (Node API)
- Database files missing: Ensure `COPY database/` is included
- Dev dependencies in production: Use `npm ci --only=production`
- Port not exposed: Add `EXPOSE 3000`

---

## Diagnostic Workflow

When a Docker build fails:

1. **Read the error message carefully**
   - Don't just see "exit code 1"—find the actual error
   - Look for npm ERR!, ENOENT, "failed", "not found"

2. **Identify the failing step**
   - Which Docker instruction failed? (Step X/Y in output)
   - COPY? RUN? FROM?

3. **Check COPY/RUN command order**
   - Is WORKDIR set before COPY?
   - Is package.json copied before npm install?
   - Is COPY . . last (after dependencies)?

4. **Verify paths are correct**
   - Paths in COPY are relative to build context
   - Check `docker build` context directory
   - Check .dockerignore isn't excluding needed files

5. **Test layer caching**
   - Does changing one line of code re-run npm install?
   - If yes, COPY order is wrong

6. **Run the script**
   - Use `analyze-dockerfile.js` to check for common issues
   - The script validates COPY order, WORKDIR, caching patterns

---

## Using the Diagnostic Script

Run the validator before debugging:

```bash
node .github/skills/docker-build-debugger/analyze-dockerfile.js backend/Dockerfile
```

**Output Example**:
```json
{
  "file": "backend/Dockerfile",
  "issues": [
    {
      "line": 4,
      "severity": "error",
      "message": "RUN npm install before COPY package.json - will fail with ENOENT",
      "fix": "Move COPY package*.json ./ before RUN npm install"
    }
  ],
  "summary": "Found 1 potential issue(s)"
}
```

**Interpretation**:
- `severity: error` — Will definitely cause build failure
- `severity: warning` — May cause slow builds or issues
- `fix` — Specific action to resolve

---

## Best Practices for Node.js Dockerfiles

1. **Always set WORKDIR** before COPY/RUN
   ```dockerfile
   WORKDIR /app
   ```

2. **Copy package files first** (for caching)
   ```dockerfile
   COPY package*.json ./
   ```

3. **Use `npm ci` instead of `npm install`** (faster, reproducible)
   ```dockerfile
   RUN npm ci
   ```

4. **Copy source code last**
   ```dockerfile
   COPY . .
   ```

5. **Use multi-stage builds** for production
   ```dockerfile
   FROM node:18-alpine AS builder
   # ... build steps ...
   FROM node:18-alpine
   COPY --from=builder /app/dist ./dist
   ```

6. **Create .dockerignore** to reduce context size
   ```
   node_modules
   .git
   *.log
   ```

---

## Quick Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `ENOENT package.json` | COPY order wrong | Move COPY package.json before RUN npm install |
| `no source files` | Wrong context path | Check docker build command context |
| Slow rebuilds | Bad layer caching | Copy package.json first, code last |
| Context 1GB+ | Missing .dockerignore | Create .dockerignore with node_modules |
| `executor failed` | Actual error buried | Read full output for npm ERR! lines |

---

## When to Use This Skill

Ask Copilot with this skill when:
- Docker build fails with cryptic errors
- Builds are slow (re-installing deps every time)
- "It works locally but not in Docker"
- Need to validate Dockerfile before committing
- Teaching someone Docker build patterns
- **Creating a new Dockerfile from scratch** (use the template)

**Example prompts**:
- *"Why does my Dockerfile fail with ENOENT?"*
- *"My Docker build is slow—every code change re-runs npm install. What's wrong?"*
- *"Run the Docker analyzer on backend/Dockerfile"*
- *"Use the Dockerfile template to create a production Dockerfile for a Node.js API on port 4000"*
- *"Generate a multi-stage Dockerfile for a React app using the template"*
