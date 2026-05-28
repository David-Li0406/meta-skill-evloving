# Python Backend - Validations

## Hardcoded secret in code

### **Id**
hardcoded-secret
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (password|api_key|secret|token)\s*=\s*["'][^"']{8,}
  - SECRET_KEY\s*=\s*["'][^"']+["']
### **Message**
Secrets should be in environment variables, not code
### **Fix Action**
Use os.getenv() or pydantic-settings
### **Applies To**
  - *.py

## Possible SQL injection

### **Id**
sql-injection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - execute\s*\(\s*f["']
  - execute\s*\([^)]*%\s*\(
  - raw\s*\(\s*f["']
### **Message**
Use parameterized queries to prevent SQL injection
### **Fix Action**
Use query parameters: execute(sql, (param,))
### **Applies To**
  - *.py

## Debug mode enabled

### **Id**
debug-enabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DEBUG\s*=\s*True
  - debug\s*=\s*True
### **Message**
Debug mode should be disabled in production
### **Fix Action**
Use environment variable: DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
### **Applies To**
  - *.py
  - settings.py

## Blocking call in async function

### **Id**
blocking-in-async
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async def.*\n.*requests\.
  - async def.*\n.*time\.sleep
  - async def.*\n.*\.objects\.(get|filter|all|create)
### **Message**
Blocking calls in async functions block the event loop
### **Fix Action**
Use async alternatives: httpx, asyncio.sleep, sync_to_async
### **Applies To**
  - *.py

## Potential N+1 query

### **Id**
django-n-plus-one
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*in.*\.all\(\)|for.*in.*objects\.
### **Message**
Loop over queryset may cause N+1 queries
### **Fix Action**
Use select_related() or prefetch_related()
### **Applies To**
  - *.py

## Model change without migration

### **Id**
missing-migration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class\s+\w+\(models\.Model\)
### **Message**
Remember to create migrations after model changes
### **Fix Action**
Run: python manage.py makemigrations
### **Applies To**
  - models.py

## Function without return type hint

### **Id**
no-return-type
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def \w+\([^)]*\)\s*:
### **Message**
Functions should have return type hints
### **Fix Action**
Add return type: def func() -> ReturnType:
### **Applies To**
  - *.py

## Mutable default argument

### **Id**
mutable-default
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def\s+\w+\([^)]*=\s*\[\]
  - def\s+\w+\([^)]*=\s*\{\}
### **Message**
Mutable defaults are shared across calls
### **Fix Action**
Use None and create inside function: if arg is None: arg = []
### **Applies To**
  - *.py

## Bare except clause

### **Id**
bare-except
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - except\s*:
### **Message**
Bare except catches all exceptions including SystemExit
### **Fix Action**
Use specific exceptions: except ValueError: or except Exception:
### **Applies To**
  - *.py

## Print statement (use logging)

### **Id**
print-debug
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \bprint\s*\(
### **Message**
Use logging instead of print for production code
### **Fix Action**
Use logger.info() or logger.debug()
### **Applies To**
  - *.py

## FastAPI endpoint without response_model

### **Id**
missing-response-model
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @app\.(get|post|put|delete)\s*\([^)]*\)\s*\n\s*async def
### **Message**
Consider adding response_model for OpenAPI documentation
### **Fix Action**
Add response_model=YourSchema to the decorator
### **Applies To**
  - *.py

## Pydantic v1 syntax (deprecated)

### **Id**
pydantic-v1-syntax
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class Config:
  - @validator\s*\(
  - \.dict\s*\(
### **Message**
Consider updating to Pydantic v2 syntax
### **Fix Action**
Use model_config, @field_validator, .model_dump()
### **Applies To**
  - *.py