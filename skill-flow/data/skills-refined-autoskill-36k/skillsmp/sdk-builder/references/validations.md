# Sdk Builder - Validations

## HTTP Client Without Timeout

### **Id**
no-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - httpx\.Client\(\)
  - httpx\.AsyncClient\(\)
  - requests\.get\([^,]*\)$
  - requests\.post\([^,]*\)$
### **Message**
HTTP client without timeout. Requests can hang indefinitely.
### **Fix Action**
Add timeout parameter: httpx.AsyncClient(timeout=30.0)
### **Applies To**
  - **/*.py

## Credentials in Error Message

### **Id**
credential-in-error
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - raise.*api_key
  - raise.*secret
  - raise.*password
  - raise.*token.*=
  - Error.*f.*api_key
### **Message**
Potential credential leak in error message. Never include secrets.
### **Fix Action**
Remove credentials from error: raise AuthError('Invalid API key')
### **Applies To**
  - **/*.py

## Dict Return Instead of Typed Object

### **Id**
dict-return-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - -> dict:
  - -> Dict\[
  - -> dict\[str, Any\]
### **Message**
Returning dict loses type safety. Use Pydantic model or dataclass.
### **Fix Action**
Return typed object: -> Memory instead of -> dict
### **Applies To**
  - **/client*.py
  - **/sdk*.py

## Bare Exception in SDK

### **Id**
bare-exception-sdk
### **Severity**
error
### **Type**
regex
### **Pattern**
  - except:
  - except Exception:
### **Message**
Bare exception hides errors from SDK users. Be specific.
### **Fix Action**
Catch and convert to SDK-specific errors: except httpx.HTTPError as e:
### **Applies To**
  - **/*.py

## New HTTP Client Per Request

### **Id**
new-client-per-request
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async with httpx\.AsyncClient
  - with requests\.Session\(\)
### **Message**
Creating new client per request. Reuse client for connection pooling.
### **Fix Action**
Create client once in __init__, reuse for all requests
### **Applies To**
  - **/*.py

## Sync HTTP in Async SDK

### **Id**
sync-in-async-sdk
### **Severity**
error
### **Type**
regex
### **Pattern**
  - async def.*\n.*requests\.
  - async def.*\n.*urllib
### **Message**
Using sync HTTP in async function. Use httpx or aiohttp.
### **Fix Action**
Replace requests with httpx.AsyncClient
### **Applies To**
  - **/*.py

## No Retry Logic

### **Id**
no-retry-logic
### **Severity**
info
### **Type**
regex
### **Pattern**
  - await.*\.get\(
  - await.*\.post\(
### **Message**
No retry logic visible. Consider adding for transient failures.
### **Fix Action**
Add retry wrapper with exponential backoff for 5xx and 429
### **Applies To**
  - **/client*.py
  - **/http*.py

## Magic String Instead of Enum

### **Id**
magic-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - "episodic"|"semantic"|"procedural"
  - "pending"|"completed"|"failed"
### **Message**
Magic string should be enum or Literal for type safety.
### **Fix Action**
Use enum: MemoryType.EPISODIC or Literal['episodic', 'semantic']
### **Applies To**
  - **/*.py

## Missing __repr__ on Client

### **Id**
no-repr
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Client.*:(?!.*__repr__)
### **Message**
Client class without __repr__. Debug output may leak credentials.
### **Fix Action**
Add __repr__ that masks sensitive fields
### **Applies To**
  - **/client*.py

## Retry Without Backoff

### **Id**
immediate-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sleep\(0\)
  - sleep\(1\)
  - for.*retry.*:(?!.*sleep)
### **Message**
Retry without backoff can overwhelm servers.
### **Fix Action**
Add exponential backoff: delay = initial * (2 ** attempt)
### **Applies To**
  - **/*.py

## Potential Credential Logging

### **Id**
credential-logging
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - logger.*headers
  - print.*headers
  - log.*Authorization
### **Message**
Logging headers may expose credentials.
### **Fix Action**
Never log headers containing Authorization or API keys
### **Applies To**
  - **/*.py

## Client Without Close Method

### **Id**
missing-close
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*Client.*:(?!.*close|.*__aexit__|.*__exit__)
### **Message**
HTTP client should have close() or context manager support.
### **Fix Action**
Add async def close() and __aenter__/__aexit__ methods
### **Applies To**
  - **/client*.py