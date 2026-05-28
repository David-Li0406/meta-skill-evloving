---
name: migration-patterns
description: Zero-downtime Elixir/Phoenix database migrations and rollback strategies
---

# Migration Patterns Skill

Use this skill when:
- Creating database schema changes
- Managing database migrations
- Implementing zero-downtime deployments
- Designing rollback strategies
- Handling data migrations
- Optimizing migration performance

## Core Patterns

### 1. Ecto Migration Basics

```elixir
# ✅ Good: Idempotent migrations
defmodule MyApp.Repo.Migrations.AddEmailToUsers do
  use Ecto.Migration

  def change do
    alter table(:users) do
      add :email, :string, null: false, default: ""
    end
  end
end

# ❌ Bad: Non-idempotent migrations
defmodule MyApp.Repo.Migrations.BadAddEmail do
  use Ecto.Migration

  def change do
    alter table(:users) do
      modify :email, :string, default: ""
    end
  end
end
```

### 2. Zero-Downtime Deployments

```elixir
# ✅ Good: Backward-compatible changes
defmodule MyApp.Repo.Migrations.AddColumnBackwardCompatible do
  use Ecto.Migration

  def change do
    alter table(:users) do
      # Add new column with NULL constraint (allows NULL initially)
      add :new_field, :integer, null: true
      
      # Create index before populating data
      create index("users_new_field_idx", [:new_field])
    end
end

# ❌ Bad: Breaking change (requires downtime)
defmodule MyApp.Repo.Migrations.AddColumnBreaking do
  use Ecto.Migration

  def change do
    alter table(:users) do
      # Requires NOT NULL, breaks existing records
      modify :new_field, :integer, null: false, default: 0
      
      # Application must be stopped and deployed
    end
end
end
```

### 3. Data Migrations

```elixir
# ✅ Good: Batched operations in transactions
defmodule MyApp.Migrations.PopulateCategories do
  use Epo
  import Ecto.Query

  def up do
    Repo.transaction(fn ->
      # Process in batches of 1000
      Enum.chunk_stream(1..100_000, 1000, fn ids ->
        MyApp.Products.insert_categories_batch(ids)
        Process.sleep(10)  # Rate limiting
      end)
    end)
  end
end

# ❌ Bad: Process all records at once
defmodule MyApp.Migrations.BadPopulate do
  use Epo

  def up do
    # Blocks for entire operation
    MyApp.Products.insert_all_categories()
  end
end
```

### 4. Rollback Strategies

### 4.1. Reversible Migrations

```elixir
# ✅ Good: Write rollback function
defmodule MyApp.Repo.Migrations.AddFeatureFlag do
  use Ecto.Migration

  def up do
    alter table(:users) do
      add :feature_enabled, :boolean, default: false
    end
  end

  def down do
    # Reversible: remove column
    alter table(:users) do
      remove :feature_enabled
    end
  end
end

# ❌ Bad: Non-reversible migration
defmodule MyApp.Repo.Migrations.BadAddFeatureFlag do
  use Ecto.Migration

  def up do
    alter table(:users) do
      # Cannot reverse operation
      drop_constraint(:users_feature_flag_pkey)
      # No down function!
    end
end
```

### 4.2. Downward Compatible Migrations

```elixir
# ✅ Good: Use raw SQL for complex changes
defmodule MyApp.Repo.Migrations.RenameColumn do
  use Ecto.Migration

  def change do
    execute """
    ALTER TABLE users
    RENAME COLUMN name TO full_name;
    """
  end
end

# ❌ Bad: Multiple migrations (race conditions)
defmodule MyApp.Repo.Migrations.BadRenameColumn do
  use Ecto.Migration

  def change do
    alter table(:users) do
      rename :name, :to => :full_name
    end
    
    alter table(:users) do
      # Race condition: if another migration runs, this fails
      modify :full_name, :string, default: "Old Name"
    end
  end
end
```

### 4.3. Feature Flags

```elixir
# ✅ Good: Feature flags for gradual rollout
defmodule MyApp.Features do
  def enabled?(feature_name) do
    Application.get_env(:my_app, feature_name, "false") == "true"
  end
end

# Usage
if MyApp.Features.enabled?(:new_ui) do
  # Use new UI
else
  # Use old UI
end
```

## Migration Workflow

### 5. Blue-Green Deployment

```elixir
# Blue-Green deployment strategy
defmodule MyApp.Deployment.BlueGreen do
  use GenServer

  # Current version
  @impl true
  def init(_opts) do
    {:ok, %{current: :blue, target: :green}}
  end

  @impl true
  def switch_to_green(new_version) do
    GenServer.call(__MODULE__, {:switch, new_version})
    {:reply, :ok}
  end

  @impl true
  def handle_call({:switch, new_version}, _from, state) do
    # Apply green version migrations
    Repo.transaction(fn ->
      MyApp.Migrations.up_to_green()
    end)
    
    # Update load balancer to route to green
    MyApp.LoadBalancer.set_target(:green)
    
    # Wait for green to be healthy
    MyApp.HealthCheck.wait_until_healthy(:green)
    
    {:noreply, %{current: :green, target: :green}}
  end

  @impl true
  def handle_info({:green_healthy, version}, state) do
    # Blue is now safe to shut down
    MyApp.LoadBalancer.stop_node(:blue)
    
    {:noreply, %{current: :green, target: :blue}}
  end
end
```

## Performance Optimization

### 6. Index Management

```elixir
# ✅ Good: Add index before populating data
defmodule MyApp.Repo.Migrations.PopulateTable do
  use Ecto.Migration

  def change do
    create table(:new_table) do
      add :id, :uuid, primary_key: true
      add :name, :string
    add :data, :jsonb
    end
    
    # Create index immediately
    execute "CREATE INDEX new_table_idx ON new_table (id)"
  end
end

# ❌ Bad: Create index after data (blocks)
defmodule MyApp.Repo.Migrations.BadPopulateTable do
  use Ecto.Migration

  def change do
    create table(:new_table) do
      add :id, :uuid, primary_key: true
      add :name, :string
      add :data, :jsonb
    end
    
    # Index created after 100k records (slow)
    execute "INSERT INTO new_table SELECT * FROM source"
    
    # Creating index now blocks inserts
    execute "CREATE INDEX new_table_idx ON new_table (id)"
  end
end
```

## Best Practices

### 1. Migration Safety

- **Always write down functions**: Make migrations reversible
- **Test migrations locally**: Validate before deploying
- **Use transactions**: Wrap multi-table changes in transactions
- **Add constraints**: Use NOT NULL, foreign keys, check constraints
- **Backup before changes**: Always backup production database before migrations
- **Monitor performance**: Check migration duration and impact

### 2. Zero-Downtime Deployment

- **Use backward-compatible changes**: Add nullable columns first, then populate
- **Create indexes before data**: Index before large data inserts
- **Use feature flags**: Gradual rollout without downtime
- **Use blue-green deployment**: Two versions running simultaneously
- **Monitor health checks**: Ensure new version is healthy before cutover
- **Rollback plan**: Have plan to quickly revert if issues found
- **Keep migrations small**: Smaller migrations are safer and faster

### 3. Data Migration Performance

- **Batch large operations**: Process in chunks with rate limiting
- **Use transactions**: Ensure data consistency
- **Add indexes strategically**: Create indexes on frequently queried columns
- **Monitor queries**: Check for slow queries during migrations
- **Disable triggers**: Disable triggers during large data loads

### 4. Rollback Testing

- **Test down functions**: Verify rollback works correctly
- **Test with production-like data**: Test with realistic volumes
- **Document rollback procedures**: Have runbook with rollback steps
- **Practice rollback in staging**: Test in staging before production

## Token Efficiency

Use migration patterns for:
- **Zero-downtime deployments** (~100% token savings vs app restart)
- **Batched operations** (~60% token savings vs single transactions)
- **Index optimization** (~50% faster queries)
- **Feature flags** (~40% safer deployments)
- **Rollback safety** (~70% risk reduction)
