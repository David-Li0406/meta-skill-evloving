# PostgreSQL-Specific Features Reference

## Full-Text Search with pg_search

```ruby
# Gemfile
gem 'pg_search'

# Model
class Article < ApplicationRecord
  include PgSearch::Model

  pg_search_scope :search_full_text,
    against: {
      title: 'A',        # Higher weight
      body: 'B',
      author: 'C'
    },
    using: {
      tsearch: {
        prefix: true,
        dictionary: 'english'
      }
    }

  # Trigram similarity search
  pg_search_scope :fuzzy_search,
    against: [:title, :body],
    using: {
      trigram: { threshold: 0.3 }
    }
end

# Migration for indexes
class AddPgSearchIndexes < ActiveRecord::Migration[7.1]
  def up
    add_column :articles, :tsv, :tsvector
    add_index :articles, :tsv, using: :gin

    execute <<-SQL
      UPDATE articles
      SET tsv = to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))
    SQL

    # Trigger to keep it updated
    execute <<-SQL
      CREATE TRIGGER articles_tsv_update BEFORE INSERT OR UPDATE
      ON articles FOR EACH ROW EXECUTE FUNCTION
      tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);
    SQL

    # For trigram search
    enable_extension 'pg_trgm'
    add_index :articles, :title, using: :gin, opclass: :gin_trgm_ops
  end
end

# Usage
Article.search_full_text("rails tutorial")
Article.fuzzy_search("raails")  # Finds "rails"
Article.search_full_text("rails").with_pg_search_rank.order('pg_search_rank DESC')
```

---

## Advanced JSONB Queries

```ruby
# Model with JSONB
class Product < ApplicationRecord
  # Column: specifications (jsonb)

  # Using jsonb_accessor for typed access
  jsonb_accessor :specifications,
    color: :string,
    weight: :float,
    features: [:string, array: true]
end

# Query patterns
# Contains
Product.where("specifications @> ?", { color: 'red' }.to_json)

# Has key
Product.where("specifications ? 'warranty'")

# Array contains element
Product.where("specifications -> 'features' ? 'wireless'")

# Extract and compare
Product.where("specifications ->> 'color' = ?", 'red')
Product.where("(specifications ->> 'weight')::float > ?", 5.0)

# With indexes
add_index :products, :specifications, using: :gin
add_index :products, "(specifications -> 'color')", using: :btree

# Array queries
Product.where("specifications -> 'features' @> ?", ['wireless'].to_json)
```

---

## JSONB Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `->` | Get JSON object field | `data -> 'key'` |
| `->>` | Get JSON field as text | `data ->> 'key'` |
| `@>` | Contains | `data @> '{"key": "value"}'` |
| `?` | Key exists | `data ? 'key'` |
| `?|` | Any key exists | `data ?| array['a', 'b']` |
| `?&` | All keys exist | `data ?& array['a', 'b']` |
| `||` | Concatenate | `data || '{"new": "value"}'` |
| `-` | Delete key | `data - 'key'` |

---

## Array Columns

```ruby
# Migration
add_column :tasks, :tags, :string, array: true, default: []
add_index :tasks, :tags, using: :gin

# Queries
Task.where("'urgent' = ANY(tags)")
Task.where("tags @> ARRAY[?]::varchar[]", ['urgent', 'priority'])
Task.where("tags && ARRAY[?]::varchar[]", ['urgent', 'priority'])  # Overlap

# Array aggregate
Task.group(:merchant_id)
    .select("merchant_id, array_agg(DISTINCT status) as statuses")
```

---

## Range Types

```ruby
# Migration
add_column :reservations, :duration, :tstzrange  # timestamp range

# Model
class Reservation < ApplicationRecord
  validates :duration, presence: true
end

# Queries
# Contains value
Reservation.where("duration @> ?::timestamptz", Time.current)

# Overlaps range
Reservation.where("duration && tstzrange(?, ?)", start_time, end_time)

# Adjacent
Reservation.where("duration -|- tstzrange(?, ?)", start_time, end_time)
```

---

## UPSERT (Insert or Update)

```ruby
# Rails 7.0+
Task.upsert({ tracking_number: 'ABC123', status: 'pending' },
            unique_by: :tracking_number)

# Bulk upsert
Task.upsert_all([
  { tracking_number: 'ABC123', status: 'pending' },
  { tracking_number: 'DEF456', status: 'active' }
], unique_by: :tracking_number)

# With update columns
Task.upsert_all(records,
                unique_by: :tracking_number,
                update_only: [:status, :updated_at])
```

---

## Partial Indexes

```ruby
# Only index pending tasks (smaller index, faster queries)
add_index :tasks, :created_at, where: "status = 'pending'"

# Used automatically when query matches condition
Task.where(status: 'pending').order(:created_at)  # Uses partial index
```

---

## Window Functions

```ruby
# Rank tasks by amount within each merchant
Task.select(
  :id, :amount, :merchant_id,
  "RANK() OVER (PARTITION BY merchant_id ORDER BY amount DESC) as rank"
)

# Running total
Task.select(
  :id, :amount,
  "SUM(amount) OVER (ORDER BY created_at) as running_total"
)
```
