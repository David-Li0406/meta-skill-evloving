# Terraform Provider Testing Skill

Generic testing patterns and templates for Terraform provider development.

## Contents

### Templates
- **`templates/test-examples-template.sh`** - Generic example testing framework
  - Copy to your project's `scripts/test-examples.sh`
  - Customize provider name and environment variables
  - **Implement `cleanup_resources()` function** (provider-specific)

### Documentation
- **`docs/example-testing-guide.md`** - Complete guide for example testing
  - Quick start instructions
  - Customization requirements
  - Cleanup implementation patterns
  - Best practices

### Scripts
- **`scripts/run_tests_parallel.sh`** - Parallel acceptance test execution
  - Runs tests by file with concurrency control
  - Detailed progress tracking
  - Result aggregation

## Quick Start

### 1. Example Testing
```bash
# Copy template to your project
cp .claude/skills/terraform-provider-tests/templates/test-examples-template.sh \
   scripts/test-examples.sh

# Customize for your provider
# 1. Set PROVIDER_NAME
# 2. Update environment variables
# 3. Implement cleanup_resources()

# Run tests
./scripts/test-examples.sh
```

See `docs/example-testing-guide.md` for detailed instructions.

### 2. Parallel Acceptance Tests

**✅ RECOMMENDED: Two-Step Process**

```bash
# Step 1: Start tests in background with logging
LOG_FILE="/tmp/terraform-tests-$(date +%Y%m%d-%H%M%S).log"
TF_ACC=1 BCM_ENDPOINT="${BCM_ENDPOINT}" BCM_USERNAME="${BCM_USERNAME}" \
BCM_PASSWORD="${BCM_PASSWORD}" \
.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh \
  -c 21 -t 30m > "$LOG_FILE" 2>&1 &
TEST_PID=$!

# Step 2: Monitor with tail
tail -f "$LOG_FILE"
```

**Alternative: Wrapper script (ensure env vars are exported)**

```bash
# Run all 21 test files - auto-logs and tails output
.claude/skills/terraform-provider-tests/scripts/run_tests_with_log.sh -c 21 -t 30m

# Run only resource tests
.claude/skills/terraform-provider-tests/scripts/run_tests_with_log.sh --resources-only -c 8
```

**Quick Piped Output:**

```bash
# Quick feedback - see last 100 lines
.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100

# CI/CD - save full log
.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh -c 21 2>&1 | tee test-results.log
```

See `docs/parallel-testing-guide.md` for complete usage patterns.

## Key Principles

### ✅ Generic in Skill
- Test execution framework
- Build automation
- Logging and reporting
- Parallel execution patterns
- Command-line interface

### ❌ Provider-Specific in Project
- Cleanup logic (API calls, authentication)
- Environment variable validation
- Provider configuration
- Resource naming conventions

## Separation of Concerns

**The skill provides:**
- Reusable testing patterns
- Generic automation scripts
- Best practice documentation

**Your project implements:**
- Provider-specific cleanup
- API integration
- Authentication logic
- Resource lifecycle management

## Example Structure

```
your-project/
├── scripts/
│   └── test-examples.sh          # Copied from template, customized
├── examples/
│   ├── data-sources/
│   └── resources/
└── internal/provider/
    ├── *_test.go                 # Acceptance tests
    └── test_helpers.go           # Test utilities
```

## See Also

- Terraform Plugin Framework: https://developer.hashicorp.com/terraform/plugin/framework
- Terraform Plugin Testing: https://developer.hashicorp.com/terraform/plugin/testing
- HashiCorp Testing Best Practices: https://developer.hashicorp.com/terraform/plugin/best-practices/testing
