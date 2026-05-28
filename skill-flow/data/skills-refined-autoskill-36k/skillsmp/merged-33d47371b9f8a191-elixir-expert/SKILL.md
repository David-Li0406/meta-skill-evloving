---
name: elixir-expert
description: Use this skill when you need expert guidance in Elixir and Phoenix development, including functional programming, OTP, and Ecto.
---

# Elixir Expert

You are an expert in Elixir and Phoenix development with deep knowledge of functional programming and concurrent systems. This skill provides guidance on best practices, patterns, and advanced topics in Elixir.

## Core Concepts

### Elixir Fundamentals
- Functional programming
- Pattern matching
- Immutability
- Pipe operator
- Modules and functions
- Structs and maps

### OTP (Open Telecom Platform)
- GenServer
- Supervisors
- Applications
- Tasks
- Agents
- ETS (Erlang Term Storage)

### Phoenix Framework
- Contexts and schemas
- LiveView
- Channels (WebSockets)
- Plug
- Ecto (database)
- Testing

## Best Practices

### Elixir
- Use pattern matching extensively
- Leverage the pipe operator for readability
- Write small, focused functions
- Handle all pattern match cases
- Use proper error handling
- Follow naming conventions

### OTP
- Use GenServers for state management
- Implement supervisors properly
- Design for failure
- Keep processes focused
- Use process monitoring

### Phoenix
- Follow context boundaries
- Use changesets for validation
- Implement proper authentication
- Handle errors gracefully
- Test thoroughly

## Technical Practices

### Elixir & Phoenix Usage
- Write concise, idiomatic Elixir code with accurate examples
- Follow Phoenix conventions and best practices
- Embrace functional programming patterns and immutability
- Prefer higher-order functions and recursion over imperative loops

### Error Handling
- Use Elixir's 'let it crash' philosophy and supervisor trees
- Implement proper error logging with user-friendly messages
- Use Ecto changesets for validation

## Advanced Topics

- Use Phoenix LiveView for dynamic, real-time interactions
- Implement responsive design with Tailwind CSS
- Implement GenServers for stateful processes
- Use ExUnit for comprehensive testing with TDD
- Apply Guardian/Pow for authentication and authorization

## Concurrency

### Tasks
- Use `Task.async` for parallel processing
- Use `Task.Supervisor` for managing background jobs
- Use `Agent` for simple state management
- Use ETS for efficient storage and retrieval

## Ecto Database Patterns

### Schemas and Changesets
- Define schemas using Ecto
- Use changesets for data validation and constraints

### Queries
- Use Ecto queries for database operations
- Optimize queries with indexing and preloading

## Example Code Snippets

### Pattern Matching
```elixir
def greet(%User{name: name, role: :admin}), do: "Hello Admin #{name}"
def greet(%User{name: name}), do: "Hello #{name}"
def greet(_), do: "Hello stranger"
```

### GenServer Example
```elixir
defmodule Counter do
  use GenServer

  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.cast(__MODULE__, :increment)
  end

  def get do
    GenServer.call(__MODULE__, :get)
  end

  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_cast(:increment, state) do
    {:noreply, state + 1}
  end

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

### Phoenix Controller Example
```elixir
defmodule MyAppWeb.UserController do
  use MyAppWeb, :controller

  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, :index, users: users)
  end

  def create(conn, %{"user" => user_params}) do
    case Accounts.create_user(user_params) do
      {:ok, user} ->
        conn
        |> put_flash(:info, "User created successfully")
        |> redirect(to: Routes.user_path(conn, :show, user))

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, :new, changeset: changeset)
    end
  end
end
```

## Resources
- Elixir: [elixir-lang.org](https://elixir-lang.org/)
- Phoenix: [phoenixframework.org](https://www.phoenixframework.org/)
- Ecto: [hexdocs.pm/ecto](https://hexdocs.pm/ecto/)
- Elixir School: [elixirschool.com](https://elixirschool.com/)
- Programming Elixir (book)

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.