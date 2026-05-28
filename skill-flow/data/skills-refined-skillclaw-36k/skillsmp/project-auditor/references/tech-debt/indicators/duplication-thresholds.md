# Code Duplication Thresholds

Thresholds for detecting and scoring code duplication (DRY violations).

## Overall Duplication

Percentage of codebase that is duplicated.

| Range | Level | Score | Description |
|-------|-------|-------|-------------|
| 0-3% | Excellent | 0 | Minimal duplication |
| 3-5% | Good | 15 | Acceptable DRY adherence |
| 5-10% | Moderate | 35 | Consider refactoring |
| 10-20% | High | 65 | Significant duplication |
| 20%+ | Critical | 100 | Severe DRY violations |

## Clone Types

### Detection Parameters

- **Minimum Lines**: 6 lines
- **Minimum Tokens**: 50 tokens

### Clone Classification

| Type | Name | Severity | Weight | Description |
|------|------|----------|--------|-------------|
| 1 | Exact Clones | High | 1.0 | Identical code fragments |
| 2 | Renamed Clones | Medium | 0.8 | Identical structure, renamed identifiers |
| 3 | Gapped Clones | Medium | 0.6 | Copied with modifications |
| 4 | Semantic Clones | Low | 0.4 | Different syntax, same semantics |

## Hotspot Detection

Files are flagged as duplication hotspots when:

- Duplication percentage exceeds **30%** of file
- Clone count exceeds **5** instances

## Acceptable Duplication

Patterns where duplication may be acceptable:

- Test fixtures and setup
- Generated code
- Configuration files
- Database migrations
- Protocol buffers / IDL
- Boilerplate required by frameworks

## Recommended Tools

| Tool | Languages |
|------|-----------|
| jscpd | JavaScript, TypeScript, Python, Java, Go |
| PMD CPD | Java, JavaScript, Python |
| Simian | Java, C#, JavaScript |
| SonarQube | Multi-language |

## Remediation Strategies

### Extract Common Code

1. Identify duplicated logic
2. Extract to shared function/method
3. Replace duplicates with calls
4. Add appropriate tests

### Use Inheritance/Composition

1. Identify duplicated class structures
2. Extract base class or mixin
3. Refactor to use inheritance/composition
4. Test all derived implementations

### Template/Generics

1. Identify type-only differences
2. Create generic/template version
3. Replace duplicates with parameterized calls
