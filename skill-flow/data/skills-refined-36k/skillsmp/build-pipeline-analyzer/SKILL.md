---
name: build-pipeline-analyzer
description: Diagnoses GitHub Actions CI/CD failures for FanHub's Node.js workflows. Identifies test failures, build errors, Docker issues, and environment problems.
---

# Build Pipeline Analyzer Skill

This skill helps diagnose GitHub Actions workflow failures for FanHub's frontend and backend CI/CD pipelines.

## FanHub CI/CD Pipeline Structure

### Frontend Workflow
```yaml
name: Frontend CI
steps:
  1. Checkout code
  2. Setup Node.js 18
  3. npm ci (install dependencies)
  4. npm run lint (ESLint)
  5. npm test -- --coverage (Jest tests, 80% minimum)
  6. npm run build (production build)
```

### Backend Workflow
```yaml
name: Backend CI
steps:
  1. Checkout code
  2. Setup Node.js 18
  3. Setup PostgreSQL service
  4. npm ci (install dependencies)
  5. npm run lint (ESLint)
  6. npm test -- --coverage (Jest + integration tests)
  7. Docker build (multi-stage Dockerfile)
```

**Environment**: ubuntu-latest runners, Node 18 LTS

---

## Common CI/CD Failure Patterns

### 1. Test Failures

#### 1A. Test Timeout

**Symptom**:
```
FAIL src/components/CharacterCard.test.js
  ● CharacterCard › renders character name
    
    Timeout - Async callback was not invoked within the 5000ms timeout 
    specified by jest.setTimeout.
    
npm ERR! Test failed. See above for more details.
```

**Root Causes**:
- Unmocked API call (waiting for real network request)
- Database connection not established (in integration tests)
- Infinite loop or unresolved Promise
- CI runner slower than local machine

**Diagnostic Questions**:
- Does test pass locally? (flaky vs. broken)
- Is there an API call without a mock?
- Is there an async operation without await?
- Is there a database dependency?

**Fixes**:
1. **Increase timeout** (if genuinely slow operation):
   ```javascript
   jest.setTimeout(10000); // 10 seconds
   ```

2. **Add missing mocks**:
   ```javascript
   jest.mock('../api/characters', () => ({
     getCharacter: jest.fn().mockResolvedValue({ name: 'Test' })
   }));
   ```

3. **Ensure async completion**:
   ```javascript
   await waitFor(() => {
     expect(screen.getByText('Character Name')).toBeInTheDocument();
   });
   ```

4. **Fix database setup** (backend tests):
   ```javascript
   beforeEach(async () => {
     await db.reset();  // Ensure DB is ready
   });
   ```

---

#### 1B. Assertion Failure

**Symptom**:
```
FAIL src/api/characters.test.js
  ● GET /api/characters/:id › returns character with related data
    
    Expected: 200
    Received: 500
    
    Database connection timeout
```

**Root Causes**:
- Test database not properly configured in CI
- Missing environment variables
- Race condition (test runs before setup completes)
- Test isolation issue (previous test left dirty state)

**Diagnostic Questions**:
- Does test pass when run alone? (`npm test -- CharacterCard`)
- Are environment variables set in GitHub Actions?
- Is the database service running? (check workflow YAML)
- Is test cleanup happening? (afterEach hooks)

**Fixes**:
1. **Check GitHub Actions secrets/env vars**:
   ```yaml
   env:
     DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
     NODE_ENV: test
   ```

2. **Add test isolation**:
   ```javascript
   afterEach(async () => {
     await db.query('TRUNCATE TABLE characters, quotes CASCADE');
   });
   ```

3. **Wait for services to be ready**:
   ```yaml
   - name: Wait for PostgreSQL
     run: |
       until pg_isready -h localhost -p 5432; do
         sleep 1
       done
   ```

---

### 2. Build Failures

#### 2A. Dependency Install Failure

**Symptom**:
```
Run npm ci
npm ERR! cipm can only install packages when your package.json and 
package-lock.json are in sync.
```

**Root Cause**: `package-lock.json` is out of sync with `package.json`

**Fixes**:
1. **Locally regenerate lock file**:
   ```bash
   rm package-lock.json
   npm install
   git add package-lock.json
   git commit -m "fix: regenerate package-lock.json"
   ```

2. **Or use `npm install` in CI** (slower but more forgiving):
   ```yaml
   - run: npm install  # Instead of npm ci
   ```

---

#### 2B. Build Step Failure

**Symptom**:
```
Run npm run build
> react-scripts build

Failed to compile.

Module not found: Can't resolve './CharacterCard' in '/src/pages'
```

**Root Causes**:
- Import path wrong (case-sensitive on Linux, not on Mac/Windows)
- File not committed to git
- Build-time environment variable missing

**CI vs Local Differences**:
- CI runs on Linux (case-sensitive filesystem)
- CI clones from git (doesn't see untracked files)
- CI has different environment variables

**Diagnostic Questions**:
- Is the file name exactly right? (`CharacterCard.js` vs. `characterCard.js`)
- Is the file committed? (`git ls-files | grep CharacterCard`)
- Does the build need env vars? (check for `process.env.REACT_APP_*`)

**Fixes**:
1. **Fix import case**:
   ```javascript
   // If file is CharacterCard.js:
   import CharacterCard from './CharacterCard'; // ✅ Correct
   import CharacterCard from './characterCard'; // ❌ Works on Mac, fails on Linux
   ```

2. **Commit missing files**:
   ```bash
   git add src/components/CharacterCard.js
   git commit -m "fix: add missing component file"
   ```

3. **Add build-time env vars**:
   ```yaml
   - name: Build
     env:
       REACT_APP_API_URL: ${{ secrets.API_URL }}
     run: npm run build
   ```

---

### 3. Linting Failures

**Symptom**:
```
Run npm run lint

/home/runner/work/fanhub/src/components/CharacterCard.js
  12:7  error  'character' is assigned a value but never used  no-unused-vars

✖ 1 problem (1 error, 0 warnings)
```

**Root Cause**: Code passes locally because lint warnings were ignored

**Why CI Catches It**:
- Local: `npm run lint` may just warn
- CI: Often configured to fail on errors (`--max-warnings 0`)

**Fixes**:
1. **Fix the lint error** (preferred):
   ```javascript
   // Remove unused variable
   const { character } = props; // ❌ Unused
   const { name } = props;      // ✅ Used
   ```

2. **Run lint with auto-fix locally**:
   ```bash
   npm run lint -- --fix
   ```

3. **Add lint-staged to prevent this**:
   ```json
   // package.json
   {
     "husky": {
       "hooks": {
         "pre-commit": "lint-staged"
       }
     },
     "lint-staged": {
       "*.js": "eslint --fix"
     }
   }
   ```

---

### 4. Docker Build Failures in CI

#### 4A. COPY Path Issues

**Symptom**:
```
Step 4/7 : COPY package*.json ./
COPY failed: file not found in build context or excluded by .dockerignore: 
stat package.json: file does not exist
```

**Root Cause**: Docker build context is wrong in GitHub Actions

**CI vs Local Difference**:
- Local: You run `docker build` from the right directory
- CI: Workflow might run from repo root

**Diagnostic Questions**:
- What's the `docker build` command in the workflow?
- Where is the Dockerfile? (`backend/Dockerfile`)
- Where is package.json relative to the Dockerfile?

**Fixes**:
1. **Check workflow docker build command**:
   ```yaml
   # ❌ Wrong context
   - name: Build Docker image
     run: docker build -f backend/Dockerfile .
   
   # ✅ Correct context
   - name: Build Docker image
     run: docker build -f backend/Dockerfile ./backend
   ```

2. **Or adjust Dockerfile COPY paths**:
   ```dockerfile
   # If context is repo root and Dockerfile is in backend/:
   COPY backend/package*.json ./
   ```

---

### 5. Flaky Tests

**Symptom**: Test passes sometimes, fails other times (~30% failure rate)

**Example**:
```
Run npm test
FAIL src/api/characters.test.js (Run 1/1)
  ● GET /api/characters/:id › returns character with related data
    Expected: 200
    Received: 500
```

But re-running the workflow... it passes.

**Root Causes**:
- Race condition (async operations not properly awaited)
- Shared state between tests (one test affects another)
- External dependency (database, network)
- Timing-dependent assertion

**Diagnostic Questions**:
- Does it fail consistently or intermittently?
- Does it pass when run alone?
- Is there shared state (global variables, database)?
- Are async operations properly awaited?

**Fixes**:
1. **Improve test isolation**:
   ```javascript
   beforeEach(async () => {
     await db.resetAllTables();  // Clean slate for each test
   });
   ```

2. **Add retry logic for known-flaky tests**:
   ```javascript
   jest.retryTimes(2);  // Retry failed tests twice
   ```

3. **Use proper async patterns**:
   ```javascript
   // ❌ Race condition
   render(<CharacterCard id={1} />);
   expect(screen.getByText('Name')).toBeInTheDocument();
   
   // ✅ Wait for async data
   render(<CharacterCard id={1} />);
   await waitFor(() => {
     expect(screen.getByText('Name')).toBeInTheDocument();
   });
   ```

4. **Increase timeout for slow CI runners**:
   ```javascript
   jest.setTimeout(10000);  // CI may be slower than local
   ```

---

## Diagnostic Workflow

When a GitHub Actions build fails:

1. **Identify which step failed**
   - Click on the failed workflow run
   - Expand the failed step
   - Look for the red ✖ icon

2. **Extract the actual error message**
   - Don't stop at "exit code 1"
   - Scroll up to find the actual error (npm ERR!, FAIL, ERROR)
   - Copy the error message

3. **Determine the failure type**
   | Error Contains | Failure Type |
   |----------------|--------------|
   | `FAIL`, `Timeout` | Test failure |
   | `npm ERR!`, `ERESOLVE` | Dependency issue |
   | `Module not found` | Build error |
   | `error` + `eslint` | Lint failure |
   | `COPY failed` | Docker build issue |

4. **Check if it's a regression**
   - Did this pass on the previous commit?
   - Check the commit diff—what changed?
   - Look at previous successful runs for comparison

5. **Distinguish CI-specific vs. universal issues**
   | Issue | CI-Specific? |
   |-------|--------------|
   | Test timeout | Maybe (CI slower) |
   | Import case mismatch | Yes (Linux vs Mac) |
   | Missing mocks | No (universal) |
   | Docker context path | Yes (workflow-specific) |
   | Lint error | No (should fail locally too) |

6. **Apply the appropriate fix**
   - See specific sections above for each failure type

---

## Quick Triage Guide

```
Build Failed
└─ Which step?
   ├─ npm ci
   │  └─ "out of sync" → Regenerate package-lock.json
   ├─ npm run lint
   │  └─ ESLint error → Fix or run --fix locally
   ├─ npm test
   │  ├─ "Timeout" → Check mocks, increase timeout
   │  ├─ Assertion failed → Check DB setup, env vars
   │  └─ "Flaky" → Improve test isolation, add retries
   ├─ npm run build
   │  ├─ "Module not found" → Check import case, file committed
   │  └─ Build error → Check for missing env vars
   └─ docker build
      └─ "COPY failed" → Check context path in workflow
```

---

## Cross-Skill Integration

This skill works well with:

**Docker Build Debugger Skill**:
- When Docker build fails in CI
- Validates Dockerfile patterns
- Checks COPY order, layer caching

**Dependency Conflict Resolver Skill**:
- When npm ci fails with ERESOLVE
- Diagnoses peer dependency conflicts
- Suggests upgrade paths

**Example question that uses both**:
> *"The CI pipeline fails during Docker build. The error is 'ENOENT package.json'. What should I check?"*

Copilot might:
1. Use Build Pipeline Analyzer: Check CI workflow docker build context
2. Use Docker Build Debugger: Validate Dockerfile COPY order

---

## When to Use This Skill

Ask Copilot with this skill when:
- GitHub Actions workflow fails
- Need to understand what step failed and why
- Want to diagnose test failures in CI
- Dealing with flaky tests
- Docker build works locally but fails in CI
- Teaching someone about CI/CD debugging

**Example prompts**:
- *"The GitHub Actions build failed with test timeout. How do I debug it?"*
- *"Why does my Docker build work locally but fail in CI?"*
- *"This test is flaky—passes sometimes, fails others. What should I check?"*
- *"The workflow failed at the lint step. How do I fix ESLint errors?"*

---

## Prevention Strategies

### 1. Run CI Checks Locally

```bash
# Run the same commands CI runs
npm ci               # Exact install (like CI)
npm run lint         # Catch lint errors
npm test -- --coverage  # Run with coverage (like CI)
npm run build        # Test production build
```

### 2. Use Act to Test Workflows Locally

```bash
# Install act: https://github.com/nektos/act
act  # Runs GitHub Actions locally with Docker
```

### 3. Add Lint-Staged (Pre-commit Hooks)

Catch issues before they reach CI:
```json
{
  "lint-staged": {
    "*.js": ["eslint --fix", "git add"]
  }
}
```

### 4. Monitor Flaky Tests

Track which tests fail intermittently:
```bash
# Run tests multiple times to find flakes
for i in {1..10}; do npm test; done
```

---

## Links to Future Modules

This skill connects to:

**Module 6 (MCP Servers)**:
- Use GitHub MCP to query Actions logs programmatically
- Fetch failure history for pattern analysis

**Module 8 (Copilot Web)**:
- Create/modify GitHub Actions workflows in browser
- Your pipeline knowledge speeds up workflow creation

**Module 9 (Copilot CLI)**:
- Run CI commands locally through CLI
- Debug workflows from terminal

**Module 10 (Agentic SDLC)**:
- Automated testing and CI/CD integration
- Full build → test → deploy pipeline
