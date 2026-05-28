# Docs Engineer - Validations

## Project Without README

### **Id**
missing-readme
### **Severity**
error
### **Type**
regex
### **Pattern**
  - setup\.py(?!.*README)
  - package\.json(?!.*README)
### **Message**
Project missing README file.
### **Fix Action**
Add README.md with quick start and basic usage
### **Applies To**
  - **/setup.py
  - **/package.json

## README Without Installation Instructions

### **Id**
readme-no-installation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - README\.md(?!.*install|.*pip|.*npm)
### **Message**
README missing installation instructions.
### **Fix Action**
Add ## Installation section with install command
### **Applies To**
  - **/README.md

## Hardcoded Secret in Documentation

### **Id**
hardcoded-secret-in-docs
### **Severity**
error
### **Type**
regex
### **Pattern**
  - api_key\s*=\s*["']sk-[^"']+["']
  - password\s*=\s*["'][^"']{8,}["']
  - token\s*=\s*["'][A-Za-z0-9]{20,}["']
### **Message**
Documentation contains what looks like a real secret.
### **Fix Action**
Use placeholder or env var: api_key = os.environ['API_KEY']
### **Applies To**
  - **/*.md
  - **/docs/**/*

## Reference to Non-Existent File

### **Id**
dead-link-reference
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \[.*\]\(\./[^)]+\.md\)
  - \[.*\]\(\.\./[^)]+\.md\)
### **Message**
Markdown link to relative file. Verify file exists.
### **Fix Action**
Check that linked file exists, or use absolute URL
### **Applies To**
  - **/*.md

## API Documentation Without Code Example

### **Id**
no-code-example
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ## API(?!.*```)
  - ### Method(?!.*```)
  - ## Usage(?!.*```)
### **Message**
API documentation section without code example.
### **Fix Action**
Add code example showing usage
### **Applies To**
  - **/*.md
  - **/docs/**/*

## Reference to Old Version

### **Id**
outdated-version-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - v[0-9]+\.[0-9]+\.[0-9]+(?!.*current|.*latest)
  - version [0-9]+\.[0-9]+\.[0-9]+
### **Message**
Version number in docs. May become outdated.
### **Fix Action**
Use 'current version' or automate version replacement
### **Applies To**
  - **/*.md

## TODO in Published Documentation

### **Id**
todo-in-docs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TODO:
  - FIXME:
  - \[WIP\]
  - Coming soon
### **Message**
Incomplete section in documentation.
### **Fix Action**
Complete the section or remove placeholder
### **Applies To**
  - **/*.md
  - **/docs/**/*

## Very Long Paragraph Without Break

### **Id**
long-paragraph
### **Severity**
info
### **Type**
regex
### **Pattern**
  - [^\n]{500,}
### **Message**
Very long paragraph. Consider breaking up for readability.
### **Fix Action**
Split into shorter paragraphs or use bullet points
### **Applies To**
  - **/*.md

## Documentation Without Headings

### **Id**
no-heading-structure
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!#).*\n(?!#).*\n(?!#).*\n(?!#).*\n(?!#).*\n(?!#).*\n(?!#).*
### **Message**
Large section without headings. Add structure.
### **Fix Action**
Add section headings for better navigation
### **Applies To**
  - **/*.md

## Unclosed Code Block

### **Id**
broken-code-block
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ```[^`]*$
  - ```\w+[^`]*```[^`]*```
### **Message**
Code block may not be properly closed.
### **Fix Action**
Ensure all code blocks have opening and closing ```
### **Applies To**
  - **/*.md

## Project Without Changelog

### **Id**
missing-changelog
### **Severity**
info
### **Type**
regex
### **Pattern**
  - version.*bump(?!.*CHANGELOG|.*changelog)
### **Message**
Version change without changelog update.
### **Fix Action**
Add CHANGELOG.md entry for version changes
### **Applies To**
  - **/*.py
  - **/package.json

## Public Function Without Documentation

### **Id**
undocumented-public-api
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def [a-z][^_].*\):\s*\n\s+[^"']
  - export function [a-z].*\{(?!.*\*|.*//)
### **Message**
Public function without docstring or comment.
### **Fix Action**
Add documentation explaining purpose and usage
### **Applies To**
  - **/*.py
  - **/*.ts