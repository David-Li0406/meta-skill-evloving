# Claude Code Hooks - Validations

## Hook Exit Without Message

### **Id**
missing-error-message
### **Severity**
high
### **Type**
regex
### **Pattern**
exit\s+1\s*["\)]
### **Negative Pattern**
echo.*exit 1|printf.*exit 1
### **Message**
Hook exits with error but no message. Claude won't know why it was blocked.
### **Fix Action**
Add echo message before exit: echo 'BLOCKED: reason' && exit 1
### **Applies To**
  - *.json
  - .claude/settings*.json

## Regex Pattern in Matcher

### **Id**
regex-in-matcher
### **Severity**
high
### **Type**
regex
### **Pattern**
matcher.*\\\\[dswDSW+*?]|matcher.*\\.\\*|matcher.*\\[.*\\]
### **Message**
Hook matcher uses regex syntax. Matchers use glob patterns, not regex.
### **Fix Action**
Use glob patterns: Bash(git*) not Bash(git\s+.*)
### **Applies To**
  - *.json
  - .claude/settings*.json

## Complex Inline Command

### **Id**
long-inline-command
### **Severity**
medium
### **Type**
regex
### **Pattern**
"command":\s*"[^"]{150,}"
### **Message**
Hook command is very long. Complex logic should be in external scripts.
### **Fix Action**
Move complex logic to a script file: ./scripts/hook-name.sh
### **Applies To**
  - *.json
  - .claude/settings*.json

## Chained Commands Without Error Handling

### **Id**
chained-commands-no-error
### **Severity**
medium
### **Type**
regex
### **Pattern**
&&[^|]*&&[^|]*&&
### **Negative Pattern**
\|\|.*exit|\|\|.*echo
### **Message**
Multiple chained commands without error handling. Middle failures are silent.
### **Fix Action**
Add || exit 1 or use set -e in script
### **Applies To**
  - *.json
  - .claude/settings*.json
  - *.sh

## Hardcoded Temp Path Without Session

### **Id**
hardcoded-tmp-path
### **Severity**
medium
### **Type**
regex
### **Pattern**
/tmp/[a-zA-Z-]+[^$]
### **Negative Pattern**
\$SESSION_ID|\$\{SESSION_ID\}
### **Message**
Hardcoded /tmp path may conflict across sessions. Consider session-scoped paths.
### **Fix Action**
Use session ID: /tmp/marker-$SESSION_ID
### **Applies To**
  - *.json
  - .claude/settings*.json

## Potentially Long-Running Synchronous Command

### **Id**
sync-long-command
### **Severity**
medium
### **Type**
regex
### **Pattern**
npm run (test|build|e2e|lint)[^&]*["\)]|npm test[^&]*["\)]
### **Negative Pattern**
--bail|--passWithNoTests|timeout
### **Message**
Full test/build may timeout. Consider --bail or async patterns.
### **Fix Action**
Add --bail for early exit or run in background
### **Applies To**
  - *.json
  - .claude/settings*.json

## Variable Used Without Null Check

### **Id**
missing-null-check
### **Severity**
low
### **Type**
regex
### **Pattern**
\$TOOL_INPUT[A-Z_]+[^}]
### **Negative Pattern**
-n.*\$TOOL|-z.*\$TOOL|\$\{TOOL_[^:]+:-
### **Message**
Environment variable used without null check. May fail silently if undefined.
### **Fix Action**
Add null check: [ -n "$VAR" ] && ... or ${VAR:-default}
### **Applies To**
  - *.json
  - .claude/settings*.json
  - *.sh

## Hooks in Non-Settings File

### **Id**
hooks-in-wrong-file
### **Severity**
low
### **Type**
regex
### **Pattern**
"hooks"\s*:\s*\{
### **Message**
Hooks found in file - ensure this is .claude/settings.json or .claude/settings.local.json
### **Fix Action**
Move hooks to .claude/settings.json (shared) or .claude/settings.local.json (personal)
### **Applies To**
  - *.json
### **Excludes**
  - .claude/settings.json
  - .claude/settings.local.json
  - **/package.json
  - **/tsconfig.json

## Overly Broad Matcher

### **Id**
blocking-all-tools
### **Severity**
medium
### **Type**
regex
### **Pattern**
"matcher"\s*:\s*"(Write|Edit|Bash)"[^(]
### **Message**
Matcher blocks ALL uses of this tool. Consider more specific patterns.
### **Fix Action**
Add path/command pattern: Write(*.env*) or Bash(rm*)
### **Applies To**
  - *.json
  - .claude/settings*.json

## Old Hook Configuration Syntax

### **Id**
deprecated-hook-syntax
### **Severity**
low
### **Type**
regex
### **Pattern**
"preToolUse"|"postToolUse"|"sessionStart"
### **Message**
Hook key should be PascalCase: PreToolUse, PostToolUse, SessionStart
### **Fix Action**
Use PascalCase keys in hooks configuration
### **Applies To**
  - *.json
  - .claude/settings*.json