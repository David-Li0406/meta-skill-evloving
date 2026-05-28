---
name: mastering-python-skill
description: Use this skill when you need guidance on writing Python code, explaining concepts, setting up projects, or implementing best practices in Python development.
---

# Mastering Python Skill

Production-ready Python patterns with runnable code examples.

## Contents

- [Workflow](#workflow)
- [When NOT to Use](#when-not-to-use)

---

## Workflow

### Phase 1: Setup

1. Verify Python version
   ```bash
   python --version  # Require 3.10+, prefer 3.12+
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv .venv && source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   poetry install  # or: pip install -r requirements.txt
   ```

### Phase 2: Develop

4. Reference appropriate patterns:
   - Types
   - Async
   - APIs
   - Database access

5. Follow project structure guidelines.

### Phase 3: Validate

6. Run quality checks
   ```bash
   ruff check . && ruff format --check .
   mypy src/
   ```

7. Run tests with coverage
   ```bash
   pytest -v --cov=src --cov-report=term-missing
   ```

### Phase 4: Deploy

8. Build and verify package
   ```bash
   python -m build && twine check dist/*
   ```

9. Deploy using Docker or CI/CD pipelines.

**Pre-Completion Checklist:**
```
- [ ] All tests pass
- [ ] mypy reports no errors
- [ ] ruff check clean
- [ ] Coverage ≥80%
- [ ] No security warnings
```