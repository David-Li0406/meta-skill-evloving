# Migration Patterns Reference

## Create Table

```ruby
class CreateTasks < ActiveRecord::Migration[7.1]
  def change
    create_table :tasks do |t|
      t.references :account, null: false, foreign_key: true
      t.references :merchant, null: false, foreign_key: true
      t.references :carrier, foreign_key: true  # nullable

      t.string :tracking_number, null: false
      t.string :status, null: false, default: 'pending'
      t.decimal :amount, precision: 10, scale: 2
      t.jsonb :metadata, default: {}

      t.datetime :completed_at
      t.timestamps

      t.index :tracking_number, unique: true
      t.index :status
      t.index [:account_id, :status]
      t.index [:merchant_id, :created_at]
      t.index :metadata, using: :gin  # For JSONB queries
    end
  end
end
```

---

## Safe Migrations

```ruby
# Add column with default (safe in PostgreSQL 11+)
class AddPriorityToTasks < ActiveRecord::Migration[7.1]
  def change
    add_column :tasks, :priority, :integer, default: 0, null: false
  end
end

# Add index concurrently (for large tables)
class AddIndexToTasksStatus < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!

  def change
    add_index :tasks, :status, algorithm: :concurrently
  end
end

# Remove column safely (with strong_migrations gem)
class RemoveOldColumnFromTasks < ActiveRecord::Migration[7.1]
  def change
    safety_assured { remove_column :tasks, :old_column, :string }
  end
end
```

---

## JSONB Columns

```ruby
# Migration
add_column :tasks, :metadata, :jsonb, default: {}
add_index :tasks, :metadata, using: :gin

# Model
class Task < ApplicationRecord
  # Using jsonb_accessor gem
  jsonb_accessor :metadata,
    priority: :integer,
    tags: [:string, array: true],
    notes: :string
end

# Queries
Task.where("metadata @> ?", { priority: 1 }.to_json)
Task.where("metadata->>'priority' = ?", '1')
Task.where("metadata ? 'special_flag'")
```

---

## Common Column Types

| Type | PostgreSQL | Use Case |
|------|------------|----------|
| `string` | varchar(255) | Short text |
| `text` | text | Long text |
| `integer` | integer | Numbers |
| `bigint` | bigint | Large numbers, IDs |
| `decimal` | decimal | Money (precision: 10, scale: 2) |
| `boolean` | boolean | True/false |
| `datetime` | timestamp | Date + time |
| `date` | date | Date only |
| `jsonb` | jsonb | JSON data |
| `uuid` | uuid | UUIDs |
| `references` | bigint + FK | Foreign keys |

---

## Generated Columns (PostgreSQL)

```ruby
class AddFullNameToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :full_name, :virtual,
      type: :string,
      as: "first_name || ' ' || last_name",
      stored: true  # Or false for computed on-the-fly

    add_index :users, :full_name
  end
end
```
