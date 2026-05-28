# GraphQL Patterns for Rails

Detailed patterns for building GraphQL APIs with graphql-ruby.

## Schema Organization

```
app/graphql/
├── my_app_schema.rb           # Main schema file
├── types/
│   ├── base_object.rb         # Base type class
│   ├── base_input_object.rb
│   ├── base_enum.rb
│   ├── query_type.rb          # Root query type
│   ├── mutation_type.rb       # Root mutation type
│   ├── user_type.rb
│   └── post_type.rb
├── mutations/
│   ├── base_mutation.rb
│   ├── create_post.rb
│   └── update_post.rb
├── resolvers/
│   └── posts_resolver.rb
└── sources/
    └── record_loader.rb
```

## Type Definitions

### Object Types

```ruby
# app/graphql/types/post_type.rb
module Types
  class PostType < Types::BaseObject
    description "A blog post"

    field :id, ID, null: false
    field :title, String, null: false
    field :content, String, null: false
    field :published, Boolean, null: false
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false

    # Association
    field :author, Types::UserType, null: false

    # Computed field
    field :excerpt, String, null: false

    def excerpt
      object.content.truncate(200)
    end

    # Batched association to prevent N+1
    def author
      dataloader.with(Sources::RecordLoader, User).load(object.user_id)
    end
  end
end
```

### Input Types

```ruby
# app/graphql/types/post_input_type.rb
module Types
  class PostInputType < Types::BaseInputObject
    argument :title, String, required: true
    argument :content, String, required: true
    argument :published, Boolean, required: false, default_value: false
  end
end
```

### Enum Types

```ruby
# app/graphql/types/post_status_enum.rb
module Types
  class PostStatusEnum < Types::BaseEnum
    value "DRAFT", "Not yet published", value: "draft"
    value "PUBLISHED", "Publicly visible", value: "published"
    value "ARCHIVED", "No longer active", value: "archived"
  end
end
```

## Query Type

```ruby
# app/graphql/types/query_type.rb
module Types
  class QueryType < Types::BaseObject
    # Single record
    field :user, Types::UserType, null: true do
      argument :id, ID, required: true
    end

    # Collection with pagination
    field :posts, Types::PostType.connection_type, null: false do
      argument :status, Types::PostStatusEnum, required: false
      argument :author_id, ID, required: false
    end

    def user(id:)
      User.find_by(id: id)
    end

    def posts(status: nil, author_id: nil)
      scope = Post.all
      scope = scope.where(status: status) if status
      scope = scope.where(author_id: author_id) if author_id
      scope.order(created_at: :desc)
    end
  end
end
```

## Mutations

### Base Mutation

```ruby
# app/graphql/mutations/base_mutation.rb
module Mutations
  class BaseMutation < GraphQL::Schema::RelayClassicMutation
    argument_class Types::BaseArgument
    field_class Types::BaseField
    input_object_class Types::BaseInputObject
    object_class Types::BaseObject

    def current_user
      context[:current_user]
    end

    def authenticate!
      raise GraphQL::ExecutionError, "Authentication required" unless current_user
    end

    def authorize!(record, action)
      policy = Pundit.policy!(current_user, record)
      unless policy.public_send("#{action}?")
        raise GraphQL::ExecutionError, "Not authorized"
      end
    end
  end
end
```

### CRUD Mutations

```ruby
# app/graphql/mutations/create_post.rb
module Mutations
  class CreatePost < BaseMutation
    argument :input, Types::PostInputType, required: true

    field :post, Types::PostType
    field :errors, [Types::UserErrorType], null: false

    def resolve(input:)
      authenticate!

      post = current_user.posts.build(input.to_h)

      if post.save
        { post: post, errors: [] }
      else
        { post: nil, errors: user_errors(post) }
      end
    end

    private

    def user_errors(record)
      record.errors.map do |error|
        { field: error.attribute.to_s.camelize(:lower), message: error.message }
      end
    end
  end
end

# app/graphql/mutations/update_post.rb
module Mutations
  class UpdatePost < BaseMutation
    argument :id, ID, required: true
    argument :input, Types::PostInputType, required: true

    field :post, Types::PostType
    field :errors, [Types::UserErrorType], null: false

    def resolve(id:, input:)
      authenticate!
      post = Post.find(id)
      authorize!(post, :update)

      if post.update(input.to_h)
        { post: post, errors: [] }
      else
        { post: nil, errors: user_errors(post) }
      end
    end
  end
end

# app/graphql/mutations/delete_post.rb
module Mutations
  class DeletePost < BaseMutation
    argument :id, ID, required: true

    field :success, Boolean, null: false
    field :errors, [String], null: false

    def resolve(id:)
      authenticate!
      post = Post.find(id)
      authorize!(post, :destroy)

      if post.destroy
        { success: true, errors: [] }
      else
        { success: false, errors: ["Failed to delete post"] }
      end
    end
  end
end
```

## DataLoader for N+1 Prevention

### Basic Record Loader

```ruby
# app/graphql/sources/record_loader.rb
class Sources::RecordLoader < GraphQL::Dataloader::Source
  def initialize(model_class, column: :id)
    @model_class = model_class
    @column = column
  end

  def fetch(ids)
    records = @model_class.where(@column => ids).index_by { |r| r.send(@column) }
    ids.map { |id| records[id] }
  end
end

# Usage
def author
  dataloader.with(Sources::RecordLoader, User).load(object.user_id)
end
```

### Association Loader

```ruby
# app/graphql/sources/association_loader.rb
class Sources::AssociationLoader < GraphQL::Dataloader::Source
  def initialize(model_class, association_name)
    @model_class = model_class
    @association_name = association_name
  end

  def fetch(records)
    ActiveRecord::Associations::Preloader.new(
      records: records,
      associations: @association_name
    ).call

    records.map { |record| record.public_send(@association_name) }
  end
end

# Usage
def comments
  dataloader.with(Sources::AssociationLoader, Post, :comments).load(object)
end
```

### Count Loader

```ruby
# app/graphql/sources/count_loader.rb
class Sources::CountLoader < GraphQL::Dataloader::Source
  def initialize(model_class, foreign_key)
    @model_class = model_class
    @foreign_key = foreign_key
  end

  def fetch(ids)
    counts = @model_class
      .where(@foreign_key => ids)
      .group(@foreign_key)
      .count

    ids.map { |id| counts[id] || 0 }
  end
end

# Usage
def comments_count
  dataloader.with(Sources::CountLoader, Comment, :post_id).load(object.id)
end
```

## Connections (Pagination)

```ruby
# app/graphql/types/query_type.rb
field :posts, Types::PostType.connection_type, null: false do
  argument :order_by, Types::PostOrderEnum, required: false
end

def posts(order_by: nil)
  scope = Post.published
  scope = scope.order(order_by) if order_by
  scope
end
```

### Custom Connection

```ruby
# app/graphql/types/post_connection_type.rb
module Types
  class PostConnectionType < GraphQL::Types::Connection
    edge_type(Types::PostEdgeType)

    field :total_count, Integer, null: false

    def total_count
      object.items.size
    end
  end
end
```

## Authentication & Authorization

### Context Setup

```ruby
# app/controllers/graphql_controller.rb
class GraphqlController < ApplicationController
  skip_before_action :verify_authenticity_token

  def execute
    result = MyAppSchema.execute(
      params[:query],
      variables: prepare_variables(params[:variables]),
      context: {
        current_user: current_user,
        request: request
      },
      operation_name: params[:operationName]
    )
    render json: result
  rescue StandardError => e
    handle_error(e)
  end

  private

  def current_user
    return nil unless auth_header.present?

    token = auth_header.split(' ').last
    User.find_by(api_token: token)
  end

  def auth_header
    request.headers['Authorization']
  end
end
```

### Field-Level Authorization

```ruby
module Types
  class UserType < Types::BaseObject
    field :email, String, null: false

    # Only visible to the user themselves
    field :private_notes, String do
      authorize :read_private
    end

    def self.authorized?(object, context)
      # Type-level authorization
      context[:current_user].present?
    end
  end
end
```

## Subscriptions

```ruby
# app/graphql/types/subscription_type.rb
module Types
  class SubscriptionType < Types::BaseObject
    field :post_created, Types::PostType, null: false do
      argument :author_id, ID, required: false
    end

    def post_created(author_id: nil)
      return object unless author_id
      object if object.author_id.to_s == author_id
    end
  end
end

# Trigger from model
class Post < ApplicationRecord
  after_create_commit :notify_subscribers

  private

  def notify_subscribers
    MyAppSchema.subscriptions.trigger(:post_created, {}, self)
  end
end
```

## Error Handling

### User Error Type

```ruby
# app/graphql/types/user_error_type.rb
module Types
  class UserErrorType < Types::BaseObject
    field :field, String, description: "Field with error"
    field :message, String, null: false, description: "Error message"
  end
end
```

### Execution Errors

```ruby
# Raise to halt execution
raise GraphQL::ExecutionError, "Not found"

# Add to errors without halting
context.add_error(GraphQL::ExecutionError.new("Warning: rate limited"))
```

## Query Complexity

```ruby
# app/graphql/my_app_schema.rb
class MyAppSchema < GraphQL::Schema
  max_complexity 300
  max_depth 15

  # Custom complexity per field
  field :expensive_field, String do
    complexity 50
  end
end
```

## Testing

```ruby
RSpec.describe Types::QueryType do
  let(:user) { create(:user) }
  let(:context) { { current_user: user } }

  describe 'posts query' do
    let(:query) do
      <<~GQL
        query($status: PostStatus) {
          posts(status: $status) {
            nodes {
              id
              title
            }
            totalCount
          }
        }
      GQL
    end

    it 'returns published posts' do
      create_list(:post, 3, :published)

      result = MyAppSchema.execute(query, context: context, variables: { status: "PUBLISHED" })

      expect(result['data']['posts']['totalCount']).to eq(3)
      expect(result['errors']).to be_nil
    end
  end
end
```
