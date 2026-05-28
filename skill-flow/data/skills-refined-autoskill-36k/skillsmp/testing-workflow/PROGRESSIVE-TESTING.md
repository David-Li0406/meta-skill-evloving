# Progressive Testing Strategy

**Core Principle:** Order tests by execution speed to catch errors early and fail fast.

## The Problem

AWS Lambda deployments take ~8 minutes. Finding bugs after deployment wastes time and creates long iteration cycles:

```
Write code → Deploy to AWS (8 min) → Test fails → Fix → Deploy again (8 min)
= 16+ minutes per iteration
```

## The Solution

Order tests by execution speed. Catch errors in seconds locally before deploying to AWS:

```
Write code → Unit tests (15s) → Docker tests (90s) → Deploy (8 min) → Integration tests (60s)
= Find 90% of bugs in <2 minutes, before AWS deployment
```

## The 7 Layers

Progressive testing strategy with early error detection:

| Layer | Test Type | Runtime | Purpose | Catches |
|-------|-----------|---------|---------|---------|
| 1 | Unit Tests | 15s | Logic validation | Function errors, type issues |
| 2 | Docker Import | 30s | Dependency check | Missing packages, import errors |
| 3 | Docker Local | 60s | Execution validation | Handler errors, config issues |
| 4 | Contract Tests | 10s | Schema validation | Integration mismatches |
| 5 | Terraform Validation | 30s | Infrastructure check | Syntax errors, policy violations |
| 6 | Integration Tests | 60s | AWS validation | Deployment issues, permissions |
| 7 | OPA/Terratest | varies | Policy & infra tests | Compliance, integration |

**Total:** ~2 minutes for layers 1-5 (pre-deployment), ~5 minutes for all layers

## Layer Details

### Layer 1: Unit Tests (15s)
**Purpose:** Test business logic with mocked dependencies

**Command:**
```bash
pytest tests/scheduler/ -v
just test-scheduler-unit
```

**What it catches:**
- Function logic errors
- Type mismatches
- Missing parameters
- Exception handling bugs

**Example:**
```python
def test_triggers_precompute_on_successful_fetch():
    result = lambda_handler({}, None)
    assert result['body']['precompute_triggered'] is True
```

---

### Layer 2: Docker Import Tests (30s)
**Purpose:** Verify all Python imports work inside Lambda Docker container

**Command:**
```bash
./scripts/test_docker_imports.sh
```

**What it catches:**
- Missing dependencies in requirements.txt
- Import errors (wrong module paths)
- Missing system libraries
- Python version incompatibilities

**Example test:**
```bash
docker run --rm lambda-image python3 -c "
from src.scheduler.handler import lambda_handler
assert callable(lambda_handler)
"
```

**Why this matters:** Lambda container has different environment than local dev (system libs, Python path). Catches "works on my machine" issues.

---

### Layer 3: Docker Local Execution (60s)
**Purpose:** Execute Lambda handlers inside Docker with mocked AWS services

**Command:**
```bash
./scripts/test_docker_local.sh
```

**What it catches:**
- Handler execution errors
- Environment variable issues
- Response format problems
- Error handling bugs

**Example test:**
```bash
docker run --rm -e BUCKET=test lambda-image python3 -c "
from src.scheduler.handler import lambda_handler
result = lambda_handler({}, None)
assert result['statusCode'] == 200
"
```

---

### Layer 4: Contract Tests (10s)
**Purpose:** Validate Lambda outputs match Step Functions JSONPath expectations

**Command:**
```bash
./scripts/test_contracts.sh
just test-scheduler-contracts
```

**What it catches:**
- Lambda output schema mismatches
- Missing required fields
- Wrong data types
- JSONPath extraction failures

**Example:**
```python
def test_output_matches_jsonpath():
    result = lambda_handler({}, None)
    # Step Functions expects: $.ticker_list.tickers
    assert 'tickers' in result
    assert isinstance(result['tickers'], list)
```

---

### Layer 5: Terraform Validation (30s)
**Purpose:** Validate infrastructure code syntax and policies

**Command:**
```bash
cd terraform && terraform fmt -check && terraform validate
```

**What it catches:**
- Terraform syntax errors
- Invalid resource references
- Missing required arguments
- Policy violations (if OPA configured)

---

### Layer 6: Integration Tests (60s)
**Purpose:** Test against real AWS services (post-deployment)

**Command:**
```bash
pytest tests/integration/ -v -m integration
just test-scheduler-integration
```

**What it catches:**
- IAM permission issues
- VPC connectivity problems
- Resource configuration errors
- Cross-service integration failures

**Example:**
```python
@pytest.mark.integration
def test_lambda_invokes_step_functions():
    response = lambda_client.invoke(FunctionName='scheduler-dev')
    assert response['StatusCode'] == 200
```

**Note:** Requires deployed Lambda functions and AWS credentials

---

### Layer 7: OPA/Terratest (optional)
**Purpose:** Policy compliance and infrastructure integration tests

**Commands:**
```bash
opa test terraform/policies/ -v     # OPA policy tests
go test -v ./tests/terratest/...    # Terratest (Go)
```

**What it catches:**
- Infrastructure policy violations
- Resource configuration issues
- Cross-stack dependencies

## Master Test Orchestration

**Script:** `scripts/test_all.sh`

Runs all layers in order, stops on first failure:

```bash
# Quick validation (layers 1-5, ~2 min)
./scripts/test_all.sh
just test-scheduler

# Full validation (all layers, ~5 min)
./scripts/test_all.sh --full
just test-scheduler-all

# Run only up to layer 3
./scripts/test_all.sh --layer=3

# Skip Docker tests
./scripts/test_all.sh --skip-docker
```

**Output format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Layer 1: Unit Tests (pytest)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Layer 1 passed (15s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Layer 2: Docker Import Tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Layer 2 passed (30s)

... (continues for all layers)

✅ All test layers passed!
Total duration: 120s
```

## Intent-Based Justfile Commands

Hierarchy of test commands for different workflows:

```bash
# Quick iteration during development
just test-scheduler-unit              # Layer 1 only (~15s)

# Pre-commit validation
just test-scheduler                    # Layers 1-5 (~2 min)

# Pre-deployment validation
just test-scheduler-all                # All layers (~5 min)

# Specific layer testing
just test-scheduler-docker             # Layers 2-3 (~90s)
just test-scheduler-contracts          # Layer 4 (~10s)
just test-scheduler-integration        # Layer 6 (~60s)
```

## CI/CD Integration

### Pre-Deployment Phase (CI)
**Run BEFORE any AWS deployment**

```yaml
jobs:
  validate:
    steps:
      - name: Layer 1 - Unit Tests
        run: pytest tests/scheduler/ -v

      - name: Layer 2 - Docker Import Tests
        run: ./scripts/test_docker_imports.sh

      - name: Layer 3 - Docker Local Execution
        run: ./scripts/test_docker_local.sh

      - name: Layer 4 - Contract Tests
        run: ./scripts/test_contracts.sh

      - name: Layer 5 - Terraform Validation
        run: terraform validate

# Stop here if any test fails ❌
# Don't deploy broken code to AWS
```

### Deployment Phase
**Deploy to Lambda `$LATEST` (mutable pointer)**

```yaml
  deploy:
    needs: validate  # Only runs if validation passed
    steps:
      - name: Build Docker image
        run: docker build -t lambda-image .

      - name: Push to ECR
        run: docker push <ecr-uri>

      - name: Deploy to $LATEST
        run: aws lambda update-function-code --image-uri <uri>
```

### Post-Deployment Phase
**Test `$LATEST` before promotion**

```yaml
  test-deployment:
    needs: deploy
    steps:
      - name: Layer 6 - Integration Tests (smoke)
        run: |
          aws lambda invoke --qualifier $LATEST --payload '{}'
          pytest tests/integration/ -v -m integration

      - name: Layer 7 - Terratest (optional)
        run: go test -v ./tests/terratest/...
```

### Promotion Phase
**Create immutable version after tests pass**

```yaml
  promote:
    needs: test-deployment
    steps:
      - name: Publish version N+1
        run: |
          VERSION=$(aws lambda publish-version ...)
          echo "Published version: $VERSION"

      - name: Update alias to version N+1
        run: aws lambda update-alias --version $VERSION
```

## When to Run Which Layers

### Local Development (Fast Iteration)
```bash
just test-scheduler-unit  # Layer 1 only
# Runtime: 15s
# Use when: Developing new feature, fixing bug
```

### Before Commit
```bash
just test-scheduler  # Layers 1-5
# Runtime: 2 min
# Use when: Ready to commit, creating PR
```

### Before Deployment
```bash
just test-scheduler-all  # All layers
# Runtime: 5 min (if AWS resources deployed)
# Use when: Deploying to dev/staging/prod
```

### After Lambda Changes
```bash
just test-scheduler-docker  # Layers 2-3
# Runtime: 90s
# Use when: Changed dependencies, updated Lambda handler
```

### After Step Functions Changes
```bash
just test-scheduler-contracts  # Layer 4
# Runtime: 10s
# Use when: Modified state machine JSON, changed Lambda output schema
```

## Benefits

**Early Error Detection:**
- 90% of bugs caught in layers 1-3 (~2 min)
- 10% require AWS integration tests (~60s)
- Total: Find bugs in <3 minutes instead of 8+ minutes

**Fail Fast:**
- Master script stops on first failure
- Clear error reporting (which layer failed)
- No wasted time running later layers if early ones fail

**Reduced Iteration Time:**
- Before: 8 min deploy → 8 min redeploy = 16+ min per bug
- After: 2 min local tests → 8 min deploy = 10 min per bug
- **Savings: ~40% faster iteration**

**Developer Experience:**
- Intent-based commands (`just test-scheduler`)
- Progressive detail (unit → docker → integration)
- Clear output (colored, timed, summarized)

## Example Workflow

```bash
# 1. Develop feature
vim src/scheduler/handler.py

# 2. Quick test during development
just test-scheduler-unit
# ✅ Layer 1 passed (15s)

# 3. Changed dependencies? Test Docker
just test-scheduler-docker
# ✅ Layer 2 passed (30s)
# ✅ Layer 3 passed (60s)

# 4. Before committing
just test-scheduler
# ✅ Layers 1-5 passed (120s)

# 5. Deploy to dev
just deploy-dev
# (8 min deployment)

# 6. Post-deployment validation
just test-scheduler-integration
# ✅ Layer 6 passed (60s)

# 7. Total time: 2 min (local) + 8 min (deploy) + 1 min (AWS) = 11 min
# Compare to: Deploy blind (8 min) → Fail → Fix → Redeploy (8 min) = 16+ min
```

## References

- [Testing Patterns](PATTERNS.md) - Canonical test structure
- [Lambda Testing](LAMBDA-TESTING.md) - Docker and contract testing details
- [Defensive Testing](DEFENSIVE.md) - Validation gates and sabotage verification
- [Master Script](../../../scripts/test_all.sh) - Implementation reference
- [Justfile Commands](../../../justfile) - Intent-based test commands
