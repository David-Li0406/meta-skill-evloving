# Terraform Example Testing Guide

## Overview

This guide explains how to set up automated testing for your Terraform provider's example configurations. The framework provides a generic test harness that you customize for your specific provider.

## Quick Start

1. **Copy the template to your project:**
   ```bash
   cp .claude/skills/terraform-provider-tests/templates/test-examples-template.sh \
      scripts/test-examples.sh
   chmod +x scripts/test-examples.sh
   ```

2. **Customize for your provider:**
   - Set `PROVIDER_NAME` variable
   - Update environment variable requirements in `show_help()`
   - **Implement `cleanup_resources()` function**

3. **Run tests:**
   ```bash
   ./scripts/test-examples.sh
   ```

## Template Customization

### Required Changes

#### 1. Provider Name
```bash
# Update this line in your scripts/test-examples.sh
PROVIDER_NAME="myprovider"  # Change from "myprovider" to your provider name
```

#### 2. Environment Variables
Update the `show_help()` function to document your provider's required environment variables:

```bash
ENVIRONMENT VARIABLES (Required):
  MYPROVIDER_ENDPOINT    API endpoint (e.g., https://api.example.com)
  MYPROVIDER_API_KEY     API authentication key
```

Add validation in `validate_environment()`:
```bash
validate_environment() {
    # ... existing validation ...

    # Add your provider-specific validation
    if [ -z "${MYPROVIDER_ENDPOINT:-}" ]; then
        log_error "Missing MYPROVIDER_ENDPOINT"
        exit "$EXIT_CONFIG_ERROR"
    fi

    if [ -z "${MYPROVIDER_API_KEY:-}" ]; then
        log_error "Missing MYPROVIDER_API_KEY"
        exit "$EXIT_CONFIG_ERROR"
    fi

    log_info "✓ MYPROVIDER_ENDPOINT set"
    log_info "✓ MYPROVIDER_API_KEY set"
}
```

#### 3. Cleanup Implementation (REQUIRED)

**This is the most important customization.** You must implement provider-specific cleanup logic.

**Template Pattern:**
```bash
cleanup_resources() {
    log_info "Phase 4: Cleanup..."

    # 1. Authenticate with your API
    local auth_token
    auth_token=$(authenticate_with_provider)

    # 2. Query for test resources (use a consistent prefix like "citest-")
    local test_resources
    test_resources=$(query_provider_api "$auth_token" "list-resources" | grep "citest-")

    # 3. Delete found resources with retry logic
    local cleanup_count=0
    for resource in $test_resources; do
        if delete_with_retry "$auth_token" "$resource"; then
            cleanup_count=$((cleanup_count + 1))
            log_pass "  ✓ Deleted $resource"
        else
            log_fail "  ✗ Failed to delete $resource"
        fi
    done

    # 4. Verify deletion
    sleep 2  # Wait for eventual consistency
    remaining=$(query_provider_api "$auth_token" "list-resources" | grep -c "citest-" || true)

    if [ "$remaining" -eq 0 ]; then
        log_pass "Cleanup complete: $cleanup_count resource(s) removed"
        return 0
    else
        log_fail "Cleanup incomplete: $remaining resource(s) remain"
        return 1
    fi
}
```

**Real-World Example (BCM Provider):**
```bash
cleanup_resources() {
    log_info "Phase 4: Cleanup..."

    # 1. Authenticate
    local cookie_file
    cookie_file=$(mktemp)
    curl -k -s -c "$cookie_file" -X POST "${BCM_ENDPOINT}/json" \
        -H "Content-Type: application/json" \
        -d '{"service":"login","username":"'$BCM_USERNAME'","password":"'$BCM_PASSWORD'"}'

    # 2. Query for test images
    local images_response
    images_response=$(curl -k -s -b "$cookie_file" -X POST "${BCM_ENDPOINT}/json" \
        -H "Content-Type: application/json" \
        -d '{"service":"CMPart","call":"getSoftwareImages"}')

    # 3. Extract test resources (prefix: citest-)
    local test_images=()
    while IFS= read -r line; do
        if [[ "$line" =~ \"name\":\"(citest-[^\"]+)\" ]]; then
            test_images+=("${BASH_REMATCH[1]}")
        fi
    done <<< "$images_response"

    # 4. Delete resources
    if [ ${#test_images[@]} -gt 0 ]; then
        local images_json="[\"${test_images[0]}\""
        for ((i=1; i<${#test_images[@]}; i++)); do
            images_json="$images_json, \"${test_images[$i]}\""
        done
        images_json="$images_json]"

        curl -k -s -b "$cookie_file" -X POST "${BCM_ENDPOINT}/json" \
            -H "Content-Type: application/json" \
            -d '{"service":"CMPart","call":"removeSoftwareImages","args":['$images_json',false]}'

        log_pass "  ✓ Deleted ${#test_images[@]} test image(s)"
    fi

    rm -f "$cookie_file"
    return 0
}
```

## Test Resource Naming Convention

**Always use a consistent prefix for test resources.** Recommended: `citest-` or `test-`

**Why?**
- Easy identification of test resources
- Safe cleanup (won't accidentally delete production resources)
- Parallel test isolation

**Example:**
```hcl
resource "myprovider_instance" "test" {
  name = "citest-instance-${timestamp()}"  # ✓ Good
  # NOT: name = "my-instance"               # ✗ Bad - conflicts with other tests
}
```

## Example Directory Structure

```
examples/
├── provider/
│   └── provider.tf
├── data-sources/
│   ├── myprovider_instances/
│   │   └── data-source.tf
│   └── myprovider_networks/
│       └── data-source.tf
└── resources/
    ├── myprovider_instance/
    │   └── resource.tf
    └── myprovider_network/
        └── resource.tf
```

## Test Execution Modes

### Full Test Suite
```bash
./scripts/test-examples.sh
```
- Builds provider
- Tests all examples
- Runs cleanup

### Data Sources Only (Fast)
```bash
./scripts/test-examples.sh --data-sources-only
```
- Quick validation
- Parallel execution
- Read-only operations

### Resources Only
```bash
./scripts/test-examples.sh --resources-only
```
- Creates real resources
- Sequential execution
- Full integration testing

### Debug Mode
```bash
./scripts/test-examples.sh --verbose --no-cleanup
```
- Detailed output
- Leaves resources for inspection
- Manual cleanup required

### Cleanup Only
```bash
./scripts/test-examples.sh --cleanup-only
```
- Only runs cleanup phase
- Useful after debugging
- No tests executed

## Advanced: Parallel Testing

The framework supports parallel execution for data source examples (read-only operations).

**Configuration:**
```bash
PARALLEL_LIMIT=8 ./scripts/test-examples.sh --data-sources-only
```

**Guidelines:**
- Data sources: Safe for parallel execution (read-only)
- Resources: Must be sequential (creates/modifies infrastructure)
- Default parallel limit: 4

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Test Examples
on: [push, pull_request]

jobs:
  test-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'

      - name: Test Examples
        env:
          MYPROVIDER_ENDPOINT: ${{ secrets.MYPROVIDER_ENDPOINT }}
          MYPROVIDER_API_KEY: ${{ secrets.MYPROVIDER_API_KEY }}
        run: ./scripts/test-examples.sh
```

## Troubleshooting

### Build Failures
```bash
# Skip build and use existing binary
SKIP_BUILD=true ./scripts/test-examples.sh
```

### Cleanup Failures
```bash
# Retry cleanup only
./scripts/test-examples.sh --cleanup-only

# Debug cleanup with verbose output
./scripts/test-examples.sh --cleanup-only --verbose
```

### Example Failures
```bash
# Test specific category
./scripts/test-examples.sh --data-sources-only --verbose

# Keep resources for debugging
./scripts/test-examples.sh --no-cleanup
```

## Best Practices

1. **Unique Resource Names**
   - Use timestamp or random suffix
   - Prefix with `citest-` or `test-`
   - Never hardcode resource names

2. **Cleanup Implementation**
   - Query API for test resources
   - Use retry logic for deletions
   - Verify deletion succeeded
   - Handle eventual consistency

3. **Environment Variables**
   - Store credentials as env vars
   - Never hardcode in examples
   - Document all required vars

4. **Testing Strategy**
   - Data sources → parallel (fast feedback)
   - Resources → sequential (safe)
   - Always run cleanup after tests

5. **CI Integration**
   - Run on every commit
   - Use secrets for credentials
   - Fail fast on errors
   - Cleanup even on failure

## Summary

The example testing framework provides:
- ✅ Generic test execution (provided by skill)
- ✅ Automated provider builds
- ✅ Parallel/sequential execution
- ❌ Cleanup logic (**you must implement**)

**Remember:** The framework is generic, but cleanup is provider-specific. You must implement `cleanup_resources()` for your provider's API.
