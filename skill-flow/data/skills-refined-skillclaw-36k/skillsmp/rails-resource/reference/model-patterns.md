# Model Patterns

Complete model patterns from existing codebase (User, Post, JobPost).

## Association Patterns

```ruby
# belongs_to (always)
belongs_to :user

# has_many with dependent destroy
has_many :comments, dependent: :destroy
has_many :likes, as: :likeable, dependent: :destroy

# Polymorphic
belongs_to :likeable, polymorphic: true
```

## Validation Patterns

```ruby
# String fields
validates :title, presence: true, length: { minimum: 1, maximum: 255 }
validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }, uniqueness: true

# Text fields
validates :content, presence: true, length: { minimum: 1 }

# Enums
validates :status, presence: true
validates :category, presence: true
```

## Enum Patterns

```ruby
enum status: {
  draft: 0,
  published: 1,
  archived: 2
}

enum category: {
  development: 0,
  design: 1,
  pm: 2,
  marketing: 3
}

# i18n helper
def status_i18n
  I18n.t("activerecord.attributes.#{self.class.name.underscore}.statuses.#{status}")
end

def category_i18n
  I18n.t("activerecord.attributes.#{self.class.name.underscore}.categories.#{category}")
end
```

## Scope Patterns

```ruby
scope :recent, -> { order(created_at: :desc) }
scope :published, -> { where(status: :published) }
scope :draft, -> { where(status: :draft) }
scope :by_category, ->(cat) { where(category: cat) if cat.present? }
scope :by_user, ->(user) { where(user: user) }
```

## Instance Method Patterns

```ruby
# View counter
def increment_views!
  increment!(:views_count)
end

# Status checkers (enums provide these automatically)
def published?
  status == 'published'
end
```

## Counter Cache Pattern

```ruby
# In parent model (Post)
has_many :comments, dependent: :destroy
has_many :likes, as: :likeable, dependent: :destroy

# In child model (Comment)
belongs_to :post, counter_cache: true

# Migration adds:
t.integer :comments_count, default: 0
t.integer :likes_count, default: 0
```

## Polymorphic Pattern

```ruby
# Likeable model (Post, Comment)
has_many :likes, as: :likeable, dependent: :destroy

# Like model
belongs_to :likeable, polymorphic: true
belongs_to :user

# Validation
validates :user_id, uniqueness: { scope: [:likeable_type, :likeable_id] }

# Migration
t.references :likeable, polymorphic: true, null: false
add_index :likes, [:likeable_type, :likeable_id]
add_index :likes, [:user_id, :likeable_type, :likeable_id], unique: true
```
