---
name: rails-caching
description: Rails caching strategies including fragment caching, low-level caching with Rails.cache, cache keys, and conditional GET. Use when the user asks about caching performance or invalidation in Rails.
version: 1.0.0
---

# Rails Caching

Use Rails caching to reduce response time and database load while keeping
content fresh. This skill focuses on fragment caching, low-level caching,
cache keys, and conditional GETs.

## Fragment caching

Wrap view fragments that can be reused:
```erb
<% @products.each do |product| %>
  <% cache product do %>
    <%= render product %>
  <% end %>
<% end %>
```

Notes:
- Cache keys include a template digest; edits to the fragment invalidate it.
- Model versions (`cache_key_with_version`) help expire cached content when
  records change.

## Low-level caching with Rails.cache

Use `Rails.cache.fetch` for expensive computations:
```ruby
class Product < ApplicationRecord
  def competing_price
    Rails.cache.fetch("#{cache_key_with_version}/competing_price", expires_in: 12.hours) do
      Competitor::API.find_price(id)
    end
  end
end
```

Guidance:
- Prefer `fetch` to avoid separate read/write logic.
- Choose stable keys; use arrays/hashes when appropriate.
- Set `expires_in` for data that should age out.

## Cache keys

Objects should implement `cache_key` (Active Record provides it).
Keys can be arrays or hashes:
```ruby
Rails.cache.read(site: "mysite", owners: [owner_1, owner_2])
```

Notes:
- Storage backends may modify keys; don’t depend on backend-specific formats.

## Conditional GETs

Leverage ETags and `Last-Modified` to return `304 Not Modified`:
```ruby
class ProductsController < ApplicationController
  def show
    @product = Product.find(params[:id])
    if stale?(last_modified: @product.updated_at.utc, etag: @product.cache_key_with_version)
      # normal response rendering
    end
  end
end
```

## When to use this skill
- Cache expensive views or queries
- Decide between fragment and low-level caching
- Configure cache stores as needed
- Implement cache keys and conditional GETs
