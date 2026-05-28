---
name: api-versioning
description: API versioning strategies including URL-based, header-based, and breaking change management
---

# API Versioning Skill

Use this skill when:
- Designing API versioning strategies
- Managing breaking changes
- Creating deprecation workflows
- Implementing API gateways
- Designing backward-compatible APIs
- Planning multi-version support

## When to Use

### Use this skill when:
- Your API needs to evolve without breaking existing clients
- You're planning breaking changes to API contracts
- Designing multi-version support
- Implementing API deprecation strategies
- Creating API gateway patterns

### Key Scenarios

1. **Major API Changes**: Breaking changes to existing contracts
2. **Feature Additions**: New endpoints or parameters
3. **Field Modifications**: Changing field types or structures
4. **Deprecation**: Removing deprecated endpoints
5. **Gateway Integration**: Proxying multiple versions

---

## Versioning Strategies

### 1. URI Path Versioning

```elixir
# config/router.ex
defmodule MyAppWeb.Router do
  use MyAppWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :put_secure_browser_headers
    plug :put_root_layout, html: {MyAppWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_user_token
  end

  # v1 APIs
  scope "/api/v1", as: :api do
    pipe_through :api do
      get "/users", UserController, :index
      post "/users", UserController, :create
      get "/users/:id", UserController, :show
      put "/users/:id", UserController, :update
      delete "/users/:id", UserController, :delete
    end

  # v2 APIs (breaking changes)
  scope "/api/v2", as: :api do
    pipe_through :api do
      get "/users", UserV2Controller, :index
      post "/users", UserV2Controller, :create
      get "/users/:id", UserV2Controller, :show
      put "/users/:id", UserV2Controller, :update
      delete "/users/:id", UserV2Controller, :delete)
    end
  end
end
```

### 2. Header-Based Versioning

```elixir
# config/config.exs
config :my_app, MyAppWeb.Gateway,
  api_version: "v2"

defmodule MyAppWeb.Gateway do
  def call(conn, opts) do
    # Accept version from header
    case get_header(conn, "api-version", nil) do
      nil -> {:ok, conn}
      version when is_binary(version) ->
        Logger.info("API version from header: #{version}")
        {:ok, put_private(conn, :api_version, version)}
    end
    end
end

# In controller
defmodule UserV2Controller do
  alias MyAppWeb.Gateway

  def index(conn, params) do
    version = get_api_version(conn)

    case version do
      nil -> 
      # No version specified, use latest
      list_users_v2(conn, params)
      
      "v1" ->
        # Forward to v1 controller for backward compatibility
        UserV1Controller.index(conn, params)
      
      "v2" ->
        list_users_v2(conn, params)
      
      _ ->
        conn
        |> put_status(400)
        |> json(%{error: "Unsupported API version: #{version}"})
    end
  end

  defp get_api_version(conn) do
    Map.get(conn.private, :api_version, "v2")
  end
end
```

---

## Backward Compatibility

### 1. Deprecation Warnings

```elixir
defmodule MyApp.Deprecation do
  use GenServer
  require Logger

  # Client API
  def start_link(opts), do: GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  def deprecate(feature_name, deadline_date), do: GenServer.cast(__MODULE__, {:deprecate, feature_name, deadline_date})
  def is_deprecated?(feature_name), do: GenServer.call(__MODULE__, {:is_deprecated, feature_name})
  def get_deprecation_info(feature_name), do: GenServer.call(__MODULE__, :get_deprecation_info, feature_name})

  @impl true
  def init(opts), do
    Logger.info("Starting deprecation service")
    {:ok, %{
      deprecated_features: %{},
      opts: opts
    }}
  end

  @impl true
  def handle_cast({:deprecate, feature_name, deadline_date}, state) do
    new_deprecated = %{
      feature_name: %{
        deprecated_at: DateTime.utc_now(),
        deadline_date: deadline_date
      }
    }

    new_state = put_in(state, :deprecated_features, feature_name, new_deprecated)
    {:noreply, new_state}
  end

  @impl true
  def handle_call({:is_deprecated, feature_name}, _from, state) do
    case Map.get(state.deprecated_features, feature_name) do
      nil ->
        {:reply, false, state}

      %{deprecated_at: deadline_date} ->
        now = DateTime.utc_now()
        if DateTime.compare(now, deadline_date) == :gt do
          Logger.error("Feature #{feature_name} is deprecated and past deadline")
          {:reply, true, state}
        else
          {:reply, false, state}
        end

      _deprecated_info ->
        {:reply, true, state}
    end
  end

  def handle_call({:get_deprecation_info, feature_name}, _from, state) do
    case Map.get(state.deprecated_features, feature_name) do
      nil ->
        {:reply, nil, state}

      info -> {:reply, info, state}
    end
  end
end
```

### 2. Field Evolution

```elixir
# Schema evolution with Ash
defmodule MyApp.Accounts.User do
  use Ash.Resource

  attributes do
    uuid_primary_key :id
    attribute :email, :string, allow_nil?: false
    attribute :name, :string
    # Deprecated field - marked for removal
    attribute :old_field, :string, deprecated_reason: "Replaced by new_field", allow_nil?: true
    attribute :new_field, :string

    timestamps()
  end

  actions do
    read :read
    update :update
    create :create
    destroy :destroy
  end
end

# Migration for deprecation
defmodule MyApp.Repo.Migrations.DeprecateOldField do
  use Ecto.Migration

  def change do
    alter table(:users) do
      add :new_field, :string
    end

    # Add deprecation warning to queries
    create index(:users, [:email, :new_field])
  end

  def down do
    drop index(:users, [:email, :new_field])
    alter table(:users) do
      remove :new_field
    end
  end
end
```

### 3. Adapters for Backward Compatibility

```elixir
defmodule MyApp.Api.V1ToV2Adapter do
  require Logger

  def adapt_request(conn, params) do
    Logger.info("Adapting v1 request to v2 structure")

    # Map v1 params to v2 structure
    v2_params = %{
      "user_id" => params["id"],
      "email" => params["email"],
      "password" => params["password"],
      # New required fields
      "full_name" => params["full_name"] || params["name"],
      "phone" => params["phone"]
    }

    Logger.debug("Mapped v1 params to v2: #{inspect(v2_params)}")

    {:ok, v2_params}
  end

  def adapt_response(v2_response) do
    Logger.info("Adapting v2 response to v1 structure")

    # Map v2 response to v1 structure
    v1_response = %{
      "id" => v2_response.id,
      "email" => v2_response.email,
      "name" => v2_response.full_name || v2_response.name,
      "phone" => v2_response.phone
      "created_at" => v2_response.inserted_at
    }

    Logger.debug("Mapped v2 response to v1: #{inspect(v1_response)}")

    {:ok, v1_response}
  end
end
```

---

## Breaking Change Management

### 1. Semanic Versioning

```elixir
defmodule MyApp.Versioning do
  @major "1.0"
  @minor "0"
  @patch "0"
  @pre_release "dev"

  def current_version do
    @major <> "." <> @minor <> "." <> @patch
  end

  def next_major_version, do
    next_major = String.to_integer(@major) + 1)
    %{current_version | major: Integer.to_string(next_major), minor: @minor, patch: @patch}
  end

  def next_minor_version, do
    next_minor = String.to_integer(@minor) + 1)
    %{current_version | major: @major, minor: Integer.to_string(next_minor), patch: @patch}
  end

  def next_patch_version, do
    next_patch = String.to_integer(@patch) + 1)
    %{current_version | major: @major, minor: @minor, patch: Integer.to_string(next_patch)}
  end

  def bump_version(version_type) do
    case version_type do
      :major -> next_major_version()
      :minor -> next_minor_version()
      :patch -> next_patch_version()
      :pre -> current_version()
    end
  end

  def is_backward_compatible?(v1, v2) do
    # Parse versions
    v1_parts = String.split(v1, ".")
    v2_parts = String.split(v2, ".")

    {v1_major, v1_minor, _v1_patch} = v1_parts
    {v2_major, v2_minor, _v2_patch} = v2_parts

    # v1 < v2: backward compatible
    cond do
      String.to_integer(v1_major) < String.to_integer(v2_major) -> true
      String.to_integer(v1_major) == String.to_integer(v2_major) ->
        String.to_integer(v1_minor) < String.to_integer(v2_minor) -> true
        true -> false
    end
  end
  end
end
```

### 2. Breaking Change Policy

```elixir
defmodule MyApp.Api.BreakingChangePolicy do
  require Logger

  # Breaking change levels
  @levels [:minor, :major, :breaking]
  @policy %{
    :minor => %{
      deprecation_period: 90,  # 90 days
      warnings: true,
      client_notification: true,
      grace_period: 7   # 7 days
    },
    :major => %{
      deprecation_period: 180,  # 180 days
      warnings: true,
      client_notification: true,
      grace_period: 30  # 30 days
      grace_period: 7  # 7 days
    },
    :breaking => %{
      deprecation_period: 0,
      warnings: true,
      client_notification: true,
      grace_period: 0
      client_notification: true,
      requires_major_version_bump: true
    }
  }

  # Client API
  def check_compatibility(version, feature), do
    # Get feature version from config
    feature_versions = Application.get_env(:my_app, :feature_versions, %{})

    case Map.get(feature_versions, feature) do
      nil -> {:ok, :compatible}
      feature_version -> is_backward_compatible?(version, feature_version)
    end
  end

  def get_deprecation_deadline(feature, change_level) do
    policy = Map.get(@policy, change_level, @policy[:minor])
    days = policy[:deprecation_period]
    Date.add(Date.utc_today(), days)
  end

  # Notify clients
  def notify_deprecation(feature, deadline, policy, change_level) do
    if policy[:client_notification] do
      Logger.warning("Deprecating #{feature}, deadline: #{deadline}")
      # Send notification to clients
      MyApp.Notifier.notify_clients(:feature_deprecation, %{
        feature: feature,
        deadline: deadline,
        change_level: change_level
      })
    end
  end
end
```

---

## API Gateway Patterns

### 1. Version-Based Routing

```elixir
defmodule MyApp.Gateway.Router do
  use Plug.Router

  @api_versions ["v1", "v2", "v3"]

  plug Plug.Static, at: "/", from: :v1
  plug Plug.Static, at: "/v1", from: :v2
  plug Plug.Static, at: "/v2", from: :v3

  # Default version (latest)
  @api_version "v3"

  # Health check endpoint
  get "/health", HealthCheckController, :check

  # API version endpoints (with latest alias)
  scope "/", as: :api do
    pipe_through :api do
      # Latest version routes (aliased to /v3)
      get "/users", UserV3Controller, :index
      post "/users", UserV3Controller, :create
    end
  end

  # Versioned endpoints
  Enum.each(@api_versions, fn version ->
    scope "/#{version}", as: :api do
      pipe_through :api do
        get "/users", :"UserController#{version}", :index
        post "/users", :"UserController#{version}", :create
      end
    end)
  end
end
```

### 2. Version Compatibility Headers

```elixir
defmodule MyApp.VersionHeaders do
  @supported_versions ["v1", "v1.1", "v2", "v2.1", "v3"]

  def validate_version(conn) do
    case get_header(conn, "api-version", nil) do
      nil ->
        {:ok, nil}
      version ->
        if version in @supported_versions do
          {:ok, version}
        else
          {:error, :unsupported_version}
        end
    end
  end

  def add_version_headers(conn) do
    supported_versions = Enum.join(@supported_versions, ", ")
    conn
    |> put_resp_header("api-version", @api_version)
    |> put_resp_header("api-supported-versions", supported_versions)
    |> put_resp_header("api-latest-version", @api_version)
  end
end
```

---

## Best Practices

### DO

✅ Choose versioning strategy upfront
✅ Document version semantics clearly
✅ Provide deprecation warnings
✅ Implement graceful degradation
✅ Use semantic versioning
✅ Test backward compatibility
✅ Document breaking changes in CHANGELOG
✅ Notify clients of deprecations
✅ Support multiple versions when needed
✅ Consider API gateways for evolution

### DON'T

❌ Change API versioning strategy mid-project
❌ Forget to document breaking changes
❌ Remove v1 immediately without deprecation
❌ Skip deprecation warnings
❌ Make breaking changes without grace period
❌ Ignore backward compatibility
❌ Forget to version databases
❌ Use ambiguous version numbers
❌ Skip client notification
❌ Make breaking changes without documentation

---

## Integration with ai-rules

### Roles to Reference

- **Architect**: Use for API design and versioning strategy selection
- **Orchestrator**: Implement versioning in features
- **Backend Specialist**: Design version-aware APIs
- **Reviewer**: Verify version compatibility and deprecation policies
- **QA**: Test backward compatibility

### Skills to Reference

- **api-design**: Use versioning in API design
- **test-generation**: Write tests for version compatibility
- **observability**: Monitor deprecated API usage
- **distributed-systems**: Combine with distributed API patterns

---

## Summary

API versioning provides:
- ✅ URI path versioning
- ✅ Header-based versioning
- ✅ Breaking change management
- ✅ Deprecation workflows
- ✅ Backward compatibility patterns
- ✅ Multi-version support

**Key**: Choose strategy upfront, document changes, deprecate gracefully, and maintain backward compatibility.
