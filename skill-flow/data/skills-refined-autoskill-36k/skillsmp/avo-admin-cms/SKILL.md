---
name: avo-admin-cms
description: Guidance for working with the Avo admin CMS. Use when creating or updating Avo resources, dashboards, actions, filters, or any other Avo-related functionality.
---

# Avo Admin CMS

## Guidelines

- Full LLM docs for Avo: `#fetch https://docs.avohq.io/3.0/llms-full.txt`.

## Adding Resources

Use this as the baseline structure for a new Avo resource:

```ruby
# frozen_string_literal: true

class Avo::Resources::NewResource < Avo::BaseResource
  def fields
    field :id
    [more fields here]
    timestamp_fields
    field :tasks
  end

  _baseline_finalize
end
```

Always add a matching controller file as well:

```ruby
# frozen_string_literal: true

class Avo::NewResourcesController < Avo::ResourcesController
end
```

## Fields

Fields can be added without specifying a type via the `:as` parameter:

```ruby
field :name
field :pdf_file
field :processed_at
```

If no `:as` parameter is present, the type and default attributes are determined automatically. See `Baseline::ActsAsAvoResource#field` in Baseline for details.
