---
name: rails-resource
description: Generate complete Rails resources (model, controller, views, tests) following project patterns. Use when user requests creating models, adding features, scaffolding CRUD, or says "create/add/generate [model/resource/feature]", "build [system]", "new [feature] model".
---

# Rails Resource Generator

Generate complete Rails resources matching this project's established patterns.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Parse request and plan structure
- [ ] 2. Generate migration with indexes
- [ ] 3. Create model with validations/scopes
- [ ] 4. Create controller with auth
- [ ] 5. Generate views with Tailwind
- [ ] 6. Update routes
- [ ] 7. Create tests and fixtures
- [ ] 8. Add i18n translations
- [ ] 9. Run migration and verify
```

## Project Patterns

**Critical patterns from existing code**:
- Composite index: `[user_id, created_at]` for timeline queries
- N+1 prevention: Always `includes(:user)` in index actions
- Authorization: `@resource.user == current_user`
- Counter caches: `likes_count`, `comments_count`, `views_count`
- Enums: integer with `category_i18n` helper method
- Flash messages: Korean ("성공적으로 생성되었습니다")
- Query limits: `.limit(50)` for lists

**Reference existing code**:
- Models: [model-patterns.md](reference/model-patterns.md)
- Controllers: [controller-template.md](reference/controller-template.md)
- Views: [view-patterns.md](reference/view-patterns.md)
- Tests: [test-patterns.md](reference/test-patterns.md)
- Scripts: [generate_resource.rb](scripts/generate_resource.rb)

## Generation Workflow

### 1. Migration

```ruby
class CreateResourceNames < ActiveRecord::Migration[8.1]
  def change
    create_table :resource_names do |t|
      t.references :user, null: false, foreign_key: true
      t.string :title, null: false
      t.integer :status, default: 0, null: false
      t.integer :views_count, default: 0
      t.timestamps
    end

    add_index :resource_names, [:user_id, :created_at]  # Always add
    add_index :resource_names, :status                    # For enums
  end
end
```

**Key rules**:
- NOT NULL on required fields
- Default 0 for enums and counters
- Foreign key constraints
- Composite index for user timelines

### 2. Model

```ruby
class ResourceName < ApplicationRecord
  belongs_to :user

  enum status: { draft: 0, published: 1 }

  validates :title, presence: true, length: { maximum: 255 }

  scope :recent, -> { order(created_at: :desc) }
  scope :published, -> { where(status: :published) }

  def status_i18n
    I18n.t("activerecord.attributes.resource_name.statuses.#{status}")
  end
end
```

See [reference/model-patterns.md](reference/model-patterns.md) for full model patterns.

### 3. Controller

```ruby
class ResourceNamesController < ApplicationController
  before_action :require_login, except: [:index, :show]
  before_action :set_resource, only: [:show, :edit, :update, :destroy]
  before_action :authorize_user, only: [:edit, :update, :destroy]

  def index
    @resources = ResourceName.includes(:user).recent.limit(50)
  end

  def create
    @resource = current_user.resource_names.build(resource_params)
    if @resource.save
      redirect_to @resource, notice: '성공적으로 생성되었습니다.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def authorize_user
    redirect_to root_path unless @resource.user == current_user
  end
end
```

See [reference/controller-template.md](reference/controller-template.md) for complete controller template.

### 4. Views

Use Tailwind patterns from existing views:
- Card layout: `bg-card rounded-xl p-6 border`
- Forms: `space-y-6` with error handling
- Buttons: `bg-primary text-primary-foreground`

See [reference/view-patterns.md](reference/view-patterns.md) for complete view templates.

### 5. Tests

Generate for:
- Associations: `test "should belong to user"`
- Validations: `test "should validate presence of title"`
- Enums: `test "should transition statuses"`
- Controller auth: `test "should require login"`

See [reference/test-patterns.md](reference/test-patterns.md) for test patterns.

## After Generation

```bash
rails db:migrate
rails test
rubocop
rails server
```

Visit http://localhost:3000/resource_names

## Examples

**Basic resource**:
```
"Create Notification model with user:references, content:text, read_at:datetime"
→ Generates: migration, model, controller, views, tests
```

**Enum resource**:
```
"Add Event with category enum [workshop, meetup, conference]"
→ Includes: category integer, enum definition, category_i18n, i18n translations
```

**Polymorphic resource**:
```
"Create Vote for posts and comments"
→ Includes: votable_type, votable_id, polymorphic associations
```

## Common Mistakes to Avoid

❌ Forgetting composite index `[user_id, created_at]`
❌ Missing `includes(:user)` (N+1 queries)
❌ Not adding `authorize_user` check
❌ Using different Tailwind classes than existing views
❌ Skipping i18n for enums
❌ Not adding tests

## Checklist

- [ ] Migration has composite index
- [ ] Model has validations
- [ ] Controller has `includes(:user)`
- [ ] Controller has authorization
- [ ] Views use project Tailwind patterns
- [ ] Tests cover CRUD operations
- [ ] i18n added for enums
- [ ] `rails db:migrate` runs successfully
- [ ] `rails test` passes
- [ ] No rubocop violations
