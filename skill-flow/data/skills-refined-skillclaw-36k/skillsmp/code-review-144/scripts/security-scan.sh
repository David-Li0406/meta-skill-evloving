#!/bin/bash
# Security-focused code scan
# Usage: ./security-scan.sh [directory]

PROJECT_ROOT="/Users/jietaoxie/my-prototype-logistics"
TARGET_DIR="${1:-$PROJECT_ROOT}"

echo "=========================================="
echo "  Security Scan"
echo "=========================================="
echo "Target: $TARGET_DIR"
echo ""

ISSUES_FOUND=0

# 1. Credential Leaks
echo "[1/6] Checking for credential leaks..."
CRED_PATTERNS="password\s*=\s*['\"]|apiKey\s*=\s*['\"]|secret\s*=\s*['\"]|ACCESS_KEY\s*=\s*['\"]"
CRED_RESULTS=$(grep -rn "$CRED_PATTERNS" "$TARGET_DIR" --include="*.ts" --include="*.tsx" --include="*.java" --include="*.properties" 2>/dev/null | grep -v "node_modules" | grep -v ".git" | head -10)

if [ -n "$CRED_RESULTS" ]; then
    echo "  WARNING: Potential hardcoded credentials found:"
    echo "$CRED_RESULTS"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No hardcoded credentials detected"
fi

# 2. Insecure Storage
echo ""
echo "[2/6] Checking for insecure token storage..."
INSECURE_STORAGE=$(grep -rn "AsyncStorage.*token\|localStorage.*token" "$TARGET_DIR" --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null | grep -v "node_modules" | head -5)

if [ -n "$INSECURE_STORAGE" ]; then
    echo "  WARNING: Tokens in insecure storage:"
    echo "$INSECURE_STORAGE"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No insecure token storage"
fi

# 3. SQL Injection
echo ""
echo "[3/6] Checking for SQL injection risks..."
SQL_CONCAT=$(grep -rn "\".*+.*\"\s*[+]" "$TARGET_DIR/backend-java" --include="*.java" 2>/dev/null | grep -i "select\|insert\|update\|delete" | head -5)

if [ -n "$SQL_CONCAT" ]; then
    echo "  WARNING: Potential SQL injection (string concatenation):"
    echo "$SQL_CONCAT"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No obvious SQL injection patterns"
fi

# 4. Command Injection
echo ""
echo "[4/6] Checking for command injection..."
CMD_INJECTION=$(grep -rn "Runtime.getRuntime().exec\|ProcessBuilder\|exec(\s*['\"]" "$TARGET_DIR" --include="*.java" --include="*.ts" 2>/dev/null | head -5)

if [ -n "$CMD_INJECTION" ]; then
    echo "  WARNING: Command execution found (verify input sanitization):"
    echo "$CMD_INJECTION"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No obvious command injection patterns"
fi

# 5. XSS Risks
echo ""
echo "[5/6] Checking for XSS risks..."
XSS_PATTERNS=$(grep -rn "dangerouslySetInnerHTML\|innerHTML\s*=" "$TARGET_DIR" --include="*.tsx" --include="*.jsx" --include="*.ts" 2>/dev/null | grep -v "node_modules" | head -5)

if [ -n "$XSS_PATTERNS" ]; then
    echo "  WARNING: Potential XSS risks:"
    echo "$XSS_PATTERNS"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No innerHTML/dangerouslySetInnerHTML usage"
fi

# 6. Sensitive Data Logging
echo ""
echo "[6/6] Checking for sensitive data in logs..."
LOG_SENSITIVE=$(grep -rn "console\.log.*password\|console\.log.*token\|logger.*password\|logger.*token" "$TARGET_DIR" --include="*.ts" --include="*.tsx" --include="*.java" 2>/dev/null | grep -v "node_modules" | head -5)

if [ -n "$LOG_SENSITIVE" ]; then
    echo "  WARNING: Sensitive data may be logged:"
    echo "$LOG_SENSITIVE"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo "  PASS: No sensitive data in logs"
fi

# Summary
echo ""
echo "=========================================="
if [ "$ISSUES_FOUND" -gt 0 ]; then
    echo "  Security Scan: $ISSUES_FOUND ISSUES FOUND"
    echo "  Please review and fix before deployment"
else
    echo "  Security Scan: PASSED"
fi
echo "=========================================="
