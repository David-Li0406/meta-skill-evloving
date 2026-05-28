# Technical Specification Template

This document defines the standard structure of technical specifications generated from PRs.

## Standard Chapter Structure

### 1. Overview
Basic PR information (number, URL, creation date, branch info, description)

### 2. Change Summary
Numerical metrics of changes (files changed, lines added/removed, commits)

### 3. Folder Structure
```
src/
├── components/
│   ├── NewComponent.tsx (Added)
│   └── ExistingComponent.tsx (Modified)
└── ...
```

### 4. Commit History
Chronological change history in table format

### 5. DB Schema Changes
Detection of migration files and schema definition changes

### 6. API Definition
Detection of new/modified endpoints

### 7. Major Changes
Key changes extracted from code diffs

### 8. Tests
Detection of test file additions/changes

### 9. Dependencies
Detection of dependency changes in package.json, etc.

### 10. Generation Info
Document metadata (generation date, repository path, etc.)

## Customization

Depending on the project nature, you can add chapters such as:

- Security Considerations
- Performance Impact
- Breaking Changes
- Migration Steps
- Deployment Requirements
- Environment Variable Changes
