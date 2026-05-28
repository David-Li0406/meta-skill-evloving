# Mcp Testing - Validations

## No Test Files Found

### **Id**
mcp-no-test-files
### **Severity**
warning
### **Type**
regex
### **Pattern**
setRequestHandler
### **Negative Pattern**
\.test\.|\.spec\.|__tests__|/tests/
### **Message**
MCP server without test files. Tests are critical for MCP reliability.
### **Fix Action**
Create test files: *.test.ts or *.spec.ts
### **Applies To**
  - *.ts
  - *.js

## Missing Error Case Tests

### **Id**
mcp-no-error-case-tests
### **Severity**
warning
### **Type**
regex
### **Pattern**
describe.*|it\s*\(
### **Negative Pattern**
error|Error|invalid|Invalid|reject|fail
### **Message**
Tests may lack error case coverage. Test invalid inputs and error paths.
### **Fix Action**
Add tests for invalid inputs, missing fields, and error conditions
### **Applies To**
  - *.test.ts
  - *.spec.ts

## Tests With Only Mocks

### **Id**
mcp-only-mocks
### **Severity**
info
### **Type**
regex
### **Pattern**
mock|Mock|jest\.fn|vi\.fn
### **Negative Pattern**
integration|Integration|e2e|E2E|real|Real
### **Message**
Tests use mocks heavily. Consider adding integration tests.
### **Fix Action**
Add integration tests that test real server behavior
### **Applies To**
  - *.test.ts
  - *.spec.ts

## Missing Schema Tests

### **Id**
mcp-no-schema-tests
### **Severity**
warning
### **Type**
regex
### **Pattern**
inputSchema
### **Negative Pattern**
validateSchema|schemaTest|schema.*test
### **Message**
Tool schemas defined but not tested. Invalid schemas cause runtime errors.
### **Fix Action**
Add tests validating all tool schemas
### **Applies To**
  - *.ts
  - *.js