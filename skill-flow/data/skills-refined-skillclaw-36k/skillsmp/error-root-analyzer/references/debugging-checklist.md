# Debugging Checklist

Comprehensive language and framework-specific debugging checklists for systematic error resolution.

## Table of Contents

1. Python Debugging Checklist
2. JavaScript/Node.js Debugging Checklist
3. Java Debugging Checklist
4. C/C++ Debugging Checklist
5. Database Debugging Checklist
6. Web Framework Debugging Checklist
7. API Debugging Checklist

---

## 1. Python Debugging Checklist

### Environment and Dependencies

- [ ] Correct Python version activated (`python --version`)
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] No dependency version conflicts
- [ ] `requirements.txt` or `pyproject.toml` up to date
- [ ] `PYTHONPATH` correctly configured
- [ ] No circular import dependencies

### Code Structure

- [ ] All `__init__.py` files present in packages
- [ ] Import statements at module top (except dynamic imports)
- [ ] No module name shadowing (e.g., file named `json.py`)
- [ ] Relative vs absolute imports used correctly
- [ ] Function/class definitions before usage

### Variable and Type Issues

- [ ] All variables initialized before use
- [ ] Type hints consistent with actual usage
- [ ] No variable shadowing (local hiding global)
- [ ] Mutable default arguments avoided (`def func(x=[]):`)
- [ ] Type conversions explicit where needed
- [ ] `None` checks before attribute/method access

### Function and Method Calls

- [ ] Correct number of arguments passed
- [ ] Keyword arguments spelled correctly
- [ ] `self` parameter in instance methods
- [ ] `cls` parameter in class methods  
- [ ] `@staticmethod` or `@classmethod` decorators as needed
- [ ] Return statements in all code paths (or explicit `return None`)

### Collections and Iterators

- [ ] List/tuple/dict indexing within bounds
- [ ] Dictionary keys exist before access (or use `.get()`)
- [ ] No modification of collection during iteration
- [ ] Generator exhaustion considered
- [ ] Slice indices valid
- [ ] List comprehension vs generator expression chosen appropriately

### File and Resource Handling

- [ ] File paths cross-platform compatible (`pathlib.Path` or `os.path.join`)
- [ ] Files closed properly (use context managers: `with open()`)
- [ ] File modes correct ('r', 'w', 'a', 'rb', 'wb')
- [ ] Directory existence checked before file operations
- [ ] Proper encoding specified for text files
- [ ] Resource cleanup in `finally` or context managers

### Exception Handling

- [ ] Exceptions caught at appropriate level
- [ ] Specific exceptions caught (not bare `except:`)
- [ ] Resources cleaned up in error paths
- [ ] Exception messages informative
- [ ] No silent exception swallowing
- [ ] Custom exceptions inherit from appropriate base
- [ ] `finally` blocks for cleanup

### Object-Oriented Programming

- [ ] `__init__` initializes all instance attributes
- [ ] Parent class `__init__` called in subclasses
- [ ] Method resolution order (MRO) understood
- [ ] Properties have both getter and setter if needed
- [ ] `__str__` and `__repr__` implemented for debugging
- [ ] Class vs instance attributes used correctly

### Async/Await

- [ ] `async def` for coroutine functions
- [ ] `await` used with coroutines
- [ ] Event loop running
- [ ] Blocking operations not in async code
- [ ] `asyncio.run()` or loop management correct
- [ ] Async context managers used (`async with`)

### Performance and Memory

- [ ] No unnecessary data copying
- [ ] Generators used for large datasets
- [ ] List comprehensions vs loops chosen appropriately
- [ ] Large files read in chunks/streamed
- [ ] Database queries paginated
- [ ] No accumulation of large objects in loops

### Testing and Debugging

- [ ] Print/log statements for debugging (remove before commit)
- [ ] Assertions used for invariants
- [ ] Test cases cover edge cases
- [ ] Mock/patch used for external dependencies
- [ ] Debugger breakpoints strategic

---

## 2. JavaScript/Node.js Debugging Checklist

### Environment and Dependencies

- [ ] Correct Node.js version (`node --version`)
- [ ] Dependencies installed (`npm install` or `yarn install`)
- [ ] `package.json` and `package-lock.json` in sync
- [ ] No dependency version conflicts
- [ ] Environment variables set (`.env` file loaded)
- [ ] Module system consistent (CommonJS vs ES6 modules)

### Code Structure

- [ ] Imports/requires before usage
- [ ] Export statements correct (`module.exports`, `export`, `export default`)
- [ ] File extensions in imports if required
- [ ] No circular dependencies

### Variable and Type Issues

- [ ] `const` vs `let` vs `var` used appropriately
- [ ] Variable hoisting understood
- [ ] `undefined` vs `null` distinction clear
- [ ] Type coercion considered (use `===` not `==`)
- [ ] Truthy/falsy values understood
- [ ] Template literals for string interpolation

### Function Issues

- [ ] `this` binding correct (arrow functions vs regular)
- [ ] Callback functions not called prematurely
- [ ] Arrow function parentheses for single param
- [ ] Default parameters used instead of `||` pattern
- [ ] Rest parameters syntax correct (`...args`)
- [ ] Destructuring syntax valid

### Promises and Async

- [ ] Promises have `.catch()` or `try/catch`
- [ ] `async` functions return promises
- [ ] `await` only in `async` functions
- [ ] Promise chains use `.then()` correctly
- [ ] No mixing callbacks and promises
- [ ] `Promise.all()` vs `Promise.race()` used correctly
- [ ] Unhandled promise rejection listeners added

### Objects and Arrays

- [ ] Array methods not mutating when immutability expected
- [ ] Object property access checked (`obj?.prop` or `obj.hasOwnProperty`)
- [ ] Spread operator used correctly
- [ ] Array indices within bounds
- [ ] JSON parse/stringify error handling

### Error Handling

- [ ] Try/catch blocks around risky operations
- [ ] Errors thrown with meaningful messages
- [ ] Error objects have stack traces
- [ ] Custom error classes extend Error
- [ ] Async errors caught properly

### Browser-Specific (Frontend)

- [ ] DOM elements exist before access
- [ ] Event listeners attached after DOM ready
- [ ] Event delegation for dynamic elements
- [ ] CORS configured for API calls
- [ ] LocalStorage/SessionStorage quota not exceeded
- [ ] Memory leaks from event listeners addressed

### Node.js-Specific (Backend)

- [ ] Callback error handling (`if (err)`)
- [ ] Streams properly closed
- [ ] Buffer encoding specified
- [ ] File paths use `path.join()`
- [ ] Process exit codes appropriate
- [ ] Uncaught exception handlers present

---

## 3. Java Debugging Checklist

### Environment and Dependencies

- [ ] Correct JDK version
- [ ] CLASSPATH configured
- [ ] All dependencies in build file (Maven/Gradle)
- [ ] Build successful without errors
- [ ] Environment-specific configs correct

### Code Structure

- [ ] Package declarations match directory structure
- [ ] Import statements present and correct
- [ ] Class names match file names
- [ ] Public classes one per file
- [ ] Access modifiers appropriate

### Variable and Type Issues

- [ ] Variables initialized before use
- [ ] Primitives vs objects distinction clear
- [ ] Autoboxing/unboxing understood
- [ ] Type casting safe
- [ ] Generic types specified
- [ ] Null checks before dereferencing

### Object-Oriented Issues

- [ ] Constructors initialize all fields
- [ ] Super constructor called if needed
- [ ] Method overriding vs overloading understood
- [ ] Abstract methods implemented
- [ ] Interface methods implemented
- [ ] Access to private members valid

### Collections

- [ ] Correct collection type chosen
- [ ] Generic types specified
- [ ] No modification during iteration (or use Iterator.remove())
- [ ] Equals and hashCode overridden for custom keys
- [ ] Collections not null before operations

### Exception Handling

- [ ] Checked exceptions caught or declared
- [ ] Resources closed in finally or try-with-resources
- [ ] Specific exceptions caught
- [ ] Exception messages informative
- [ ] Custom exceptions extend appropriate base class

### Concurrency

- [ ] Shared variables synchronized
- [ ] No race conditions
- [ ] Deadlock potential analyzed
- [ ] Thread-safe collections used
- [ ] Volatile keyword used appropriately
- [ ] Executors shut down properly

### Memory and Resources

- [ ] No memory leaks from collections
- [ ] Resources closed (files, connections, streams)
- [ ] String concatenation in loops avoided
- [ ] Large objects dereferenced when done
- [ ] Static collections cleaned up

---

## 4. C/C++ Debugging Checklist

### Memory Management

- [ ] Every `malloc`/`new` has corresponding `free`/`delete`
- [ ] No double free
- [ ] No use after free
- [ ] Array `new[]` matched with `delete[]`
- [ ] Null pointer checks before dereferencing
- [ ] Buffer sizes validated
- [ ] No buffer overflows
- [ ] String null terminators present

### Pointers

- [ ] Pointers initialized (not wild pointers)
- [ ] Pointer arithmetic within bounds
- [ ] Dereferencing only valid pointers
- [ ] Function pointers signature matches
- [ ] Smart pointers used (C++)
- [ ] Reference vs pointer usage appropriate

### Arrays and Strings

- [ ] Array indices within bounds
- [ ] String functions buffer sizes correct
- [ ] strncpy/snprintf used instead of strcpy/sprintf
- [ ] Null terminators in strings
- [ ] Character arrays sized appropriately

### Functions

- [ ] Function signatures match declarations
- [ ] Return values checked
- [ ] Parameters passed correctly (by value/ref/pointer)
- [ ] Static vs extern understood
- [ ] Recursion has base case
- [ ] Stack overflow potential considered

### Compilation and Linking

- [ ] All warnings addressed (`-Wall -Wextra`)
- [ ] Header guards prevent double inclusion
- [ ] Declarations and definitions match
- [ ] External linkage correct
- [ ] Library linking order correct
- [ ] Undefined references resolved

### Concurrency

- [ ] Race conditions identified
- [ ] Mutexes locked/unlocked correctly
- [ ] Deadlock potential analyzed
- [ ] Atomic operations used where needed
- [ ] Thread joining/detaching correct

---

## 5. Database Debugging Checklist

### Connection Issues

- [ ] Database service running
- [ ] Connection string correct (host, port, database)
- [ ] Authentication credentials valid
- [ ] Network connectivity verified
- [ ] Connection pool configured
- [ ] Connections closed after use
- [ ] Maximum connections not exceeded

### Query Issues

- [ ] SQL syntax valid for database dialect
- [ ] Table and column names correct (case sensitivity)
- [ ] JOINs have appropriate conditions
- [ ] WHERE clauses filter correctly
- [ ] NULL handling explicit
- [ ] Subqueries return expected result set
- [ ] Query performance acceptable (use EXPLAIN)

### Data Issues

- [ ] Data types match schema
- [ ] Constraints validated before insert/update
- [ ] Foreign key relationships maintained
- [ ] Unique constraints not violated
- [ ] NOT NULL constraints satisfied
- [ ] Date/time formats correct
- [ ] String length within column limits

### Transaction Issues

- [ ] Transactions committed or rolled back
- [ ] Isolation level appropriate
- [ ] Deadlock detection and handling
- [ ] Long transactions avoided
- [ ] No uncommitted transactions left open

### Schema Issues

- [ ] Tables and indexes exist
- [ ] Schema migrations applied
- [ ] Permissions granted
- [ ] Views and procedures up to date

---

## 6. Web Framework Debugging Checklist

### Routing

- [ ] Routes defined before server start
- [ ] Route patterns correct (URL parameters syntax)
- [ ] HTTP methods match (GET, POST, PUT, DELETE)
- [ ] Route parameters extracted correctly
- [ ] Middleware order correct
- [ ] Route conflicts resolved (most specific first)

### Request/Response

- [ ] Request body parsed correctly
- [ ] Content-Type headers set
- [ ] Response status codes appropriate
- [ ] Headers sent before body
- [ ] Response sent only once
- [ ] Redirects use correct status codes

### Middleware

- [ ] Middleware next() called if not terminal
- [ ] Middleware order matters
- [ ] Error middleware has 4 parameters
- [ ] Async middleware errors caught

### Templates/Views

- [ ] Template files exist at correct path
- [ ] Template variables passed correctly
- [ ] Template syntax valid
- [ ] Template escaping for XSS protection

### Session/Auth

- [ ] Session middleware configured
- [ ] Session secret set and secure
- [ ] Authentication checked for protected routes
- [ ] Cookies configured correctly
- [ ] CSRF protection enabled

---

## 7. API Debugging Checklist

### Request Issues

- [ ] Endpoint URL correct
- [ ] HTTP method correct
- [ ] Headers included (Authorization, Content-Type)
- [ ] Request body format correct (JSON, form data)
- [ ] Query parameters properly encoded
- [ ] Timeout configured appropriately

### Response Issues

- [ ] Status code checked
- [ ] Response body parsed correctly
- [ ] Error responses handled
- [ ] Pagination implemented for large datasets
- [ ] Rate limiting considered

### Authentication

- [ ] API keys/tokens valid
- [ ] Authentication header format correct
- [ ] Token expiration handled
- [ ] Refresh token mechanism working
- [ ] OAuth flow completed correctly

### Data Validation

- [ ] Request data validated
- [ ] Response data schema validated
- [ ] Required fields present
- [ ] Data types correct
- [ ] Enum values valid

### Error Handling

- [ ] Network errors caught
- [ ] Timeout errors handled
- [ ] 4xx errors handled gracefully
- [ ] 5xx errors retried appropriately
- [ ] Error messages logged

---

## General Debugging Workflow

For any issue:

1. **Reproduce**: Consistently reproduce the error
2. **Isolate**: Narrow down to minimal failing case
3. **Check Environment**: Verify environment setup correct
4. **Review Code**: Walk through code logic step by step
5. **Use Tools**: Debugger, profiler, linter as appropriate
6. **Check Logs**: Review all relevant logs
7. **Test Assumptions**: Validate all assumptions with assertions/logs
8. **Fix Root Cause**: Address fundamental issue, not symptom
9. **Test Thoroughly**: Verify fix and check for regressions
10. **Document**: Record what failed and how it was fixed
