# Docs Engineer - Sharp Edges

## Broken Examples

### **Id**
broken-examples
### **Summary**
Code examples in docs don't actually work
### **Severity**
critical
### **Situation**
Publishing documentation with code samples
### **Why**
  User copies example. Gets error. Loses trust immediately.
  "If the docs are wrong, what else is wrong?"
  One broken example destroys documentation credibility.
  
### **Solution**
  1. Test examples automatically:
     # pytest-doctest runs examples from markdown
     pytest --doctest-modules docs/
  
  2. Use extract-and-run pattern:
     ```python
     # filename: examples/quickstart.py
     from mind import Agent
     agent = Agent("test")
     ```
     # CI runs all examples/*.py
  
  3. Use versioned examples:
     # Link examples to specific version
     # ```python <!-- mind==5.0.0 -->
  
  4. Add example to CI matrix:
     # Test examples against all supported Python versions
  
### **Symptoms**
  
---
    ##### **User Issues**
Example doesn't work
  
---
ImportError, NameError in copied examples
  
---
Examples use deprecated APIs
### **Detection Pattern**
example|sample.*code|```python

## Version Drift

### **Id**
version-drift
### **Summary**
Docs describe old version, users run new version
### **Severity**
high
### **Situation**
Documentation not updated with releases
### **Why**
  API changed in v5.2. Docs still show v5.0 patterns.
  User follows docs. Gets deprecation warnings or errors.
  "These docs are useless" - user goes to Stack Overflow instead.
  
### **Solution**
  1. Version your docs:
     # docs.memory-service.io/v5.0/
     # docs.memory-service.io/v5.1/
     # docs.memory-service.io/latest/
  
  2. Include version badges:
     ![Version](https://img.shields.io/badge/version-5.0-blue)
  
  3. Add "since" annotations:
     ## `memory.consolidate()`
     _Available since v5.1_
  
  4. Require docs update in PR:
     # PR checklist: [ ] Docs updated
     # CI: Fail if public API changed without docs change
  
### **Symptoms**
  - "Docs say X but code does Y"
  - DeprecationWarning following docs
  - "This method doesn't exist" errors
### **Detection Pattern**
version|deprecated|since|v[0-9]

## Missing Error Docs

### **Id**
missing-error-docs
### **Summary**
No docs for error messages or troubleshooting
### **Severity**
medium
### **Situation**
User gets error with no guidance
### **Why**
  Error: "MemoryStoreFull". What does this mean? How do I fix it?
  User googles. No results. Creates issue. Waits for response.
  Good error docs prevent 50% of support tickets.
  
### **Solution**
  1. Document every error code:
     # docs/errors/MEMORY_STORE_FULL.md
     ## Error: MEMORY_STORE_FULL
  
     ### What it means
     Your memory store has reached capacity.
  
     ### How to fix
     1. Consolidate old memories: `agent.consolidate()`
     2. Delete unused memories: `agent.forget(older_than=30)`
     3. Increase store size: `Agent(store_size="10GB")`
  
  2. Add troubleshooting section:
     ## Troubleshooting
     - [Installation issues](./troubleshooting/installation.md)
     - [Connection errors](./troubleshooting/connection.md)
     - [Performance problems](./troubleshooting/performance.md)
  
  3. Link errors to docs:
     raise MemoryStoreFullError(
         "Store is full. See: https://docs.mind/errors/MEMORY_STORE_FULL"
     )
  
### **Symptoms**
  - "What does this error mean?" issues
  - Same error questions asked repeatedly
  - Users stuck with no path forward
### **Detection Pattern**
error|troubleshoot|FAQ|common.*issue

## No Getting Started

### **Id**
no-getting-started
### **Summary**
Docs dive into details without quick start
### **Severity**
high
### **Situation**
New user landing on documentation
### **Why**
  User wants to try your library. Docs start with architecture.
  30 pages of concepts. No "how do I run this?" for 10 minutes.
  User leaves. Tries competitor with 5-line quick start.
  
### **Solution**
  1. Quick start on first page:
     # Memory Service
  
     ```bash
     pip install memory-service
     ```
  
     ```python
     from mind import Agent
     agent = Agent("my-agent")
     await agent.remember("Hello, world!")
     ```
  
  2. Time estimate:
     # Quick Start (5 minutes)
  
  3. Immediate success:
     # First example should produce visible output
  
  4. Progressive disclosure:
     # Quick Start → Tutorial → Concepts → API Reference
  
### **Symptoms**
  - Users asking "how do I start?"
  - High bounce rate on docs homepage
  - Adoption lower than code quality deserves
### **Detection Pattern**
quick.*start|getting.*started|installation

## Copy Paste Unsafe

### **Id**
copy-paste-unsafe
### **Summary**
Examples work but have security/production issues
### **Severity**
high
### **Situation**
Users copy examples directly to production
### **Why**
  Example uses hardcoded password for simplicity.
  User copies to production. Gets hacked.
  "But I followed the docs!"
  
### **Solution**
  1. Use obvious placeholders:
     # BAD
     api_key = "sk-1234567890"
  
     # GOOD
     api_key = os.environ["MIND_API_KEY"]
  
  2. Add security warnings:
     ```python
     # ⚠️ DEVELOPMENT ONLY - Use secrets manager in production
     db_password = "localdevpassword"
     ```
  
  3. Show production pattern:
     ## Quick Start (Development)
     ```python
     agent = Agent("test")  # In-memory storage
     ```
  
     ## Production Setup
     ```python
     agent = Agent(
         "prod",
         storage=PostgresStorage(os.environ["DATABASE_URL"])
     )
     ```
  
  4. Separate dev and prod docs:
     # /docs/development/quickstart.md
     # /docs/production/deployment.md
  
### **Symptoms**
  - Security vulnerabilities from copied examples
  - Hardcoded credentials in production
  - But the docs said to do this
### **Detection Pattern**
example|demo|development.*only|production

## Dead Links

### **Id**
dead-links
### **Summary**
Documentation links lead to 404 pages
### **Severity**
medium
### **Situation**
Links to moved or deleted pages
### **Why**
  User follows "See Advanced Usage" link. 404.
  Now they're lost. Trust in docs decreases.
  Common in growing docs with refactoring.
  
### **Solution**
  1. Check links in CI:
     # markdown-link-check
     npx markdown-link-check docs/**/*.md
  
  2. Use relative links:
     # BAD: Will break if domain changes
     [API](https://docs.memory-service.io/api)
  
     # GOOD: Relative to current doc
     [API](./api/index.md)
  
  3. Add redirects for moved pages:
     # In docs config
     redirects:
       - from: /old/path
         to: /new/path
  
  4. Periodic link audit:
     # Monthly: run link checker on production docs
  
### **Symptoms**
  - 404 errors in docs
  - "Link doesn't work" issues
  - Users can't find referenced content
### **Detection Pattern**
link|href|url|see.*also

## No Search

### **Id**
no-search
### **Summary**
Can't find anything in docs without reading everything
### **Severity**
medium
### **Situation**
Large documentation without search
### **Why**
  User knows feature exists but can't find docs.
  Scrolls through 50 pages. Gives up. Asks on Discord.
  Good search is the difference between docs and a book.
  
### **Solution**
  1. Add search (Algolia, Typesense, Meilisearch):
     # docsearch.algolia.com for free OSS indexing
  
  2. Use semantic organization:
     # Group by user task, not by code structure
     - Getting Started
     - Storing Memories
     - Retrieving Memories
     - Configuration
  
  3. Add keyword synonyms:
     # "login", "signin", "authentication" → same page
  
  4. Include common searches in nav:
     # Most visited: Installation, Quick Start, API Reference
  
### **Symptoms**
  - Where are the docs for X?
  - Users can't find existing documentation
  - Support questions for documented features
### **Detection Pattern**
search|find|navigation|index