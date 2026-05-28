---
name: test-gen
description: Generate comprehensive Minitest suites for Rails models and controllers. Use when user wants to add tests, improve coverage, fill empty test files, or says "test [model/controller]", "add tests", "write tests for", "test coverage", "generate tests".
---

# Test Generator

Fill empty test files with comprehensive Minitest suites based on existing code.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Analyze model/controller code
- [ ] 2. Generate association tests
- [ ] 3. Generate validation tests
- [ ] 4. Generate enum/scope tests
- [ ] 5. Generate controller CRUD tests
- [ ] 6. Create realistic fixtures
- [ ] 7. Add test helpers
- [ ] 8. Run tests and verify
```

## Current State

**All test files are empty stubs**. This skill transforms them into working test suites.

```ruby
# Current state
class UserTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
```

## Generation Strategy

1. **Read the model/controller** to identify:
   - Associations
   - Validations
   - Enums
   - Scopes
   - Instance methods
   - Controller actions

2. **Generate tests** for each element found

3. **Create fixtures** with valid, realistic data

4. **Run tests** to verify they pass

## Test Patterns

See detailed examples:
- Models: [examples/model_tests.md](examples/model_tests.md)
- Controllers: [examples/controller_tests.md](examples/controller_tests.md)
- Fixtures: [examples/fixture-patterns.md](examples/fixture-patterns.md)
- Scripts: [run_tests.sh](scripts/run_tests.sh), [generate_fixtures.rb](scripts/generate_fixtures.rb)

## Quick Examples

**Association test**:
```ruby
test "should belong to user" do
  post = posts(:one)
  assert_instance_of User, post.user
end
```

**Validation test**:
```ruby
test "should validate presence of title" do
  post = Post.new
  assert_not post.valid?
  assert_includes post.errors[:title], "can't be blank"
end
```

**Enum test**:
```ruby
test "should transition between statuses" do
  post = posts(:one)
  post.draft!
  assert post.draft?

  post.published!
  assert post.published?
end
```

**Controller authorization test**:
```ruby
test "should not update when unauthorized" do
  log_in_as users(:two)
  patch post_path(@post), params: { post: { title: "Hacked" } }

  assert_redirected_to root_path
  assert_not_equal "Hacked", @post.reload.title
end
```

## Fixture Pattern

```yaml
one:
  user: one
  email: user1@example.com
  password_digest: <%= BCrypt::Password.create('password', cost: 4) %>
  name: Test User One
  created_at: <%= 2.days.ago %>
```

Key points:
- BCrypt cost 4 for faster tests
- Valid associations
- Realistic data
- Proper timestamps

## Test Helper

Add to `test/test_helper.rb`:

```ruby
def log_in_as(user)
  session[:user_id] = user.id
end
```

## Coverage Goals

- **Core models** (User, Post): 90%+
- **Feature models** (JobPost, Comment): 85%+
- **Simple models** (Like, Bookmark): 80%+

## After Generation

```bash
# Run all tests
rails test

# Run specific file
rails test test/models/user_test.rb

# With coverage (if SimpleCov installed)
COVERAGE=true rails test
```

## Common Test Types

**For models**:
- Associations
- Validations (presence, format, uniqueness, length)
- Enums (transitions, i18n)
- Scopes (ordering, filtering)
- Instance methods
- Counter caches

**For controllers**:
- Index (public access)
- Show (public access, view increment)
- New/Create (require login, authorization)
- Edit/Update/Destroy (require ownership)
- Invalid data handling
- Flash messages

## Project Patterns

From existing codebase:
- Use **Minitest** (not RSpec)
- Use **Fixtures** (not FactoryBot)
- Flash messages in **Korean**
- Auth via `session[:user_id]`
- BCrypt cost 4 in fixtures
- `ActiveSupport::TestCase` for models
- `ActionDispatch::IntegrationTest` for controllers

## Checklist

- [ ] All associations tested
- [ ] All validations tested (valid + invalid cases)
- [ ] Enum transitions tested
- [ ] Scopes tested
- [ ] Controller auth tested
- [ ] CRUD operations tested
- [ ] Fixtures have realistic data
- [ ] Test helper methods added
- [ ] All tests pass
- [ ] Coverage >= 80%
