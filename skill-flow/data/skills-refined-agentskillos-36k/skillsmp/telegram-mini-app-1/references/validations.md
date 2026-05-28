# Telegram Mini App - Validations

## No initData Validation

### **Id**
no-init-validation
### **Severity**
high
### **Type**
conceptual
### **Check**
Backend should validate initData
### **Indicators**
  - No hash validation
  - Trusting initDataUnsafe
  - No server-side verification
### **Message**
Not validating initData - security vulnerability.
### **Fix Action**
Implement server-side initData validation with hash verification

## Missing Telegram Web App Script

### **Id**
no-telegram-script
### **Severity**
high
### **Type**
pattern
### **Check**
Should include Telegram Web App script
### **Pattern**
telegram-web-app\.js
### **Indicators**
  - No Telegram script loaded
  - window.Telegram undefined
  - tg.ready() fails
### **Message**
Telegram Web App script not included.
### **Fix Action**
Add <script src='https://telegram.org/js/telegram-web-app.js'></script>

## Not Calling tg.ready()

### **Id**
no-tg-ready
### **Severity**
medium
### **Type**
pattern
### **Check**
Should call tg.ready() on load
### **Pattern**
tg\.ready\(\)|WebApp\.ready\(\)
### **Indicators**
  - No ready() call
  - App doesn't load properly
  - Telegram shows loading
### **Message**
Not calling tg.ready() - Telegram may show loading state.
### **Fix Action**
Call window.Telegram.WebApp.ready() when app is ready

## Not Using Telegram Theme

### **Id**
no-theme-support
### **Severity**
medium
### **Type**
pattern
### **Check**
Should adapt to Telegram theme
### **Pattern**
tg-theme|themeParams
### **Indicators**
  - Hardcoded colors
  - No theme variables
  - Looks different from Telegram
### **Message**
Not adapting to Telegram theme colors.
### **Fix Action**
Use CSS variables from tg.themeParams for colors

## Missing Viewport Meta Tag

### **Id**
no-viewport-meta
### **Severity**
medium
### **Type**
pattern
### **Check**
Should have mobile viewport meta
### **Pattern**
viewport.*width=device-width
### **Indicators**
  - No viewport meta
  - Zooming issues
  - Layout broken on mobile
### **Message**
Missing viewport meta tag for mobile.
### **Fix Action**
Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>