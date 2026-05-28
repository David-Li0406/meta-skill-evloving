# Expo - Validations

## Missing URL Scheme

### **Id**
missing-scheme
### **Severity**
medium
### **Type**
regex
### **Pattern**
"expo"\s*:\s*\{
### **Negative Pattern**
"scheme"\s*:
### **Message**
App should have URL scheme for deep linking.
### **Fix Action**
Add 'scheme': 'myapp' to expo config
### **Applies To**
  - app.json
  - app.config.js

## Hardcoded API Key in Config

### **Id**
hardcoded-api-key
### **Severity**
high
### **Type**
regex
### **Pattern**
(apiKey|API_KEY|secret)["']?\s*[:=]\s*["'][a-zA-Z0-9_-]{20,}
### **Message**
API keys should not be hardcoded. Use environment variables.
### **Fix Action**
Use EAS secrets or expo-constants for runtime config
### **Applies To**
  - *.json
  - *.js
  - *.ts

## Missing Error Boundary

### **Id**
no-error-boundary
### **Severity**
medium
### **Type**
regex
### **Pattern**
export default function \w+Layout
### **Negative Pattern**
ErrorBoundary
### **Message**
Root layout should have error boundary for crash protection.
### **Fix Action**
Add ErrorBoundary component to catch rendering errors
### **Applies To**
  - _layout.tsx
  - _layout.js

## Console Logs in Production Code

### **Id**
console-log-production
### **Severity**
low
### **Type**
regex
### **Pattern**
console\.(log|debug|info)\(
### **Negative Pattern**
__DEV__|if.*DEV
### **Message**
Console logs should be wrapped in __DEV__ check.
### **Fix Action**
Use if (__DEV__) console.log() or remove
### **Applies To**
  - *.tsx
  - *.ts
  - *.jsx
  - *.js

## Using React Native Image for Remote

### **Id**
react-native-image
### **Severity**
medium
### **Type**
regex
### **Pattern**
import.*Image.*from ['"]react-native['"]
### **Message**
expo-image is faster and has caching for remote images.
### **Fix Action**
Use Image from 'expo-image' for remote images
### **Applies To**
  - *.tsx
  - *.jsx

## FlatList Without keyExtractor

### **Id**
flatlist-no-keyextractor
### **Severity**
medium
### **Type**
regex
### **Pattern**
<FlatList[^>]*data=
### **Negative Pattern**
keyExtractor
### **Message**
FlatList needs keyExtractor for performance.
### **Fix Action**
Add keyExtractor={(item) => item.id}
### **Applies To**
  - *.tsx
  - *.jsx

## Missing Splash Screen Config

### **Id**
no-splash-config
### **Severity**
low
### **Type**
regex
### **Pattern**
"expo"\s*:
### **Negative Pattern**
"splash"\s*:
### **Message**
App should have splash screen configuration.
### **Fix Action**
Add splash configuration with image and backgroundColor
### **Applies To**
  - app.json

## Missing Runtime Version for Updates

### **Id**
no-runtime-version
### **Severity**
medium
### **Type**
regex
### **Pattern**
"updates"\s*:
### **Negative Pattern**
"runtimeVersion"\s*:
### **Message**
EAS Updates needs runtimeVersion configured.
### **Fix Action**
Add runtimeVersion policy in expo config
### **Applies To**
  - app.json
  - app.config.js