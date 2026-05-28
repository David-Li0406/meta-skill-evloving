#!/usr/bin/env bash
set -euo pipefail

# Test format-message transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing format-message transformation..."

# Test 1: Basic template with two placeholders
echo -n "Test 1: Basic template {role}: {content}... "
result=$(jq -r -f "$TRANSFORM" --arg template "{role}: {content}" "$SCRIPT_DIR/test-input-1.json")
expected='user: Hello world'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: Multiple placeholders (3 fields)
echo -n "Test 2: Multiple placeholders... "
result=$(jq -r -f "$TRANSFORM" --arg template "[{role}] {content} at {timestamp}" "$SCRIPT_DIR/test-input-2.json")
expected='[assistant] I can help with that at 2024-01-01'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 3: Missing field replaced with empty string
echo -n "Test 3: Missing field becomes empty string... "
result=$(jq -r -f "$TRANSFORM" --arg template "{role}: {content}" "$SCRIPT_DIR/test-input-3.json")
expected='system: '
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 4: Nested field paths with dots
echo -n "Test 4: Nested field paths {user.name}... "
result=$(jq -r -f "$TRANSFORM" --arg template "[{user.name}#{user.id}] {message}" "$SCRIPT_DIR/test-input-4.json")
expected='[skogix#123] Testing nested paths'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 5: No placeholders (return template as-is)
echo -n "Test 5: No placeholders returns template... "
result=$(jq -r -f "$TRANSFORM" --arg template "Static text only" "$SCRIPT_DIR/test-input-5.json")
expected='Static text only'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 6: Empty template returns empty string
echo -n "Test 6: Empty template returns empty... "
result=$(jq -r -f "$TRANSFORM" --arg template "" "$SCRIPT_DIR/test-input-6.json")
expected=''
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 7: Field with null value becomes empty string
echo -n "Test 7: Null field becomes empty string... "
result=$(jq -r -f "$TRANSFORM" --arg template "{value} and {other}" "$SCRIPT_DIR/test-input-7.json")
expected=' and data'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 8: Number values converted to string
echo -n "Test 8: Number values converted to string... "
result=$(jq -r -f "$TRANSFORM" --arg template "Count: {count}, Price: {price}" "$SCRIPT_DIR/test-input-8.json")
expected='Count: 42, Price: 19.99'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 9: Boolean values converted to string
echo -n "Test 9: Boolean values converted to string... "
result=$(jq -r -f "$TRANSFORM" --arg template "Active: {active}, Disabled: {disabled}" "$SCRIPT_DIR/test-input-8.json")
expected='Active: true, Disabled: false'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 10: Special characters in template preserved
echo -n "Test 10: Special characters in template... "
result=$(jq -r -f "$TRANSFORM" --arg template "Message: {text} @#\$%!" "$SCRIPT_DIR/test-input-9.json")
expected='Message: Special chars: @#$%^&*() @#$%!'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 11: Zero and empty string as valid values (falsy values)
echo -n "Test 11: Zero and empty string preserved... "
result=$(jq -r -f "$TRANSFORM" --arg template "{zero}|{empty}|{label}" "$SCRIPT_DIR/test-input-10.json")
expected='0||value'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 12: Repeated placeholder (same field multiple times)
echo -n "Test 12: Repeated placeholder... "
result=$(jq -r -f "$TRANSFORM" --arg template "{a} and {b} and {a} again" "$SCRIPT_DIR/test-input-11.json")
expected='first and second and first again'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 13: Field value contains curly braces (not treated as template)
echo -n "Test 13: Field value with curly braces... "
result=$(jq -r -f "$TRANSFORM" --arg template "Name: {name}" "$SCRIPT_DIR/test-input-12.json")
expected='Name: test {curly} braces'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

echo "All format-message tests passed!"
