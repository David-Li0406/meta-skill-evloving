# Advanced Migration Patterns

## Zero-Downtime Migrations

### Adding a Column with Default

```ruby
# Rails 5+ handles this efficiently
# But for high-traffic tables, consider:

class AddStatusToOrders < ActiveRecord::Migration[7.1]
  def change
    # Step 1: Add column without default
    add_column :orders, :status, :string

    # Step 2: Backfill in batches (do this in a rake task)
    # Order.in_batches.update_all(status: 'pending')

    # Step 3: Add default and NOT NULL in separate migration
    # change_column_default :orders, :status, 'pending'
    # change_column_null :orders, :status, false
  end
end
```

### Renaming a Column Safely

```ruby
# Multi-step process for zero downtime:

# Step 1: Add new column
class AddNewNameToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :full_name, :string
  end
end

# Step 2: Backfill data (rake task)
# User.in_batches.update_all('full_name = name')

# Step 3: Update application to write to both columns

# Step 4: Update application to read from new column

# Step 5: Remove old column
class RemoveNameFromUsers < ActiveRecord::Migration[7.1]
  def change
    remove_column :users, :name, :string
  end
end
```

### Adding an Index Concurrently (PostgreSQL)

```ruby
class AddIndexToUsersEmail < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!

  def change
    add_index :users, :email, algorithm: :concurrently, if_not_exists: true
  end
end
```

## Complex Table Changes

### Creating a Join Table

```ruby
class CreateArticlesTags < ActiveRecord::Migration[7.1]
  def change
    create_join_table :articles, :tags do |t|
      t.index :article_id
      t.index :tag_id
      t.index [:article_id, :tag_id], unique: true
    end
  end
end
```

### Splitting a Table

```ruby
# Step 1: Create new table
class CreateProfiles < ActiveRecord::Migration[7.1]
  def change
    create_table :profiles do |t|
      t.references :user, null: false, foreign_key: true, index: { unique: true }
      t.string :bio
      t.string :avatar_url
      t.string :website
      t.timestamps
    end
  end
end

# Step 2: Migrate data (rake task)
# User.find_each do |user|
#   Profile.create!(
#     user_id: user.id,
#     bio: user.bio,
#     avatar_url: user.avatar_url,
#     website: user.website
#   )
# end

# Step 3: Remove columns from users
class RemoveProfileFieldsFromUsers < ActiveRecord::Migration[7.1]
  def change
    remove_column :users, :bio, :text
    remove_column :users, :avatar_url, :string
    remove_column :users, :website, :string
  end
end
```

## Conditional Migrations

### Check Before Adding

```ruby
class AddSlugToArticles < ActiveRecord::Migration[7.1]
  def change
    unless column_exists?(:articles, :slug)
      add_column :articles, :slug, :string
      add_index :articles, :slug, unique: true
    end
  end
end
```

### Database-Specific Code

```ruby
class AddFullTextSearch < ActiveRecord::Migration[7.1]
  def change
    if ActiveRecord::Base.connection.adapter_name == 'PostgreSQL'
      execute <<-SQL
        CREATE INDEX articles_search_idx ON articles
        USING gin(to_tsvector('english', title || ' ' || body));
      SQL
    end
  end
end
```

## Enum Columns (PostgreSQL)

```ruby
class AddStatusEnumToOrders < ActiveRecord::Migration[7.1]
  def up
    execute <<-SQL
      CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered');
    SQL

    add_column :orders, :status, :order_status, default: 'pending'
  end

  def down
    remove_column :orders, :status

    execute <<-SQL
      DROP TYPE order_status;
    SQL
  end
end
```

## UUID Primary Keys

```ruby
class EnableUuid < ActiveRecord::Migration[7.1]
  def change
    enable_extension 'pgcrypto'
  end
end

class CreateProducts < ActiveRecord::Migration[7.1]
  def change
    create_table :products, id: :uuid do |t|
      t.string :name
      t.references :category, type: :uuid, foreign_key: true
      t.timestamps
    end
  end
end
```

## Partitioned Tables (PostgreSQL)

```ruby
class CreatePartitionedEvents < ActiveRecord::Migration[7.1]
  def up
    execute <<-SQL
      CREATE TABLE events (
        id bigserial,
        name varchar(255),
        created_at timestamp NOT NULL,
        PRIMARY KEY (id, created_at)
      ) PARTITION BY RANGE (created_at);

      CREATE TABLE events_2024_01 PARTITION OF events
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
    SQL
  end

  def down
    drop_table :events_2024_01
    drop_table :events
  end
end
```

## Check Constraints

```ruby
class AddCheckConstraintToProducts < ActiveRecord::Migration[7.1]
  def change
    add_check_constraint :products, "price > 0", name: "price_must_be_positive"
    add_check_constraint :orders, "quantity >= 1", name: "quantity_minimum"
  end
end
```

## Multi-Tenant Considerations

### Schema-Per-Tenant (PostgreSQL)

```ruby
class CreateTenantSchema < ActiveRecord::Migration[7.1]
  def change
    reversible do |dir|
      dir.up do
        execute "CREATE SCHEMA IF NOT EXISTS tenant_#{tenant_id}"
      end
      dir.down do
        execute "DROP SCHEMA IF EXISTS tenant_#{tenant_id} CASCADE"
      end
    end
  end
end
```

## Migration Testing

```ruby
# test/migrations/add_status_to_orders_test.rb
require "test_helper"

class AddStatusToOrdersTest < ActiveSupport::TestCase
  def setup
    @migration = AddStatusToOrders.new
  end

  test "adds status column" do
    @migration.migrate(:up)
    assert Order.column_names.include?("status")
  end

  test "removes status column on rollback" do
    @migration.migrate(:up)
    @migration.migrate(:down)
    Order.reset_column_information
    refute Order.column_names.include?("status")
  end
end
```

## Bulk Operations

### Efficient Backfills

```ruby
# Bad - loads all records
User.all.each { |u| u.update(processed: true) }

# Good - batch update
User.in_batches(of: 1000).update_all(processed: true)

# Good - with progress
User.in_batches(of: 1000).each_with_index do |batch, index|
  batch.update_all(processed: true)
  puts "Processed batch #{index + 1}"
end
```

### Disable Callbacks During Migration

```ruby
# In rake task, not migration
User.in_batches do |batch|
  batch.update_all(updated_at: Time.current)
end
# This bypasses model callbacks and validations
```
