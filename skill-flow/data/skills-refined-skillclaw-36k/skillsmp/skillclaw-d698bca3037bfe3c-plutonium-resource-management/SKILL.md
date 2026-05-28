---
name: plutonium-resource-management
description: Use this skill when you need to define and manage resource models and their interactions in a Plutonium application.
---

# Skill body

## Overview

This skill provides guidance on setting up and managing resource models and their definitions in a Plutonium application. It covers the structure, setup, and best practices for both resource models and their UI definitions.

## Resource Model Setup

A model becomes a Plutonium resource by including `Plutonium::Resource::Record`. This provides enhanced ActiveRecord functionality for routing, labeling, field introspection, associations, and monetary handling.

### Standard Setup

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

`Plutonium::Resource::Record` includes several modules for various functionalities:

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
    address
  end
end
```

## Resource Definition Overview

Resource definitions configure **HOW** resources are rendered and interacted with. They are the central configuration point for UI behavior in Plutonium applications.

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

This allows for customization of fields, actions, and behaviors per portal while keeping the main app definition clean.