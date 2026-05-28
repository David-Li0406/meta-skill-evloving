# I18N - Validations

## Hardcoded user-facing string

### **Id**
hardcoded-string
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <(button|h[1-6]|p|span|label)>[A-Z][a-z]+
### **Message**
User-facing strings should use translations
### **Fix Action**
Replace with t('key')
### **Applies To**
  - *.tsx
  - *.jsx

## Manual date formatting

### **Id**
manual-date-format
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - getMonth\(\).*getDate\(\)
  - toLocaleDateString\(\)
### **Message**
Use Intl.DateTimeFormat for locale-aware dates
### **Fix Action**
Use useFormatter() or Intl.DateTimeFormat
### **Applies To**
  - *.tsx
  - *.ts

## String concatenation in translations

### **Id**
string-concatenation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - t\([^)]+\)\s*\+\s*
  - \+\s*t\([^)]+\)
### **Message**
Use ICU message format instead of concatenation
### **Fix Action**
Use interpolation: t('key', { var })
### **Applies To**
  - *.tsx
  - *.jsx