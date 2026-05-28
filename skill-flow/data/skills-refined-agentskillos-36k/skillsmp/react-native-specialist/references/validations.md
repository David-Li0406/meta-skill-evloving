# React Native Specialist - Validations

## Inline Style Object

### **Id**
inline-style-object
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - style=\{\{
  - style=\{[^}]+\}\s*>
### **Message**
Inline style objects create new objects every render.
### **Fix Action**
Use StyleSheet.create() or memoize dynamic styles
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Console.log in Production Code

### **Id**
console-log-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.warn\(
  - console\.error\(
### **Message**
Console statements impact performance in production.
### **Fix Action**
Remove or use babel-plugin-transform-remove-console
### **Applies To**
  - **/src/**/*.ts
  - **/src/**/*.tsx
### **Excludes**
  - **/__tests__/**
  - **/test/**

## Missing Key Prop in List

### **Id**
missing-key-prop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.map\([^)]+\)\s*=>\s*<(?!.*key=)
### **Message**
List items missing key prop causes performance issues.
### **Fix Action**
Add unique key prop to list items
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Large Data in AsyncStorage

### **Id**
async-storage-large-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - AsyncStorage\.setItem.*JSON\.stringify
### **Message**
AsyncStorage has size limits and is slow for large data.
### **Fix Action**
Use MMKV or SQLite for large/complex data
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Animated Value Created in Render

### **Id**
animated-in-render
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Animated\.Value\(
  - useRef\(new Animated\.Value
### **Message**
Creating Animated.Value in render causes issues.
### **Fix Action**
Use useAnimatedValue() or create outside component
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Event Listener Without Cleanup

### **Id**
missing-cleanup
### **Severity**
error
### **Type**
regex
### **Pattern**
  - addListener\([^)]+\)(?!.*remove)
  - addEventListener\([^)]+\)(?!.*removeEventListener)
### **Message**
Event listener without cleanup causes memory leaks.
### **Fix Action**
Return cleanup function from useEffect
### **Applies To**
  - **/*.ts
  - **/*.tsx

## FlatList Without keyExtractor

### **Id**
flatlist-without-keyextractor
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <FlatList(?!.*keyExtractor)
  - <FlashList(?!.*keyExtractor)
### **Message**
List without keyExtractor uses index, causing issues.
### **Fix Action**
Add keyExtractor prop with unique identifier
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Synchronous I/O in Component

### **Id**
sync-io-in-component
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - require\([^)]+\.json\)
  - fs\.readFileSync
### **Message**
Synchronous I/O blocks JS thread.
### **Fix Action**
Use async loading with proper loading states
### **Applies To**
  - **/components/**/*.tsx
  - **/screens/**/*.tsx

## Platform-Specific Style Missing

### **Id**
platform-specific-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - shadowColor(?!.*Platform)
  - elevation(?!.*Platform)
### **Message**
Shadow/elevation without Platform check may not work cross-platform.
### **Fix Action**
Use Platform.select() for shadow/elevation
### **Applies To**
  - **/*.tsx
  - **/*.ts

## Hermes Incompatible Code

### **Id**
hermes-incompatible
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - with\s*\(
  - eval\s*\(
### **Message**
Code pattern not supported by Hermes engine.
### **Fix Action**
Remove with/eval for Hermes compatibility
### **Applies To**
  - **/*.js
  - **/*.ts

## Navigation Without TypeScript

### **Id**
navigation-no-type
### **Severity**
info
### **Type**
regex
### **Pattern**
  - useNavigation\(\)(?!.*<)
  - navigation\.navigate\(
### **Message**
Untyped navigation is error-prone.
### **Fix Action**
Type navigation with RootStackParamList
### **Applies To**
  - **/*.tsx

## Network Image Without Caching

### **Id**
image-no-cache
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <Image.*source=\{\{.*uri:
### **Message**
Built-in Image doesn't cache well. Consider FastImage.
### **Fix Action**
Use react-native-fast-image for better caching
### **Applies To**
  - **/*.tsx
  - **/*.jsx