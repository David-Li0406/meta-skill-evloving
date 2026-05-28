# Personal Tool Builder - Validations

## Hardcoded Absolute Paths

### **Id**
hardcoded-paths
### **Severity**
medium
### **Type**
regex
### **Pattern**
["']/Users/|["']C:\\\\Users\\\\|["']/home/
### **File Patterns**
  - *.js
  - *.ts
  - *.py
### **Message**
Hardcoded absolute path - use homedir() or environment variables.
### **Fix Action**
Use os.homedir() or path.join for portable paths

## Hardcoded Credentials

### **Id**
credentials-in-code
### **Severity**
critical
### **Type**
regex
### **Pattern**
(api[_-]?key|secret|token|password)\s*[=:]\s*["\x27][a-zA-Z0-9_\-]{10,}["\x27]
### **File Patterns**
  - *.js
  - *.ts
  - *.py
  - *.json
### **Message**
Potential hardcoded credential - use environment variables or config file.
### **Fix Action**
Move to process.env.VAR or external config file (gitignored)

## Server Bound to All Interfaces

### **Id**
network-exposed-server
### **Severity**
high
### **Type**
regex
### **Pattern**
listen\([^)]*['"]0\.0\.0\.0['"]|listen\([^)]*,\s*null
### **File Patterns**
  - *.js
  - *.ts
### **Message**
Server exposed to network - bind to localhost for personal tools.
### **Fix Action**
Use '127.0.0.1' or 'localhost' instead of '0.0.0.0'

## Missing Error Handling

### **Id**
no-error-handling
### **Severity**
medium
### **Type**
regex
### **Pattern**
\.(readFileSync|writeFileSync|execSync)\([^)]+\)(?!.*catch)
### **File Patterns**
  - *.js
  - *.ts
### **Message**
Sync operation without error handling - wrap in try/catch.
### **Fix Action**
Add try/catch for graceful error messages

## CLI Without Help

### **Id**
no-help-command
### **Severity**
low
### **Type**
conceptual
### **Check**
CLI should have --help option
### **Indicators**
  - No usage instructions
  - Unclear how to use
  - Missing command documentation
### **Message**
CLI has no help - future you will forget how to use it.
### **Fix Action**
Add .description() and --help to CLI commands

## Tool Without README

### **Id**
no-readme
### **Severity**
low
### **Type**
conceptual
### **Check**
Personal tools should have basic README
### **Indicators**
  - No README.md file
  - README missing purpose
  - No usage examples
### **Message**
No README - document for your future self.
### **Fix Action**
Add README with: what it does, why you built it, how to use it

## Debug Console Logs Left In

### **Id**
console-log-debugging
### **Severity**
low
### **Type**
regex
### **Pattern**
console\.log\(['"]debug|console\.log\(['"]TODO|console\.log\(['"]test
### **File Patterns**
  - *.js
  - *.ts
### **Message**
Debug logging left in code - remove or use proper logging.
### **Fix Action**
Remove debug logs or use a proper logger with levels

## Script Missing Shebang

### **Id**
missing-shebang
### **Severity**
low
### **Type**
conceptual
### **Check**
Executable scripts need shebang
### **Indicators**
  - Script in bin/ without #!/usr/bin/env
  - Python script without shebang
  - Script not executable
### **Message**
Script missing shebang - won't execute directly.
### **Fix Action**
Add #!/usr/bin/env node (or python3) at top of file

## Tool Without Version

### **Id**
no-version
### **Severity**
low
### **Type**
conceptual
### **Check**
Tools should have version numbers
### **Indicators**
  - No --version flag
  - No version in package.json
  - Unclear which version is running
### **Message**
No version tracking - will cause confusion when updating.
### **Fix Action**
Add version to package.json and --version flag