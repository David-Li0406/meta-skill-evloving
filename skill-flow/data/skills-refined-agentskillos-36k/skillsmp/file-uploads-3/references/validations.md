# File Uploads - Validations

## Only checking file extension

### **Id**
extension-only-check
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - endsWith\(["\x27]\.(jpg|png|gif)
  - \.split\(["\x27]\.\)["\x27]
### **Message**
Check magic bytes, not just extension
### **Fix Action**
Use file-type library to verify actual type
### **Applies To**
  - *.ts
  - *.js

## User filename used directly in path

### **Id**
user-filename-in-path
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - path\.join.*req\.(body|query)\.filename
  - uploads/.*\+.*filename
### **Message**
Sanitize filenames to prevent path traversal
### **Fix Action**
Use path.basename() and generate safe name
### **Applies To**
  - *.ts
  - *.js