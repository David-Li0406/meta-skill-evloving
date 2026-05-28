# Monorepo Management - Validations

## Missing workspace protocol

### **Id**
no-workspace-protocol
### **Severity**
info
### **Type**
regex
### **Pattern**
  - "@repo/.*":\s*"\^
  - "@monorepo/.*":\s*"\^
### **Message**
Use workspace:* for internal packages
### **Fix Action**
Replace version with workspace:*
### **Applies To**
  - package.json

## Build task without outputs

### **Id**
missing-outputs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - "build":\s*\{[^}]*(?!"outputs")
### **Message**
Build tasks should define outputs for caching
### **Fix Action**
Add outputs array to task config
### **Applies To**
  - turbo.json