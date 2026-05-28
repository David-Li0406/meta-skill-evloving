# Python Testing Troubleshooting - Evidence-Based

I provide troubleshooting solutions based on your actual project analysis. I'll examine your current setup and provide targeted fixes for specific issues.

## Project Context Analysis

Before providing solutions, I'll analyze:
```python
# Your current setup (I use Read/Glob tools)
project_config = detect_configuration_files()
installed_packages = check_current_packages()
python_version = get_python_version()
error_context = analyze_error_patterns()

# Your actual testing issues
test_discovery_issues = check_test_discovery()
configuration_problems = identify_configuration_issues()
execution_failures = analyze_test_failures()
```

## Issue-Based Troubleshooting

### Test Discovery Problems

#### First, I'll check your actual structure:

```python
# Files not found - I'll analyze your actual project
if test_files_exist() and not_discovering():
    print("🔍 Analyzing test discovery issues...")

    # Check your actual file naming patterns
    found_files = glob("**/*test*.py", recursive=True)
    py_files = glob("**/*.py", recursive=True)

    print(f"Found {len(found_files)} files with 'test' in name")
    print(f"Total Python files: {len(py_files)}")

    # Check naming convention compliance
    test_pattern_compliant = [
        f for f in found_files
        if f.startswith("test_") or f.endswith("_test.py")
    ]

    print(f"Files following pytest naming: {len(test_pattern_compliant)}")

    # Show specific issues
    non_compliant = [
        f for f in found_files
        if not (f.startswith("test_") or f.endswith("_test.py"))
    ]

    if non_compliant:
        print("\nFiles that don't follow pytest naming convention:")
        for f in non_compliant[:5]:  # Show first 5
            print(f"  - {f}")
        print("    Should be: test_{name} or {name}_test.py")
```

#### Configuration File Detection

```python
# Check what configuration you actually have
config_files = {
    'pyproject.toml': glob("pyproject.toml"),
    'pytest.ini': glob("pytest.ini"),
    'setup.cfg': glob("setup.cfg"),
    'tox.ini': glob("tox.ini")
}

if not any(config_files.values()):
    print("No pytest configuration files found.")
    print("Consider creating pytest.ini with basic configuration:")
    print("  [tool:pytest]")
    print("  testpaths = tests")
    print("  python_files = test_*.py *_test.py")
```

### Import Errors (Project-Specific Analysis)

#### Python Path Issues

```python
# I'll analyze your actual project structure
project_structure = analyze_project_layout()
import_errors = detect_import_errors()

if import_errors:
    print(f"🔍 Found {len(import_errors)} import issues:")

    for error in import_errors[:5]:  # Show first 5
        print(f"  - {error['file']}:{error['line']}: {error['error']}")
        print(f"    Trying to import: {error['import_module']}")

    # Provide solution based on your structure
    if project_structure['layout'] == 'src_layout':
        print("    Solution: Install in development mode:")
        print("      pip install -e .")
        print("    Or add to PYTHONPATH:")
        print("      export PYTHONPATH=$(pwd)/src:$PYTHONPATH")

    elif project_structure['layout'] == 'flat_layout':
        print("    Solution: Add current directory to path:")
        print("      export PYTHONPATH=$(pwd):$PYTHONPATH")
```

#### Dependency Conflicts

```python
# Check for actual dependency conflicts
conflicts = analyze_dependency_conflicts()

if conflicts:
    print("⚠️ Dependency conflicts detected:")
    for conflict in conflicts:
        print(f"  - {conflict['package']}: {conflict['issue']}")
        print(f"    Current: {conflict['installed_version']}")
        print(f"    Required: {conflict['required_version']}")

    # Provide specific resolution
    if conflict['resolution_type'] == 'upgrade':
        print(f"    Resolution: pip install {conflict['package']}>={conflict['required_version']}")
    elif conflict['resolution_type'] == 'downgrade':
        print(f"    Resolution: pip install {conflict['package']}=={conflict['required_version']}")
```

### Test Execution Issues

#### Fixture Problems

```python
# Analyze your actual fixture usage
fixture_issues = analyze_fixture_issues()

if fixture_issues:
    print("🔧 Fixture-related issues found:")

    for issue in fixture_issues:
        print(f"  - {issue['test_file']}:{issue['line']}: {issue['description']}")

        if issue['type'] == 'undefined_fixture':
            print(f"    Undefined fixture: {issue['fixture_name']}")
            similar_fixtures = find_similar_fixtures(issue['fixture_name'])
            if similar_fixtures:
                print(f"    Did you mean: {similar_fixtures[0]}?")

        elif issue['type'] == 'scope_mismatch':
            print(f"    Fixture scope issue: {issue['current_scope']}")
            print(f"    Suggested scope: {issue['suggested_scope']}")
```

#### Assertion Failures

```python
# Analyze actual assertion failures
assertion_failures = analyze_assertion_failures()

for failure in assertion_failures:
    print(f"❌ {failure['test_file']}:{failure['line']}")
    print(f"   Expected: {failure['expected']}")
    print(f"   Actual: {failure['actual']}")
    print(f"   Context: {failure['context']}")

    # Provide targeted fix suggestions
    if "float comparison" in failure['context']:
        print("   💡 Consider using pytest.approx for floating point comparisons")
        print(f"   Suggested: assert {failure['expected'].replace('==', '== pytest.approx')}")

    elif "collection length" in failure['context']:
        print("   💡 Check collection contents:")
        print(f"   Debug: print(len({failure['actual_variable']}))")
```

## Configuration-Specific Issues

### pytest.ini Problems

```python
# Analyze your actual pytest.ini
config_content = read_pytest_ini()
config_issues = analyze_pytest_ini_issues(config_content)

for issue in config_issues:
    print(f"⚙️ pytest.ini issue: {issue}")
    print(f"   Line: {issue['line_number']}")
    print(f"   Current: {issue['current_content']}")
    print(f"   Suggested: {issue['suggested_content']}")
```

### pyproject.toml Integration

```python
# Check if pyproject.toml is properly configured
if has_pyproject_toml():
    toml_content = read_pyproject_toml()

    if '[tool.pytest.ini_options]' not in toml_content:
        print("⚙️ pyproject.toml found but pytest config missing")
        print("Add this section to your pyproject.toml:")
        print("""
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
""")
```

## Environment-Specific Issues

### Virtual Environment Problems

```python
# Check your actual environment setup
env_analysis = analyze_environment()

if env_analysis['python_path_issues']:
    print("🌍 Python path issues detected:")
    print("  Current PYTHONPATH:", env_analysis['current_path'])
    print("  Project not in path")

    # Provide targeted fix
    if env_analysis['project_location']:
        print("  Fix: export PYTHONPATH={project_location}:$PYTHONPATH")

if env_analysis['package_conflicts']:
    print("📦 Package conflicts found:")
    for conflict in env_analysis['package_conflicts']:
        print(f"  - {conflict}")
        print(f"    Try: pip install --force-reinstall {conflict}")
```

### CI/CD Testing Failures

```python
# Analyze CI configuration if it exists
ci_config = detect_ci_configuration()

if ci_config and test_failures_in_ci:
    print("🔄 CI testing issues found:")
    print(f"  Platform: {ci_config['platform']}")
    print(f"  Python version: {ci_config['python_version']}")

    # Compare with local environment
    local_version = get_python_version()
    if local_version != ci_config['python_version']:
        print(f"  Version mismatch: local={local_version}, CI={ci_config['python_version']}")
        print(f"  Consider: Use same Python version locally")
```

## Real-time Error Analysis

### When You Report Specific Errors

I'll analyze your specific error context:

```python
def analyze_specific_error(error_message, stack_trace):
    """Analyze your specific error with full context"""

    print("🔍 Analyzing error context...")

    # Extract key information
    error_type = extract_error_type(error_message)
    test_file = extract_test_file(stack_trace)
    line_number = extract_line_number(stack_trace)

    print(f"Error Type: {error_type}")
    print(f"Location: {test_file}:{line_number}")

    # Check for common patterns
    if "ModuleNotFoundError" in error_message:
        missing_module = extract_missing_module(error_message)
        print(f"Missing module: {missing_module}")

        # Check if it's a dependency issue
        if missing_module in get_required_packages():
            print(f"Required dependency not installed. Try:")
            print(f"  pip install {missing_module}")
        else:
            print(f"Import issue - check PYTHONPATH and project structure")

    # Provide specific fixes based on actual error
    provide_specific_fix(error_type, error_message, stack_trace)
```

## Progressive Problem Solving

### Step 1: Diagnose with Evidence

```python
# Always start with concrete evidence
def diagnose_testing_issue():
    """Provide evidence-based diagnosis"""

    evidence = {
        'project_structure': analyze_project_layout(),
        'existing_tests': find_test_files(),
        'configuration': detect_configuration(),
        'environment': analyze_environment(),
        'recent_failures': get_recent_test_failures()
    }

    return evidence
```

### Step 2: Targeted Solutions

```python
# Provide solutions only for identified issues
def provide_targeted_solutions(evidence):
    """Solutions based on actual analysis"""

    solutions = []

    if evidence['environment']['python_path_issues']:
        solutions.append({
            'type': 'environment',
            'issue': 'Python path problem',
            'fix': 'export PYTHONPATH=...',
            'command': 'export PYTHONPATH=$PWD/src:$PYTHONPATH'
        })

    if evidence['configuration']['missing_config']:
        solutions.append({
            'type': 'configuration',
            'issue': 'No pytest configuration',
            'fix': 'Create pytest.ini',
            'example': '[tool:pytest]\ntestpaths = tests\n'
        })

    return solutions
```

## Getting Help with Specific Issues

### When You Report Problems

Provide context about your issue:

```python
# When you report a problem, please include:
context = {
    'error_message': "The full error you're seeing",
    'command_run': "Command you ran (e.g., pytest tests/)",
    'expected_behavior': "What you expected to happen",
    'actual_result': "What actually happened",
    'recent_changes': "Any recent changes to tests or configuration"
}
```

### Example Issue Report

```
❌ Error Message: ModuleNotFoundError: No module named 'pytest_asyncio'
🔍 Command Run: pytest tests/test_async.py
📋 Expected: Tests should run with async support
📍 Actual Result: Module import error
📝 Recent Changes: Added async test function

🔍 Analysis: Async test found but pytest-asyncio not installed
💡 Solution: pip install pytest-asyncio
✅ Verification: pytest --version should show pytest-asyncio plugin
```

## Key Principles

1. **Evidence First** - Always start with actual project analysis
2. **Context-Aware** - Solutions tailored to your specific setup
3. **Backup Conscious** - Remind to backup before configuration changes
4. **Incremental** - One fix at a time, verify each works
5. **Verification** - Test each solution before moving to the next

Remember: I'll analyze your actual project and provide specific, actionable solutions based on concrete evidence rather than generic troubleshooting advice.