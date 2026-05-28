# Common Error Patterns and Root Causes

This document catalogs common error patterns, their typical root causes, and systematic approaches to resolution.

## Table of Contents

1. Import and Dependency Errors
2. Type Errors
3. Attribute and Name Errors
4. Index and Key Errors
5. File and I/O Errors
6. Network and Connection Errors
7. Database Errors
8. Memory and Resource Errors
9. Concurrency Errors
10. Configuration Errors

---

## 1. Import and Dependency Errors

### ModuleNotFoundError / ImportError

**Surface Symptoms:**
- `ModuleNotFoundError: No module named 'X'`
- `ImportError: cannot import name 'Y' from 'X'`

**Root Causes:**
- Module not installed in current environment
- Wrong virtual environment activated
- Typo in module name
- Circular import dependency
- Module file doesn't exist at expected path
- PYTHONPATH misconfiguration
- Package structure issues (`__init__.py` missing)

**Investigation Steps:**
1. Verify module installation: `pip list | grep module_name`
2. Check virtual environment: `which python` or `where python`
3. Verify PYTHONPATH: `echo $PYTHONPATH` or `$env:PYTHONPATH`
4. Check for circular imports by reviewing import graph
5. Verify package structure and `__init__.py` files
6. Check Python version compatibility

**Comprehensive Fix:**
- Install missing dependencies
- Fix import order to break circular dependencies
- Update PYTHONPATH or use relative imports correctly
- Add missing `__init__.py` files
- Review entire module for other import issues
- Document dependencies in requirements.txt

---

## 2. Type Errors

### TypeError: Argument Type Mismatch

**Surface Symptoms:**
- `TypeError: unsupported operand type(s)`
- `TypeError: 'X' object is not callable`
- `TypeError: argument X must be Y, not Z`

**Root Causes:**
- Incorrect type passed to function
- Missing type conversion
- Variable shadowing (function/class name overwritten)
- API contract violation
- Deserialization producing wrong type
- Default value with wrong type

**Investigation Steps:**
1. Trace variable origin and transformations
2. Check all assignments to the variable
3. Review function signature and docstring
4. Check for variable shadowing
5. Verify data deserialization logic
6. Review type hints and mypy/pyright feedback

**Comprehensive Fix:**
- Add type conversion at appropriate point
- Implement input validation
- Add type hints throughout module
- Use runtime type checking for critical paths
- Review all function calls in module for similar issues
- Add assertions for type invariants

---

## 3. Attribute and Name Errors

### AttributeError

**Surface Symptoms:**
- `AttributeError: 'X' object has no attribute 'Y'`
- `AttributeError: 'NoneType' object has no attribute 'Y'`

**Root Causes:**
- Object not initialized properly
- Accessing attribute before it's set
- None returned instead of expected object
- API version mismatch
- Typo in attribute name
- Conditional initialization path not taken
- Object lifecycle issue

**Investigation Steps:**
1. Check object initialization code
2. Trace variable assignments leading to access
3. Verify all code paths set required attributes
4. Check if function returned None unexpectedly
5. Review object lifecycle and state machine
6. Check API documentation for version changes

**Comprehensive Fix:**
- Initialize all attributes in `__init__`
- Add None checks before attribute access
- Use `getattr()` with defaults where appropriate
- Fix conditional initialization logic
- Review entire class for initialization completeness
- Add validation in setter methods

### NameError

**Surface Symptoms:**
- `NameError: name 'X' is not defined`

**Root Causes:**
- Variable used before assignment
- Typo in variable name
- Scope issue (variable not in current scope)
- Conditional assignment path not taken
- Import statement missing or failed silently

**Investigation Steps:**
1. Check if variable is defined before use
2. Verify variable scope (local vs global)
3. Check all code paths for variable definition
4. Look for typos in variable names
5. Check import statements

**Comprehensive Fix:**
- Define variable before use
- Fix scope issues (use `nonlocal` or `global` if needed)
- Ensure all paths define required variables
- Add default values where appropriate
- Review module for similar issues

---

## 4. Index and Key Errors

### IndexError

**Surface Symptoms:**
- `IndexError: list index out of range`
- `IndexError: tuple index out of range`

**Root Causes:**
- Empty collection accessed
- Off-by-one error in loop/index
- Wrong assumption about collection size
- Collection modified during iteration
- Incorrect slice bounds

**Investigation Steps:**
1. Check collection size before access
2. Review index calculation logic
3. Verify loop bounds
4. Check for collection modifications during iteration
5. Review collection population logic

**Comprehensive Fix:**
- Add bounds checking before access
- Fix loop bounds (use `range(len(x))` carefully)
- Use enumeration or iteration instead of indexing
- Validate collection size assumptions
- Add defensive programming (try/except or size checks)
- Review all indexing operations in module

### KeyError

**Surface Symptoms:**
- `KeyError: 'X'`

**Root Causes:**
- Key doesn't exist in dictionary
- Wrong key name (typo or case mismatch)
- Dictionary not populated as expected
- Data schema changed
- Missing data validation

**Investigation Steps:**
1. Check if key exists before access: `'key' in dict`
2. Review dictionary population logic
3. Verify data source schema
4. Check for typos in key names
5. Review data validation logic

**Comprehensive Fix:**
- Use `dict.get(key, default)` instead of `dict[key]`
- Add key existence checks
- Validate data schema on input
- Use default dictinaries where appropriate
- Add data validation layer
- Review all dictionary accesses in module

---

## 5. File and I/O Errors

### FileNotFoundError

**Surface Symptoms:**
- `FileNotFoundError: [Errno 2] No such file or directory`

**Root Causes:**
- File path incorrect (absolute vs relative)
- File doesn't exist
- Working directory not what expected
- Path separator issues (Windows vs Unix)
- Permissions issue (appears as not found)
- Symbolic link broken

**Investigation Steps:**
1. Print absolute path being accessed
2. Check current working directory: `os.getcwd()`
3. Verify file exists: `os.path.exists(path)`
4. Check file permissions
5. Verify path construction logic
6. Check for path separator issues

**Comprehensive Fix:**
- Use absolute paths or `Path` from pathlib
- Verify file existence before access
- Create directories if needed: `makedirs(exist_ok=True)`
- Use `os.path.join()` or `pathlib.Path` for cross-platform paths
- Add better error messages with full path
- Review all file operations in module

### PermissionError

**Surface Symptoms:**
- `PermissionError: [Errno 13] Permission denied`

**Root Causes:**
- Insufficient file/directory permissions
- File locked by another process
- Trying to write to read-only location
- Process doesn't have required privileges
- File open in another application

**Investigation Steps:**
1. Check file permissions: `os.stat(path).st_mode`
2. Verify user has write access
3. Check if file is locked
4. Verify directory permissions
5. Check if running with required privileges

**Comprehensive Fix:**
- Request appropriate permissions
- Check permissions before access
- Use appropriate file modes ('r', 'w', 'a')
- Close files properly (use context managers)
- Add permission verification
- Document permission requirements

---

## 6. Network and Connection Errors

### ConnectionError / TimeoutError

**Surface Symptoms:**
- `ConnectionError: Failed to establish a new connection`
- `TimeoutError: timed out`
- `requests.exceptions.ConnectionError`

**Root Causes:**
- Service not running
- Wrong host/port
- Network connectivity issues
- Firewall blocking connection
- Service overloaded
- DNS resolution failure
- SSL/TLS certificate issues

**Investigation Steps:**
1. Verify service is running
2. Test connection manually (telnet, curl)
3. Check host and port configuration
4. Verify network conectivity
5. Check firewall rules
6. Review timeout settings
7. Check SSL certificates

**Comprehensive Fix:**
- Add connection retry logic with exponential backoff
- Implement connection pooling
- Add health checks before operations
- Configure appropriate timeouts
- Add fallback mechanisms
- Implement circuit breaker pattern
- Log connection attempts for debugging
- Review all network calls in module

---

## 7. Database Errors

### Operational Errors

**Surface Symptoms:**
- `OperationalError: database is locked`
- `OperationalError: no such table`
- `IntegrityError: UNIQUE constraint failed`

**Root Causes:**
- Database not initialized
- Schema not created or migrated
- Concurrent access without proper locking
- Data violates constraints
- Transaction not committed
- Connection not closed properly

**Investigation Steps:**
1. Verify database initialization
2. Check schema version/migrations
3. Review transaction handling
4. Check constraint definitions
5. Verify connection management
6. Review concurrent access patterns

**Comprehensive Fix:**
- Initialize database schema properly
- Add migration system
- Implement proper transaction management
- Add data validation before insert/update
- Use connection pooling
- Implement retry logic for locks
- Add conflict resolution strategies
- Review all database operations in module

---

## 8. Memory and Resource Errors

### MemoryError

**Surface Symptoms:**
- `MemoryError`
- Process killed by OS (OOM killer)

**Root Causes:**
- Loading too much data in memory
- Memory leak (objects not garbage collected)
- Infinite data structure growth
- Large file read without streaming
- Inefficient data structures

**Investigation Steps:**
1. Profile memory usage
2. Check for memory leaks
3. Review data loading patterns
4. Check collection growth
5. Verify garbage collection
6. Review generator vs list usage

**Comprehensive Fix:**
- Use generators/iterators for large datasets
- Implement streaming for file operations
- Add pagination for database queries
- Break large operations into chunks
- Clear references to large objects
- Use memory-efficient data structures
- Add memory monitoring
- Review entire module for memory issues

---

## 9. Concurrency Errors

### Race Conditions

**Surface Symptoms:**
- Inconsistent results
- Sporadic failures
- Data corruption
- Deadlocks

**Root Causes:**
- Unsynchronized access to shared state
- Lock ordering issues
- Missing locks
- Async/await misuse
- Thread-unsafe libraries

**Investigation Steps:**
1. Identify shared state
2. Review synchronization mechanisms
3. Check lock acquisition order
4. Verify thread-safe library usage
5. Review async/await patterns
6. Use race detection tools

**Comprehensive Fix:**
- Add appropriate locks/semaphores
- Use thread-safe data structures
- Implement proper lock ordering
- Use atomic operations where possible
- Consider lock-free algorithms
- Add synchronization logging
- Review all concurrent code paths

---

## 10. Configuration Errors

### Configuration Missing or Invalid

**Surface Symptoms:**
- KeyError on config access
- ValueError from invalid config values
- Application starts but behaves incorrectly

**Root Causes:**
- Environment variables not set
- Config file missing or malformed
- Default values not provided
- Configuration not validated
- Case-sensitive config keys
- Type mismatch in config values

**Investigation Steps:**
1. Check which config is expected
2. Verify config sources (env, file, defaults)
3. Check config validation logic
4. Review default value handling
5. Verify config file format
6. Check environment variable names

**Comprehensive Fix:**
- Implement config validation on startup
- Provide sensible defaults
- Document all required configuration
- Add config file examples
- Validate config types and ranges
- Add helpful error messages for missing config
- Use configuration library (pydantic, configparser)
- Review all config accesses in application

---

## General Investigation Pattern

For any error, follow this pattern:

1. **Collect**: Full stack trace, error message, input state, environment
2. **Categorize**: Which pattern does this match?
3. **Trace Back**: Find where incorrect state originated
4. **Root Cause**: Identify fundamental cause, not symptom
5. **Expand**: Review entire module for related issues
6. **Fix Completely**: Address root cause + related issues + add prevention
7. **Verify**: Test fix + regression test + integration test
8. **Document**: What failed, why, what was fixed, how to prevent
