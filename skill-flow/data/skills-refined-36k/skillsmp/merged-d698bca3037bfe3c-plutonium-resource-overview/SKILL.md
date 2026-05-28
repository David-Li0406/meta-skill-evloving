---
name: plutonium-resource-overview
description: Use this skill when you need to understand the structure, setup, and best practices for Plutonium resource models and definitions.
---

# Plutonium Resource Overview

This document provides an overview of Plutonium resource models and definitions, detailing their structure, setup, and best practices for effective use in applications.

## Plutonium Resource Models

A model becomes a Plutonium resource by including `Plutonium::Resource::Record`, which enhances ActiveRecord functionality for routing, labeling, field introspection, associations, and monetary handling.

### Setup

#### Standard Setup

```ruby
# app/models/application_record.rb
class ApplicationRecord < ActiveRecord::Base
  include Plutonium::Resource::Record
  primary_abstract_class
end

# app/models/resource_record.rb (optional abstract class)
class ResourceRecord < ApplicationRecord
  self.abstract_class = true
end

# app/models/property.rb
class Property < ResourceRecord
  # Now has access to all Plutonium features
end
```

### What's Included

`Plutonium::Resource::Record` includes six modules:

| Module | Purpose |
|--------|---------|
| `HasCents` | Monetary value handling (cents → decimal) |
| `Routes` | URL parameters, path customization |
| `Labeling` | Human-readable `to_label` method |
| `FieldNames` | Field introspection and categorization |
| `Associations` | SGID support for secure serialization |
| `AssociatedWith` | Entity scoping for multi-tenant apps |

### Model Structure

Follow the template structure (comment markers indicate where to add code):

```ruby
class Property < ResourceRecord
  # add concerns above.

  TYPES = {apartment: "Apartment", house: "House"}.freeze
  # add constants above.

  enum :state, archived: 0, active: 1
  enum :property_class, residential: 0, commercial: 1
  # add enums above.

  has_cents :market_value_cents
  # add model configurations above.

  belongs_to :company
  # add belongs_to associations above.

  has_one :address
  # add has_one associations above.

  has_many :units
  has_many :amenities, class_name: "PropertyAmenity"
  # add has_many associations above.

  has_one_attached :photo
  has_many_attached :documents
  # add attachments above.

  scope :active, -> { where(state: :active) }
  scope :by_company, ->(company) { where(company: company) }
  # add scopes above.

  validates :name, presence: true
  validates :property_code, presence: true, uniqueness: {scope: :company_id}
  # add validations above.

  before_validation :generate_code, on: :create
  # add callbacks above.

  delegate :name, to: :company, prefix: true
  # add delegations above.

  has_rich_text :description
  # add misc attribute macros above.

  def full_address
    address&.to_s
  end

  # add methods above. add private methods below.

  private

  def generate_code
    self.property_code ||= SecureRandom.hex(4).upcase
  end
end
```

### Common Patterns

#### Archiving (State-Based)

```ruby
class Property < ResourceRecord
  enum :state, archived: 0, active: 1

  scope :active, -> { where(state: :active) }
  scope :archived, -> { where(state: :archived) }

  def archive!
    update!(state: :archived)
  end

  def restore!
    update!(state: :active)
  end
end
```

#### Multi-Tenant Scoping

```ruby
class Property < ResourceRecord
  belongs_to :company

  # Compound uniqueness for multi-tenant
  validates :property_code, uniqueness: {scope: :company_id}

  # Custom scope for entity scoping
  scope :associated_with_company, ->(company) { where(company: company) }
end
```

## Plutonium Resource Definitions

Resource definitions configure **HOW** resources are rendered and interacted with, serving as the central configuration point for UI behavior in Plutonium applications.

### Key Principle

**All model attributes are auto-detected** - you only declare when overriding defaults.

### File Location

- Main app: `app/definitions/model_name_definition.rb`
- Packages: `packages/pkg_name/app/definitions/pkg_name/model_name_definition.rb`

### Definition Structure

```ruby
class PostDefinition < Plutonium::Resource::Definition
  # Fields, inputs, displays, columns
  field :content, as: :markdown
  input :title, hint: "Be descriptive"
  display :content, as: :markdown
  column :title, align: :center

  # Search, filters, scopes, sorting
  search { |scope, q| scope.where("title ILIKE ?", "%#{q}%") }
  filter :status, with: Plutonium::Query::Filters::Text, predicate: :eq
  scope :published
  sort :created_at

  # Actions
  action :publish, interaction: PublishInteraction
end
```

### Definition Hierarchy

Definitions exist at multiple levels:

#### Main App (created by generators)

```ruby
# app/definitions/resource_definition.rb (base - created during install)
class ResourceDefinition < Plutonium::Resource::Definition
  action :archive, interaction: ArchiveInteraction, color: :danger, position: 1000
end

# app/definitions/post_definition.rb (resource-specific - created by scaffold)
class PostDefinition < ResourceDefinition
  scope :published
  input :content, as: :markdown
end
```

#### Portal-Specific Overrides

After connecting a resource to a portal, you can create a portal-specific definition to override defaults for that portal only:

```ruby
# packages/admin_portal/app/definitions/admin_portal/post_definition.rb
class AdminPortal::PostDefinition < ::PostDefinition
  # Override or extend for admin portal only
  input :internal_notes, as: :text  # Only admins see this field
  scope :pending_review             # Admin-specific scope
end
```

### Auto-Detection

Plutonium automatically detects from your model:
- Database columns (string, text, integer, boolean, datetime, etc.)
- Associations (belongs_to, has_many, has_one)
- Active Storage/Active Shrine attachments (has_one_attached, has_many_attached)
- Enums
- Virtual attributes (with accessor methods)

**Only declare fields when you need to override the auto-detected behavior.**

### Best Practices

1. **Use enums for state** - `enum :state, archived: 0, active: 1` instead of soft-delete.
2. **Compound uniqueness** - Always scope uniqueness to tenant/parent.
3. **Organize with comments** - Use section headers for readability.
4. **Keep models focused** - Business logic in interactions, not models.
5. **Validate at boundaries** - Validate user input, trust internal code.
6. **Use scopes** - Define commonly used queries as scopes.

## Related Skills

- `plutonium-model-features` - has_cents, associations, scopes, routes
- `plutonium-create-resource` - Scaffold generator for new resources
- `plutonium-definition-fields` - Fields, inputs, displays, columns
- `plutonium-definition-actions` - Actions and interactions
- `plutonium-definition-query` - Search, filters, scopes, sorting
- `plutonium-views` - Custom page, form, display, and table classes