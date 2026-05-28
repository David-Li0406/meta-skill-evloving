---
name: test-generation
description: Generates comprehensive Elixir tests using ExUnit following TDD principles.
---

# Test Generation Skill

Use this skill to generate Elixir tests using ExUnit with TDD workflow.

## When to Use

- Writing tests for new features
- Creating test coverage for existing code
- Implementing test strategies for complex logic
- Writing property-based tests for edge cases

## TDD Workflow

### Red - Write Failing Test

Write a test that describes the desired behavior, then implement the feature to make it pass.

```elixir
# 1. Red - Write failing test
defmodule Accounts.User.CreateTest do
  use Accounts.DataCase

  test "creates user with valid attributes" do
    attrs = %{email: "test@example.com", password: "password123"}
    assert {:ok, %User{} = user} = Accounts.User.Create.call(attrs)
    assert user.email == "test@example.com"
  end
end
```

### Green - Make Test Pass

Implement the minimal code needed to make the test pass.

```elixir
# 2. Green - Make test pass
defmodule Accounts.User.Create do
  alias Accounts.{User, Repo}

  @spec call(map()) :: {:ok, User.t()} | {:error, Ecto.Changeset.t()}
  def call(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end
end
```

### Refactor - Improve Code

Refactor the code with confidence, knowing tests will catch any regressions.

```elixir
# 3. Refactor - Improve with confidence
defmodule Accounts.User.Create do
  alias Accounts.{User, Repo}

  @spec call(map()) :: {:ok, User.t()} | {:error, Ecto.Changeset.t()}
  def call(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> put_password_hash()
    |> Repo.insert()
  end

  defp put_password_hash(changeset) do
    case get_change(changeset, :password) do
      {nil, _} -> changeset
      {password, changeset} ->
        hash = Bcrypt.hash_pwd(password)
        put_change(changeset, :password_hash, hash)
    end
  end
end
```

## Test Patterns

### Unit Test Pattern

```elixir
defmodule Accounts.User.CreateTest do
  use Accounts.DataCase

  describe "call/1" do
    test "creates user with valid attributes" do
      attrs = %{email: "test@example.com", password: "password123"}
      assert {:ok, %User{} = user} = Accounts.User.Create.call(attrs)
      assert user.email == "test@example.com"
    end

    test "returns error with duplicate email" do
      # Setup: Create existing user
      attrs = %{email: "test@example.com", password: "password456"}
      {:ok, _existing} = Accounts.User.Create.call(attrs)

      # Action: Try to create duplicate
      assert {:error, %Ecto.Changeset{} = changeset} =
               Accounts.User.Create.call(attrs)

      # Assertion: Check error message
      assert %{email: ["has already been taken"]} = errors_on(changeset)
    end

    test "returns error with invalid email format" do
      attrs = %{email: "invalid", password: "password123"}
      assert {:error, %Ecto.Changeset{} = changeset} =
               Accounts.User.Create.call(attrs)
      assert %{email: ["has invalid format"]} = errors_on(changeset)
    end
  end
end
```

### GenServer Test Pattern

```elixir
defmodule Cache.WorkerTest do
  use ExUnit.Case, async: false
  alias Cache.Worker

  setup do
    {:ok, pid} = start_supervised!(Cache.Worker)
    %{pid: pid}
  end

  describe "get/1" do
    test "returns stored value", %{pid: pid} do
      Cache.Worker.put(:test_key, "test_value")
      assert Cache.Worker.get(:test_key) == "test_value"
    end

    test "returns nil for missing key", %{pid: pid} do
      assert is_nil(Cache.Worker.get(:missing_key))
    end
  end

  describe "put/2" do
    test "stores value successfully", %{pid: pid} do
      assert :ok = Cache.Worker.put(:new_key, "new_value")
      assert Cache.Worker.get(:new_key) == "new_value"
    end
  end
end
```

### Property-Based Testing Pattern

```elixir
defmodule StringProcessorTest do
  use ExUnit.Case
  use PropCheck

  describe "reverse/1" do
    property "reversing twice returns original" do
      forall {str} <- term() do
        str
        |> StringProcessor.reverse()
        |> StringProcessor.reverse()
        == str
      end
    end
  end
end
```

## Test Organization

### Directory Structure

```
test/
└── my_app/
    └── accounts/
        └── user/
            ├── create_test.exs
            ├── update_test.exs
            └── delete_test.exs
```

### Test Naming Convention

```
<feature>_<resource>_<action>_test.exs
```

**Example**: `user_registration_test.exs`, `post_publish_test.exs`

## Test Coverage Goals

Aim for:
- **Business Logic**: 80%+ coverage
- **Domain Modules**: 85%+ coverage
- **Integration Points**: 90%+ coverage
- **Critical Paths**: 100% coverage

## Commands to Run

```bash
# Run all tests
mix test

# Run tests with coverage
mix test --cover

# View coverage report
open cover/excoveralls.html

# Run specific test file
mix test test/accounts/user/create_test.exs

# Run tests with trace output
mix test --trace
```

## Best Practices

### Do

- Write failing test first (TDD Red)
- Implement minimal code to make test pass (TDD Green)
- Refactor with confidence (TDD Refactor)
- Test happy paths and error cases
- Test edge cases and boundaries
- Use descriptive test names
- Organize tests by feature/resource

### Don't

- Skip TDD (write tests after implementation)
- Implement before writing tests
- Write tests that only test implementation details
- Use vague or non-descriptive test names
- Skip testing error cases
- Ignore test failures
- Write tests that are fragile or hard to maintain

---

**Use this skill to follow TDD and write comprehensive tests.**
