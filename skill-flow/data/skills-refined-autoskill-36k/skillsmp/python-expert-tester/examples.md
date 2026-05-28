# Python Testing Examples - Evidence-Based

These examples are provided after I analyze your existing project structure. I'll only suggest changes when there's concrete evidence of improvement opportunities.

## Project Analysis First

Before providing examples, I'll examine:
```python
# Your current setup (I use Read/Glob tools)
project_structure = analyze_project_layout()
existing_config = detect_configuration()
test_files = find_test_files()
installed_packages = check_dependencies()

# Evidence-based analysis
test_quality = analyze_test_quality(test_files)
coverage_gaps = identify_coverage_gaps()
configuration_needs = assess_configuration_effectiveness()
```

## Example Analysis Output

### When NO Changes Are Needed

If your tests are already well-structured:
```
✅ Analysis Complete
- Found 15 test files with good naming conventions
- Coverage: 87% (adequate for project size)
- Configuration: Effective pytest.ini setup
- Test patterns: Uses fixtures, parametrization, and markers appropriately

Recommendation: Your current testing setup is well-organized. Consider minor enhancements only if specific gaps are identified.
```

### When Changes Are Justified

If I find concrete issues:
```
📝 Analysis Complete
- Found 12 test files with improvement opportunities
- Coverage: 45% (low for mature project)
- Issues identified:
  - 3 non-descriptive test names
  - Missing async tests for async code
  - No integration tests for external APIs

Evidence-based recommendations:
1. Rename tests for clarity
2. Add async testing setup
3. Add integration tests
```

## Unit Testing Examples

### Evidence-Driven Test Naming

**Before suggesting naming improvements:**
```python
# I'll show you the actual test names I found
current_tests = [
    ("test1", "tests/user.py:15"),           # Non-descriptive
    ("test_data", "tests/user.py:25"),       # Vague
    ("test_user_creation", "tests/user.py:35"),  # Good
    ("email_validation", "tests/user.py:45")   # Good
]

if len(non_descriptive) / len(current_tests) > 0.3:
    print(f"Found {len(non_descriptive)} tests with unclear names:")
    for name, location in non_descriptive:
        better_name = suggest_better_name(name, location)
        print(f"  {location}: '{name}' → '{better_name}'")
```

### Pattern-Based Testing

**Only suggest patterns when gaps are identified:**

```python
# If your project has validation logic but no edge case testing:
if has_validation_code() and not_has_edge_case_tests():
    print("Found validation code without edge case coverage:")
    print("Suggest adding tests for:")
    print("  - Empty strings")
    print("  - Boundary values")
    print("  - Invalid formats")

    # Concrete example based on your code
    print(f"\nIn tests/test_validation.py:")
    print("  + def test_email_validation_edge_cases():")
    print("  +     assert validate_email('') == False")
    print("  +     assert validate_email('test@') == False")
```

## Integration Testing Examples

### Framework-Specific (Based on Detection)

**I'll check what frameworks you actually use:**

```python
# Detect your actual dependencies
frameworks = {
    'fastapi': check_import('fastapi'),
    'flask': check_import('flask'),
    'django': check_import('django'),
    'aiohttp': check_import('aiohttp'),
    'httpx': check_import('httpx')
}

# Only suggest integration tests for frameworks you use
if frameworks['fastapi'] and not_has_integration_tests():
    print("FastAPI detected but no integration tests found.")
    print("Consider adding tests for:")
    print("  - API endpoint testing")
    print("  - Database interaction")
    print("  - Authentication flow")
```

### Database Testing (Based on Your Setup)

```python
# Check your actual database setup
if has_sqlalchemy() and not_has_database_tests():
    print("SQLAlchemy detected but no database tests found.")

    # Show you your current models
    models = find_sqlalchemy_models()
    if models:
        print("Found models without tests:")
        for model in models:
            print(f"  - {model.__name__} in {model.__module__}")

    print("Suggest database testing pattern:")
    print("  def test_user_crud_operations(db_session):")
    print("      # Test Create, Read, Update, Delete")
```

## Configuration Examples

### Analysis-Based Enhancements

**I'll show you exactly what I'm changing:**

```python
# Current configuration analysis
current_config = read_pytest_ini()
print("Current pytest.ini:")
for line in current_config:
    print(f"  {line}")

# Suggested changes with diff view
suggested_config = enhance_pytest_config(current_config)
print(f"\nSuggested additions:")
for addition in suggested_config['additions']:
    print(f"  + {addition}")

print(f"\nReason: {suggested_config['reason']}")
print("Backup your current config before applying changes.")
```

### Progressive Configuration

**Only add what you actually need:**

```python
# Check what testing features you need
needs = analyze_testing_needs()
config_additions = {}

if needs['coverage'] and '--cov' not in current_config:
    config_additions['addopts'] = ['--cov=src']
    config_additions['reason'] = "Project size indicates coverage needs"

if needs['markers'] and 'markers' not in current_config:
    config_additions['markers'] = {
        'unit': 'marks tests as unit tests',
        'integration': 'marks tests as integration tests'
    }
    config_additions['reason'] = "Better test organization found"

if config_additions:
    print("Recommended pytest.ini additions:")
    for key, value in config_additions.items():
        if key != 'reason':
            print(f"  {key}: {value}")
    print(f"\nRationale: {config_additions['reason']}")
```

## Mock Testing Examples

### Context-Aware Mocking

**I'll analyze what you're actually testing:**

```python
# Find your external dependencies
external_calls = analyze_external_dependencies()

# Only suggest mocks for actual external calls
if 'requests.get' in external_calls:
    print("Found requests.get() calls in your code.")
    print("Consider mock example:")
    print("  @patch('requests.get')")
    print("  def test_api_call(mock_get):")
    print("      mock_get.return_value.json.return_value = {'id': 1}")
    print("      result = fetch_user_data(1)")
    print("      assert result['id'] == 1")

if 'database_connection' in external_calls:
    print("Found database connections that might need mocking.")
```

### Risk-Based Mocking

**Only mock what could affect test reliability:**

```python
# Analyze risk factors
risk_factors = {
    'external_api_calls': check_external_api_usage(),
    'network_dependencies': check_network_dependencies(),
    'timing_sensitive': check_timing_sensitive_code()
}

if sum(risk_factors.values()) > 2:
    print("Multiple risk factors detected. Consider mocking strategies:")
    print("  1. External API calls for reliability")
    print("  2. Network dependencies to avoid test failures")
    print("  3. Time-sensitive operations for deterministic tests")
```

## Performance Testing Examples

### Need-Based Benchmarking

**Only suggest performance testing when it's actually needed:**

```python
# Check if performance is a concern
performance_indicators = {
    'large_datasets': check_dataset_sizes(),
    'complex_algorithms': check_algorithmic_complexity(),
    'user_complaints': check_performance_issues()
}

if any(performance_indicators.values()):
    print("Performance testing considerations:")

    if performance_indicators['large_datasets']:
        print("  - Large datasets detected: consider performance tests")
        print("  - Example: pytest --benchmark sorting_large_dataset")

    if performance_indicators['complex_algorithms']:
        print("  - Complex algorithms found: benchmark critical paths")

    if performance_indicators['user_complaints']:
        print("  - Performance issues reported: identify bottlenecks")
```

## Dependency Management

### Evidence-Based Package Addition

**Only suggest packages you actually need:**

```python
# Analyze your actual needs
needs = {
    'async_testing': check_async_code_without_tests(),
    'http_testing': check_http_clients_without_tests(),
    'coverage_tools': check_coverage_needs(),
    'performance_tools': check_performance_needs()
}

package_recommendations = []

if needs['async_testing']:
    package_recommendations.append({
        'package': 'pytest-asyncio',
        'reason': f"Found async code in {count_async_files()} files",
        'current_version': get_installed_version('pytest-asyncio')
    })

if package_recommendations:
    print("Recommended package additions:")
    for pkg in package_recommendations:
        print(f"  - {pkg['package']}")
        print(f"    Reason: {pkg['reason']}")
        if pkg['current_version']:
            print(f"    Current version: {pkg['current_version']}")
        else:
            print("    Not currently installed")
```

## Quality Metrics Examples

### Quantitative Analysis

**I'll provide concrete metrics:**

```python
def analyze_test_metrics(test_files):
    """Analyze your test quality with concrete metrics"""

    metrics = {
        'test_count': len(test_files),
        'assertion_count': sum(f.count('assert ') for f in test_files),
        'fixture_usage': sum(f.count('@pytest.fixture') for f in test_files),
        'parametrization': sum(f.count('@pytest.mark.parametrize') for f in test_files)
    }

    # Calculate quality score
    naming_score = calculate_naming_quality(test_files)
    coverage_score = estimate_coverage_quality(test_files)

    print("Test Quality Analysis:")
    print(f"  Test files: {metrics['test_count']}")
    print(f"  Assertions: {metrics['assertion_count']}")
    print(f"  Fixtures: {metrics['fixture_usage']}")
    print(f"  Parametrized tests: {metrics['parametrization']}")
    print(f"  Naming quality: {naming_score}/10")
    print(f"  Coverage quality: {coverage_score}/10")

    overall_score = (naming_score + coverage_score) / 2
    if overall_score >= 8:
        print("  Overall: ✅ Excellent test quality")
    elif overall_score >= 6:
        print("  Overall: ⚠️  Good test quality, minor improvements possible")
    else:
        print("  Overall: 🔄 Test quality needs improvement")
```

## Usage Notes

1. **Evidence First** - All recommendations based on actual project analysis
2. **Backup Conscious** - Always backup before configuration changes
3. **Incremental** - Small, safe improvements over wholesale changes
4. **Context-Aware** - Adapt to your specific project and needs
5. **Risk-Based** - Focus on areas that could cause real problems

Remember: I'll analyze your actual project first and only suggest examples when there's concrete evidence of improvement opportunities. Your existing tests and configurations will be respected unless there are clear issues.