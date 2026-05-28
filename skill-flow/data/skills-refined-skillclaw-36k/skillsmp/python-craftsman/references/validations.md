# Python Craftsman - Validations

## Any Type Usage

### **Id**
any-type-usage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - : Any[^a-zA-Z]
  - -> Any[^a-zA-Z]
  - Any\]
### **Message**
Using Any type defeats type safety. Consider specific types or TypeVar.
### **Fix Action**
Replace with concrete type, Union, or TypeVar for generics
### **Applies To**
  - **/*.py

## Bare Exception Handler

### **Id**
bare-except
### **Severity**
error
### **Type**
regex
### **Pattern**
  - except:
  - except Exception:
### **Message**
Bare except catches too much (KeyboardInterrupt, SystemExit). Be specific.
### **Fix Action**
Catch specific exceptions: except ValueError, TypeError:
### **Applies To**
  - **/*.py

## Blocking Call in Async

### **Id**
blocking-in-async
### **Severity**
error
### **Type**
regex
### **Pattern**
  - async def.*\n.*requests\.
  - async def.*\n.*time\.sleep
  - async def.*\n.*open\(
### **Message**
Blocking call in async function will freeze event loop.
### **Fix Action**
Use httpx instead of requests, asyncio.sleep instead of time.sleep
### **Applies To**
  - **/*.py

## Mutable Default Argument

### **Id**
mutable-default-arg
### **Severity**
error
### **Type**
regex
### **Pattern**
  - def.*=\s*\[\]
  - def.*=\s*\{\}
  - def.*=\s*set\(\)
### **Message**
Mutable default argument is shared between calls. Use None and create inside.
### **Fix Action**
Use = None, then create in function body with: if arg is None: arg = []
### **Applies To**
  - **/*.py

## Pydantic V1 Config Style

### **Id**
pydantic-v1-config
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class Config:
  - orm_mode\s*=
  - @validator\(
### **Message**
Pydantic V1 style detected. V2 uses model_config, from_attributes, @field_validator.
### **Fix Action**
Migrate to Pydantic V2: ConfigDict, from_attributes=True, @field_validator
### **Applies To**
  - **/*.py

## Excessive Type Ignore

### **Id**
type-ignore-abuse
### **Severity**
info
### **Type**
regex
### **Pattern**
  - type:\s*ignore(?!\[)
### **Message**
Blanket type: ignore hides real issues. Use specific ignore codes.
### **Fix Action**
Use specific codes: type: ignore[arg-type] or fix the underlying issue
### **Applies To**
  - **/*.py

## Unpinned Dependency

### **Id**
unpinned-dependency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^[a-zA-Z][a-zA-Z0-9_-]*$
  - ^[a-zA-Z][a-zA-Z0-9_-]*\s*$
### **Message**
Unpinned dependency will cause inconsistent builds.
### **Fix Action**
Pin with version range: package>=1.0.0,<2.0.0
### **Applies To**
  - **/requirements*.txt

## Missing Return Type Annotation

### **Id**
missing-return-type
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def [a-z_]+\([^)]*\):
  - async def [a-z_]+\([^)]*\):
### **Message**
Function missing return type annotation. Add -> Type.
### **Fix Action**
Add return type: def func() -> ReturnType:
### **Applies To**
  - **/*.py

## Print Statement in Production

### **Id**
print-statement
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - print\(
### **Message**
Print statements in production code. Use logging instead.
### **Fix Action**
Replace with logger.info(), logger.debug(), or logger.error()
### **Applies To**
  - **/src/**/*.py
  - !**/tests/**

## Star Import

### **Id**
star-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - from .* import \*
### **Message**
Star imports pollute namespace and hide dependencies.
### **Fix Action**
Import specific names: from module import Class, function
### **Applies To**
  - **/*.py

## Dataclass Without Slots

### **Id**
no-slots
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @dataclass[^(]
  - @dataclass\(\)$
  - @dataclass\([^s]*\)$
### **Message**
Dataclass without slots uses more memory. Consider slots=True.
### **Fix Action**
Add slots=True: @dataclass(slots=True)
### **Applies To**
  - **/*.py

## Relative Import Issues

### **Id**
relative-import-outside-package
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^from \.\.\. import
### **Message**
Deep relative imports are confusing. Use absolute imports or restructure.
### **Fix Action**
Use absolute imports or restructure package to reduce nesting
### **Applies To**
  - **/*.py