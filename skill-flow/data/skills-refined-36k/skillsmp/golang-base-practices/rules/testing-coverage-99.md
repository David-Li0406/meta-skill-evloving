---
title: 99% Test Coverage Target
impact: CRITICAL
impactDescription: Code quality assurance
tags: testing, coverage, quality
---

## 99% Test Coverage Target

Target 99% test coverage to ensure code quality.

**Running Coverage Detection:**

```bash
# Generate coverage report
go test -coverprofile=coverage.out ./...

# View coverage summary
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# View by package
go test -cover ./...
```

**CI Enforced Coverage:**

```yaml
# .github/workflows/test.yml
- name: Test with coverage
  run: |
    go test -coverprofile=coverage.out ./...
    COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
    if (( $(echo "$COVERAGE < 99" | bc -l) )); then
      echo "Coverage is below 99%: $COVERAGE%"
      exit 1
    fi
```

**Coverage Strategy:**

| Layer | Target Coverage | Focus |
|-------|-----------------|-------|
| Domain Layer | 100% | Core business logic |
| Application Layer | 99% | Use case flows |
| Infrastructure Layer | 95% | Integration tests primarily |
| Interface Layer | 90% | HTTP handlers |

**Excluding Code from Coverage:**

```go
// Add comment to exclude generated code
//go:generate mockgen ...

// Wire-generated code is typically in wire_gen.go
```

**Makefile Integration:**

```makefile
.PHONY: test
test:
	go test -race -coverprofile=coverage.out ./...
	@go tool cover -func=coverage.out | grep total | awk '{print "Coverage: " $$3}'

.PHONY: coverage
coverage: test
	go tool cover -html=coverage.out -o coverage.html
	open coverage.html
```
