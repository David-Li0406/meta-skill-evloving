# Ios Swift Specialist - Validations

## Force Unwrap in Production

### **Id**
force-unwrap
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?<!!)!(?![=!])
  - \.unwrap\(\)
### **Message**
Force unwrapping crashes when value is nil.
### **Fix Action**
Use guard-let, if-let, or nil coalescing
### **Applies To**
  - **/*.swift
### **Excludes**
  - **/Tests/**
  - **/XCTests/**

## Strong Self in Escaping Closure

### **Id**
strong-self-closure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - { self\.
  - completion = \{(?!.*weak)
### **Message**
Strong self in closure may cause retain cycle.
### **Fix Action**
Use [weak self] or [unowned self]
### **Applies To**
  - **/*.swift

## UI Update from Background Thread

### **Id**
main-thread-ui
### **Severity**
error
### **Type**
regex
### **Pattern**
  - DispatchQueue\.global.*self\..*view
  - async.*\{.*self\.view
### **Message**
UI updates must be on main thread.
### **Fix Action**
Use @MainActor or DispatchQueue.main
### **Applies To**
  - **/*.swift

## Sensitive Data in UserDefaults

### **Id**
userdefaults-sensitive
### **Severity**
error
### **Type**
regex
### **Pattern**
  - UserDefaults.*token
  - UserDefaults.*password
  - UserDefaults.*secret
  - UserDefaults.*key
### **Message**
Sensitive data should use Keychain, not UserDefaults.
### **Fix Action**
Use KeychainAccess or Security framework
### **Applies To**
  - **/*.swift

## Print Statement in Production

### **Id**
print-statement
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - print\(
  - debugPrint\(
### **Message**
Print statements impact performance and expose data.
### **Fix Action**
Use os.log or structured logging
### **Applies To**
  - **/*.swift
### **Excludes**
  - **/Tests/**
  - **/Debug/**

## Force Try

### **Id**
try-force
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - try!
### **Message**
Force try crashes on error.
### **Fix Action**
Use do-catch or try?
### **Applies To**
  - **/*.swift
### **Excludes**
  - **/Tests/**

## Implicitly Unwrapped Optional

### **Id**
implicitly-unwrapped
### **Severity**
info
### **Type**
regex
### **Pattern**
  - : [A-Z][a-zA-Z]+!
### **Message**
Implicitly unwrapped optionals are risky outside IBOutlets.
### **Fix Action**
Use regular optional or ensure initialization
### **Applies To**
  - **/*.swift

## Class Where Struct Would Work

### **Id**
class-over-struct
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class [A-Z][a-zA-Z]+(?!.*:.*ViewController|.*:.*View)
### **Message**
Consider struct for value types (no inheritance needed).
### **Fix Action**
Use struct for data models without identity
### **Applies To**
  - **/Models/**/*.swift

## Large View Controller

### **Id**
massive-view-controller
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*ViewController.*\{[\s\S]{5000,}
### **Message**
Large view controller violates single responsibility.
### **Fix Action**
Extract to view model, coordinators, child VCs
### **Applies To**
  - **/*ViewController.swift

## String-Based Identifier

### **Id**
stringly-typed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - performSegue.*"[^"]+"
  - dequeueReusableCell.*"[^"]+"
  - Notification\.Name\("
### **Message**
String identifiers are error-prone.
### **Fix Action**
Use static constants or generated identifiers
### **Applies To**
  - **/*.swift

## Deprecated iOS API

### **Id**
deprecated-api
### **Severity**
info
### **Type**
regex
### **Pattern**
  - UIApplication\.shared\.keyWindow
  - statusBarStyle
  - topLayoutGuide
  - bottomLayoutGuide
### **Message**
Using deprecated API that may be removed.
### **Fix Action**
Use modern equivalent (see Apple documentation)
### **Applies To**
  - **/*.swift

## Async Without Task Management

### **Id**
async-no-task
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Task \{(?!.*cancel)
  - Task\.init
### **Message**
Task without cancellation handling may leak.
### **Fix Action**
Store Task and cancel in deinit/disappear
### **Applies To**
  - **/*.swift