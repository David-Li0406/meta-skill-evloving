---
name: rails-migrations
description: This skill should be used when the user asks about "migrations", "database schema", "create_table", "add_column", "remove_column", "add_index", "foreign keys", "db:migrate", "db:rollback", "schema.rb", "change_column", "reversible", "references", "timestamps", or needs guidance on modifying database structure in Rails applications.
version: 1.0.0
---

# ActiveRecord Migrations

Comprehensive guide to creating and managing database migrations in Rails.

## Creating Migrations

### Generator Commands

```bash
# Standalone migration
rails generate migration AddPartNumberToProducts part_number:string

# Create table
rails generate migration CreateProducts name:string price:decimal

# Add reference/foreign key
rails generate migration AddUserRefToProducts user:references

# Add index
rails generate migration AddIndexToUsersEmail
```

### Naming Conventions

Migration names determine auto-generated code:

| Pattern | Generated Code |
|---------|----------------|
| `AddColumnToTable` | `add_column :table, :column, :type` |
| `RemoveColumnFromTable` | `remove_column :table, :column, :type` |
| `CreateTable` | `create_table` block |
| `AddIndexToTable` | `add_index :table, :column` |

File format: `YYYYMMDDHHMMSS_migration_name.rb`

## Column Types

| Type | Description |
|------|-------------|
| `:string` | Short text (VARCHAR, default 255) |
| `:text` | Long text (unlimited) |
| `:integer` | Standard integer |
| `:bigint` | Large integer (default for PKs in Rails 5.1+) |
| `:float` | Floating point |
| `:decimal` | Precise decimal (use for money) |
| `:boolean` | True/false |
| `:date` | Date only |
| `:time` | Time only |
| `:datetime` | Date and time |
| `:timestamp` | Same as datetime |
| `:binary` | Binary data |
| `:json` | JSON (native if supported) |
| `:jsonb` | Binary JSON (PostgreSQL) |
| `:uuid` | UUID type |
| `:references` | Foreign key column |

## Column Modifiers

```ruby
add_column :products, :name, :string,
  null: false,              # NOT NULL constraint
  default: "Untitled",      # Default value
  limit: 100,               # Max length (string) or bytes (integer)
  precision: 8,             # Total digits (decimal)
  scale: 2,                 # Digits after decimal
  index: true,              # Create index
  unique: true,             # Unique index
  comment: "Product name"   # Database comment
```

## Table Operations

### Create Table

```ruby
class CreateProducts < ActiveRecord::Migration[7.1]
  def change
    create_table :products do |t|
      t.string :name, null: false
      t.text :description
      t.decimal :price, precision: 10, scale: 2
      t.integer :quantity, default: 0
      t.boolean :active, default: true
      t.references :category, foreign_key: true
      t.references :user, null: false, foreign_key: true

      t.timestamps  # created_at and updated_at
    end

    add_index :products, :name
    add_index :products, [:category_id, :active]
  end
end
```

### Modify Table

```ruby
class AddFieldsToProducts < ActiveRecord::Migration[7.1]
  def change
    change_table :products do |t|
      t.string :sku
      t.remove :temporary_field
      t.rename :old_name, :new_name
      t.index :sku, unique: true
    end
  end
end
```

### Drop Table

```ruby
def change
  drop_table :products do |t|
    # Include schema for reversibility
    t.string :name
    t.timestamps
  end
end
```

## Column Operations

### Add Columns

```ruby
def change
  add_column :products, :weight, :decimal, precision: 8, scale: 2
  add_column :products, :dimensions, :json
  add_column :users, :role, :string, default: "member", null: false
end
```

### Remove Columns

```ruby
def change
  # Include type for reversibility
  remove_column :products, :discontinued, :boolean, default: false
end
```

### Rename Column

```ruby
def change
  rename_column :products, :upc, :sku
end
```

### Change Column

```ruby
# Not automatically reversible - use up/down
def up
  change_column :products, :price, :decimal, precision: 12, scale: 2
  change_column_null :products, :name, false
  change_column_default :products, :status, from: nil, to: "draft"
end

def down
  change_column :products, :price, :decimal, precision: 10, scale: 2
  change_column_null :products, :name, true
  change_column_default :products, :status, from: "draft", to: nil
end
```

## References and Foreign Keys

### Add Reference

```ruby
def change
  # Adds category_id column with index and foreign key
  add_reference :products, :category, foreign_key: true

  # Polymorphic reference
  add_reference :comments, :commentable, polymorphic: true, index: true

  # Without foreign key constraint
  add_reference :products, :supplier, foreign_key: false

  # Nullable reference
  add_reference :products, :brand, null: true, foreign_key: true
end
```

### Foreign Key Options

```ruby
def change
  add_foreign_key :articles, :authors

  # Custom column name
  add_foreign_key :articles, :users, column: :author_id

  # On delete behavior
  add_foreign_key :comments, :articles, on_delete: :cascade
  add_foreign_key :orders, :users, on_delete: :nullify

  # Remove foreign key
  remove_foreign_key :articles, :authors
  remove_foreign_key :articles, column: :author_id
end
```

## Indexes

```ruby
def change
  # Basic index
  add_index :users, :email

  # Unique index
  add_index :users, :email, unique: true

  # Composite index
  add_index :products, [:category_id, :status]

  # Partial index (PostgreSQL)
  add_index :orders, :shipped_at, where: "shipped_at IS NOT NULL"

  # Named index
  add_index :products, :sku, name: "idx_products_sku"

  # Remove index
  remove_index :users, :email
  remove_index :products, name: "idx_products_sku"
end
```

## The change Method

Auto-reversible operations (use `change`):

- `add_column` / `remove_column` (with type)
- `add_foreign_key` / `remove_foreign_key`
- `add_index` / `remove_index`
- `add_reference` / `remove_reference`
- `add_timestamps` / `remove_timestamps`
- `create_table` / `drop_table` (with block)
- `create_join_table` / `drop_join_table`
- `rename_column`
- `rename_index`
- `rename_table`
- `change_column_default` (with `:from` and `:to`)
- `change_column_null`

## Reversible and Up/Down

### Using reversible

```ruby
def change
  create_table :products do |t|
    t.string :name
    t.timestamps
  end

  reversible do |dir|
    dir.up do
      execute <<-SQL
        CREATE INDEX idx_products_search ON products
        USING gin(to_tsvector('english', name));
      SQL
    end
    dir.down do
      execute "DROP INDEX idx_products_search;"
    end
  end
end
```

### Using up/down

```ruby
def up
  change_column :products, :price, :decimal, precision: 12, scale: 2
end

def down
  change_column :products, :price, :decimal, precision: 10, scale: 2
end
```

### Irreversible Migration

```ruby
def up
  drop_table :legacy_products
end

def down
  raise ActiveRecord::IrreversibleMigration
end
```

## Running Migrations

```bash
# Run pending migrations
rails db:migrate

# Migrate to specific version
rails db:migrate VERSION=20240101120000

# Rollback last migration
rails db:rollback

# Rollback multiple migrations
rails db:rollback STEP=3

# Redo last migration (rollback + migrate)
rails db:migrate:redo

# Check migration status
rails db:migrate:status

# Run in specific environment
rails db:migrate RAILS_ENV=production
```

## Database Commands

```bash
# Create database
rails db:create

# Drop database
rails db:drop

# Reset (drop + create + migrate)
rails db:reset

# Setup (create + load schema + seed)
rails db:setup

# Prepare (idempotent setup)
rails db:prepare

# Load schema directly (faster than migrations)
rails db:schema:load

# Dump current schema
rails db:schema:dump

# Run seeds
rails db:seed
```

## Safe Migration Practices

### Do's

1. **Always include column type in remove_column** for reversibility
2. **Use `change_column_default` with `:from` and `:to`**
3. **Add indexes on foreign keys** (automatic with `references`)
4. **Test rollback**: `rails db:migrate:redo`
5. **Keep migrations small and focused**

### Don'ts

1. **Don't edit committed migrations** - create new ones
2. **Don't use model classes** directly in migrations (schema may change)
3. **Don't add data migrations** - use seeds or maintenance tasks

### Data Migration Alternative

```ruby
# Instead of data in migrations, use:
# lib/tasks/data_migration.rake

namespace :data do
  desc "Migrate user status values"
  task migrate_status: :environment do
    User.where(status: "old_value").update_all(status: "new_value")
  end
end
```

### Concurrent Index (PostgreSQL)

```ruby
class AddIndexToUsersEmail < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!

  def change
    add_index :users, :email, algorithm: :concurrently
  end
end
```

## Additional Resources

### Reference Files

- **`references/migration-patterns.md`** - Complex migration patterns, zero-downtime migrations
