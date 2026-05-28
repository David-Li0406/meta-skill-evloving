---
name: component-tester
description: This skill should be used when the user asks to "test memex-cli", "test code-with-codex", "test ux-design-gemini", "test /multcode", "run component tests", "validate workflow components", "run integration tests", or "verify plugin functionality". Provides comprehensive testing framework for coding-workflow plugin components.
version: 1.0.0
---

# Component Tester Skill

## Purpose

This skill provides a comprehensive testing framework for validating the core components of the coding-workflow plugin. It automates verification of memex-cli backend integration, code-with-codex skill functionality, ux-design-gemini skill capabilities, and the /multcode command orchestration workflow.

Use this skill to ensure all components work correctly after installation, updates, or configuration changes.

## When to Use This Skill

Invoke this skill when:

- **Initial Setup Validation**: Verify plugin installation and dependency configuration
- **Pre-Deployment Testing**: Validate components before committing workflow changes
- **Regression Testing**: Ensure updates haven't broken existing functionality
- **Troubleshooting**: Diagnose issues with specific components
- **Quality Assurance**: Generate test reports for workflow reliability

## Component Testing Overview

### 1. memex-cli Backend Testing

**Objective**: Verify memex-cli installation, version compatibility, and basic execution.

**Test Execution**:

```bash
# Run automated memex-cli validation
bash scripts/test-memex-cli.sh
```

**Validation Checklist**:
- Command availability (`which memex-cli`)
- Version requirement (>= 1.0.0)
- Backend connectivity (Claude, Codex, Gemini)
- Basic execution test (simple prompt response)
- Error handling for missing configuration

**Common Issues**:
- **Not Found**: Install via `npm install -g memex-cli`
- **Permission Denied**: Check `chmod +x` on memex-cli executable
- **Backend Errors**: Validate API keys in environment variables

Refer to **`references/memex-cli-testing.md`** for detailed troubleshooting scenarios.

### 2. code-with-codex Skill Testing

**Objective**: Validate code generation quality, accuracy, and integration with memex-cli.

**Test Execution**:

```bash
# Test code generation with standard scenarios
python scripts/test-code-with-codex.py
```

**Test Scenarios**:
- **Simple Function**: Generate utility function with docstrings
- **Class Implementation**: Create class with methods and properties
- **Bug Fixing**: Modify existing code to resolve issues
- **Test Generation**: Generate unit tests for given code
- **Multi-File Project**: Scaffold basic project structure

**Success Criteria**:
- ✓ Generated code is syntactically valid
- ✓ Output includes proper comments/docstrings
- ✓ Code follows language conventions
- ✓ Files are created in correct locations
- ✓ Execution completes within timeout (60s per scenario)

**Output Validation**:

```bash
# Validate generated code structure and syntax
python scripts/validate-code-output.py --test-run <run_id>
```

Refer to **`references/test-scenarios.md`** for complete scenario definitions and expected outputs.

### 3. ux-design-gemini Skill Testing

**Objective**: Validate UX design generation, visual specifications, and Gemini backend integration.

**Test Execution**:

```bash
# Test UX design generation with standard scenarios
python scripts/test-ux-design-gemini.py
```

**Test Scenarios**:
- **Component Wireframe**: Generate UI component specifications
- **User Flow Diagram**: Create user journey documentation
- **Design System**: Generate color palette and typography specs
- **Responsive Layout**: Define breakpoint and layout guidelines
- **Interaction Pattern**: Document interactive behaviors

**Success Criteria**:
- ✓ Design specs include all required sections
- ✓ Visual specifications use valid CSS/design tokens
- ✓ Wireframes reference standard UI patterns
- ✓ Output is structured (Markdown with clear sections)
- ✓ Execution completes within timeout (90s per scenario)

**Output Validation**:

```bash
# Validate design output structure and completeness
python scripts/validate-design-output.py --test-run <run_id>
```

Refer to **`examples/expected-design-outputs/`** for sample output structures.

### 4. /multcode Command Testing

**Objective**: Validate end-to-end workflow orchestration with multiple AI backends.

**Test Execution**:

```bash
# Run full /multcode workflow test
python scripts/test-multcode-command.py
```

**Workflow Stages Tested**:
1. **Requirements Analysis** (Claude) - Input: Feature description → Output: Requirements document
2. **UX Design** (Gemini) - Input: Requirements → Output: Design specifications
3. **Implementation Planning** (Codex) - Input: Requirements + Design → Output: Implementation plan
4. **Code Development** (Codex) - Input: Plan → Output: Source code files
5. **Quality Assurance** (Claude) - Input: Code → Output: Test results and review

**Success Criteria**:
- ✓ All stages complete without errors
- ✓ Each stage produces expected output files
- ✓ Stage transitions maintain context correctly
- ✓ Final output includes: code files, tests, documentation
- ✓ Total execution time < 10 minutes

**Orchestration Validation**:

```bash
# Verify stage outputs and dependencies
python scripts/validate-multcode-orchestration.py --workflow-dir <output_dir>
```

Refer to **`references/multcode-workflow.md`** for detailed stage specifications and data flow diagrams.

## Running Complete Test Suite

Execute all tests in sequence with comprehensive reporting:

```bash
# Run full component test suite
python scripts/run-all-tests.py --output test-report.json
```

**Test Suite Phases**:
1. **Dependency Check** - Validate memex-cli, Python packages, API keys
2. **Component Tests** - Run individual component test suites
3. **Integration Tests** - Test component interactions (skill → skill, skill → command)
4. **Performance Tests** - Measure execution times and resource usage
5. **Report Generation** - Create HTML/JSON test reports

**Report Contents**:
- Test execution summary (passed/failed/skipped)
- Per-component performance metrics
- Error logs with stack traces
- Recommendations for failed tests
- Environment configuration snapshot

**Example Report Review**:

```bash
# Generate HTML report for review
python scripts/generate-test-report.py test-report.json --format html --output test-report.html
```

Open `test-report.html` in browser to review detailed results with visual charts.

## Test Configuration

**Environment Variables Required**:

```bash
# Set API keys for backend testing
export ANTHROPIC_API_KEY="sk-ant-..."       # For Claude backend
export OPENAI_API_KEY="sk-..."              # For Codex backend
export GOOGLE_API_KEY="AI..."               # For Gemini backend
```

**Test Configuration File** (`.component-tester.yaml`):

```yaml
# Test execution settings
timeouts:
  memex_cli: 30          # seconds
  code_generation: 60    # seconds
  ux_design: 90          # seconds
  multcode_workflow: 600 # seconds (10 min)

# Skip specific tests (if needed)
skip_tests:
  - "test_gemini_backend"  # Example: skip if no Google API key

# Custom test scenarios (extend defaults)
custom_scenarios:
  code_with_codex:
    - name: "Generate FastAPI endpoint"
      prompt: "Create a FastAPI endpoint for user authentication"
      expected_files: ["app/routes/auth.py", "app/models/user.py"]
```

Place this file in project root to customize test behavior.

## Troubleshooting

### Common Test Failures

**1. memex-cli Not Found**
```
Error: memex-cli command not found
Fix: npm install -g memex-cli
```

**2. Backend Authentication Errors**
```
Error: API key invalid or expired
Fix: Verify environment variables are set correctly
```

**3. Timeout Errors**
```
Error: Test exceeded timeout (60s)
Fix: Increase timeout in .component-tester.yaml or check network connectivity
```

**4. Output Validation Failures**
```
Error: Generated code missing expected file
Fix: Review test scenario expectations, may need to adjust validation rules
```

**5. Orchestration State Errors**
```
Error: /multcode stage transition failed
Fix: Check .bmad/state.yaml for corruption, may need to reset workflow state
```

Refer to **`references/troubleshooting.md`** for comprehensive error resolution guide.

## Advanced Testing

### Custom Test Scenarios

Add custom scenarios to extend default test coverage:

```python
# In scripts/test-code-with-codex.py
from component_tester import CodeScenario

# Define custom scenario
custom_scenario = CodeScenario(
    name="Generate gRPC Service",
    prompt="Create a gRPC service for user management with proto definitions",
    expected_files=["proto/user.proto", "services/user_service.py"],
    validation_rules=[
        "proto file contains service definition",
        "Python file implements service methods"
    ]
)

# Run test
result = run_scenario(custom_scenario)
```

### Performance Benchmarking

Track performance metrics across test runs:

```bash
# Run tests with performance profiling
python scripts/run-all-tests.py --profile --output performance-report.json

# Compare with baseline
python scripts/compare-performance.py performance-report.json baseline.json
```

### Continuous Integration

Integrate component tests into CI/CD pipeline:

```yaml
# .github/workflows/component-tests.yml
name: Component Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install -g memex-cli && pip install -r requirements.txt
      - name: Run component tests
        run: python scripts/run-all-tests.py --ci-mode
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

## Additional Resources

### Reference Files

For detailed testing documentation, consult:

- **`references/memex-cli-testing.md`** - memex-cli installation, configuration, and troubleshooting
- **`references/test-scenarios.md`** - Complete scenario definitions for all components
- **`references/multcode-workflow.md`** - /multcode stage specifications and data flow
- **`references/troubleshooting.md`** - Comprehensive error resolution guide
- **`references/performance-baselines.md`** - Expected performance metrics and optimization tips

### Example Files

Working examples in `examples/`:

- **`examples/test-project/`** - Sample project for testing code generation
- **`examples/expected-code-outputs/`** - Reference outputs for code-with-codex tests
- **`examples/expected-design-outputs/`** - Reference outputs for ux-design-gemini tests
- **`examples/multcode-workflow-output/`** - Complete /multcode execution example

### Test Scripts

Automated testing utilities in `scripts/`:

- **`scripts/test-memex-cli.sh`** - Validate memex-cli installation and basic execution
- **`scripts/test-code-with-codex.py`** - Code generation test suite
- **`scripts/test-ux-design-gemini.py`** - UX design generation test suite
- **`scripts/test-multcode-command.py`** - End-to-end workflow test
- **`scripts/run-all-tests.py`** - Complete test suite orchestrator
- **`scripts/validate-code-output.py`** - Code output structure validator
- **`scripts/validate-design-output.py`** - Design output structure validator
- **`scripts/validate-multcode-orchestration.py`** - Workflow orchestration validator
- **`scripts/generate-test-report.py`** - Test report generator (HTML/JSON)

## Usage Examples

### Quick Validation

Verify plugin installation:

```bash
# Run quick health check
bash scripts/test-memex-cli.sh && echo "✓ memex-cli OK"
python scripts/test-code-with-codex.py --quick && echo "✓ code-with-codex OK"
python scripts/test-ux-design-gemini.py --quick && echo "✓ ux-design-gemini OK"
```

### Full Test Run

Execute comprehensive test suite:

```bash
# Run all tests with detailed reporting
python scripts/run-all-tests.py \
  --output test-report.json \
  --verbose \
  --profile

# Generate HTML report
python scripts/generate-test-report.py test-report.json \
  --format html \
  --output test-report.html

# Review results
open test-report.html  # macOS
start test-report.html # Windows
```

### Targeted Testing

Test specific components:

```bash
# Test only code generation
python scripts/test-code-with-codex.py --scenarios "Simple Function,Class Implementation"

# Test only /multcode workflow
python scripts/test-multcode-command.py --stages "Requirements Analysis,UX Design"
```

### CI/CD Integration

Run tests in non-interactive mode:

```bash
# CI-friendly execution (no prompts, exit code reporting)
python scripts/run-all-tests.py \
  --ci-mode \
  --output ci-report.json \
  --fail-fast

# Check exit code
if [ $? -eq 0 ]; then
  echo "All tests passed"
else
  echo "Tests failed, check ci-report.json"
  exit 1
fi
```

## Best Practices

**Before Each Release**:
1. Run full test suite: `python scripts/run-all-tests.py`
2. Review test report for regressions
3. Update baseline performance metrics
4. Commit test reports to `test-results/` directory

**After Configuration Changes**:
1. Run dependency check: `bash scripts/test-memex-cli.sh`
2. Test affected components individually
3. Verify integration tests still pass

**During Development**:
1. Use `--quick` flag for rapid validation
2. Run targeted tests for modified components
3. Profile performance for optimization work

**For Debugging**:
1. Enable verbose logging: `--verbose` flag
2. Review detailed error traces in test reports
3. Consult troubleshooting reference for known issues
4. Run single scenarios to isolate problems

---

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Maintainer**: coding-workflow plugin team
