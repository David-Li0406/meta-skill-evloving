# Technical Writer - Validations

## TODO in Documentation

### **Id**
todo-in-docs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TODO
  - FIXME
  - TBD
  - WIP
  - \[TODO\]
  - \[TBD\]
### **Message**
Incomplete documentation shipped. Finish or remove the TODO.
### **Fix Action**
Complete the section or remove placeholder before publishing
### **Applies To**
  - **/README.md
  - **/docs/**/*.md
  - **/*.mdx

## Potentially Broken Link

### **Id**
broken-link-pattern
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \]\(\s*\)
  - \]\(#\)
  - \]\(http://localhost
  - \]\(\.\./\.\./\.\./\.\.
### **Message**
Link appears broken or temporary. Verify link destination.
### **Fix Action**
Replace with actual URL or remove the link
### **Applies To**
  - **/*.md
  - **/*.mdx

## Hardcoded Version Number

### **Id**
outdated-version-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - v[0-9]+\.[0-9]+\.[0-9]+
  - version [0-9]+\.[0-9]+
  - @[0-9]+\.[0-9]+\.[0-9]+
### **Message**
Hardcoded version in docs. May become outdated. Consider dynamic reference.
### **Fix Action**
Use version variable or clearly mark which version docs apply to
### **Applies To**
  - **/README.md
  - **/docs/**/*.md

## API Endpoint Without Example

### **Id**
no-code-example
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ## (POST|GET|PUT|DELETE|PATCH)\s+/[^\n]+\n\n(?!.*```)
  - ### Endpoint\n\n[^`]+\n\n(?!.*```)
### **Message**
API endpoint documented without code example. Add working example.
### **Fix Action**
Add curl/code example showing actual usage with expected response
### **Applies To**
  - **/docs/**/*.md
  - **/api/**/*.md

## Placeholder Text

### **Id**
placeholder-text
### **Severity**
error
### **Type**
regex
### **Pattern**
  - lorem ipsum
  - foo bar baz
  - example\.com(?!/)
  - your-.*-here
  - REPLACE_ME
  - INSERT_.*_HERE
### **Message**
Placeholder text in documentation. Replace with real content.
### **Fix Action**
Replace placeholders with actual values or realistic examples
### **Applies To**
  - **/*.md
  - **/*.mdx
### **Exceptions**
  - example\.com/[a-z]

## Tutorial Without Prerequisites

### **Id**
missing-prerequisites
### **Severity**
info
### **Type**
regex
### **Pattern**
  - # Getting Started\n\n(?!.*Prerequisites|.*Requirements|.*Before)
  - ## Quick Start\n\n(?!.*need|.*require|.*install)
### **Message**
Tutorial may be missing prerequisites section.
### **Fix Action**
Add Prerequisites section listing required tools, accounts, knowledge
### **Applies To**
  - **/README.md
  - **/docs/**/getting-started.md
  - **/docs/**/quickstart.md

## Public Function Without Example

### **Id**
jsdoc-no-example
### **Severity**
info
### **Type**
regex
### **Pattern**
  - /\*\*[^*]*@public[^*]*\*/\s*(?!.*@example)
  - /\*\*[^*]*@export[^*]*\*/\s*(?!.*@example)
### **Message**
Public/exported function without @example in JSDoc.
### **Fix Action**
Add @example showing typical usage
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - @example

## Comment Explaining What Instead of Why

### **Id**
comment-what-not-why
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // (loop|iterate|check|get|set|return|call|create|add|remove|delete)s? (the|a|an)? \w+
  - // (increment|decrement|initialize|update|fetch) 
### **Message**
Comment explains what code does (visible in code). Consider explaining why.
### **Fix Action**
Either remove comment or change to explain why/context
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## README Without Quick Start

### **Id**
readme-no-quickstart
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*Quick Start|.*Getting Started|.*Installation|.*Usage)
### **Message**
README may be missing quick start section.
### **Fix Action**
Add Quick Start section showing minimal working example
### **Applies To**
  - **/README.md
### **Exceptions**
  - Getting Started|Quick Start|Installation|Usage

## Marketing Language in Technical Docs

### **Id**
marketing-in-docs
### **Severity**
info
### **Type**
regex
### **Pattern**
  - best-in-class
  - world-class
  - cutting-edge
  - revolutionary
  - game-changing
  - seamless
  - powerful and flexible
  - unlike the competition
### **Message**
Marketing language in technical docs. Keep docs factual and practical.
### **Fix Action**
Remove marketing language. Focus on what it does and how to use it.
### **Applies To**
  - **/docs/**/*.md
  - **/api/**/*.md

## Potential Dead Link

### **Id**
dead-link-indicator
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \]\(.*\.(html|htm)\)
  - \]\(https?://[^)]+/wiki/[^)]+\)
  - \]\([^)]*github\.com[^)]*blob/[^)]+\)
### **Message**
External link that may break over time. Consider archiving or removing.
### **Fix Action**
Verify link works. For critical docs, consider web.archive.org backup
### **Applies To**
  - **/*.md

## Screenshot That May Need Updates

### **Id**
screenshot-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - !\[.*\]\(.*screenshot.*\)
  - !\[.*\]\(.*\.png\)
  - !\[.*\]\(.*\.gif\)
  - <img.*src=.*screenshot
### **Message**
Documentation contains screenshots which may become outdated.
### **Fix Action**
Ensure screenshots are current. Consider if text description would suffice.
### **Applies To**
  - **/*.md
  - **/*.mdx

## Environment Variable Without Documentation

### **Id**
undocumented-env-var
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process\.env\.[A-Z_]+(?!.*//.*description)
  - Deno\.env\.get\(['"][A-Z_]+['"]\)
### **Message**
Environment variable used without nearby documentation.
### **Fix Action**
Document env vars in .env.example or README with description
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - NODE_ENV|PATH|HOME|PWD

## Dated Comment That May Be Stale

### **Id**
stale-comment-date
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // (TODO|FIXME|HACK).*20[0-2][0-9]
  - # (TODO|FIXME|HACK).*20[0-2][0-9]
  - <!-- .*20[0-2][0-2].*-->
### **Message**
Comment with date that may indicate stale content.
### **Fix Action**
Review if this is still relevant. Fix or remove.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.md

## Deprecated Without Alternative

### **Id**
deprecated-no-alternative
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @deprecated(?!.*use|.*see|.*replaced|.*instead)
  - DEPRECATED(?!.*use|.*see|.*replaced|.*instead)
### **Message**
Marked as deprecated but doesn't suggest alternative.
### **Fix Action**
Add 'Use X instead' or link to migration guide
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.md

## README Without License Reference

### **Id**
readme-no-license
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*LICENSE|.*license|.*MIT|.*Apache|.*GPL)
### **Message**
README may be missing license information.
### **Fix Action**
Add License section or link to LICENSE file
### **Applies To**
  - **/README.md
### **Exceptions**
  - LICENSE|license|MIT|Apache|GPL|BSD

## Error Documentation Without Solution

### **Id**
error-doc-no-solution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ## Error:.*\n\n(?!.*fix|.*solution|.*resolve|.*cause)
  - ### .*Error\n\n(?!.*fix|.*solution|.*resolve|.*cause)
### **Message**
Error documented without fix or explanation.
### **Fix Action**
Add Cause and Fix sections to error documentation
### **Applies To**
  - **/docs/**/*.md
  - **/TROUBLESHOOTING.md