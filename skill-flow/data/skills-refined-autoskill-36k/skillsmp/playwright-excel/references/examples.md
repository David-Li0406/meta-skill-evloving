# Examples

## Invocation input
```
/playwright-excel tests/login.py data/users.xlsx

Mapping:
- "user123" -> Excel[Users][ID==U001][Username]
- "pass456" -> Excel[Users][ID==U001][Password]
```

## config.yaml example
```yaml
excel:
  path: "data/users.xlsx"
  sheet_name: "Users"
  columns:
    subject: "ID"
    username: "Username"
    password: "Password"

target:
  subject: "U001"
```

## Before/after snippet
```python
# Before
def run(playwright):
    page.fill("#username", "user123")
    page.fill("#password", "pass456")

# After
def run(playwright):
    data = load_data_from_excel()
    page.fill("#username", data["username"])
    page.fill("#password", data["password"])
```

## Run with override
```bash
PLAYWRIGHT_TARGET_SUBJECT=U002 conda run -n playwright python tests/login.py
```
