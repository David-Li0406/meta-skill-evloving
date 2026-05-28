# Test Patterns

Minitest patterns for models, controllers, and fixtures.

## Model Test Template

```ruby
require "test_helper"

class ResourceNameTest < ActiveSupport::TestCase
  # Associations
  test "should belong to user" do
    resource = resource_names(:one)
    assert_instance_of User, resource.user
  end

  # Validations
  test "should validate presence of title" do
    resource = ResourceName.new(user: users(:one))
    assert_not resource.valid?
    assert_includes resource.errors[:title], "can't be blank"
  end

  test "should validate title length" do
    resource = ResourceName.new(user: users(:one), title: "a" * 256)
    assert_not resource.valid?
  end

  # Enums
  test "should have status enum" do
    resource = resource_names(:one)
    resource.draft!
    assert resource.draft?

    resource.published!
    assert resource.published?
  end

  # Scopes
  test "recent scope should order by created_at desc" do
    resources = ResourceName.recent.to_a
    assert resources.first.created_at >= resources.last.created_at
  end
end
```

## Controller Test Template

```ruby
require "test_helper"

class ResourceNamesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @resource = resource_names(:one)
    @user = users(:one)
  end

  test "should get index" do
    get resource_names_path
    assert_response :success
  end

  test "should redirect to login for new when not logged in" do
    get new_resource_name_path
    assert_redirected_to login_path
  end

  test "should create when valid" do
    log_in_as @user

    assert_difference('ResourceName.count', 1) do
      post resource_names_path, params: {
        resource_name: { title: "Test", content: "Content" }
      }
    end

    assert_redirected_to resource_name_path(ResourceName.last)
  end

  test "should not update when unauthorized" do
    log_in_as users(:two)
    patch resource_name_path(@resource), params: {
      resource_name: { title: "Hacked" }
    }

    assert_redirected_to root_path
    assert_not_equal "Hacked", @resource.reload.title
  end
end
```

## Fixture Template

```yaml
one:
  user: one
  title: "First Resource"
  content: "Content here"
  status: 1
  views_count: 10
  created_at: <%= 1.day.ago %>

two:
  user: two
  title: "Second Resource"
  content: "More content"
  status: 0
  views_count: 0
  created_at: <%= 2.hours.ago %>
```

## Test Helper Methods

Add to test/test_helper.rb:

```ruby
def log_in_as(user)
  session[:user_id] = user.id
end
```
