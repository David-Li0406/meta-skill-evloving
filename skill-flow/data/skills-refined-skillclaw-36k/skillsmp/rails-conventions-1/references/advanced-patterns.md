# Advanced Rails Patterns

## Service Objects

Service objects encapsulate complex business operations that don't belong in models or controllers.

### When to Use

- Operation involves multiple models
- Complex business logic with many steps
- External API interactions
- Operations that need transaction handling
- Logic that's hard to test in controllers

### Pattern

```ruby
# app/services/users/registration_service.rb
module Users
  class RegistrationService
    Result = Struct.new(:success?, :user, :errors, keyword_init: true)

    def initialize(params, invited_by: nil)
      @params = params
      @invited_by = invited_by
    end

    def call
      user = User.new(@params)

      ActiveRecord::Base.transaction do
        user.save!
        create_default_settings(user)
        send_welcome_email(user)
        credit_referrer(user) if @invited_by
      end

      Result.new(success?: true, user: user)
    rescue ActiveRecord::RecordInvalid => e
      Result.new(success?: false, user: user, errors: user.errors)
    end

    private

    def create_default_settings(user)
      user.create_settings!(notification_frequency: "daily")
    end

    def send_welcome_email(user)
      UserMailer.welcome(user).deliver_later
    end

    def credit_referrer(user)
      @invited_by.credits.create!(amount: 10, reason: "referral")
    end
  end
end

# Usage in controller
result = Users::RegistrationService.new(user_params).call
if result.success?
  redirect_to dashboard_path
else
  @user = result.user
  render :new
end
```

## Query Objects

Encapsulate complex database queries for reusability and testing.

```ruby
# app/queries/articles/search_query.rb
module Articles
  class SearchQuery
    def initialize(relation = Article.all)
      @relation = relation
    end

    def call(params)
      @relation
        .then { |r| filter_by_status(r, params[:status]) }
        .then { |r| filter_by_author(r, params[:author_id]) }
        .then { |r| filter_by_date_range(r, params[:from], params[:to]) }
        .then { |r| search_text(r, params[:q]) }
        .then { |r| apply_sorting(r, params[:sort]) }
    end

    private

    def filter_by_status(relation, status)
      return relation if status.blank?
      relation.where(status: status)
    end

    def filter_by_author(relation, author_id)
      return relation if author_id.blank?
      relation.where(author_id: author_id)
    end

    def filter_by_date_range(relation, from, to)
      relation = relation.where("created_at >= ?", from) if from.present?
      relation = relation.where("created_at <= ?", to) if to.present?
      relation
    end

    def search_text(relation, query)
      return relation if query.blank?
      relation.where("title ILIKE :q OR body ILIKE :q", q: "%#{query}%")
    end

    def apply_sorting(relation, sort)
      case sort
      when "oldest" then relation.order(created_at: :asc)
      when "title" then relation.order(title: :asc)
      else relation.order(created_at: :desc)
      end
    end
  end
end

# Usage
@articles = Articles::SearchQuery.new.call(params.permit(:status, :author_id, :q, :sort))
```

## Form Objects

Handle complex forms that span multiple models or need custom validation.

```ruby
# app/forms/registration_form.rb
class RegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :password, :string
  attribute :password_confirmation, :string
  attribute :company_name, :string
  attribute :terms_accepted, :boolean

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :company_name, presence: true
  validates :terms_accepted, acceptance: true
  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      @user = User.create!(email: email, password: password)
      @company = Company.create!(name: company_name, owner: @user)
      @user.update!(company: @company)
    end

    true
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end

  attr_reader :user, :company

  private

  def passwords_match
    return if password == password_confirmation
    errors.add(:password_confirmation, "doesn't match password")
  end
end

# In controller
def create
  @form = RegistrationForm.new(registration_params)
  if @form.save
    sign_in(@form.user)
    redirect_to dashboard_path
  else
    render :new
  end
end
```

## Presenter/Decorator Pattern

Add view-specific logic without polluting models.

```ruby
# app/presenters/article_presenter.rb
class ArticlePresenter < SimpleDelegator
  def initialize(article, view_context)
    super(article)
    @view = view_context
  end

  def formatted_date
    created_at.strftime("%B %d, %Y")
  end

  def status_badge
    css_class = case status
                when "published" then "bg-green-100 text-green-800"
                when "draft" then "bg-yellow-100 text-yellow-800"
                else "bg-gray-100 text-gray-800"
                end

    @view.content_tag(:span, status.titleize, class: "px-2 py-1 rounded #{css_class}")
  end

  def truncated_body(length: 200)
    @view.truncate(body, length: length)
  end

  def author_link
    @view.link_to(author.name, @view.user_path(author))
  end
end

# In view
<% presenter = ArticlePresenter.new(@article, self) %>
<%= presenter.status_badge %>
<%= presenter.formatted_date %>
```

## Policy Objects

Encapsulate authorization logic (alternative to Pundit/CanCanCan for simple cases).

```ruby
# app/policies/article_policy.rb
class ArticlePolicy
  def initialize(user, article)
    @user = user
    @article = article
  end

  def show?
    @article.published? || owner_or_admin?
  end

  def update?
    owner_or_admin?
  end

  def destroy?
    owner_or_admin?
  end

  def publish?
    owner_or_admin? && @article.draft?
  end

  private

  def owner_or_admin?
    @user&.admin? || @article.author == @user
  end
end

# Usage
policy = ArticlePolicy.new(current_user, @article)
redirect_to root_path unless policy.show?
```

## Value Objects

Encapsulate domain concepts that are defined by their attributes.

```ruby
# app/models/money.rb
class Money
  include Comparable

  attr_reader :amount_cents, :currency

  def initialize(amount_cents, currency = "USD")
    @amount_cents = amount_cents.to_i
    @currency = currency.to_s.upcase
  end

  def amount
    amount_cents / 100.0
  end

  def to_s
    format("%.2f %s", amount, currency)
  end

  def +(other)
    raise ArgumentError, "Currency mismatch" unless currency == other.currency
    Money.new(amount_cents + other.amount_cents, currency)
  end

  def <=>(other)
    return nil unless currency == other.currency
    amount_cents <=> other.amount_cents
  end

  def self.from_amount(amount, currency = "USD")
    new((amount.to_f * 100).round, currency)
  end
end

# Usage
price = Money.from_amount(29.99)
tax = Money.from_amount(2.40)
total = price + tax
```

## Null Object Pattern

Avoid nil checks with null objects.

```ruby
# app/models/guest_user.rb
class GuestUser
  def name
    "Guest"
  end

  def email
    nil
  end

  def admin?
    false
  end

  def can_comment?
    false
  end

  def persisted?
    false
  end
end

# In ApplicationController
def current_user
  @current_user ||= User.find_by(id: session[:user_id]) || GuestUser.new
end

# Now safe to call methods without nil checks
current_user.name  # Works for both User and GuestUser
```
