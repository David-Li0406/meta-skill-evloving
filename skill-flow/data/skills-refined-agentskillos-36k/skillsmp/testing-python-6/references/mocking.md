# Mocking Patterns Reference

## pytest-mock Basics

```python
def test_with_mocker(mocker):
    # Patch a function
    mock = mocker.patch("module.function")
    mock.return_value = "mocked"

    result = code_under_test()

    assert result == "mocked"
    mock.assert_called_once()
```

## Where to Patch

**Patch where it's used, not where it's defined:**

```python
# myapp/service.py
from myapp.email import send_email  # Imported here

def notify_user(email):
    return send_email(email, "Hello")

# tests/test_service.py
def test_notify(mocker):
    # Patch in service module, not email module
    mock = mocker.patch("myapp.service.send_email")  # ✓ Correct
    # mock = mocker.patch("myapp.email.send_email")  # ✗ Wrong

    notify_user("test@example.com")

    mock.assert_called_once()
```

## Return Values

```python
# Single return value
mock.return_value = "result"

# Different returns per call
mock.side_effect = ["first", "second", "third"]

# Conditional returns
def smart_return(*args, **kwargs):
    if args[0] == 1:
        return "one"
    return "other"

mock.side_effect = smart_return

# Raise exception
mock.side_effect = ValueError("error message")

# Raise then succeed
mock.side_effect = [ConnectionError(), "success"]
```

## Assertions

```python
# Called at all
mock.assert_called()

# Called once
mock.assert_called_once()

# Called with specific args
mock.assert_called_with("arg1", key="value")
mock.assert_called_once_with("arg1", key="value")

# Any call had these args
mock.assert_any_call("arg1")

# Call count
assert mock.call_count == 3

# Not called
mock.assert_not_called()

# Call args
assert mock.call_args == call("arg1", key="value")
assert mock.call_args_list == [call("a"), call("b")]
```

## Async Mocking

```python
from unittest.mock import AsyncMock

async def test_async(mocker):
    # Mock async function
    mock = mocker.patch("module.async_func", new_callable=AsyncMock)
    mock.return_value = {"data": "mocked"}

    result = await code_under_test()

    mock.assert_awaited_once()
    assert result["data"] == "mocked"


# Async side effects
mock.side_effect = [
    AsyncMock(return_value="first")(),
    AsyncMock(return_value="second")(),
]

# Or simpler
mock.side_effect = ["first", "second"]  # Works with AsyncMock
```

## Class Mocking

```python
def test_mock_class(mocker):
    # Mock entire class
    MockClass = mocker.patch("module.MyClass")

    # Instance returned by constructor
    mock_instance = MockClass.return_value
    mock_instance.method.return_value = "mocked"

    obj = MyClass()  # Returns mock_instance
    result = obj.method()

    assert result == "mocked"


def test_mock_method(mocker):
    # Mock single method
    mocker.patch.object(MyClass, "method", return_value="mocked")

    obj = MyClass()  # Real instance
    result = obj.method()  # Mocked method

    assert result == "mocked"
```

## Property Mocking

```python
def test_mock_property(mocker):
    mocker.patch.object(
        MyClass,
        "my_property",
        new_callable=mocker.PropertyMock,
        return_value="mocked"
    )

    obj = MyClass()
    assert obj.my_property == "mocked"
```

## Context Manager Mocking

```python
def test_mock_context_manager(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="content"))

    with open("file.txt") as f:
        data = f.read()

    assert data == "content"
    mock_open.assert_called_once_with("file.txt")


def test_mock_custom_cm(mocker):
    mock_cm = mocker.MagicMock()
    mock_cm.__enter__.return_value = "resource"
    mock_cm.__exit__.return_value = False

    mocker.patch("module.get_resource", return_value=mock_cm)

    with get_resource() as r:
        assert r == "resource"
```

## Spy (Partial Mock)

```python
def test_spy(mocker):
    # Call real function but track calls
    spy = mocker.spy(module, "function")

    result = module.function("arg")  # Real call

    spy.assert_called_once_with("arg")
    assert result == "real result"
```

## Multiple Patches

```python
def test_multiple_patches(mocker):
    mock1 = mocker.patch("module.func1", return_value="one")
    mock2 = mocker.patch("module.func2", return_value="two")
    mock3 = mocker.patch("module.func3", return_value="three")

    result = code_under_test()

    mock1.assert_called()
    mock2.assert_called()
    mock3.assert_called()
```

## Environment Variables

```python
def test_env_var(mocker):
    mocker.patch.dict("os.environ", {"API_KEY": "test-key"})

    result = get_api_key()

    assert result == "test-key"


def test_env_clear(mocker):
    mocker.patch.dict("os.environ", {"API_KEY": "test"}, clear=True)
    # All other env vars removed
```

## Time Mocking

```python
from freezegun import freeze_time

@freeze_time("2024-01-15 12:00:00")
def test_with_frozen_time():
    from datetime import datetime
    assert datetime.now().year == 2024


# Or with mocker
def test_mock_datetime(mocker):
    mock_now = mocker.patch("module.datetime")
    mock_now.now.return_value = datetime(2024, 1, 15, 12, 0, 0)

    result = get_current_date()

    assert result.year == 2024
```

## Common Patterns

### Mock External API

```python
async def test_api_call(mocker):
    mock_response = mocker.AsyncMock()
    mock_response.json.return_value = {"id": 1, "name": "Test"}
    mock_response.status_code = 200

    mock_client = mocker.patch("module.httpx.AsyncClient")
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

    result = await fetch_user(1)

    assert result["name"] == "Test"
```

### Mock Database

```python
@pytest.fixture
def mock_db(mocker):
    mock = mocker.MagicMock()
    mock.query.return_value = [{"id": 1}]
    mock.execute.return_value = None
    return mock


def test_with_mock_db(mock_db):
    service = UserService(db=mock_db)
    users = service.list_users()

    assert len(users) == 1
    mock_db.query.assert_called_once()
```

### Mock File System

```python
def test_read_config(mocker, tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"key": "value"}')

    mocker.patch("module.CONFIG_PATH", config_file)

    config = load_config()

    assert config["key"] == "value"
```
