# Angular - Validations

## Component using default change detection

### **Id**
default-change-detection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @Component\s*\(\s*\{(?![\s\S]*changeDetection)[\s\S]*?\}\s*\)
### **Message**
Consider using ChangeDetectionStrategy.OnPush for better performance
### **Fix Action**
Add changeDetection: ChangeDetectionStrategy.OnPush
### **Applies To**
  - *.component.ts

## Method call in template

### **Id**
template-method-call
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{\{\s*\w+\s*\([^)]*\)\s*\}\}
  - \[[\w.]+\]="[^"]*\w+\s*\([^)]*\)[^"]*"
### **Message**
Method calls in templates run on every change detection cycle
### **Fix Action**
Use computed signal, pipe, or pre-compute in component
### **Applies To**
  - *.component.html
  - *.component.ts

## Subscribe without unsubscribe mechanism

### **Id**
subscribe-without-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.subscribe\s*\([^)]+\)(?![\s\S]*takeUntil|[\s\S]*takeUntilDestroyed|[\s\S]*unsubscribe)
### **Message**
Subscription may not be properly cleaned up
### **Fix Action**
Use async pipe, toSignal, takeUntilDestroyed, or manual unsubscribe
### **Applies To**
  - *.component.ts

## Nested subscribe calls

### **Id**
nested-subscribe
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.subscribe\s*\([^}]*\.subscribe\s*\(
### **Message**
Nested subscribes cause callback hell - use RxJS operators
### **Fix Action**
Use switchMap, mergeMap, or forkJoin instead
### **Applies To**
  - *.ts

## Using 'any' type

### **Id**
any-type-usage
### **Severity**
info
### **Type**
regex
### **Pattern**
  - :\s*any\s*[;=\)]
  - <any>
  - as\s+any
### **Message**
Using 'any' bypasses TypeScript benefits
### **Fix Action**
Define proper types or interfaces
### **Applies To**
  - *.ts

## Using == instead of ===

### **Id**
non-strict-equals
### **Severity**
info
### **Type**
regex
### **Pattern**
  - [^!=]==\s*[^=]
  - [^!]==[^=]
### **Message**
Use strict equality (===) for type-safe comparisons
### **Fix Action**
Replace == with ===
### **Applies To**
  - *.ts

## HTTP calls directly in component

### **Id**
logic-in-component
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @Component[\s\S]*HttpClient[\s\S]*\.get\s*\(
  - @Component[\s\S]*HttpClient[\s\S]*\.post\s*\(
### **Message**
HTTP calls should be in services, not components
### **Fix Action**
Move HTTP logic to a dedicated service
### **Applies To**
  - *.component.ts

## NgModule usage in standalone project

### **Id**
ngmodule-in-new-project
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @NgModule\s*\(
### **Message**
Consider using standalone components for new Angular 17+ projects
### **Fix Action**
Migrate to standalone components with imports array
### **Applies To**
  - *.module.ts

## ngFor without trackBy (old syntax)

### **Id**
missing-trackby
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \*ngFor="[^"]*"(?![\s\S]*trackBy)
### **Message**
ngFor without trackBy can cause performance issues
### **Fix Action**
Add trackBy function or migrate to @for with track
### **Applies To**
  - *.html
  - *.component.ts

## @for without track expression

### **Id**
missing-track-in-for
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @for\s*\([^)]+\)\s*\{(?![^}]*track\s)
### **Message**
@for requires a track expression
### **Fix Action**
Add 'track item.id' or 'track $index'
### **Applies To**
  - *.html
  - *.component.ts

## Template-driven form with complex validation

### **Id**
template-driven-complex-form
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ngModel[\s\S]*ngModel[\s\S]*ngModel[\s\S]*ngModel
### **Message**
Consider reactive forms for complex form handling
### **Fix Action**
Migrate to ReactiveFormsModule for better control
### **Applies To**
  - *.html

## Direct innerHTML binding

### **Id**
innerhtml-binding
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \[innerHTML\]="
### **Message**
innerHTML can be an XSS vector - ensure content is sanitized
### **Fix Action**
Use DomSanitizer or avoid innerHTML if possible
### **Applies To**
  - *.html
  - *.component.ts

## Bypassing Angular security

### **Id**
bypass-security
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - bypassSecurityTrust
### **Message**
Bypassing security should be a last resort with trusted content only
### **Fix Action**
Ensure content is from trusted source, document why bypass is needed
### **Applies To**
  - *.ts