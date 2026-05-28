# Prompt To Game - Validations

## Eval Usage

### **Id**
eval-usage
### **Pattern**
eval\s*\([^)]*\)
### **Severity**
error
### **Message**
eval() detected - critical security vulnerability
### **Fix**
Remove eval and use safe alternatives like JSON.parse for data
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - eval(userInput)
    - eval(`code ${variable}`)
  #### **Should Not Match**
    - JSON.parse(userInput)
    - // eval is dangerous

## Exposed Api Key

### **Id**
exposed-api-key
### **Pattern**
(?:api[_-]?key|secret|token|password)\s*[=:]\s*["'][a-zA-Z0-9_-]{16,}["']
### **Severity**
error
### **Message**
Hardcoded secret detected - use environment variables
### **Fix**
Move to .env file and access via process.env
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - apiKey = "sk-1234567890abcdef"
    - API_SECRET: 'abcdefghijklmnop'
  #### **Should Not Match**
    - apiKey = process.env.API_KEY
    - const key = getSecret()

## Innerhtml Assignment

### **Id**
innerhtml-assignment
### **Pattern**
\.innerHTML\s*=\s*[^"'`]
### **Severity**
warning
### **Message**
innerHTML with variable - potential XSS vulnerability
### **Fix**
Use textContent or sanitize input
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - element.innerHTML = userInput
    - div.innerHTML = getMessage()
  #### **Should Not Match**
    - element.innerHTML = "<b>static</b>"
    - element.textContent = userInput

## No Framework Version

### **Id**
no-framework-version
### **Pattern**
import.*(?:phaser|three|kaboom)(?!.*@)
### **Severity**
info
### **Message**
Framework import without version pin - may cause issues
### **Fix**
Pin version in package.json or specify in prompt
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - import Phaser from 'phaser'
    - import * as THREE from 'three'
  #### **Should Not Match**
    - import Phaser from 'phaser@3.90.0'

## Global Variable Pollution

### **Id**
global-variable-pollution
### **Pattern**
^(?:var|let|const)\s+\w+\s*=
### **Severity**
warning
### **Message**
Top-level variable may pollute global scope
### **Fix**
Wrap in module, class, or IIFE
### **Applies To**
  - *.js
### **Test Cases**
  #### **Should Match**
    - var game = new Phaser.Game()
    - let score = 0
  #### **Should Not Match**
    - class Game { score = 0 }
    - export const game = new Game()

## Console Log Production

### **Id**
console-log-production
### **Pattern**
console\.(log|debug|info)\s*\(
### **Severity**
info
### **Message**
Console log may be leftover from debugging
### **Fix**
Remove or guard with development check
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - console.log('debug')
    - console.debug(data)
  #### **Should Not Match**
    - console.error('critical')
    - // console.log('removed')

## Single File Too Large

### **Id**
single-file-too-large
### **Pattern**
.{20000,}
### **Severity**
warning
### **Message**
File likely exceeds maintainable size - consider splitting
### **Fix**
Refactor into separate modules by concern
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**

  #### **Should Not Match**


## Deep Nesting

### **Id**
deep-nesting
### **Pattern**
{\s*{\s*{\s*{\s*{
### **Severity**
warning
### **Message**
Deep nesting detected - hard to maintain and debug
### **Fix**
Extract nested logic into separate functions
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - if (a) { if (b) { if (c) { if (d) { if (e) {
  #### **Should Not Match**
    - if (a) { if (b) { } }

## Magic Number

### **Id**
magic-number
### **Pattern**
(?:width|height|speed|damage|health)\s*[=:]\s*\d{2,}
### **Severity**
info
### **Message**
Magic number detected - consider using named constant
### **Fix**
Extract to CONFIG object or constant
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - width = 800
    - playerSpeed: 200
  #### **Should Not Match**
    - width = CONFIG.SCREEN_WIDTH
    - const PLAYER_SPEED = 200

## Missing Error Handling

### **Id**
missing-error-handling
### **Pattern**
fetch\s*\([^)]*\)(?!\.then.*\.catch|.*try)
### **Severity**
warning
### **Message**
fetch without error handling
### **Fix**
Add .catch() or wrap in try/catch
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - fetch(url)
    - fetch(url).then(r => r.json())
  #### **Should Not Match**
    - fetch(url).then().catch()
    - try { await fetch(url) }

## Browser Api In Shared

### **Id**
browser-api-in-shared
### **Pattern**
(?:window|document|localStorage)\.
### **Severity**
info
### **Message**
Browser-only API - ensure not used in Node.js context
### **Fix**
Add runtime check or isolate to browser-only files
### **Applies To**
  - *.js
  - *.ts
### **Test Cases**
  #### **Should Match**
    - window.innerWidth
    - document.querySelector
    - localStorage.getItem
  #### **Should Not Match**
    - // window.innerWidth
    - if (typeof window !== 'undefined')