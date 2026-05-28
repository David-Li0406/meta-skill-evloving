---
id: ruby-activerecord
name: "ActiveRecord Patterns"
domain: RUBY
skill: faion-software-developer
category: "backend"
---

## ActiveRecord Patterns

### Problem
Efficient database access with proper query optimization.

### Framework: Query Objects

```ruby
# app/queries/users_query.rb
class UsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def active
    @relation = @relation.where(active: true)
    self
  end

  def with_role(role)
    @relation = @relation.where(role: role)
    self
  end

  def created_after(date)
    @relation = @relation.where('created_at > ?', date)
    self
  end

  def search(term)
    return self if term.blank?
    @relation = @relation.where(
      'name ILIKE :term OR email ILIKE :term',
      term: "%#{term}%"
    )
    self
  end

  def ordered
    @relation = @relation.order(created_at: :desc)
    self
  end

  def with_associations
    @relation = @relation.includes(:profile, :roles)
    self
  end

  def paginate(page:, per_page: 20)
    @relation = @relation.page(page).per(per_page)
    self
  end

  def results
    @relation
  end
end

# Usage
users = UsersQuery.new
  .active
  .with_role('admin')
  .search(params[:q])
  .with_associations
  .ordered
  .paginate(page: params[:page])
  .results
```

### Scopes and Callbacks

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Associations
  has_one :profile, dependent: :destroy
  has_many :orders, dependent: :nullify
  has_many :roles, through: :user_roles

  # Validations
  validates :email, presence: true, uniqueness: { case_sensitive: false }
  validates :name, presence: true, length: { minimum: 2, maximum: 100 }

  # Scopes
  scope :active, -> { where(active: true) }
  scope :admins, -> { joins(:roles).where(roles: { name: 'admin' }) }
  scope :recent, -> { where('created_at > ?', 30.days.ago) }

  # Callbacks
  before_validation :normalize_email
  after_create_commit :send_welcome_email

  private

  def normalize_email
    self.email = email&.downcase&.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end
end
```

### Agent

faion-backend-agent
