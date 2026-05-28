# Error Prevention

Techniques for preventing errors before they occur through validation, guardrails, and best practices.

---

## Pre-Operation Validation

### File Operations

Before reading files:

```javascript
// Validate file exists
const exists = await fileExists(path);
if (!exists) {
  throw new Error(`File not found: ${path}`);
}

// Validate is readable
const stats = await stat(path);
if (!stats.isFile()) {
  throw new Error(`Not a file: ${path}`);
}

// Validate file size
if (stats.size > MAX_FILE_SIZE) {
  throw new Error(`File too large: ${path} (${stats.size} bytes)`);
}
```

Before writing files:

```javascript
// Validate directory exists
const dir = dirname(path);
if (!await directoryExists(dir)) {
  await mkdir(dir, { recursive: true });
}

// Check write permission
try {
  await access(dir, W_OK);
} catch {
  throw new Error(`Cannot write to directory: ${dir}`);
}

// Check disk space (if critical)
const space = await checkDiskSpace(dir);
if (space.free < REQUIRED_SPACE) {
  throw new Error(`Insufficient disk space: ${space.free} bytes available`);
}
```

---

### Path Validation

```javascript
function validatePath(path) {
  // Check for null bytes
  if (path.includes('\0')) {
    throw new Error('Invalid path: contains null byte');
  }

  // Check for path traversal
  const normalized = normalize(path);
  if (!normalized.startsWith(allowedRoot)) {
    throw new Error('Invalid path: outside allowed directory');
  }

  // Check for invalid characters (Windows)
  if (process.platform === 'win32') {
    if (/[<>:"|?*]/.test(path)) {
      throw new Error('Invalid path: contains invalid characters');
    }
  }

  return normalized;
}
```

---

### Command Validation

Before running Bash commands:

```javascript
function validateCommand(command) {
  // Check for dangerous patterns
  const dangerous = [
    'rm -rf /',
    'rm -rf ~',
    '> /dev/sda',
    'mkfs',
    ':(){:|:&};:',  // Fork bomb
  ];

  for (const pattern of dangerous) {
    if (command.includes(pattern)) {
      throw new Error(`Dangerous command detected: ${pattern}`);
    }
  }

  // Check for unquoted variables
  if (/\$\w+[^"]/.test(command)) {
    console.warn('Unquoted variable in command');
  }

  return true;
}
```

---

## Context Management

### Monitor Context Size

Track context usage to prevent overflow:

```
Current Context: 45,000 tokens
Max Context: 100,000 tokens
Usage: 45%
Warning Threshold: 80%
```

**When to Act:**
- **50%**: Normal operation
- **70%**: Consider clearing old context
- **80%**: Run `/compact` proactively
- **90%**: Clear non-essential data immediately
- **95%**: Emergency `/clear` required

---

### File Read Strategies

**Small Files (<10KB):**
Read entire file directly.

**Medium Files (10KB-1MB):**
Read with awareness, may need chunking later.

**Large Files (>1MB):**
Always use offset/limit parameters:

```javascript
// Read first 500 lines
read(path, { limit: 500 });

// Read specific section
read(path, { offset: 1000, limit: 200 });

// Read end of file
const lineCount = countLines(path);
read(path, { offset: lineCount - 100, limit: 100 });
```

**Very Large Files (>10MB):**
Use streaming or external tools:

```bash
# Get specific lines with sed
sed -n '1000,1500p' large_file.txt

# Get specific section with head/tail
head -n 1500 large_file.txt | tail -n 500

# Search within file
grep -n "pattern" large_file.txt | head -20
```

---

### Proactive Compaction

Compact context before it becomes a problem:

```
Task Started
    |
    +-- After every major operation:
    |   - Check context size
    |   - If > 70%, consider /compact
    |
    +-- After every 10 tool calls:
    |   - Review context usage
    |   - Remove redundant history
    |
    +-- Before large file operations:
        - Compact first if > 50%
        - Ensure headroom for output
```

---

## Permission Management

### Pre-Configure Permissions

Set up permissions before operations:

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(bun:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(mkdir:*)"
    ]
  }
}
```

### Project-Specific Permissions

```json
// .claude/settings.json (in project root)
{
  "permissions": {
    "allow": [
      "mcp__database__query",
      "mcp__api__request"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

### Permission Patterns

| Pattern | Meaning |
|---------|---------|
| `Read` | All read operations |
| `Write` | All write operations |
| `Bash(git:*)` | All git commands |
| `Bash(npm:install)` | Only npm install |
| `mcp__server__*` | All tools from server |
| `mcp__server__tool` | Specific tool only |

---

## Input Validation

### Validate User Input

```javascript
function validateInput(input, type) {
  switch (type) {
    case 'path':
      if (!isValidPath(input)) {
        throw new Error(`Invalid path format: ${input}`);
      }
      break;

    case 'url':
      try {
        new URL(input);
      } catch {
        throw new Error(`Invalid URL: ${input}`);
      }
      break;

    case 'json':
      try {
        JSON.parse(input);
      } catch {
        throw new Error('Invalid JSON format');
      }
      break;

    case 'number':
      if (isNaN(Number(input))) {
        throw new Error(`Invalid number: ${input}`);
      }
      break;
  }
  return true;
}
```

### Sanitize Inputs

```javascript
function sanitizeForBash(input) {
  // Escape shell special characters
  return input.replace(/(['"\\$`!])/g, '\\$1');
}

function sanitizeForRegex(input) {
  // Escape regex special characters
  return input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function sanitizePath(input) {
  // Remove null bytes and normalize
  return normalize(input.replace(/\0/g, ''));
}
```

---

## Configuration Validation

### Validate JSON Configuration

```bash
# Validate settings.json
jq . ~/.claude/settings.json > /dev/null 2>&1 && echo "Valid" || echo "Invalid"

# Validate with schema (if available)
jq --arg schema "$SCHEMA" '. as $config | $schema | .validate($config)' config.json

# Pretty print to verify structure
jq . ~/.claude/settings.json
```

### Validate Hook Configuration

```bash
# Check hook paths exist
for hook in $(jq -r '.hooks[]?.command // empty' ~/.claude/settings.json); do
  if [[ -x "$hook" ]]; then
    echo "OK: $hook"
  else
    echo "MISSING: $hook"
  fi
done

# Test hook execution
echo '{"event": "test"}' | ./path/to/hook.sh
echo "Exit code: $?"
```

### Validate MCP Configuration

```bash
# Validate .mcp.json syntax
jq . .mcp.json

# Check server commands exist
for cmd in $(jq -r '.mcpServers[].command // empty' .mcp.json); do
  which "$cmd" > /dev/null && echo "OK: $cmd" || echo "MISSING: $cmd"
done

# Test server connection
claude mcp list
```

---

## Defensive Programming

### Always Handle Errors

```javascript
// Bad - unhandled error
const data = JSON.parse(fileContent);

// Good - handle potential error
let data;
try {
  data = JSON.parse(fileContent);
} catch (error) {
  throw new Error(`Invalid JSON in file: ${error.message}`);
}
```

### Check Before Operating

```javascript
// Bad - assume file exists
const content = readFile(path);

// Good - verify first
if (!await fileExists(path)) {
  throw new Error(`File not found: ${path}`);
}
const content = readFile(path);
```

### Validate Assumptions

```javascript
// Bad - assume property exists
const value = config.settings.timeout;

// Good - validate chain
const value = config?.settings?.timeout ?? defaultTimeout;

// Better - explicit check
if (!config?.settings?.timeout) {
  console.warn('Missing timeout config, using default');
}
const value = config.settings?.timeout ?? defaultTimeout;
```

---

## Guardrails

### Operation Limits

| Operation | Limit | Rationale |
|-----------|-------|-----------|
| File read size | 10MB | Prevent context overflow |
| File count per glob | 1000 | Prevent memory issues |
| Command timeout | 120s | Prevent hangs |
| Retry attempts | 5 | Avoid infinite loops |
| Concurrent requests | 3 | Respect rate limits |

### Safety Checks

```javascript
// Before large operations
function safetyCheck(operation) {
  const checks = {
    diskSpace: checkDiskSpace() > MINIMUM_SPACE,
    memoryAvailable: checkMemory() > MINIMUM_MEMORY,
    contextHeadroom: checkContext() < MAX_CONTEXT * 0.8,
    withinRateLimits: checkRateLimits(),
  };

  const failed = Object.entries(checks)
    .filter(([_, passed]) => !passed)
    .map(([name]) => name);

  if (failed.length > 0) {
    throw new Error(`Safety checks failed: ${failed.join(', ')}`);
  }
}
```

### Confirmation for Destructive Operations

```javascript
const destructive = ['rm', 'delete', 'drop', 'truncate', 'format'];

function requiresConfirmation(command) {
  return destructive.some(d => command.toLowerCase().includes(d));
}

if (requiresConfirmation(command)) {
  console.log(`About to run: ${command}`);
  console.log('This is a destructive operation.');
  // In interactive mode, would prompt for confirmation
}
```

---

## Testing Before Production

### Test Hooks Locally

```bash
# Test with sample input
echo '{"event": "test", "data": {}}' | ./hook.sh

# Check exit code
echo "Exit code: $?"

# Validate output format
echo '{"event": "test"}' | ./hook.sh | jq .
```

### Test Commands Safely

```bash
# Dry run with echo
echo "Would run: rm -rf $path"

# Test with single file first
ls target_directory | head -1 | xargs command

# Use --dry-run flags when available
rsync --dry-run source/ dest/
```

### Test MCP Tools

```bash
# List available tools
/mcp

# Test with minimal input
mcp__server__tool '{"minimal": "input"}'

# Check tool description matches behavior
claude mcp get server-name
```

---

## Checklists

### Pre-Operation Checklist

- [ ] Validate all inputs
- [ ] Check file paths exist (for reads)
- [ ] Check directories exist (for writes)
- [ ] Verify permissions are granted
- [ ] Check context has headroom
- [ ] Validate configuration files
- [ ] Test commands in dry-run mode

### Pre-Session Checklist

- [ ] Run `claude doctor` for health check
- [ ] Verify credentials are valid
- [ ] Check MCP servers are running
- [ ] Validate hooks are configured correctly
- [ ] Review permissions settings
- [ ] Check available disk space
- [ ] Clear old session data if needed

### Pre-Release Checklist

- [ ] All hooks tested locally
- [ ] All configurations validated
- [ ] All MCP servers tested
- [ ] Permissions documented
- [ ] Error handling verified
- [ ] Recovery procedures tested
- [ ] Documentation updated

---

## Common Prevention Patterns

### Pattern: Check-Then-Act

```javascript
// Check conditions before acting
if (await canPerformAction()) {
  await performAction();
} else {
  throw new Error('Prerequisites not met');
}
```

### Pattern: Prepare Environment

```javascript
// Ensure environment is ready
async function prepareEnvironment() {
  await createRequiredDirectories();
  await validateConfigurations();
  await checkDependencies();
  await warmupConnections();
}
```

### Pattern: Validate Early

```javascript
// Validate at entry point, not deep in code
function apiHandler(request) {
  validateRequest(request); // Throws if invalid

  // Rest of code can assume valid input
  const result = processRequest(request);
  return result;
}
```

### Pattern: Fail Fast

```javascript
// Check for problems immediately
function processFile(path) {
  // Fail fast on obvious issues
  if (!path) throw new Error('Path required');
  if (!path.endsWith('.json')) throw new Error('Must be JSON file');
  if (!fileExists(path)) throw new Error('File not found');

  // Only proceed if all checks pass
  const content = readFile(path);
  return JSON.parse(content);
}
```
