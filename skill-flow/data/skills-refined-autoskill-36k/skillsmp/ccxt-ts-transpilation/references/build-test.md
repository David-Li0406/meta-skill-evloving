# Build & Test

## Build System

CCXT uses Node.js-based transpilation to generate Python, PHP, Go, and C# from TypeScript sources.

### Transpile Single Exchange

```bash
# Transpile REST API for one exchange
npm run emitAPI binance
npm run transpileRest binance

# Transpile WebSocket for one exchange
npm run transpileWs binance

# Complete build for one exchange (Python only)
npm run emitAPI binance && npm run transpileRest binance && npm run transpileWs binance
```

### Build All Exchanges

```bash
# Full build (all languages, all exchanges)
npm run build

# This internally runs:
# - npm run emitAPI
# - npm run transpileRest
# - npm run transpileWs
# - npm run vss (version sync)
```

### Build for Specific Language

```bash
# Python only
npm run transpilePython

# PHP only
npm run transpilePHP

# Go only (not commonly used standalone)
# C# only (not commonly used standalone)
```

## Build Process Details

### 1. Emit API

**Generates API method signatures** from abstract files.

```bash
npm run emitAPI binance
```

**What it does**:
- Reads `ts/src/abstract/binance.ts`
- Generates API method stubs (e.g., `publicGetTicker`, `privatePostOrder`)
- Updates main exchange file with method signatures

### 2. Transpile REST

**Converts TypeScript to target languages.**

```bash
npm run transpileRest binance
```

**Output**:
- `python/ccxt/binance.py`
- `php/binance.php`
- `go/ccxt/binance.go`
- `cs/ccxt/binance.cs`

### 3. Transpile WebSocket

**Converts WebSocket implementation** (if exists).

```bash
npm run transpileWs binance
```

**Output**:
- `python/ccxt/pro/binance.py`
- Similar for other languages

## Testing

### Run Tests

```bash
# Test single exchange (JavaScript)
node run-tests.js --js --exchange=binance

# Test single exchange (Python)
node run-tests.js --python --exchange=binance

# Test single exchange (PHP)
node run-tests.js --php --exchange=binance

# Test specific method
node run-tests.js --js --exchange=binance --method=fetchTicker

# Test all exchanges (takes hours!)
node run-tests.js --js
```

### Skip Tests

Exchanges in `skip-tests.json` are skipped:

```json
{
    "binance": {
        "fetchTicker": "temporarily disabled"
    }
}
```

### Test Configuration

Exchange API keys in `keys.json` (gitignored):

```json
{
    "binance": {
        "apiKey": "YOUR_API_KEY",
        "secret": "YOUR_SECRET",
        "uid": "optional_user_id",
        "password": "optional_password"
    }
}
```

## Debugging Transpilation

### Check Transpiled Output

After building, **verify transpiled code**:

```bash
# Check Python output
cat python/ccxt/binance.py | grep -A 10 "def fetch_ticker"

# Check PHP output
cat php/binance.php | grep -A 10 "function fetch_ticker"
```

### Common Transpilation Issues

**Problem**: Ternary operators break build
```bash
# Error: Transpilation failed with ternary
```
**Solution**: Replace with if/else

**Problem**: Type annotations on locals
```bash
# Error: Cannot transpile typed locals
```
**Solution**: Remove type annotations

**Problem**: Null checks fail
```bash
# Error: Null handling inconsistent
```
**Solution**: Use undefined checks only

## CI/CD Workflow

### GitHub Actions

CCXT runs automated tests on every PR:

```yaml
# .github/workflows/test.yml (simplified)
- name: Build
  run: npm run build

- name: Test JavaScript
  run: node run-tests.js --js

- name: Test Python
  run: node run-tests.js --python

- name: Test PHP
  run: node run-tests.js --php
```

### Pre-commit Hooks

**Always run before committing**:

```bash
# Setup git hooks (do this once)
git config core.hooksPath .git-templates/hooks

# Pre-commit will automatically:
# - Lint TypeScript
# - Run transpilation
# - Run tests
# - Check formatting
```

## Development Workflow

### Recommended Process

1. **Make TypeScript edits** in `ts/src/`
   ```bash
   vim ts/src/binance.ts
   ```

2. **Build exchange**
   ```bash
   npm run emitAPI binance && npm run transpileRest binance
   ```

3. **Check transpiled output**
   ```bash
   # Verify Python looks correct
   vim python/ccxt/binance.py
   ```

4. **Test changes**
   ```bash
   node run-tests.js --js --exchange=binance --method=fetchTicker
   node run-tests.js --python --exchange=binance --method=fetchTicker
   ```

5. **Commit only TypeScript**
   ```bash
   git add ts/src/binance.ts ts/src/abstract/binance.ts
   git commit -m "feat(binance): add fetchTicker method"
   ```

**Do NOT commit**:
- `python/ccxt/*.py` (except base classes)
- `php/*.php` (except base classes)
- `go/*.go` (except base classes)
- `cs/*.cs` (except base classes)
- `/build/*`
- `/dist/*`
- `/README.md` (auto-generated)

These are regenerated on CI.

## Performance Optimization

### Incremental Builds

When editing multiple exchanges, build one at a time:

```bash
# Instead of npm run build (builds everything)
npm run emitAPI binance && npm run transpileRest binance
npm run emitAPI coinbase && npm run transpileRest coinbase
```

### Parallel Testing

Test multiple exchanges in parallel (carefully):

```bash
# Terminal 1
node run-tests.js --js --exchange=binance

# Terminal 2
node run-tests.js --js --exchange=coinbase
```

## Troubleshooting

### Build Fails

```bash
# Error: Module not found
npm install

# Error: TypeScript compilation failed
npm run tsBuild

# Error: Transpilation error
# Check for ternaries, type annotations, null checks in your code
```

### Tests Fail

```bash
# Check API credentials
cat keys.json

# Check exchange status
curl https://api.binance.com/api/v3/ping

# Enable verbose mode
node run-tests.js --js --exchange=binance --verbose
```

### Version Mismatch

```bash
# Sync versions across languages
npm run vss
```
