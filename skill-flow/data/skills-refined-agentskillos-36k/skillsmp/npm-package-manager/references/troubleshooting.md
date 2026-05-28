# npm Troubleshooting Guide

Common npm issues and their solutions for the LucidData project.

## Table of Contents

1. [Installation Errors](#installation-errors)
2. [Dependency Conflicts](#dependency-conflicts)
3. [Lock File Issues](#lock-file-issues)
4. [Cache Problems](#cache-problems)
5. [Permission Errors](#permission-errors)
6. [Version Mismatches](#version-mismatches)
7. [Network Issues](#network-issues)
8. [Build Errors](#build-errors)

## Installation Errors

### Error: `ENOENT: no such file or directory`

**Symptom:**
```
npm ERR! ENOENT: no such file or directory, open 'package.json'
```

**Cause:** Running npm command in wrong directory

**Solution:**
```bash
# Navigate to project root
cd c:\repo\LucidData

# Verify you're in correct location
ls package.json

# Then run npm command
npm install
```

---

### Error: `ERESOLVE unable to resolve dependency tree`

**Symptom:**
```
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! Found: react@19.0.0
npm ERR! Could not resolve dependency: peer react@"^18.0.0" required by some-package
```

**Cause:** Package requires older version of peer dependency (React 18 vs React 19)

**Solutions:**

**Option 1: Use legacy peer deps (recommended)**
```bash
npm install --legacy-peer-deps
```

**Option 2: Force installation (may cause runtime errors)**
```bash
npm install --force
```

**Option 3: Wait for package update or find alternative**
```bash
# Check if package has React 19 support
npm view <package-name> peerDependencies

# Search for alternative packages
npm search <functionality>
```

**Best practice for LucidData:**
- Add `--legacy-peer-deps` flag to npm install commands
- Document in issue tracker which packages require this flag
- Monitor package updates for React 19 support

---

### Error: `npm ERR! code EINTEGRITY`

**Symptom:**
```
npm ERR! code EINTEGRITY
npm ERR! Verification failed while extracting @package/name
```

**Cause:** Corrupted download or cache mismatch

**Solution:**
```bash
# Clean npm cache
npm cache clean --force

# Delete node_modules and lockfile
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

### Error: `gyp ERR! build error` (native modules)

**Symptom:**
```
gyp ERR! build error
gyp ERR! stack Error: `C:\Program Files\MSBuild\14.0\bin\msbuild.exe` failed
```

**Cause:** Missing build tools for native modules (bcrypt, node-sass, etc.)

**Solution (Windows):**
```bash
# Install windows-build-tools
npm install --global windows-build-tools

# Or install Visual Studio Build Tools manually
# https://visualstudio.microsoft.com/downloads/
```

**Solution (Mac):**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

**Solution (Linux):**
```bash
# Install build essentials
sudo apt-get install build-essential
```

**Note:** LucidData avoids native modules when possible. If you encounter this, consider pure JavaScript alternatives.

---

## Dependency Conflicts

### Error: Multiple versions of same package

**Symptom:**
```
npm WARN conflicting peer dependency: react@18.0.0
  node_modules/some-package/react
```

**Cause:** Different packages require different versions of the same dependency

**Solution:**

**Step 1: Identify the conflict**
```bash
npm list react
# Shows dependency tree with all React versions
```

**Step 2: Update conflicting packages**
```bash
# Update packages to versions compatible with React 19
npm update <package-name>
```

**Step 3: Use resolutions (if package.json supports it)**
```json
{
  "overrides": {
    "react": "19.0.0",
    "react-dom": "19.0.0"
  }
}
```

**Step 4: Deduplicate**
```bash
npm dedupe
```

---

### Error: Cannot find module after install

**Symptom:**
```
Error: Cannot find module '@package/name'
```

**Cause:** Incomplete installation or corrupted node_modules

**Solution:**
```bash
# Clean installation
rm -rf node_modules package-lock.json
npm install

# If specific package is missing, reinstall it
npm uninstall <package-name>
npm install <package-name>

# Verify installation
npm list <package-name>
```

---

## Lock File Issues

### Error: `package-lock.json` conflicts in Git

**Symptom:**
```
<<<<<<< HEAD
  "lockfileVersion": 2,
=======
  "lockfileVersion": 3,
>>>>>>> branch-name
```

**Cause:** Merge conflict from different npm versions or parallel changes

**Solutions:**

**Option 1: Accept one version and regenerate**
```bash
# Accept your version
git checkout --ours package-lock.json
npm install

# Or accept their version
git checkout --theirs package-lock.json
npm install

# Stage resolved file
git add package-lock.json
```

**Option 2: Delete and regenerate**
```bash
rm package-lock.json
npm install
git add package-lock.json
```

**Option 3: Manual merge (advanced)**
```bash
# Resolve conflicts manually in editor
# Ensure "packages" and "dependencies" sections are consistent
# Run npm install to validate
npm install
```

---

### Error: `package.json` and `package-lock.json` out of sync

**Symptom:**
```
npm ERR! Cannot read properties of null (reading 'edgesOut')
```

**Cause:** package.json was edited manually without updating lockfile

**Solution:**
```bash
# Update lockfile to match package.json
npm install

# Or force update
rm package-lock.json
npm install
```

---

## Cache Problems

### Error: Corrupted npm cache

**Symptom:**
```
npm ERR! Unexpected end of JSON input while parsing near '...'
```

**Cause:** Corrupted cache data

**Solution:**
```bash
# Verify cache
npm cache verify

# Clean cache
npm cache clean --force

# Reinstall packages
rm -rf node_modules
npm install
```

---

### Error: Cache taking too much disk space

**Solution:**
```bash
# Check cache size
du -sh $(npm config get cache)

# Clean cache
npm cache clean --force

# Verify integrity
npm cache verify
```

**Note:** npm cache is located at:
- Windows: `%LocalAppData%\npm-cache`
- Mac/Linux: `~/.npm`

---

## Permission Errors

### Error: `EACCES` permission denied (Windows)

**Symptom:**
```
npm ERR! code EACCES
npm ERR! errno -4048
npm ERR! Error: EACCES: permission denied
```

**Cause:** File or directory locked by another process

**Solution:**
```bash
# Close VS Code, terminals, dev server
# Delete node_modules
rm -rf node_modules

# Reinstall
npm install
```

**If issue persists:**
```bash
# Run PowerShell as Administrator
# Navigate to project directory
cd c:\repo\LucidData

# Take ownership of directory
takeown /f node_modules /r /d y

# Then retry
npm install
```

---

### Error: `EACCES` permission denied (Mac/Linux)

**Symptom:**
```
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
```

**Cause:** Trying to install global packages without sudo (anti-pattern)

**Solution (recommended): Use nvm**
```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js
nvm install 18
nvm use 18

# Now npm install works without sudo
npm install -g npm
```

**Solution (quick fix): Change npm default directory**
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH=~/.npm-global/bin:$PATH

# Reload shell
source ~/.bashrc
```

---

## Version Mismatches

### Error: Prisma version mismatch

**Symptom:**
```
Error: @prisma/client version 6.19.1 does not match prisma version 6.20.0
```

**Cause:** @prisma/client and prisma packages out of sync

**Solution:**
```bash
# Check versions
npm list @prisma/client prisma

# Install matching versions
npm install @prisma/client@6.20.0 prisma@6.20.0

# Generate Prisma client
npx dotenv -e .env.local -- npx prisma generate

# Verify
npm list @prisma/client prisma
```

**Prevention:**
Always update both packages together:
```bash
npm install @prisma/client@<version> prisma@<version>
```

---

### Error: Node version mismatch

**Symptom:**
```
npm ERR! engine Unsupported engine
npm ERR! engine Not compatible with your version of node
```

**Cause:** Package requires different Node.js version

**Solution:**
```bash
# Check Node version
node --version

# LucidData requires Node 18+
# Install correct version with nvm
nvm install 18
nvm use 18

# Verify
node --version
npm --version

# Reinstall packages
npm install
```

---

## Network Issues

### Error: `ETIMEDOUT` or `ENOTFOUND`

**Symptom:**
```
npm ERR! code ETIMEDOUT
npm ERR! errno ETIMEDOUT
npm ERR! network request to https://registry.npmjs.org/<package> failed
```

**Cause:** Network connectivity issues or proxy problems

**Solutions:**

**Option 1: Retry with longer timeout**
```bash
npm install --timeout=60000
```

**Option 2: Check network connectivity**
```bash
# Test connection to npm registry
curl https://registry.npmjs.org/

# Check proxy settings
npm config get proxy
npm config get https-proxy
```

**Option 3: Clear DNS cache (Windows)**
```bash
ipconfig /flushdns
```

**Option 4: Use different registry mirror (China)**
```bash
npm config set registry https://registry.npmmirror.com
npm install
# Reset to default after
npm config set registry https://registry.npmjs.org/
```

---

### Error: SSL certificate problem

**Symptom:**
```
npm ERR! certificate has expired
npm ERR! code UNABLE_TO_VERIFY_LEAF_SIGNATURE
```

**Cause:** Outdated SSL certificates or corporate proxy

**Solution (temporary, not recommended):**
```bash
npm config set strict-ssl false
npm install
# Reset after
npm config set strict-ssl true
```

**Solution (proper):**
- Update Node.js to latest LTS version
- Update npm: `npm install -g npm@latest`
- Configure corporate proxy certificates if behind firewall

---

## Build Errors

### Error: `Out of memory` during build

**Symptom:**
```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

**Cause:** Large project or complex builds exhausting Node.js memory

**Solution:**
```bash
# Increase Node.js memory limit
$env:NODE_OPTIONS="--max-old-space-size=4096"  # PowerShell (Windows)
export NODE_OPTIONS="--max-old-space-size=4096"  # Bash (Mac/Linux)

# Then build
npm run build

# For permanent fix, add to package.json scripts:
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' next build"
  }
}
```

---

### Error: Module not found in production build

**Symptom:**
- Works in dev (`npm run dev`)
- Fails in production build (`npm run build`)
- Error: `Module not found: Can't resolve '@/components/...'`

**Cause:** Case-sensitive imports or missing files

**Solution:**
```bash
# Check import casing matches file name exactly
# Wrong: import { Button } from '@/components/ui/Button'
# Correct: import { Button } from '@/components/ui/button'

# Verify file exists
ls components/ui/button.tsx

# Clean build
rm -rf .next
npm run build
```

---

### Error: Type errors in build but not in editor

**Symptom:**
```
npm run build
> tsc --noEmit
error TS2307: Cannot find module '@/lib/utils'
```

**Cause:** TypeScript path alias not configured correctly

**Solution:**
```bash
# Verify tsconfig.json has paths configured:
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}

# Restart TypeScript server in VS Code
# Ctrl+Shift+P > "TypeScript: Restart TS Server"

# Clean and rebuild
rm -rf .next node_modules
npm install
npm run build
```

---

## Emergency Recovery

### Nuclear option: Complete reinstall

When all else fails:

```bash
# 1. Backup .env files
cp .env.local .env.local.backup
cp .env.test .env.test.backup

# 2. Delete all generated files
rm -rf node_modules
rm -rf .next
rm package-lock.json

# 3. Clear caches
npm cache clean --force

# 4. Reinstall Node.js dependencies
npm install

# 5. Generate Prisma client
npx dotenv -e .env.local -- npx prisma generate

# 6. Test
npm run dev
npm run build
npm run test:run

# 7. Restore env files if needed
cp .env.local.backup .env.local
```

---

## Getting Help

If issues persist after trying solutions above:

1. **Check npm version**: Upgrade to latest: `npm install -g npm@latest`
2. **Check Node version**: Use Node 18 LTS: `nvm use 18`
3. **Search npm issues**: https://github.com/npm/cli/issues
4. **Search package issues**: Check the specific package's GitHub issues
5. **Ask the team**: Post in team chat with error message and steps tried
6. **Create minimal reproduction**: Isolate the issue in a fresh Next.js project

## Useful Debugging Commands

```bash
# Show npm configuration
npm config list

# Show package installation location
npm root

# Show global packages
npm list -g --depth=0

# Show where npm is installed
which npm  # Mac/Linux
where npm  # Windows

# Show Node.js version
node --version

# Show npm version
npm --version

# Verbose install (debug output)
npm install --verbose

# Dry run (show what would be installed)
npm install --dry-run

# Check for issues
npm doctor
```

---

**For more information:**
- [Package Operations Reference](package-operations.md)
- [Main Skill Documentation](../SKILL.md)
- [npm Documentation](https://docs.npmjs.com/troubleshooting)
