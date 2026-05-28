# Detection Patterns

This document describes various detection patterns used during technical specification generation.

## DB Schema Change Detection

### Detection Patterns

```python
patterns = [
    r'CREATE TABLE',
    r'ALTER TABLE', 
    r'DROP TABLE',
    r'CREATE INDEX',
    r'DROP INDEX',
    r'migration',
    r'schema\.prisma',
    r'\.sql$'
]
```

### Supported Frameworks

- **Prisma**: Changes to `schema.prisma` files
- **TypeORM**: `*migration*.ts` files
- **Alembic** (Python): `versions/*.py` files
- **Liquibase**: `*.xml`, `*.sql` files
- **Raw SQL**: `*.sql` files

## API Definition Detection

### Detection Patterns

```python
route_patterns = [
    r'@(Get|Post|Put|Delete|Patch)\([\'"]([^\'"]+)',  # NestJS, Spring
    r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)',  # Flask, FastAPI
    r'router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)',  # Express
    r'(GET|POST|PUT|DELETE|PATCH)\s+[\'"]([^\'"]+)[\'"]'  # Generic
]
```

### Supported Frameworks

- **NestJS**: `@Get()`, `@Post()` decorators
- **Express**: `router.get()`, `router.post()`
- **FastAPI**: `@app.get()`, `@app.post()`
- **Flask**: `@app.route()`
- **Spring**: `@GetMapping`, `@PostMapping`

### API File Identification

Files containing the following keywords are identified as API files:
- `route`
- `controller`
- `api`

## Test File Detection

### Detection Patterns

```python
test_patterns = [
    r'\.test\.',      # *.test.js, *.test.ts
    r'\.spec\.',      # *.spec.js, *.spec.ts
    r'__tests__',     # __tests__/ directory
    r'/tests?/',      # /test/ or /tests/ directory
    r'/test/'
]
```

### Supported Frameworks

- **Jest**: `*.test.js`, `*.test.ts`, `__tests__/`
- **Mocha**: `*.spec.js`, `test/`
- **pytest**: `test_*.py`, `*_test.py`
- **RSpec**: `*_spec.rb`
- **JUnit**: `*Test.java`

## Dependency Detection

### Target Files

```python
dependency_files = [
    'package.json',      # Node.js
    'requirements.txt',  # Python
    'Gemfile',          # Ruby
    'pom.xml',          # Java (Maven)
    'build.gradle',     # Java (Gradle)
    'go.mod',           # Go
    'Cargo.toml'        # Rust
]
```

## Major Change Detection

Extract lines containing the following keywords from code diffs:

- `function ` - Function definitions
- `class ` - Class definitions
- `def ` - Python function definitions
- `const ` - Constant definitions
- `export` - Export declarations

## Customization

To add project-specific patterns, edit the corresponding functions in `generate_spec.py`:

- `detect_db_changes()` - DB schema detection patterns
- `detect_api_changes()` - API detection patterns
- `detect_test_changes()` - Test file detection patterns
- `detect_dependency_changes()` - Dependency detection files

## Notes

- Detection patterns are regex-based and may produce false positives
- Patterns may need adjustment based on project coding conventions
- For large PRs, output limits are in place to prevent excessive results
